function run_glaucohome_pipeline(frontPath, sidePath, fundusPath, patientJsonPath, outputDir)
% RUN_GLAUCOHOME_PIPELINE
% Main execution entrypoint for GlaucoHome Tri-Modal Screening.
% Invoked via batch command or Python API:
%   matlab -batch "run_glaucohome_pipeline('front.jpg', 'side.jpg', 'fundus.jpg', 'patient.json', 'out')"

    fprintf('========================================================\n');
    fprintf('  GLAUCOHOME: TRI-MODAL GLAUCOMA SCREENING PIPELINE\n');
    fprintf('========================================================\n');

    if ~exist(outputDir, 'dir'), mkdir(outputDir); end

    % 1. Patient Profile
    patientInfo = struct('age', 52, 'diabetes', 0, 'hypertension', 0, ...
                         'familyHistory', 0, 'myopia', 0, 'steroidUse', 0);
    if exist(patientJsonPath, 'file')
        rawText = fileread(patientJsonPath);
        patientInfo = jsondecode(rawText);
        fprintf('[+] Patient Profile Loaded from %s\n', patientJsonPath);
    end

    % 2. Front Eye Processing
    if ~isempty(frontPath) && exist(frontPath, 'file')
        fprintf('[+] Analyzing Front View: %s\n', frontPath);
        frontRes = segment_front_eye(frontPath);
    else
        fprintf('[!] Front view not provided. Using anatomical baselines.\n');
        frontRes.pupilRadius = 45; frontRes.irisRadius = 115;
        frontRes.pupilCircularity = 0.94; frontRes.pupilToIrisRatio = 0.39;
        frontRes.pupilAsymmetryPx = 3.2; frontRes.cornealClarity = 95.0;
    end

    % 3. Side Profile Processing
    if ~isempty(sidePath) && exist(sidePath, 'file')
        fprintf('[+] Analyzing Side Profile: %s\n', sidePath);
        sideRes = segment_side_eye_acd_aca(sidePath);
    else
        fprintf('[!] Side profile not provided. Using baseline open angle.\n');
        sideRes.acdMm = 2.85; sideRes.acaDegrees = 32.0;
        sideRes.vanHerickGrade = 'Grade 3 (Open)'; sideRes.closureRisk = 'Low Risk';
    end

    % 4. External Fundus Standardization & Quality Gate
    fprintf('[+] Fundus Preprocessing & Quality Assessment: %s\n', fundusPath);
    qc = qc_check_fundus_gate(fundusPath);
    fprintf('    -> Quality Status: %s (Blur: %.1f | Disc: %d)\n', qc.status, qc.blurScore, qc.discVisible);

    [standardFundus, rawFundus, ~] = standardize_fundus_image(fundusPath);
    fundusRes = segment_fundus_cdr_gradcam(standardFundus);
    fprintf('    -> vCDR: %.2f | hCDR: %.2f | ISNT: %d\n', fundusRes.vCDR, fundusRes.hCDR, fundusRes.isntCompliant);

    % 5. Multimodal AI Fusion
    fprintf('[+] Executing Multimodal AI Fusion Engine...\n');
    diag = multimodal_ai_fusion(frontRes, sideRes, fundusRes, patientInfo);
    fprintf('    -> Glaucoma Risk Score  : %.1f%% [%s]\n', diag.riskScorePercent, diag.riskLevel);
    fprintf('    -> Investigational IOP : %.1f mmHg (%s)\n', diag.iopEst, diag.iopCategory);
    fprintf('    -> Disease Subtype      : %s\n', diag.diseaseSubtype);

    % 6. Generate Diagnostic Report
    fprintf('[+] Generating Multi-Panel Report & Grad-CAM Visualizations...\n');
    [reportImg, reportPdf] = generate_clinical_report(frontRes, sideRes, fundusRes, diag, patientInfo, outputDir);

    gradCamPath = fullfile(outputDir, 'gradcam_overlay.jpg');
    imwrite(fundusRes.gradCamOverlay, gradCamPath);

    % 7. Export JSON Results
    res.front_pupil_ratio       = frontRes.pupilToIrisRatio;
    res.front_pupil_asymmetry   = frontRes.pupilAsymmetryPx;
    res.acd_mm                  = sideRes.acdMm;
    res.aca_degrees             = sideRes.acaDegrees;
    res.van_herick_grade        = sideRes.vanHerickGrade;
    res.fundus_vcdr             = fundusRes.vCDR;
    res.fundus_hcdr             = fundusRes.hCDR;
    res.isnt_compliant          = fundusRes.isntCompliant;
    res.rnfl_defect_detected    = fundusRes.rnflDefectDetected;
    res.predicted_iop_mmhg      = diag.iopEst;
    res.iop_category            = diag.iopCategory;
    res.iop_severity            = diag.iopSeverity;
    res.glaucoma_risk_score     = diag.riskScorePercent;
    res.risk_level              = diag.riskLevel;
    res.disease_subtype         = diag.diseaseSubtype;
    res.clinical_action_plan    = diag.recommendation;
    res.report_image_path       = reportImg;
    res.report_pdf_path         = reportPdf;
    res.gradcam_image_path      = gradCamPath;
    res.qc_status               = qc.status;

    jsonFile = fullfile(outputDir, 'glaucohome_report.json');
    fid = fopen(jsonFile, 'w');
    fprintf(fid, '%s', jsonencode(res, 'PrettyPrint', true));
    fclose(fid);

    fprintf('========================================================\n');
    fprintf('  SUCCESS: Diagnostic Report Generated at:\n');
    fprintf('  %s\n', reportImg);
    fprintf('========================================================\n');
end
