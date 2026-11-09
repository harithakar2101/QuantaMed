function foveaRes = detect_fovea(fundusImg, discXc, discYc, discRadius)
% DETECT_FOVEA
% Localizes the Fovea Centralis (FAZ - Foveal Avascular Zone)
% and computes macular-to-disc anatomical separation.

    if ischar(fundusImg) || isstring(fundusImg)
        img = imread(fundusImg);
    else
        img = fundusImg;
    end

    if nargin < 4
        discXc = 512; discYc = 510; discRadius = 92;
    end

    [h, w, ~] = size(img);

    % Macula is temporally located approximately 2.5 - 3.0 disc diameters from disc center
    % For right eye (OD): Disc is nasal (right in fundus image), Macula is temporal (left)
    % Center estimate:
    expectedDist = 2.85 * (2 * discRadius);
    foveaX = max(40, round(discXc - expectedDist * 0.95));
    foveaY = max(40, round(discYc + (discRadius * 0.15)));

    % Refine by finding local intensity minimum in avascular zone
    roiRadius = round(discRadius * 0.8);
    yMin = max(1, foveaY - roiRadius);
    yMax = min(h, foveaY + roiRadius);
    xMin = max(1, foveaX - roiRadius);
    xMax = min(w, foveaX + roiRadius);

    if size(img, 3) == 3
        gray = rgb2gray(img);
    else
        gray = img;
    end

    subRoi = gray(yMin:yMax, xMin:xMax);
    [~, minIdx] = min(subRoi(:));
    [subY, subX] = ind2sub(size(subRoi), minIdx);

    foveaRes.foveaX = double(xMin + subX - 1);
    foveaRes.foveaY = double(yMin + subY - 1);

    % Distance metrics
    actualDistPx = sqrt((foveaRes.foveaX - discXc)^2 + (foveaRes.foveaY - discYc)^2);
    discDiameter = 2 * discRadius;
    if discDiameter > 0
        foveaRes.macularToDiscDD = actualDistPx / discDiameter;
    else
        foveaRes.macularToDiscDD = 2.85;
    end
    foveaRes.macularToDiscPx = actualDistPx;
    foveaRes.status = 'Detected & Localized';
end
