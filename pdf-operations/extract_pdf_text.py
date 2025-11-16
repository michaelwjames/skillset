import argparse
from pdfminer.high_level import extract_text

def extract_pdf_text(input_path, output_path=None):
    """
    Extracts text from a PDF file.

    Args:
        input_path (str): The path to the input PDF file.
        output_path (str, optional): The path to save the extracted text.
                                     If None, prints to stdout.
    """
    try:
        text = extract_text(input_path)

        if output_path:
            with open(output_path, "w", encoding="utf-8") as out_file:
                out_file.write(text)
            print(f"Successfully extracted text from '{input_path}' to '{output_path}'")
        else:
            print(text)

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}'")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and run the PDF text extraction.
    """
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file."
    )
    parser.add_argument(
        "input_file",
        metavar="INPUT_PDF",
        type=str,
        help="The path to the PDF file from which to extract text.",
    )
    parser.add_argument(
        "-o",
        "--output",
        dest="output_file",
        type=str,
        help="The path to save the extracted text as a .txt file. If not provided, prints to console.",
    )

    args = parser.parse_args()

    extract_pdf_text(args.input_file, args.output_file)

if __name__ == "__main__":
    main()