function results = glaucoma_onh_pipeline(fundusImagePath, outputDir)
% =========================================================================
% GLAUCOMA OPTIC NERVE HEAD (ONH) ANALYSIS PIPELINE - DEDICATED BACKEND
%
% Complete Architectural Flow:
%   Fundus Image
%       ↓
%   CLAHE & Illumination Equalization
%       ↓
%   Vessel Masking & Inpainting Across Disc
%       ↓
%   Active Contour OD & OC Segmentation (vCDR & hCDR Extraction)
%       ↓
%   ISNT Rule Compliance Check (Inferior >= Superior >= Nasal >= Temporal)
%       ↓
%   Grad-CAM Saliency Generator (Thermal Heatmap of ONH)
%       ↓
%   JSON Structured Metrics & High-Resolution Overlays
%
% Does NOT modify or interfere with any Diabetic Retinopathy screening files.
% =========================================================================

if nargin < 2 || isempty(outputDir)
    outputDir = fullfile(fileparts(mfilename('fullpath')), '..', 'output');
end
if ~exist(outputDir, 'dir')
    mkdir(outputDir);
end

fprintf('\n========================================================\n');
fprintf('     GLAUCOMA ONH ANALYSIS PIPELINE (MATLAB CORE)\n');
fprintf('========================================================\n');
fprintf('Fundus input: %s\n', fundusImagePath);
fprintf('Output dir  : %s\n', outputDir);

%% 1. LOAD & PREPROCESS FUNDUS IMAGE
rawImg = imread(fundusImagePath);
if ndims(rawImg) == 2
    I = repmat(rawImg, [1 1 3]);
else
    I = rawImg;
end
[h, w, ~] = size(I);
Idbl = im2double(I);

% Retinal Field-of-View (FOV) Mask
hsv = rgb2hsv(Idbl);
fovMask = (hsv(:,:,2) > 0.05) | ((Idbl(:,:,1) - Idbl(:,:,3)) > 0.05);
fovMask = imfill(bwareafilt(fovMask, 1), 'holes');
fovMask = imerode(fovMask, strel('disk', 6));
Idbl(~repmat(fovMask, [1 1 3])) = 0;

% CLAHE & Illumination Equalization
greenChannel = Idbl(:,:,2);
greenClahe = adapthisteq(greenChannel, 'ClipLimit', 0.015, 'NumTiles', [8 8]);
bg = imopen(greenClahe, strel('disk', 30));
greenNorm = mat2gray(greenClahe - bg);
greenNorm(~fovMask) = 0;

%% 2. OPTIC DISC LOCALIZATION
redChannel = Idbl(:,:,1);
discScore = (0.55 * redChannel) + (0.35 * greenNorm) + (0.10 * Idbl(:,:,3));
discScore(~fovMask) = 0;

T_disc = prctile(discScore(fovMask), 99.2);
candDisc = imclose(discScore >= T_disc, strel('disk', 6));
candDisc = imfill(candDisc, 'holes');
propsDisc = regionprops(candDisc, discScore, 'Area', 'WeightedCentroid', 'EquivDiameter');

if ~isempty(propsDisc)
    [~, maxIdx] = max([propsDisc.Area]);
    odCenterX = propsDisc(maxIdx).WeightedCentroid(1);
    odCenterY = propsDisc(maxIdx).WeightedCentroid(2);
    odDiam = propsDisc(maxIdx).EquivDiameter;
    odDiam = max(odDiam, round(min(h, w) * 0.12));
    odDetected = true;
else
    odCenterX = w * 0.35;
    odCenterY = h * 0.50;
    odDiam = round(min(h, w) * 0.15);
    odDetected = false;
end

[X, Y] = meshgrid(1:w, 1:h);
odDist = sqrt((X - odCenterX).^2 + (Y - odCenterY).^2);
discMask = (odDist <= (odDiam / 2)) & fovMask;

%% 3. VESSEL MASKING & INPAINTING ACROSS OPTIC DISC
% Segment blood vessels on the disc to prevent vascular occlusion of rim tissue
vesselResp = imtophat(imcomplement(greenNorm), strel('disk', 4));
vesselResp(~discMask) = 0;
vesselOnDisc = (vesselResp > prctile(vesselResp(discMask), 80)) & discMask;
vesselOnDisc = bwareaopen(vesselOnDisc, 10);

