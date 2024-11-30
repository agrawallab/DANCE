README: Extracting Continuous Series of 1s from `track.tsv` Files
---------------------------------------------------------------

Overview:
---------
This script processes `track.tsv` files located within subfolders of a given main folder of MateBook output files. It identifies continuous series of `1s` in a specified column of the TSV files and saves the results as CSV files in a designated output folder.

Features:
---------
1. Processes `track.tsv` files only if found in folders containing `DetectedArena_1` or `CustomArena_`.
2. Allows the user to specify the column name of interest interactively.
3. Identifies and extracts all continuous series of `1s` in the specified column.
4. Saves the results to an organized output folder (`matebook_output`) in CSV format.

Requirements:
-------------
- Python 3.x
- Pandas library for data manipulation.

Install dependencies if not already available: pip install pandas


Usage:
------
1. Clone or download the script.
2. Run the script in Python
3. Provide input:
- **Main folder path:** Enter the full path to the main folder containing subfolders with `track.tsv` files.
- **Column name:** Specify the column name (e.g., `following`) to analyze.

4. Output:
- Results are saved in the `matebook_output` folder within the specified main folder.
- The CSV filenames are generated dynamically and include:
  - The base name of the original file (minus the `track_` prefix).
  - The 5th folder component of the file path (if available).
  - The column name.

Output Example:
---------------
For a `track.tsv` file located at: <main_folder>/CustomArena_1/track_12345.tsv


If the user specifies the column `following`, the output file will be saved as:
<main_folder>/matebook_output/12345_CustomArena_1_following_extracted.csv


Each output CSV contains two columns: **start index** and **end index** of each continuous series of `1s`.

Error Handling:
---------------
- Skips invalid or corrupted files (`on_bad_lines='skip'`).
- Handles cases where the specified column is not found.

Additional Notes:
-----------------
- Ensure that `track.tsv` files are properly formatted, with headers in the **second row** and data starting from the **fifth row**.
- The script is customizable for different input file formats or header locations.




