README: 
This code is the same as courtship_bout_num_extractor except, it works for unsegmented videos (raw videos)

Overview
--------
This script processes unsegmented video files and associated score files, renaming and copying the files to a new folder. It then extracts courtship frames and compiles data into CSV files.

Functionality
-------------
1. Rename and Copy Files:
   - The script will rename video files and classifier score files based on predefined names, organizing them into a new folder named "score_files".

2. Extract Lunge Frames:
   - Uses MATLAB to process score files and extract courtship classifier's frames data, saving it in a structured format.

3. Compile CSV Files:
   - Compiles individual CSV files containing score data into a final CSV that tracks classifier's counts and compiles male/female analysis.

Requirements
------------
- Python 3.x  
- MATLAB Engine API for Python: Used for MATLAB script execution.
- Required Libraries:
  - os
  - shutil
  - csv
  - glob
  - matlab.engine

Usage
-----
1. Ensure you have the necessary Python libraries installed.
2. Make sure you have the MATLAB engine set up.
3. Run the script:
   - The script will ask for the complete path of the parent folder containing all videos and JAABA folders.
   - The script will rename files and organize them into the "score_files" folder.
   - It will then process the score files and output compiled CSV data.

Instructions:
-------------
1. Place your video and JAABA score files in a folder.
2. Execute the script.
3. Enter the path of the parent folder when prompted.
4. The script will generate:
   - A folder named "score_files" containing renamed and organized files.
   - A compiled CSV file for each classifier.

Notes:
------
- Ensure that your file structure matches the expected layout for the script to process correctly.
- The script assumes specific file names for classifiers. Modify "classifier_names" if your classifiers differ.
