"""CLI tool for running Groq Llama 4 Scout OCR on a PDF document.

Features:
- Converts each page of a PDF to a PNG image.
- Sends a user-provided prompt alongside each page image for OCR.
- Aggregates the results and converts model output into a single CSV or Markdown file.

PowerShell Usage Examples:
# Basic usage with simple prompt
python pdf-vision-ocr/pdf_vision_ocr.py --pdf "path/to/file.pdf" --prompt "simple text" --mode table

# Usage with complex prompt (use single quotes to preserve spaces)
python pdf-vision-ocr/pdf_vision_ocr.py --pdf "path/to/file.pdf" --prompt 'Extract all key financial amounts, tax year dates. Provide section headings matching the certificate, list each data point with labels and values, and summarize any totals or important notes.' --mode table

# Output to text mode
python pdf-vision-ocr/pdf_vision_ocr.py --pdf "path/to/file.pdf" --prompt "extract text content" --mode text

PowerShell Command Formatting Tips:
- Use single quotes for prompts with spaces and special characters: --prompt 'your text here'
- Use double quotes for file paths with spaces: --pdf "path with spaces/file.pdf"
- Avoid complex punctuation in prompts when possible
- Keep prompts concise or use single quotes to preserve formatting
"""

from __future__ import annotations

import argparse
import datetime
import time
import base64
import csv
import json
import mimetypes
import os
import sys
import tempfile
from pathlib import Path
from typing import Iterable, List, Sequence

from groq import Groq
from pdf2image import convert_from_path

DEFAULT_MODEL = "meta-llama/llama-4-scout-17b-16e-instruct"
TABLE_SYSTEM_PROMPT = (
    "You are an OCR specialist. Extract tabular data from images and respond "
    "with a JSON object containing a 'columns' array and a 'rows' array. Each "
    "entry in 'rows' must match the length and ordering of 'columns'."
)
TEXT_SYSTEM_PROMPT = (
    "You are an OCR specialist. Extract textual content from images and "
    "respond in clear Markdown with sections, lists, and code fences when "
    "appropriate."
)


class OCRScriptError(Exception):
    """Custom exception for predictable script failures."""


def load_env_from_file() -> None:
    """Populate environment variables from a nearby .env file if needed."""
    if os.getenv("GROQ_API_KEY"):
        return

    candidate_dirs = [
        Path.cwd(),
        Path(__file__).resolve().parent,
        Path(__file__).resolve().parent.parent,
    ]

    for directory in candidate_dirs:
        if directory is None:
            continue
        env_path = directory / ".env"
        if not env_path.exists():
            continue

        for line in env_path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue

            if stripped.lower().startswith("export "):
                stripped = stripped[7:].lstrip()

            key, sep, value = stripped.partition("=")
            if not sep:
                continue

            key = key.strip()
            value = value.strip()
            if key and not os.getenv(key):
                os.environ[key] = value
        break


def infer_mode(prompt: str, mode_arg: str | None) -> str:
    """Infer output mode based on CLI flag or prompt content."""
    if mode_arg:
        return mode_arg

    lowered = prompt.lower()
    if "table" in lowered or "csv" in lowered:
        return "table"
    return "text"


def encode_local_image(path: Path) -> str:
    """Return a data URL for a local image file."""
    if not path.is_file():
        raise OCRScriptError(f"Image path does not exist or is not a file: {path}")

    mime_type, _ = mimetypes.guess_type(path.name)
    if mime_type is None:
        mime_type = "image/png"  # Default for our temp files

    with path.open("rb") as image_file:
        b64 = base64.b64encode(image_file.read()).decode("utf-8")
    return f"data:{mime_type};base64,{b64}"


def build_image_contents(image_inputs: Sequence[str]) -> List[dict]:
    """Convert image paths/URLs into Groq message content entries."""
    if not image_inputs:
        raise OCRScriptError("At least one image must be supplied.")

    contents: List[dict] = []
    for raw in image_inputs:
        raw = raw.strip()
        if raw.startswith("http://") or raw.startswith("https://"):
            url = raw
        else:
            url = encode_local_image(Path(raw))

        contents.append({"type": "image_url", "image_url": {"url": url}})

    return contents


def call_groq(
    prompt: str,
    image_contents: Sequence[dict],
    mode: str,
    model: str = DEFAULT_MODEL,
    temperature: float = 0.1,
) -> str:
    load_env_from_file()
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise OCRScriptError("GROQ_API_KEY environment variable is required.")

    client = Groq(api_key=api_key)

    start_time = time.time()

    messages: List[dict] = [
        {"role": "system", "content": TABLE_SYSTEM_PROMPT if mode == "table" else TEXT_SYSTEM_PROMPT},
        {"role": "user", "content": [{"type": "text", "text": prompt}, *image_contents]},
    ]

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_completion_tokens": 1024,
    }

    if mode == "table":
        kwargs["response_format"] = {"type": "json_object"}

    completion = client.chat.completions.create(**kwargs)
    elapsed = time.time() - start_time

    usage = getattr(completion, 'usage', None)
    total_tokens = getattr(usage, 'total_tokens', 'N/A') if usage else 'N/A'
    prompt_tokens = getattr(usage, 'prompt_tokens', 'N/A') if usage else 'N/A'
    completion_tokens = getattr(usage, 'completion_tokens', 'N/A') if usage else 'N/A'

    print(
        f"[INFO] Groq API call completed in {elapsed:.2f}s | "
        f"total_tokens={total_tokens} prompt_tokens={prompt_tokens} completion_tokens={completion_tokens}",
        file=sys.stderr,
    )

    content = completion.choices[0].message.content
    if content is None:
        raise OCRScriptError("Empty response received from the Groq API.")
    return content


