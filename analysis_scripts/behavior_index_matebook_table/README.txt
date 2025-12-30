XLSX to CSV Metrics Calculator
================================

Description
-----------
This Python script reads an XLSX file with multiple sheets, calculates specific metrics based on predefined columns, 
and writes the results to a CSV file. The calculations involve computing indices for `manual`, `JAABA`, and `Matebook` 
annotations by performing operations on time columns within each sheet.

Prerequisites
-------------
Before using this script, ensure you have the following installed on your system:

- Python 3.x
- Required Python libraries:
  - pandas
  - openpyxl
  - csv

You can install the necessary libraries by running:
    pip install pandas openpyxl

Usage
-----
1. Save the script to a file, e.g., `xlsx_to_csv_metrics.py`.
2. Run the script in a Python environment:
       python xlsx_to_csv_metrics.py
3. Follow the prompts:
   - Provide the full path to the input XLSX file.
   - Enter a name for the output file (the script will prepend "output_" to your specified name).

Example
-------
If your XLSX file is located at `C:\Users\Paulami\metrics.xlsx`:
- Enter `C:\Users\Paulami\metrics.xlsx` when prompted for the file's path.
- Enter `results` when prompted for the final file name.

The script will create a CSV file named `output_results.csv` in the same directory as the input file.

Script Details
--------------
1. **Input File**: The script accepts an XLSX file with multiple sheets. Each sheet should have the following required columns:
   - `manual t0`
   - `manual t1`
   - `JAABA t0`
   - `JAABA t1`
   - `Matebook t0`
   - `Matebook t1`

2. **Calculations**:
   - E = manual t1 - manual t0
   - F = JAABA t1 - JAABA t0
   - G = Matebook t1 - Matebook t0
   - The script computes sums for each of these (`sum_of_E`, `sum_of_F`, `sum_of_G`) and divides them by 27,000 to calculate indices:
     - Manual Index: sum_of_E / 27000
     - JAABA Index: sum_of_F / 27000
     - Matebook Index: sum_of_G / 27000

3. **Output File**:
   - The script creates a CSV file with the following structure:
        Sheet Name   | Manual Index | JAABA Index | Matebook Index 
        ----------------------------------------------------------
        Sheet1       | 0.123        | 0.456       | 0.789         

Error Handling
--------------
The script includes basic error handling:
- **FileNotFoundError**: If the specified file is not found, the script will prompt you to check the file path.
- **General Exceptions**: Any other errors will display an appropriate message with details.

