## Hargreaves Lansdown Statement Normalization for South African Tax Year

The South African tax year runs from March 1st to the last day of February of the following year. Hargreaves Lansdown (HL) statements are typically issued for the UK tax year, which runs from April 6th to April 5th of the following year.

To normalize HL statements for South African tax purposes, you need to extract all transactions that fall within the South African tax year.

### Steps:

1.  **Gather all HL statements:** Collect all your HL statements for the relevant period. This may include statements that span across two South African tax years.
2.  **Identify the SA tax year:** Determine the start and end dates of the South African tax year for which you are filing. For example, the 2024/2025 tax year runs from March 1, 2024, to February 28, 2025.
3.  **Extract relevant transactions:** Go through each HL statement and identify all transactions (dividends, interest, capital gains/losses) that occurred within the South African tax year.
4.  **Convert to ZAR:** Convert all amounts from GBP (or other foreign currencies) to ZAR using the average exchange rate for the year, or the spot rate on the day of the transaction. The South African Revenue Service (SARS) publishes official exchange rate tables that should be used for this purpose.
5.  **Populate the spreadsheets:** Use the extracted and converted data to populate the relevant spreadsheet stubs in the `spreadsheets` directory.

### Example:

Let's say you are filing for the 2024/2025 South African tax year (March 1, 2024 - February 28, 2025). You have an five quarterly HL statements that overlap with the SA tax year.

You would need to extract all transactions from those statements that fall between March 1, 2024, and February 28, 2025. Anything prior or after those dates is to be ignored.
