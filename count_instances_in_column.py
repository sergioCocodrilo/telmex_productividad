
import pandas as pd

def count_instances(series: pd.Series, count_range: range):
    counter = series.value_counts().sort_index()
    rv = {x: (counter[x] if x in counter.index else 0) for x in count_range}
    return rv
