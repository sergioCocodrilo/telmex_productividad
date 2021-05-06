
import argparse
import os
import pandas as pd

from files_with_prefix_in_directory import read_files
from count_by_data_types import data_type_analysis

def identify_files(directory: str, prefix: str) -> list:
    files_matching_description = [file for file in os.listdir(directory) if file.startswith(prefix)]
    if len(files_matching_description) == 0:
        raise ValueError('Your directory and prefix filter found no match.')
    return files_matching_description

def get_sheet_names(file: str) -> list:
    excel_file = pd.ExcelFile(file)
    return excel_file.sheet_names

def select_sheet(sheet_names: list) -> str:
    print()
    print('Pick a sheet to read')
    for sheet in sheet_names:
        print('\t', sheet)
    sheet_name = input('\t')
    return sheet_name

def take_decision(options: list, message: str) -> str:
    print()
    print(message)
    for option in options:
        print('\t', option)
    decision = input('\t')
    return decision

def filter_by_column(df: pd.DataFrame, chosen_column_filter: str, filter_criteria: str) -> pd.DataFrame:
    df = df[df[chosen_column_filter] == filter_criteria]
    return df

def main(argv = None):
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='location of files', type = str, required = True)
    parser.add_argument('-p', '--prefix', help = 'prefix of files', type = str, required = True)
    args = parser.parse_args(argv)

    input_files = identify_files(args.directory, args.prefix)
    sheet_names = get_sheet_names(args.directory + input_files[0])
    chosen_sheet = take_decision(sheet_names, 'Pick a sheet to read')
    df = read_files(args.directory, args.prefix, chosen_sheet)
    chosen_column_filter = take_decision(df.columns, 'Pick a column as filter')
    if len(chosen_column_filter) > 0:
        df = df[df[chosen_column_filter].notna()]
        filter_criteria = take_decision(sorted(df[chosen_column_filter].unique()), 'Pick your filter criteria')
        df = filter_by_column(df, chosen_column_filter, filter_criteria)

    date_results, numeric_results, category_results = data_type_analysis(df)
    print(date_results)
    print()
    print(numeric_results)
    print()
    print(category_results)


    '''
    checked:
    python productivity_analysis.py -d /home/sergio/Documents/TELMEX/Productividad/Datos/2020/CalTraf/ -p CalTraf
    python productivity_analysis.py -d /home/sergio/Documents/TELMEX/Productividad/Datos/2020/ -p cobo
    python productivity_analysis.py -d /home/sergio/Documents/TELMEX/Productividad/Datos/2020/rda/ -p rdat
    '''

if __name__ == '__main__':
    # date_results, numeric_results, category_results = main()
    # print(date_results)
    # print(numeric_results)
    # print(category_results)
    main()
