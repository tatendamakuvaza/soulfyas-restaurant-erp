# Chapter 16: Counting and Grouping

*Part III — SQL: The Language of Data*

> "The question is never 'what is the total?' It is 'what is the total, for each what?'"

### In this chapter you will learn

- The aggregates — COUNT, SUM, AVG, MIN, MAX — and the star habit of grouping.
- GROUP BY: the pivot table's engine, exposed.
- HAVING: filtering groups after they are built, and why WHERE cannot.
- GROUP BY's execution order — the mental model that prevents most beginner errors.
- The rounding trap, the NULL count, and other honest-details.

## 16.1 The Aggregates

SQL's aggregate functions collapse many rows into one number, and their names are their job descriptions:

```sql
SELECT COUNT(*)      AS n_sales,
       SUM(amount)   AS total_revenue,
       AVG(amount)   AS avg_basket,
       MIN(amount)   AS smallest,
       MAX(amount)   AS largest
FROM   sales;
```

One query, the whole shop: 6,420 sales, 54,013.50 total, 8.41 average, 0.50 smallest, 412.00 largest. The `AS` clauses give the result columns clean names — cosmetic, and a professional habit (reports read by others name their columns).

Two details before anything else. **COUNT has two forms with different meanings**: `COUNT(*)` counts rows; `COUNT(customer_id)` counts non-NULL values — on Tariro's data, all sales versus member sales only, a distinction that *is* an analysis (the loyalty share, one query). **AVG of amounts ignores NULLs** — usually what you want, occasionally a trap (a table of NULL-heavy discounts averages the known, not the whole); know which you are computing, and say so in the report.

## 16.2 GROUP BY: For Each What

A bare aggregate answers the whole table. Business questions are almost always "for each what": revenue by month, sales by payment type, average basket by weekday. **GROUP BY** builds the "for each": it splits the table into groups — one per distinct value of the grouping column — and runs the aggregates *inside each group*:

```sql
-- the monthly revenue pivot, in one query
SELECT   substr(date, 1, 7) AS month,
         COUNT(*)           AS n_sales,
         SUM(amount)        AS revenue
FROM     sales
GROUP BY substr(date, 1, 7)
ORDER BY month;
```

Read it aloud: *for each* month, the count and the revenue. Eighteen rows appear — the exact table a pivot produced in Chapter 10, now reproducible forever with one saved query instead of a re-dragged dance. Swap the grouping column and the query re-twists exactly like the pivot: `GROUP BY payment_type`, `GROUP BY weekday`, `GROUP BY till`. The pivot's four shelves, translated: Rows is GROUP BY, Values is the aggregates, Columns is a second grouping column (GROUP BY weekday, payment_type — every combination gets a row), Filters is WHERE.

One law, unbreakable, and the source of most beginner errors: **every column in SELECT must be either grouped or aggregated.** `SELECT weekday, amount FROM sales GROUP BY weekday` is refused by the engine — and rightly: weekday has seven values, amount has thousands, and no honest table can show both unaggregated. The error message is the database teaching you its model; read it as a lesson, not an insult.

## 16.3 HAVING: Filtering Groups

Tariro's next question: *which categories average over 15 dollars a sale?* — a filter on an average, which is a filter **after** grouping. WHERE cannot do this (WHERE runs before groups exist), so SQL provides HAVING, the group-filter:

```sql
SELECT   category,
         COUNT(*)    AS n_sales,
         AVG(amount) AS avg_basket
FROM     sales
GROUP BY category
HAVING   AVG(amount) > 15
ORDER BY avg_basket DESC;
```

The pair to remember: **WHERE chooses rows before grouping; HAVING chooses groups after.** A query can carry both, and often does — small sales (WHERE) excluded before the category averages are computed (HAVING), which changes the answer, and the analyst chooses the order deliberately:

