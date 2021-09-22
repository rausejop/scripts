# pdf_splitter.py
# Divide un fichero nombre.pdf en varios ficheros comenzando en nombre_page_001.pdf hasta la última página
# Basado en los scripts del siguiente enlace
#  https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
# Actualizado para añadir un cero en ficheros menores de 10 y dos ceros en menores de 100,
#   lo que permite ordenar los ficheros para ser procesados por pdf_merger.py sin que falle hasta 99 páginas

import os
from PyPDF2 import PdfFileReader, PdfFileWriter
def pdf_splitter(path):
    fname = os.path.splitext(os.path.basename(path))[0]
    pdf = PdfFileReader(path)
    for page in range(pdf.getNumPages()):
        pdf_writer = PdfFileWriter()
        pdf_writer.addPage(pdf.getPage(page))
        if page < 9:
            output_filename = '{}_page_00{}.pdf'.format(fname, page+1)
        elif page >= 99:
            output_filename = '{}_page_{}.pdf'.format(fname, page+1)
        else:
            output_filename = '{}_page_0{}.pdf'.format(fname, page+1)
        with open(output_filename, 'wb') as out:
            pdf_writer.write(out)
            
        print('Created: {}'.format(output_filename))


if __name__ == '__main__':
    path = 'revista_ejercito_julio_952.pdf'
    pdf_splitter(path)