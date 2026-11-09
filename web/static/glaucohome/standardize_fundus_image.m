function [standardImg, rawImg, fovMask, qualityInfo] = standardize_fundus_image(fundusInput, targetSize)
% STANDARDIZE_FUNDUS_IMAGE
% Image Quality Assessment, Adaptive Enhancement, and Standardization Pipeline.
% Evaluates focus, illumination, and field-of-view adequacy.
% Applies large-kernel Gaussian equalization (sigma=30), CLAHE (ClipLimit=0.015),
% and provides recapture guidance.

    if nargin < 2, targetSize = [800 800]; end

    if ischar(fundusInput) || isstring(fundusInput)
        if ~isfile(fundusInput)
            error('Fundus image file not found: %s', fundusInput);
        end
        rawImg = imread(fundusInput);
    else
        rawImg = fundusInput;
    end

    [origH, origW, ~] = size(rawImg);

    % 1. Detect Circular Retinal Field-of-View (FOV)
    if size(rawImg, 3) == 3
        gray = rgb2gray(rawImg);
    else
        gray = rawImg;
    end
    thresh = max(15, graythresh(gray) * 255 * 0.25);
    fovMask = gray > thresh;
    fovMask = imfill(fovMask, 'holes');
    fovMask = bwareafilt(fovMask, 1);

    % 2. Quality Metrics
    retinalPixels = sum(fovMask(:));
    totalPixels = origH * origW;
    fovCoveragePct = (retinalPixels / totalPixels) * 100.0;

    % Mean brightness within FOV
    if any(fovMask(:))
        brightnessScore = round(mean(double(gray(fovMask))), 2);
    else
        brightnessScore = round(mean(double(gray(:))), 2);
    end

    % Sharpness index via normalized Laplacian/Tenengrad variance
    [Gx, Gy] = imgradientxy(double(gray));
    gradMag = Gx.^2 + Gy.^2;
    if any(fovMask(:))
        sharpnessScore = var(gradMag(fovMask)) / (mean(gradMag(fovMask))^2 + 1e-5);
    else
        sharpnessScore = var(gradMag(:)) / (mean(gradMag(:))^2 + 1e-5);
    end
    sharpnessScore = round(sharpnessScore, 4);

    % Adequacy evaluation
    isAdequate = (sharpnessScore >= 0.0015) && (brightnessScore >= 35) && (fovCoveragePct >= 50.0);
    if isAdequate
        adequacyGrade = 'Adequate (Gradeable)';
        recaptureGuidance = 'None - Image quality meets diagnostic standards.';
    else
        adequacyGrade = 'Borderline / Recapture Advised';
        recaptureGuidance = 'Recapture Guidance: Focus blur or uneven illumination detected. Stabilize camera and center on optic disc.';
    end

    overallQualityIndex = round(min(100.0, max(10.0, 0.40 * min(100, (brightnessScore / 130.0) * 100) + ...
                                                     0.35 * min(100, sharpnessScore * 600.0) + ...
                                                     0.25 * min(100, fovCoveragePct))), 1);

    qualityInfo.brightnessScore = brightnessScore;
    qualityInfo.sharpnessScore = sharpnessScore;
    qualityInfo.retinalFovPixels = retinalPixels;
    qualityInfo.retinalFovCoverage = round(fovCoveragePct, 1);
    qualityInfo.isAdequate = isAdequate;
    qualityInfo.adequacyGrade = adequacyGrade;
    qualityInfo.recaptureGuidance = recaptureGuidance;
    qualityInfo.overallQualityIndex = overallQualityIndex;
    qualityInfo.sensorWorkingResolution = sprintf('%d x %d px', targetSize(1), targetSize(2));

    % 3. Crop Bounding Box
    stats = regionprops(fovMask, 'BoundingBox');
    if ~isempty(stats)
        bb = round(stats(1).BoundingBox);
        x1 = max(1, bb(1)); y1 = max(1, bb(2));
        x2 = min(origW, x1 + bb(3)); y2 = min(origH, y1 + bb(4));
        cropped = rawImg(y1:y2, x1:x2, :);
    else
        cropped = rawImg;
    end

    % 4. Resize to Standard Matrix
    resized = imresize(cropped, targetSize);

    % 5. Adaptive Enhancement: Large-Kernel Gaussian Equalization (sigma=30)
    greenChan = resized(:, :, 2);
    hGauss = fspecial('gaussian', [61 61], 30);
    bgIllum = imfilter(greenChan, hGauss, 'replicate');
    flatGreen = double(greenChan) - double(bgIllum) + 128;
    flatGreen = uint8(max(0, min(255, flatGreen)));

    % 6. Controlled CLAHE (ClipLimit=0.015)
    claheGreen = adapthisteq(flatGreen, 'ClipLimit', 0.015, 'Distribution', 'rayleigh');

    standardImg = resized;
    standardImg(:, :, 2) = claheGreen;
end
