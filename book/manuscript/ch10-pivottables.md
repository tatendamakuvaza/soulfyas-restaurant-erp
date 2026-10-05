# Chapter 10: PivotTables — The Analyst's Best Friend

*Part II — Excel: Your First Superpower*

> "A pivot table is a question you can twist: drop the numbers in, turn the handle, watch the table reorganise itself around a new question."

### In this chapter you will learn

- The PivotTable in one idea, and the five clicks that build your first one.
- Rows, columns, values, filters — the four shelves, each explained plainly.
- The rearrangements: share-of-total, month grouping, and the drill-down.
- Reading a pivot like an analyst: where the planted patterns hide.
- The limits that send you to SQL later — and why that is fine.

## 10.1 The One Idea

You now have a clean sales table with customer facts joined on. Tariro's questions are all of the form *"totals of something, for each something else"* — revenue by month, sales by category, average basket by payment type, weekday versus weekend. A **PivotTable** is the tool that answers every question of that form *without formulas*: you tell it which facts to sum (values), which groups to sum them by (rows and columns), and which slices to hold aside (filters), and it builds the summary table. One pivot, re-twisted five ways, is a whole monthly report — this is why working analysts call it the best friend, and why interviews test it (Chapter 52).

## 10.2 Five Clicks to Your First Pivot

On your clean, single-table sheet (one table per sheet, headers in row 1 — Chapter 6's rules are load-bearing here; pivots are strict about hygiene):

1. Click any cell inside the table.
2. Insert → PivotTable (LibreOffice: Insert → Pivot Table). Accept the defaults (new sheet).
3. The field list appears: every column of your table, waiting. Drag **`category`** into **Rows**.
4. Drag **`amount`** into **Values** (it arrives as "Sum of amount" — exactly what we want).
5. Look: total revenue for every product category, in one table, zero formulas.

Then the twist that names the tool: drag **`payment_type`** into **Columns**. The table re-pivots — revenue by category *and* by payment type in a cross-tab. Drag it out, drag `date` into Rows instead — and when a date arrives, the pivot usually groups it by month/year automatically (if not: right-click the date → Group → Months). Revenue by month appears: the line behind Tariro's bank-manager chart, six clicks in.

## 10.3 The Four Shelves

| Shelf | Plain English | Example |
|---|---|---|
| Rows | "one row for each..." | category, month, item |
| Columns | "...and one column for each..." | payment type, suburb |
| Values | "show me the total/average/count of..." | Sum of amount, Average of amount, Count of rows |
| Filters | "only look at..." | one suburb, one month, members only |

Two details that double your power. **Values can be re-aimed**: click on "Sum of amount" and switch to Average, or Count — the same shelf answers "how much?", "how big typically?", "how many?". **Values can be stacked**: drop `amount` twice, set one to Sum and one to Count, and you have revenue *and* transaction counts side by side — divide them (a small formula beside the pivot) and you have average basket, the number every retailer breathes by.

And the analysis trick that feels like magic the first time: **double-click any number in the pivot** — the rows behind that number open as a new sheet. That "18,400 in March cooking oil" is now a list of the actual sales. This is the drill-down, and it is how pivots stay honest: every summary can be exploded back into its evidence.

## 10.4 Reading a Pivot Like an Analyst

Build the weekday question (Tariro's Sunday question deserves a first look here, properly settled in Part IV): `date` grouped by month in Rows — no: for weekdays, make a helper column first, `=TEXT(A2, "ddd")` (the day name), then pivot by it. Now read the table with Chapter 2's habits:

- **Compare, don't just see**: Friday and Saturday totals tower — but *by how much*? Switch Values to "Show Values As → % of Column Total": now the share of the week is explicit, and "the weekend is a third of everything" is a sentence you can defend.
- **Look for the plants**: payday spikes (compare the last week of each month's rows), the month-9 cooking-oil dip (category × month pivot), the loyalty share (member vs non-member columns on any measure).
- **Small categories lie quietly**: a category with 3 sales can show a spectacular average basket. Count and sum, side by side, always — the pairing habit that prevents nonsense.

## 10.5 Where Pivots End

Honest limits, so you know what Chapter 14 starts: pivots on a laptop get slow past a few hundred thousand rows; they do not *remember* the steps (redo the drag-dance monthly — until Chapter 37 automates it); they cannot join many tables at once (Chapter 39's data model does); and their "refresh" is manual (Data → Refresh — the button everyone forgets before the Monday meeting, once, and never again).

None of this subtracts from the friend. For the questions of a business Tariro's size — and, honestly, most businesses — the pivot is the analysis, and the rest is presentation.

> **From Your Toolkit — the same shelves everywhere:** SQL's `GROUP BY` (Chapter 16) is the pivot's Rows shelf with values beside it; pandas' `.groupby()` (Chapter 34) is the same shelves in code; Power BI's whole visual system (Part VI) is a pivot per chart. When you meet each one, translate back to these four shelves and nothing in this book will ever feel new — only re-accented.

## Key Takeaways

- The pivot answers every "totals of X by Y" question without formulas: five clicks, then twist.
- Four shelves: rows, columns, values (re-aimable and stackable), filters.
- Double-click any pivot number to explode it back into its rows — summaries stay honest.
- Read like an analyst: % of total for shares, sum beside count for trap-catching, and compare before concluding.
- Limits (size, memory, joins) are real and are exactly what SQL, Python, and Power BI are for.

## Practice Lab

1. Build the category × payment_type revenue pivot; then re-twist to month × category; write the three sentences each table tells Tariro (planted patterns included).
2. Day-of-week pivot with the TEXT helper column: totals, then % of column, then Sum and Count side by side with an average-basket column beside them. Write your first — explicitly unofficial — verdict on Sundays.
3. The members pivot: revenue and counts by member vs non-member (Chapter 9's join feeding the values); note the share loyalty members take, and the caveat you must attach.
4. Drill-down audit: explode the biggest cell in your category pivot back to rows; find its largest single sale; write the two lines that connect summary to evidence.
5. The refresh lesson: change one amount in your source table, refresh the pivot, and record what did and did not change in your log — the habit that saves a Monday meeting.

## Further Reading

- Chapter 11 (charts — the pivot's findings get their picture), Chapter 16 (GROUP BY — this chapter in SQL)
- Any "pivot table" tutorial video, ten minutes — use it to review the shelves, then twist a pivot no video suggests.
