# Last edited by Paulami Dey on 28/11/2024

import csv
import os

input_file = input("What is the input file path?")

# Create a directory to store output files
output_folder = os.path.join(os.path.dirname(input_file), 'manual_output_files')
os.makedirs(output_folder, exist_ok=True)

# Dictionary to store data for each unique path
path_data = {}

# Dictionary to count occurrences of each video path
video_count = {}

# Read the input CSV file
try:
    with open(input_file, 'r') as f_in:
        reader = csv.reader(f_in)
        
        for row in reader:
            path = os.path.dirname(row[0])  # Extract the directory path
            
            # If the path is not in the dictionary, create a new list
            if path not in path_data:
                path_data[path] = []
            
            # Append the third and fourth columns to the list corresponding to the path
            path_data[path].append([row[2], row[3]])
            
            # Count occurrences of video paths (assuming path is in column 0)
            video_path = row[0]
            if video_path in video_count:
                video_count[video_path] += 1
            else:
                video_count[video_path] = 1

    # Print basenames of the paths and collect them in a list
    video_names_list = []
    for path in path_data.keys():
        basename = os.path.basename(path)
        print(basename)
        video_names_list.append(basename)

    # # Add additional names to the list
    # additional_names = ['Chamber_5', 'test3_3']
    # video_names_list.extend(additional_names)

    # Write data to separate CSV files for each unique path
    for path, data in path_data.items():
        output_file = os.path.join(output_folder, f'{os.path.basename(path)}_output.csv')
        print("Output file path:", output_file)  # Print the output file path
        with open(output_file, 'w', newline='') as f_out:
            writer = csv.writer(f_out)
            writer.writerows(data)

    # Output video path counts
    print("Video path counts:")
    for path, count in video_count.items():
        print(f"{path}: {count}")

    # Save the video path counts to a CSV file if needed
    count_output_file = os.path.join(output_folder, 'video_path_counts.csv')
    with open(count_output_file, 'w', newline='') as count_out:
        writer = csv.writer(count_out)
        writer.writerow(["Video Path", "Count"])
        for path, count in video_count.items():
            writer.writerow([path, count])

    # Output the video names list
    print("Video names list:")
    print(video_names_list)

except FileNotFoundError:
    print("Error: Input file not found.")
except PermissionError:
    print("Error: Permission denied for input file.")
except Exception as e:
    print("Error:", e)
