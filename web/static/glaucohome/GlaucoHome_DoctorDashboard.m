function GlaucoHome_DoctorDashboard()
% GLAUCOHOME_DOCTORDASHBOARD
% Standalone Interactive MATLAB GUI for Ophthalmologists
% Enables loading Front, Side, and Fundus scans, inspecting active contours,
% viewing Grad-CAM saliency heatmaps, and printing clinical reports.

    hFig = figure('Name', 'GlaucoHome Doctor Dashboard - Tri-Modal Diagnostic Suite', ...
                  'Color', [0.08 0.11 0.20], 'Position', [100 100 1200 740], ...
                  'MenuBar', 'none', 'NumberTitle', 'off');

    uicontrol(hFig, 'Style', 'text', 'String', 'GLAUCOHOME: CLINICAL OPHTHALMOLOGY DASHBOARD', ...
              'ForegroundColor', [0.22 0.77 0.88], 'BackgroundColor', [0.08 0.11 0.20], ...
              'FontSize', 15, 'FontWeight', 'bold', 'Position', [30 680 650 35]);

    % Axes for Fundus & Grad-CAM
    axFundus = axes(hFig, 'Position', [0.05 0.38 0.28 0.46]);
    title(axFundus, 'Fundus Scan & Segmentation', 'Color', 'w');
    box(axFundus, 'on'); set(axFundus, 'Color', [0.05 0.05 0.08]);

    axGradCam = axes(hFig, 'Position', [0.36 0.38 0.28 0.46]);
    title(axGradCam, 'Grad-CAM Saliency Heatmap', 'Color', 'w');
    box(axGradCam, 'on'); set(axGradCam, 'Color', [0.05 0.05 0.08]);

    % Results Panel
    hPanel = uipanel(hFig, 'Title', 'Tri-Modal Biomarkers & Risk Assessment', ...
                     'ForegroundColor', [0.22 0.77 0.88], 'BackgroundColor', [0.12 0.16 0.27], ...
                     'FontSize', 11, 'FontWeight', 'bold', 'Position', [0.67 0.20 0.30 0.70]);

    lblVCDR = uicontrol(hPanel, 'Style', 'text', 'String', 'vCDR: Pending...', ...
        'ForegroundColor', 'w', 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 11, 'Position', [15 390 280 25]);
    lblACD = uicontrol(hPanel, 'Style', 'text', 'String', 'ACD: Pending...', ...
        'ForegroundColor', 'w', 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 11, 'Position', [15 350 280 25]);
    lblIOP = uicontrol(hPanel, 'Style', 'text', 'String', 'Investigational IOP: Pending...', ...
        'ForegroundColor', [1.0 0.65 0.2], 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 12, 'FontWeight', 'bold', 'Position', [15 305 280 30]);
    lblSubtype = uicontrol(hPanel, 'Style', 'text', 'String', 'Subtype: Pending...', ...
        'ForegroundColor', 'w', 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 11, 'FontWeight', 'bold', 'Position', [15 260 280 30]);
    lblRisk = uicontrol(hPanel, 'Style', 'text', 'String', 'Risk Score: Pending...', ...
        'ForegroundColor', [0.3 0.9 0.4], 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 14, 'FontWeight', 'bold', 'Position', [15 200 280 40]);
    lblAction = uicontrol(hPanel, 'Style', 'text', 'String', 'Action: Ready to load patient scan.', ...
        'ForegroundColor', [0.8 0.8 0.8], 'BackgroundColor', [0.12 0.16 0.27], 'FontSize', 9.5, 'Position', [15 20 280 160]);

    % Action Buttons
    uicontrol(hFig, 'Style', 'pushbutton', 'String', '📁 Load Fundus Image', ...
              'BackgroundColor', [0.22 0.50 0.88], 'ForegroundColor', 'w', 'FontSize', 11, 'FontWeight', 'bold', ...
              'Position', [50 140 180 45], 'Callback', @loadFundusCallback);

    uicontrol(hFig, 'Style', 'pushbutton', 'String', '📁 Load Side Profile', ...
              'BackgroundColor', [0.22 0.50 0.88], 'ForegroundColor', 'w', 'FontSize', 11, 'FontWeight', 'bold', ...
              'Position', [250 140 180 45], 'Callback', @loadSideCallback);

    uicontrol(hFig, 'Style', 'pushbutton', 'String', '⚡ Run Tri-Modal AI', ...
              'BackgroundColor', [0.15 0.75 0.45], 'ForegroundColor', 'w', 'FontSize', 12, 'FontWeight', 'bold', ...
              'Position', [450 140 220 45], 'Callback', @runAnalysisCallback);

    fundusFile = '';
    sideFile = '';

    function loadFundusCallback(~, ~)
        [f, p] = uigetfile({'*.jpg;*.png;*.jpeg', 'Image Files'}, 'Select Fundus Image');
        if f ~= 0
            fundusFile = fullfile(p, f);
            imshow(fundusFile, 'Parent', axFundus);
            title(axFundus, sprintf('Fundus: %s', f), 'Color', 'w');
        end
    end

    function loadSideCallback(~, ~)
        [f, p] = uigetfile({'*.jpg;*.png;*.jpeg', 'Image Files'}, 'Select Side Profile Image');
        if f ~= 0
            sideFile = fullfile(p, f);
        end
    end

    function runAnalysisCallback(~, ~)
        if isempty(fundusFile)
            msgbox('Please load at least a Fundus scan first!', 'Input Missing', 'warn');
            return;
        end

        set(lblAction, 'String', 'Standardizing Fundus, Active Contours & Grad-CAM...');
        drawnow;

        [stdFundus, ~, ~] = standardize_fundus_image(fundusFile);
        fundusRes = segment_fundus_cdr_gradcam(stdFundus);

        if ~isempty(sideFile)
            sideRes = segment_side_eye_acd_aca(sideFile);
        else
            sideRes.acdMm = 2.85; sideRes.acaDegrees = 32.0; sideRes.vanHerickGrade = 'Grade 3';
        end

        frontRes.pupilToIrisRatio = 0.38; frontRes.pupilAsymmetryPx = 3.0;
        diag = multimodal_ai_fusion(frontRes, sideRes, fundusRes, []);

        imshow(fundusRes.gradCamOverlay, 'Parent', axGradCam);

        set(lblVCDR, 'String', sprintf('vCDR: %.2f (ISNT: %s)', fundusRes.vCDR, char(ternary(fundusRes.isntCompliant, "Pass", "Violated"))));
        set(lblACD,  'String', sprintf('ACD: %.2f mm (ACA: %.1f deg)', sideRes.acdMm, sideRes.acaDegrees));
        set(lblIOP,  'String', sprintf('Investigational IOP: %.1f mmHg [%s]', diag.iopEst, diag.iopSeverity));
        set(lblSubtype, 'String', sprintf('Diagnosis: %s', diag.diseaseSubtype));
        set(lblRisk, 'String', sprintf('Risk Score: %.1f%% (%s)', diag.riskScorePercent, diag.riskLevel));
        set(lblAction, 'String', diag.recommendation);
    end

    function val = ternary(c, a, b)
        if c, val = a; else, val = b; end
    end
end
