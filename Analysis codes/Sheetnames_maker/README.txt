Create Excel Workbook with Sheets Script
=========================================

Description
-----------
This script generates an Excel workbook with multiple sheets and a common header in each sheet. Sheet names can be customized, and names longer than 31 characters are truncated automatically.

Features
--------
- Creates an Excel file with specified sheet names; experimental video's name.
- Adds a common header to each sheet [manual_t0, manual_t1, JAABA_t0, JAABA_t1, MatBbook_t0, Matebook_t1].
- Removes the default "Sheet" created by openpyxl.

Usage
-----
1. Modify the `sheet_names` list in the `main` function to include desired sheet names.
2. Set the `directory_path` and `file_name` for the Excel file.
3. Run the script, and the Excel file will be created in the specified location.

Headers
-------
Each sheet will include the following header by default:
`manual t0`, `manual t1`, `JAABA t0`, `JAABA t1`, `Matebook t0`, `Matebook t1`

Example
-------
- Sheet Names: `['Chamber_10', 'Chamber_11', 'test1', 'test2']`
- File Path: `E:\Paulami\Ground-truthing Data\...\Copulation_SB_Workbook.xlsx`

The script will create an Excel file with these sheets and the common header.

Notes
-----
- Ensure the `directory_path` exists before running the script.
- Sheet names longer than 31 characters will be truncated automatically.
