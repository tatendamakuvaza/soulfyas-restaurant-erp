# Chapter 19: Window Functions

*Part III — SQL: The Language of Data*

> "GROUP BY folds rows into one. A window function walks along the rows and leaves every one of them standing — carrying new knowledge."

### In this chapter you will learn

- The OVER clause: partition, order, and the "moving window" idea in plain words.
- Running totals and moving averages — the shop's rhythm, computed.
- Rankings: ROW_NUMBER, RANK, DENSE_RANK — and which to reach for.
- LAG and LEAD: the previous and next row, and month-over-month change.
- The pattern that completes Chapter 18: top-N within each group, in one query.

## 19.1 The Idea

Chapter 16's aggregates collapse: seventeen hundred June rows become one row, one SUM. Sometimes that is the deliverable. But the shop's most human questions keep the rows and *annotate* them: "add up my revenue so far", "rank these items within their category", "compare this month to last month". These are aggregate-flavoured computations that must not collapse anything — and that is a **window function**: an aggregate (or rank, or offset) computed over a *window* of rows, with the result attached to every row, rows intact.

The whole grammar is the **OVER** clause and its two optional settings:

```sql
SUM(amount) OVER (
    PARTITION BY category      -- restart the computation for each category
    ORDER BY date              -- walk the rows in date order
    ROWS BETWEEN ...           -- (optional) which neighbours count
)
```

`PARTITION BY` is GROUP BY's gentler cousin: it splits rows into partitions and computes *within* each, without folding them. `ORDER BY` turns a partition into an ordered walk — which is what makes *running* totals and *previous* rows meaningful. Nothing here collapses; every input row survives with a new column of knowledge.

## 19.2 Running Totals and Moving Averages

Tariro's bank manager wants to see the year accumulating. The running total:

```sql
SELECT date, amount,
       SUM(amount) OVER (ORDER BY date, sale_id) AS running_total
FROM   sales
ORDER  BY date;
```

Read the OVER: walk the rows in date order, and at each row, sum *this row and everything before it*. Each row now carries the year-to-date figure for its moment — the cumulative line a bank manager reads at a glance. (The `sale_id` tiebreaker matters more than it looks: rows sharing a date need a deterministic order, or "everything before it" is ambiguous and engines may differ — a professional detail that prevents a subtle bug.)

The moving average — smoothing the daily noise into a weekly rhythm:

```sql
SELECT date, amount,
       AVG(amount) OVER (ORDER BY date
                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7day
FROM   sales;
```

The frame — `ROWS BETWEEN 6 PRECEDING AND CURRENT ROW` — is the "moving window": the last seven rows including this one, recomputed at every step. The sawtooth of daily takings flattens into a readable trend; this same shape returns as the analyst's standard smoothing move in Python (Chapter 35) and on dashboards (Chapter 42). Frames give you any neighbourhood you can describe: `3 PRECEDING AND 3 FOLLOWING` (centred), `UNBOUNDED PRECEDING` (everything before), and friends.

## 19.3 The Ranking Trio

Three functions that order rows, with subtly different behaviours you must be able to name:

```sql
SELECT sale_id, category, amount,
       ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount DESC) AS rn,
       RANK()       OVER (PARTITION BY category ORDER BY amount DESC) AS rnk,
       DENSE_RANK() OVER (PARTITION BY category ORDER BY amount DESC) AS drnk
FROM   sales;
```

- **ROW_NUMBER()** — 1, 2, 3, 4... arbitrary but unique: ties broken silently. Use when you need *exactly N rows per group*, no arguments.
- **RANK()** — 1, 2, 2, 4... ties share a rank, then a gap. Use for leaderboards ("joint second place, next is fourth").
- **DENSE_RANK()** — 1, 2, 2, 3... ties share, no gaps. Use when "the top 3 ranks" should mean the podium, however many share it.

On Tariro's data the difference shows up wherever the 5.00 mode (Chapter 12) repeats heavily at the top of a category: ROW_NUMBER hands out 1,2,3 among equal amounts; RANK declares a five-way tie for first and jumps to 6; DENSE_RANK stays at 2. Choosing wrongly does not error — it silently returns the wrong rows, which is worse. Name your tie policy out loud before you pick.

## 19.4 LAG and LEAD

