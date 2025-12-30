README 
======

## Purpose
This Python script processes an input CSV file (manual labels from a .jab file) to extract and organize ground-truth labels data based on unique directory paths (according to each video). It creates separate output files for each unique path and counts occurrences of video paths. 
---

## Features
1. **Path-Based Data Organization**:
   - Extracts the directory path from each row of the CSV file.

2. **Output File Creation**:
   - Creates a separate CSV file for each unique path.
   - Saves these files in a folder named `manual_output_files` within the same directory as the input file.

3. **Video Path Counting**:
   - Counts occurrences of each unique video path (assumed to be in column 0).
   - Outputs the count to both the console and a CSV file.

4. **Video Names List**:
   - Extracts and prints basenames of all unique paths.

---

## Usage Instructions

### Prerequisites
- Python 3.x
- CSV file with appropriate data.

### Steps
1. Run the script and provide the file path to your input CSV file when prompted.
2. The script will:
   - Create an output folder (`manual_output_files`) in the same location as the input file.
   - Process the input file to group data by paths and generate output files.
   - Count occurrences of each video path and save the results in a summary CSV file.
3. View the outputs:
   - Individual CSV files for each path in `manual_output_files`.
   - A summary file named `video_path_counts.csv` in the same folder.

### Input File Format
- .csv file
- The input file must be a CSV that can be extracted from 'extractLabel's' code - 
  - Column 0 contains file paths.
  - Columns 2 and 3 contain data to be grouped and saved for each unique path.

### Output Files
- **Path-Specific CSV Files**:
  - Saved as `<basename_of_path>_output.csv` in the `manual_output_files` folder.
- **Video Path Counts**:
  - A summary CSV file (`video_path_counts.csv`) listing video paths and their counts.

