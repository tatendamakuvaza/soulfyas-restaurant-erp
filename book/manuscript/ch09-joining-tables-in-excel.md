# Chapter 9: Joining Tables in Excel

*Part II — Excel: Your First Superpower*

> "A join answers a question one table cannot: 'who are these people, and what else do we know about them?'"

### In this chapter you will learn

- Why joins exist, in plain words, and the key idea that makes them work.
- VLOOKUP and XLOOKUP — the spreadsheet join, step by step.
- INDEX-MATCH: the classic upgrade, and why analysts still love it.
- The errors: #N/A, and what it is trying to tell you.
- The trap that multiplies money: the fan-out, seen here first.

## 9.1 The Question One Table Cannot Answer

Tariro asks her fifth question early, because a loyalty-card promotion is due: *"How much do my loyalty members actually spend, compared to everyone else?"* The sales table knows the spending but only records a membership code. The customers table knows the members — their suburbs, join dates, ages — but not what anyone spent. The answer lives in **both tables at once**, and the act of combining them is the single most important data operation in this book: the **join**.

The idea that makes joins possible is almost embarrassingly small: both tables carry a **key** — a column whose values identify the same thing in each. Here it is `member_id`: every loyalty sale row carries one, and every customer row is one. The join is "for each sale, find the customer row with the same member_id, and bring that row's facts across". Every join you ever run — in Excel today, SQL in Chapter 17, Python in Chapter 34, Power BI in Chapter 39 — is this sentence in a different accent.

## 9.2 VLOOKUP: The Workhorse

In your clean sales sheet, add a column: "suburb". Then, in the first data row:

```text
=VLOOKUP(G2, customers!A:E, 3, FALSE)
```

Read it as a sentence with four parts: *look up* the value in G2 (this sale's member_id), *inside* the customers table (columns A to E), *bring back* column 3 of the matching row, and be *exact* about it (FALSE means exact match — always FALSE; TRUE is approximate-match, a setting with a dark side this book will not let you use on keys).

Fill it down and every sale row now knows its customer's suburb: the join, done, in one formula. The modern **XLOOKUP** says the same thing more naturally — `=XLOOKUP(G2, customers!A:A, customers!C:C, "no match")` — and its fourth argument is the error handler we want next.

## 9.3 #N/A Is a Message

Some rows will show `#N/A`: the lookup found no match. Before you treat it as noise, read it — it is one of exactly three real situations:

1. **Genuine non-members** — many sales have no loyalty card at all; "not found" is correct and should become a clean label ("non-member"), not an error.
2. **A spelling or type mismatch** — the member_id "M0012 " (trailing space, Chapter 8's ghost) does not match "M0012". This is a data flaw, and the fix is TRIM, not the formula.
3. **The key itself is wrong** — a member_id in sales that exists in no customer row: a data-quality finding for Tariro's till.

The professional habit: wrap the lookup — `=IFNA(VLOOKUP(...), "no match")` — so the error becomes a label you can *count*, and then count it: 200 no-matches is a story (mostly non-members); 20,000 is a broken key. Chapter 2's skepticism, in formula form.

## 9.4 INDEX-MATCH: The Classic

Before XLOOKUP existed, analysts swore by INDEX-MATCH, and you will meet it in older workbooks on your first job, so you must read it:

```text
=INDEX(customers!C:C, MATCH(G2, customers!A:A, 0))
```

Sentence: *MATCH* finds the row number where G2 appears in the id column (the `0` means exact); *INDEX* returns the value at that row in the suburb column. Two functions doing VLOOKUP's one job — but robustly: insert a column in customers and VLOOKUP's "column 3" silently becomes the wrong column, while INDEX-MATCH keeps aiming at what you named. Robustness by naming, not by position, is a professional instinct that follows you into SQL (where *naming* is the only way anything is ever joined).

## 9.5 The Trap: Fan-Out

One warning now, planted here because seeing it in a spreadsheet is the cheapest education you will ever get. Suppose instead of one sale per row, Tariro's export had one **line item** per row, and you joined it to a *monthly* discount table — one row per member per month. A member with 40 line items in a month now matches... 40 rows of sales × the month's single discount row? No — the direction that bites is the reverse: joining a many-row side to a table that *also* has many rows for the same key (say, two rows for one member: one old address, one new) **multiplies**: every sale matches *both* rows, and revenue silently doubles.

The spreadsheet version of the defence is the sanity check: **after any join, verify that a total you knew before (total revenue) is unchanged**. If revenue moved, you did not join — you duplicated. This exact trap, named **fan-out**, is the most common way real analysts corrupt real numbers on real jobs, and it is why the totals-reconciliation habit from Chapter 8 becomes a reflex here. When SQL formalizes joins in Chapter 17, you will meet it again with better tools — and recognise it instantly, which is the point.

> **From Your Toolkit — future joins:** Excel's lookup is a *column-by-column* join; SQL's JOIN (Chapter 17) does whole tables at once with explicit directions (left, inner); pandas' `merge` (Chapter 34) is SQL's join in Python clothing; Power BI's data model (Chapter 39) draws the join as a line between tables you click once and reuse forever. Four accents, one sentence: *match the keys, bring the facts across, check the totals.*

## Key Takeaways

- A join combines two tables on a shared key — one row per thing, matched, facts brought across.
- VLOOKUP/XLOOKUP do the spreadsheet join; always exact-match on keys; INDEX-MATCH survives column insertions.
- #N/A is a message: non-member, spelling mismatch, or broken key — count it, don't hide it.
- Fan-out is the money trap: joins can duplicate rows; totals must reconcile after every join or you copied, not joined.
- Four tools will speak this chapter; the sentence never changes.

## Practice Lab

1. Join sales to customers on member_id with XLOOKUP or VLOOKUP+IFNA; label non-members; and count the three kinds of #N/A (genuine, trimmable, broken key) in your log.
2. The comparison answer: average sale amount for members vs non-members — Tariro's fifth question has its first number. Write the two-line answer for her, including the Chapter 2 caveat that members may always have been bigger spenders.
3. INDEX-MATCH rebuild: replace your VLOOKUP with INDEX-MATCH in a copy, then insert a column in customers and watch which formula survives. Write one sentence on why.
4. Fan-out, safely: build the trap on purpose — a tiny two-table example where one member has two customer rows — and watch revenue double; then fix it by deduplicating the lookup side first. (You will never forget it now.)
5. The key audit: count distinct member_ids in sales that appear in customers, and vice versa; write down what each direction's missing ids mean in business words.

## Further Reading

- Chapter 10 (PivotTables — analyse the joined table), Chapter 17 (SQL joins — the same chapter, grown up)
- Excel help: "VLOOKUP troubleshooting" — every listed cause is a section of this chapter in miniature
