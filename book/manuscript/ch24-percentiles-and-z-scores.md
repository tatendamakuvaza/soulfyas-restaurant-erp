# Chapter 24: Percentiles and Z-Scores — "Above Average", Properly

*Part IV — Statistics Without Fear*

> "'Above average' is a compliment paid by people who never asked how far above, or how rare that is."

### In this chapter you will learn

- Percentiles and quartiles, formally — and the "which method?" footnote that no one warns you about.
- The z-score: any value, restated in units of its own data's spread.
- What z-scores are for: flagging, comparing apples to oranges, and standardising columns.
- The empirical rule and Chebyshev's fallback — the bell's promise, and the promise that works on anything.
- Tariro's dashboards get a genuinely new number: how each day ranks, honestly.

## 24.1 Percentiles, Formally

The **p-th percentile** is the value below which p% of the data lies. The median is the 50th; quartiles are the 25th, 50th, 75th. The percentile *rank* of a value answers the reverse question: what percentage of the data lies below *this*? The two directions — value from rank, rank from value — are the same ruler read from opposite ends, and fluency is reading both without noticing.

Percentiles are the great democratic statistic: they compare a value to *its peers* without assuming any shape. "A 5,200-dollar Saturday is the 91st percentile of Saturdays" is true whether Saturdays are bell-shaped, skewed, or bumpy — no bell required. That shape-freedom is why percentiles dominate reporting where tails matter: exam scores ("90th percentile"), website latency ("p95 response time"), and income ("the 99th percentile") are all peers-relative-to-peers claims.

