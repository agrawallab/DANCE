MATLAB Script for Extracting and Saving JAABA Data

This MATLAB script processes `.mat` files from subfolders within a specified directory, extracts data from the `allScores` structure, and writes the results into CSV files. It is designed to work with JAABA analysis outputs.

---

Script Overview
Input:
- The `.mat` files should contain an `allScores` structure with the fields:
  - `t0s`: Cell array where each element is a vector of time points (start times).
  - `t1s`: Cell array where each element is a vector of time points (end times).

Output:
For each `.mat` file:
1. Two CSV files are generated:
   - `<BaseFileName>_Fly1.csv`
   - `<BaseFileName>_Fly2.csv`
2. Each CSV file contains two columns:
   - Column 1: Start times (`t0s` values).
   - Column 2: End times (`t1s` values).

Processing Details:
1. The script loops through all subfolders in the main folder.
2. For each `.mat` file:
   - It checks if the required fields (`t0s` and `t1s`) exist in `allScores`.
   - Extracts and processes data for `Fly1` and `Fly2`.
   - Filters out rows with missing (`NaN`) values.
   - Saves the data into CSV files in the same subfolder as the original `.mat` file.
3. If the required fields are missing or an error occurs during processing, a warning or error message is displayed.

---

Usage
1. Modify the main folder path:
   Update the `mainFolder` variable in the script to point to your target directory.
   Example:
   mainFolder = 'E:\Paulami\All cropped videos\test_SH\JAABAPlot_1';

2. Run the script in MATLAB.

---

Error Handling
- If a `.mat` file does not contain the expected `t0s` or `t1s` fields, a warning is logged.
- If any other errors occur while processing a file, the script will continue to process the remaining files, logging the error details for debugging.

---

Requirements
- MATLAB R2020b or later (recommended).
- Access to `.mat` files containing the expected `allScores` structure.

---

Notes
- Ensure your `.mat` files follow the expected structure before running the script.
- Adjust error handling or logging as needed for your specific use case.

---