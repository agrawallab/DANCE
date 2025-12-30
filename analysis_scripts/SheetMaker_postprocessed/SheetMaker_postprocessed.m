mainFolder = 'E:\Paulami\All cropped videos\test_SH\JAABAPlot_1';
subfolders = dir(mainFolder);
subfolders = subfolders([subfolders.isdir] & ~startsWith({subfolders.name}, '.'));

for i = 1:length(subfolders)
    subfolderName = subfolders(i).name;
    subfolderPath = fullfile(mainFolder, subfolderName);
    myFiles = dir(fullfile(subfolderPath, '*.mat'));
    
    for k = 1:length(myFiles)
        matFilePath = fullfile(subfolderPath, myFiles(k).name);
        load(matFilePath)
        [~, baseFileName, ~] = fileparts(myFiles(k).name);
        
        filenameFly1 = fullfile(subfolderPath, strcat(baseFileName, "_Fly1.csv"));
        filenameFly2 = fullfile(subfolderPath, strcat(baseFileName, "_Fly2.csv"));
        
        try
            % Check if allScores.t0s and allScores.t1s exist and have required structure
            if isfield(allScores, 't0s') && isfield(allScores, 't1s')
                % Matrix Fly1
                Fly1 = [];
                t0s = allScores.t0s{1};
                t1s = allScores.t1s{1};
                max_length = max(numel(t0s), numel(t1s));
                Fly1 = NaN(max_length, 2);
                Fly1(1:numel(t0s), 1) = t0s;
                Fly1(1:numel(t1s), 2) = t1s;
                Fly1 = Fly1(~isnan(Fly1(:,1)) | ~isnan(Fly1(:,2)), :); % Remove NaN rows
                
                % Matrix Fly2
                Fly2 = [];
                t0s = allScores.t0s{2};
                t1s = allScores.t1s{2};
                max_length = max(numel(t0s), numel(t1s));
                Fly2 = NaN(max_length, 2);
                Fly2(1:numel(t0s), 1) = t0s;
                Fly2(1:numel(t1s), 2) = t1s;
                Fly2 = Fly2(~isnan(Fly2(:,1)) | ~isnan(Fly2(:,2)), :); % Remove NaN rows
                
                % Write matrices to CSV files
                writematrix(Fly1, filenameFly1)
                writematrix(Fly2, filenameFly2)
            else
                warning('File %s does not contain expected fields: t0s or t1s', matFilePath);
            end
        catch ME
            fprintf('Error processing file %s: %s\n', matFilePath, ME.message);
        end
    end
end
