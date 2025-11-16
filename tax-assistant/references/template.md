## <INSTITUTION> Reference Documentation

This template provides a skeleton for documenting, in a generic way, how to interpret and understand the structure of <INSTITUTION>'s documents. It is **not** for doing calculations; it is only for describing shapes, fields, and where key information lives so that a future agent can process these documents quickly without needing to think deeply.

---

## Document Types
- List the main document types (e.g. IT3b tax certificates, account statements, contribution certificates).
- Briefly describe what each document is used for in the tax workflow.

## Key Data Fields to Identify
From the primary documents (statements, certificates, etc.), **only identify and describe** where the following appear; do not perform any calculations in this step:
- Tax period or reporting period (describe how it is presented and where)
- Account identifiers and account types (e.g. savings, current, investment, RA)
- Income-related fields (interest, dividends, other income) and where they appear in tables/sections
- Capital gains/losses or similar movement information and which columns/sections hold them
- Any summary totals and the tables/sections they summarize

## Processing Steps (Descriptive Only)
1. Identify and name the relevant tables/sections that contain tax-relevant or reporting-relevant data (e.g. "Account Information", "Interest Summary", "Capital Gains Schedule").
2. For each key table/section, describe its columns/fields and what each represents.
3. Describe where period dates, account identifiers, and taxpayer identifiers are located, and how they are formatted.
4. Describe, at a high level, which fields would typically map to downstream tax or reporting fields (e.g. "this column corresponds to local interest income"), **without** actually performing any calculations or reconciliations.
5. Note any institution-specific quirks (e.g. accrual vs paid, FX conversion conventions, combined vs split totals, unusual naming), again in descriptive terms only.

## Validation / Consistency Notes (for future processing)
- Describe how detailed rows relate to statement summary totals (e.g. "this summary row is the sum of the preceding detail rows"). Do not perform the summation here; just document the relationship.
- Note how the reporting period is indicated and any common deviations (e.g. calendar year vs tax year) that future processing must normalize.
- Note where account holder/taxpayer details appear and how they should match the taxpayer.
- Document how FX conversions or currency indicators are presented (e.g. per-line currency codes, separate FX notes), without performing FX calculations.

