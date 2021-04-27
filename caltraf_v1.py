
'''
Report generator of RDA files. This uses Matplotlib plots and the result is a
Latex pdf.


'''
import pandas as pd
from datetime import date, timedelta, time
import numpy as np
import os
import argparse
import copy
# import plotext as plt
from collections import defaultdict

# Latex
# from pylatex import Document, Section, Subsection, Command
# from pylatex.utils import italic, NoEscape

# Typing
from typing import Optional
from typing import Sequence

from plotter import Plotter as plt


def instances_dictionary(instances: pd.Series, dates: list):
    # Make an dictionary of dates and instances (zeros included)
    partial_instances = dict() # instances present in the data
    for k, v in instances.iteritems():
        partial_instances[k.date()] = v

    instances = dict() # instances considering all day in a year
    for day in dates:
        instances[day] = 0 if day not in partial_instances.keys() else partial_instances[day]
    
    return instances


class Productivity_Analizer:
    def __init__(self, sheet_name: str, directory: str, file_prefix: str, cm: str = None, cm_col: str = None):

        data = defaultdict(list)
        caltraf_files = sorted([f for f in os.listdir(directory) if f.endswith(".xls") and f.startswith(file_prefix)])

        for f in caltraf_files:
            df = pd.read_excel(directory + f, sheet_name = sheet_name)
            CM = df[df["CENTRO DE MANTENIMIENTO"] == cm].iloc[:,5:]
            print("-" * 100)
            print(CM)
            
            for index in range(CM.shape[0]):
                data[CM.iloc[index,1] +" - " + CM.iloc[index,0]].append(list(CM.iloc[index,2:].astype(int)))
        self.data = data 


    def caltraf_analysis(self):
        print("\n\nPorcentaje de paso\n")
        for k, v in self.data.items():
            print(k)
            for month in v:
                # 100% = COB, NC, OC, VACANTES + INC + TNP, BLOI, BLOE, FTS, FTE, OPR, ABANDONO, FALLA TEC.
                total = sum(month[:5]) + sum(month[7:])
                if total != month[5]:
                    raise ValueError("Error de suma del total")
                porcentaje_de_paso = month[6] * 100 // total
                print(f"[{'-'*porcentaje_de_paso}|{' '*(100-porcentaje_de_paso)}] {porcentaje_de_paso} %")
        print("\n\nBloqueo interno\n")
        for k, v in self.data.items():
            print(k) # edificio
            bloi = []
            for month in v:
                bloi.append(month[7])
            print(bloi)

def main(argv = None):

    # check arguments
    parser = argparse.ArgumentParser()
    # parser.add_argument('-g', '--grafica', help='Ancho de gráfica', type = int, required = True)
    parser.add_argument('-d', '--directory', help='xls files directory', type = str, required = False)
    parser.add_argument('-cm', help='Centro de Mantenimiento', type = str, required = False)
    parser.add_argument('-cmcol', help='Column to filter by CM (where the CM is)', type = str, required = False)
    parser.add_argument('-s', '--sheet', help='Sheet name for pandas', type = str, required = True)
    parser.add_argument('-p', '--prefix', help='Common prefix of xls files', type=str, required = True)
    parser.add_argument('-f', '--file', help='Output latex file', type=str, required = True)
    parser.add_argument('-a', '--area', help='caltraf | rda | cobos', type=str, required = True)
    # parser.add_argument('-th', '--hora', help='Tipo de hora', type=str, required = True)

    args = parser.parse_args(argv)

    if args.area == 'rda':
        analyzer = Productivity_Analizer(args.area, args.sheet, args.directory, args.cm, args.cmcol, args.prefix)
        analyzer.hourly_reports()
        analyzer.daily_reports()
        analyzer.monthly_report()
        analyzer.plot()
        analyzer.repetitions_analysis()
        analyzer.numeric_analysis()

    if args.area == 'caltraf':
        # analyzer = Productivity_Analizer(args.area, args.sheet, args.directory, args.cm, args.cmcol, args.prefix)
        analyzer = Productivity_Analizer(args.sheet, args.directory, args.prefix, args.cm, args.cmcol)
        analyzer.caltraf_analysis()

if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
