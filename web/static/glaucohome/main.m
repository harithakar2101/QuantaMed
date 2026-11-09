function varargout = main(varargin)
% GlaucoHome Master Launcher
% Forwards inputFundusPath and optional patientInput to matlab/main.m
    currDir = pwd;
    matlabDir = fullfile(fileparts(mfilename('fullpath')), 'matlab');
    if ~exist(matlabDir, 'dir')
        matlabDir = fullfile(fileparts(mfilename('fullpath')), 'Glaucohome-Flutter-main', 'matlab');
    end
    addpath(matlabDir);
    cd(matlabDir);
    try
        if nargout > 0
            [varargout{1:nargout}] = main(varargin{:});
        else
            main(varargin{:});
        end
        cd(currDir);
    catch ME
        cd(currDir);
        rethrow(ME);
    end
end
