# Last edited by Paulami Dey on 28/11/2024

import os

def rename_csv_files_in_subfolders(main_folder_path):
    # Iterate over each subfolder in the main folder
    for subfolder_name in os.listdir(main_folder_path):
        subfolder_path = os.path.join(main_folder_path, subfolder_name)
        
        if os.path.isdir(subfolder_path):
            # Remove '_JAABA' from the subfolder name if present
            clean_subfolder_name = subfolder_name.replace('_JAABA', '')
            
            # List all files in the subfolder
            files = os.listdir(subfolder_path)
            
            for file_name in files:
                # Check if the file is a CSV file and matches the pattern "scores_" and "_Fly1.csv" or "_Fly2.csv"
                if file_name.startswith('scores') and file_name.endswith('.csv') and ("_Fly1" in file_name or "_Fly2" in file_name):
                    # Construct the new file name by replacing the old substring with the clean subfolder name
                    if "_Fly1" in file_name:
                        new_file_name = f"{clean_subfolder_name}_{Classifier_name}_Fly1.csv"
                    elif "_Fly2" in file_name:
                        new_file_name = f"{clean_subfolder_name}_{Classifier_name}_Fly2.csv"
                    
                    # Construct the full paths
                    old_file_path = os.path.join(subfolder_path, file_name)
                    new_file_path = os.path.join(subfolder_path, new_file_name)
                    
                    # Check if the new file already exists and append a unique identifier if needed
                    counter = 1
                    while os.path.exists(new_file_path):
                        new_file_name = f"{clean_subfolder_name}_Fly1_{counter}.csv" if "_Fly1" in file_name else f"{clean_subfolder_name}{Classifier_name}_Fly2_{counter}.csv"
                        new_file_path = os.path.join(subfolder_path, new_file_name)
                        counter += 1
                    
                    # Rename the file
                    os.rename(old_file_path, new_file_path)
                    print(f"Renamed '{file_name}' to '{new_file_name}'")

# Example usage:
main_folder_path = input("What is the file's path?")
Classifier_name = input("Enter the classifier name: ")
rename_csv_files_in_subfolders(main_folder_path)
