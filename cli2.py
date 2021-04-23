
import inspect
import typing
import argparse

import rda_spanish

def main(argv = None):

    # check arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("-g", "--grafica", help="Ancho de gráfica", type = int, required = True)
    parser.add_argument("-d", "--directorio", help="Ubicación de los archivos a leer", type = str, required = True)
    parser.add_argument("-cm", help="Centro de Mantenimiento", type = str, required = True)
    parser.add_argument("-p", "--prefijo", help="Prefijo de los archivos a leer", type=str)
    parser.add_argument("-th", "--hora", help="Tipo de hora", type=str, required = True)

    try:
        args = parser.parse_args(argv)
    except:
        print('''
        Se requieren los siguientes argumentos:
            -g/--grafica,
            -d/--directorio,
            -cm
            -p/--prefijo
            -th/--hora

        Entonces necesitas ejecutar este archivo con una instrucción similar a:
        productividad_rda -d C:\\TELMEX\\Productividad\\RDA\\ -g 120 -cm CMABS -p rdat_metro -th HORA_REAL
        ''')
        return 1


    # read files
    df = rda_spanish.leer_archivos(args.directorio, args.prefijo)
    return df

    commands = [f for f in inspect.getmembers(rda_spanish) if inspect.isfunction(f[1])]
    commands_dict = {}
    print('¿Qué deseas hacer?')
    for i, c in enumerate(commands, start=1):
        name = c[0]
        docs = c[1].__doc__
        args = typing.get_type_hints(c[1])
        print(f'\t{i}. {name}')

if __name__ == '__main__':
    df = main()
