# Instructions for Humans Needing Tax Assistance

## Prerequisites

- Groq API key (https://console.groq.com/keys - sign up for a free account, generate an API key)
- An `.env` file in the `pdf-vision-ocr` directory with your Groq API key
- Python 3.12
- An asynchronous agent connected with your Github account. [Jules](https://jules.google) is free and works well.

## Populate PDF/CSV data

- Add your tax relevant data to the `data` directory. Push this to your GitHub repository (keep it private).

## Give the agent instructions
- Ask the agent to process the data as per the workflow in `SKILL.md`.
- If it asks for your intervention at any point, tell it to continue as per the workflow.

## Review the results
- Review the results in the `spreadsheets` directory.
- Check the `review.md` file for any issues or insights that may have arisen while processing the documents and completing the tax spreadsheets. Add the agent to improve the skill where required.
- Repeat the process as required to increase accuracy and completeness of the outputted spreadsheets.