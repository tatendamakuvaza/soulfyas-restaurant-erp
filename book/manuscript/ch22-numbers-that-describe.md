# Chapter 22: Numbers That Describe

*Part IV — Statistics Without Fear*

> "The mean is a fact about arithmetic. The median is a fact about people. Knowing which sentence you are writing is half of statistics."

### In this chapter you will learn

- The three "typical" numbers — mean, median, mode — as *theory*, not functions.
- When each one lies, and the shape-of-data reasoning that picks the honest one.
- Weighted means, and the market-share question that needs one.
- The first formal notation — read and write statistics like a native.
- The questions from Part III that statistics will now formalise.

## 22.1 Description Is a Claim

Part II computed the numbers; Part IV asks what they *mean* — and the first lesson is that every descriptive number is a claim about a whole distribution, compressed into one figure. A mean claims: "if every value were equal, here is the value that preserves the total." A median claims: "half of this data lies below me." A mode claims: "this value is the most common." Three different claims — all true, all partial, all capable of lying by selection. Statistics without fear is not statistics without care; it is knowing precisely which claim your number makes, and saying so.

## 22.2 The Mean: Arithmetic's Tyranny and Grace

The mean is the balance point of the data — physically, if you cut the histogram out of wood, it balances on the mean's edge. Its grace: it uses every value, and it is the only typical that plays correctly with totals (mean × n = sum — the reconciliation identity of Chapter 8, now understood as a *theorem*). Its tyranny: it is dragged by extremes. One 412-dollar whale moved Tariro's basket from 6.50 (median) to 8.42 (mean) — a 29% distortion from a single row.

The formal rule for when the mean lies: when the distribution is **skewed** — lopsided, with a long tail on one side. Money is almost always right-skewed (a floor at zero, no ceiling): incomes, basket sizes, city populations, website visits. The whale is not an aberration in money data; the whale is *what money data is*. Hence the professional default: **medians for money headlines, means for totals arithmetic**, both reported when they disagree enough to matter — the Part II habit, now with its reasoning attached.

## 22.3 The Median and the Mode

The median is the middle value by rank — the 50th percentile (Chapter 24 builds the whole percentile family). Its virtues are the mean's vices: it ignores magnitude (the whale counts as one row), so it is **robust** — a word statisticians use to mean "liars cannot move it easily." Its vice: it ignores magnitude — for totals thinking it is useless (median × n is not the sum; try it and watch the reconciliation fail).

The mode — most common value — is the only typical that works on *categories*: the modal payment type (EcoCash), the modal shopping day (Saturday), the modal basket (5.00). It is underused and quietly valuable in retail, where "what do most people actually do" is often the question. Its failure mode: multimodal data (two humps — weekday shoppers and Saturday shoppers, each with their own typical) has no single mode, and reporting one anyway is a small lie with a straight face.

## 22.4 Which Number, Decided by Shape

The choosing rule, formalised:

| Shape | Mean vs median | Honest headline |
|---|---|---|
| Symmetric (roughly mirror) | Close together | Either; report mean, sleep well |
| Right-skewed (long tail up: money) | Mean > median | Median for "typical"; mean only with totals |
| Left-skewed (long tail down: rare — ages at death, days-to-delivery) | Mean < median | Median again |
| Multimodal (two humps) | Either, misleadingly | Report the humps: "two kinds of shopper" |

Draw the histogram (even a rough one) before choosing; the eye that sees two humps saves the mouth from one number. This is why Part II insisted on quartiles: the five-number summary is a *shape* description disguised as five values.

## 22.5 Weighted Means

One more typical, because a real question needs it: *what is the average price of cooking oil across all bottles sold?* Not the average of the prices (that treats a 30-bottle week and a 1-bottle week as equals) — the average *experienced by bottles*: weight each price by the bottles sold at it. The weighted mean:

```text
weighted mean = Σ(price × bottles) / Σ(bottles)
```

