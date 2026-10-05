# Chapter 6: Thinking in Grids

*Part II — Excel: Your First Superpower*

> "Every tool in this book reads the same shape: one row per thing, one column per fact. Learn the shape once here."

### In this chapter you will learn

- The anatomy of a spreadsheet: cells, rows, columns, sheets.
- The single most important rule in all of data work: one row per thing.
- What a CSV is, and why data arrives in them.
- How to open Tariro's data properly (and the one mistake that corrupts dates).
- Grid hygiene: the rules that keep a sheet trustworthy.

## 6.1 The Anatomy

Open LibreOffice Calc or Excel. What you see is a **grid**: columns lettered A, B, C..., rows numbered 1, 2, 3..., and every **cell** named by its crossing — B3 is column B, row 3. Along the bottom, **sheets** (Sheet1, Sheet2...) let you keep related tables in one file. That is the entire furniture of the tool. Everything else in Part II is what you *do* with this furniture.

Two habits make the grid yours immediately. First: **click any cell and read the formula bar** (the long box above the grid) — it shows what the cell really contains, not just what it displays. A cell showing "5" might contain `=2+3`, and knowing the difference is the beginning of analyst sight. Second: **Ctrl+arrow keys jump** — Ctrl+Down from A1 lands on the last filled row. Big data moves fast once you stop scrolling.

## 6.2 The Golden Rule: One Row Per Thing

Here is the rule that every tool, every chapter, and every employer assumes:

> **Each row is exactly one thing; each column is one fact about that thing.**

In Tariro's `sales.csv`, one row = one item sold, one time. The row's columns are its facts: the date, the time, the item's name, how many units, the price, the total. In `customers.csv`, one row = one loyalty member. The rule sounds obvious and is violated everywhere within a week of anyone using a spreadsheet — merged cells for pretty headers, two years of sales in the same row, one column holding both a name and a phone number. Every violation is a small tax paid later, usually by you, usually at a deadline.

The rule's quiet power: **questions become counts**. "How many sales?" = how many rows. "How many items do we sell?" = how many distinct names in the item column. "Revenue" = add up the amount column. Keep the rule and half of analytics is arithmetic on a table.

## 6.3 CSV: Data's Native Costume

The files in your `03-Data/raw/tariro/` folder end in `.csv` — "comma-separated values". A CSV is just a table saved as plain text: the first line names the columns, every following line is one row, and commas mark the column edges. Open `sales.csv` in Notepad (or any text editor) and look — then open it in Calc and see the same data in a grid. Same table, two costumes.

Why this matters: **every tool in this book opens CSVs** — Excel, DB Browser (Part III), Python (Part V), Power BI (Part VI). It is the universal exchange costume of data, and you will both receive and produce thousands of them.

The one classic mistake: opening a CSV by double-clicking can mangle **dates** (the program guesses the format — day-first or month-first — and sometimes guesses wrong) and **leading zeros** (item code "007" becomes 7, silently). The professional habit: open via **File → Open/Import**, look carefully at the preview step it offers, check that dates look like dates and codes kept their zeros, *then* confirm. Thirty seconds of checking beats an afternoon of wondering why March has 31 days of sales in a day column.

## 6.4 Opening Tariro's Data, Properly

The procedure (Calc and Excel are near-identical here):

1. File → Open, choose `sales.csv` from `03-Data/raw/tariro/`.
2. The import dialog appears with a preview of the first rows. Confirm: commas are the separators; the first row is indeed column names (a header).
3. Scan the columns: `date` shows as a date; `item` and `category` as text; `units`, `unit_price`, `amount` as numbers. If anything looks wrong in the preview, fix it *in the dialog* — each column can be told its type explicitly.
4. Confirm, and **immediately Save As** an `.xlsx`/`.ods` file into `03-Data/clean/` — you never edit the raw original (Chapter 4's rule), and working in a copy in the clean folder is the workflow that rule describes.

Now look around the grid with analyst eyes: how many rows (Ctrl+Down)? Eighteen months of sales is tens of thousands of rows — real. What is one row, in one sentence? Write that sentence on the data card you started in Chapter 5; it is the most important line on it.

## 6.5 Grid Hygiene: Five Rules

1. **One table per sheet** — no second table squeezed below the first; the empty rows convince humans, never tools.
2. **Row 1 is headers** — one short, self-explanatory name per column; no merged cells anywhere, ever, for any reason.
3. **No blank rows or columns inside the table** — gaps break sorting, filtering, and every tool that follows.
4. **One kind of thing per column** — a column is a date OR a number OR text; a column of mixed kinds is a bug in waiting.
5. **Notes live beside the table, not inside it** — if you must annotate, do it in a separate sheet called `notes`, with your cleaning log (Chapter 8 makes this a habit).

These five rules are what Chapter 69's professionals call a *data contract* — you are learning it now, in one sheet, so that warehouses later feel like familiar territory.

> **From Your Toolkit — future tools:** the grid rule is the bridge to everything. When SQL's tables arrive (Chapter 14) you will meet the same rows and columns wearing a database; when pandas arrives (Chapter 33) its "DataFrame" is literally this grid, programmable; when Power BI loads (Chapter 39) it asks the same question every tool asks: *what is one row here?* Answer that and the tool works; dodge it and every tool, politely and eventually, breaks.

## Key Takeaways

- The grid is columns (facts) × rows (things); the formula bar shows what a cell really contains.
- The golden rule: one row per thing, one column per fact — questions become counts.
- CSV is the universal costume of data; open it through the import dialog so dates and leading zeros survive.
- Raw is sacred: work on copies in `clean/`, log what you change.
- Five hygiene rules — one table per sheet, row 1 headers, no gaps, one kind per column, notes beside — make every later tool trust your data.

## Practice Lab

1. Open `sales.csv` via the import dialog (dates and zeros checked), save the working copy to `clean/`, and write the one-sentence row definition on your data card.
2. Formula-bar safari: find one cell in the amount column; check what it displays versus what it contains. Find the last row with Ctrl+Down and note the row number — your first "how big is this?" number.
3. Rule audit: find any spreadsheet in your life (or build a tiny fake one) that breaks the five hygiene rules; list each break and what it would cost.
4. The CSV eye: open `customers.csv` in a text editor; identify the header line and describe, in words, what row 10's commas are separating.
5. Make a `notes` sheet in your working file and write your first entry: the date, what you opened, and one thing you checked.

## Further Reading

- Chapter 7 (formulas — the grid starts computing), Chapter 8 (cleaning Tariro's real messes)
- LibreOffice Calc help: "Importing and Exporting CSV" (five minutes, saves you five hours someday)
