# Appendix A: SQL Cookbook

*Appendices — The Cookbook*

> "Thirty-five queries, commented line by line — the 25 patterns this book used, plus the advanced set promised in Chapters 18–19. Replace table and column names, keep the shape."

Conventions: queries run on SQLite unless noted (dialect notes at the end); the running tables are `sales(sale_id, date, till, customer_id, payment_type, amount)`, `customers(customer_id, name, suburb, joined, loyalty_tier)`, `stock(week, item, qty_on_hand)`, `suppliers(item, supplier, unit_cost, last_price_change)`.

## Reading and Filtering

**1. First look — the safe preview**

```sql
SELECT *               -- asterisk for exploring ONLY; name columns for real work
FROM   sales
LIMIT  5;              -- never meet a new table without LIMIT
```

**2. Named columns, chosen order**

```sql
SELECT sale_id,
       date,
       amount,         -- SELECT order is your presentation order
       payment_type
FROM   sales;
```

**3. Filtering rows — the core comparisons**

```sql
SELECT *
FROM   sales
WHERE  amount >= 50            -- numeric: no quotes
   AND payment_type = 'EcoCash'  -- text: quotes, case-sensitive
ORDER BY amount DESC;
```

**4. Date ranges — two safe forms**

```sql
SELECT *
FROM   sales
WHERE  date >= '2025-06-01'
  AND  date <  '2025-07-01';    -- half-open range: survives timestamps
                                 -- ("2025-06-30 14:33") that BETWEEN can miss
```

**5. Membership and exclusion**

```sql
SELECT *
FROM   sales
WHERE  payment_type IN ('Cash', 'Card')     -- the readable OR chain
  AND  customer_id IS NOT NULL              -- NULLs never match; test by name
  AND  suburb NOT IN ('Avondale');          -- careful: NOT IN + NULL = empty result
```

**6. Top-N**

```sql
SELECT sale_id, date, amount
FROM   sales
ORDER BY amount DESC     -- sort first
LIMIT 10;                -- then cap
```

**7. Text matching**

```sql
SELECT DISTINCT item
FROM   stock
WHERE  item LIKE '%Oil%'          -- % = any characters
   AND item NOT LIKE '%sample%';  -- LIKE is case-insensitive in SQLite,
                                  -- case-sensitive in Postgres (use ILIKE)
```

## Grouping and Aggregating

**8. The whole table in one line**

```sql
SELECT COUNT(*)        AS n_sales,        -- rows
       SUM(amount)     AS total_revenue,
       AVG(amount)     AS avg_basket,     -- NULLs ignored
       MIN(amount)     AS smallest,
       MAX(amount)     AS largest
FROM   sales;
```

**9. The two COUNTs**

```sql
SELECT COUNT(*)             AS all_sales,       -- every row
       COUNT(customer_id)   AS member_sales     -- non-NULL only
FROM   sales;                                  -- the difference IS an analysis
```

**10. Totals of something, for each something else**

```sql
SELECT   payment_type,
         COUNT(*)    AS n,
         SUM(amount) AS revenue
FROM     sales
GROUP BY payment_type          -- one row per distinct value
ORDER BY revenue DESC;
```

**11. Groups with conditions — WHERE chooses rows, HAVING chooses groups**

```sql
SELECT   category,
         COUNT(*)    AS n_sales,
         AVG(amount) AS avg_basket
FROM     sales
WHERE    amount <= 21.50         -- exclude whales BEFORE averaging
GROUP BY category
HAVING   COUNT(*) >= 50          -- then keep busy categories
ORDER BY avg_basket DESC;
```

**12. Month extraction and grouping (SQLite / portable-ish)**

```sql
SELECT   substr(date, 1, 7) AS month,     -- '2025-06'; Postgres: date_trunc('month', date)
         SUM(amount)        AS revenue
FROM     sales
GROUP BY substr(date, 1, 7)
ORDER BY month;
```

**13. Percentile (the robust typical)**

```sql
SELECT AVG(amount)                                AS mean,
       (SELECT amount FROM sales ORDER BY amount
        LIMIT 1 OFFSET (SELECT COUNT(*)/2 FROM sales))  AS approx_median
FROM   sales;
-- Postgres/Snowflake/BigQuery: PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount)
```

## Joining

**14. Enrichment join (LEFT — keep all sales)**

