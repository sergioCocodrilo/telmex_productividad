
#-------------------- reading files
import os

def open_files(directory = None):
    file_dir = directory if directory else os.path.abspath("../Datos")
    files = os.listdir(file_dir)
    return file_dir, files 

import pandas as pd
from collections import defaultdict

def caltraf(file_dir, files, cm):
    data = defaultdict(list)
    for f in files:
        df = pd.read_excel(file_dir + "/" + f, sheet_name="Datos")
        CM = df[df["CENTRO DE MANTENIMIENTO"] == cm].iloc[:,5:]
        print("-" * 100)
        print(CM)
        
        for index in range(CM.shape[0]):
            data[CM.iloc[index,1] +" - " + CM.iloc[index,0]].append(list(CM.iloc[index,2:].astype(int)))
    return data 



#--------------------  data processing

def data_analysis(data):
    """Input: dictionary with the buildings and its months values as lists"""
    """
    for k, v in data.items():
        print(k)
        for month in v:
            print(month)
    """

    print("\n\nPorcentaje de paso\n")

    for k, v in data.items():
        print(k)
        for month in v:
            # 100% = COB, NC, OC, VACANTES + INC + TNP, BLOI, BLOE, FTS, FTE, OPR, ABANDONO, FALLA TEC.
            total = sum(month[:5]) + sum(month[7:])
            if total != month[5]:
                raise ValueError("Error de suma del total")
            porcentaje_de_paso = month[6] * 100 // total
            print(f"[{'-'*porcentaje_de_paso}|{' '*(100-porcentaje_de_paso)}] {porcentaje_de_paso} %")
    """
    DATA ORDER:
    0  A.- Cob	
    1  B.- NC
    2  C.- OC	
    3  D.- INC	
    4  E.- TNP	
    5  F.- Intentos	
    6  Paso	
    7  Bloi	
    8  Bloe	
    9 FTS	
    10 FTE	
    11 OPR	
    12 Vacantes	
    13 Falla Tecnica
    """
    print("\n\nBloqueo interno\n")
    for k, v in data.items():
        print(k) # edificio
        bloi = []
        for month in v:
            bloi.append(month[7])
        print(bloi)
#-------------------- main processing
if __name__ == "__main__":
    file_dir, files = open_files()
    caltraf_files = [f for f in files if f.lower().startswith("caltraf")]
    #[print(f) for f in caltraf_files]

    cm = input("¿Qué CM te interesa? ")
    data = caltraf(file_dir, sorted(caltraf_files), cm)
    data_analysis(data)
