# Command-Line-PDF-Utility-Suit
Command line PDF utility suit written in Python3.

PDF utility suit allowing easy merging, splitting and simple editing of PDF files.

To run the project, clone the repository or download the PdfEditor.py file from this project.
It can be executed using Python3 by running: `python3 PdfEditor.py <command>`.

Available commands:
* help - Display help with commands including example usage.
* read - Displays metadata information about the PDF, including title, subject, author and page numbers. For reading the text of a PDF, use [PDFMiner](https://pypi.org/project/pdfminer/).
* merge - Merges multiple PDF files in order together into one new PDF file.
* split - Splits a PDF file into multiple files at certain pages.
