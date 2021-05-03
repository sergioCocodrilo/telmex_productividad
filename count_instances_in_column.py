
import pandas as pd

def count_instances(series: pd.Series, count_range: range, time_delta: str):

    # dates_results.append(make_plot(column + ' - cobos por día de la semana', ('Día', 'Cobos'), count_instances(df[column].dt.dayofweek, range(0, 7))))
    if time_delta == 'month':
        series = series.dt.month
    elif time_delta == 'day':
        series = series.dt.day
    elif time_delta == 'dayofweek':
        series = series.dt.dayofweek
    elif time_delta == 'hour':
        series = series.dt.hour
    else:
        raise ValueError('time_delta must be month, day, dayofweek of hour')

    counter = series.value_counts().sort_index()
    rv = {x: (counter[x] if x in counter.index else 0) for x in count_range}
    return rv
