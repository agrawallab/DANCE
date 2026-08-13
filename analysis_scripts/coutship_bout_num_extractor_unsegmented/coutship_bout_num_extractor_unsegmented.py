# Last edited by Paulami Dey on 12/08/2026

import os
import shutil
import csv
import glob
import scipy.io
import numpy as np

# Change this as required
classifier_names = ["scores_Attempted_copulation", "scores_Copulation", "scores_Circling", "scores_Following", "scores_WingExt"]

def rename_files_recursively(root_path):

    score_folder = "score_files"
    new_path = os.path.join(root_path, score_folder)

    if os.path.exists(new_path):
        shutil.rmtree(new_path)
        print("score_files folder already exists, deleting old data")

    os.makedirs(new_path, exist_ok=True)
    print(f"Created directory: {new_path}")

    copied_files = 0
    jaaba_folders_found = 0

    for current_root, dirs, files in os.walk(root_path):

        # Skip the output score_files folder
        if os.path.abspath(current_root).startswith(os.path.abspath(new_path)):
            continue

        # Only look inside folders ending with _JAABA
        if os.path.basename(current_root).endswith("_JAABA"):

            jaaba_folders_found += 1
            jaaba_folder_name = os.path.basename(current_root)

            print(f"\nFound JAABA folder: {current_root}")

            # Search everything inside this JAABA folder
            for jaaba_root, jaaba_dirs, jaaba_files in os.walk(current_root):

                for file in jaaba_files:

                    name, extension = os.path.splitext(file)

                    for classifier_name in classifier_names:

                        if classifier_name in name:

                            file_path = os.path.join(jaaba_root, file)

                            video_name = jaaba_folder_name.replace("_JAABA", "")

                            new_name = os.path.join(
                                new_path,
                                f"{video_name}_{file}"
                            )

                            print(f"Copying: {file}")
                            print(f" -> {new_name}")

                            shutil.copy2(file_path, new_name)

                            copied_files += 1
                            break

    print("\n------------------------------------")
    print(f"JAABA folders found: {jaaba_folders_found}")
    print(f"Score files copied: {copied_files}")
    print(f"Output folder: {new_path}")
    print("------------------------------------")

    if jaaba_folders_found == 0:
        print("WARNING: No folders ending with '_JAABA' were found.")

    if copied_files == 0:
        print("WARNING: JAABA folders were found, but no matching score files were found.")

def sheet_maker(folder_path):
    """Reads JAABA .mat score files in folder_path and writes one CSV per .mat file.
    Each row in the CSV holds the bout frame numbers for one fly (row 0 = Fly1,
    row 1 = Fly2, and for unsegmented videos additional row-pairs follow for
    each extra fly-pair stacked in the same .mat file).
    Uses allScores.scores > 0 to find bout frames (robust for single-frame classifiers
    where t0s/t1s can be empty after post-processing)."""
    for mat_file in glob.glob(os.path.join(folder_path, '*.mat')):
        base_name = os.path.splitext(os.path.basename(mat_file))[0]
        out_filename = os.path.join(folder_path, base_name + ".csv")
        try:
            data = scipy.io.loadmat(mat_file, squeeze_me=True, struct_as_record=False)
            all_scores = data['allScores']
            if hasattr(all_scores, 'scores') and hasattr(all_scores, 'tStart'):
                t_start = np.atleast_1d(all_scores.tStart)
                scores_list = np.atleast_1d(all_scores.scores)
                rows = []
                for idx in range(len(scores_list)):
                    fly_scores = np.atleast_1d(scores_list[idx]).flatten()
                    bout_frames = (np.where(fly_scores > 0)[0] + int(t_start[idx])).tolist()
                    rows.append(bout_frames)
                with open(out_filename, 'w', newline='') as f:
                    csv.writer(f).writerows(rows)
            else:
                print(f"File {mat_file} does not contain expected fields: scores or tStart")
        except NotImplementedError:
            print(f"File {mat_file} is MATLAB v7.3 (HDF5) format — install h5py to read it")
        except Exception as e:
            print(f"Error processing file {mat_file}: {e}")

def extract_lunge_frames_to_csv(root_path):
    sheet_maker(os.path.join(root_path, "score_files"))

