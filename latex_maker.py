
from pylatex import Document, Section, Subsection, Command, Enumerate, Figure, NoEscape
from pylatex.utils import italic, NoEscape
from datetime import date
import matplotlib.pyplot as plt

from graphical_plotter import single_line_plot as slp
import cobos

def make_report_header():

    doc = Document()

    doc.preamble.append(Command('title', 'Análisis de desempeño'))
    doc.preamble.append(Command('author', 'Sergio Solano'))
    doc.preamble.append(Command('date', date.today()))
    doc.append(NoEscape(r'\maketitle'))

def add_text_section(doc: Document, section_title: str, section_body: str):
    with doc.create(Section(section_title)):
        doc.append(section_body)
    return doc

def add_plot_section(doc, ax):
    d = dict()
    d['theme'] = 'test'
    d['title'] = 'test'
    d['cols'] = ('test', 'coltest')
    d['xys'] = {
        'x': [0, 1, 2, 3, 4, 5, 6],
        'y': [1, 2, 4, 8, 16, 32, 64]
        }
    ax = slp(d)
    for k, v in d['xys'].items():
        print(k, v)
    ax.bar(d['xys']['x'], d['xys']['y'])
    ax.plot()
    with doc.create(Figure(position = 'htbp')) as plot:
        plot.add_plot(width = NoEscape(r'1\textwidth'))
        plot.add_caption('Plot caption')

def write_pdf(doc: Document, name: str):
    today = str(date.today()).replace('-', '_')
    doc.generate_pdf(name + today, clean_tex = False)

if __name__ == '__main__':

    # testing plots
    d = dict()
    d['theme'] = 'test'
    d['title'] = 'test'
    d['cols'] = ('test', 'coltest')
    d['xys'] = {
        'x': [0, 1, 2, 3, 4, 5, 6],
        'y': [1, 2, 4, 8, 16, 32, 64]
        }
    ax = slp(d)
    for k, v in d['xys'].items():
        print(k, v)
    ax.bar(d['xys']['x'], d['xys']['y'])
    ax.plot()

    with doc.create(Section('Cobos')):
        doc.append('Text before plot')
        with doc.create(Figure(position = 'htbp')) as plot:
            plot.add_plot(width = NoEscape(r'1\textwidth'))
            plot.add_caption('Plot caption')
        doc.append('Text after plot')

    # today = str(date.today()).replace('-', '_')
    # doc.generate_pdf('cobos' + today, clean_tex=False)
