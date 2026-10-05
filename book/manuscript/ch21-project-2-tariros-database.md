# Chapter 21: Project 2 — Tariro's Database

*Part III — SQL: The Language of Data*

> "The spreadsheet answered questions. The database answers them again — reproducibly, on next month's data, in one click — and then answers questions the spreadsheet never could."

### In this chapter you will learn

- How to build Tariro's full database: schema, import, keys, and the loading checks.
- How to answer ten real business questions in SQL, each a pattern you now own.
- How to package queries as a reusable monthly pack — the analyst's real deliverable.
- How this project becomes portfolio evidence (the second of six).
- A self-assessment: what SQL you actually command, honestly measured.

## 21.1 Build the Database

You already have `sales` and `customers` from Chapter 14. Now the full shop, and the design moment that makes it real. In DB Browser → Execute SQL:

```sql
CREATE TABLE stock (
    week        TEXT,      -- ISO date of the Sunday counted
    item        TEXT,
    qty_on_hand INTEGER
);

CREATE TABLE suppliers (
    item              TEXT,
    supplier          TEXT,
    unit_cost         REAL,
    last_price_change TEXT
);

CREATE TABLE customers (
    customer_id  TEXT PRIMARY KEY,
    name         TEXT,
    suburb       TEXT,
    joined       TEXT,
    loyalty_tier TEXT
);

CREATE TABLE sales (
    sale_id       INTEGER PRIMARY KEY,
    date          TEXT,
    till          INTEGER,
    customer_id   TEXT,
    payment_type  TEXT,
    amount        REAL
);
```

Then **File → Import** the four CSVs into their tables (Appendix E has the generated files). Now the loading checks — the reconciliation liturgy, performed at every load, forever:

1. **Row counts**: four counts (one per table) written into your log, compared against the CSV line counts. No surprises, or explained surprises.
2. **The key census**: `SELECT customer_id, COUNT(*) FROM customers GROUP BY customer_id HAVING COUNT(*) > 1` — duplicates in a primary-key column must be zero (the engine enforces it; let it refuse, and fix the CSV — never weaken the key).
3. **The orphan check**: the Chapter 17 anti-join, sales→customers; document every orphan (the planted broken keys) as *known* — an undocumented orphan is an unexploded finding.
4. **The totals**: total sales revenue in SQL vs the workbook's cleaned total from Part II. To the cent. This number is the bridge between eras of your own work; crossing it safely is the habit that makes you trustworthy with bigger data.
5. **The NULL census**: NULL counts per critical column (customer_id, amount), each with its business meaning written beside it.

## 21.2 Ten Questions

Tariro brings the list to the new laptop — ten questions, the month's agenda, each answerable from the database you just built. Answer each as a saved query (the naming and header discipline of Chapter 20), and keep the reconciliation habit running quietly underneath: any total you produce, you check once against a second route to it.

**Q1 — How did this month compare with last?** Monthly revenue with LAG: month-over-month change and pct_change (Ch. 19). *Deliverable: a three-column table and one sentence.*

**Q2 — Which items earn the most, and does it change by till?** Top 10 items overall; then top 5 per till (top-N-per-group). *Finding: the second till skews staples — basket composition differs by position in the shop.*

**Q3 — Do suburbs differ in what they buy?** Join sales→customers, GROUP BY suburb and category, and read the cross-tab (Ch. 16–17). *Finding: one suburb's cooking-oil share is double the others' — a segment, not noise.*

**Q4 — What did the price rise actually do?** Cooking oil: monthly quantity and revenue before vs after the month-9 price change, from suppliers' `last_price_change` and the sales history — the quantity-led collapse you first saw in a pivot, now stated with the before/after numbers side by side (Ch. 18's CTE pattern).

**Q5 — Who are the top loyalty members, and are they drifting?** Top 20 members by lifetime revenue; then their monthly revenue over the last six months with LAG — the loyal-core churn signal planted in the design (Ch. 19).

**Q6 — Which items never sell on Sundays?** Items with zero Sunday sales but healthy weekday sales: two grouped CTEs, the anti-join of item lists (Ch. 17–18). *Operational answer: what not to stock for the Sunday run.*

**Q7 — What share of revenue does each payment type take, per month?** The share-of-total CTE, grouped by month and payment type (Ch. 18) — *finding: EcoCash share is rising, month over month, a slow structural shift the monthly chart in Part VI will show live.*

**Q8 — Where are the data problems this month?** The audit pack as one script: duplicate-key census, orphans, NULL census, amounts outside the IQR fences (constants from your Part II log), sales on impossible dates (before opening day, after today). *This query is not a chore — it is Q8 of the meeting agenda, and the one that makes the other nine trustworthy.*

