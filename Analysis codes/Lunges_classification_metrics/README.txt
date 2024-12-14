# README: Data Metrics Processing Script

## Overview
This script processes CSV files containing timestamp and frame data for multiple flies. It calculates key metrics such as True Positives (TP), False Positives (FP), False Negatives (FN), Precision, Recall, and F1 scores by comparing models (`DANCE`, `CADABRA`, and `Divider`) against the ground truth data.

---

## Requirements
- **Programming Language**: R
- **Required Libraries**:
  - `tidyverse`
  - `dplyr`
  - `ggplot2`

---

## File Structure
- **Input Files**: CSV files with timestamp and frame data located in:
  - `~/Documents/DANCE/Modified tables`
- **Output Files**: Processed CSV files saved in:
  - `~/Documents/DANCE/modified tables`
- **Log File**: A single log file `all_files_log.txt` for all outputs.

---

## How to Run
1. **Set Up Environment**:
   - Install required libraries if not already installed:
     ```R
     install.packages("tidyverse")
     install.packages("dplyr")
     install.packages("ggplot2")
     ```

2. **Run the Script**:
   - Open RStudio.
   - Set the working directory using:
     ```R
     setwd("~/Documents/DANCE/Modified tables")
     ```
   - Source the script or copy-paste it into the R console.

3. **Bulk Processing**:
   - The script will automatically loop through all `.csv` files and save processed metrics results.

---

## Script Logic
1. **Read Data**:
   - Load the input CSV files.
   - Extract relevant columns for each fly and model.

2. **Data Cleaning and Length Adjustment**:
   - Ensure consistent vector lengths using padding or truncation.
   - Remove rows where all values are `NA`.

3. **Metrics Calculation**:
   - Compare ground truth data against each model.
   - Calculate TP, FP, FN, Precision, Recall, and F1 scores.

4. **Save Data**:
   - Save metrics results for each file.
   - Compile an overall summary CSV file.

---

## Example Output
Sample processed metrics CSV file:

| Comparison               | True_Positives | False_Positives | False_Negatives | Precision | Recall | F1_Score |
|--------------------------|----------------|----------------|----------------|-----------|--------|----------|
| Groundtruth vs DANCE     | 100            | 20             | 10             | 0.83      | 0.91   | 0.87     |
| Groundtruth vs CADABRA   | 95             | 25             | 15             | 0.79      | 0.86   | 0.82     |
| Groundtruth vs Divider   | 90             | 30             | 20             | 0.75      | 0.82   | 0.78     |

---

## Notes
- Ensure the input files follow the expected structure.
- Processed files are saved with informative file names to avoid overwriting.

---

## Contact
For questions or issues, please reach out to the Agrawal Lab research team.


