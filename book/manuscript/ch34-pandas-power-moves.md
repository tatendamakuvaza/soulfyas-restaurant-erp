# Chapter 34: pandas Power Moves — groupby, merge, time series

*Part V — Python: From Zero to Dangerous*

> "Every analysis in this book so far — pivots, joins, running totals, month-over-month, top-N — arrives in this chapter as one line. All of them. One line each."

### In this chapter you will learn

- `groupby`: the pivot, the HAVING, and the aggregate habit — in one idiom.
- `merge`: Chapter 17's joins, with the fan-out defence built in.
- The time-series kit: resample, rolling, shift — running totals and month-over-month, natively.
- Pipes and method chains: the CTE habit, Python's accent.
- The full re-run: Part II's monthly report analysis, in fifteen lines.

## 34.1 groupby: The One Idiom

The single most-used line in pandas is also the single most-used idea in this book — "totals of something, for each something else":

```python
sales.groupby("payment_type")["amount"].agg(["count", "sum", "mean"])
```

Read it as the sentence it is: *take sales, group by payment_type, take amount, aggregate count/sum/mean.* That is Chapter 16's query and Chapter 10's pivot, simultaneously. The variations you need, each one a Part II–III skill:

```python
# multiple group keys -- the two-shelf pivot (rows x columns, stacked long)
sales.groupby(["month", "category"])["amount"].sum()

# named aggregations -- the query with AS aliases
(sales.groupby("category")
      .agg(revenue=("amount", "sum"),
           n_sales=("amount", "count"),
           avg_basket=("amount", "mean")))

# filter groups -- HAVING, verbatim
by_cat = sales.groupby("category")["amount"].agg(["sum", "count"])
by_cat[by_cat["count"] >= 100].sort_values("sum", ascending=False)

# the top-N-within-group pattern (Ch. 19), pandas edition
(sales.groupby(["category", "item"])["amount"].sum()
      .reset_index()
      .sort_values(["category", "amount"], ascending=[True, False])
      .groupby("category").head(3))
```

