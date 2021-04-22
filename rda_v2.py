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

def load_data(sheet_name, file_prefix = 'rdat_metro'):
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
            try:
                df_tmp = pd.read_excel(directory + f, sheet_name = sheet_name)
            except:
                print(f'No se encontró la hoja "{sheet_name}", favor de verificar el nombre.')
                exit(1)
            columns.append(df_tmp.columns)
            df = df.append(df_tmp)
            
    return df



##############################
# TIME-RELATED REPORTS
##############################
def hourly_reports(df, plot_length, col = ''):
    cols = [
        'HORATLMI',
        'HORACTEI',
        'HORATLMF',
        'HORA_REAL',
    ]

    if col in cols:
        cols = [col]

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
                
        plot_length = plot_length if plot_length < 143 else 142
        plot = plt(plot_length)
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


        plot = plt(plot_length)
        plot.set_values(xys.keys(), xys.values(), 'Turno', 'Reportes')
        plot.show(col)
        print()
        print()
        print()

def instances_dictionary(instances, dates):
    # Make an dictionary of dates and instances (zeros included)
    partial_instances = dict() # instances present in the data
    for k, v in instances.iteritems():
        partial_instances[k.date()] = v

    instances = dict() # instances considering all day in a year
    for day in dates:
        instances[day] = 0 if day not in partial_instances.keys() else partial_instances[day]
    
    return instances

def daily_reports(df, plot_length):
    # BUILD ALL DATES
    start_date = df['FECHA_REAL'].min().date()
    end_date = df['FECHA_REAL'].max().date()

    # Make date range
    delta = end_date - start_date

    dates = []
    for i in range(delta.days + 1):
        dates.append(start_date + timedelta(days=i))

    # Get number of reports
    instances_by_day = df['FECHA_REAL'].dt.floor('d').value_counts()
    instances = instances_dictionary(instances_by_day, dates)

    plot_length = plot_length if plot_length < 143 else 142

    plot = plt(plot_length)
    plot.set_values(instances.keys(), instances.values(), 'Día', 'Reportes')
    plot.show('Reportes por día')

def monthly_report(df, plot_length):
    instances_by_month = df['FECHA_REAL'].groupby([df.FECHA_REAL.dt.year, df.FECHA_REAL.dt.month]).agg('count')
    instances_by_month = pd.DataFrame(instances_by_month)
    instances_by_month['year_month'] = instances_by_month.index.to_series().apply(lambda x: '{0}-{1:02}'.format(*x))

    plot_length = plot_length if plot_length < 143 else 142

    plot = plt(plot_length)
    plot.set_values(instances_by_month['year_month'], instances_by_month['FECHA_REAL'], 'Mes', 'Reportes')
    plot.show('Reportes por mes')

def repetitions_analysis(df):
    # For each column, counts the values and prints the first 8 rows
    for col in df.columns:
        values = pd.DataFrame(df[col].value_counts()[:8])
        values['percentage'] = values / 59 * 100
        print(values)
        print()

def numeric_analysis(df):
    print(df.describe())

def main():
    sheet_name = input('¿Qué hoja quieres analizar? ')
    print('Cargando los datos...')
    df = load_data(sheet_name)

    cm = input('¿Qué CM te interesa? (Dejar en blanco para no filtrar datos por CM.) ')
    if len(cm) > 2:
        df_tmp = df[df['CMANTENI'] == cm]

    if df_tmp.shape[0] == 0:
        print('No se encontró ningún CM con el nombre propocionado.')
        print('El nombre debe coincidir con alguno de los presentes en los reportes.')
        print('Los únicos CM encontrados son:')
        # for cm in df['CMANTENI'].unique():
        for cm in sorted(df[df['CMANTENI'].notnull()]['CMANTENI'].unique()):
            print(f'\t{cm}')
        return
    print(f'Los datos tienen {df.shape[1]} columnas y {df.shape[0]} renglones.')

    df = df_tmp
    

    # SPLIT DATA BY COLUMNS' TYPE
    # date_cols = df.select_dtypes('datetime')

    # hour analysis
    hourly_reports(df, 60, col = 'HORA_REAL')

    # daily reports - seem useless
    # daily_reports(df[df['CMANTENI'] == 'CMABS'], 40)
    # daily_reports(df, 142)

    # monthly reports
    monthly_report(df, 142)

    df_obj = df.select_dtypes(object)
    repetitions_analysis(df_obj)

    numeric_analysis(df)

app = typer.Typer()

if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
