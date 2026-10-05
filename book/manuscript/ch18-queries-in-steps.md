# Chapter 18: Queries in Steps — Subqueries and CTEs

*Part III — SQL: The Language of Data*

> "No one writes a hundred-line query. Everyone writes five twenty-line queries and glues them together."

### In this chapter you will learn

- Why big queries fail as queries and succeed as pipelines.
- The subquery: a query inside a query, and where it may stand.
- The CTE — WITH — the professional's building block, step by step.
- Solving the share-of-total problem that Chapter 16 left open.
- Reading and debugging layered queries without fear.

## 18.1 The Case for Steps

Here is a real question, mid-sized: *"Which payment types take more than their fair share of revenue — and how does that differ between the first and second till?"* As one flat query it is a monster: two groupings, two filters, a share computation, a comparison. Written in one breath it cannot be read, cannot be debugged, and — the working analyst's real criterion — cannot be *changed* on Friday afternoon when the question shifts.

The answer to complexity in SQL is not cleverness; it is **decomposition**: write small queries that each do one thing, and connect them. SQL gives you two connection mechanisms. The **subquery** nests a query inside another, where a value or a table is expected. The **CTE** (Common Table Expression, the `WITH` clause) names each step and stacks them like paragraphs. Same engine under both; different ergonomics. Professionals reach for CTEs by default, and you will see why in three paragraphs.

## 18.2 The Subquery

A subquery is a complete query in parentheses, used in one of three slots:

**In WHERE, where a value is expected** — "sales bigger than the average sale":

```sql
SELECT sale_id, amount
FROM   sales
WHERE  amount > (SELECT AVG(amount) FROM sales);
```

The inner query runs first, returns one number (8.41), and the outer query uses it. This is a *scalar subquery* — one row, one column — and it can stand anywhere a number could.

**In FROM, where a table is expected** — "average *per month*, then the best months": aggregate first, query the aggregate second (the "aggregate, then join" pattern from Chapter 17, in its simplest form):

```sql
SELECT month, revenue
FROM   (SELECT substr(date, 1, 7) AS month,
               SUM(amount)        AS revenue
        FROM   sales
        GROUP BY substr(date, 1, 7)) AS monthly
ORDER  BY revenue DESC
LIMIT  5;
```

The inner query builds a table named `monthly` — invisible, unpersisted, existing only for this query — and the outer query treats it like any table. This is the mechanism, plain and complete; the CTE is the same thing with better manners.

