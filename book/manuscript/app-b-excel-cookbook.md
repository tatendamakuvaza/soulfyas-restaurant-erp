# Appendix B: Excel Cookbook

*Appendices — The Cookbook*

> "Twenty-five formulas and tricks — the spreadsheet craft of Part II, compressed to a reference. Formulas shown for Excel; LibreOffice Calc and Google Sheets agree on nearly everything (notes where they don't)."

Conventions: `sales` refers to a clean table with headers in row 1: `A` date, `B` item, `C` category, `D` payment_type, `E` amount, `F` customer_id; `customers` is a second sheet. Row 2 is the first data row. Structured-table references (`Table1[amount]`) are the professional habit where available; plain ranges shown for universality.

## The Essentials

**1. The anchoring dollar — copy-safe ranges**

```text
=SUM($E$2:$E$6421)     -- $ = lock: column, row, or both (F4 cycles)
                       -- ranges without $ drift when copied
```

**2. SUMIF / COUNTIF — one-condition aggregation**

```text
=SUMIF(D:D, "EcoCash", E:E)      -- revenue for EcoCash
=COUNTIF(C:C, "Staples")         -- how many staple sales
=AVERAGEIF(D:D, "Cash", E:E)     -- average cash basket
```

**3. SUMIFS / COUNTIFS — multiple conditions**

```text
=SUMIFS(E:E, D:D, "EcoCash", A:A, ">=2025-06-01", A:A, "<2025-07-01")
-- criteria in (range, criterion) PAIRS; dates as ISO strings
```

**4. SUMPRODUCT — the anything-condition (incl. weighted means)**

```text
=SUMPRODUCT((D2:D6421="EcoCash") * E2:E6421)          -- SUMIFS without the limits
=SUMPRODUCT(prices, bottles) / SUM(bottles)           -- the weighted mean (Ch. 22)
```

## Looking Up and Joining

**5. XLOOKUP — the modern join**

```text
=XLOOKUP(F2, customers!A:A, customers!C:C, "no match")
-- find F2, return the suburb, fail politely
```

**6. VLOOKUP with error handling (the inherited-code version)**

```text
=IFNA(VLOOKUP(F2, customers!$A:$E, 3, FALSE), "no match")
-- always FALSE (exact); always IFNA; count the "no match"es
```

**7. INDEX-MATCH — the column-insertion-proof join**

```text
=INDEX(customers!C:C, MATCH(F2, customers!A:A, 0))
-- MATCH finds the row; INDEX returns the value; survives inserted columns
```

**8. The dup check**

```text
=IF(COUNTIF(F:F, F2) > 1, "DUP", "")     -- fill down; filter for DUP
```

**9. The TRIM/CLEAN stack — ghost blanks and hidden characters**

```text
=TRIM(CLEAN(UPPER(D2)))                  -- whitespace, non-printables, case
-- run on a helper column, then paste-as-VALUES over the original, delete helper
```

## Dates and Text

**10. Date hygiene**

```text
=DATEVALUE("2025-06-14")               -- text date -> real date
=TEXT(A2, "yyyy-mm")                   -- real date -> month key "2025-06"
=TEXT(A2, "ddd")                       -- "Sat" (weekday name, Ch. 10)
=EOMONTH(A2, 0)                        -- month end; -1 = previous month end
=DATEDIF(B2, A2, "d")                  -- days between (quietly useful)
```

**11. Text splitting**

```text
=LEFT(B2, FIND(" ", B2) - 1)           -- first word
=TEXTSPLIT(B2, " ")                    -- modern: splits to adjacent cells
=TEXTJOIN(", ", TRUE, C2, D2)          -- joins, skipping blanks
```

**12. The id-building concat**

```text
=TEXT(A2, "yyyymmdd") & "-" & TEXT(ROW()-1, "0000")
-- deterministic row id from date + row number (dedupe/reconciliation key)
```

## Statistics (Part II's set)

**13. The typicals**

```text
=AVERAGE(E2:E6421)    =MEDIAN(E2:E6421)    =MODE.SNGL(E2:E6421)
=TRIMMEAN(E2:E6421, 0.05)                 -- mean dropping top/bottom 5% (robust-ish)
```

