function reportData = analyze_image(fundusImagePath)
% ANALYZE_IMAGE - GlaucoHome One-Command Retinal Diagnostic Analyzer
%
% Usage:
%   analyze_image;                       % Prompts with an interactive file browser
%   analyze_image('path_to_image.jpg');  % Analyzes the specified image file
%
% Output displays on screen:
%   - Figure 1: GlaucoHome Retinal Diagnostic Report & Microvascular Lesions
%   - Figure 2: Optic Disc & Cup Segmentation, Vessel Skeleton & 5-Class Probabilities
%   - Detailed Clinical Summary in Command Window
%
% Generated files saved to disk:
%   - Final_Retinal_Report.png
%   - GradCAM_Result.png
%   - GradCAM_3Panel.png
%   - glaucohome_clinical_report.pdf
%   - glaucohome_report.json

    if nargin < 1
        fundusImagePath = '';
    end
    reportData = run_all_glaucohome_matlab(fundusImagePath);
end
