# Chapter 28: Relationships — Correlation, Regression, and the Trap

*Part IV — Statistics Without Fear*

> "Correlation is a fact about data. Causation is a claim about the world. The first is arithmetic; the second requires an argument."

### In this chapter you will learn

- Correlation: the scatter plot's number, built by hand once, read honestly.
- The line of best fit: regression as "the line that minimises squared wrongness".
- Prediction with a line — and prediction intervals, the honesty attachments.
- The three explanations of any correlation, and the causation trap's escape routes.
- Tariro's price-and-quantity question, answered the professional way.

## 28.1 The Scatter's Number

Chapter 11's sleeper chart — the scatter — now gets its arithmetic. **Correlation (r)** measures the strength and direction of a *straight-line* relationship between two numeric variables, on a ruler from −1 (perfect negative) through 0 (no linear relationship) to +1 (perfect positive).

Built by hand once, on five points of price vs bottles-sold (cooking oil, monthly): the trick is to standardise both variables (z-scores, Chapter 24) and multiply — r is the average of "x's z times y's z". When both are unusually high together (expensive month, few bottles — negative products) or unusually low together, the products run negative; months that agree in direction push r; months that disagree pull it. Five points of oil: r ≈ **−0.87** — a strong negative relationship: higher price, fewer bottles. (The formula, for the record: r = Σ(zx·zy)/(n−1).)

Reading rules that hold forever: |r| < 0.3 weak (usually ignorable, in business data); 0.3–0.7 moderate (interesting, exploitable); > 0.7 strong (rare, suspicious — check it is not an artefact); r ≈ 0 means *no straight-line* relationship — not "no relationship" (a U-shape has r ≈ 0 and a perfect relationship; plot before you conclude — the scatter, always the scatter).

## 28.2 The Line

The **line of best fit** (least-squares regression) answers the question the scatter begs: *what line summarises this cloud?* — specifically, the line minimising the sum of *squared* vertical misses (residuals — squared for the Chapter 23 reason: positivity plus severity). Two numbers define it, and both are sentences:

```text
bottles ≈ 6.2 − 1.1 × price        (on the oil months)

slope −1.1: each extra dollar of price ≈ 1.1 fewer bottles per month
intercept 6.2: at price zero — extrapolation, not knowledge (no data there)
```

The **slope is the finding** — "a dollar costs a bottle a month" is a sentence a shop owner acts on (it prices the wholesaler's increase: at +0.80, expect ≈ −0.9 bottles/month per customer). The **intercept** anchors the line but means nothing outside the data's range. **R²** (r squared, here ≈ 0.76) is "the share of the y-variance the line explains" — 76% of month-to-month bottle swings track price; the other 24% is everything else (paydays, rivals, weather) — the residual world where the next question lives.

**Prediction, with honesty attached**: at price 3.60 the line says 2.24 bottles. That is a *point* prediction; the honest version carries an interval wide enough to matter (prediction intervals widen with distance from the data's centre and with the residual scatter — every tool prints them; Appendix D has the formulas). Lines are for interpolating within the data's range; extrapolation — price 9.00, predicted −3.7 bottles (impossible, and the line does not care) — is where straight lines lie confidently. Extrapolate at your reputation's risk.

## 28.3 The Trap, Formally

Honesty Rule 2 becomes a taxonomy. You find a correlation — oil price and quantity, r = −0.87. Three explanations, *always all three, always in this order*:

1. **Coincidence** — two unrelated series drifting together (n = 18 months is small; spurious correlations are industry on the internet). Defence: the surprise score (a significance test on r — p ≈ 0.0005 here, so not *pure* luck, though significance never converted coincidence to cause by itself).
2. **Confounding** — a third variable drives both (oil price and quantity both driven by the *harvest year*; ice creams and drownings both driven by *summer*). The most common truth in observational data; the defence is to *name and measure the confounder* — or hold it constant (compare within one harvest year only).
3. **Causation** — X actually moves Y. The claim requires an *argument*, and in business the argument's gold standard is the **experiment**: change the price deliberately, on one shelf, for one month, and watch quantity move while everything else holds — the A/B logic of Chapter 57's world, available to Tariro at shelf scale.

The professional's phrasebook: "price and quantity are strongly negatively correlated (r = −0.87, p < 0.001)" — always safe, always true. "The price rise cost us about 1.1 bottles per customer per month, pending a shelf trial" — a causal claim, honestly flagged as pending. What is never safe: sliding from the first sentence to the second without noticing. (Classic traps for your collection: summer → both; health-conscious people both buy gym memberships and eat salad (self-selection — the loyalty-scheme caveat's family); richer suburbs buy more of everything — *everything correlates with money*.)

