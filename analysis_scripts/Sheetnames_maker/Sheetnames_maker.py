# Last edited by Paulami Dey on 28/11/2024

from openpyxl import Workbook
import os

def create_excel_with_sheets(sheet_names, file_path):
    # Create a new Workbook object
    wb = Workbook()

    # Loop through the sheet names and create sheets accordingly
    for index, name in enumerate(sheet_names, start=1):
        # Truncate the sheet name if it exceeds 31 characters
        if len(name) > 31:
            name = name[:31]
        # Create a new sheet
        ws = wb.create_sheet(title=name, index=index)

        # Add common header
        header = ['manual t0', 'manual t1', 'JAABA t0', 'JAABA t1', 'Matebook t0',	'Matebook t1']  # Add your desired headers here
        ws.append(header)

# ['manual t0', 'manual t1', 'JAABA t0', 'JAABA t1', 'Matebook t0',	'Matebook t1']
# ['singleblind t0', 'singleblind t1', 'ground-truth t0', 'ground-truth t1', 'DANCE t0', 'DANCE t1']

    # Remove the default sheet created by openpyxl (Sheet)
    wb.remove(wb["Sheet"])

    # Save the workbook
    wb.save(file_path)
    print(f"Excel file '{file_path}' with specified sheets and common header created successfully.")

def main():
    # Input sheet names
    sheet_names = ['Chamber_10', 'Chamber_11', 'Chamber_14', 'Chamber_1', 'test1', 'test2', 'test3_10', 'test3_11', 'test3_1', 'test7V_3', 'test7V_4', 'test7V_8', 'test7V_9', 'test7V_13', 'test_10', 'test9_15', 'testDVGH_10', 'testDVGH_11', 'testDV_1', 'testDV_2', 'testDV_4', 'testDV_5', 'test_SH_4', 'test_SH_5', 'test_SH_7']

      # Directory path to save the Excel file 
    directory_path = r"E:\Paulami\Ground-truthing Data\Single Blind\10 mm chamber\Manohar\Copulation\28112024"

    # File name for the Excel file
    file_name = "Copulation_SB_Workbook.xlsx"

    # Combine directory path and file name
    file_path = os.path.join(directory_path, file_name)

    # Create Excel file with specified sheet names and common header
    create_excel_with_sheets(sheet_names, file_path)

if __name__ == "__main__":
    main()


