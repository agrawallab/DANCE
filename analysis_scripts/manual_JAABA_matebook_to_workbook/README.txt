README for CSV to Workbook Integration Script
=============================================

## Purpose
This Python script processes CSV files from three different folders and writes their data into an Excel workbook. Each CSV file is matched to a specific sheet in the workbook, and the data is written to specified columns starting from the second row.

---

## Features
1. **Dynamic Workbook Detection**:
   - Automatically locates an Excel workbook file in the main folder that ends with "Workbook.xlsx".

2. **Multiple Folder Handling**:
   - Reads CSV files from three subfolders: `manual_output_files`, `JAABA_output`, and `matebook_output`.
   - Processes data from each folder separately and writes it into appropriate workbook sheets.

3. **Flexible Sheet Naming**:
   - Derives sheet names from CSV filenames, stripping prefixes, suffixes, or specific patterns (e.g., "_output", "track_", etc.).

4. **Custom Column Writing**:
   - Writes data from the first folder into columns 1 and 2.
   - Writes data from the second folder into columns 3 and 4.
   - Writes data from the third folder into columns 5 and 6.

5. **JAABA Name Stripping**:
   - Allows the user to specify parts of JAABA filenames to be removed when deriving sheet names.

---

## Usage Instructions

### Prerequisites
- Python 3.x
- Required Python libraries: `os`, `csv`, `glob`, and `openpyxl`.
- An Excel workbook file ending with "Workbook.xlsx" in the main folder.
- Three subfolders under the main folder: `manual_output_files`, `JAABA_output`, and `matebook_output`.

### Steps
1. Run the script and provide the main folder's path when prompted.
2. Specify the parts of JAABA filenames to strip when prompted.
3. The script will:
   - Locate the workbook file and read its sheets.
   - Process CSV files in each folder and write their data to the appropriate columns in matching workbook sheets.
4. The workbook will be updated and saved.

### Input File Requirements
#### CSV Files:
- Three subfolders with the respective scores in csv files, to be named as (can be changed) - 
 - "manual_output"
 - "JAABA_output"
 - "Matebook_output"
 - "name_Workbook.xlsx"

- Formats:
  - **Folder 1**: Columns written to the 1st and 2nd columns.
  - **Folder 2**: Columns written to the 3rd and 4th columns.
  - **Folder 3**: Columns written to the 5th and 6th columns. 