```sql
SELECT s.sale_id, s.amount,
       c.name, c.suburb          -- qualify columns when tables share names
FROM   sales s
LEFT JOIN customers c
       ON c.customer_id = s.customer_id;   -- unmatched -> NULLs on the right
```

**15. The fan-out defence (run after EVERY join)**

```sql
SELECT (SELECT COUNT(*) FROM sales)     AS rows_before,
       COUNT(*)                         AS rows_after,   -- must equal rows_before
       SUM(s.amount)                    AS revenue       -- must equal the bridge
FROM   sales s
LEFT JOIN customers c ON c.customer_id = s.customer_id;
```

**16. The anti-join — rows with no match**

```sql
SELECT s.customer_id, COUNT(*) AS orphan_sales
FROM   sales s
LEFT JOIN customers c ON c.customer_id = s.customer_id
WHERE  c.customer_id IS NULL          -- keep only the unmatched
GROUP BY s.customer_id;
-- "customers who never bought" = same pattern, tables swapped
```

**17. Aggregate, then join (the fan-out-proof pattern)**

```sql
WITH member_value AS (
    SELECT customer_id, SUM(amount) AS lifetime_revenue, COUNT(*) AS n_sales
    FROM   sales
    WHERE  customer_id IS NOT NULL
    GROUP BY customer_id            -- one row per customer FIRST
)
SELECT c.name, c.suburb,
       v.lifetime_revenue, v.n_sales
FROM   customers c
JOIN   member_value v ON v.customer_id = c.customer_id
ORDER BY v.lifetime_revenue DESC
LIMIT 20;
```

**18. Join with condition on the right table (the classic trap)**

```sql
-- WRONG: WHERE c.suburb = 'Avondale' silently turns LEFT into INNER
SELECT s.sale_id, c.suburb
FROM   sales s
LEFT JOIN customers c
       ON c.customer_id = s.customer_id
      AND c.suburb = 'Avondale';   -- condition INSIDE ON: non-matching kept, NULL suburb
```

## Layering (CTEs and Windows)

**19. Share of total**

```sql
WITH by_payment AS (
    SELECT payment_type, SUM(amount) AS revenue
    FROM   sales
    GROUP BY payment_type
)
SELECT payment_type,
       revenue,
       ROUND(100.0 * revenue / SUM(revenue) OVER (), 1) AS pct_share
                              -- OVER () = whole table, rows not collapsed
FROM   by_payment
ORDER BY revenue DESC;       -- 100.0 forces decimal division
```

**20. Top-N within each group**

```sql
WITH item_rev AS (
    SELECT item, SUM(amount) AS revenue
    FROM   sales GROUP BY item
),
ranked AS (
    SELECT item, revenue,
           ROW_NUMBER() OVER (ORDER BY revenue DESC) AS rn_all,
           DENSE_RANK() OVER (ORDER BY revenue DESC) AS dr_all
    FROM   item_rev
)
SELECT * FROM ranked WHERE rn_all <= 10;
-- per-category: PARTITION BY category inside the OVER
```

**21. Running total and moving average**

```sql
SELECT date,
       SUM(amount) OVER (ORDER BY date, sale_id) AS running_total,
       AVG(amount) OVER (ORDER BY date
                         ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) AS avg_7day
FROM   sales;
-- tie-break with sale_id: same-date rows need a deterministic order
```

**22. Month-over-month with LAG**

```sql
WITH monthly AS (
    SELECT substr(date,1,7) AS month, SUM(amount) AS revenue
    FROM   sales
    GROUP BY substr(date,1,7)
)
SELECT month,
       revenue,
       LAG(revenue) OVER (ORDER BY month)              AS prev_month,
       ROUND(100.0 * (revenue - LAG(revenue) OVER (ORDER BY month))
             / LAG(revenue) OVER (ORDER BY month), 1)  AS pct_change
FROM   monthly;
```

**23. Deduplicate — keep the latest row per key**

```sql
WITH ranked AS (
    SELECT *,
           ROW_NUMBER() OVER (PARTITION BY customer_id
                              ORDER BY date DESC) AS rn
    FROM   messy_contacts
)
SELECT * FROM ranked WHERE rn = 1;
```

**24. Gap check — the data-quality sweep**