```sql
SELECT   category, COUNT(*) AS n, AVG(amount) AS avg_basket
FROM     sales
WHERE    amount <= 21.50            -- drop the whales FIRST
GROUP BY category
HAVING   COUNT(*) >= 50             -- then keep busy categories
ORDER BY avg_basket DESC;
```

## 16.4 The Execution Order in Your Head

SQL is written in one order and executed in another, and holding both orders in your head is the difference between guessing and knowing:

```text
Written:   SELECT → FROM → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT
Executed:  FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT
```

Read the executed order as a story: gather the tables (FROM), keep the rows that qualify (WHERE), build the groups (GROUP BY), keep the groups that qualify (HAVING), compute the selected columns (SELECT), sort, cap. Every confusing query becomes readable by walking it down this pipeline — and every error message ("no such column" in HAVING for something computed in SELECT) makes sense once you know SELECT happens *after* HAVING. (Aliases from SELECT are invisible to WHERE and HAVING; they exist for ORDER BY — or repeat the expression.)

## 16.5 Honest Details

- **The rounding trap.** `AVG(amount)` on cents can return 8.419859227... — the engine is not wrong, it is exact. Round for display (`ROUND(AVG(amount), 2)`), never for computation; rounding intermediate results accumulates error the way floats did in Chapter 7, and reports that don't add up come from exactly this habit.
- **The NULL group.** `GROUP BY customer_id` produces a NULL group — the non-members, grouped as one "customer". It appears at the top or bottom of your results; name it in the report ("non-member sales") rather than letting a reader ask what NULL means.
- **Percent shares.** "What share of revenue is each payment type?" needs each group's sum over the total — a self-join of aggregates that is the natural first CTE, which is exactly where Chapter 18 goes. You can feel the need for it here; the tool is two chapters away, and that feeling is the best predictor that a tool will stick.

> **From Your Toolkit — the same habit everywhere:** this chapter *is* the pivot table, formalised — and it arrives again as pandas' `.groupby()` (Chapter 34), as Power BI's implicit measures (Chapter 40: drag `amount` in, choose Sum or Average — you are writing this query), and as the GROUP BY you will someday optimise on a million-row table. The "for each what" habit — total, count, and average, grouped, sorted, and checked — is the single most-used move in working analytics. Everything else is decoration.

## Key Takeaways

- Five aggregates: COUNT (two meanings: rows vs non-NULLs), SUM, AVG, MIN, MAX.
- GROUP BY answers "for each what": one row per group, aggregates inside; every selected column grouped or aggregated.
- WHERE filters rows before grouping; HAVING filters groups after — order is analysis, choose it deliberately.
- Execution order: FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT; walk queries down the pipeline.
- Round for display only; name the NULL group; and let the hunger for shares lead you to Chapter 18.

## Practice Lab

1. The shop on one line: the five aggregates over all sales; then the same five *for each till* — and write the two-sentence till comparison (the second till is new: what does its presence do to comparisons over time?).
2. Rebuild Chapter 10's pivots as saved queries: month × revenue, category × revenue (ordered descending), weekday × count and average basket. Reconcile each against the workbook pivot totals — all three must match to the cent.
3. The payment story: revenue and row share by payment_type with COUNT(*) and SUM; add COUNT(customer_id) to the same query and explain the difference between the two counts in one sentence.
4. HAVING, both ways: categories averaging over 15; categories with at least 100 sales; then one query with both a WHERE (exclude whales) and a HAVING — and write one sentence on how the answer differs from the no-WHERE version.
5. The execution-order drill: take your longest query from this lab and annotate each clause with its position in the executed pipeline; then deliberately break it (add an unaggregated column to SELECT with GROUP BY), read the error aloud, and write down what the engine was teaching you.

## Further Reading

- Chapter 17 (joins — the groups get richer), Chapter 18 (CTEs — the share-of-total question, solved)
- Appendix A (the grouping patterns, ready to copy), sqlbolt.com lessons 12–13 for reps