Compute it once by hand on five weeks of data and you will never confuse it again: the naive mean of prices says 3.10; the bottle-weighted mean says 3.42 — because more bottles sold at the higher price. Every "average" you meet at work is secretly a choice of weights: average revenue per *store* vs per *transaction* vs per *customer* are three different weighted means of the same data, and reports that mix them up are quietly wrong. When someone says "the average", the professional reflex is now: *weighted by what?*

## 22.6 The Notation, Gently

Statistics has a small formal language, and reading it removes the foreigner's tax. The core, all of it used repeatedly in this book:

- **x̄** ("x-bar") — the sample mean. **μ** ("mu") — the population mean (Chapter 25 draws the line between them).
- **n** — the count of values. **Σ** ("sigma", uppercase) — "add these up": x̄ = Σx / n is the mean, written properly.
- **Md** or the tilde X̃ — the median (usage varies by book; this book writes "median" in words, always).
- **s** — sample standard deviation; **σ** ("sigma", lowercase) — population standard deviation (next chapter's star).

That is the entire notation kit for four chapters. When a formula in the wild looks alien, translate it back to these five symbols and it collapses into a sentence.

## 22.7 The Questions Returning

Part III ended owed: is Sunday's shortfall a pattern or a coincidence? Did the price rise *significantly* hurt? Did loyalty *cause* anything? Descriptive statistics — this chapter — sharpens the questions but cannot close them; that takes spread and shape (next), z-scores (24), sampling theory (25), and tests (26). The arc is deliberate: description → distribution → standardisation → sampling → inference. By Chapter 29 you will close every open question in the ledger, and the SPSS/Stata chapter will show you the menus where the same tests live in classic packages.

> **From Your Toolkit — one claim per number:** mean, median, mode, weighted mean appear in every tool of this book — `AVG` and `PERCENTILE_CONT` in SQL (Appendix A), `.mean()/.median()` in pandas (Chapter 34), the "Average/Sum" toggle in Power BI (Chapter 40), Descriptives in SPSS (Chapter 29). What transfers is not the function name but the *claim*: which typical, why, weighted by what, with the shape checked first. That habit is the statistics.

## Key Takeaways

- Every descriptive number is a claim: the mean preserves totals, the median preserves typicality, the mode preserves frequency — choose by the claim your sentence needs.
- Skew decides: money is right-skewed; medans headline money; means do totals; both when they disagree.
- Multimodal data has no honest single typical — report the humps.
- Weighted means are everywhere; the reflex question is "weighted by what?" (store, transaction, or customer — three answers, one dataset).
- Notation kit: x̄, μ, n, Σ, s, σ — five symbols, four chapters, no more foreigner's tax.

## Practice Lab

1. By hand (calculator or spreadsheet, no functions): compute mean, median, mode of these ten baskets — 2.50, 5.00, 5.00, 5.00, 6.50, 7.00, 8.00, 11.50, 19.00, 412.00. Then remove the whale and recompute. Write the two-sentence comparison that explains skew to a shop owner.
2. The choosing drill: for `amount`, `customer age` (from customers), and `items per sale`, sketch (or histogram) the distribution, name the shape, and choose the headline typical — with one sentence defending each choice.
3. The weighted trap: compute the naive and bottle-weighted average cooking-oil price from your data (or the five-week mini-dataset above); write the two numbers side by side and the sentence explaining the gap to Tariro.
4. Notation translation: write "the mean of the amounts is Σx/n" and "the median basket" using correct symbols; then find one formula in any statistics resource online and translate it into a sentence using your kit.
5. The ledger: open your questions log (from Chapter 2's habit); mark each open question with what it needs — description, spread, standardisation, sampling, or a test. You have just written Part IV's table of contents for yourself.

## Further Reading

- Chapter 23 (spread and shape — the rest of the portrait), *Naked Statistics* (Wheelan) chapters 2–3
- *How to Lie with Statistics* (Huff) — the 1954 classic; every trick is still in daily service
