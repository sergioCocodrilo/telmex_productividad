
from pylatex import Document, Section, Subsection, Command, Enumerate
from pylatex.utils import italic, NoEscape
from datetime import date

if __name__ == '__main__':
    doc = Document()

    doc.preamble.append(Command('title', 'Análisis de desempeño'))
    doc.preamble.append(Command('author', 'Sergio Solano'))
    doc.preamble.append(Command('date', date.today()))
    doc.append(NoEscape(r'\maketitle'))

    with doc.create(Section('CalTraf')):
        with doc.create(Enumerate(enumeration_symbol=r"\alph*)",
                                  options={'start': 1})) as enum:
            enum.add_item("CalTraf")
            enum.add_item("Cobos")
            enum.add_item("RDA")
            enum.add_item("Tramos")
            enum.add_item(NoEscape("the third etc \\ldots"))

    with doc.create(Section('Índice')):
        doc.append('Some regular text and some ')
        doc.append(italic('italic text. '))

        with doc.create(Subsection('A subsection')):
            doc.append('Also some crazy characters: $&#{}')

    with doc.create(Section('A second section')):
        doc.append('Some text.')

    doc.generate_pdf('basic_maketitle2', clean_tex=False)
