import pandas as pd
import os

def find_continuous_ones(data):
    """
    This function finds all the continuous series of 1s in the data and returns their starting and ending indices.
    """
    results = []
    start = None
    for i, v in enumerate(data):
        if v == 1 and start is None:
            start = i
        elif v == 0 and start is not None:
            results.append((start, i - 1))  # Ending index at i-1
            start = None
    if start is not None:
        results.append((start, len(data) - 1))
    return results

# Get the path of the main folder from user input
main_folder = input("What is the path of the main folder? ")

# Create a main folder for output files
output_main_folder = os.path.join(main_folder, "matebook_output")
os.makedirs(output_main_folder, exist_ok=True)

# Function to get column name from user
def get_column_name():
    while True:
        column_name = input("Enter the column name to extract (e.g., 'following'): ").strip()
        if column_name:
            return column_name
        else:
            print("Column name cannot be empty. Please try again.")

# Get column name from the user
column_name = get_column_name()

# Function to process each file
def process_file(file_path, column_name):
    try:
        # Load the TSV file
        data = pd.read_csv(file_path, sep='\t', header=None, on_bad_lines='skip', low_memory=False)

        # Extract column headers from the second row (change this if headers are in a different row)
        headers = data.iloc[1].tolist()

        # Check if the specified column exists
        if column_name in headers:
            print(f"Processing file: {file_path}")
            print(f"Column name found: {column_name}")

            # Extract data from specified column
            column_index = headers.index(column_name)
            data_list = pd.to_numeric(data.iloc[4:, column_index], errors='coerce')

            # Drop rows with NaN (not a number) values
            data_list = data_list.dropna()

            # Find continuous series of 1s
            results = find_continuous_ones(data_list)

            if results:
                # Create a DataFrame from results
                df = pd.DataFrame(results)

                # Extract the 5th component of the path (if it exists)
                path_components = file_path.split(os.path.sep)
                fifth_component = path_components[4] if len(path_components) > 4 else ""

                # Construct output filename without 'track_' prefix
                base_filename = os.path.splitext(os.path.basename(file_path))[0]
                if base_filename.startswith('track_'):
                    base_filename = base_filename[6:]  # Remove 'track_' prefix

                output_filename = f"{base_filename}_{fifth_component}_{column_name}_extracted.csv"
                output_path = os.path.join(output_main_folder, output_filename)

                # Save DataFrame to CSV in the main output folder without headers
                df.to_csv(output_path, index=False, header=False)
                print(f"Output saved to: {output_path}")
                print(df)
            else:
                print("No continuous 1s found.")

        else:
            print(f"Error: Column '{column_name}' not found in file: {file_path}")

    except Exception as e:
        print(f"Error processing file: {file_path}. Exception: {e}")

# Iterate through subfolders and process 'track.tsv' files
for root, dirs, files in os.walk(main_folder):
    for name in files:
        if name == "track.tsv" and ("DetectedArena_1" in root or "CustomArena_" in root):
            file_path = os.path.join(root, name)
            process_file(file_path, column_name)
