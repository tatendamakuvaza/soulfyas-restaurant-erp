# Chapter 17: Joins Without Fear

*Part III — SQL: The Language of Data*

> "In a relational database, the join is not a feature. It is the reason the database exists."

### In this chapter you will learn

- The join in SQL: FROM two tables, ON the keys.
- INNER vs LEFT — the two joins that cover 95% of real work.
- Fan-out, formally: how joins multiply rows, and the totals check that catches it.
- Many-to-many, and the bridge table that resolves it.
- Aliases, qualified names, and reading other people's joins.

## 17.1 The Join, Grown Up

Chapter 9 taught the sentence: *match the keys, bring the facts across.* SQL says it in one line — the join lives in the FROM clause:

```sql
SELECT s.sale_id, s.date, s.amount, c.name, c.suburb
FROM   sales s
JOIN   customers c ON c.customer_id = s.customer_id;
```

Three new notations, all habit-forming. The **alias** (`sales s`) shortens every later mention — one letter per table is the working convention. The **qualified name** (`s.amount`, `c.suburb`) says which table a column comes from; SQL requires it when two tables share a column name (`customer_id` exists in both) and professionals write it always — a query that survives next month's schema change is worth two extra characters per column. And **ON** states the join condition: the key match, in exactly the spreadsheet's sense.

## 17.2 INNER and LEFT

