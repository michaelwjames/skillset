# Skills Catalog

| Skill | Primary Use Case | Key Dependencies |
| --- | --- | --- |
| `architecture-analyzer/` | Conduct deep architectural analysis of codebases, documenting technology stack, design patterns, database schemas, and key architectural decisions. It can also perform static analysis to suggest improvements. | Python 3.10+, `radon>=5.1.0`. |
| `pdf-decryptor/` | Remove password protection from encrypted PDF files by providing the password and generating unlocked copies. | Python 3.7+, `pikepdf>=8.0.0`. |
| `skill-creator/` | Design and package new skills with reusable resources, workflows, and metadata. | Documentation and helper guidance only; no bundled runtime dependencies. |
| `test-coverage-expansion/` | Raise test coverage by targeting critical gaps, adding robust tests, and validating the full suite autonomously. | Test tooling already configured in the repository; no additional dependencies bundled. |
| `pdf-operations/` | Merge, split, compress, watermark, and extract data from PDFs. | Python 3.10+, `pypdf`, `pdfminer.six`, `reportlab`, `Pillow`. |
| `groq-vision-ocr/` | Run the bundled Groq Llama 4 Scout CLI to extract text or tables from local/remote images with deterministic OCR prompts. | Python 3.10+, `groq` package, `.env` containing `GROQ_API_KEY`. |
| `pdf-vision-ocr/` | Convert PDFs to page images and send them through Groq Llama 4 Scout OCR to capture tables or text. | Python 3.10+, `groq`, `pdf2image` (requires poppler), `.env` with `GROQ_API_KEY`. |
