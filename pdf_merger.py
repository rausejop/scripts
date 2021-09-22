# pdf_merger.py
# Mezcla en un único fichero el resultado de los ficheros generados por pdf_splitter.py en varios ficheros comenzando en nombre_page_001.pdf hasta la última página
# Basado en los scripts del siguiente enlace
#  https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/

import os
import glob
from PyPDF2 import PdfFileWriter, PdfFileReader

def merger(output_path, input_paths):
    pdf_writer = PdfFileWriter()
            
    for path in input_paths:
        pdf_reader = PdfFileReader(path)
        for page in range(pdf_reader.getNumPages()):
            pdf_writer.addPage(pdf_reader.getPage(page))
        
    with open(output_path, 'wb') as fh:
        pdf_writer.write(fh)
        
        
if __name__ == '__main__':
    paths = glob.glob('revista_ejercito_julio_952_*.pdf')
    paths.sort()
    merger('Fichero_completo.pdf', paths)