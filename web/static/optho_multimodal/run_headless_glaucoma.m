% =========================================================================
% HEADLESS BATCH RUNNER FOR GLAUCOMA ONH PIPELINE
% =========================================================================

try
    if ~exist('inputImage', 'var') || isempty(inputImage)
        if exist('C:\Users\Dheshini\Downloads\DR_Screening_SIH\01_original_fundus.png', 'file')
            inputImage = 'C:\Users\Dheshini\Downloads\DR_Screening_SIH\01_original_fundus.png';
        else
            inputImage = fullfile(fileparts(mfilename('fullpath')), '..', 'sample_data', 'sample_fundus_onh.png');
        end
    end

    if ~exist('outputDir', 'var') || isempty(outputDir)
        outputDir = fullfile(fileparts(mfilename('fullpath')), '..', 'output');
    end

    res = glaucoma_onh_pipeline(inputImage, outputDir);
    exit(0);
catch ME
    fprintf(2, 'Error in run_headless_glaucoma: %s\n', ME.message);
    exit(1);
end
