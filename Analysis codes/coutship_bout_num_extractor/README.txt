README.txt
==========

Script Description
-------------------
This script automates the following processes for analyzing behavioral data from JAABA (Janelia Automatic Animal Behavior Annotator) outputs from cropped chamber videos:

1. Rename Files Recursively:
   - Renames and copies specific classifier score files from deeply nested directories into a centralized folder (`score_files`) for further analysis.
   - Classifier names are pre-defined in the script.
   - Ensures organized storage and prepares data for processing.

2. Extract Courtship Behavior Frames:
   - Utilizes a MATLAB function `SheetMaker` (assumed to be present in the MATLAB path) to extract courtship behavior frames into CSV format.

3. Compile CSV Files:
   - Compiles CSV files based on specific classifiers, aggregating courtship behavior data for analysis.
   - Identifies dominant flies (based on behavioral counts) and creates new CSV files summarizing the data.

Setup and Dependencies
----------------------
Prerequisites:
1. Python Packages:
   - Standard libraries: `os`, `shutil`, `csv`, `glob`
   - No external Python libraries are required.

2. MATLAB:
   - A valid MATLAB installation is required for running the `SheetMaker` function.
   - MATLAB Engine API for Python must be installed and configured.

3. File Structure:
   - The parent folder should contain video and JAABA output folders structured into nested directories.

Functions
---------
1. rename_files_recursively(root_path)
   - Input: `root_path` - The parent directory containing JAABA output folders.
   - Functionality: 
     - Searches for files matching specific classifier names.
     - Renames and copies them to a new folder (`score_files`).

2. extract_courtship_behavior_frames_to_csv(root_path)
   - Input: `root_path` - The parent directory containing the `score_files` folder.
   - Functionality:
     - Changes directory to `score_files`.
     - Calls the `SheetMaker` MATLAB function to process files.

3. compile_csv_files(root_path)
   - Input: `root_path` - The parent directory containing the `score_files` folder.
   - Functionality:
     - Compiles courtship behavior data for classifiers into new CSV files.
     - Aggregates counts for Fly1 and Fly2, and determines the dominant fly.

4. main()
   - Functionality:
     - Takes user input for the root path.
     - Calls the above functions in sequence.
     - Designed to handle multiple runs interactively.

Instructions for Use
--------------------
1. Ensure the folder structure follows the nested JAABA output format.
2. Save this script and run it using Python 3.
3. During execution:
   - Enter the complete path of the parent folder containing video and JAABA folders when prompted.
4. Outputs:
   - A `score_files` folder containing renamed and copied files.
   - Extracted courtship behavior frames in CSV format.
   - Compiled CSV files summarizing behavioral data.

Notes
-----
- The `SheetMaker` MATLAB function must be predefined and accessible. Ensure it works correctly for extracting courtship behavior frames.
- Adjust the list of classifier names (`classifier_names`) as needed.
- The script assumes that all files are properly formatted and follow a standard naming convention.
- For large datasets, ensure sufficient disk space is available for copied and compiled files.




