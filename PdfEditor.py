from PyPDF2 import PdfFileReader, PdfFileWriter
from typing import List
import sys


def handle_command(args: []):
    """
    Handle the command line arguments and redirect them to the proper functions.
    :param args: The arguments that were used to call this script.
    """
    while True:
        # Ask user what they want to do if no command line arguments were given.
        if len(args) == 1:
            args.append(input('\nWhat would you like to do?\nAvailable actions: help - read - merge - split\n>>>').lower())

        command: str = args[1]

        if command == 'help':
            print('----------------------\nScript usage commands\n----------------------\n'
                  f'# help\n'
                  f'# read <Path/To/Pdf.pdf>\n'
                  f'  Example usage: read JobOfferContract.pdf\n'
                  f'# merge <Path/To/Pdf1.pdf> <Path/To/Pdf2.pdf> <Path/To/Pdf3.pdf> ...\n'
                  f'  Example usage: merge scan1.pdf scan2.pdf scan3.pdf\n'
                  f'# split <Path/To/Pdf.pdf>\n'
                  f'  Example usage: split ScannedFiles.pdf\n')
            return
        elif command == 'read':
            extract_metadata(arguments=args[2:])
            return
        elif command == 'merge':
            merge_pdf(arguments=args[2:])
            return
        elif command == 'split':
            split_pdf(arguments=args[2:])
            return
        elif command in abort_commands:
            return

        print(f'{args[1]} is not a valid command. Please choose one from the list or enter "quit" to stop this application.')
        args.remove(args[1])


def extract_metadata(arguments: List):
    """
    Extract metadata from a PDF file and displays it on the command line.
    :param arguments: The command line arguments given with this command.
    """
    while True:
        while len(arguments) == 0:
            file: str = input('\nWhich file would you like to read?\nTip: Pressing tab auto-completes the filename.\n>>>')
            if file:
                if file in abort_commands:
                    return
                arguments.append(file)
            else:
                print('Please enter a filename.')

        raw_path: str = arguments[0]
        pdf_path: str
        try:
            print('Attempting to extract PDF metadata...')
            if not raw_path.endswith('.pdf'):
                pdf_path = raw_path + '.pdf'
            else:
                pdf_path = raw_path

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
            arguments.remove(raw_path)
            print(f"File '{pdf_path}' not found. Double check if the file exists in the specified location.")


def merge_pdf(arguments: List):
    """
    Merge PDF files together.
    :param arguments: The command line arguments given with this command.
    """
    while True:
        if len(arguments) >= 1:
            if input(f'\nThe following files are in currently in the list: {arguments}\n\n'
                     f'Would you like to add another file? (y/n)\n'
                     f'>>>').lower() not in confirmation:
                break

        file: str = input('\nEnter a filename to merge.\nTip: Pressing tab auto-completes the filename.\n>>>')
        if file:
            if file in abort_commands:
                return
            arguments.append(file)
        else:
            print('Please enter a filename.')

    if len(arguments) == 0:
        print('Merging can only be done for one or more files.')
        return

    pdf_writer: PdfFileWriter = PdfFileWriter()
    files: List[str] = arguments

    # Define output filename ending in .pdf
    output: str = input('Enter filename for output:\n>>> ')
    print('Attempting to merge PDF files...')
    if not output:
        output = 'merged.pdf'
    elif not output.endswith('.pdf'):
        output += '.pdf'

    all_files_exist: bool = True
    for f in files:
        if not f.endswith('.pdf'):
            f += '.pdf'
        try:
            pdf_reader: PdfFileReader = PdfFileReader(f)
            for page in range(pdf_reader.getNumPages()):
                pdf_writer.addPage(pdf_reader.getPage(page))
        except FileNotFoundError:
            print(f"File '{f}' not found. Double check if the file exists in the specified location.")
            all_files_exist = False

    if not all_files_exist:
        if input(f'\nWould you like to merge the existing files anyway? (y/n)\n').lower() not in confirmation:
            return

    # Write & Save the merged PDF.
    with open(output, 'wb') as out:
        pdf_writer.write(out)
        print(f"Merged existing files together as '{output}'.")


def split_pdf(arguments: List):
    """
    Split a PDF at certain pages and save the results as new PDF files.
    :param arguments: The command line arguments given with this command.
    """
    while True:
        while len(arguments) == 0:
            file: str = input('\nWhich file would you like to read?\nTip: Pressing tab auto-completes the filename.\n>>>')
            if file:
                if file in abort_commands:
                    return
                arguments.append(file)
            else:
                print('Please enter a filename.')

        raw_path: str = arguments[0]
        pdf_path: str
        try:
            if not raw_path.endswith('.pdf'):
                pdf_path = raw_path + '.pdf'
            else:
                pdf_path = raw_path

            print('Attempting to split PDF file(s)...')
            # Try to read the file first to check if it exists.
            pdf_reader: PdfFileReader = PdfFileReader(pdf_path)
            pdf_length: int = pdf_reader.getNumPages()

            # Ask what page the user wants to split the PDF.
            pages: [] = [int(input('After which page do you want to split this document?\n>>> ')) - 1]

            while True:
                if input('Would you like to split it again after another page? (y/n)\n>>> ').lower() in confirmation:
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
            min_page: int = -1
            for page in range(pdf_length):
                if min_page == -1:
                    min_page = page + 1
                pdf_writer.addPage(pdf_reader.getPage(page))

                if page in pages:
                    with open(f'split{split}.pdf', 'wb') as out:
                        pdf_writer.write(out)
                        print(f"Split pages {min_page}-{page + 1} into 'split{split}'.")
                    # Re-initiate the writer to empty the pages and increment the split counter.
                    pdf_writer = PdfFileWriter()
                    split += 1
        except FileNotFoundError:
            print(f"File '{pdf_path}' not found. Double check if the file exists in the specified location.")

        if input('Would you like to split another file?\n>>> ').lower() not in ['y', 'yes']:
            return


if __name__ == '__main__':
    print(f'{"="*48}\nCommand Line PDF Editor - © Alexander Colen 2020\n{"="*48}')
    abort_commands = ['"quit"', 'quit', 'q', 'exit']
    confirmation = ['yes', 'ye', 'y']
    handle_command(args=sys.argv)
