---
name: pdf-vision-ocr
description: Extract printed or handwritten text from PDF documents using Groq's Llama 4 Scout vision model.
metadata:
  provider: groq
  model: meta-llama/llama-4-scout-17b-16e-instruct
---

# Overview
Use this skill when you need fast Optical Character Recognition (OCR) on PDF documents. The bundled `pdf_vision_ocr.py` CLI first converts each page of the input PDF into a PNG image. It then iterates through these images, sending them to Groq's multimodal `chat.completions` API with the **Llama 4 Scout** vision model. The script handles output formatting and error reporting. Needs a .env with the groq api key - assume this is already in place.

# Usage requirements

The AI agent **must** interact with this skill by executing the bundled CLI. Do **not** craft custom HTTP requests or alternate scripts.

1. Prepare a PDF file path.
2. Run the script:

   ```bash
   python pdf_vision_ocr.py \
     --pdf <pdf_file_path> \
     --prompt "<instructions for the OCR task>" \
     [--mode table|text] \
     [--output <desired_output_path>] \
     [--model <groq_model>] \
     [--temperature <float>]
```

E.g. `python d:\MySites\skillset\pdf-vision-ocr\pdf_vision_ocr.py --pdf "d:\MySites\skillset\mydocument.pdf" --prompt "Extract the table data as CSV" --mode table`

4. Wait for the script to finish and read the saved output path echoed in the terminal.

## Argument notes

- `--pdf` accepts a local filesystem path to a PDF file.
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
- For multi-page documents, the script processes each page sequentially and aggregates the results.

# Error handling & limits
- The Groq API enforces request and token limits—check the [rate limits dashboard](https://console.groq.com/limits).
- Handle `401` responses by confirming the API key is present and active.
- Large images may require resizing/compression client-side to stay within payload size limits.

# References
- [Groq Vision documentation](https://console.groq.com/docs/vision)
- [chat.completions API reference](https://console.groq.com/docs/text-chat)