```sql
SELECT 'duplicate sale_ids' AS check_name, COUNT(*) AS n
FROM   (SELECT sale_id FROM sales GROUP BY sale_id HAVING COUNT(*) > 1)
UNION ALL
SELECT 'null amounts', COUNT(*) FROM sales WHERE amount IS NULL
UNION ALL
SELECT 'orphan customer refs', COUNT(*)
FROM   sales s LEFT JOIN customers c ON c.customer_id = s.customer_id
WHERE  s.customer_id IS NOT NULL AND c.customer_id IS NULL;
```

**25. The professional header (not a query — the wrapper)**

```sql
-- monthly_revenue_by_till.sql
-- Purpose: monthly revenue split by till, for the ops meeting
-- Author: <you>, created 2025-06; source: sales (till system export)
-- Expected when last run: 18 rows, total 54,013.50  -- reconcile before trusting
WITH monthly AS (
    SELECT substr(date,1,7) AS month, till, SUM(amount) AS revenue
    FROM   sales
    GROUP BY substr(date,1,7), till
)
SELECT * FROM monthly ORDER BY month, till;
```

## Beyond the 25 — The Advanced Patterns (promised in Chapters 18–19)

**26. Gaps and islands — find runs of consecutive days**

```sql
-- Which stretches of days was each item out of stock (or on promotion)?
WITH dated AS (
    SELECT item, week,
           -- days since a fixed epoch, numbered
           CAST(julianday(week) AS INTEGER) AS d    -- Postgres: week - DATE '2024-01-01'
    FROM   stock
),
grouped AS (
    SELECT item, d,
           d - ROW_NUMBER() OVER (PARTITION BY item
                                  ORDER BY d) AS island_id
    -- consecutive days share the same (d - row_number): the gap trick
    FROM   dated
)
SELECT item,
       MIN(week) AS run_start,
       MAX(week) AS run_end,
       COUNT(*)  AS run_length
FROM   grouped
GROUP BY item, island_id
HAVING COUNT(*) > 1                 -- runs longer than one
ORDER BY item, run_start;
```

**27. Sessionisation — group events into visits**

```sql
-- A new "visit" starts when a gap exceeds 30 minutes (web logs, till events)
WITH stamped AS (
    SELECT customer_id, occurred_at,
           LAG(occurred_at) OVER (PARTITION BY customer_id
                                  ORDER BY occurred_at) AS prev_at
    FROM   events
),
flagged AS (
    SELECT *,
           CASE WHEN prev_at IS NULL
              OR (julianday(occurred_at) - julianday(prev_at)) * 24 * 60 > 30
                THEN 1 ELSE 0 END AS new_visit   -- Postgres: EXTRACT(EPOCH FROM ...)
    FROM   stamped
),
visited AS (
    SELECT *,
           SUM(new_visit) OVER (PARTITION BY customer_id
                                ORDER BY occurred_at
                                ROWS UNBOUNDED PRECEDING) AS visit_no
    FROM   flagged
)
SELECT customer_id, visit_no,
       COUNT(*)                AS events,
       MIN(occurred_at)        AS started,
       MAX(occurred_at)        AS ended
FROM   visited
GROUP BY customer_id, visit_no;
```

