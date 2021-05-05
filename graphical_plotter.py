
import matplotlib.pyplot as plt

# def single_line_plot(plots):
    # for plot in plots:
        # x, y = plot['xys'].keys(), plot['xys'].values()
        # # plt.plot(x, y)
        # plt.bar(x, y)
        # plt.title(plot['title'])
        # plt.legend()
        # plt.show()

# this is where the plotting configuration should happend
def single_line_plot(plot):
    print(plot)
    f, ax = plt.subplots()
    x, y = plot['xys'].keys(), plot['xys'].values()
    # plt.plot(x, y)
    # ax.bar(x, y)
    # ax.title(plot['title'])
    # ax.legend()
    return ax
    # plt.show()

def plt_plotter(plots):
    '''
    plots is a list of dictionaries, each with the structure:
        d['theme']
        d['title']
        d['cols']
        d['xys']
    '''
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
