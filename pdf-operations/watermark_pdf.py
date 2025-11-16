import argparse
import os
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
from io import BytesIO

def create_text_watermark(text, page_size, font_size, color, opacity):
    """Creates a temporary PDF with a text watermark."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=page_size)
    c.setFont("Helvetica", font_size)
    c.setFillColor(color, alpha=opacity)
    c.drawCentredString(page_size[0] / 2, page_size[1] / 2, text)
    c.save()
    packet.seek(0)
    return PdfReader(packet)

def create_image_watermark(image_path, page_size, opacity):
    """Creates a temporary PDF with an image watermark."""
    packet = BytesIO()
    c = canvas.Canvas(packet, pagesize=page_size)
    img = ImageReader(image_path)
    img_width, img_height = img.getSize()
    c.setGlobalAlpha(opacity)
    c.drawImage(img, (page_size[0] - img_width) / 2, (page_size[1] - img_height) / 2, mask='auto')
    c.save()
    packet.seek(0)
    return PdfReader(packet)

def watermark_pdf(input_path, output_path, watermark_text=None, watermark_image=None, font_size=40, color="#C0C0C0", opacity=0.5):
    """
    Adds a text or image watermark to each page of a PDF.

    Args:
        input_path (str): The path to the input PDF file.
        output_path (str): The path to save the watermarked PDF file.
        watermark_text (str, optional): The text to use for the watermark.
        watermark_image (str, optional): The path to the image to use for the watermark.
        font_size (int, optional): The font size for the text watermark.
        color (str, optional): The color of the text watermark in hex format.
        opacity (float, optional): The opacity of the watermark (0.0 to 1.0).
    """
    try:
        pdf_reader = PdfReader(input_path)
        pdf_writer = PdfWriter()

        for i, page in enumerate(pdf_reader.pages):
            page_size = (page.mediabox.width, page.mediabox.height)

            if watermark_text:
                watermark_pdf = create_text_watermark(watermark_text, page_size, font_size, HexColor(color), opacity)
            elif watermark_image:
                watermark_pdf = create_image_watermark(watermark_image, page_size, opacity)
            else:
                raise ValueError("Either watermark_text or watermark_image must be provided.")

            page.merge_page(watermark_pdf.pages[0])
            pdf_writer.add_page(page)

        with open(output_path, "wb") as out_file:
            pdf_writer.write(out_file)

        print(f"Successfully added watermark to '{input_path}' and saved as '{output_path}'")

    except FileNotFoundError:
        print(f"Error: Input file not found at '{input_path}' or watermark image not found.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def main():
    """
    Main function to parse command-line arguments and run the PDF watermarking process.
    """
    parser = argparse.ArgumentParser(description="Add a text or image watermark to a PDF.")
    parser.add_argument("input_file", metavar="INPUT_PDF", type=str, help="The path to the PDF file.")
    parser.add_argument("-o", "--output", dest="output_file", type=str, required=True, help="The path for the output watermarked PDF.")

    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-t", "--text", dest="watermark_text", type=str, help="The watermark text.")
    group.add_argument("-i", "--image", dest="watermark_image", type=str, help="The path to the watermark image.")

    parser.add_argument("--font-size", type=int, default=40, help="Font size for text watermark.")
    parser.add_argument("--color", type=str, default="#C0C0C0", help="Color for text watermark (hex format).")
    parser.add_argument("--opacity", type=float, default=0.5, help="Opacity for the watermark (0.0-1.0).")

    args = parser.parse_args()

    watermark_pdf(args.input_file, args.output_file, args.watermark_text, args.watermark_image, args.font_size, args.color, args.opacity)

if __name__ == "__main__":
    main()