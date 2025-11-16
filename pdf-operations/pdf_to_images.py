import argparse
import os
from pathlib import Path
from typing import List

from pdf2image import convert_from_path

def pdf_to_images(pdf_path: str, output_dir: str = None, dpi: int = 300) -> List[Path]:
    """Convert each page of a PDF to a PNG image.

    Returns a list of image file paths.
    """
    pdf_path = Path(pdf_path)
    if not pdf_path.is_file():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    if output_dir is None:
        output_dir = pdf_path.parent / "_pdf_images"
    else:
        output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    images = convert_from_path(str(pdf_path), dpi=dpi)
    image_paths: List[Path] = []
    for i, img in enumerate(images, start=1):
        img_path = output_dir / f"page_{i}.png"
        img.save(img_path, "PNG")
        image_paths.append(img_path)
    return image_paths

def main():
    parser = argparse.ArgumentParser(description="Convert a PDF into per‑page PNG images.")
    parser.add_argument("pdf_path", help="Path to the PDF file.")
    parser.add_argument("-o", "--output-dir", help="Directory to store images (default: <pdf>/_pdf_images).")
    parser.add_argument("-d", "--dpi", type=int, default=300, help="Resolution for image conversion (default 300).")
    args = parser.parse_args()

    images = pdf_to_images(args.pdf_path, args.output_dir, args.dpi)
    for p in images:
        print(p)

if __name__ == "__main__":
    main()
