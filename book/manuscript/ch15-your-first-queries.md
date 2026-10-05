# Chapter 15: Your First Queries

*Part III — SQL: The Language of Data*

> "SQL is the closest thing data has to a lingua franca: one small grammar, spoken by every database on Earth."

### In this chapter you will learn

- What SQL is and why it has ruled for fifty years.
- The first query — SELECT, FROM — and reading a table in the language.
- Narrowing with WHERE, ordering with ORDER BY, limiting with LIMIT.
- Text, numbers, and dates in WHERE — the comparison habits that do 80% of the work.
- NULL: the value that is not a value, and why SQL is strict about it.

## 15.1 The Language

SQL — Structured Query Language, pronounced "sequel" or "ess-cue-ell"; both are fine, arguments are a hobby — is how you ask a relational database questions. You describe the result you want; the engine decides how to fetch it. You do not loop, you do not hunt cell by cell: you *declare*. That declarative style is why SQL has survived every fashion since 1974 — and why, alone of the tools in this book, SQL appears in some form in virtually every data job posting you will ever read (Chapter 50's numbers).

The grammar fits on a napkin. Every query in this chapter is built from five keywords:

```sql
SELECT column, column   -- what you want back
FROM table              -- from which table
WHERE condition         -- which rows only
ORDER BY column         -- in what order
LIMIT n;                -- how many rows
```

Type these into DB Browser's **Execute SQL** tab (your `tariros.db` from Chapter 14, sales imported) and press the run button. Welcome to the language.

## 15.2 SELECT and FROM

The simplest honest query — all of it, every column, every row:

```sql
SELECT * FROM sales;
```

The asterisk means "every column" — fine for a first look, bad as a habit: real tables are wide, real queries name their columns, and naming is documentation. The professional form:

```sql
SELECT sale_id, date, till, amount
FROM   sales;
```

Column order is yours to choose; duplicates are removed if you ask (`SELECT DISTINCT payment_type FROM sales;` — three payment types, one query, no pivot needed). SQL keywords are conventionally UPPERCASE and SQL does not care about case for keywords, but *does* care about your data's case: 'Ecocash' and 'ecocash' are different values (the cleaning chapter's ghost, now with teeth).

## 15.3 WHERE: Choosing Rows

WHERE keeps only the rows that pass a test, and the tests are the arithmetic you already know: `=`, `<>` (not equal), `<`, `<=`, `>`, `>=`.

```sql
-- one day's takings, both tills
SELECT * FROM sales WHERE date = '2025-06-14';

-- the big baskets
SELECT sale_id, date, amount FROM sales
WHERE amount >= 50;

-- everything except the bulk-order whale
SELECT * FROM sales WHERE sale_id <> 4123;
```

Text takes quotes, numbers do not — `'Ecocash'` is a value, `50` is a number, and mixing the habits is the first bug everyone writes. Dates take ISO quotes (`'2025-06-14'`) — year-month-day, the unambiguous international form; Chapter 8's date hygiene pays its first dividend here, because a database will *refuse* the ambiguous, which is exactly what you want.

The combiners, and the parentheses that make them safe:

```sql
-- cash sales over 20 dollars -- AND means both must hold
SELECT * FROM sales
WHERE payment_type = 'Cash' AND amount > 20;

-- weekend rows -- OR means either holds
SELECT * FROM sales
WHERE weekday = 'Sat' OR weekday = 'Sun';

-- a range, written either way
SELECT * FROM sales
WHERE date >= '2025-06-01' AND date <= '2025-06-30';

SELECT * FROM sales
WHERE date BETWEEN '2025-06-01' AND '2025-06-30';
```

And the one that replaces a hundred spreadsheet filters — the membership test:

```sql
SELECT * FROM sales
WHERE payment_type IN ('Cash', 'EcoCash', 'Card');
```

## 15.4 ORDER BY and LIMIT

ORDER BY sorts the result — `ASC` (default, smallest first) or `DESC` (largest first) — and it can sort by several keys in sequence: `ORDER BY amount DESC, date ASC` ranks sales by size and breaks ties by date. LIMIT caps the rows returned, which turns any query into a top-list:

```sql
-- the ten biggest sales in eighteen months
SELECT sale_id, date, amount
FROM   sales
ORDER BY amount DESC
LIMIT  10;
```

That query — biggest, smallest, first, latest, top N — is in every analyst's daily rotation; ten rows and the whale hunt from Chapter 12 is already underway. Together with WHERE it completes the working core: **choose the rows (WHERE), choose the columns (SELECT), choose the order (ORDER BY), cap it (LIMIT)** — the grammar of "look".

## 15.5 NULL: Not Zero, Not Blank

One SQL idea has no spreadsheet twin and must be learned properly: **NULL** — a value that means *unknown or absent*. Not zero (zero is a known amount: a free item, a voided sale); not an empty string (which is a known nothing). NULL is the database saying "this fact is missing". Tariro's data carries them honestly: non-member sales have NULL customer_id; the three missing stock weeks are NULL rows, not zero rows — a distinction Chapter 23's statistics and Chapter 25's sampling will lean on.

The trap that catches every beginner: **NULL fails every comparison**. `WHERE customer_id <> 'C0102'` does *not* return the rows where customer_id is NULL — unknown is not unequal, it is unknown. The test is its own keyword:

```sql
SELECT * FROM sales WHERE customer_id IS NULL;     -- the non-members
SELECT * FROM sales WHERE customer_id IS NOT NULL; -- the members
```

Count both. The NULL discipline — know them, name them, choose deliberately whether they are excluded — is a marker of professional SQL, and interviewers probe it deliberately (Chapter 52).

> **From Your Toolkit — one grammar, five tools:** this five-keyword core is the same SQL spoken by Python's pandas (`.query()`, Chapter 34), spoken *to* Power BI's data model (Chapter 39), and shadowed by spreadsheet filters. Master `SELECT–FROM–WHERE–ORDER BY–LIMIT` and you can read half of every code example in the rest of this book — and, one day, half of the queries left behind by the analyst whose job you inherit.

## Key Takeaways

- SQL is declarative: describe the result, the engine fetches — five keywords do the looking.
- Name your columns; `SELECT *` is for exploring, not for delivering.
- Text and dates take quotes (ISO dates), numbers don't; AND/OR/IN/BETWEEN with parentheses do the choosing.
- ORDER BY + LIMIT = top-lists and whale hunts; sort is cheap and reversible.
- NULL is unknown, not zero — it fails every comparison; test with IS NULL, and count what you exclude.

## Practice Lab

1. The first five: run `SELECT * FROM sales LIMIT 5`, then name your columns; then write queries for the ten biggest sales, the ten smallest, and the first five sales Tariro ever recorded (ORDER BY date ASC).
2. The day report: one query for all sales on the most recent Saturday, ordered by amount descending; another for that day's Ecocash sales only; reconcile both totals against a pivot of the same day in your workbook — the numbers must match, or write down why.
3. The membership split: count NULL and non-NULL customer_id rows (two queries with IS NULL); write the sentence comparing your counts to the "no match" labels from Chapter 9's join — they should tell one story.
4. The range habit: sales in the last full month three ways — two comparisons with AND, BETWEEN, and one IN list of dates; confirm all three return the same row count.
5. Whale hunt, sequel: amounts over the Chapter 12 fence (21.50) with ORDER BY DESC; paste the top ten into your log and annotate the bulk buyers you already know by name.

## Further Reading

- Chapter 16 (GROUP BY — the pivot, in SQL), Appendix A (the cookbook: every query pattern from this book, ready to copy)
- sqlbolt.com — interactive lessons 1–4 for extra reps of this chapter
