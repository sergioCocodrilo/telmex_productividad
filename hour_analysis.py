'''
The idea is to try to identify if ocurrences increase on a certain hour.
'''


import pandas as pd
import socket
import os

def load_data():
    hostname = socket.gethostname()

    if hostname == 'arch':
        directory = '/home/sergio/Documents/TELMEX/Productividad/Datos/2020/rda/'
    else:
        directory = '/home/sergio/Documents/Telmex/Productividad/Data/2020/rda/'

    file_prefix = 'rdat_metro'

    df = pd.DataFrame()

    rda_files = []
    columns = []
    for f in os.listdir(directory):
        if f.startswith(file_prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name='base')
            #print(f, '-', df_tmp.shape)
            columns.append(df_tmp.columns)
            df = df.append(df_tmp)
            
    #print(df.shape)

    return df

def hour_analysis(df, col):
    
    # not all the data has the same format, so parsing within a loop is needed
    for index, row in df.iterrows():
        print(str(row[col])[:8])


def main():
    df = load_data()
    
    # ==============
    # Split data by types
    # ==============
    date_cols = df.select_dtypes('datetime')
    int_cols = df.select_dtypes('number')
    obj_cols = df.select_dtypes(object)

    # cols with time stamp data
    cols = [
        'HORATLMI',
        'HORACTEI',
        'HORATLMF',
        'HORA_REAL',
    ]

    hour_analysis(obj_cols, cols[0])

if __name__ == '__main__':
    main()
