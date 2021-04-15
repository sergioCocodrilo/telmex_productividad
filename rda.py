#!/bin/python

'''
This script make the analysis of the RDA reports.

Inputs:
    - reports' directory
    - cm to filter (optional)
'''

import pandas as pd
import sys
import seaborn as sns

def verify_columns(cols):
    '''
    Check that all required cols are included. This is needed because not all
    reports have the same structure.
    '''

    #expected_cols should be reduced to its minimum
    #expected_cols should be reduced to its minimum
    #expected_cols should be reduced to its minimum
    #expected_cols should be reduced to its minimum

    expected_cols = set(
            [
        'ID',
        'SITIO',
        'SERVICIO',
        'CENTRAL',
        'CATENCIO',
        'CMANTENI',
        'CTGOM',
        'SERV',
        'CLIENTE',
        'SEMANA',
        'division',
        'DOMICILIOA',
        'DOMICILIOB',
        'EST_N',
        'FECHATLMI',
        'HORATLMI',
        'FECHACTEI',
        'HORACTEI',
        'FECHATLMF',
        'HORATLMF',
        'FECHA_REAL',
        'HORA_REAL',
        'DURACTE',
        'DURAREP',
        'DURATLM',
        'QUEJA_PBA',
        'FALLAENC',
        'FOLIOF',
        'FOLIOQ',
        'COD01',
        'COD02',
        'COD03',
        'COD04',
        'COD05',
        'FOL_SER',
        'TEC_ASIG',
        'TEC_CIERRA',
        'cto_x_sent',
        'ONTIME',
        'CODIGO',
        't_1a_oin_c',
        'tipo_cliente',
        'Entiempo_tipocte',
        'centro_atendio',
        'entidad_ctro_atendio',
        'INX',
        ]
        )
    for col in expected_cols:
        if col not in cols:
            raise AttributeError(f'An expected column ({col}) is missing in the report.')

def file_reading(directory = None):
    'Reads all rda reports and returns a pandas.DataFrame'
    if directory is None:
        directory = '/home/sergio/Documents/Telmex/Productividad/Data/2020/rda/'
    file_prefix = 'rdat_metro'

    df = pd.DataFrame()

    import os
    rda_files = []
    for f in os.listdir(directory):
        if f.startswith(file_prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name='base')
            #print(f, '-', df_tmp.shape)

            # check that required columns are present
            verify_columns(df_tmp.columns)

            df = df.append(df_tmp)
            
    #print(df.shape)
    return df


def numeric_analysis(df):
    print(df.describe())

def date_analysis(df, granularity = 0):
    '''
    Plotting events by date.

    granularity can be:
        0: monthly
        1: daily
    '''
    months = df['FECHA_REAL'].dt.month
    df_MONTH = df.join(months, rsuffix='_MONTH')
    #df_MONTH[['FECHA_REAL', 'FECHA_REAL_MONTH']]   # verify month and date match

    fig, ax = plt.subplots()

    # Count RDA errors by day
    if granularity == 1:
        instances_by_day = df['FECHA_REAL'].dt.floor('d').value_counts()
        ax.bar(instances_by_day.index, instances_by_day.values)
    else:
        y = df['FECHA_REAL'].dt.year
        m = df['FECHA_REAL'].dt.month

        instances_by_day = df['FECHA_REAL'].groupby([df.FECHA_REAL.dt.year, df.FECHA_REAL.dt.month]).agg('count')
        xs = instances_by_day.index.to_series().apply(lambda x: '{0}-{1}'.format(*x))
        ax.plot(xs, instances_by_day.values)
    instances_by_day.sort_index(inplace=True)

    # Plotting
    plt.show()

def plotting(df, granularitty = 0):
    # months = df['FECHA_REAL'].dt.month
    # df_MONTH = df.join(months, rsuffix='_MONTH')
    # #df_MONTH[['FECHA_REAL', 'FECHA_REAL_MONTH']]   # verify month and date match

    # fig, ax = plt.subplots()

    # # Count RDA errors by day
    # if granularity == 1:
        # instances_by_day = df['FECHA_REAL'].dt.floor('d').value_counts()
        # ax.bar(instances_by_day.index, instances_by_day.values)
    # else:
        # y = df['FECHA_REAL'].dt.year
        # m = df['FECHA_REAL'].dt.month

        # instances_by_day = df['FECHA_REAL'].groupby([df.FECHA_REAL.dt.year, df.FECHA_REAL.dt.month]).agg('count')
        # xs = instances_by_day.index.to_series().apply(lambda x: '{0}-{1}'.format(*x))
        # ax.plot(xs, instances_by_day.values)
    # instances_by_day.sort_index(inplace=True)

    # # Plotting
    # plt.show()



    instances_by_day = df['FECHA_REAL'].dt.floor('d').value_counts()

    sns.displot(
        data=instances_by_day,
        # x="carat", hue="cut",
        kind="kde", height=6,
        multiple="fill", clip=(0, None),
        palette="ch:rot=-.25,hue=1,light=.75",
    )

def rda_analysis():
    directory = None
    cm = None

    # args reading
    if len(sys.argv) == 3:
        directory, cm = sys.argv[1:]
    elif len(sys.argv) == 2:
        directory = sys.argv[1]

    # Read files
    df = file_reading(directory)

    # filter by CM
    if cm is not None:
        df = df[df['CMANTENI'] == cm]

    # split data by type
    date_df = df.select_dtypes('datetime')
    numeric_df = df.select_dtypes('number')
    string_df = df.select_dtypes(object)

    # print(df.head())

    # --------------------------------
    # pick the type of analysis wanted
    # --------------------------------

    # numeric_analysis(numeric_df)
    # date_analysis(date_df)
    plotting(date_df)

if __name__ == '__main__':
    rda_analysis()