**28. Cohort retention grid in SQL (Project 4's shape)**

```sql
WITH first_purchase AS (
    SELECT customer_id, MIN(date) AS first_date
    FROM   sales
    WHERE  customer_id IS NOT NULL
    GROUP BY customer_id
),
activity AS (
    SELECT s.customer_id,
           substr(f.first_date, 1, 7) AS join_cohort,
           CAST((julianday(substr(s.date,1,7) || '-01')
               - julianday(substr(f.first_date,1,7) || '-01')) / 30.4 AS INT)
                                       AS age_months,   -- months since first buy
           1 AS active
    FROM   sales s
    JOIN   first_purchase f USING (customer_id)
    GROUP BY s.customer_id, join_cohort,
             substr(s.date, 1, 7)      -- one row per active month
)
SELECT join_cohort,
       age_months,
       COUNT(*) AS active_customers
FROM   activity
GROUP BY join_cohort, age_months
ORDER BY join_cohort, age_months;
-- read as a grid: cohort down, age across -- the retention heatmap, in SQL
```

**29. Year-over-year same-period comparison**

```sql
SELECT month,
       revenue,
       LAG(revenue, 12) OVER (ORDER BY month) AS same_month_ly,
       ROUND(100.0 * (revenue - LAG(revenue, 12) OVER (ORDER BY month))
             / LAG(revenue, 12) OVER (ORDER BY month), 1) AS yoy_pct
FROM   monthly_revenue;
-- LAG with an offset of 12 -- the year-over-year version of query 22
```

**30. Conditional aggregation (the pivot-in-SUM trick)**

```sql
SELECT substr(date, 1, 7) AS month,
       SUM(amount)                                        AS total,
       SUM(CASE WHEN payment_type = 'EcoCash'
                THEN amount ELSE 0 END)                    AS ecocash,
       ROUND(100.0 * SUM(CASE WHEN payment_type = 'EcoCash'
                              THEN amount ELSE 0 END)
             / SUM(amount), 1)                             AS ecocash_pct
FROM   sales
GROUP BY substr(date, 1, 7)
ORDER BY month;
-- one pass, one table, columns-as-conditions -- the cross-tab without pivoting
```

**31. The running-total reconciliation (a check worth saving)**

```sql
-- Does the ledger's running total land exactly on the closing total?
WITH daily AS (
    SELECT date, SUM(amount) AS day_total
    FROM   sales GROUP BY date
),
checked AS (
    SELECT date, day_total,
           SUM(day_total) OVER (ORDER BY date) AS running,
           SUM(day_total) OVER ()              AS grand
    FROM   daily
)
SELECT MAX(running) AS final_running,   -- must equal grand
       MAX(grand)   AS grand_total
FROM   checked;
```

**32. Sampling — N random rows (for audits and quick checks)**

```sql
SELECT * FROM sales ORDER BY RANDOM() LIMIT 100;   -- SQLite
-- Postgres: TABLESAMPLE SYSTEM (1)   BigQuery: TABLESAMPLE SYSTEM (1 PERCENT)
-- the audit habit: pull 100 random rows and eyeball them, monthly
```

**33. The histogram in SQL (bins before charts)**

```sql
SELECT CAST(amount / 5 AS INTEGER) * 5 AS bin_floor,   -- $5-wide bins
       COUNT(*) AS n,
       printf('%s', substr('████████████████████████', 1,
              MIN(20, COUNT(*) / 20))) AS bar           -- ASCII bar, SQLite
FROM   sales
GROUP BY bin_floor
ORDER BY bin_floor;
-- shape-checking in a terminal: the histogram, no chart tool required
```

**34. Medians per group (the robust typical, SQLite edition)**

```sql
WITH ranked AS (
    SELECT category, amount,
           ROW_NUMBER() OVER (PARTITION BY category ORDER BY amount) AS rn,
           COUNT(*)     OVER (PARTITION BY category) AS n
    FROM   sales
)
SELECT category, AVG(amount) AS median
FROM   ranked
WHERE  rn IN ((n + 1) / 2, (n + 2) / 2)   -- middle one, or middle two averaged
GROUP BY category;
-- Postgres/Snowflake: PERCENTILE_CONT(0.5) WITHIN GROUP (ORDER BY amount)
```

**35. The pre-aggregation pattern (warehouse etiquette)**

```sql
-- Never join a 40-million-row fact to a dimension for one number:
-- aggregate the fact to the grain you need FIRST, then join.
WITH daily_region AS (
    SELECT region_id, date, SUM(amount) AS revenue
    FROM   fact_sales
    WHERE  date >= '2025-01-01'         -- sargable: filter before the work
    GROUP BY region_id, date            -- aggregate before the join
)
SELECT r.region_name, SUM(d.revenue) AS revenue
FROM   daily_region d
JOIN   dim_region r ON r.region_id = d.region_id
GROUP BY r.region_name;
-- smaller intermediate, smaller bill, same answer (Ch. 58's cost instinct)
```

## Dialect Notes

| Task | SQLite | PostgreSQL / BigQuery / Snowflake |
|---|---|---|
| First N rows | `LIMIT 10` | `LIMIT 10` / `FETCH FIRST 10 ROWS ONLY` |
| Substring | `substr(x,1,7)` | `SUBSTRING(x,1,7)` or `date_trunc` |
| Case-insensitive text | `LIKE` (already) | `ILIKE` |
| Median | hand-rolled (Q13) | `PERCENTILE_CONT(0.5) WITHIN GROUP (...)` |
| Booleans | 0/1 | true/false |
| Date math | `date(d,'+1 month')` | `d + INTERVAL '1 month'` |

*Keep the shapes; translate the dialect. The query you cannot read is the query you cannot trust — comment the why, header the expectation, reconcile the total.*
