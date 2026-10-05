# Chapter 27: Categories and Surveys

*Part IV — Statistics Without Fear*

> "Half the world's data is counts. It deserves better than being forced into averages."

### In this chapter you will learn

- Categorical data analysis: percentages done honestly, and the count-of-what trap.
- Cross-tabulations: the pivot table's statistical soulmate.
- Chi-square: the courtroom for counts, built by hand once.
- Surveys from first principles: questions, sampling, and margins of error.
- Tariro's customer survey — designed, executed, and analysed, in SPSS's menus step by step.

## 27.1 Counts Are Data Too

Payment types, suburbs, loyalty tiers, weekdays, buy/didn't-buy — categorical data has no mean, and averaging it (or, worse, "averaging the codes") is a category error that production dashboards commit weekly. The honest statistics of categories are **counts, percentages, and cross-tabs** — with three rules that keep them truthful:

1. **Percent of what?** — every percentage declares its denominator. "23% are members" (of customers) vs "31% of revenue is members'" (of dollars) differ because the denominators differ. The unlabelled percentage is the most common lie in business reporting.
2. **Count beside rate.** "Suburb X: 80% repeat-purchase rate" on n = 5 is a headline made of air; the count rides along, always (Chapter 10's pairing habit, categorical edition).
3. **Rare categories and the small-denominator trap.** Percentages of tiny groups swing wildly; collapse small categories into "Other" (stated) or report them as counts only.

## 27.2 The Cross-Tab

A **cross-tabulation** is category-by-category counts — the pivot table (Chapter 10) with its statistical hat on. Tariro's loyalty question in cross-tab form: rows = loyalty tier (Gold/Silver/none), columns = "shopped this month?" (yes/no):

```text
             | Shopped | Not shopped | Row total
Gold         |    34   |     6       |    40
Silver       |    90   |    50       |   140
None (no card)|   310  |    150      |   460
Column total |   434   |    206      |   640
```

Read a cross-tab by **row percentages** (each row's counts as % of its row total): Gold 85% shopped, Silver 64%, none 67%. The eye's question: *do the rows differ?* Gold looks special; Silver looks like everyone else — and that pattern (loyal core, then nothing) is the planted design made visible. The cross-tab shows the pattern; the courtroom decides if it is real; enter chi-square.

## 27.3 Chi-Square, by Hand Once

**Chi-square (χ²)** tests whether two categorical variables are *associated* — whether the table's rows differ more than sampling noise explains. The logic is the courtroom's, applied to each cell: compare **observed** counts (O) against **expected** counts (E) — what each cell *would* contain if the variables were completely independent (E = row total × column total / grand total) — and total the standardized surprises:

```text
χ² = Σ (O − E)² / E     over every cell

Gold/Shopped:    E = 40×434/640 = 27.1;  (34−27.1)²/27.1 = 1.76
Gold/Not:        E = 40×206/640 = 12.9;  (6−12.9)²/12.9 = 3.69
Silver/Shopped:  E = 140×434/640 = 94.9; (90−94.9)²/94.9 = 0.25
... (all six cells summed) χ² ≈ 5.5
```

Degrees of freedom = (rows−1)(cols−1) = 2; the χ² table (or any tool) gives **p ≈ 0.064** — *fail to reject* at α = 0.05. The honest verdict: the tier-vs-activity association is *suggestive but not established*; Gold's 85% is built on 40 customers, and counts that small wobble. (Note what the test did *not* say: "no difference exists" — it said the evidence is not yet strong enough to convict. Collect more Gold members, or more months, and retry.)

Two craft rules for χ²: **expected counts ≥ 5 per cell** (the approximation degrades; collapse categories or use the exact test — tools offer "Fisher's exact" for small cells); and **df is not a formality** — it is how many cells could freely vary, and the table's p-value hangs on it.

## 27.4 Surveys, First Principles

Tariro's Sunday-promotion question (Chapter 25's memo promised this) needs data nobody has: what customers *would* do. The survey is the instrument, and surveys fail at design long before analysis. The craft in five rules:

1. **Define the population and the frame.** Population: all shoppers. Frame: who you can actually reach — customers in the shop next week (which misses the Sunday-stayers at home; write that limitation down).
2. **Sample honestly.** Every shopper a chance, no hand-picking friends (convenience sampling is fine for exploration, poison for inference); aim for n from the Chapter 25 calculation (30 → ±18% at worst; for a real margin you want 100+ → ±10% or better; 385 → ±5% — the famous n; diminishing √n returns beyond).
3. **Ask one thing at a time.** "Would you shop Sundays if we ran double points?" — not "…and would you also like longer hours?" Double-barrelled questions manufacture uninterpretable answers.
4. **Offer a scale with a neutral, and label it.** A 5-point from "Definitely would" to "Definitely would not" with a middle "Unsure" — balanced, labelled, and analysable as counts per level (not averaged into a "2.7 attitude").
5. **Pretest on five people.** Every question that five humans misread is a question fixed before it lies to you at scale.

## 27.5 The Survey, in SPSS

The chapter's deliverable: Tariro's survey, run for real (n = 112 in-shop respondents over two Saturdays), analysed in **SPSS** — the classic statistics package you will meet in research, government, health, and market-research work (installation: the free trial or your institution's licence; Appendix D's tool tables carry the equivalents). SPSS's philosophy is the *opposite* of SQL's: no code visible, menus all the way — and behind every menu is a chapter you have already lived. The run-through:

1. **Enter the data** — Variable View: name each column (`sunday_intent`, `tier`, `usual_spend`), set Type (numeric/string) and, crucially, **Value Labels** (1 = "Definitely would", 2 = "Probably would"… 5 = "Definitely would not") — SPSS's equivalent of a data dictionary, and where categorical hygiene happens. Data View: one row per respondent.
2. **Frequencies** — Analyze → Descriptive Statistics → Frequencies: counts and percentages per question. The first honest look: 18% "Definitely would", 26% "Probably would", 22% unsure…
3. **Cross-tab with the test** — Analyze → Descriptive Statistics → Crosstabs: `sunday_intent` by `tier`; click Statistics → Chi-square; Cells → Row percentages. The output table is Chapter 27.2's cross-tab with the χ², df, and p appended at the bottom — read exactly as this chapter taught: effect (the row percentages) first, then the surprise score, then the small-cell warnings SPSS prints honestly ("X cells have expected count < 5" — you know that sentence now).
4. **The finding, written properly**: "Among surveyed shoppers (n = 112), intent to shop Sundays was higher among loyalty members (51% definitely/probably would) than non-members (37%); χ²(4) = 9.8, p = 0.045 — a suggestive but modest association from a convenience sample; the promotion should be trialled and *measured in till data*, not assumed from the survey."

That last clause is the survey-analysis wisdom: surveys say what people *say*; tills say what people *do*; the professional uses the survey to design the experiment and the till to judge it — which is exactly the four-Sunday trial Project 4's dashboard will measure.

> **From Your Toolkit — counts everywhere:** cross-tabs return as pandas' `crosstab` (Chapter 34), Power BI matrix visuals (Chapter 42), SQL's `GROUP BY two columns` (Chapter 16 — you have been cross-tabbing since Part III); chi-square lives in `scipy.stats.chi2_contingency` (Chapter 36) and every statistics package ever shipped. Survey margins of error are the Chapter 25 arithmetic on proportions — the "±3 points" of news polls, demystified forever.

## Key Takeaways

- Categorical data's honest statistics: counts, percentages (denominator declared), cross-tabs — count beside rate, always.
- Chi-square: observed vs expected per cell, χ² = Σ(O−E)²/E, df = (r−1)(c−1); expected ≥ 5 per cell; p ≈ 0.064 means suggestive, not established.
- Surveys fail at design: define the frame, sample honestly, one thing per question, labelled scales, pretest on five.
- SPSS is menus over this chapter: Variable View labels, Frequencies, Crosstabs + chi-square — you can read the output because you built the logic by hand.
- Surveys say; tills do. Design the trial with the survey; judge it with the till.

## Practice Lab

1. The hand χ²: complete the six-cell computation on the loyalty cross-tab above; reconcile your χ² against a tool (SPSS if installed, or a spreadsheet's `CHISQ.TEST`); write the verdict sentence with effect, statistic, and p.
2. The denominator audit: find five percentages in your Part II report or a news article; label each denominator; rewrite the two that were ambiguous into honest sentences.
3. Design Tariro's survey properly: write five questions (one at a time, labelled scales), the sampling plan with its stated limitation, and the n you would need for a ±5% margin on the key proportion (Chapter 25's formula — show the arithmetic).
4. SPSS (or spreadsheet equivalent): enter a 30-row mini-survey, run Frequencies and Crosstabs with chi-square, and write the four-line finding in the Chapter's format; if SPSS is unavailable, build the identical outputs with pivots + CHISQ.TEST and note the translation.
5. The say/do memo: one page for Tariro — what the survey suggests, its three limitations (frame, n, self-report), and the four-Sunday trial design (what till metric will decide, what threshold counts as success). Portfolio-grade; keep it.

## Further Reading

- Chapter 29 (SPSS and Stata, properly), Chapter 36 (chi-square in Python)
- *Asking Questions* (Bradburn, Sudman, Wansink) — survey craft from the people who built the field
