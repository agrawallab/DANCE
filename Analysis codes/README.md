# DANCE: Drosophila Aggression and Courtship Evaluator

The following are the codes that have been used for various steps during the development and testing of the aggression and courtship classifiers.

## I. Ground-Truthing Labels

### 1. `extractLabels`
**Description**: Extracts manual ground-truth labels from a `test.jab` file and saves them into a `test.csv` file.  
**Input**: `test.jab` (input)  
**Output**: `test.csv` (output)

### 2. `individual_video_manual_labels`
**Description**: Processes `test.csv` to calculate the number of bouts (`t0` and `t1` values) for all videos listed. Outputs individual files for each video and a summary file of total bouts.  
**Input**: `test.csv`  
**Outputs**:  
- Individual bout files per video  
- `video_path_counts.csv` (contains total bout counts for each video along with their names)

### 3. `Sheetnames_maker`
**Description**: Takes a list of video names and generates an empty `test.xlsx` file with each video as a separate sheet. Each sheet includes a common header:  
`['manual_t0', 'manual_t1', 'JAABA_t0', 'JAABA_t1', 'Matebook_t0', 'Matebook_t1']`.  
**Input**: List of video names (output from `individual_video_manual_labels`)  
**Output**: `test_Workbook.xlsx`

---

## II. DANCE Classifier (using JAABA) Score Files

### 1. `SheetMaker_postprocessed`
**Description**: Processes a directory containing JAABA folders with score files to extract individual Fly1 and Fly2 bouts (`t0` and `t1` values).  
**Input**: Directory containing JAABA folders with score files  
**Output**: Files for Fly1 and Fly2 with `t0` and `t1` values

### 2. `renaming_JAABA_scorefiles`
**Description**: Renames the Fly1 and Fly2 score file outputs to include corresponding video names for better traceability.  
**Input**: Score file outputs from `SheetMaker_postprocessed`  
**Output**: Renamed score files

---

## III. Matebook Score Files

### 1. `Matebook_indiviual_output_scores`
**Description**: Processes `track.tsv` files within a specified folder structure. It extracts continuous series of `1s` from a user-specified column and saves the results as individual CSV files. The script ensures proper handling of file names, missing data, and output structure.  
**Input**:  
- Main folder path: The directory path containing the `track.tsv` files  
- Column name: The column to process (e.g., `following`) from the `track.tsv` files  
**Output**: A folder named `matebook_output` within the main folder path containing the processed CSV files. Each CSV file includes the start and end indices of continuous sequences of `1s`.

---

## IV. Compiled Score Files from Different Methods

### 1. `manual_JAABA_mateBook_to_workbook`
**Input Folder Structure**:  
The input folder should contain the following:
- Manual output, JAABA output, and Matebook output folders, each corresponding to their respective methods.
- Inside each method folder, individual CSV files should be created for each video, with the video name as the file name. These CSV files should contain the scores for `t0` and `t1`, organized accordingly.
- The folder should also include a `text_Workbook.xlsx` file.

**Code Functionality**:  
The code compiles all the score files from the `manual_output`, `JAABA_output`, and `Matebook_output` folders. The scores from each individual CSV file are compiled into the `text_Workbook.xlsx` file, with a common header that includes the relevant data for `t0` and `t1`.

---

## V. Analyzing the Scores from Different Methods

### 1. `Overlap_analyzer`
**Description**: Analyzes overlaps between bouts from each method and provides detailed information on overlaps and missed overlaps. Calculates the total number of true positives, false positives, and false negatives based on the overlap analysis.  
**Input**: Path to the `test_Workbook.xlsx` file

### 2. `Classification_metrices_table`
**Description**: Counts the number of True Positives (TP), False Positives (FP), and False Negatives (FN) for each video. Calculates the Precision, Recall, and F1 score for each video based on these counts.

### 3. `behavior_index_table`
**Description**: Calculates the behavior index for each video and presents the results in a tabular format.

---

## VI. Analyzing Behavior Videos

### 1. `Simplyfly_cropper_v4`
**Description**: This code takes a folder containing experimental videos, detects the circles within the videos, and automatically crops the chambers. The cropped chambers are saved in individual folders for each video.

### 2. `courtship_bout_num_extractor/unsegmented`
**Description**: Automates the analysis of behavioral data from JAABA outputs of cropped chamber videos by performing the following tasks:

- **Rename Files Recursively**: Renames and copies classifier score files from nested directories into a centralized folder (`score_files`) for easy access, with classifier names predefined in the script.
- **Extract Courtship Behavior Frames**: Uses a MATLAB function (`SheetMaker`) to extract and save courtship behavior frames into CSV format.
- **Compile CSV Files**: Aggregates courtship behavior data from multiple classifiers into new CSV files, identifying dominant flies based on behavioral counts.

**Versions**:  
- **Cropped Videos**: Processes videos that are pre-cropped, performing tasks like renaming files, extracting courtship behavior frames, and compiling CSV files based on classifier outputs.
- **Unsegmented Videos**: Handles unsegmented videos by applying additional segmentation steps before performing the same analysis tasks as for cropped videos.

### 3. `RasterPlots_one_frame_classifier`
**Description**: For one-frame behaviors (e.g., lunges).  
This Python script processes a CSV file containing frame data from various behavioral analysis tools (e.g., Manual, DANCE, CADABRA, Divider) and generates a raster plot visualization of these behaviors over a 20-minute period. The resulting plot is saved as a PNG image in the same directory as the input CSV file.

### 4. `RasterPlot`
**Description**: For duration-based behaviors (e.g., wing extension, following, circling, attempted-copulation, copulation).  
This Python script processes a CSV file containing frame data from various behavioral analysis tools (e.g., Manual, DANCE, and Matebook) and generates a raster plot visualization of these behaviors over a 15-minute period. The resulting plot is saved as a PNG image in the same directory as the input CSV file.

---

## Repository Link
[DANCE/Analysis codes at main · agrawallab/DANCE](#)
