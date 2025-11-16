---
name: frontend-style-guide-generator
description: Identify existing frontend styles, UI and UX patterns from a representative page or set of pages/components, and to derive a set of standardized styles, UI & UX norms that can be used as an authoritative frontend guidance document.
---

# Frontend Style Guide Generator Skill

This skill provides a tool to identify existing frontend styles, UI and UX patterns from a representative page or set of pages/components, and to derive a set of standardized styles, UI & UX norms that can be used as an authoritative frontend guidance document.

## AI Agent Analysis Workflow

This workflow is designed for an AI agent to perform frontend style analysis using its available tools.

### Step 1: Fetch Page Content

1.  **Use `view_text_website`:**
    *   Call `view_text_website` with the target URL to get the full HTML content of the page.

### Step 2: Extract Stylesheets

1.  **Identify Stylesheet Links:**
    *   Parse the HTML to find all `<link rel="stylesheet" ...>` tags and extract their `href` attributes.
    *   Also, find all `<style>` tags and extract their content.

2.  **Fetch Stylesheet Content:**
    *   For each external stylesheet URL, use `view_text_website` to fetch its content.
    *   Combine the content of all external and inline stylesheets into a single text file (e.g., `styles.css`).

### Step 3: Analyze CSS

1.  **Identify Common Properties:**
    *   Use `grep` to find all occurrences of common CSS properties:
        *   `grep "color:" styles.css`
        *   `grep "background-color:" styles.css`
        *   `grep "font-family:" styles.css`
        *   `grep "font-size:" styles.css`
        *   `grep "margin:" styles.css`
        *   `grep "padding:" styles.css`

2.  **Count Frequencies:**
    *   For each property, use shell commands (`sort`, `uniq -c`, `sort -nr`) to count the frequencies of the different values. For example:
        ```bash
        grep "color:" styles.css | awk -F ':' '{print $2}' | sort | uniq -c | sort -nr > color_frequencies.txt
        ```

### Step 4: Synthesize and Document

1.  **Create a Markdown Document:**
    *   Start a new Markdown file (e.g., `STYLE_GUIDE.md`).

2.  **Document Findings:**
    *   **Colors:** Based on the frequency counts, list the most common colors.
    *   **Typography:** List the most common font families and sizes.
    *   **Spacing:** List the most common margin and padding values.

## Automated Script

For a quicker, automated analysis, you can use the provided Python script.

### `generate_style_guide.py`
Analyzes a web page's CSS to find common colors, fonts, and spacing, and then generates a `STYLE_GUIDE.md` document summarizing these frontend norms.

**Usage:**
```bash
python generate_style_guide.py <url>
```
The output will be a `STYLE_GUIDE.md` file in the current directory.
