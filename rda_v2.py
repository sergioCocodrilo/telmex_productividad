import pandas as pd
from datetime import date, timedelta, time
import numpy as np
import socket
import os
# import plotext as plt

from plotter import Plotter as plt

##############################
# Data Loading
##############################

def load_data(file_prefix = 'rdat_metro'):
    hostname = socket.gethostname()
    if hostname == 'arch':
        directory = '/home/sergio/Documents/TELMEX/Productividad/Datos/2020/rda/'
    else:
        directory = '/home/sergio/Documents/Telmex/Productividad/Data/2020/rda/'

    df = pd.DataFrame()
    rda_files = []
    columns = []

    for f in os.listdir(directory):
        if f.startswith(file_prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name='base')
            columns.append(df_tmp.columns)
            df = df.append(df_tmp)
            
    #print(df.shape)
    return df



##############################
# HOURLY REPORTS
##############################
def hourly_reports(df, cm_to_filter = None):
    cols = [
        'HORATLMI',
        'HORACTEI',
        'HORATLMF',
        'HORA_REAL',
    ]

    if cm_to_filter is not None:
        df = df[df['CMANTENI'] == cm_to_filter]

    for i, col in enumerate(cols):
        # remove nan values
        hour_data = df[df[col].notna()]
        # extract hour as int
        time_df = pd.DataFrame(hour_data[col].astype(str).str[:2].astype(int))

        xy = time_df.value_counts().sort_index()
        xs, ys = [], []
        xs = [x for x in range(24)]

        for h in range(24):
            try:
                ys.append(xy[h])
            except KeyError:
                ys.append(0)
                
        plot = plt(80)
        plot.set_values(xs, ys, 'HORA', 'Reportes')
        plot.show(col)


        # Análisis por turno
        xys = {
                'mat' : 0,
                'vesp': 0,
                'noct': 0,
                }

        for x, y  in zip(xs, ys):
            if 7 < x < 17:
                xys['mat'] += y
            elif 16 < x < 24:
                xys['vesp'] += y
            else:
                xys['noct'] += y

        plot = plt(80)
        plot.set_values(xys.keys(), xys.values(), 'Turno', 'Reportes')
        plot.show(col)
        print()
        print()
        print()



def main():
    df = load_data()

    # SPLIT DATA BY COLUMNS' TYPE
    date_cols = df.select_dtypes('datetime')
    int_cols = df.select_dtypes('number')
    obj_cols = df.select_dtypes(object)

    # hour analysis
    hourly_reports(obj_cols, 'CMABS')

if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
