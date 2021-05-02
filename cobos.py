
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
    for column in date_columns:
        d['title'] = column + ' - cobos por mes'
        d['cols'] = ('Mes', 'Cobos')
        d['xys'] = count_instances(df[column].dt.month, range(1, 13))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por día'
        d['cols'] = ('día', 'Cobos')
        d['xys'] = count_instances(df[column].dt.day, range(1, 32))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por día de la semana'
        d['cols'] = ('día', 'Cobos')
        d['xys'] = count_instances(df[column].dt.dayofweek, range(0, 7))
        dates_results.append(copy.deepcopy(d))

        d['title'] = column + ' - cobos por hora'
        d['cols'] = ('hora', 'Cobos')
        d['xys'] = count_instances(df[column].dt.hour, range(1, 25))
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
        df = filter_df(df, args.cm, args.cm_column)

    # date analysis
    date_results = count_cobos_by_date(df)
    slp(date_results)

    # numeric analysis
    # print(df.describe())

    # object analysis
    count_cobos_by_category(df)
    

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
