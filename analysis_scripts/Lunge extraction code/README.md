# `Lunge_Analyzer_indiC.py` — works for segmented videos (individual cropped chamber videos)

## Overview

This script processes video files and associated score files, renaming and copying the files to a new folder. It then extracts frame numbers at which lunges occur and compiles it into CSV files.

## Functionality

1. **Rename and Copy Files**
   The script will rename video files and classifier score files based on predefined names, organizing them into a new folder named `score_files`.

2. **Extract Lunge Frames**
   Uses scipy.io to read JAABA score files directly and extracts frame numbers where classifier score exceeds zero.

3. **Compile CSV Files**
   Compiles individual CSV files containing frame numbers into a final CSV that represents lunge bout numbers.

## Requirements

- Python 3.x
- Required libraries:
  - `os`
  - `shutil`
  - `csv`
  - `glob`
  - `numpy`
  - `scipy.io`

## Usage

1. Ensure you have the necessary Python libraries installed.
2. Run the script:
   - The script will ask for the complete path of the parent folder containing all videos and JAABA folders.
   - The script will rename files and organize them into the `score_files` folder.
   - It will then process the score files, giving output in the form of compiled CSV data.

## Instructions

1. Place your video and JAABA score files in a folder.
2. Execute the script.
3. Enter the path of the parent folder when prompted.
4. The script will generate:
   - A folder named `score_files` containing renamed and organized files.
   - A compiled CSV file for the lunge classifier frame data.

## Notes

- Ensure that your file structure matches the expected layout for the script to process correctly.
- The script assumes specific file names for classifiers. Modify `classifier_names` if your classifiers differ.
