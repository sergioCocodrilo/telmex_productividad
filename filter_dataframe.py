
import pandas as pd

def filter_df(df: pd.DataFrame, cm: str, cm_column: str):
    df = df[df[cm_column] == cm]
    if df.shape[0] == 0:
        raise ValueError('Your CM filter produced an empty data frame.')
    print(f'Rows found after filter: {df.shape[0]}')
    return df
