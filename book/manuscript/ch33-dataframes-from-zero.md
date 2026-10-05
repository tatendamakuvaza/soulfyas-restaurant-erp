# Chapter 33: DataFrames from Zero

*Part V — Python: From Zero to Dangerous*

> "A DataFrame is a spreadsheet that obeys orders exactly, remembers everything you did, and never detaches a column in a sort."

### In this chapter you will learn

- The DataFrame and Series: pandas' two objects, and how they relate to what you know.
- Loading Tariro's four CSVs — with the loading checks, now as code.
- Inspecting properly: head, info, describe, value_counts — the four instruments.
- Selecting: columns, rows by name and by boolean — the WHERE of pandas.
- Creating columns: the derived features that turn raw data into analysis material.

## 33.1 Two Objects

pandas has exactly two objects to learn, and both are old friends in new clothes:

- A **Series** is one column: a labelled list — `sales["amount"]` — with all of Python's arithmetic applied *to the whole column at once* (the vectorised way, Chapter 32).
- A **DataFrame** is the table: a dict of Series sharing an index — `sales` itself.

The **index** is the row-labels (0, 1, 2... by default) — a built-in row identity that survives sorts and filters and becomes genuinely powerful with dates (Chapter 34's time series). For now: know it exists, notice the bold numbers on the left, and let `.loc` (below) be your respectful way of addressing it.

```python
import pandas as pd

sales = pd.read_csv("sales.csv")       # the load
customers = pd.read_csv("customers.csv")
stock = pd.read_csv("stock.csv")
suppliers = pd.read_csv("suppliers.csv")
```

Four loads, four tables, the whole shop in memory — and unlike a spreadsheet, these are *values*, not views: nothing moves unless you say so.

## 33.2 The Loading Checks, as Code

Project 2's loading liturgy — row counts, key census, orphan check, totals, NULL census — was a checklist in a log; in pandas it is *code that checks*, which means it runs itself every month:

```python
# row counts -- the log writes itself
print(f"sales rows: {len(sales)}")
print(f"customers rows: {len(customers)}")

# key census: duplicate customer_ids must be zero
print(customers["customer_id"].duplicated().sum())      # 0

# orphan check: sales' ids that match no customer (non-members excluded first)
orphan = sales.loc[sales["customer_id"].notna()
                   & ~sales["customer_id"].isin(customers["customer_id"])]
print(f"orphan sales: {len(orphan)}")

# the totals bridge -- reconciles to Part II's workbook, to the cent
print(f"total revenue: {sales['amount'].sum():,.2f}")   # 54,013.50

# NULL census, with meanings
print(sales["customer_id"].isna().sum())    # non-member sales
print(sales["amount"].isna().sum())         # must be 0 -- or a story
```

Read each line and find the Part II–III habit it mechanises: `.duplicated().sum()` is the key census; `~ .isin()` is the anti-join; `.isna().sum()` is the NULL census; the total is the bridge. **The checks you used to perform, your code now performs** — that is the whole meaning of "from zero to dangerous": the discipline becomes ambient.

## 33.3 The Four Instruments of Inspection

The four methods that open any new table, in the order you run them:

```python
sales.head()          # the first five rows -- eyeball the columns, spot obvious trouble
sales.info()          # every column: type, non-null count -- the schema, free
sales.describe()      # numeric summary -- the five numbers plus count/mean/std
sales["payment_type"].value_counts()      # the categorical summary -- counts per value
```

`info()` deserves its own sentence: it prints each column's **dtype** (`int64`, `float64`, `object` — the last is usually text, *sometimes a date that failed to parse, sometimes numbers with a stray letter in them*). "Column of 6,420 with 300 nulls and dtype object that should be float" — that one line of `info()` output is the entire data-quality conversation of Chapter 8, printed automatically. And `value_counts()` is the frequency table for *any* categorical column, normalising with `normalize=True` for shares — `sales["payment_type"].value_counts(normalize=True)` is the payment-mix pie, minus the pie.

## 33.4 Selecting: the WHERE of pandas

Selection has two gears, and both matter. **By name** (columns with `[...]`, rows by label with `.loc`):

```python
sales["amount"]                       # one column (a Series)
sales[["date", "amount"]]             # two columns (note the double brackets)
sales.loc[0]                          # the row labelled 0
sales.loc[10:15, ["date", "amount"]]  # rows 10-15, those columns
```

**By condition** (the boolean, powering a filter — the gear you will use daily):

```python
sales[sales["amount"] >= 50]                          # big baskets
sales[sales["payment_type"] == "EcoCash"]             # one payment type
sales[(sales["amount"] >= 50) & (sales["till"] == 2)] # AND -- note the parentheses!
```

Two syntax landmines, both famous: **combine conditions with `&` / `|` (not `and`/`or`)** and **wrap each condition in parentheses** — `and` on Series is a `ValueError` with a helpful message, and you will meet it once, exactly once. And the date-range filter, pandas' daily bread:

```python
sales["date"] = pd.to_datetime(sales["date"])         # parse once (see 33.5)
june = sales[(sales["date"] >= "2025-06-01") & (sales["date"] <= "2025-06-30")]
```

SELECT, WHERE, and BETWEEN — Chapter 15, wearing different brackets. (There is also `.query('amount >= 50 and till == 2')` — SQL-flavoured selection, almost a dialect pun; use whichever your team reads better.)

## 33.5 New Columns

Analysis begins when raw columns become *features*. A new column is an assignment over the whole column at once:

```python
# parse the date properly (info() showed object -- fix it on load, always)
sales["date"] = pd.to_datetime(sales["date"])

# derived features, vectorised
sales["month"] = sales["date"].dt.to_period("M")       # 2025-06 -- grouping key
sales["weekday"] = sales["date"].dt.day_name()          # "Saturday"
sales["is_weekend"] = sales["weekday"].isin(["Saturday", "Sunday"])
sales["is_whale"] = sales["amount"] > 21.50             # the Part II fence
sales["basket_class"] = sales["amount"].apply(
    lambda a: "whale" if a > 21.50 else ("big" if a >= 10 else "small"))
```

Three idioms in that block, in ascending order of power: **arithmetic/boolean over columns** (`is_whale` — the fastest, use it whenever possible); **`.dt` and `.str` accessors** (`dt.day_name()`, `str.upper()`, `str.strip()` — the cleaning chapter *inside* the column: `sales["payment_type"].str.strip().str.upper()` is the three-EcoCash-solutions fix, permanently); and **`.apply()`** with a `lambda` — a per-row function when no column-level idiom fits (the loop of Chapter 32, wearing a suit; use it *last*, because it is the slowest and the least searchable).

The craft rule that ends the chapter: **every new column is an assumption made visible**. `is_whale` hard-codes the 21.50 fence — better written as a named constant and commented (the argument-defaults lesson): `WHALE_FENCE = 21.50  # 1.5 x IQR, Part II`, then `sales["amount"] > WHALE_FENCE`. Your columns are your analysis's load-bearing walls; label the load.

> **From Your Toolkit — the table, finally programmatic:** the DataFrame is the object the whole rest of this book manipulates: Chapter 34 analyses it, Chapter 35 draws it, Chapter 36 tests it, Chapter 37 schedules it, Chapter 39 exports it to Power BI, and Chapter 58 learns from it. Everything a spreadsheet *is*, it is — minus the fragility, plus the audit trail: a notebook re-run is proof the table was built the same way twice.

## Key Takeaways

- Series = one labelled column; DataFrame = the table; the index is row identity.
- The loading checks become code: duplicated(), ~isin() (anti-join), isna().sum(), the totals bridge — discipline mechanised.
- The four instruments: head (eyeball), info (dtypes and nulls — the schema free), describe (numbers), value_counts (categories).
- Select by name ([...] / .loc) or by condition (booleans; `&`/`|` with parentheses; .query() as the SQL pun); dates parse once with to_datetime.
- New columns are vectorised first (.dt/.str second, .apply last); every column is an assumption — name its constants and comment its loads.

## Practice Lab

1. The four loads + full loading-checks block on all four of Tariro's tables; reconcile revenue and row counts against your Project 2 log; paste the printed check output into a Markdown cell as the audit page.
2. The instrument sweep: head/info/describe/value_counts on `customers`; find one dtype surprise or NULL story per table (there are planted ones); write the four findings in four bullets.
3. Selection drills, all reconciled against SQL you wrote in Part III: (a) the ten biggest sales (`sort_values` + `head(10)`), (b) June EcoCash sales, (c) weekend member sales with amount ≥ 50 — for each, also write the equivalent SQL in a Markdown cell and note the comparison.
4. The cleaning column: build `payment_clean` from `payment_type` with `.str.strip().str.upper()`, then `value_counts()` before and after — the three-EcoCash story in two output blocks; document which rows changed.
5. The feature shelf: add `month`, `weekday`, `is_weekend`, `is_whale` (with the named constant), and `basket_class`; then produce one finding per new column (e.g., weekend share of revenue; whale share of transactions vs revenue) — each as a sentence with its f-string.

## Further Reading

- Chapter 34 (groupby, merge, time series — the power moves), *Python for Data Analysis* ch. 5
- pandas' "10 minutes to pandas" — the official tour, painless after this chapter
