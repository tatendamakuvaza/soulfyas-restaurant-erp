# Chapter 40: Measures and DAX — the Ten Formulas

*Part VI — Dashboards and Storytelling with Power BI*

> "A measure is a formula with a name and a home. DAX is the dialect it speaks — and you already speak three of its parent languages."

### In this chapter you will learn

- Measures vs calculated columns — the distinction that separates DAX users from DAX sufferers.
- The evaluation context: the one idea that makes DAX make sense.
- The ten formulas that cover 90% of real dashboards, each on Tariro's data.
- Time intelligence: month-over-month, running totals, period comparisons.
- The filter-propagation insight: why a measure is right in *every* slice.

## 40.1 Measures, Not Columns

Your first DAX decision is architectural, and beginners get it wrong by reflex. A **calculated column** computes row by row at refresh time (`amount * 1.15` for every row — a new column stored in the table): use it for *attributes* (weekday flag, price band). A **measure** computes at *query* time, over whatever rows the current context selects (`SUM of amount` — a formula with a name, evaluated live for every visual, filter, and slicer). The rule the professionals follow: **if the number answers "how much/how many", it is a measure; if it labels a row, it is a column.** Revenue, count, share, growth: measures. Weekend flag, suburb, tier: columns.

Create a measure: right-click the `sales` table in the Fields pane → New measure:

```dax
Revenue = SUM(sales[amount])
```

Then drag it into a card visual: the bridge number again (54,013.50 — reconciled at the moment of its birth, as Chapter 39 required). Rename tables' display names, keep measures in a dedicated "Measures" home table if you like (a professional habit for navigation), and format each measure once (Format → Currency/Percentage) — formatting is part of the measure's definition, not a per-visual chore.

## 40.2 The One Idea: Evaluation Context

DAX is confusing for exactly one reason, and understanding it dissolves 80% of the confusion: **every measure evaluates inside a context** — the set of rows currently visible — and the *same measure* computes a different (correct) number in each context. `Revenue` in a card with no filters: 54,013.50. The same `[Revenue]` in a table visual by payment_type: three numbers, each the sum over that type's rows. The same `[Revenue]` under the EcoCash slicer: only EcoCash rows. This is **filter context**, and it propagates through the model's relationships: click Avondale in a suburb slicer, and the filter flows customers → sales, and `[Revenue]` recomputes — *the reader's click becomes a WHERE clause executed against your star schema*. Nothing in DAX makes sense except in light of filter context — and everything in DAX becomes manageable once you hold it: you never write "revenue for March" — you write `[Revenue]` and let March be the context. (Row context, its sibling, is calculated-column territory; you will feel it when you meet it.)

## 40.3 The Ten

The working set — genuinely, on real dashboards, these ten (and their obvious mutations) cover almost everything. Type each on Tariro's model, and meet old friends:

```dax
-- 1. Total revenue
Revenue = SUM(sales[amount])

-- 2. Count (of rows = of sales)
Sales Count = COUNTROWS(sales)

-- 3. Average basket
Average Basket = DIVIDE([Revenue], [Sales Count])

-- 4. Share of total (% of grand total -- the Ch. 18 share pattern, live)
Revenue Share =
DIVIDE([Revenue], CALCULATE([Revenue], ALL(sales)))

-- 5. Distinct customers (the loyalty denominator)
Distinct Customers = DISTINCTCOUNT(sales[customer_id])

-- 6. Members' revenue share (filter context, steered by hand)
Member Revenue =
CALCULATE([Revenue], sales[customer_id] <> BLANK())

-- 7. Month-over-month (needs the marked date table)
Revenue MoM % =
VAR CurrentMonth = [Revenue]
VAR PrevMonth =
    CALCULATE([Revenue], DATEADD('Calendar'[Date], -1, MONTH))
RETURN DIVIDE(CurrentMonth - PrevMonth, PrevMonth)

-- 8. Running total (the cumulative year, Ch. 19 again)
Revenue YTD = TOTALYTD([Revenue], 'Calendar'[Date])

-- 9. Same period last year (the comparison every manager asks for)
Revenue LY =
CALCULATE([Revenue], SAMEPERIODLASTYEAR('Calendar'[Date]))

-- 10. The Sunday verdict, as a measure
Sunday Avg Basket =
CALCULATE([Average Basket], 'Calendar'[Weekday] = "Sunday")
```

