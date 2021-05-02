'''
Columnas:
    datos numéricos -> generan un resumen (describe)
        ctes_inf
        lin_pots
        tpo_real
        cump_tpo
        rein_dias
        rein
        rang_hrs
    datos fecha     -> generan gráficas
        fech_ini_a
        fech_fin_a
        mes_rep
    datos texto     -> genera un resumen por tipo de dato (value_counts)
        no_boleta
        estado
        div_resp
        sub_resp
        gcia_resp
        edif_resp
        sigctralr
        cm_p
        tipo_cns
        clase_afec
        tip_red
        ctral_afec
        eq_ctral_a
        subred
        cau_gen
        cau_esp
        elem_red
        siglas
'''

import pandas as pd
import os
import argparse
import copy
# import matplotlib.pyplot as plt
from graphical_plotter import single_line_plot as slp

def read_data(directory: str, prefix: str, sheet_name: str = None):
    df = pd.DataFrame()
    read_files = 0
    for f in os.listdir(directory):
        if f.startswith(prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name = sheet_name)
            df = pd.concat([df, df_tmp])
            read_files += 1

    print(f'Files read: {read_files} Rows found:{df.shape[0]}')
    return df

def filter(df: pd.DataFrame, cm: str, cm_column: str):
    df = df[df[cm_column] == cm]
    if df.shape[0] == 0:
        raise ValueError('Your CM filter produced an empty data frame.')
    print(f'Rows found after filter: {df.shape[0]}')
    return df

def series_counter(series: pd.Series, count_range: range):
    counter = series.value_counts().sort_index()
    rv = {x: (counter[x] if x in counter.index else 0) for x in count_range}
    return rv

def count_cobos_by_date(df: pd.DataFrame):
    date_columns = (
            'fech_ini_a',
            'fech_fin_a',
            'mes_rep',
            )

    dates_results = []

    # different ways of counting cobos:
    d = dict()
    for column in date_columns:
        d['title'] = column + ' - cobos por mes'
        d['cols'] = ('Mes', 'Cobos')
        d['xys'] = series_counter(df[column].dt.month, range(1, 13))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por día'
        d['cols'] = ('día', 'Cobos')
        d['xys'] = series_counter(df[column].dt.day, range(1, 32))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por día de la semana'
        d['cols'] = ('día', 'Cobos')
        d['xys'] = series_counter(df[column].dt.dayofweek, range(0, 7))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por hora'
        d['cols'] = ('hora', 'Cobos')
        d['xys'] = series_counter(df[column].dt.hour, range(1, 25))
        dates_results.append(copy.deepcopy(d))

    return dates_results

def count_cobos_by_category(df: pd.DataFrame):
    df = df.select_dtypes(object)
    for c in df.columns:
        most_common = df[c].value_counts()[:8]
        print(most_common)
        print()


def main(argv = None):
    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='location of files', type = str, required = True)
    parser.add_argument('-p', '--prefix', help = 'prefix of files', type = str, required = True)
    parser.add_argument('-sn', '--sheet_name', help = 'sheet name within the xml', required = True)
    parser.add_argument('-cm', help = 'CM of interest', required = False)
    parser.add_argument('-cmcol', '--cm_column', help = 'Column where to find the CM', required = False)
    args = parser.parse_args(argv)

    # load data
    df = read_data(args.directory, args.prefix, args.sheet_name)

    # filter data
    if args.cm is not None:
        df = filter(df, args.cm, args.cm_column)

    # date analysis
    date_results = count_cobos_by_date(df)
    slp(date_results)

    # numeric analysis
    # print(df.describe())

    # object analysis
    count_cobos_by_category(df)
    




    

if __name__ == '__main__':
    main()
