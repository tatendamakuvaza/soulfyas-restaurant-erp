# Chapter 20: SQL in Real Life

*Part III — SQL: The Language of Data*

> "In real jobs, nobody gives you an empty editor and a polite question. They give you a database you didn't design, a query named 'final_v3_John_old', and a deadline."

### In this chapter you will learn

- The databases you will actually meet at work, and how to connect to them.
- The queries you will actually write — the working analyst's top patterns.
- Reading and repairing inherited SQL — a survival method.
- Performance in three habits: why is it slow, EXPLAIN, and the indexing idea.
- SQL etiquette: saving, naming, commenting — how your queries will be judged.

## 20.1 The Databases You Will Meet

SQLite taught you the language; at work the engine will almost always be a **server database** — the same relational model, reached over a network. The names to know, so meeting them is recognition rather than surprise:

| Database | Where you'll meet it | Notes for you |
|---|---|---|
| PostgreSQL | Modern product/backend teams; the analyst favourite | Free, strict, standards-loving — a pleasure to inherit |
| MySQL / MariaDB | Websites, smaller product stacks | Ubiquitous; dialect quirks around dates |
| SQL Server (Microsoft) | Finance, corporates, anything already Microsoft | Pair with SSMS, the classic workbench; T-SQL dialect |
| Oracle | Banks, insurers, governments | Ancient, powerful, fond of ceremony |
| BigQuery / Snowflake / Databricks | "Data warehouse" / analytics teams (Chapter 57's world) | Billions of rows; SQL-as-a-service; cost-aware querying |

Two practical consequences. First, **dialects**: 90% of your SQL transfers unchanged, but dates, string functions, and NULL handling vary at the edges (`substr` vs `SUBSTRING`, `LIMIT` vs `TOP` vs `FETCH FIRST`); Appendix A carries the translation table, and every engine's docs have a "SQL dialect" page you read once. Second, **connection tools**: at work you will not browse the database in DB Browser but in a workbench — SSMS, DBeaver, Azure Data Studio, the warehouse's own web SQL editor — and connecting is the first-day task: host, port, database, your credentials, and (the realistic part) asking a colleague which of the 400 schemas is the real one. Asking is not a beginner's weakness; it is the professional's first move.

## 20.2 The Queries You'll Actually Write

Five years of an analyst's SQL rounds down to a short list — you know every piece of it now:

1. **Filtered extraction** — `SELECT ... WHERE date BETWEEN ... AND ...` — "pull last month's orders for the western region". (Chapter 15.)
2. **Grouped summaries** — `GROUP BY` with COUNT/SUM/AVG, HAVING for busy groups. (Chapter 16.)
3. **Enrichment joins** — LEFT JOIN a dimension table onto a fact table; the anti-join for what is missing. (Chapter 17.)
4. **Layered analysis** — CTE pipelines: share-of-total, month-over-month, top-N-per-group. (Chapters 18–19.)
5. **Data-quality sweeps** — COUNT(*) vs COUNT(column), GROUP BY a key with HAVING COUNT(*)>1 (duplicates), the orphan anti-join, NULL censuses. (Chapters 8 and 15–17, in SQL.)

Notice what is *absent*: noINSERT-every-day, no schema surgery, no stored procedures — those are engineers' work. The analyst's SQL is reading, aggregating, joining, and checking — which is why Part III could teach it in eight chapters, and why "strong SQL" on a CV (Chapter 53) means exactly this list, fluent.

## 20.3 Inherited SQL

You will spend more time reading SQL than writing it. The survival method, assembled from everything you now know:

1. **Diagram the FROM first** (Chapter 17): tables, aliases, join lines, INNER vs LEFT, which side is many. The picture is half the meaning.
2. **Walk the execution pipeline** (Chapter 16): WHERE → groups → HAVING → SELECT. Mark which columns are filters, which are aggregates.
3. **Peel the layers** (Chapter 18): if it is CTEs, run each one alone; if it is nested subqueries, rewrite the innermost as a CTE on a scratch copy — the rewrite is itself the reading.
4. **Suspect the usual criminals** when results look wrong: an INNER JOIN that amputated rows (should have been LEFT), a fan-out doubling totals (keys repeating both sides), a WHERE on a LEFT-joined table that silently turned it into an INNER (the classic: `LEFT JOIN c ... WHERE c.suburb = 'Avondale'` discards NULL rows — move the condition into the ON clause or accept INNER deliberately), and `SELECT *` in a GROUP BY that some dialects forgive and others refuse.
5. **Change nothing until you can reconcile it**: run the old query, save its totals, change, compare. Inherited SQL is under nobody's tests except yours.

## 20.4 Slow Queries: Three Habits

Sooner than you think, a query takes ninety seconds and someone is watching.

- **Read the shape before the engine does.** `WHERE substr(date,1,7) = '2025-06'` forces the engine to compute substr for every row; `WHERE date >= '2025-06-01' AND date < '2025-07-01'` lets it *seek*. Functions on columns hide values from optimisation — the habit is *sargability*: keep columns bare, put the transformation on the constant side.
- **EXPLAIN (QUERY PLAN)** before the engine spends your patience: prefix any query with `EXPLAIN` and the engine prints its plan — which tables it scans fully, which it seeks, how it joins. You are not expected to read it like a database engineer; you are expected to notice "full table scan on a 40-million-row table" and think "ah".
- **The indexing idea.** An index is a lookup structure the engine maintains so key-lookups and range filters do not read the whole table — the database equivalent of a book's index, and the reason joins on keys are fast. You will rarely create indexes as an analyst; you will benefit from them existing, and occasionally ask a friendly engineer (with the EXPLAIN output in hand) whether one is missing. Asking with evidence is the professional form.

## 20.5 Etiquette: How Your SQL Is Judged

Your queries will be read by colleagues and successors; the craft norms are small and heavily rewarded:

- **Name files for the question** (`monthly_revenue_by_till.sql`, not `query12.sql`), and version by copy or git — never `final_v2`.
- **Comment the why, not the what**: `-- exclude whales: bulk buyers analysed separately (see report p.2)` is a comment; `-- select from sales` is noise.
- **A header block** on anything saved: purpose, author, date, source tables, and — the mark of trust — *the expected row count or total when you last ran it*, so the next runner can reconcile before trusting (the habit of this entire book, in five lines).
- **Format deliberately**: one clause per line, aliases aligned, CTEs named for the story. Formatting is documentation that never goes stale.

> **From Your Toolkit — the working set:** everything in this chapter is tool-independent: the engines change, the workbenches change, but extraction, grouping, joining, layering, auditing, and etiquette are the job. When Part VI connects Power BI to a warehouse, it will be this chapter's connection habits; when Part VII's portfolio projects ship, they will carry this chapter's header blocks. The language is learned; the profession is these habits.

## Key Takeaways

- Server databases (Postgres, MySQL, SQL Server, Oracle, warehouses) share the model; dialects differ at the edges; connecting is a first-day task — ask which schema is real.
- The working analyst writes five shapes of SQL: extract, group, join, layer, audit — you know them all.
- Read inherited SQL by diagramming FROM, walking the pipeline, peeling layers; suspect INNER-amputation, fan-out, and WHERE-on-a-LEFT; reconcile before you change.
- Performance: keep columns bare in WHERE (sargability), EXPLAIN before blaming, know what an index is for.
- Name for the question, comment the why, header with expected totals — your SQL is your handwriting.

## Practice Lab

1. The dialect drill: rewrite three of your saved queries in a second dialect (e.g. SQLite → SQL Server: `LIMIT` → `TOP`, `substr` → `SUBSTRING`); note each difference in a dialects.txt — the start of your personal translation table (Appendix A has the official one).
2. The inheritance, simulated: take your Chapter 18 share-of-total query, rename everything cryptically (`q1`, `t1`, `x`), remove the comments, and hand it to a friend (or your future self, three days); time the explanation-back. Then restore names and comments and repeat. Log both times.
3. The sargability lab: run both date filters on your sales table (substr vs range) and EXPLAIN QUERY PLAN each; write down what differs in the plans, and the rule you'll follow from now on.
4. The criminal line-up: deliberately commit the four sins — INNER where LEFT was needed, a fan-out join, WHERE on a LEFT-joined table, `SELECT *` with GROUP BY — and for each, note the wrong number it produced and the check that caught it. This is the most valuable page in your log so far.
5. The professional file: pick your five most useful queries from all of Part III; give each the full treatment (filename, header block with expected totals, comments-for-why, formatting); store them in a `queries/` folder — they are the seeds of your portfolio's SQL evidence (Chapter 46).

## Further Reading

- Chapter 21 (Project 2 — all of Part III assembled), Chapter 57 (the warehouse world: BigQuery, Snowflake, lakehouse)
- Use The Index, Luke (use-the-index-luke.com) — indexing and sargability, friendly and deep
