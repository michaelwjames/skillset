## Easy Crypto Statement Normalization for South African Tax Year

This document provides guidance on normalizing Easy Crypto statements for the South African tax year.

### Document Types
- **Tax Certificate/Statement**: Shows crypto trading activity for tax period
- **Portfolio Summary**: Contains opening/closing balances and profit/loss calculations

### Key Data Fields to Extract
From Tax Certificates:
- **Instrument**: Cryptocurrency ticker (BTC, EC10, ECE10, etc.)
- **Opening Balance**: Quantity and cost base carried forward
- **Purchases**: Quantity acquired and cost during tax year
- **Sales**: Quantity sold and cost base of sold assets
- **Proceeds**: Amount received from sales
- **Profit/Loss**: Realized gains/losses from disposals
- **Closing Balance**: Quantity and cost base at period end
- **Trading Fees**: Total fees paid for transactions

### Processing Steps
1. **Verify tax period** aligns with South African tax year (1 Mar to 28 Feb)
2. **Extract trading data** for each cryptocurrency instrument
3. **Calculate realized gains/losses** using Proceeds - Cost of Sales
4. **Identify disposals** that trigger capital gains events
5. **Map to spreadsheet fields**:
   - Realized profits → Capital gains section
   - Trading fees → Allowable deductions
   - Closing balances → Carry-forward to next tax year

### Tax Treatment
- **BTC and other cryptocurrencies**: Capital assets subject to CGT
- **EC10/ECE10 (crypto baskets)**: Treated as single capital assets
- **Trading fees**: Deductible against capital gains
- **Held assets**: Not taxable until disposed of

### Validation Rules
- Opening balances should match previous year's closing balances
- Purchases + Opening = Sales + Closing (quantity reconciliation)
- Proceeds - Cost of Sales = Profit/Loss per instrument
- Portfolio totals should sum individual instrument values
- Trading fees should be reasonable relative to transaction volume

### Important Notes
- Only realized gains/losses are taxable - unrealized gains are not
- Cost base includes purchase price plus associated fees
- Use FIFO (First In, First Out) method for cost base calculation unless specified otherwise
- Crypto-to-crypto trades are taxable events (both disposal and acquisition)
- All amounts are typically in ZAR, verify currency denomination
