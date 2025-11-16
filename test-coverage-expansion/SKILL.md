---
name: test-coverage-expansion
description: Improve repository test coverage by targeting critical gaps and validating the full suite without additional user input.
---

# Test Coverage Expansion Workflow

## Objective

Identify and cover the most critical untested code paths to meaningfully raise repository test coverage while preserving existing conventions.

## Prerequisites

- Determine the project's primary testing frameworks, assertion libraries, and helper utilities.
- Review any existing coverage reports or tooling configuration (e.g., Jest, Vitest, NYC, Istanbul, Coverage.py).

## Steps

1. **Perform Coverage Analysis**
   - Enumerate all testable source directories.
   - Generate or inspect coverage metrics to locate the lowest-covered files, modules, or functions.
   - Prioritize business-critical or high-risk paths that currently lack assertions.

2. **Design Meaningful Tests**
   - For each identified gap, outline the behaviors, edge cases, and failure modes that must be verified.
   - Reuse existing test fixtures, mocks, and helpers to maintain stylistic consistency.

3. **Implement New Tests**
   - Add unit and/or integration tests matching repository standards (naming, directory structure, tooling).
   - Ensure each test exercises real logic, guarding against purely superficial coverage increases.

4. **Validate the Suite**
   - Run the entire test suite locally, capturing output for failures or regressions.
   - Confirm newly added tests pass and coverage metrics improve.

5. **Summarize Enhancements**
   - Document which files gained new tests and what behaviors are now covered.
   - Prepare a concise summary for inclusion in commit messages or change logs.

## Deliverables

- New or updated test files covering previously untested critical paths.
- Evidence of passing test suite execution and improved coverage metrics.
- Written summary of coverage improvements, affected files, and validated behaviors.
- No additional user clarification requests prior to completion.