Four vocabulary notes, and they are the grammar's core: **DIVIDE** is the division that survives zeros (returns BLANK instead of an error — the IFERROR of dignity). **ALL(table)** removes the filters — "the whole thing, regardless of context" — which is how shares get their denominators (measure 4 is literally Chapter 18's CTE pair). **CALCULATE** is DAX's crown jewel: *evaluate this measure in a context I modify* — a WHERE clause you write by hand, composed with the reader's clicks. And **VAR ... RETURN** names intermediate steps — the CTE habit, DAX's accent; name your thinking.

## 40.4 Time Intelligence, Properly

Measures 7–9 are **time intelligence** — DAX's biggest practical gift, all of it dependent on the marked date table from Chapter 39. The patterns to recognise on sight (and reuse endlessly): **DATEADD** (shift the period: −1 month, −1 year — month-over-month, year-over-year); **TOTALYTD/MTD** (cumulative within a boundary — the running total, the bank-manager line); **SAMEPERIODLASTYEAR** (the comparison that makes trends meaningful: this month against its own past, not against last month's season). Note the deep honesty these enable: "revenue is down" becomes "revenue is down 4% against the same month last year but up 11% year-to-date" — context, not vibes, the Chapter 2 habit compiled into formulas.

One classic trap, named so you never fall in: time intelligence compares *dates*, and a partial current month (data to the 14th) will "collapse" against full comparison months. The professional's fix is a measure like `Is Current Month Complete` or reporting MTD with a data-age stamp (Chapter 41 implements the stamp) — the stale-dashboard lie, prevented at the measure layer.

## 40.5 Right in Every Slice

The chapter's closing claim, and thePart's heart: a measure built on a correct model is right in *every* context — every filter, every slicer, every combination — because it computes from the rows the context selects, not from a number you froze. That is the qualitative jump from the spreadsheet world: the pivot you re-dragged monthly (Part II), the query you re-ran monthly (Part III), the report that rebuilt itself monthly (Part V) — all of them are now **one measure, evaluated live, for a reader you will never watch**. The craft obligation follows: you must *test* the slices (does `[Revenue MoM %]` behave in the January boundary? does the member share survive the suburb slicer?) — the quality gate of Chapter 13, applied to contexts instead of pages.

> **From Your Toolkit — the measure mindset:** a DAX measure is a named formula evaluated in context — the same object as a SQL aggregate over a GROUP BY you cannot see, a pandas `.agg()` whose groupby the reader chooses, an Excel named formula with a filter attached. CALCULATE is WHERE; ALL is "remove the WHERE"; VAR/RETURN is the CTE. You have been training for DAX since Chapter 9 — the accent is new; the sentences are yours.

## Key Takeaways

- Columns label rows (refresh-time); measures answer "how much" (query-time, in context) — choose by the question, not by reflex.
- Filter context is the one idea: the same measure is a different, correct number in every visual/slicer combination; clicks are WHERE clauses.
- The ten: SUM, COUNTROWS, DIVIDE average, ALL-share, DISTINCTCOUNT, CALCULATE-filters, DATEADD MoM, TOTALYTD, SAMEPERIODLASTYEAR, steered verdicts.
- DIVIDE survives zero; CALCULATE steers context; VAR/RETURN names your thinking — CTE habits, DAX accent.
- Test the slices (boundaries, slicer combos); stamp the data age — a measure is a promise to readers you will never watch.

## Practice Lab

1. Build all ten measures on your model, each formatted once at creation; drag each into a card or table and reconcile the unfiltered numbers against your Part II/III bridges (Revenue, count, average basket, distinct customers — four cent-for-cent matches logged).
2. The context experiment: one table visual (payment type × `[Revenue]` and `[Revenue Share]`), then add suburb and month slicers; click ten combinations and verify two of them by hand against SQL or pandas — the "right in every slice" promise, personally audited.
3. The boundary test: place `[Revenue MoM %]` in a month table and check the January row (does it reach for last *December*? does your date table span that far?); fix the calendar if needed and note the fix — this is the trap, sprung and defused.
4. The steer drill: write three custom measures with CALCULATE — weekend revenue, whale-only revenue (amount > 21.50), till-2 revenue; display beside `[Revenue]`; verify one against a pandas equivalent.
5. The tenth, extended: a small "verdict table" — Sunday vs weekday average basket and revenue, using measures 10 and a weekday variant; caption it with Part IV's formal finding (t = −18.5, p < 0.001) — the dashboard now *displays the test's verdict*, the analysis-to-dashboard bridge this Part keeps building.

## Further Reading

- Chapter 41 (the dashboard itself — the measures get their page)
- *The Definitive Guide to DAX* (Russo & Ferrari) — when you outgrow the ten, this is the mountain