**14. The five-number summary**

```text
=MIN(E2:E6421)   =QUARTILE.INC(E2:E6421,1)   =MEDIAN(E2:E6421)
=QUARTILE.INC(E2:E6421,3)   =MAX(E2:E6421)
```

**15. Spread**

```text
=STDEV.S(E2:E6421)     -- sample (n-1): your default
=STDEV.P(E2:E6421)     -- population (n): only for complete censuses
=QUARTILE.INC(E2:E6421,3) - QUARTILE.INC(E2:E6421,1)   -- IQR
```

**16. The 1.5×IQR fence**

```text
=QUARTILE.INC(E2:E6421,3) + 1.5 * (QUARTILE.INC(E2:E6421,3) - QUARTILE.INC(E2:E6421,1))
-- flag: =IF(E2 > that_cell, "whale", "")
```

**17. Z-score per row**

```text
=(E2 - AVERAGE($E$2:$E$6421)) / STDEV.S($E$2:$E$6421)    -- anchored, fill down
```

**18. Rank and percentile rank**

```text
=RANK.EQ(E2, $E$2:$E$6421)                   -- 1 = largest
=PERCENTRANK.INC($E$2:$E$6421, E2)           -- 0.91 = 91st percentile
```

**19. Correlation and the line**

```text
=CORREL(x_range, y_range)                    -- r
=INTERCEPT(y_range, x_range)  =SLOPE(y_range, x_range)
=FORECAST.LINEAR(new_x, y_range, x_range)    -- predict on the line
=RSQ(y_range, x_range)                       -- R-squared
```

**20. The tests (Part IV in cells)**

```text
=T.TEST(range1, range2, 2, 3)        -- two-tailed, unequal variance (Welch)
=T.TEST(range1, range2, 2, 1)        -- paired
=CHISQ.TEST(observed_range, expected_range)
=CONFIDENCE.T(0.05, STDEV.S(range), COUNT(range))  -- the +/- of a 95% CI
```

## Craft and Guardrails

**21. The error handlers**

```text
=IFNA(VLOOKUP(...), "no match")            -- lookup misses
=IFERROR(1/0_cell, 0)                      -- last resort; IFNA first (hides less)
```

**22. Rounding — display vs truth**

```text
=ROUND(E2 * 1.15, 2)                       -- round the RESULT once, for money
=TEXT(E2, "#,##0.00")                      -- format for display; never destroys value
```

**23. Conditional formatting as a check** — Home → Conditional Formatting →
"Duplicate values" on the key column; "Greater than" the fence cell on amounts; a red-fill rule on `=ISBLANK(A2)`. *Three rules, the whole loading liturgy, visible.*

**24. Data validation — the guard at the door** — Data → Data Validation → List (payment types from a named range); whole-number bounds on amounts. *Prevents the flaw at entry, which beats cleaning it at load (Ch. 8's deepest lesson, as a feature).*

**25. The audit trio (trace your inheritance)** — Formulas ribbon: **Trace Precedents** (what feeds this cell), **Trace Dependents** (what breaks if I change it), **Evaluate Formula** (watch the calculation step by step — the EXPLAIN of spreadsheets). Plus `Ctrl + ]` (jump to precedents) and the whole-book habit: **Ctrl + T** (make it a Table — structured references, auto-extension, one-click totals).

## Calc / Sheets Notes

- Calc and Sheets support everything above; XLOOKUP exists in recent versions (Calc 24.8+, Sheets yes); TEXTSPLIT is Excel/Sheets-only (Calc: `SPLIT()` in newer builds or Text→Columns).
- Sheets' `QUERY()` function (a mini-SQL on ranges) is a legitimate bridge to Part III: `=QUERY(A:F, "select D, sum(E) where E > 0 group by D", 1)`.
- The ToolPak equivalents live in Calc under Data → Statistics; Sheets needs the formulas themselves.

*The cookbook's one law: every formula is a step in a story someone else must read — anchor the ranges, label the helpers, and reconcile the total before you believe the sheet.*
