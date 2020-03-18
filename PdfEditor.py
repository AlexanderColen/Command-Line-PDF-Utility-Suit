from PyPDF2 import PdfFileReader, PdfFileMerger, PdfFileWriter
import sys


def handle_command(args: []):
    """
    Handle the command line arguments and redirect them to the proper functions.
    :param args: The arguments that were used to call this script.
    """
    if len(args) < 2:
        print(f"Invalid script usage. Check commands with '{args[0]} help'.")
        return

    command: str = args[1]
    if len(args) >= 3:
        path: str = args[2]

    if command == 'help':
        print('======================\nScript usage commands\n======================')
        print(f'# {args[0]} help')
        print(f'# {args[0]} read <Path/To/Pdf.pdf>')
        print(f'  Example usage: {args[0]} read JobOfferContract.pdf')
        print(f'# {args[0]} merge <Path/To/Pdf1.pdf> <Path/To/Pdf2.pdf> <Path/To/Pdf3.pdf> ...')
        print(f'  Example usage: {args[0]} merge scan1.pdf scan2.pdf scan3.pdf')
        print(f'# {args[0]} split <Path/To/Pdf.pdf> <(Optional) Page number>')
        print(f'  Example usage: {args[0]} split ScannedFiles.pdf 13')
    elif command == 'read':
        print('Attempting to extract PDF information...')
        extract_information(pdf_path=path)
    elif command == 'merge':
        print('Attempting to merge PDF files...')
        merge_pdf(args[2:])
    elif command == 'split':
        print('Attempting to split PDF file(s)...')
        if len(args) == 4 and isinstance(args[3], int):
            # Split with giving split page.
            split_pdf(pdf_path=path, page=args[3])
        else:
            # Split without giving split page.
            split_pdf(pdf_path=path)


def extract_information(pdf_path: str):
    """
    Extract information from a PDF file and displays it on the command line.
    :param pdf_path: The path to the PDF file.
    :return The information belonging to the PDF file.
    """
    try:
        with open(pdf_path, 'rb') as f:
            pdf: PdfFileReader = PdfFileReader(f)
            information = pdf.getDocumentInfo()
            number_of_pages: int = pdf.getNumPages()

        txt = f"Information about {pdf_path}: \n" \
            f"  Author: {information.author}\n" \
            f"  Creator: {information.creator}\n" \
            f"  Producer: {information.producer}\n" \
            f"  Subject: {information.subject}\n" \
            f"  Title: {information.title}\n" \
            f"  Number of pages: {number_of_pages}"

        print(txt)
        return information
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
        output = 'merged'
    if not output.endswith('.pdf'):
        output += '.pdf'

    for f in files:
        try:
            pdf_reader = PdfFileReader(f)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except FileNotFoundError:
            print(f"File '{f}' not found. Double check if the file exists in the specified location.")

    # Write & Save the merged PDF.
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        print(f"Merged existing files together as '{output}'.")


def split_pdf(pdf_path: str, page: int = 0):
    """
    Split a PDF at a certain page and save the results as two new PDF files.
    :param pdf_path: The path to the PDF.
    :param page: The page number where to split. Defaults to 0.
    """
    if not page:
        page = input('At what page do you want to split this document?\n>>> ')

    # TODO: Write split functionality.
    print('NOT YET IMPLENTED. Terminating program.')


if __name__ == '__main__':
    print('================================================\n'
          'Command Line PDF Editor - © Alexander Colen 2020\n'
          '================================================\n')
    handle_command(args=sys.argv)
