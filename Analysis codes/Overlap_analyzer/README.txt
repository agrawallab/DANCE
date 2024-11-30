OverlapAnalyzer README

Overview
--------
The OverlapAnalyzer script processes Excel sheets containing tuples and analyzes overlaps between different tuple sets.
It calculates true positives, false positives, and false negatives, and computes performance metrics like precision, recall, and F1 score.

Features
--------
1. Processes multiple sheets from an Excel workbook.
2. Supports comparison between three sets of tuples:
   - Manual vs. JAABA
   - Manual vs. Matebook
3. Computes overlap counts and performance metrics:
   - True Positives (TP)
   - False Positives (FP)
   - False Negatives (FN)
   - Precision, Recall, F1 Score
4. Outputs results into a well-structured CSV file.

Requirements
------------
- Python 3.x
- Required libraries:
  - os
  - openpyxl
  - csv

Usage
-----
1. Place your Excel file in a known location.
2. Run the script and provide:
   - The full path to the Excel file.
   - A name for the output CSV file.
3. The script will process each sheet and save results in the specified CSV file.

Input Format
------------
- The Excel file should contain:
  - Columns A & B: Tuple data for the "Manual" set.
  - Columns C & D: Tuple data for the "JAABA" set.
  - Columns E & F: Tuple data for the "Matebook" set.

Output
------
The script generates a CSV file containing:
1. Overlap results for each sheet.
2. Performance metrics:
   - Precision
   - Recall
   - F1 Score

Error Handling
--------------
- FileNotFoundError: Prompts if the provided file path is invalid.
- Other exceptions are logged with an error message.