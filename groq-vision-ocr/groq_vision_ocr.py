"""CLI tool for running Groq Llama 4 Scout OCR over one or more images.

Features:
- Accepts local image paths or remote image URLs.
- Sends a user-provided prompt alongside the images.
- Converts model output into CSV when extracting table data, or Markdown when producing text.
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
from pathlib import Path
from typing import Iterable, List, Sequence

from groq import Groq

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
        raise OCRScriptError(
            f"Could not determine MIME type for {path.name}. "
            "Add an appropriate file extension."
        )

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

    # Start timing the API request
    start_time = time.time()

    messages: List[dict] = []
    if mode == "table":
        messages.append({"role": "system", "content": TABLE_SYSTEM_PROMPT})
    else:
        messages.append({"role": "system", "content": TEXT_SYSTEM_PROMPT})

    messages.append(
        {
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                *image_contents,
            ],
        }
    )

    kwargs: dict = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "max_completion_tokens": 2048,
    }

    if mode == "table":
        kwargs["response_format"] = {"type": "json_object"}

    completion = client.chat.completions.create(**kwargs)
    # End timing
    elapsed = time.time() - start_time

    # Extract usage stats if available (compatible with OpenAI-like response)
    usage_info = getattr(completion, "usage", None)
    if usage_info:
        total_tokens = getattr(usage_info, "total_tokens", "N/A")
        prompt_tokens = getattr(usage_info, "prompt_tokens", "N/A")
        completion_tokens = getattr(usage_info, "completion_tokens", "N/A")
    else:
        total_tokens = prompt_tokens = completion_tokens = "N/A"

    # Log stats to stderr (so they don't interfere with stdout CSV/MD output)
    print(
        f"[INFO] Groq API call completed in {elapsed:.2f}s | "
        f"total_tokens={total_tokens} prompt_tokens={prompt_tokens} completion_tokens={completion_tokens}",
        file=sys.stderr,
    )

    choice = completion.choices[0].message
    content = choice.content
    if content is None:
        raise OCRScriptError("Empty response received from the Groq API.")
    return content


def write_csv(output_path: Path, payload: str) -> None:
    try:
        data = json.loads(payload)
    except json.JSONDecodeError as exc:
        raise OCRScriptError(
            "Expected JSON output for table mode but failed to parse response."
        ) from exc

    if isinstance(data, dict) and "columns" in data and "rows" in data:
        columns = data["columns"]
        rows = data["rows"]
    elif isinstance(data, list):
        # Assume list of row dicts.
        columns = sorted({key for row in data for key in row.keys()})
        rows = [[row.get(col, "") for col in columns] for row in data]
    else:
        raise OCRScriptError(
            "Unexpected JSON structure. Provide 'columns' and 'rows', or a list of objects."
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(columns)
        for row in rows:
            writer.writerow(row)


def write_markdown(output_path: Path, payload: str) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(payload, encoding="utf-8")


def parse_args(argv: Iterable[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Groq Llama 4 Scout OCR helper")
    parser.add_argument(
        "--images",
        nargs="+",
        required=True,
        help="Image paths or URLs to process."
    )
    parser.add_argument(
        "--prompt",
        required=True,
        help="Instruction for the model (e.g., describe extraction goals)."
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
    args = parse_args(argv or sys.argv[1:])

    try:
        mode = infer_mode(args.prompt, args.mode)
        contents = build_image_contents(args.images)
        response = call_groq(
            prompt=args.prompt,
            image_contents=contents,
            mode=mode,
            model=args.model,
            temperature=args.temperature,
        )

        # Generate output file in same directory as first input image
        first_image = Path(args.images[0])
        if first_image.exists():
            output_dir = first_image.parent
            base_name = first_image.stem
        else:
            # For URLs, use current directory
            output_dir = Path.cwd()
            base_name = "ocr_result"
        
        default_name = f"{base_name}.csv" if mode == "table" else f"{base_name}.md"
        output_file = Path(args.output) if args.output else Path(default_name)
        output_path = output_dir / output_file

        if mode == "table":
            write_csv(output_path, response)
        else:
            write_markdown(output_path, response)

    except OCRScriptError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    except Exception as exc:  # noqa: BLE001
        print(f"Unexpected error: {exc}", file=sys.stderr)
        return 1

    print(f"Saved OCR output to {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
