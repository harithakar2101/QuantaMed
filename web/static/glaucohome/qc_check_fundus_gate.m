function qc = qc_check_fundus_gate(imgInput)
% QC_CHECK_FUNDUS_GATE - Phase 3: Fundus Preprocessing & Quality Assessment Gate
%
% Clinical Quality Gate for Glaucoma Tele-Ophthalmology:
% 1. Brightness Homogeneity & Illumination Dynamic Range
% 2. Laplacian / Tenengrad Focus Blur Score
% 3. Field of View (FOV) Adequacy & Coverage
% 4. Optic Nerve Head (ONH) Region Visibility
% 5. Safety Gate with Real-Time Recapture Guidance

    if ischar(imgInput) || isstring(imgInput)
        if ~isfile(imgInput)
            error('Input image file not found: %s', imgInput);
        end
        img = imread(imgInput);
    else
        img = imgInput;
    end

    if size(img, 3) == 3
        gray = rgb2gray(img);
        green = img(:, :, 2);
    else
        gray = img;
        green = img;
    end
    grayD = double(gray);
    [H, W] = size(gray);

    % ── 1. Field of View (FOV) Detection ──
    fovMask = gray > max(12, graythresh(gray) * 255 * 0.22);
    fovMask = imfill(fovMask, 'holes');
    fovMask = bwareafilt(fovMask, 1);
    fovPixels = sum(fovMask(:));
    totalPixels = H * W;
    fovCoveragePct = (fovPixels / totalPixels) * 100.0;

    % ── 2. Focus & Blur Measurement (Tenengrad / Modified Laplacian) ──
    hx = [-1 0 1; -2 0 2; -1 0 1];
    hy = hx';
    Gx = conv2(grayD, hx, 'same');
    Gy = conv2(grayD, hy, 'same');
    gradMag = sqrt(Gx.^2 + Gy.^2);
    
    if fovPixels > 0
        tenengrad = mean(gradMag(fovMask).^2);
        lapScore = var(gradMag(fovMask)) / (mean(gradMag(fovMask))^2 + 1e-5);
    else
        tenengrad = mean(gradMag(:).^2);
        lapScore = var(gradMag(:)) / (mean(gradMag(:))^2 + 1e-5);
    end
    blurScore = round(tenengrad / 10.0, 2);

    % ── 3. Illumination Dynamic Range & Homogeneity ──
    if fovPixels > 0
        meanLum = mean(grayD(fovMask));
        stdLum  = std(grayD(fovMask));
    else
        meanLum = mean(grayD(:));
        stdLum  = std(grayD(:));
    end

    % Quadrant brightness homogeneity
    midY = round(H/2); midX = round(W/2);
    q1 = mean(grayD(1:midY, 1:midX));
    q2 = mean(grayD(1:midY, midX:end));
    q3 = mean(grayD(midY:end, 1:midX));
    q4 = mean(grayD(midY:end, midX:end));
    qMeans = [q1, q2, q3, q4];
    homogeneityScore = round(100.0 - (std(qMeans) / (mean(qMeans) + eps) * 100.0), 1);
    homogeneityScore = max(0.0, min(100.0, homogeneityScore));

    isTooDark  = (meanLum < 32);
    isTooLight = (meanLum > 228);
    isLowContrast = (stdLum < 18);
    isBlurry = (blurScore < 14.0);
    isLowFOV = (fovCoveragePct < 55.0);

    % ── 4. Optic Nerve Head (ONH) Visibility Check ──
    hGauss = fspecial('gaussian', [25 25], 5);
    smoothGreen = imfilter(double(green), hGauss);
    maxVal = max(smoothGreen(:));
    discVisible = (maxVal > 110);

    % ── 5. Safety Gate Composite Decision ──
    if ~isBlurry && ~isTooDark && ~isTooLight && ~isLowContrast && ~isLowFOV && discVisible
        isPassed = true;
        status = 'PASS';
        msg = 'Fundus image quality verified. Ready for Active Contour & AI segmentation.';
    elseif isBlurry
        isPassed = false;
        status = 'FAIL_BLUR';
        msg = 'Image is blurry! Stabilize smartphone mount or refocus retinal adapter.';
    elseif isTooDark
        isPassed = false;
        status = 'FAIL_UNDEREXPOSED';
        msg = 'Retinal illumination too dim. Increase flash or coaxial LED intensity.';
    elseif isTooLight
        isPassed = false;
        status = 'FAIL_OVEREXPOSED';
        msg = 'Severe glare or overexposure detected. Adjust retinal camera aperture.';
    elseif isLowFOV
        isPassed = false;
        status = 'FAIL_FOV_ALIGNMENT';
        msg = 'Field of view misaligned. Center fundus lens directly along optic axis.';
    else
        isPassed = false;
        status = 'FAIL_DISC_NOT_FOUND';
        msg = 'Optic nerve head not clearly visible in field of view.';
    end

    qc.isPassed          = isPassed;
    qc.status            = status;
    qc.blurScore         = blurScore;
    qc.laplacianScore    = round(lapScore, 4);
    qc.meanLum           = round(meanLum, 1);
    qc.contrastStd       = round(stdLum, 1);
    qc.homogeneityScore  = homogeneityScore;
    qc.fovCoveragePct    = round(fovCoveragePct, 1);
    qc.discVisible       = discVisible;
    qc.message           = msg;
end