`JOIN` (bare) means **inner join**: only rows that match on both sides survive. Every sale with a matching customer appears, enriched with name and suburb; every *non-member* sale — customer_id NULL — vanishes, because NULL matches nothing (Chapter 15's rule, with consequences). The inner join answers "what do we know about both?" and silently amputates the unmatched.

The **LEFT JOIN** keeps every row of the left table, matched or not, and fills the missing right-side columns with NULLs:

```sql
SELECT s.sale_id, s.amount, c.suburb
FROM   sales s
LEFT JOIN customers c ON c.customer_id = s.customer_id;
```

Non-member sales now appear, suburb NULL — the honest full picture of the till. The choice between the two is an *analysis decision*, not a syntax preference: revenue from all sales (LEFT) versus revenue from identifiable customers (INNER) are different numbers answering different questions, and the wrong choice quietly biases a report. **Default to LEFT when the left table is the subject** ("all sales, enriched where possible"); use INNER when only matches are meaningful ("customer purchases").

The other two named joins — RIGHT (mirror of LEFT) and FULL OUTER (keep everything from both sides) — exist for completeness and appear rarely; when you need one, you will know, and Appendix A has it.

## 17.3 The Anti-Join

One join pattern earns its own section because it is pure professional gold: rows on the left with *no* match on the right. "Customers who have never bought anything", "items in stock that never sold", "member_ids in sales that exist in no customer row" (Chapter 9's broken key, found by query):

```sql
SELECT s.customer_id, COUNT(*) AS orphan_sales
FROM   sales s
LEFT JOIN customers c ON c.customer_id = s.customer_id
WHERE  c.customer_id IS NULL
GROUP BY s.customer_id;
```

The trick: LEFT JOIN keeps the unmatched, and `WHERE c.customer_id IS NULL` keeps *only* the unmatched. Data-quality auditing, cold-customer lists, unreconciled invoices — the anti-join is the pattern behind all of them, and it is the single most common "how would you find...?" interview question you will meet in SQL rounds.

## 17.4 Fan-Out, Formally

Now the trap from Chapter 9.5 gets its real name and mechanism. Joins multiply when *both* sides can repeat a key. One-to-many is safe in one direction: sales-to-customers joins many sales (left) to one customer each (right) — each sale appears once. But if the right side *also* repeats the key — say a `customer_discounts` table with two rows for one customer (an old offer and a new one) — then each of that customer's sales matches *both* rows, and appears *twice*: 40 sales become 80 rows, and `SUM(amount)` doubles the customer's revenue. That is **fan-out**: row counts inflate, and every aggregate after the join is quietly wrong. **Many-to-many** — keys repeating on both sides — is fan-out waiting to fire.

The defence is a habit, not a talent:

1. **Count rows before and after.** `SELECT COUNT(*) FROM sales` before the join; count after. If the after-count exceeds the left table, you fanned out.
2. **Reconcile a known total.** Total revenue before the join must equal total revenue after — the Chapter 8 reflex, now load-bearing. If revenue moved, you duplicated, not joined.
3. **Aggregate before joining when you can.** Sum the many-side down to one row per key *first* (a subquery or CTE — next chapter), then join the tidy results. "Aggregate, then join" is the professional's default pattern for exactly this reason.

The **bridge table** resolves true many-to-many relationships by design: a customer can buy many items, an item is bought by many customers — so sales *line items* sit between them (`sale_items(sale_id, item, quantity)`), turning two impossible joins into two safe one-to-many joins. When you design, or inherit, a schema, look for the bridges; their absence is where fan-out breeds.

## 17.5 Reading Others' Joins

Inherited queries — the analyst before you left SQL behind, and now it is yours — are read with a method. Walk the FROM clause first, not the SELECT: list the tables and aliases on paper, draw a line for each ON (a little diagram: boxes, lines, arrowheads at the "many" side), and label each join INNER or LEFT. The picture *is* the query's meaning: which rows survive, which tables are decoration, where the fan-out risk sits. Then read WHERE, then the aggregates — the Chapter 16 pipeline, applied to someone else's work. Chapter 20 turns this into a full survival guide; the diagram habit starts here.

> **From Your Toolkit — joins everywhere, same law:** pandas' `merge(how='left'/'inner')` (Chapter 34) is this chapter wearing Python; Power BI's model view (Chapter 39) draws the boxes-and-lines diagram for you and guards cardinality ("many-to-many" warnings are fan-out warnings); Excel's lookups were one-column joins. The law never varies: **match the keys, check the row counts, reconcile the totals.** Analysts who internalise it are the ones whose numbers survive audit.

## Key Takeaways

- The join lives in FROM: alias the tables, qualify the columns, state the key match in ON.
- INNER keeps matches only; LEFT keeps all left rows — the choice is an analysis decision, not syntax.
- LEFT JOIN + WHERE right-key IS NULL = the anti-join: unmatched rows on demand (audits, cold lists, broken keys).
- Fan-out = keys repeating on both sides; count rows, reconcile totals, aggregate-then-join; bridges resolve many-to-many.
- Read inherited queries by diagramming FROM first — boxes, lines, and which side is "many".

## Practice Lab

1. Enrich: every sale with customer name and suburb (LEFT JOIN); reconcile total revenue and row count against the un-joined sales table — both must match exactly; write the two numbers in your log.
2. The comparison, properly: average basket for member sales vs non-member sales via `c.customer_id IS NULL` grouping on the LEFT JOIN — this is Chapter 9's loyalty question, now in one query; write the caveat sentence beside the number, as always.
3. The anti-join audit: orphan member_ids in sales with no customer row (the query above); count them; cross-check against the broken-key count in your Chapter 9 log — one story, two tools, same numbers.
4. Fan-out on purpose: create a tiny `customer_discounts` table (DB Browser → Create Table) with two rows for one member; join sales to it; watch revenue double; then fix it by aggregating discounts to one row per customer before joining. Log both revenue totals — this pair of numbers is the lesson.
5. Diagram drill: draw the four-table boxes-and-lines picture of Tariro's schema (customers, sales, stock, suppliers) with arrowheads at the "many" ends; hand your diagram to a friend and have them read the relationships back to you from the picture alone.

## Further Reading

- Chapter 18 (CTEs — "aggregate, then join" made easy), Chapter 34 (merge — this chapter in pandas)
- Appendix A (join patterns incl. FULL OUTER and self-joins)
