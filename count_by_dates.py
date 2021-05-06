
import pandas as pd
import copy

from count_instances_by_time import count_instances_by_time

def count_by_date(df: pd.DataFrame) -> list:
    # date columns should be: fech_ini_a, fech_fin_a, mes_rep
    date_columns = df.select_dtypes(include = ['datetime64']).columns
    dates_results = []

    # different ways of counting cobos:
    plotting_arguments = [
        [' - por mes',              'Mes',  'month',     range(1, 13)],
        [' - por día',              'Día',  'day',       range(1, 32)],
        [' - por día de la semana', 'Día',  'dayofweek', range(0, 7)],
        [' - por hora',             'Hora', 'hour',      range(1, 25)],
        ]

    for column in date_columns:
        series = df[column]
        for plot_argument in plotting_arguments:
            xys = count_instances_by_time(series, plot_argument[3], plot_argument[2])
            if xys is not None:
                dates_results.append(
                        build_plotting_structure(
                            column + plot_argument[0],
                            (plot_argument[1], 'Cobos'),
                            xys,
                            )
                        )
    return dates_results

def build_plotting_structure(title: str, cols: tuple, xys: dict) -> dict:
    d = dict()
    d['title'] = title
    d['cols'] = cols
    d['xys'] = xys
    return copy.deepcopy(d)

