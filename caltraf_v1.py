
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
from collections import defaultdict

def instances_dictionary(instances: pd.Series, dates: list):
    # Make an dictionary of dates and instances (zeros included)
    partial_instances = dict() # instances present in the data
    for k, v in instances.iteritems():
        partial_instances[k.date()] = v

    instances = dict() # instances considering all day in a year
    for day in dates:
        instances[day] = 0 if day not in partial_instances.keys() else partial_instances[day]
    
    return instances


def load_data(sheet_name: str, directory: str, file_prefix: str, cm: str = None, cm_col: str = None):
    data = defaultdict(list)
    caltraf_files = sorted([f for f in os.listdir(directory) if f.endswith(".xls") and f.startswith(file_prefix)])

    for f in caltraf_files:
        df = pd.read_excel(directory + f, sheet_name = sheet_name)
        CM = df[df[cm_col] == cm].iloc[:,5:]
        
        for index in range(CM.shape[0]):
            data[CM.iloc[index,1] +" - " + CM.iloc[index,0]].append(list(CM.iloc[index,2:].astype(int)))
    return data 


def caltraf_analysis(data):
    plots = []
    for edificio, v in data.items():
        xys = dict()
        for i, month in enumerate(v, start = 1):
            # 100% = COB, NC, OC, VACANTES + INC + TNP, BLOI, BLOE, FTS, FTE, OPR, ABANDONO, FALLA TEC.
            total = sum(month[:5]) + sum(month[7:])
            if total != month[5]:
                raise ValueError("Error de suma del total")
            porcentaje_de_paso = month[6] * 100 // total
            xys[i] = porcentaje_de_paso
        
        d = dict()
        d['theme'] = 'Porcentaje de paso'
        d['title'] = edificio
        d['cols'] = ('Mes', 'Paso (%)')
        d['xys'] = xys
        plots.append(copy.deepcopy(d))

        bloi = []
        xys = dict()
        for i, month in enumerate(v, start = 1):
            bloi.append(month[7])
            xys[i] = month[7]
        d['theme'] = 'Bloqueo interno'
        d['cols'] = ('Mes', 'Bloqueos Internos')
        d['xys'] = xys
        # if 'S23T' not in edificio and 'ERMITA' not in edificio:
            # plots.append(copy.deepcopy(d))
        plots.append(copy.deepcopy(d))
    return plots

def my_plotter(plots):
    from plotter import Plotter as plt
    for d in plots:
        plot = plt(140)
        plot.set_values(d['xys'].keys(), d['xys'].values(), d['cols'][0], d['cols'][1])
        plot.show(d['theme'] + ' ' + d['title'])

def plt_plotter(plots):
    import matplotlib.pyplot as plt
    bloi_plot = []
    paso_plot = []

    for plot in plots:
        if plot['theme'] == 'Bloqueo interno':
            bloi_plot.append(plot)
        else:
            paso_plot.append(plot)

    for bloi in bloi_plot:
        x, y = bloi['xys'].keys(), bloi['xys'].values()
        plt.plot(x, y, label = bloi['title'])

    plt.title('Bloqueo interno')
    plt.legend()
    plt.show()

    for paso in paso_plot:
        x, y = paso['xys'].keys(), paso['xys'].values()
        plt.plot(x, y, label = paso['title'])

    plt.title('Paso interno')
    plt.legend()
    plt.show()


def main(argv = None):

    # arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--directory', help='xls files directory', type = str, required = True)
    parser.add_argument('-cm', help='Centro de Mantenimiento', type = str, required = True)
    parser.add_argument('-cmcol', help='Column to filter by CM (where the CM is)', type = str, required = True)
    parser.add_argument('-s', '--sheet', help='Sheet name for pandas', type = str, required = True)
    parser.add_argument('-p', '--prefix', help='Common prefix of xls files', type=str, required = True)

    args = parser.parse_args(argv)

    data = load_data(args.sheet, args.directory, args.prefix, args.cm, args.cmcol)
    plots = caltraf_analysis(data)
    # my_plotter(plots)
    plt_plotter(plots)

if __name__ == '__main__':
    main()

# checkout corella in github
# https://github.com/nk412/corella
