# Last edited by Paulami Dey on 28/11/2024

import os
import shutil
import csv
import glob
import matlab.engine

# Change this as required
classifier_names = ["scores_AC_10", "scores_C_v4", "scores_Circling", "scores_Following14", "scores_WingExt_26"]

def rename_files_recursively(root_path):
    # Create score files folder
    score_folder = "score_files"
    new_path = os.path.join(root_path, score_folder)
    
    if os.path.exists(new_path):
        shutil.rmtree(new_path)
        print("Score_files_folder already exists, deleting old data")
    
    os.mkdir(new_path)  # Make a new score_files directory
    print(f"Created directory: {new_path}")

    for dir in os.listdir(root_path):
        dir_path = os.path.join(root_path, dir)
        if os.path.isdir(dir_path):
            for subdir in os.listdir(dir_path):
                subdir_path = os.path.join(dir_path, subdir)
                if os.path.isdir(subdir_path):
                    for folder in os.listdir(subdir_path):
                        folder_path = os.path.join(subdir_path, folder)
                        if os.path.isdir(folder_path):
                            for sub_folder in os.listdir(folder_path):
                                sub_folder_path = os.path.join(folder_path, sub_folder)
                                if os.path.isdir(sub_folder_path): 
                                    for file in os.listdir(sub_folder_path):
                                        file_path = os.path.join(sub_folder_path, file)
                                        name, extension = os.path.splitext(file)
                                        for classifier_name in classifier_names:
                                            if classifier_name in name:
                                                new_name = os.path.join(new_path, f"{dir}_{subdir}_{name}{extension}")
                                                # os.rename(file_path, new_name)
                                                print(name, new_name)
                                                shutil.copy(file_path, new_name)
                                                break  # Move to next file after copying

    print(f"Score files were renamed and copied to {new_path}")

def extract_lunge_frames_to_csv(root_path):
    os.chdir(os.path.join(root_path, "score_files"))
    eng = matlab.engine.start_matlab()
    eng.SheetMaker(nargout=0)
    eng.quit()

def compile_csv_files(root_path):
    path = os.path.join(root_path, "score_files")
    extension = 'csv'
    os.chdir(path)
    filenames = glob.glob(f'*.{extension}')
    print(filenames)

    list_of_males =[]
        
    for file in filenames:
        if "scores_WingExt" in file:
            filename = str(file)
            rows = []
            # Reading CSV file
            with open(filename, 'r') as csvfile:
                csvreader = csv.reader(csvfile)
                for row in csvreader:
                    rows.append(row)

            for n in range(0, len(rows), 2):
                lunges1 = 0
                lunges2 = 0
                for col in rows[n]:
                    if col != "NaN":
                        lunges1 += 1
                for col in rows[n + 1]:
                    if col != "NaN":
                        lunges2 += 1
                if lunges1>lunges2:
                    list_of_males.append(0)
                else:
                    list_of_males.append(1)
        
    print(list_of_males)

    for classifier_name in classifier_names:
        new_filename = f"{classifier_name}_compiled.csv"
        new_rows = []

        i = 0
        for file in filenames:
            if classifier_name in file:
                i = i+1
                filename = str(file)
                rows = []
                # Reading CSV file
                with open(filename, 'r') as csvfile:
                    csvreader = csv.reader(csvfile)
                    for row in csvreader:
                        rows.append(row)
                
                new_row = [f"{filename}_Fly1_Fly2"]

                for n in range(0, len(rows), 2):
                    lunges1 = 0
                    lunges2 = 0
                    for col in rows[n]:
                        if col != "NaN":
                            lunges1 += 1
                    for col in rows[n + 1]:
                        if col != "NaN":
                            lunges2 += 1
                    new_row.append(lunges1)
                    new_row.append(lunges2)
                    if list_of_males[i-1] == 0:
                        new_row.append(lunges1)
                    else:
                        new_row.append(lunges2)
                new_rows.append(new_row)

        with open(new_filename, 'w', newline="") as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(new_rows)
        print(f"Compiled CSV file created: {new_filename}")

def main():
    while True:
        root_path = input("What is the complete path of the parent folder containing all videos and JAABA folders?")
        rename_files_recursively(root_path)
        extract_lunge_frames_to_csv(root_path)
        compile_csv_files(root_path)
        continue

if __name__ == "__main__":
    main()
