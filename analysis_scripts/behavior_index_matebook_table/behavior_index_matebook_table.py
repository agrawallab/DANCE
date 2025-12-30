# Last edited by Paulami Dey on 28/11/2024

import pandas as pd
import os
import openpyxl
import csv

file_path = input("What is the file's path\n")

input_directory = os.path.dirname(file_path)

final_file_name = input("Enter the final file name for the output XLSX file: ")
output_file = os.path.join(input_directory, f'output_{final_file_name}.csv')

try:
    workbook = openpyxl.load_workbook(file_path)

    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        writer.writerow(["Sheet Name", "Manual_index", "JAABA_index", "Matebook_index"])

        all_metrics = []

        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]

            df = pd.read_excel(file_path, sheet_name=sheet_name)  # Read directly from the sheet

            # Ensure columns exist before calculations
            if all(col in df.columns for col in ['manual t0', 'manual t1', 'JAABA t0', 'JAABA t1', 'Matebook t0', 'Matebook t1']):
                df.columns = df.columns.str.strip()

                df['E'] = df['manual t1'] - df['manual t0']
                df['F'] = df['JAABA t1'] - df['JAABA t0']
                df['G'] = df['Matebook t1'] - df['Matebook t0']

                sum_of_E = df['E'].sum()
                sum_of_F = df['F'].sum()
                sum_of_G = df['G'].sum()

                index_manual = sum_of_E / 27000
                index_JAABA = sum_of_F / 27000
                index_Matebook = sum_of_G / 27000

                all_metrics.append([sheet_name, round(index_manual, 3), round(index_JAABA, 3), round(index_Matebook, 3)])

        writer.writerows(all_metrics)

    print("Data written to CSV successfully.")

except FileNotFoundError:
    print("File not found. Please check the file path.")
except Exception as e:
    print("An error occurred:", e)
