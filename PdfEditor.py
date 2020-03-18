from PyPDF2 import PdfFileReader, PdfFileWriter
import sys


def handle_command(args: []):
    """
    Handle the command line arguments and redirect them to the proper functions.
    :param args: The arguments that were used to call this script.
    """

    command: str = args[1]

    if command == 'help':
        print('----------------------\nScript usage commands\n----------------------\n'
              f'# {args[0]} help\n'
              f'# {args[0]} read <Path/To/Pdf.pdf>\n'
              f'  Example usage: {args[0]} read JobOfferContract.pdf\n'
              f'# {args[0]} merge <Path/To/Pdf1.pdf> <Path/To/Pdf2.pdf> <Path/To/Pdf3.pdf> ...\n'
              f'  Example usage: {args[0]} merge scan1.pdf scan2.pdf scan3.pdf\n'
              f'# {args[0]} split <Path/To/Pdf.pdf>\n'
              f'  Example usage: {args[0]} split ScannedFiles.pdf\n')
        return

    if len(args) < 3:
        print(f"Invalid script usage. Check commands with '{args[0]} help'.")
        return

    if command == 'read':
        print('Attempting to extract PDF metadata...')
        extract_metadata(pdf_path=args[2])
        return
    elif command == 'merge':
        print('Attempting to merge PDF files...')
        merge_pdf(args[2:])
        return
    elif command == 'split':
        print('Attempting to split PDF file(s)...')
        split_pdf(pdf_path=args[2])
        return

    print(f"Invalid script usage. Check commands with '{args[0]} help'.")


def extract_metadata(pdf_path: str):
    """
    Extract metadata from a PDF file and displays it on the command line.
    :param pdf_path: The path to the PDF file.
    """
    try:
        if not pdf_path.endswith('.pdf'):
            pdf_path += '.pdf'

        with open(pdf_path, 'rb') as f:
            pdf_reader: PdfFileReader = PdfFileReader(f)
            information = pdf_reader.getDocumentInfo()
            pages = pdf_reader.getNumPages()

        txt = f"Information about {pdf_path}: \n" \
            f"  Author: {information.author}\n" \
            f"  Creator: {information.creator}\n" \
            f"  Producer: {information.producer}\n" \
            f"  Subject: {information.subject}\n" \
            f"  Title: {information.title}\n" \
            f"  Number of pages: {pages}"

        print(txt)
    except FileNotFoundError:
        print(f"File '{pdf_path}' not found. Double check if the file exists in the specified location.")


def merge_pdf(files: []):
    """
    Merge PDF files together.
    :param files: An array of paths to PDF files.
    """
    pdf_writer: PdfFileWriter = PdfFileWriter()

    # Define output filename ending in .pdf
    output: str = input('Enter filename for output:\n>>> ')
    if not output:
        output = 'merged.pdf'
    elif not output.endswith('.pdf'):
        output += '.pdf'

    for f in files:
        if not f.endswith('.pdf'):
            f += '.pdf'
        try:
            pdf_reader: PdfFileReader = PdfFileReader(f)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except FileNotFoundError:
            print(f"File '{f}' not found. Double check if the file exists in the specified location.")

    # TODO: Check if files were found before trying to save in case of empty/unfound files.
    # Write & Save the merged PDF.
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        print(f"Merged existing files together as '{output}'.")


def split_pdf(pdf_path: str):
    """
    Split a PDF at certain pages and save the results as new PDF files.
    :param pdf_path: The path to the PDF.
    """
    try:
        if not pdf_path.endswith('.pdf'):
            pdf_path += '.pdf'

        # Try to read the file first to check if it exists.
        pdf_reader: PdfFileReader = PdfFileReader(pdf_path)
        pdf_length: int = pdf_reader.getNumPages()

        # Ask what page the user wants to split the PDF.
        pages: [] = [int(input('After which page do you want to split this document?\n>>> ')) - 1]

        while True:
            if input('Would you like to split it again after another page? (y/n)\n>>> ').lower() in ['y', 'yes']:
                page: int = int(input('After which page do you want to split this document?\n>>> ')) - 1
                if pdf_length > page:
                    pages.append(page)
                else:
                    print(f'Cannot split after {page} because the selected PDF only has {pdf_length} pages.')
            else:
                pages.append(pdf_length - 1)
                break

        pdf_writer: PdfFileWriter = PdfFileWriter()
        split: int = 1
        for page in range(pdf_length):
            pdf_writer.addPage(pdf_reader.getPage(page))

            if page in pages:
                with open(f'split{split}.pdf', 'wb') as out:
                    pdf_writer.write(out)
                    print(f"Merged existing files together as 'split{split}'.")
                # Re-initiate the writer to empty the pages and increment the split counter.
                pdf_writer = PdfFileWriter()
                split += 1
    except FileNotFoundError:
        print(f"File '{pdf_path}' not found. Double check if the file exists in the specified location.")


if __name__ == '__main__':
    print('================================================\n'
          'Command Line PDF Editor - © Alexander Colen 2020\n'
          '================================================\n')
    handle_command(args=sys.argv)