One footnote you need once and then forever: **there are several defensible ways to compute a percentile from finite data** (linear interpolation between ranks, nearest-rank, and variants) and tools differ — Excel's `PERCENTILE.INC` vs `PERCENTILE.EXC`, different defaults in SQL engines and pandas. On large data the differences vanish; on a 20-value column they can move a quartile noticeably. The professional rule: know your tool's default, state it when precision matters, and never compare percentiles computed by different methods without checking. (Appendix C's cheat sheet lists the defaults.)

## 24.2 The Z-Score

The z-score is one of the smallest, most powerful formulas in this book:

```text
z = (value − mean) / standard deviation
```

It restates any value as **a number of standard deviations from its own mean**. A 4,270-dollar day against daily takings with mean 2,990, s 640: z = (4,270 − 2,990)/640 = **+2.0** — a two-sigma day. The formula's quiet achievement: it *removes the units*. Dollars, seconds, kilograms, test scores — after z, everything is on the same dimensionless ruler, "typical distances from typical", and Chapter 23's 68–95–99.7 rule applies directly: a +2.0 day happens about once per twenty days (the 95% band's outside edge); a −3.0 day is a three-in-a-thousand event; a +1.6 day is merely a good day.

Negative z = below mean; the sign matters and beginners drop it. And z is exactly the machinery inside the IQR-fence derivation from Chapter 23.4 — the fence *is* a z-score of ±2.7 built from robust ingredients. One sentence, three costumes, as promised.

## 24.3 What Z-Scores Are Actually For

**Flagging.** The daily-exceptions report: compute z for each day's takings against the trailing ninety days; flag |z| > 2. This is the analyst's on-call instrument — the same skeleton that powers fraud alerts (z of transaction size per customer), quality control (Chapter 60's control charts), and anomaly detection in its simplest honest form. Build it once as a spreadsheet or SQL query (Appendix A has it) and you own a professional tool.

**Comparing incomparables.** Which is more remarkable: Tariro's 4,270-dollar day, or her 61-customer Saturday (mean 35, s 9 → z = +2.9)? The dollars differ; the z's do not. "The Saturday *crowd* was more unusual than the Saturday *takings*" — a sentence no raw comparison can produce, and the seed of a real insight (what drove the crowd if not the spend?).

**Standardising columns.** Subtract the mean, divide by s — every column now sits on the z-ruler. This is the standard preparation for comparing many variables at once, and it is *literally* what lies under the hood of the z-tests of Chapter 26, the regression of Chapter 28, and machine learning's distance calculations (Chapter 58 gets a whiff of why unscaled columns bully scaled ones).

## 24.4 The Empirical Rule and Its Rival

Two rules, and knowing when each applies is half the exam and all of the craft:

- **The empirical rule** (68–95–99.7) holds for *normal* data. Beautiful, tight, conditional.
- **Chebyshev's inequality** holds for *any* shape: at least 75% of data lies within ±2s, at least 89% within ±3s, at least 1 − 1/k² within ±k s. Weaker, unconditional — the floor that works even when the bell is a lie.

The pairing is a moral lesson in statistical honesty: *if you can assume the bell, you get tighter promises; if you cannot, you still get promises — just humbler ones.* Daily takings, near-bell: empirical rule, −2s once a month-ish. Basket amounts, skewed: Chebyshev only — and even Chebyshev is conservative, because percentiles (shape-free) are usually the better instrument on skewed data. The craft hierarchy on any column: **histogram first; bell-ish → z and empirical; not bell → percentiles and fences.**

## 24.5 The New Dashboard Number

Tariro's whiteboard gets its most useful line yet. Beside each day's takings, the day's **percentile among the last ninety days** — "Tuesday: 2,410 (14th percentile — quiet)"; "Saturday: 4,270 (99th — best day since opening)". The owner reads percentiles instantly ("one of the best days we've had") where z-scores would need translation; the analyst keeps z internally for flagging. Same ruler, two costumes, audience-chosen — a preview of Part VI's whole philosophy: *the number is not the deliverable; the sentence the reader can act on is.*

And with the ruler in hand, the Part III ledger's biggest question — *is Sunday's 28% shortfall a pattern or luck?* — is now one step from answerable: Sunday's mean takings against the spread of days, in s-units, is exactly the calculation Chapter 26's first hypothesis test will formalise. The z you built today is the t-test's embryo.

> **From Your Toolkit — the standard ruler:** `PERCENTILE_CONT` and window-rankings in SQL (Appendix A), `(x − x̄)/s` as a one-liner in pandas (`(df.x - df.x.mean())/df.x.std()`, Chapter 34) and in Power BI measures (Chapter 40); SPSS's Descriptives panel prints z-scores on a checkbox ("Save standardized values"). Every tool you will ever touch computes both, because every analyst needs both — percentiles for shape-freedom, z for the bell's tight promises.

## Key Takeaways

- Percentiles compare a value to its peers with no shape assumptions — the democratic ruler; know your tool's method footnote.
- z = (value − mean)/s: units dissolved; |z| > 2 is a once-in-twenty event *if* the bell holds.
- z's three jobs: flag (exceptions, fraud, control), compare incomparables, standardise columns for later machinery.
- Empirical rule if bell, Chebyshev if not (75% within 2s, always); hierarchy: histogram → z or percentiles/fences.
- Percentile for the audience, z for the engine — the same ruler in the costume the reader needs.

## Practice Lab

1. Hand-z: pick three days from your daily takings (an ordinary one, the worst, the best); compute z for each by hand; write the three sentences ("a −1.9 day: quiet, not alarming" etc.).
2. The exceptions report, built: z of takings vs trailing 90 days for every day (spreadsheet or SQL — Appendix A's pattern); list every |z| > 2 day; annotate each with what you find when you look (holiday? payday weekend? nothing?). This artefact is portfolio-grade.
3. Incomparables, compared: z of the best day's takings vs z of the best day's customer count; which record is more remarkable? One sentence with both z's in it.
4. The method footnote, experienced: compute "median" three ways — `PERCENTILE.INC(…,0.5)`, `PERCENTILE.EXC(…,0.5)`, `MEDIAN` — on a 12-value column; report the (small) differences; write the one-line policy you will follow when precision matters.
5. The Sunday pre-analysis (ledger item): mean Sunday takings, mean weekday takings, the s of daily takings; express the Sunday gap in s-units; write your *informal* verdict ("about a −1.8s shortfall every week") and mark the ledger: "formal test pending Chapter 26". You are one chapter from closing your first real question.

## Further Reading

- Chapter 25 (sampling — where the population's μ and σ enter the story), Chapter 26 (the t-test — your Sunday z grows up)
- Appendix C (the statistics cheat sheet: every rule in this Part, one page)
