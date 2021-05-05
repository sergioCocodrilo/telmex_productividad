from pylatex import Document, Section, Figure, NoEscape, Command
import datetime

def create_document(fname: str) -> Document:
    geometry_options = {"right": "2cm", "left": "2cm"}
    doc = Document(fname, geometry_options=geometry_options)
    return doc

def add_header(doc: Document, title: str, author: str) -> Document:
    date = str(datetime.date.today())
    doc.preamble.append(Command('title', title))
    doc.preamble.append(Command('author', author))
    doc.preamble.append(Command('date', date))
    doc.append(NoEscape(r'\maketitle'))
    return doc

def add_section(doc: Document, sec_title: str, sec_content: str) -> Document:
    with doc.create(Section(sec_title)):
        doc.append(sec_content)
    return doc

def write_document(doc: Document, title: str, directory: str):
    doc.generate_pdf(directory + title, clean_tex=False)

def add_plot(doc: Document, width, *args, **kwargs) -> Document:
    with doc.create(Figure(position='htbp')) as plot:
        plot.add_plot(width=NoEscape(width), *args, **kwargs)
        plot.add_caption('I am a caption.')
    return doc

############################### Test the previous functions

import matplotlib.pyplot as plt
import numpy as np

def produce_data():
    x = np.linspace(0, 2 * np.pi, 400)
    y = np.sin(x ** 2)
    return x, y

def plot(x, y):
    fig, ax = plt.subplots()
    ax.plot(x, y)
    ax.set_title('A single plot')
    return ax

def test_write():
    doc = create_document('last chance name')
    doc = add_header(doc, 'Chico Trujillo', 'Aldo Asenjo')
    doc = add_section(doc, 'Y ahora quién', 'Sino soy yo, ..., el beso que pudo ser')

    # plot test
    x, y = produce_data()
    ax = plot(x, y)
    ax.plot()
    add_plot(doc, r'1\textwidth', dpi=300)
    
    ax.plot()
    add_plot(doc, r'1\textwidth', dpi=300)

    write_document(doc, 'Lyrics.pdf', '/tmp/')

if __name__ == '__main__':
    test_write()
