# README: Lunges Data Processing Script

## Overview
This script processes lunge timestamp data for two flies recorded in text files. The goal is to convert timestamps into frame numbers (assuming 30 frames per second), adjust frames by ±1, and save the processed data into CSV files.

---

## Requirements
- **Programming Language**: R
- **Required Libraries**:
  - `tidyverse`
  - `dplyr`

---

## File Structure
- **Input Files**: Text files with lunges timestamp data located in:
  - `~/Documents/Scripts/CADABRA/Tables/tables_0326`
  - `~/Documents/DANCE/CADABRA/CADABRA_framedata/Tables/tables_0401`
- **Output Files**: Processed CSV files saved in the working directory.

---

## How to Run
1. **Set Up Environment**:
   - Install required libraries if not already installed:
     ```R
     install.packages("tidyverse")
     install.packages("dplyr")
     ```

2. **Run the Script**:
   - Open RStudio.
   - Set the working directory using:
     ```R
     setwd("~/Documents/Scripts/CADABRA/Tables/tables_0326")
     ```
   - Source the script or copy-paste it into the R console.

3. **Bulk Processing**:
   - To process multiple files, set the working directory to:
     ```R
     setwd("~/Documents/DANCE/CADABRA/CADABRA_framedata/Tables/tables_0401")
     ```
   - The script will automatically loop through all `.txt` files and save the processed CSV files.

---

## Script Logic
1. **Read Data**:
   - Read the input text file, skipping the first 3 lines.
   
2. **Data Cleaning**:
   - Remove unnecessary columns.
   - Rename columns to `Timestamps_Fly1` and `Timestamps_Fly2`.
   
3. **Data Conversion**:
   - Convert timestamps to numeric.
   - Multiply timestamps by 30 to get frame numbers.
   
4. **Data Transformation**:
   - Create `Frames_plus1` and `Frames_minus1`.
   - Rearrange and merge frames data.

5. **Save Data**:
   - Save the final data frame as a CSV file with a `processed_` prefix.

---

## Example Output
Sample processed CSV file structure:

| Fly            | Type          | Frames |
|----------------|----------------|--------|
| Frames_Fly1    | Frames_minus1 | 599   |
| Frames_Fly1    | Frames         | 600   |
| Frames_Fly1    | Frames_plus1  | 601   |
| Frames_Fly2    | Frames_minus1 | 1200  |
| Frames_Fly2    | Frames         | 1201  |

---

## Notes
- The frame rate is assumed to be 30 frames per second.
- Ensure that the input files follow the same structure.
- Processed files are saved with the prefix `processed_` to avoid overwriting.

---



