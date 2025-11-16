---
name: pdf-decryptor
description: Remove password protection from encrypted PDF files by providing the password and generating unlocked copies.
---

# PDF Decryptor Skill

This skill removes password protection from encrypted PDF files, creating unlocked copies that can be freely accessed.

## Dependencies

- Python 3.7+
- `pikepdf` library (see `requirements.txt`)

## Installation

Install dependencies:

```bash
pip install -r skillset/pdf-decryptor/requirements.txt
```

## Usage

### Decrypt a single PDF

```bash
python skillset/pdf-decryptor/decrypt_pdf.py --input "path/to/encrypted.pdf" --output "path/to/decrypted.pdf" --password "your-password"
```

### Decrypt multiple PDFs with the same password

```bash
python skillset/pdf-decryptor/decrypt_pdf.py --input "file1.pdf" "file2.pdf" "file3.pdf" --password "your-password"
```

When multiple input files are provided without `--output`, the script will automatically generate output filenames by appending `_unlocked` to the original filename.

## Script Options

- `--input` or `-i`: Input PDF file path(s). Can specify multiple files.
- `--output` or `-o`: Output PDF file path (optional for single file, auto-generated for multiple files).
- `--password` or `-p`: Password to decrypt the PDF(s).
- `--overwrite`: Overwrite output files if they already exist.

## Notes

- Output files are saved with the same directory as input unless a full output path is specified
- For multiple files, output names are automatically generated as `{original_name}_unlocked.pdf`
- The script validates that input files exist and are readable before processing
- Uses `pikepdf` which handles various PDF encryption types reliably
