import pandas as pd

N_FIRST_ITEMS = 8

def count_by_category(df: pd.DataFrame):
    df = df.select_dtypes(object)
    category_results = []
    for c in df.columns:
        most_common = df[c].value_counts()[:N_FIRST_ITEMS]
        category_results.append(most_common)
        # print(most_common)
        # print()
    return category_results

