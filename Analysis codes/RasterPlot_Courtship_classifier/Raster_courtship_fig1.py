import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

# Load the workbook
workbook_path = '/DANCE/Raster/Courtship/Courtship Raster Plot Figure 1.xlsx'

workbook = pd.ExcelFile(workbook_path)

# Get all sheet names
sheet_names = workbook.sheet_names

# Number of sheets
num_sheets = len(sheet_names)

# Create a figure to hold all subplots (5 subplots per sheet)
fig, axs = plt.subplots(3 * num_sheets, 1, figsize=(10, 0.7 * num_sheets),  # Reduce the overall height further
                        gridspec_kw={'hspace': 0.1})  # Reduce hspace to bring video instances closer

# Function to plot raster plots for durations with specified alignment and optional lines
def plot_raster(ax, bouts, color, alignment, add_bottom_line=False, add_top_line=False):
    if alignment == 'bottom':
        y_position = 0.15
    elif alignment == 'top':
        y_position = 0.85
    else:  # 'middle'
        y_position = 0.5
    
    for start, end in bouts:
        ax.plot([start, end], [y_position, y_position], color=color, lw=4.0)  # Align according to specified alignment
    ax.set_ylim(0, 1)  # Set ylim to align within the subplot
    ax.set_xlim(0, 15)
    
    # Add lines if specified
    if add_bottom_line:
        ax.axhline(y=0, color='black', linewidth=1)  # This should be added only to Matebook subplot
    if add_top_line:
        ax.axhline(y=1, color='gray', linewidth=1, alpha=0.5)  # Lighter top line for Ground-truth

# Define colors
raster_colors = {
    'Ground-truth': (128/255, 128/255, 128/255),  # Gray
    'JAABA': (238/255, 118/255, 66/255),         # Orange
    'Matebook': (146/255, 99/255, 209/255)       # Purple
}

# Loop through each sheet and plot the data
for i, sheet_name in enumerate(sheet_names):
    df = workbook.parse(sheet_name)
    
    # Convert frame numbers to time in minutes (assuming 30 fps)
    frame_rate = 30
    bouts_in_minutes1 = [(row['manual t0'] / (frame_rate * 60), row['manual t1'] / (frame_rate * 60)) for index, row in df.iterrows()]
    bouts_in_minutes2 = [(row['JAABA t0'] / (frame_rate * 60), row['JAABA t1'] / (frame_rate * 60)) for index, row in df.iterrows()]
    bouts_in_minutes3 = [(row['Matebook t0'] / (frame_rate * 60), row['Matebook t1'] / (frame_rate * 60)) for index, row in df.iterrows()]
    
    # Plot each set of behavior bouts in its respective subplot with specified alignment
    plot_raster(axs[3*i], bouts_in_minutes1, raster_colors['Ground-truth'], 'bottom', add_top_line=True)  # Add top line for Ground-truth
    plot_raster(axs[3*i+1], bouts_in_minutes2, raster_colors['JAABA'], 'middle')
    plot_raster(axs[3*i+2], bouts_in_minutes3, raster_colors['Matebook'], 'top', add_bottom_line=True)  # Add bottom line for Matebook

    # Set y-axis label for the first subplot of each sheet
    axs[3*i].set_ylabel(sheet_name, fontsize=12, labelpad=10, rotation=0, ha='right', va='center')  # Vertical alignment

# Remove extra legend entries by creating legend only once
legend_patches = [
    patches.Patch(color=raster_colors['Ground-truth'], label='Ground-truth'),
    patches.Patch(color=raster_colors['JAABA'], label='DANCE'),
    patches.Patch(color=raster_colors['Matebook'], label='Matebook')
]

# Add legend to the right of the plot area
# fig.legend(handles=legend_patches, loc='upper right', fontsize=12, frameon=False, bbox_to_anchor=(1.1, 1))

# Remove y-axis ticks and labels, and keep y-axis boundaries visible
for ax in axs:
    ax.set_yticks([])
    ax.set_yticklabels([])
    ax.spines['left'].set_visible(True)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

# Keep the bottom spine visible for the last subplot
axs[-1].spines['bottom'].set_visible(True)

# Set x-axis ticks and reduced font size
xticks = np.arange(0, 16, 5)
axs[-1].set_xticks(xticks)
axs[-1].tick_params(axis='x', labelsize=12)

# Hide x-axis for the top subplots
for ax in axs[:-1]:
    ax.xaxis.set_visible(False)

# Add vertical lines on both sides to create a box effect
for ax in axs:
    ax.axvline(x=0, color='black', linewidth=1)
    ax.axvline(x=15, color='black', linewidth=1)

# Save the figure as both PNG and PDF with 300 DPI
output_directory = '/DANCE/Raster/Courtship'
base_name = os.path.splitext(os.path.basename(workbook_path))[0]
plt.savefig(os.path.join(output_directory, f"{base_name}_aligned_raster_plot_og.png"), bbox_inches='tight', dpi=300)
plt.savefig(os.path.join(output_directory, f"{base_name}_aligned_raster_plot_og.pdf"), bbox_inches='tight', dpi=300)

# Show the plot
plt.show()