**In SELECT, where a column is expected** — a correlated subquery, one value per row, discussed with its costs in the Further Reading pointers; rare in beginner work, recognised on sight in inherited code (a subquery in SELECT that mentions the outer table's alias).

## 18.3 The CTE: WITH, and Paragraphs

The CTE names each step, up front, in the order a human reads:

```sql
WITH monthly AS (
    SELECT substr(date, 1, 7) AS month,
           SUM(amount)        AS revenue
    FROM   sales
    GROUP BY substr(date, 1, 7)
),
best AS (
    SELECT * FROM monthly ORDER BY revenue DESC LIMIT 5
)
SELECT * FROM best;
```

Read it as a recipe: *with* monthly revenue in hand, *with* the best five months chosen, show them. Each CTE is a named, testable paragraph; the steps stack (later CTEs may use earlier ones); and the final SELECT is the conclusion of the argument. The differences from subqueries are ergonomics and they matter at work: CTEs **run top-to-bottom like the story they tell** (subqueries hide inside-out), they **can be tested one at a time** (run the WITH block alone — DB Browser shows you `monthly` — then add the next step), and a CTE can be *reused* twice in one query, which is exactly what the share-of-total problem needs.

## 18.4 Share of Total, Solved

Chapter 16 ended hungry for this: each group's share of the whole. The CTE solution is the pattern's canonical shape — build the grouped numbers, build (or reuse) the total, divide:

```sql
WITH by_payment AS (
    SELECT payment_type,
           SUM(amount) AS revenue
    FROM   sales
    GROUP BY payment_type
),
with_total AS (
    SELECT payment_type,
           revenue,
           SUM(revenue) OVER () AS total_revenue
    FROM   by_payment
)
SELECT payment_type,
       revenue,
       ROUND(100.0 * revenue / total_revenue, 1) AS pct_share
FROM   with_total
ORDER  BY revenue DESC;
```

Two things to notice. The `SUM(...) OVER ()` is a window function — a one-line preview of Chapter 19 that computes the total *without collapsing the rows* (empty OVER brackets means "the whole table is my group"). And `100.0 *` — the decimal point forces decimal arithmetic; with integers `100 * revenue / total` would truncate, and shares would sum to 97% mysteriously (a Chapter 7 lesson in SQL clothing).

The recipe generalises to the most-asked family of interview questions: *top X within each group* ("top-selling item per category", "busiest day per month"). Aggregate, rank (Chapter 19's ROW_NUMBER), filter the ranking — three CTE paragraphs, one answer. You now hold every ingredient but the ranking verb.

## 18.5 Debugging Layers

Layered queries are debugged layer by layer — this is precisely why they exist. The method, always the same:

1. **Run each CTE alone, from the first.** Does `by_payment` look right? (Seven rows would not; three payment types should.) Check each layer's row count and total against a known number — the reconciliation habit, now applied to intermediates.
2. **Add layers one at a time.** The step that breaks the query is the step you just added; that is a much smaller problem space than "the query is wrong".
3. **Read errors from the inside out.** "No such column: revenue" in the second CTE means the first CTE did not expose a column by that name — check the SELECT list of the step before, not the step that complained.
4. **When stuck, materialise.** Paste a CTE's output into a scratch table (`CREATE TABLE scratch AS SELECT ...`), and query the scratch — the layers become inspectable objects. Delete scratch tables when done; your future self inheriting the database thanks you.

> **From Your Toolkit — pipelines, named:** the CTE habit — decompose, name, test each step, stack — is how *all* serious analysis code is written: pandas chains each step into a named variable (Chapter 32), Python functions decompose like CTEs (Chapter 31), Power BI's Power Query Editor is literally a stack of named, reorderable, testable steps on your data (Chapter 39). SQL taught you decomposition because SQL could not hide complexity; every later tool inherits the discipline.

## Key Takeaways

- Decomposition over cleverness: small queries, connected, beat one heroic query — always.
- Subqueries slot into WHERE (value), FROM (table), SELECT (correlated, rare); CTEs name the steps.
- CTEs read top-to-bottom, test one layer at a time, and can be reused — the professional default.
- Share-of-total: grouped CTE, total via `SUM() OVER ()`, divide with a decimal point; generalises to top-X-per-group.
- Debug by layers: run each step alone, add one at a time, read errors inside-out, materialise when stuck.

## Practice Lab

1. Rewrite your Chapter 16 category query as a two-CTE pipeline: grouped revenue, then rank; run each CTE alone in DB Browser and screenshot or note both intermediate tables.
2. Share of revenue by payment type (the query above), then by suburb via a join to customers — and write the two sentences the shares tell, including the NULL/non-member handling you chose.
3. The fair-share question that opened the chapter, answered: with CTEs, revenue share by payment type *for each till*, side by side; one sentence on whether the tills differ and whether the difference matters (say how you decided).
4. Top item per category: aggregate item revenue within category, and identify the top of each — you may need a window function peek ahead (Chapter 19) or a self-join; either way, document your steps as CTEs and reconcile the grand total.
5. The refactor drill: take your longest flat query from any Practice Lab so far and rebuild it as named CTEs, one job each; then hand both versions to a friend and time which one they can explain back to you faster. That time difference is the entire argument for this chapter.

## Further Reading

- Chapter 19 (window functions — the ranking verbs this chapter reached for)
- Appendix A (the CTE patterns: share-of-total, top-per-group, gap/island queries)
