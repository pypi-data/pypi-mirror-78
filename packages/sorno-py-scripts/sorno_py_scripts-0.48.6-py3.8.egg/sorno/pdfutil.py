from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals

import PyPDF2

def pdf_to_text(filepath):
    with open(filepath, "rb") as file_obj:
        pdf_reader = PyPDF2.PdfFileReader(file_obj)
        num_pages = pdf_reader.numPages

        count = 0
        text_segments = []
        while count < num_pages:
            text_segments.append(pdf_reader.getPage(count).extractText())
            count += 1

        return ''.join(text_segments)
