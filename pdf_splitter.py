#!/usr/bin/env python3
# -*- coding: cp1252 -*-
# Python 3.12.1 Windows
# FileName= pdf_splitter.py

"""
This script divides a PDF file into multiple numbered files starting with
"basename_page_001.pdf" and increments until the last page.

Based on scripts from 
  https://www.blog.pythonlibrary.org/2018/06/07/an-intro-to-pypdf2/
"""

# Changelog
"""
* 2023-09-22: Initial release.
* 2023-12-17: Migrated from PyPDF to pypdf
* 2023-12-17: Added changelog.
"""

# What's New
"""
## 2023-03-08
* Obsoleted PyPDF2 library has been replaced by pypdf
  https://pypi.org/project/PyPDF2/
  https://pypi.org/project/pypdf/
  https://pypdf.readthedocs.io/en/stable/user/migration-1-to-2.html
* `PdfFileReader` and `PdfFileWriter` classes replaced by `PdfReader` and `PdfWriter
* `reader.getNumPages()` method replaced by `len(reader.pages)`.
* `pdf_writer.add_page()` method simplified to `pdf_writer.add_page()`.

## 2021-09-22
* Added leading zeros to filenames less than 10 and two leading zeros to filenames
  less than 100 to ensure compatibility with pdf_merger.py for files up to 99 pages.
"""

# Script Information
fecha_actualizacion = "2023-12-17"

# Imported Libraries
# ------------------
import os
from pypdf import PdfReader, PdfWriter
"""
  Requires pip install pypdf[crypto] or pip install pypdf[full]
"""



def pdf_splitter(path):
    """
    This function takes a PDF file path and splits it into multiple page-numbered PDFs.

    Args:
        path: Path to the input PDF file.
    """

 # Extract filename and extension
    fname = os.path.splitext(os.path.basename(path))[0]

# Open PDF document and read pages
    reader = PdfReader(path)

# Iterate through each page  
    for page in range(len(reader.pages)):
        # Create PdfWriter object
        pdf_writer = PdfWriter()

        #Add page to the output file
        pdf_writer.add_page(reader.pages[page])

        # Generate output filename based on page number
        if page < 9:
            output_filename = '{}_page_00{}.pdf'.format(fname, page+1)
        elif page >= 99:
            output_filename = '{}_page_{}.pdf'.format(fname, page+1)
        else:
            output_filename = '{}_page_0{}.pdf'.format(fname, page+1)
        with open(output_filename, 'wb') as out:
            # Write output file
            pdf_writer.write(out)
        # Print file creation message   
        print('Created: {}'.format(output_filename))


if __name__ == '__main__':
    path = 'revistasic157.pdf'
    pdf_splitter(path)
