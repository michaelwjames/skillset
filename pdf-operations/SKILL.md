# PDF Operations

This skill provides a suite of tools for manipulating PDF documents.

## Capabilities
- **Merge**: Combine multiple PDF files into one.
- **Split**: Divide a PDF into separate pages or page ranges.
- **Compress**: Reduce file size by optimizing images and content streams.
- **Watermark**: Add text or image watermarks to pages.
- **Extract Text**: Pull text content from a PDF.
- **Extract Tables**: Identify and extract tabular data into structured formats.
- **Vision OCR**: Convert PDF pages to images and run Groq Vision OCR on each page. *(Uses the external `groq-vision-ocr` skill; ensure it is installed and configured.)*

## Dependencies
- Python 3.10+
- `pypdf`
- `pdfminer.six`
- `reportlab`
- `Pillow`
- `pdf2image`