## 28.4 Tariro's Question, Answered Properly

The ledger's price question, closed in the manner Part IV has taught — every element of the arc in one finding:

> *Cooking-oil price and monthly quantity per customer are strongly negatively correlated (r = −0.87, p < 0.001, n = 18 months); the fitted line estimates ≈1.1 fewer bottles per month per dollar of price (R² = 0.76). The month-9 rise of 0.80 therefore predicts ≈0.9 fewer bottles — matching the observed −1.3 within the noise (paired test, Ch. 26: p ≈ 0.0008). Because price was not experimentally varied, the causal reading rests on the mechanism (a known wholesaler increase) and the size and consistency of the association; a one-shelf price trial would close the argument.*

Correlation to size the relationship, a test to rule out noise, an interval to bound the estimate, a mechanism to argue cause, an experiment to finish the job — that paragraph is the whole of Part IV assembled, and it is the calibre of finding that gets analysts hired (Chapter 46 will publish it as portfolio evidence).

## 28.5 Many Variables, a Glimpse

Real questions have several drivers — quantity by price *and* payday week *and* rival promotions. **Multiple regression** extends the line to several x's (quantity ≈ a + b₁·price + b₂·payday + …), each slope "the effect of that variable, *holding the others constant*" — the arithmetic of controlling for confounders. It is Part V-and-beyond territory (Chapter 36 runs it in Python; Chapter 58 meets its machine-learning descendants), but two warnings travel with the glimpse, today: a slope's meaning depends on *which other variables are in the model* (add/remove one, the story changes — "controlled for what?" is the reader's question); and more variables eat n (each one spends degrees of freedom; 18 months will not support eight predictors). When you meet a multiple regression in the wild, you now know the two questions to ask.

> **From Your Toolkit — the relationship kit:** `CORREL`/`LINEST` in spreadsheets, `corr()` in SQL (some engines; else compute via the appendix recipe), pandas' `.corr()` and seaborn's scatter-matrix (Chapter 35), SPSS's Analyze → Correlate/Regression dialogs (Chapter 29), and Power BI's scatter visual with a trend line (Chapter 42). The *reading* — slope as finding, R² as share, the three explanations, experiment as gold standard — transfers intact everywhere; it is the same paragraph in every tool.

## Key Takeaways

- r measures straight-line association: 0.3/0.7 as rough anchors; r ≈ 0 ≠ no relationship — plot the scatter, always.
- The line: slope is the finding ("a dollar costs a bottle"), intercept anchors only, R² is the share explained; predict within range, with intervals.
- Any correlation has three explanations — coincidence, confounding, causation — and only an argument (ideally an experiment) licenses the third.
- The professional paragraph: correlation + test + interval + mechanism + proposed trial — Part IV's arc in five clauses.
- Multiple regression holds others constant; ask "controlled for what?" and watch n.

## Practice Lab

1. Hand-r: the five oil months (price, bottles) — standardise both columns, multiply, average; reconcile with `CORREL`; write the three-clause reading (strength, direction, significance).
2. The line, by tool: fit bottles ≈ a + b·price (spreadsheet trendline, SPSS, or Python); write the slope-sentence and the R²-sentence; predict at the data's min, max, and 1.5× the max — and annotate the third prediction "extrapolation, handle with care".
3. The confounder hunt: on Tariro's data, find two variables that correlate but are plausibly both driven by a third (e.g., revenue and baskets by month — both driven by customer count); name the confounder and write the "controlled for what?" question it provokes.
4. The trap collection: find two published spurious correlations (the internet's galleries are full of them); for each, write which of the three explanations is most likely and what evidence would separate them.
5. The trial design (ledger's next opening): design the one-shelf price trial — what price, which shelf, how long, what till metric decides, and what threshold counts as "the line was wrong". One page; it is Project 4's feedstock and portfolio evidence of experimental thinking.

## Further Reading

- Chapter 36 (regression in Python), Chapter 29 (SPSS/Stata's regression dialogs)
- *The Book of Why* (Pearl) — causation's deep theory, readable; *Spurious Correlations* (Vigen) — the comedy branch of this chapter
