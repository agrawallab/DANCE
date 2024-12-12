
README for Raster Plot Generation Script - For courtship classifier

---

### Overview
This Python script processes a CSV file containing frame data from various behavioral analysis tools (e.g., Manual, DANCE, MateBook), across different courtship behaviors i.e. wing extension, circling, following, attempted copulation and copulation; and generates a raster plot visualization of these behaviors over a 20-minute period. The resulting plot is saved as a PNG image in the desired directory.

---

### Prerequisites

1. **Python Version**: Ensure you have Python 3.6 or newer installed.
2. **Required Libraries**:  
   Install the following Python libraries using `pip` or `conda`:
   - `pandas`
   - `matplotlib`
   - `numpy`
   - `os` (built-in with Python)

---

### Instructions

#### Step 1: Prepare the CSV File
1. Ensure your CSV file has the following columns (case-sensitive):
   - `Ground_truth_Fly1`, `Ground_truth_Fly2`
   - `DANCE_Fly1`, `DANCE_Fly2`
   - `MateBook_Fly1`, `MateBook_Fly2`
  
2. Missing columns are handled gracefully; the script processes available data.

#### Step 2: Run the Script
1. Save the script as `raster_plot.py` in a directory of your choice.
2. Execute the script: 
3. Provide the path to your CSV file when prompted:

#### Step 3: Output
- The script generates a raster plot for 5 different courtship behaviors.
- The image is saved in the chosen directory as input in the end.

Copy code
- The plot is also displayed during the execution.

---

### Plot Details

1. **Frame Data Conversion**:  
 Frame numbers are converted to minutes, assuming a frame rate of 30 frames per second (fps).

2. **Behavior Visualization**:  
 The plot includes 5 subplots which is further categorized as 'Ground_truth', 'DANCE' and 'MateBook'; each representing one behavior type:
 - `Ground-truth`
 - `DANCE`
 - `MateBook`

3. **Color Scheme**:
 - Manual: Grey (`#808080`)
 - DANCE: Red (`#F94040`)
 - CADABRA: Green (`#00EA64`)
 - Divider: Cyan (`#00C8C8`)

4. **Axis Configuration**:
 - X-axis shows time in minutes (0–15).
 - Y-axis labels indicate behavior type.

5. **Legend**:  
 A legend summarizing the behaviors and corresponding colors is added to the upper right of the plot.

---

### Customization Options

- **Frame Rate**:  
 Default is `30 fps`. Update the `frame_rate` variable if your video has a different frame rate.
- **Video Duration**:  
 The plot assumes a 15-minute duration. Modify the `ax.set_xlim(0, 15)` line to adjust this.

---

### Troubleshooting

1. **Missing Columns Error**:  
 Ensure your CSV contains at least one column for each behavior type.

2. **No Output Image**:  
 Check if the input directory has write permissions.

3. **Plot Overlaps**:  
 Adjust the figure dimensions in `fig, axs = plt.subplots(...)`.
