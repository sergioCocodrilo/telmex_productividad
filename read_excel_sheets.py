import pandas as pd

def get_sheet_names(file: str) -> list:
    excel_file = pd.ExcelFile(file)
    return excel_file.sheet_names
