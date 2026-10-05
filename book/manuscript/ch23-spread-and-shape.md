# Chapter 23: Spread and Shape — the Bell Curve, Gently

*Part IV — Statistics Without Fear*

> "Two shops, one average. The difference between thriving and closing is the spread — the shape around the middle."

### In this chapter you will learn

- Range, IQR, variance, and standard deviation — the spread statistics, built by hand once.
- The bell curve (normal distribution) — what it is, why it appears, and what it promises.
- Skew, in the formal sense — and the right skew of money, again, understood.
- Outlier rules derived, not memorised — why the 1.5×IQR fence is 1.5.
- Reading a histogram like an analyst: shape words that mean something.

## 23.1 Spread, Built by Hand

Take five daily takings (dollars): 100, 110, 120, 130, 140. Mean = 120. The deviations from the mean: −20, −10, 0, +10, +20. Now the ladder of spread statistics, each answering "how far from typical?":

- **Range** = max − min = 40. Simple, honest, destroyed by one wild day.
- **IQR** = Q3 − Q1 = 130 − 110 = 20. The middle half's width — robust (Chapter 12's fence-builder).
- **Variance** = the average *squared* deviation = (400+100+0+100+400)/5 = 200. Squared units (dollars²!) — unintuitive, but mathematically the deep one, because squaring makes everything positive and treats big deviations severely.
- **Standard deviation** s = √variance = √200 ≈ 14.1 — *back in dollars*: "the typical distance from the mean", and the workhorse of everything that follows.

(For a *sample* — almost always your case — we divide by n−1 instead of n: 200×5/4 = 250, s ≈ 15.8. Why n−1 is a Chapter 25 question about samples and populations; for now, note that spreadsheet's `STDEV.S` and the formulas ahead use n−1, and `STDEV.P` uses n. Choosing wrong on small data changes the answer visibly.)

Compare shop B: 60, 90, 120, 150, 180. Same mean (120), s ≈ 44.2 — triple the risk. Spread is where the business lives, which is why every serious report pairs a typical with a spread, always.

## 23.2 The Bell Curve

Draw a histogram of a thousand *sums of things* — total daily takings (many customers' baskets added), a person's height (many genes and meals), a measurement error (many small nudges) — and the same shape emerges: symmetric, one hump in the middle, tails thinning both ways. The **normal distribution** (the bell curve) is not a law someone decreed; it is what happens when many small, independent causes add up — the Central Limit Theorem's promise (Chapter 25 makes it formal), and the reason the bell is the default shape of nature and industry.

The normal's magic property, worth memorising as a picture rather than a formula:

```text
            |     68% of data within ±1s of the mean
   ~~~~~    |    95% within ±2s
  ~~~~~~~   |   99.7% within ±3s   ("the 68–95–99.7 rule")
```

On Tariro's daily takings (mean ≈ 2,990, s ≈ 640, close enough to normal for the shape's promise): roughly 68% of days land between 2,350 and 3,630; a day below 1,710 (−2s) happens about once in twenty days; a day below 1,070 (−3s) happens about three days in a thousand. Suddenly "unusual" has a *number attached*, and the bank manager's anxiety can be calibrated: a 2,200-dollar Tuesday is a bad day, not a crisis — but a 900-dollar Tuesday is a three-sigma event, and *something happened* (a road closure, a competitor's opening, a till failure). This is the analytic superpower the bell delivers: **expected variation vs signal, on a ruler.**

## 23.3 When the Bell Is a Lie