def write_csv(output_path: Path, header: list[str], rows: list[list[str]]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(header)
        writer.writerows(rows)


def write_markdown(output_path: Path, payload: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Groq Llama 4 Scout OCR helper for PDFs")
    parser.add_argument(
        "--pdf",
        required=True,
        help="PDF file path to process."
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Instruction for the model (e.g., describe extraction goals). In PowerShell, use single quotes for prompts with spaces: --prompt 'your text here'"
    )
    parser.add_argument(
        "--mode",
        choices=["table", "text"],
        help="Force output mode. Defaults to 'table' when prompt references tables; otherwise 'text'."
    )
    parser.add_argument(
        "--model",
        default=DEFAULT_MODEL,
        help=f"Groq vision model to use (default: {DEFAULT_MODEL})."
    )
    parser.add_argument(
        "--temperature",
        type=float,
        default=0.1,
        help="Sampling temperature for the model (default: 0.1)."
    )
    parser.add_argument(
        "--output",
        help="Optional output file path. Defaults to 'ocr_result.csv' or 'ocr_result.md'."
    )
    return parser.parse_args(list(argv))


def main(argv: Sequence[str] | None = None) -> int:
    # Show PowerShell usage tips on first run
    if not any(arg.startswith('--') for arg in (argv or sys.argv[1:])):
        print("PowerShell Usage Tips:", file=sys.stderr)
        print("- Use single quotes for prompts with spaces: --prompt 'your text here'", file=sys.stderr)
        print("- Use double quotes for file paths with spaces: --pdf \"path with spaces/file.pdf\"", file=sys.stderr)
        print("- Run with --help for full usage examples", file=sys.stderr)
        print("", file=sys.stderr)
    
    args = parse_args(argv or sys.argv[1:])

    try:
        mode = infer_mode(args.prompt, args.mode)

        pdf_path = Path(args.pdf)
        if not pdf_path.is_file():
            raise OCRScriptError(f"PDF path does not exist or is not a file: {pdf_path}")

        print(f"Converting PDF '{pdf_path.name}' to images...", file=sys.stderr)
        images_from_pdf = convert_from_path(pdf_path)
        if not images_from_pdf:
            raise OCRScriptError("pdf2image failed to convert any pages from the PDF.")
        print(f"Successfully converted {len(images_from_pdf)} pages.", file=sys.stderr)

        aggregated_markdown = []
        all_rows = []
        header = []

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir)
            for i, image_obj in enumerate(images_from_pdf):
                page_num = i + 1
                print(f"Processing page {page_num} of {len(images_from_pdf)}...", file=sys.stderr)

                temp_image_file = temp_path / f"page_{page_num}.png"
                image_obj.save(temp_image_file, "PNG")

                contents = build_image_contents([str(temp_image_file)])
                page_prompt = f"This is page {page_num} of a document. {args.prompt}"

                response = call_groq(
                    prompt=page_prompt,
                    image_contents=contents,
                    mode=mode,
                    model=args.model,
                    temperature=args.temperature,
                )

                if mode == "table":
                    try:
                        data = json.loads(response)
                        if page_num == 1:
                            if isinstance(data, dict) and "columns" in data:
                                header = data["columns"]
                                all_rows.extend(data.get("rows", []))
                            elif isinstance(data, list) and data:
                                header = sorted({key for row in data for key in row.keys()})
                                all_rows.extend([[row.get(col, "") for col in header] for row in data])
                        else:
                            if isinstance(data, dict) and "rows" in data:
                                all_rows.extend(data["rows"])
                            elif isinstance(data, list) and data:
                                all_rows.extend([[row.get(col, "") for col in header] for row in data])
                    except (json.JSONDecodeError, TypeError):
                        print(f"Warning: Could not parse table JSON for page {page_num}. Skipping.", file=sys.stderr)
                else:
                    aggregated_markdown.append(f"\n\n---\n\n# Page {page_num}\n\n{response}")

        # Generate output file in same directory as input PDF
        pdf_path = Path(args.pdf)
        output_dir = pdf_path.parent
        
        # Use same name as input file but with appropriate extension
        base_name = pdf_path.stem
        default_name = f"{base_name}.csv" if mode == "table" else f"{base_name}.md"
        output_file = Path(args.output) if args.output else Path(default_name)
        output_path = output_dir / output_file

        if mode == "table":
            write_csv(output_path, header, all_rows)
        else:
            write_markdown(output_path, "".join(aggregated_markdown))

    except OCRScriptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved OCR output to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
