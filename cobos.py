import pandas as pd
import os
import argparse

def read_data(directory: str, prefix: str, sheet_name: str = None):
    df = pd.DataFrame()
    read_files = 0
    for f in os.listdir(directory):
        if f.startswith(prefix):
            df_tmp = pd.read_excel(directory + f, sheet_name = sheet_name)
            df = pd.concat([df, df_tmp])
            read_files += 1

    print(f'Files read: {read_files} Rows found:{df.shape[0]}')
    return df

def filter(df: pd.DataFrame, cm: str, cm_column: str):
    df = df[df[cm_column] == cm]
    if df.shape[0] == 0:
        raise ValueError('Your CM filter produced an empty data frame.')
    print(f'Rows found after filter: {df.shape[0]}')
    return df

def series_counter(series: pd.Series, count_range: range):
    counter = series.value_counts().sort_index()
    rv = {x: (counter[x] if x in counter.index else 0) for x in count_range}
    return rv

def count_cobos_by_date(df: pd.DataFrame):
    date_columns = (
            'fech_ini_a',
            'fech_fin_a',
            'mes_rep',
            )

    count_results = {}

    # different ways of counting cobos:
    for column in date_columns:
        count_results[column + ' mensual'] = series_counter(df[column].dt.month, range(1, 13))
        count_results[column + ' por dia'] = series_counter(df[column].dt.day, range(1, 32))
        count_results[column + ' dia de la semana'] = series_counter(df[column].dt.dayofweek, range(7))
        count_results[column + ' por hora'] = series_counter(df[column].dt.hour, range(25))

    return count_results

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
        df = filter(df, args.cm, args.cm_column)

    # date analysis
    date_results = count_cobos_by_date(df)

    # for title, counter in count_results.items():
        # print('Count of', title)
        # for index, count in counter.items():
            # print(index, count)

    # numeric analysis
    # print(df.describe())

    # object analysis
    count_cobos_by_category(df)
    




    

if __name__ == '__main__':
    main()