One aesthetic note that is also a professional one: pandas expressions *chain* — method after method, each feeding the next, usually wrapped in parentheses for line breaks. The chain reads top-to-bottom like a CTE pipeline (Ch. 18's story-shape), and that is not a coincidence: it is the same discipline — decompose, name (or chain), test each step — in a different accent. Run chains a link at a time while learning: build `groupby(...)`, run; add `["amount"]`, run; add `.agg(...)`, run. Each link's output is inspectable, exactly like running each CTE alone.

## 34.2 merge: Joins, With the Defence Built In

`merge` is Chapter 17 with the craft lessons as arguments:

```python
# LEFT JOIN sales to customers, keeping non-members
enriched = sales.merge(customers, on="customer_id", how="left")

# the anti-join -- orphans and never-boughts
orphan = sales.merge(customers, on="customer_id", how="left", indicator=True)
orphan = orphan[orphan["_merge"] == "left_only"]
```

`how=` is the join direction you know ("left", "inner"; "right" and "outer" exist and are rarely right); `on=` is the key; and `indicator=True` adds the `_merge` column ("left_only" / "both" / "right_only") — the anti-join as an argument. And the fan-out defence is *easier* than SQL's, because pandas will often warn you ("merging on duplicate values" behaviour) — but do not rely on warnings; rely on the liturgy, which is two lines:

```python
print(len(sales), "->", len(enriched))                # row count before/after
print(sales["amount"].sum() == enriched["amount"].sum())   # totals reconcile
```

Count before, count after, reconcile the totals — Chapter 17's habit, mechanised. If the row count grew on a left merge, the right side repeated keys and every aggregate downstream is inflated; you now catch it in one printed line, forever.

## 34.3 Time Series: The Shop's Calendar, Natively

Dates parse once (Ch. 33) and then pandas becomes a calendar engine. The three moves that cover working time-series analysis:

```python
daily = (sales.groupby("date")["amount"].sum()
              .sort_index())                 # a dated Series: takings per day

monthly = daily.resample("ME").sum()         # 1: daily -> monthly totals
daily["rolling_7"] = daily["amount"].rolling(7).mean()   # 2: the moving average
monthly["mom_pct"] = monthly["amount"].pct_change() * 100 # 3: month-over-month
```

- **`resample`** is groupby-for-time: "ME" is month-end; "W" week; "Q" quarter — the pivot's date-grouping with calendar awareness (months of unequal length handled correctly).
- **`rolling`** is the window function's frame: `rolling(7).mean()` is Chapter 19's moving average; `.rolling(7).sum()` is the rolling total; `.cumsum()` the running total — one method each.
- **`shift`** and **`pct_change`**: shift moves a column down a row (LAG, verbatim); `pct_change()` is `(x − x.shift())/x.shift()` pre-assembled — month-over-month growth, the requested metric of Chapter 19, as one call.

The lag-then-compare idiom extends anywhere: `monthly["amount"] - monthly["amount"].shift(12)` is year-over-year change, and you did not write a loop or a window clause to get it. The time-series kit is the single biggest practical upgrade pandas gives Tariro's shop: the whole Chapter 10 drag-dance per month is now `daily.resample("ME").sum().plot()`.

## 34.4 The Full Re-Run

Proof of the chapter's opening claim — Part II's monthly report analysis, the numbers behind all three findings, in fifteen lines (run it; then read it):

```python
sales = pd.read_csv("sales.csv", parse_dates=["date"])
sales["month"] = sales["date"].dt.to_period("M")
sales["weekday"] = sales["date"].dt.day_name()

# headline: monthly revenue
monthly = sales.groupby("month")["amount"].sum()

# finding 1: top items
top_items = (sales.groupby("item")["amount"].sum()
                 .sort_values(ascending=False).head(10))

# finding 2: the oil collapse -- price vs quantity, monthly
oil = sales[sales["item"] == "Cooking Oil 2L"]
oil_monthly = oil.groupby("month")["amount"].agg(["count", "sum"])

# finding 3: Sundays (traffic, not basket) + loyalty share
by_day = sales.groupby("weekday").agg(n=("amount", "count"),
                                      revenue=("amount", "sum"),
                                      avg_basket=("amount", "mean"))
member_share = (sales.assign(member=sales["customer_id"].notna())
                     .groupby("month")["member"].mean() * 100)

print(f"Top item: {top_items.index[0]} (${top_items.iloc[0]:,.2f})")
print(f"Sunday avg basket: ${by_day.loc['Sunday', 'avg_basket']:.2f} "
      f"vs weekday ${by_day.drop('Sunday')['avg_basket'].mean():.2f}")
print(f"Member share of sales, latest month: {member_share.iloc[-1]:.1f}%")
```

Every line is a chapter you have lived: the parse, the derived columns, the pivot, the filter, the groupby-with-names, the assign-and-group, the f-strings with formats. Nothing here is new — that is the chapter's entire point. **You already know the analysis; you are now holding it as an artefact.** Next month's CSV arrives, this runs unchanged, and the report's numbers regenerate: that is "dangerous".

> **From Your Toolkit — the analytical engine:** groupby/merge/resample are the load-bearing walls of everything ahead — Chapter 36's tests consume their outputs, Chapter 37 automates this very block, Chapter 39's Power BI dataset is often *prepared* by exactly these lines before import, and Project 4's churn analysis is groupby-plus-shift wearing a business suit. The spreadsheet gave you the concepts; SQL gave you the grammar; pandas gives you the *engine* — the same machine, now yours to program.

## Key Takeaways

- groupby is pivot + GROUP BY in one idiom: `df.groupby(keys)[col].agg(...)`; named aggregations are your AS aliases; group-filtering is HAVING.
- merge is the join: `on=`, `how=`, `indicator=True` for anti-joins — and the two-line fan-out defence (row counts, totals) runs after every merge, always.
- Time series: resample (calendar groupby), rolling (frames), shift/pct_change (LAG and MoM) — running totals to year-over-year, one call each.
- Chains read like CTE pipelines; build them link by link and inspect each stage.
- Fifteen lines re-run Part II's report analysis — the concepts were yours; now the artefact is.

## Practice Lab

1. The pivot tour, re-run: rebuild Chapter 10's five pivots (category × revenue, month × revenue, weekday counts, payment mix, member share) as one chained block each; reconcile every total against the Part II workbook; paste reconciliations as a Markdown table.
2. The merge gauntlet: LEFT JOIN sales→customers with the two-line defence; then the anti-join with `indicator=True`; confirm orphan counts match Project 2's documented orphans exactly; write the one-sentence difference between doing this in SQL and in pandas.
3. The time-series shelf: from daily takings build the 7-day rolling mean, month-over-month pct change, and year-over-year change; chart the three (next chapter's `.plot()` is allowed early); annotate the biggest MoM jump with its cause (a planted pattern, by now an old friend).
4. The top-N drill: top 3 items by revenue within each category (the Section 34.1 pattern); reconcile the grand total; write the tie-policy note (which method breaks ties, and how you know).
5. The re-run, owned: extend the fifteen-line block with a fourth finding of your choosing (whales, suburbs, or the oil price question); wrap the whole thing in a function `monthly_numbers(sales)` that returns a dict of the key figures — Chapter 37 will thank you, because this function *is* the monthly pack's engine.

## Further Reading

- Chapter 35 (charts — the lines get pictures), *Python for Data Analysis* ch. 8–10
- pandas' groupby and merging user guides — the official deep dives, readable after this chapter
