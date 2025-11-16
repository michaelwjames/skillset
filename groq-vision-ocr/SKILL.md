---
name: groq-vision-ocr
description: Extract printed or handwritten text from images using Groq's Llama 4 Scout vision model.
metadata:
  provider: groq
  model: meta-llama/llama-4-scout-17b-16e-instruct
---

# Overview
Use this skill when you need fast Optical Character Recognition (OCR) on images (screenshots, scans, documents) by running the bundled `groq_vision_ocr.py` CLI. The script wraps Groq's multimodal `chat.completions` API with the **Llama 4 Scout** vision model and handles remote URLs, local files, output formatting, and error reporting. Needs a .env with the groq api key - assume this is already in place.

# Usage requirements

The AI agent **must** interact with this skill by executing the bundled CLI. Do **not** craft custom HTTP requests or alternate scripts.

1. Prepare one or more image paths or URLs.
2. Run the script:

   ```bash
   python groq_vision_ocr.py \
     --images <image_or_url> [additional_images_or_urls] \
     --prompt "<instructions for the OCR task>" \
     [--mode table|text] \
     [--output <desired_output_path>] \
     [--model <groq_model>] \
     [--temperature <float>]
```

E.g. `python d:\MySites\skillset\groq-vision-ocr\groq_vision_ocr.py --images d:\MySites\skillset\Screenshot.png --prompt "Extract the table data as CSV" --mode table`

4. Wait for the script to finish and read the saved output path echoed in the terminal.

## Argument notes

- `--images` accepts a mix of local filesystem paths and remote `http(s)` URLs. Local files are automatically encoded to base64; no manual preprocessing is required.
- `--prompt` should describe the desired extraction format (e.g., "List bullet points" or "Return JSON columns and rows").
- `--mode` defaults to `table` when the prompt references tables/CSV, otherwise `text`. Override if the inference is incorrect.
- When `--mode table` is active, the script converts JSON responses into CSV (defaults to `ocr_result.csv`). `--mode text` produces Markdown (defaults to `ocr_result.md`). Override the destination with `--output`.
- `--model` defaults to `meta-llama/llama-4-scout-17b-16e-instruct`; supply another Groq vision model if needed.
- `--temperature` defaults to 0.1 and should remain low for deterministic OCR.

## Output handling

- CSV files contain header rows followed by table rows inferred from the model output.
- Markdown files retain the model response formatting; downstream consumers can parse or render as needed.
- Always verify the output for accuracy and re-run with refined prompts when necessary.

# Prompting tips
- Set `temperature` near `0` for deterministic OCR output.
- Include instructions on desired formatting (e.g., plain text, JSON fields like `{ "ocr_text": ... }`).
- For multi-page scans, send each page in separate user turns or compress them into a single prompt while clarifying ordering.

# Error handling & limits
- The Groq API enforces request and token limits—check the [rate limits dashboard](https://console.groq.com/limits).
- Handle `401` responses by confirming the API key is present and active.
- Large images may require resizing/compression client-side to stay within payload size limits.

# References
- [Groq Vision documentation](https://console.groq.com/docs/vision)
- [chat.completions API reference](https://console.groq.com/docs/text-chat)