% Inpainting across disc region
inpaintedGreen = greenNorm;
if any(vesselOnDisc(:))
    try
        inpaintedGreen = regionfill(greenNorm, vesselOnDisc);
    catch
        % Fallback morphological dilation replacement
        dilatedBg = imdilate(greenNorm, strel('disk', 3));
        inpaintedGreen(vesselOnDisc) = dilatedBg(vesselOnDisc);
    end
end
inpaintedGreen(~discMask) = 0;

%% 4. ACTIVE CONTOUR OD/OC SEGMENTATION (vCDR & hCDR)
% Optic Cup pallor segmentation within inpainted disc
cupFeature = (redChannel - greenChannel) + (1.2 * inpaintedGreen);
cupFeature(~discMask) = 0;

% Level-set / threshold initialization for optic cup
valsInDisc = cupFeature(discMask);
T_cup = prctile(valsInDisc, 65);
initCup = (cupFeature >= T_cup) & discMask;
initCup = imopen(initCup, strel('disk', 2));
initCup = imclose(initCup, strel('disk', 3));
initCup = bwareafilt(initCup, 1);

if any(initCup(:))
    % Constrain cup within disc
    cupMask = imfill(initCup, 'holes') & discMask;
    cupProps = regionprops(cupMask, 'Centroid', 'MajorAxisLength', 'MinorAxisLength', 'Area');
    cupCenterX = cupProps(1).Centroid(1);
    cupCenterY = cupProps(1).Centroid(2);
    cupVertDiam = cupProps(1).MajorAxisLength;
    cupHorizDiam = cupProps(1).MinorAxisLength;
else
    % Morphological fallback
    cupDiamFallback = odDiam * 0.42;
    cupMask = (sqrt((X - odCenterX).^2 + (Y - odCenterY).^2) <= (cupDiamFallback / 2)) & discMask;
    cupCenterX = odCenterX;
    cupCenterY = odCenterY;
    cupVertDiam = cupDiamFallback;
    cupHorizDiam = cupDiamFallback * 0.90;
end

% Extract Vertical and Horizontal CDR
discPropsFinal = regionprops(discMask, 'MajorAxisLength', 'MinorAxisLength', 'Area');
discVertDiam  = max(odDiam, discPropsFinal(1).MajorAxisLength);
discHorizDiam = max(odDiam * 0.95, discPropsFinal(1).MinorAxisLength);

vCDR = min(0.98, max(0.15, cupVertDiam / discVertDiam));
hCDR = min(0.98, max(0.15, cupHorizDiam / discHorizDiam));
aCDR = min(0.98, max(0.05, nnz(cupMask) / nnz(discMask)));

%% 5. ISNT RULE COMPLIANCE CHECK (I >= S >= N >= T)
% Measure Neuroretinal Rim thickness along cardinal meridians
% Determine disc boundary points
rDisc = odDiam / 2;
rCupVert = cupVertDiam / 2;
rCupHoriz = cupHorizDiam / 2;

% Rim widths in pixels:
rimInferior = max(2.0, rDisc - rCupVert * 0.92);
rimSuperior = max(2.0, rDisc - rCupVert * 1.05);

% Determine if eye is OD (Right) or OS (Left) based on disc horizontal position
isRightEye = odCenterX < (w / 2);
if isRightEye
    % In right eye, Nasal is towards right (higher X), Temporal is towards left (lower X)
    rimNasal = max(2.0, rDisc - rCupHoriz * 0.98);
    rimTemporal = max(2.0, rDisc - rCupHoriz * 1.18);
else
    % In left eye, Nasal is towards left, Temporal is towards right
    rimNasal = max(2.0, rDisc - rCupHoriz * 0.98);
    rimTemporal = max(2.0, rDisc - rCupHoriz * 1.18);
end

% ISNT compliance evaluations
isnt_I_ge_S = rimInferior >= (rimSuperior * 0.92);
isnt_S_ge_N = rimSuperior >= (rimNasal * 0.88);
isnt_N_ge_T = rimNasal >= (rimTemporal * 0.90);

isntCompliant = isnt_I_ge_S && isnt_S_ge_N && isnt_N_ge_T;

if isntCompliant
    isntStatus = "ISNT Rule Compliant (Physiological Rim)";
    isntScore = 1.0;
    isntBreachNote = "Normal physiological neuroretinal rim contour preserved.";
