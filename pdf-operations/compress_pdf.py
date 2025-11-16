import argparse
import os
from pypdf import PdfReader, PdfWriter

def compress_pdf(input_path, output_path):
    """
    Compresses a PDF file by optimizing its content streams and removing duplicate objects.

    Args:
        input_path (str): The path to the input PDF file.
        output_path (str): The path to save the compressed PDF file.
    """
    try:
        pdf_reader = PdfReader(input_path)
        pdf_writer = PdfWriter()

        for page in pdf_reader.pages:
            pdf_writer.add_page(page)

        # This operation cleans up and compresses content streams
        for page in pdf_writer.pages:
            page.compress_content_streams()

        with open(output_path, "wb") as out_file:
            pdf_writer.write(out_file)

        original_size = os.path.getsize(input_path)
        compressed_size = os.path.getsize(output_path)
        reduction = (original_size - compressed_size) / original_size * 100

        print(f"Successfully compressed '{input_path}' to '{output_path}'")
        print(f"Original size: {original_size / 1024:.2f} KB")
        print(f"Compressed size: {compressed_size / 1024:.2f} KB")
        print(f"File size reduced by {reduction:.2f}%")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and run the PDF compression process.
    """
    parser = argparse.ArgumentParser(
        description="Compress a PDF file to reduce its size."
    )
    parser.add_argument(
        "input_file",
        metavar="INPUT_PDF",
        type=str,
        help="The path to the PDF file to compress.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=str,
        required=True,
        help="The path for the output compressed PDF file.",
    )

    args = parser.parse_args()

    compress_pdf(args.input_file, args.output_file)

if __name__ == "__main__":
    main()