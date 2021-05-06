
import pandas as pd

from count_by_category import count_by_category
from count_by_dates import count_by_date

def data_type_analysis(df: pd.DataFrame):
    # date analysis
    date_results = count_by_date(df)

    # numeric analysis
    numeric_results = df.describe()

    # object analysis
    category_results = count_by_category(df)

    return (date_results, numeric_results, category_results)