The offsets look one row back or forward within a partition and bring back a value — the machinery of *change*:

```sql
WITH monthly AS (
    SELECT substr(date, 1, 7) AS month, SUM(amount) AS revenue
    FROM   sales
    GROUP BY substr(date, 1, 7)
)
SELECT month, revenue,
       LAG(revenue) OVER (ORDER BY month)                 AS prev_month,
       revenue - LAG(revenue) OVER (ORDER BY month)       AS change,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 1)     AS pct_change
FROM   monthly;
```

The first month's `prev_month` is NULL — there is no previous month, and LAG is honest about it (Chapter 15's NULL discipline returns; wrap in COALESCE or filter if it offends a report). Month-over-month change is the single most requested derived metric in working analytics, and it is *this* pattern, verbatim, everywhere: revenue in a monthly CTE, LAG it, subtract, divide with the decimal point. Notice also that this chapter's example *is* Chapter 18's pipeline — CTE then window — the two compose naturally, because both keep stories readable.

## 19.5 Top-N Within Each Group

The pattern this book has been circling since Chapter 18: "the top 3 items by revenue *within each category*" — the grouped top-list that flat GROUP BY cannot express:

```sql
WITH item_revenue AS (
    SELECT category, item, SUM(amount) AS revenue
    FROM   sales
    GROUP  BY category, item
),
ranked AS (
    SELECT category, item, revenue,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY revenue DESC) AS rn
    FROM   item_revenue
)
SELECT category, item, revenue
FROM   ranked
WHERE  rn <= 3
ORDER  BY category, revenue DESC;
```

Three paragraphs: aggregate (item revenues), rank within categories (ROW_NUMBER, ties broken silently — a policy, stated), filter the podium. This exact query shape is among the most-asked SQL interview questions in existence ("top 3 salaries per department" is this query in office costume), and it is the analysis behind "what should we feature, by aisle?" — a real retail decision, arriving as one saved query.

> **From Your Toolkit — windows everywhere:** the running total returns in pandas' `.cumsum()` (Chapter 34) and Power BI's DAX pattern (Chapter 40's time intelligence); month-over-month is a standard quick-measure; the ranking trio is every "leaderboard" visual. The window concept — *annotate, don't collapse* — is also what distinguishes an intermediate analyst's SQL from a beginner's, and interviewers can smell the difference in one question.

## Key Takeaways

- Window functions compute over a window and keep every row: OVER (PARTITION BY ... ORDER BY ... frame).
- Running totals and moving averages = ORDER BY plus SUM/AVG; frame `ROWS BETWEEN n PRECEDING AND CURRENT ROW` moves the neighbourhood.
- Ranking trio: ROW_NUMBER (exact N), RANK (ties, gaps), DENSE_RANK (ties, no gaps) — choose a tie policy deliberately.
- LAG/LEAD give previous/next values: month-over-month change in one line; first rows are honestly NULL.
- Top-N-per-group = aggregate → rank → filter: the interview classic and a real retail decision, one CTE pipeline.

## Practice Lab

1. The cumulative year: running total over all sales (with the sale_id tiebreaker), filtered to one calendar year; then a 7-day moving average of daily takings beside it; write one sentence on what the smoothing reveals that the daily noise hides.
2. The trio, compared: run the ranking-trio query on your data; find a category where the three disagree (a tie at the podium); and write the tie policy you would defend for "top 3 items per category".
3. Month-over-month: the monthly LAG query with change and pct_change; annotate the biggest jump and biggest drop in your log; connect one of them to a planted pattern you already know (what happened in month 9?).
4. The podium query: top 3 items by revenue within each category (the query above); reconcile its grand total against a grouped-items total — reconciliation after filtering a ranking is exactly where fan-out-style surprises hide.
5. Stretch — the gap analysis: with LAG over daily revenue ordered by date, flag days whose takings dropped more than 40% from the previous day; list them and classify each (missing-data day, Sunday, holiday, or genuine dip). This is a real on-call analyst task wearing a small costume.

## Further Reading

- Chapter 34 (pandas' cumsum/shift — these patterns in Python), Chapter 40 (DAX time intelligence)
- Appendix A (the window cookbook: frames, gaps-and-islands, sessionisation)
