
import pandas as pd
import os
import argparse
import copy
# import matplotlib.pyplot as plt
from read_report import read_data
from graphical_plotter import single_line_plot as slp
from filter_dataframe import filter_df
from count_instances_in_column import count_instances

def count_cobos_by_date(df: pd.DataFrame):
    date_columns = (
            'fech_ini_a',
            'fech_fin_a',
            'mes_rep',
            )

    dates_results = []

    # different ways of counting cobos:
    d = dict()

    time_period = [
        [' - cobos por mes',              'Mes',  'month',     range(1, 13)],
        [' - cobos por día',              'Día',  'day',       range(1, 32)],
        [' - cobos por día de la semana', 'Día',  'dayofweek', range(0, 7)],
        [' - cobos por hora',             'Hora', 'hour',      range(1, 25)],
        ]

    for column in date_columns:
        series = df[column]
        for l in time_period:
            dates_results.append(make_plot(column + l[0], (l[1], 'Cobos'), count_instances(series, l[3], l[2])))
    return dates_results

def make_plot(title: str, cols: tuple, xys: dict):
    d = dict()
    d['title'] = title
    d['cols'] = cols
    d['xys'] = xys
    return copy.deepcopy(d)


def count_cobos_by_category(df: pd.DataFrame):
    df = df.select_dtypes(object)
    category_results = []
    for c in df.columns:
        most_common = df[c].value_counts()[:8]
        category_results.append(most_common)
        # print(most_common)
        # print()
    return category_results

def cobos_analysis(df: pd.DataFrame):
    # date analysis
    date_results = count_cobos_by_date(df)

    # numeric analysis
    numeric_results = df.describe()

    # object analysis
    category_results = count_cobos_by_category(df)

    return (date_results, numeric_results, category_results)


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
        df = filter_df(df, args.cm, args.cm_column)

    # date analysis
    date_results = count_cobos_by_date(df)
    slp(date_results)

    # numeric analysis
    # print(df.describe())

    # object analysis
    category_results = count_cobos_by_category(df)
    

if __name__ == '__main__':
    main()

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
