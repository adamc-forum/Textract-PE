import pandas as pd
import openpyxl
from utils import append_df_and_image_to_new_ws
from json_handler import json_handler_cls
from image_handler import image_handler_cls
from csv_cleaner import clean_and_save_dataframes, get_existing_file_paths

json_object = json_handler_cls("analyzeDocResponse.json")
json_object.get_tables()

image_object = image_handler_cls('Project Huron - CIM.pdf', json_object.tables_info)
image_object.get_images()
image_object.save_images()

clean_and_save_dataframes()

# Create a new Excel workbook
wb = openpyxl.Workbook()
wb.remove(wb.active)  # Remove the default sheet

# Get all cleaned CSV file paths
cleaned_file_paths = get_existing_file_paths("cleaned-table-", ".csv")

# Iterate over cleaned CSVs and images and add them to the workbook
for i, file_path in enumerate(cleaned_file_paths):
    img_path = f"table_{i + 1}.png"
    df = pd.read_csv(file_path)
    append_df_and_image_to_new_ws(wb, df, img_path, sheet_name=f"table-{i + 1}")

# Save the workbook
wb.save("Final_Output.xlsx")