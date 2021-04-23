import pandas as pd
from datetime import date, timedelta, time
import numpy as np
import socket
import os
# import plotext as plt

from plotter import Plotter as plt

def leer_archivos(directory: pd.DataFrame, prefijo: str = 'rdat_metro') -> pd.DataFrame:
    '''
    Lee los archivos de los reportes de productividad.
    Si un 'prefijo' es proporcionado, se seleccionan únicamente los archivos que
    inicien con ese nombre. El 'prefijo' determinado es 'rdat_metro'.
    '''
    # hostname = socket.gethostname()
    # if hostname == 'arch':
        # directory = '/home/sergio/Documents/TELMEX/Productividad/Datos/2020/rda/'
    # else:
        # directory = '/home/sergio/Documents/Telmex/Productividad/Data/2020/rda/'

    df = pd.DataFrame()
    rda_files = []
    columns = []

    for f in os.listdir(directory):
        if f.startswith(prefijo):
            df_tmp = pd.read_excel(directory + f, sheet_name='base')
            columns.append(df_tmp.columns)
            df = df.append(df_tmp)
            
    return df


##############################
# TIME-RELATED REPORTS
##############################
def por_hora(datos: pd.DataFrame, ancho_de_grafica: str, tipo_de_hora: str = '', cm: str = None) -> None:
    '''
    Análisis de los reportes por la hora en que ocurrieron.
    Se consideran tres 'tipo_de_hora':
        - HORATLMI
        - HORACTEI
        - HORATLMF
        - HORA_REAL

    Además, los reportes se agrupan por turnos:
        - matutino
        - vespertino
        - nocturno

    Parámetros:
        - datos [obligatorio]: variable con los reportes cargados
        - ancho_de_gráfica [obligatorio]: tamaño horizontal de la gráfica
        - tipo_de_hora [opcional]: reportar sólo los resultados de un tipo de hora
        - cm [opcional]: filtrar los datos por CM
    '''
    cols = [
        'HORATLMI',
        'HORACTEI',
        'HORATLMF',
        'HORA_REAL',
    ]

    df = datos
    plot_length = ancho_de_grafica
    col = tipo_de_hora
    cm_to_filter = cm

    if col in cols:
        cols = [col]

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

def instances_dictionary(instances: pd.Series, dates: list) -> dict:
    '''Función para control interno.'''
    # Make an dictionary of dates and instances (zeros included)
    partial_instances = dict() # instances present in the data
    for k, v in instances.iteritems():
        partial_instances[k.date()] = v

    instances = dict() # instances considering all day in a year
    for day in dates:
        instances[day] = 0 if day not in partial_instances.keys() else partial_instances[day]
    
    return instances

def por_dia(datos: pd.DataFrame, ancho_de_grafica: int, cm: str = None) -> None:
    '''
    Análisis de los reportes por el día en que ocurrieron.

    Parámetros:
        - datos [obligatorio]: variable con los reportes cargados
        - ancho_de_grafica [obligatorio]: tamaño horizontal de la gráfica
        - cm [opcional]: filtrar los datos por CM
    '''

    df = datos
    plot_length = ancho_de_grafica

    if cm is not None:
        df = df[df['CMANTENI'] == cm]

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

def por_mes(datos: pd.DataFrame, ancho_de_grafica: str, cm = None) -> None:
    '''
    Análisis mensual de los reportes.

    Parámetros:
        - datos [obligatorio]: variable con los reportes cargados
        - ancho_de_grafica [obligatorio]: tamaño horizontal de la gráfica
        - cm [opcional]: filtrar los datos por CM
    '''
    df = datos
    plot_length = ancho_de_grafica

    if cm is not None:
        df = df[df['CMANTENI'] == cm]

    instances_by_month = df['FECHA_REAL'].groupby([df.FECHA_REAL.dt.year, df.FECHA_REAL.dt.month]).agg('count')
    instances_by_month = pd.DataFrame(instances_by_month)
    instances_by_month['year_month'] = instances_by_month.index.to_series().apply(lambda x: '{0}-{1:02}'.format(*x))

    plot_length = plot_length if plot_length < 143 else 142

    plot = plt(plot_length)
    plot.set_values(instances_by_month['year_month'], instances_by_month['FECHA_REAL'], 'Mes', 'Reportes')
    plot.show('Reportes por mes')

def datos_que_se_repiten(datos: pd.DataFrame, cm = None) -> None:
    '''
    Analiza las columnas con datos de tipo texto (no numéricos). Cuenta las
    instancias más presentes en los datos e imprime las 8 más frecuentes.

    Se realiza una impresión por columna, la impresión incluye 8 renglones.

    Parámetros:
        - datos [obligatorio]
        - cm [opcional]: filtrar por CM
    '''
    df = datos

    if cm is not None:
        df = df[df['CMANTENI'] == cm]

    for col in df.columns:
        values = pd.DataFrame(df[col].value_counts()[:8])
        values['percentage'] = values / 59 * 100
        print(values)
        print()

def numerico(datos: pd.DataFrame, cm: str = None) -> None:
    '''
    Descripción de datos numéricos con media, desviación estándard, percentiles.

    Parámetros:
        - datos [obligatorio]
        - cm [opcional]: filtrar por CM
    '''
    df = datos

    if cm is not None:
        df = df[df['CMANTENI'] == cm]

    if cm is None:
        df_int = df.select_dtypes('number')
    else:
        df_int = df[df['CMANTENI'] == cm].select_dtypes('number')
    print(df_int.describe())

def main() -> None:
    df = leer_archivos()

    # SPLIT DATA BY COLUMNS' TYPE
    # date_cols = df.select_dtypes('datetime')

    # hour analysis
    por_hora(df, 60, cm_to_filter = 'CMABS', col = 'HORA_REAL')
    # por_hora(df, 60, col = 'HORA_REAL')

    # daily reports - seem useless
    # por_dia(df[df['CMANTENI'] == 'CMABS'], 40)
    # por_dia(df, 142)

    # monthly reports
    por_mes(df[df['CMANTENI'] == 'CMABS'], 142)
    # por_mes(df, 142)

    df_obj = df.select_dtypes(object)
    datos_que_se_repiten(df_obj[df_obj['CMANTENI'] == 'CMABS'])

    numerico(df, cm = 'CMABS')

if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
