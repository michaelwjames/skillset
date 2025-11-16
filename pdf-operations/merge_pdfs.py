import argparse
from pypdf import PdfWriter

def merge_pdfs(input_paths, output_path):
    """
    Merges a list of PDF files into a single PDF.

    Args:
        input_paths (list): A list of paths to the input PDF files.
        output_path (str): The path to save the merged PDF file.
    """
    pdf_writer = PdfWriter()
    try:
        for path in input_paths:
            pdf_writer.append(path)

        with open(output_path, "wb") as out_file:
            pdf_writer.write(out_file)
        print(f"Successfully merged {len(input_paths)} PDF(s) into '{output_path}'")
    except FileNotFoundError as e:
        print(f"Error: Input file not found - {e.filename}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and run the PDF merge process.
    """
    parser = argparse.ArgumentParser(
        description="Merge multiple PDF files into a single document."
    )
    parser.add_argument(
        "input_files",
        metavar="INPUT_PDF",
        type=str,
        nargs="+",
        help="A list of PDF files to merge, in order.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=str,
        required=True,
        help="The path for the output merged PDF file.",
    )

    args = parser.parse_args()

    merge_pdfs(args.input_files, args.output_file)

if __name__ == "__main__":
    main()