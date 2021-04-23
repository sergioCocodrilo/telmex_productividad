from fpdf import FPDF

class PDF(FPDF):
    def lines(self):
        self.set_line_width(0.0)
        self.line(0, pdf_h / 2, 210, pdf_h / 2)

pdf = PDF(orientation = 'P', unit = 'mm', format='A4')
pdf.add_page()

pdf_w = 210
pdf_h = 297

# pdf.output('test.pdf', 'F')