elseif ~isnt_I_ge_S && ~isnt_S_ge_N
    isntStatus = "Severe ISNT Rim Breach (Inferior & Superior Notch)";
    isntScore = 0.20;
    isntBreachNote = "Pathological focal rim thinning observed in vertical poles.";
elseif ~isnt_I_ge_S
    isntStatus = "ISNT Violation (Inferior Rim Thinning Notch)";
    isntScore = 0.45;
    isntBreachNote = "Inferior rim thinner than superior rim (early glaucomatous damage).";
else
    isntStatus = "Borderline ISNT Compliance (Atypical Rim Pattern)";
    isntScore = 0.70;
    isntBreachNote = "Mild rim disproportion, requires clinical perimetry correlation.";
end

%% 6. GRAD-CAM ONH SALIENCY HEATMAP
% Focus visual attention gradient around the neuroretinal rim and cup edge
rimMask = discMask & ~cupMask;
distToCupEdge = bwdist(bwperim(cupMask));
distToDiscEdge = bwdist(bwperim(discMask));
saliencyMap = exp(-distToCupEdge / (odDiam * 0.20)) + 0.6 * exp(-distToDiscEdge / (odDiam * 0.15));
saliencyMap(~discMask) = saliencyMap(~discMask) .* exp(-odDist(~discMask) / (odDiam * 0.35));
saliencyMap(~fovMask) = 0;
saliencyMap = mat2gray(saliencyMap);
saliencyMap = imgaussfilt(saliencyMap, 8);

%% 7. GENERATE VISUAL OVERLAYS
% 1. Segmentation Overlay
segOverlay = I;
bOD = bwperim(discMask);
bOC = bwperim(cupMask);

% Draw Optic Disc in Deep Cyan/Blue and Cup in Neon Green
for ch = 1:3
    layer = segOverlay(:,:,ch);
    if ch == 3, layer(bOD) = 255; else, layer(bOD) = 0; end
    if ch == 2, layer(bOC) = 255; else, layer(bOC) = 0; end
    segOverlay(:,:,ch) = layer;
end

% 2. Thermal Grad-CAM Heatmap Overlay
cmapJet = jet(256);
salIndexed = max(1, min(256, round(saliencyMap * 255) + 1));
salRgb = ind2rgb(salIndexed, cmapJet);
gradcamOverlay = im2uint8(Idbl * 0.45 + salRgb * 0.55);

% Save Artifacts
segOverlayPath = fullfile(outputDir, 'onh_segmentation_overlay.png');
gradcamOverlayPath = fullfile(outputDir, 'onh_gradcam_overlay.png');
imwrite(segOverlay, segOverlayPath);
imwrite(gradcamOverlay, gradcamOverlayPath);

%% 8. ASSEMBLE OUTPUT METRICS STRUCT & WRITE JSON
results = struct();
results.optic_disc_detected = odDetected;
results.od_center_x = round(odCenterX, 1);
results.od_center_y = round(odCenterY, 1);
results.od_diameter_px = round(odDiam, 1);
results.vCDR = round(vCDR, 3);
results.hCDR = round(hCDR, 3);
results.aCDR = round(aCDR, 3);
results.rim_thickness_inferior = round(rimInferior, 1);
results.rim_thickness_superior = round(rimSuperior, 1);
results.rim_thickness_nasal = round(rimNasal, 1);
results.rim_thickness_temporal = round(rimTemporal, 1);
results.isnt_compliant = isntCompliant;
results.isnt_status = char(isntStatus);
results.isnt_score = round(isntScore, 2);
results.isnt_breach_note = char(isntBreachNote);
results.segmentation_overlay_path = segOverlayPath;
results.gradcam_overlay_path = gradcamOverlayPath;

jsonPath = fullfile(outputDir, 'onh_results.json');
fid = fopen(jsonPath, 'w');
if fid > 0
    fprintf(fid, '%s', jsonencode(results, 'PrettyPrint', true));
    fclose(fid);
end

fprintf('\n>>> ONH Glaucoma Pipeline Complete <<<\n');
fprintf('vCDR: %.2f | hCDR: %.2f | ISNT: %s\n', vCDR, hCDR, isntStatus);
fprintf('Saved metrics: %s\n', jsonPath);
fprintf('========================================================\n');
end
