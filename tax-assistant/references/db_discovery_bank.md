## Discovery Bank Statement Normalization for South African Tax Year

This document provides guidance on normalizing Discovery Bank statements for the South African tax year.

### Document Types
- **IT3b Tax Certificate**: Primary source for interest income reporting
- **Account Statements**: May provide additional transaction details

### Key Data Fields to Extract
From IT3b Tax Certificates:
- **Tax period** (typically 1 Mar - 28 Feb for SA tax year)
- **Account numbers** and **account types** (Savings, Notice, Current)
- **Total interest earned** per account
- **Tax source code** (typically 4201 for interest income)

### Processing Steps
1. **Verify tax period** aligns with South African tax year (1 Mar to 28 Feb)
2. **Extract account information** from the Account Information table
3. **Sum interest amounts** across all accounts to match the Total interest earned summary
4. **Map to spreadsheet fields**:
   - Interest income → Local interest income section
   - Account numbers → Reference/audit trail
   - Tax source code 4201 → Standard interest classification

### Account Type Handling
- **Savings Accounts**: Standard interest income
- **Notice Accounts**: Interest income (may have different rates)
- **Current Accounts**: Typically minimal interest, still reportable
- **Fixed Deposit Accounts**: Interest reported when earned, not when paid (per notes)

### Validation Rules
- Total of individual account interests must equal the summary total
- Tax period should match the SA tax year boundaries
- Tax source code should be 4201 for interest income
- Verify accountholder details match taxpayer information

### Notes
- Discovery Bank includes accrued interest on Fixed Deposits in the tax year earned
- All amounts are already in ZAR, no currency conversion required
- Account numbers should be retained for audit purposes
