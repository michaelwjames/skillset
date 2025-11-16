import argparse
import os
from pypdf import PdfReader, PdfWriter

def split_pdf(input_path, output_dir, ranges=None, single_pages=False):
    """
    Splits a PDF into multiple files based on page ranges or into single pages.

    Args:
        input_path (str): The path to the input PDF file.
        output_dir (str): The directory to save the output PDF files.
        ranges (list, optional): A list of page ranges (e.g., "1-5", "8", "10-12"). Defaults to None.
        single_pages (bool, optional): If True, splits the PDF into single-page files. Defaults to False.
    """
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        pdf_reader = PdfReader(input_path)

        if single_pages:
            for i, page in enumerate(pdf_reader.pages):
                pdf_writer = PdfWriter()
                pdf_writer.add_page(page)
                output_path = os.path.join(output_dir, f"page_{i + 1}.pdf")
                with open(output_path, "wb") as out_file:
                    pdf_writer.write(out_file)
            print(f"Successfully split '{input_path}' into {len(pdf_reader.pages)} single-page files in '{output_dir}'")

        elif ranges:
            for i, page_range in enumerate(ranges):
                pdf_writer = PdfWriter()
                start, end = map(int, page_range.split('-'))
                for page_num in range(start - 1, end):
                    pdf_writer.add_page(pdf_reader.pages[page_num])

                output_path = os.path.join(output_dir, f"range_{start}-{end}.pdf")
                with open(output_path, "wb") as out_file:
                    pdf_writer.write(out_file)
            print(f"Successfully split '{input_path}' into {len(ranges)} files based on specified ranges in '{output_dir}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and run the PDF split process.
    """
    parser = argparse.ArgumentParser(
        description="Split a PDF file into multiple documents by page ranges or single pages."
    )
    parser.add_argument(
        "input_file",
        metavar="INPUT_PDF",
        type=str,
        help="The path to the PDF file to split.",
    )
    parser.add_argument(
        "-o",
        "--output-dir",
        dest="output_dir",
        type=str,
        default=".",
        help="The directory where output files will be saved. Defaults to the current directory.",
    )

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-r",
        "--ranges",
        dest="ranges",
        type=str,
        nargs="+",
        help="A list of page ranges to extract (e.g., 1-5 8 10-12).",
    )
    group.add_argument(
        "-s",
        "--single-pages",
        dest="single_pages",
        action="store_true",
        help="Split the PDF into single-page files.",
    )

    args = parser.parse_args()

    split_pdf(args.input_file, args.output_dir, args.ranges, args.single_pages)

if __name__ == "__main__":
    main()