**Q9 — What is the gross margin picture by category?** Join sales items to suppliers' unit_cost; revenue minus estimated cost per category — the first finance-flavoured query, with its caveat stated (unit costs are current, not historical; margin before overheads; a *shape*, not accounts).

**Q10 — If we lose the bottom 20% of items, what do we lose?** Rank items by revenue (Ch. 19), compute the bottom quintile's share with the share-of-total pattern — the "rationalise the range" decision every retailer eventually faces, answered in one CTE pipeline with the trade-off stated plainly.

Ten questions; every one a saved, commented, reconciled query; and the patterns are exactly the five working shapes of Chapter 20 — extraction, grouping, joining, layering, auditing — wearing business clothes. That is the whole secret of "strong SQL" on a CV.

## 21.3 The Monthly Pack

The professional deliverable is not ten answers — it is a **reusable pack** that regenerates them:

```text
queries/
  00_loading_checks.sql     -- row counts, key census, orphans, totals, NULLs
  01_month_over_month.sql
  02_top_items.sql
  ... (one per question)
  99_audit_pack.sql         -- Q8, run first and last
README.md                   -- how to run, expected totals, data dictionary
```

Next month, when the CSVs arrive, the ritual is: import → run `00_loading_checks` → reconcile → run the pack → paste results into the report template from Chapter 13. Twenty minutes, was an afternoon. **This is the pitch of the whole database era: analysis becomes a pipeline, and the analyst's craft moves from dragging to questioning.** (Chapter 37 will automate the import step too, and Part VI will refresh it live.)

## 21.4 Portfolio Evidence

Second entry in the case-study ledger (the first was Chapter 13's report; Chapter 45 assembles the portfolio):

- **The artefacts**: `tariros.db`, the `queries/` pack with headers and comments, the ten answers as a results document (PDF or markdown), the loading-check log.
- **The 150-word note**, written now while fresh: *the situation* (growing shop, four data sources), *the work* (designed a four-table schema, loaded and reconciled 18 months of data, built a ten-query monthly pack), *one number* ("answerable in twenty minutes what took an afternoon"), *the honest limits* (single-file SQLite; margins approximated; orphans documented, not deleted).
- **The interview line it funds** (Chapter 52's STAR method in embryo): "Tell me about a time you improved a reporting process" — you will tell this story, with the before/after timing as the punchline, and the loading-check ritual as the integrity beat.

## 21.5 Where You Stand

Part III is done, and honestly measured: you can design a small schema, load and reconcile data, query with the five working shapes, join without fear (and catch fan-out), layer with CTEs, rank and lag with windows, read inherited SQL, and package it all professionally. That is working-analyst SQL for the majority of analytics jobs — and it was eight chapters.

But look at what you have *not* been able to say, anywhere in Part III: whether Sunday's 28% shortfall is a *pattern or a coincidence*; whether the cooking-oil decline is *significantly* steeper than the noise; whether the loyalty scheme *caused* anything. SQL — all tools so far — describes; it cannot conclude. That is statistics' monopoly, and it is where the shop's questions are taking you next.

> **From Your Toolkit — the query pack travels:** this chapter's pack (loading checks + question queries + audit, under a README) is the template for Project 3's Python pipeline, Project 4's Power BI refresh, and any reporting role's first month. Employers ask "how would you make this repeatable?" — the pack *is* the answer.

## Key Takeaways

- Build with checks: schema with keys, CSV imports, then the five loading checks (counts, key census, orphans, totals, NULLs) — every load, forever.
- Ten business questions decompose into the five working shapes; each answer is a saved, commented, reconciled query.
- The deliverable that matters is the *reusable pack*: import, check, run, report — twenty minutes, monthly.
- Portfolio evidence #2: database + query pack + results document + the 150-word note with its honest limits.
- SQL describes; statistics concludes — the questions you now cannot answer are Part IV's syllabus.

## Practice Lab

1. Build the full database: the four CREATE TABLEs, the imports, and all five loading checks; reconcile the sales total to your Part II workbook cent-for-cent and log the bridge number.
2. Answer all ten questions as the query pack (filenames, header blocks with expected totals, comments for why); paste each result into a results document with a one-sentence finding above every table.
3. The trade-off memo: Q10's range-rationalisation as a half-page memo to Tariro — recommendation, the revenue at risk, what you would measure before deciding, and the caveat that 18 months is this shop, not all shops.
4. The dry run: pretend it is next month — re-import a (copied, lightly edited: add 50 plausible new sales) CSV set, run the whole pack, and fix whatever breaks; write down what the dry run caught that the first run hid.
5. Update the portfolio: file the artefacts, write the 150-word note, and draft the STAR paragraph for "improved a reporting process" — while the details are vivid.

## Further Reading

- Chapters 44–46 (the portfolio, assembled properly), Chapter 37 (the pack, automated)
- Appendix A (every pattern used here, ready to copy), Appendix E (the datasets)
