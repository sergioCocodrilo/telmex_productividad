import pandas as pd
import os
def read_files(directory: str, prefix: str, sheet_name: str):
    df = pd.DataFrame()
    read_files = 0
    for f in os.listdir(directory):
        if f.startswith(prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name = sheet_name)
            df = pd.concat([df, df_tmp])
            read_files += 1

    print(f'Files read: {read_files} Rows found:{df.shape[0]}')
    return df