def compile_csv_files(root_path):

    path = os.path.join(root_path, "score_files")
    os.chdir(path)

    filenames = glob.glob("*.csv")

    print(f"\nTotal CSV files found: {len(filenames)}")

    # ==================================================
    # STEP 1: Find male identity for EVERY fly-pair in
    # every WingExt file (unsegmented videos = each file
    # can contain multiple Fly1/Fly2 pairs stacked as
    # consecutive row-pairs, not just one pair per file)
    # ==================================================

    # Keyed by (chamber_name, pair_index) -> 0 (Fly1 is male) or 1 (Fly2 is male)
    male_by_pair = {}

    wing_files = sorted([
        file for file in filenames
        if "scores_WingExt" in file
    ])

    print(f"WingExt files found: {len(wing_files)}")

    for file in wing_files:

        chamber_name = file.split("_scores_WingExt")[0]

        rows = []

        with open(file, "r") as csvfile:
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                rows.append(row)

        if len(rows) < 2:
            print(f"WARNING: Invalid WingExt file (fewer than 2 rows): {file}")
            continue

        for n in range(0, len(rows), 2):

            if n + 1 >= len(rows):
                print(f"WARNING: {file} has an odd number of rows, last row skipped.")
                break

            pair_index = n // 2

            wingext1 = 0
            wingext2 = 0

            for col in rows[n]:
                if col != "NaN":
                    wingext1 += 1

            for col in rows[n + 1]:
                if col != "NaN":
                    wingext2 += 1

            if wingext1 > wingext2:
                male_by_pair[(chamber_name, pair_index)] = 0
                male = "Fly1"
            else:
                male_by_pair[(chamber_name, pair_index)] = 1
                male = "Fly2"

            print(
                f"{chamber_name} pair {pair_index}: "
                f"Fly1 WingExt = {wingext1}, "
                f"Fly2 WingExt = {wingext2} "
                f"--> Male = {male}"
            )

    # ==================================================
    # STEP 2: Show which classifiers exist per chamber
    # ==================================================

    print("\n======================================")
    print("CHECKING CLASSIFIERS PER CHAMBER")
    print("======================================")

    all_chambers = set()

    for file in filenames:
        for classifier_name in classifier_names:
            if classifier_name in file:

                chamber_name = file.split(
                    f"_{classifier_name}"
                )[0]

                all_chambers.add(chamber_name)
                break

    for chamber_name in sorted(all_chambers):

        print(f"\n{chamber_name}")

        for classifier_name in classifier_names:

            found = any(
                file.startswith(chamber_name + "_")
                and classifier_name in file
                for file in filenames
            )

            if found:
                print(f"   ✓ {classifier_name}")
            else:
                print(f"   ✗ MISSING: {classifier_name}")

        has_male_data = any(
            key[0] == chamber_name for key in male_by_pair
        )

        if not has_male_data:
            print("   !!! NO VALID WingExt → male cannot be identified")

    # ==================================================
    # STEP 3: Compile classifier files
    # (each file may contain multiple fly-pairs)
    # ==================================================

    print("\n======================================")
    print("COMPILING FILES")
    print("======================================")

    for classifier_name in classifier_names:

        new_filename = f"{classifier_name}_compiled.csv"
        new_rows = []

        classifier_files = sorted([
            file for file in filenames
            if classifier_name in file
        ])

        for file in classifier_files:

            chamber_name = file.split(
                f"_{classifier_name}"
            )[0]

            rows = []

            with open(file, "r") as csvfile:
                csvreader = csv.reader(csvfile)

                for row in csvreader:
                    rows.append(row)

            for n in range(0, len(rows), 2):

                if n + 1 >= len(rows):
                    print(f"WARNING: {file} has an odd number of rows, last row skipped.")
                    break

                pair_index = n // 2

                # --------------------------------------------------
                # WingExt identity is REQUIRED for this specific pair
                # --------------------------------------------------

                if (chamber_name, pair_index) not in male_by_pair:

                    print(
                        f"SKIPPING {file} pair {pair_index}: "
                        f"no valid WingExt data available "
                        f"to determine male identity."
                    )

                    continue

                bouts1 = 0
                bouts2 = 0

                for col in rows[n]:
                    if col != "NaN":
                        bouts1 += 1

                for col in rows[n + 1]:
                    if col != "NaN":
                        bouts2 += 1

                new_row = [f"{file}_Fly{n}_Fly{n + 1}"]

                # Add Fly1
                new_row.append(bouts1)

                # Add Fly2
                new_row.append(bouts2)

                # Add MALE
                if male_by_pair[(chamber_name, pair_index)] == 0:
                    new_row.append(bouts1)
                else:
                    new_row.append(bouts2)

                new_rows.append(new_row)

        with open(new_filename, "w", newline="") as csvfile:

            csvwriter = csv.writer(csvfile)
            csvwriter.writerows(new_rows)

        print(
            f"{new_filename}: "
            f"{len(new_rows)} fly-pairs compiled"
        )

def main():
    root_path = input(
        "What is the complete path of the parent folder containing all videos and JAABA folders? "
    ).strip().strip("'\"")

    print(f"Using folder: {root_path}")

    rename_files_recursively(root_path)
    extract_lunge_frames_to_csv(root_path)
    compile_csv_files(root_path)


if __name__ == "__main__":
    main()
