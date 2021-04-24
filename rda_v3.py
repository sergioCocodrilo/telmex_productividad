
'''
Report generator of RDA files. This uses Matplotlib plots and the result is a
Latex pdf.
'''
import pandas as pd
from datetime import date, timedelta, time
import numpy as np
import socket
import os
import argparse
import copy
# import plotext as plt

# Latex
from pylatex import Document, Section, Subsection, Command
from pylatex.utils import italic, NoEscape

# Typing
from typing import Optional
from typing import Sequence

from plotter import Plotter as plt

def load_data(sheet_name, directory, file_prefix: str = 'rdat_metro'):
    '''Loads the Excel reports of the productivity and returns a single df.'''
    hostname = socket.gethostname()
    if directory is None:
        if hostname == 'arch':
            directory = '/home/sergio/Documents/TELMEX/Productividad/Datos/2020/rda/'
        else:
            directory = '/home/sergio/Documents/Telmex/Productividad/Data/2020/rda/'

    df = pd.DataFrame()
    rda_files = []
    columns = []

    for f in os.listdir(directory):
        if f.startswith(file_prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name = sheet_name)
            columns.append(df_tmp.columns)
            df = df.append(df_tmp)
            
    return df



##############################
# TIME-RELATED REPORTS
##############################
def hourly_reports(df: pd.DataFrame) -> list[dict]:
    '''
    Analysis of the reports by hour of ocurrence.
    Three types of time data are considered:
        - HORATLMI
        - HORACTEI
        - HORATLMF
        - HORA_REAL

    Additionally, reports are grouped by ship, i.e.:
        - matutino
        - vespertino
        - nocturno

    Returns a list of dictionaries with the structure:
        [
            {
                'title': 'HORA_REAL',
                'cols': (col_a_title, col_b_title),
                'xys': {
                    'x0': 'y0',
                    'x1': 'y1',
                    ...
                    },
            },
            {
                'title': 'HORATLMF',
                'cols': (col_a_title, col_b_title),
                'xys': {
                    'x0': 'y0',
                    'x1': 'y1',
                    ...
                    },
            },
        ]

    '''
    cols = [
        'HORATLMI',
        'HORACTEI',
        'HORATLMF',
        'HORA_REAL',
    ]

    plotting_values = []

    for i, col in enumerate(cols):
        # remove nan values
        hour_data = df[df[col].notna()]
        # extract hour as int
        time_df = pd.DataFrame(hour_data[col].astype(str).str[:2].astype(int))

        xy = time_df.value_counts().sort_index()
        xys = dict()

        for h in range(24):
            try:
                xys[h] = xy[h]
            except KeyError:
                xys[h] = 0

        d = dict()
        d['title'] = col
        d['cols'] = ('HORA', 'Reportes')
        d['xys'] = xys
        plotting_values.append(copy.deepcopy(d))

        # ship analysis
        xys_ship = {
                'mat' : 0,
                'vesp': 0,
                'noct': 0,
                }

        for x, y  in xys.items():
            if 7 < int(x) < 17:
                xys_ship['mat'] += y
            elif 16 < int(x) < 24:
                xys_ship['vesp'] += y
            else:
                xys_ship['noct'] += y

        d['title'] = col + ' por turnos'
        d['cols'] = ('Turno', 'Reportes')
        d['xys'] = xys_ship
        plotting_values.append(copy.deepcopy(d))
    return plotting_values

def instances_dictionary(instances: pd.Series, dates: list):
    # Make an dictionary of dates and instances (zeros included)
    partial_instances = dict() # instances present in the data
    for k, v in instances.iteritems():
        partial_instances[k.date()] = v

    instances = dict() # instances considering all day in a year
    for day in dates:
        instances[day] = 0 if day not in partial_instances.keys() else partial_instances[day]
    
    return instances

def daily_reports(df: pd.DataFrame):
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


    # plot = plt(plot_length)
    # plot.set_values(instances.keys(), instances.values(), 'Día', 'Reportes')
    # plot.show('Reportes por día')

    d = dict()
    d['title'] = 'Reportes por día'
    d['cols'] = ('Día', 'Reportes')
    d['xys'] = instances
    return [d]

def monthly_report(df: pd.DataFrame):
    instances_by_month = df['FECHA_REAL'].groupby([df.FECHA_REAL.dt.year, df.FECHA_REAL.dt.month]).agg('count')
    instances_by_month = pd.DataFrame(instances_by_month)
    instances_by_month['year_month'] = instances_by_month.index.to_series().apply(lambda x: '{0}-{1:02}'.format(*x))

    d = dict()
    d['title'] = 'Reportes por mes'
    d['cols'] = ('Mes', 'Reportes')
    d['xys'] = dict(zip(instances_by_month['year_month'], instances_by_month['FECHA_REAL']))
    return [d]

def repetitions_analysis(df: pd.DataFrame):
    # For each column, counts the values and prints the first 8 rows
    for col in df.columns:
        values = pd.DataFrame(df[col].value_counts()[:8])
        values['percentage'] = values / 59 * 100
        print(values)
        print()

def numeric_analysis(df: pd.DataFrame, cm: str = None):
    if cm is None:
        df_int = df.select_dtypes('number')
    else:
        df_int = df[df['CMANTENI'] == cm].select_dtypes('number')
    print(df_int.describe())

def main(argv = None):

    # check arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument('-g', '--grafica', help='Ancho de gráfica', type = int, required = True)
    parser.add_argument('-d', '--directory', help='xls files directory', type = str, required = False)
    parser.add_argument('-cm', help='Centro de Mantenimiento', type = str, required = False)
    parser.add_argument('-s', '--sheet', help='Sheet name for pandas', type = str, required = True)
    parser.add_argument('-p', '--prefix', help='Common prefix of xls files', type=str, required = True)
    parser.add_argument('-f', '--file', help='Output latex file', type=str, required = True)
    # parser.add_argument('-th', '--hora', help='Tipo de hora', type=str, required = True)

    args = parser.parse_args(argv)
    df = load_data(args.sheet, args.directory, args.prefix)

    if args.cm is not None:
        df_tmp = df[df['CMANTENI'] == args.cm]
        if df_tmp.shape[0] < 1:
            print('Your CM filter resulted in no rows.')
            return 0
        df = df_tmp

    # SPLIT DATA BY COLUMNS' TYPE
    # date_cols = df.select_dtypes('datetime')

    # hour analysis
    plt_values = hourly_reports(df)
    # for d in plt_values:
        # plot = plt(140)
        # plot.set_values(d['xys'].keys(), d['xys'].values(), d['cols'][0], d['cols'][1])
        # plot.show(d['title'])


    # daily reports - seem useless
    plt_values = daily_reports(df)
    # for d in plt_values:
        # plot = plt(140)
        # plot.set_values(d['xys'].keys(), d['xys'].values(), d['cols'][0], d['cols'][1])
        # plot.show(d['title'])


    # monthly reports
    plt_values = monthly_report(df)
    for d in plt_values:
        plot = plt(140)
        plot.set_values(d['xys'].keys(), d['xys'].values(), d['cols'][0], d['cols'][1])
        plot.show(d['title'])

    return 0

    df_obj = df.select_dtypes(object)
    repetitions_analysis(df_obj)

    numeric_analysis(df)


if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
