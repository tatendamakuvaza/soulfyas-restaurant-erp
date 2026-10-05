# Chapter 12: Descriptive Statistics in Excel

*Part II — Excel: Your First Superpower*

> "Before you can say 'unusual', you must be able to say 'typical'. Descriptive statistics is the craft of saying 'typical' without lying."

### In this chapter you will learn

- The descriptive statistics any analyst must produce: mean, median, mode, range, and quartiles.
- Spread: standard deviation in plain words, and why two shops with the same average are not the same shop.
- Outliers: the 1.5×IQR rule, and what to do (and never do) about them.
- Excel's statistics functions and the Analysis ToolPak, hands on the sales data.
- The first three business questions answered with statistics, properly.

## 12.1 The Statistical Frame, in One Table

Statistics first asks four questions of any column of numbers, and Excel answers all four. On the `amount` column (every sale, eighteen months):

| Question | Statistic | Excel | On Tariro's sales |
|---|---|---|---|
| What's typical? | Mean | `=AVERAGE(amounts)` | 8.42 |
| What's typical, robustly? | Median | `=MEDIAN(amounts)` | 6.50 |
| What's most common? | Mode | `=MODE.SNGL(amounts)` | 5.00 |
| How wide is the range? | Range | `=MAX - MIN` | 0.50 – 412.00 |

And the fifth, the most important in the set: `=QUARTILE(range, 1)` and `=QUARTILE(range, 3)` — the values with a quarter and three quarters of the data below them. Together they give the **five-number summary** (min, Q1, median, Q3, max), the fastest honest portrait of any column ever invented: "half of all sales are between 4 and 11 dollars."

## 12.2 Why the Median Gets Its Own Chapter

The mean is fragile: one 412-dollar bulk order drags Tariro's average sale from about 6 to about 8.4 — the mean moved; the shop did not. The **median** (line up every sale; take the middle one) ignores that whale entirely, which is why it is the honest headline for skewed money: incomes, house prices, basket sizes. When mean and median sit far apart, the data is telling you it is lopsided (a long tail of small sales and a short one of whales) — and your report should say which number it is quoting and why (Honesty Rule 1: an average is an answer, not the answer).

The mean still matters — it is the only "typical" that interacts correctly with *totals* (mean × count = total, the reconciliation identity you used in Chapter 8). The craft is the pair: report the mean when totals matter, the median when typicality does, and both when they disagree enough to be a finding.

## 12.3 Spread: Same Average, Different Shop

Standard deviation, `=STDEV.S(amounts)`, in plain words: **the typical distance from the mean**. A small one means sales cluster tightly (a dependable newsagent rhythm); a large one means swings (a shop living on windfalls). Two hypothetical shops, both averaging 8.40: Shop A's sales almost all between 7 and 10, Shop B's half at 2 and half at 15. Same mean; utterly different business — inventory, staffing, cash-flow risk. The mean without the spread is half a portrait.

The spread statistic you will actually *use* most is the **IQR** — Q3 − Q1 — because it is robust like the median (whales do not move it), and because it powers the outlier rule, next.

## 12.4 Outliers: The 1.5×IQR Rule

The rule, used identically in Excel, SQL, Python, and SPSS (four accents, one sentence): a value is an outlier if it lies beyond

```text
fences = Q1 − 1.5×IQR   and   Q3 + 1.5×IQR
```

On Tariro's amounts: Q1 = 4, Q3 = 11, IQR = 7, so fences at −6.5 and 21.5 — every sale above 21.50 is flagged, about 4% of rows: the bulk cooking-oil orders, the December party season, one 412.00 that is *correct* (a school's term-start order — you rang and checked; Chapter 2 says the number is a claim, and some claims survive checking).

What to do with outliers, in order: **investigate** (what is it? bulk buyers are a *segment*, not an error), **report separately** ("sales excluding bulk orders"), **cap only with a stated reason** (winsorising, a Part IV word), and **never silently delete** — the deleted whale is the lost customer. Excel's **Analysis ToolPak** (File → Options → Add-ins → Analysis ToolPak; LibreOffice: Data → Statistics) does all of this in one dialog: Data Analysis → Descriptive Statistics → Summary statistics, and the five-number summary, mean, and standard deviation arrive as a table.

## 12.5 Three Questions, Answered Properly

Statistics earns its place by answering Tariro's standing questions better than the pivot alone could:

- **"Is my Sunday trade weak?"** Median basket by weekday (a pivot, Values set to Median where supported, or `MEDIAN(IF(...))` as an array formula): Sundays are not low-*basket*, they are low-*traffic* — fewer customers, spending typically. The pivot said "small"; statistics says *why* it is small. Different decisions follow (marketing vs pricing).
- **"How risky is the month?"** Monthly revenue, mean and standard deviation across eighteen months: the mean gives the expectation, the spread the risk — a month 40% below the mean is within this shop's ordinary wobble, and Tariro can stop panicking about it (or not panic *enough*, once Part IV teaches what "ordinary" really means).
- **"Who are my whale customers?"** The 4% beyond the fence, listed by member_id (the join from Chapter 9): a named, checkable list — not a vibe.

> **From Your Toolkit — the portable five:** mean, median, quartiles, IQR fences, standard deviation travel with you everywhere: SQL's `PERCENTILE_CONT` and `AVG` (Chapter 16), pandas' `.describe()` (Chapter 34, literally this chapter as one method), SPSS's Frequencies/Descriptives (Part IV), Power BI's DAX measures (Chapter 40). The five-number summary is one of the few things every tool in this book computes — because it is one of the few things every analyst needs.

## Key Takeaways

- Five numbers portrait any column: min, Q1, median, Q3, max — build it before you believe any average.
- Mean for totals-thinking, median for typicality, both when they disagree (and they will, on money).
- Standard deviation = typical distance from the mean; IQR = the robust spread that powers the fence.
- Outliers: investigate → report separately → cap with reasons → never silently delete.
- The best analyses pair a statistic with a *why*: small Sundays are traffic, not basket.

## Practice Lab

1. Five-number summary of `amount` (functions or ToolPak), plus mean and standard deviation; write the two-sentence portrait of a typical sale, quoting both typicals and explaining the gap.
2. Fence the outliers: compute the 1.5×IQR fences, count and list the flagged rows, classify each as bulk-buyer, seasonal, suspicious, or whale; annotate the 412.00 with its verified story in your log.
3. The two-shops experiment: hand-build two small columns with the same mean and different spreads; compute STDEV for both; write the one-sentence business warning spread carries and averages cannot.
4. Weekday statistics: median basket and transaction count by day of week; write the traffic-vs-basket verdict on Sundays in exactly two sentences, each carrying a number.
5. Whale roll: the outlier list joined to customers (Ch. 9), grouped by suburb in a pivot; name the three decisions Tariro could make from this one page.

## Further Reading

- Chapter 22 (the ideas get their theory), Chapters 24–25 (distributions and the tests), SPSS/Stata equivalents (Part IV)
- *Naked Statistics* — Charles Wheelan (the friendly tour of everything this chapter begins)
