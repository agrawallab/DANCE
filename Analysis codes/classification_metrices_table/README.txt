Overlap Tuple Analysis and Metrics Calculator
==============================================

Description
-----------
This Python script processes an Excel file (`.xlsx`) containing time intervals from multiple sheets to analyze overlapping tuples 
between datasets (`Manual`, `JAABA`, and `Matebook`). It calculates metrics like true positives, false positives, 
false negatives, precision, recall, and F1 scores. The results are written to a CSV file.

Prerequisites
-------------
Ensure you have the following installed on your system:

- Python 3.x
- Required Python libraries:
  - openpyxl
  - csv

You can install the necessary library by running:
    pip install openpyxl

Usage
-----
1. Save the script to a file, e.g., `overlap_analysis.py`.
2. Run the script in a Python environment:
       python overlap_analysis.py
3. Follow the prompts:
   - Provide the full path to the input XLSX file.
   - Enter a name for the output file (the script will prepend "output_" to your specified name).

Example
-------
If your XLSX file is located at `C:\Users\Paulami\data.xlsx`:
- Enter `C:\Users\Paulami\data.xlsx` when prompted for the file's path.
- Enter `results` when prompted for the final file name.

The script will create a CSV file named `output_results.csv` in the same directory as the input file.

Script Details
--------------
1. **Input File**: The script accepts an XLSX file with multiple sheets. Each sheet should contain the following columns:
   - A, B: Time intervals for `Manual` annotations
   - C, D: Time intervals for `JAABA` annotations
   - E, F: Time intervals for `Matebook` annotations

2. **Processing**:
   - Extracts tuples of start and end times from columns (A&B, C&D, E&F).
   - Compares intervals (`Manual vs JAABA` and `Manual vs Matebook`) to find overlapping tuples:
     - `True Positives`: Tuples in both datasets overlap.
     - `False Negatives`: Tuples in the reference dataset (`Manual`) with no overlaps.
     - `False Positives`: Tuples in the test dataset with no overlaps in the reference.
   - Calculates precision, recall, and F1 scores for both comparisons.

3. **Output File**:
   - The script creates a CSV file with metrics for each sheet:
        Sheet Name | True Positives | False Positives | False Negatives | Precision | Recall | F1 Score | ...
        -----------------------------------------------------------------------------------------------
        Sheet1     | 100            | 20              | 10              | 0.83      | 0.91   | 0.87     | ...
   - Includes separate metrics for `Manual vs JAABA` and `Manual vs Matebook`.

4. **Error Handling**:
   - **FileNotFoundError**: Prompts the user to check the file path.
   - **General Exceptions**: Displays an error message with details.

Metrics Calculation
-------------------
For each dataset pair:
- **Precision** = True Positives / (True Positives + False Positives)
- **Recall** = True Positives / (True Positives + False Negatives)
- **F1 Score** = 2 * (Precision * Recall) / (Precision + Recall)


