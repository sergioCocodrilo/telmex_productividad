
import argparse

from read_report import read_data
from filter_dataframe import filter_df
import latex_maker
from cobos import cobos_analysis

def main(argv = None):
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

    # date_results, numeric_results, category_results = cobos_analysis(df)
    return cobos_analysis(df)

if __name__ == '__main__':
    date_results, numeric_results, category_results = main()
