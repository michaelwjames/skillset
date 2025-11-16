#!/usr/bin/env python3
"""
PDF Decryptor - Remove password protection from encrypted PDF files.
"""

import argparse
import sys
from pathlib import Path
from typing import List

try:
    import pikepdf
except ImportError:
    print("Error: pikepdf library not found. Please install it:")
    print("  pip install pikepdf")
    sys.exit(1)


def decrypt_pdf(input_path: Path, output_path: Path, password: str, overwrite: bool = False) -> bool:
    """
    Decrypt a password-protected PDF file.
    
    Args:
        input_path: Path to the encrypted PDF
        output_path: Path where the decrypted PDF will be saved
        password: Password to decrypt the PDF
        overwrite: Whether to overwrite existing output file
        
    Returns:
        True if successful, False otherwise
    """
    # Check if input file exists
    if not input_path.exists():
        print(f"Error: Input file not found: {input_path}")
        return False
    
    # Check if output file exists
    if output_path.exists() and not overwrite:
        print(f"Error: Output file already exists: {output_path}")
        print("Use --overwrite to replace it.")
        return False
    
    try:
        # Open the encrypted PDF with password
        with pikepdf.open(input_path, password=password) as pdf:
            # Save without encryption
            pdf.save(output_path)
        
        print(f"✓ Successfully decrypted: {input_path.name} -> {output_path.name}")
        return True
        
    except pikepdf.PasswordError:
        print(f"Error: Incorrect password for {input_path}")
        return False
    except pikepdf.PdfError as e:
        print(f"Error: PDF error for {input_path}: {e}")
        return False
    except Exception as e:
        print(f"Error: Unexpected error for {input_path}: {e}")
        return False


def generate_output_path(input_path: Path) -> Path:
    """Generate an output path by appending '_unlocked' to the filename."""
    stem = input_path.stem
    suffix = input_path.suffix
    return input_path.parent / f"{stem}_unlocked{suffix}"


def main():
    parser = argparse.ArgumentParser(
        description="Remove password protection from encrypted PDF files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Decrypt a single PDF
  python decrypt_pdf.py -i encrypted.pdf -o decrypted.pdf -p mypassword
  
  # Decrypt multiple PDFs (auto-generates output names)
  python decrypt_pdf.py -i file1.pdf file2.pdf file3.pdf -p mypassword
        """
    )
    
    parser.add_argument(
        "-i", "--input",
        nargs="+",
        required=True,
        help="Input PDF file path(s). Can specify multiple files."
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file path (optional for single file, auto-generated for multiple)"
    )
    
    parser.add_argument(
        "-p", "--password",
        required=True,
        help="Password to decrypt the PDF(s)"
    )
    
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite output files if they already exist"
    )
    
    args = parser.parse_args()
    
    # Convert input paths to Path objects
    input_paths = [Path(p) for p in args.input]
    
    # Handle output path(s)
    if len(input_paths) == 1:
        # Single file
        if args.output:
            output_path = Path(args.output)
        else:
            output_path = generate_output_path(input_paths[0])
        
        success = decrypt_pdf(input_paths[0], output_path, args.password, args.overwrite)
        sys.exit(0 if success else 1)
    
    else:
        # Multiple files
        if args.output:
            print("Warning: --output ignored when processing multiple files. Auto-generating names.")
        
        successes = 0
        for input_path in input_paths:
            output_path = generate_output_path(input_path)
            if decrypt_pdf(input_path, output_path, args.password, args.overwrite):
                successes += 1
        
        print(f"\nProcessed {successes}/{len(input_paths)} files successfully.")
        sys.exit(0 if successes == len(input_paths) else 1)


if __name__ == "__main__":
    main()