The bell's danger is precisely its popularity: not everything is normal, and assuming it of money data is the classic error. Basket *amounts* — one customer, one purchase — are right-skewed (the whale's home); so are incomes, claim sizes, and website dwell times. The bell fits *sums and averages* of many small influences (daily takings = sum of ~35 baskets), not the raw skewed ingredients — a distinction Chapter 25 will make precise and profitable (averages of skewed things behave normally even when the things don't).

**Skew, formally**: the third moment's sign — tail right = positive skew (mean > median), tail left = negative skew (mean < median). The histogram words that matter: **symmetric** (bell-ish), **right-skewed** (money), **left-skewed** (rare), **bimodal** (two populations in one column — two kinds of shopper, weekdays and Saturdays; report the humps, never one typical). **Kurtosis** (tail heaviness) exists as a word; you may ignore it until an exam asks.

## 23.4 The Fence, Derived

Chapter 12's outlier rule — fences at Q1 − 1.5×IQR and Q3 + 1.5×IQR — deserved its constant. Here is where 1.5 comes from: for normal data, Q1 and Q3 sit about 0.67s below and above the mean, so IQR ≈ 1.35s, and the fence sits 1.35s × 1.5 / 2... more usefully: the fence lands near μ ± 2.7s — just outside the 99.7% band. In other words, **for bell-shaped data, the 1.5×IQR fence flags almost exactly the rarest 0.3% of values** — the rule is a significance test in costume, built from robust statistics so that whales do not move the goalposts they are judged by. (The z-score method of Chapter 24 — flag beyond ±3s — is the same idea computed from the mean and s, and *not* robust: the whale drags s and hides itself. When you must choose: fences for skewed data, z-scores for symmetric data you trust.)

That is the deeper pattern of this whole subject: **the same idea (how far is this value from typical, in units of typical variation?) reappears in fences, z-scores, t-tests, p-values, control charts** — one sentence wearing different costumes. Learn the sentence once, at whatever depth you are standing on, and every costume afterwards is a wardrobe change.

## 23.5 Reading a Histogram

The professional's shape-reading checklist — ten seconds, every numeric column, forever:

1. **One hump or two?** Two = two populations; stop, segment, report the humps.
2. **Symmetric or skewed?** Skew direction by tail; right-skew = money-shape = medians headline.
3. **Where does it end?** A hard floor at zero? A ceiling (closed shop, capped prices)? Ends carry business meaning.
4. **Any gaps or spikes?** A spike at exactly 5.00 (the mode — a psychological price point); a gap where a category has no sales — data *quality* story or business story, always worth one question.
5. **What would the fence flag?** Estimate Q1, Q3 by eye; where do the fences land; what population lives beyond them (bulk buyers — a segment, Chapter 12's lesson)?

> **From Your Toolkit — the shape kit travels:** `PERCENTILE_CONT` + a spread in SQL (Appendix A), `.describe()` and `.hist()` in pandas (Chapters 34–35), the distribution line in Power BI (Chapter 42), Explore→Descriptives→Plots in SPSS (Chapter 29). The bell's 68–95–99.7 promise returns as confidence intervals (25), hypothesis tests (26), and control charts (Chapter 60) — same bell, three costumes. And the fence/z-score equivalence is the sentence that quietly unifies Part IV.

## Key Takeaways

- Spread ladder: range (fragile), IQR (robust), variance (squared units, deep), s (dollars again — the workhorse); sample vs population divisor (n−1 vs n) matters on small data.
- The bell appears wherever many small causes add up; 68–95–99.7 turns "unusual" into a number; −3s days are events, not weather.
- Money is right-skewed; bells fit sums and averages of money, not raw money; bimodal means two populations — segment, don't average.
- The 1.5×IQR fence ≈ the 99.7% band for bells, built from robust stats — a significance test in costume; fences for skewed, z for symmetric.
- Read every histogram with the five-question checklist — humps, tails, ends, spikes, fences.

## Practice Lab

1. By hand: the five-value ladder (range, IQR, variance, s with both divisors) on shop A and shop B above; confirm your s values against `STDEV.S`/`STDEV.P` in your spreadsheet; write the "same average, different risk" sentence with numbers.
2. The bell check: histogram of daily takings (a pivot by date, then a chart); estimate μ and s by eye, mark ±1s, ±2s, ±3s, and count the days outside each band; how close to 68–95–99.7 does the shop's real data come? Write one sentence on why it is close but not exact.
3. The money-shape check: histogram of basket `amount`; name the shape; re-plot log-style if your tool allows (or simply describe the tail); write the "which typical" sentence this shape commands.
4. The fence derivation, verified: compute Q1, Q3, IQR, fences on daily takings; list the flagged days; compare with the ±2.7s rule of thumb; explain any disagreement in one sentence (hint: is the data perfectly symmetric?).
5. The bimodal hunt: histogram of basket amounts *by weekday vs Saturday* (two series or two charts); if the humps differ, write the "two kinds of shopper" sentence — and note it in the questions ledger as a segmentation finding, description-level.

## Further Reading

- Chapter 24 (z-scores — the sentence standardised), Chapter 25 (why the bell keeps appearing — the Central Limit Theorem)
- *The Art of Statistics* (Spiegelhalter) chapters 4–5 — shape and spread, by a master teacher
