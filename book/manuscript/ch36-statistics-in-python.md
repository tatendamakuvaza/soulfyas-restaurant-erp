# Chapter 36: Statistics in Python — the Same Answers, in Six Lines

*Part V — Python: From Zero to Dangerous*

> "Part IV gave you the courtroom. scipy is the courtroom, motorised — with every case you have already argued, one line each."

### In this chapter you will learn

- scipy and statsmodels: the two statistics libraries, and their division of labour.
- Every Part IV test, re-run: t-tests, chi-square, correlation, regression — in lines, not menus.
- Reading the outputs: p-values, statistics, and confidence intervals as printed objects.
- One new capability statistics alone couldn't give: the bootstrap, intuitively and in five lines.
- The three-tools answer: SPSS vs Python vs spreadsheets — when each, honestly.

## 36.1 The Two Libraries

**scipy.stats** is the workhorse: the standard distributions and tests, fast and minimal. **statsmodels** is the report-writer: the same models with full statistical output — coefficients, intervals, diagnostics, the six lines every test prints (Chapter 29's SPSS tables, in text form). The working division: scipy to *test*, statsmodels to *read everything about the model*. Both ship with Anaconda:

```python
from scipy import stats
import statsmodels.api as sm
```

## 36.2 The Re-Runs

Every analysis of Part IV, now as code. Run them against your own Part IV numbers — the reconciliation is the point (same data, same statistics, three tools; when all three agree, you have *verified* your verification).

**The Sunday test (Ch. 26)** — two independent groups:

```python
sun = daily[daily["weekday"] == "Sunday"]["amount"]
week = daily[daily["weekday"] != "Sunday"]["amount"]

t_stat, p_value = stats.ttest_ind(sun, week, equal_var=False)
print(f"Sunday t = {t_stat:.1f}, p = {p_value:.6f}")
# Sunday t = -18.5, p = 0.000000  -- the ledger's closure, reproduced
```

(`equal_var=False` is Welch's t — the version that does not assume equal spreads; the professional's default. Note the sign: Sunday first means negative t. Statistics identical to Part IV's, tool irrelevant.)

**The paired test (Ch. 26)** — before/after the price rise, per item:

```python
t_stat, p_value = stats.ttest_rel(before_bottles, after_bottles)
# t = -4.6, p = 0.0008 -- the oil verdict, reproduced
```

**Chi-square (Ch. 27)** — the survey cross-tab:

```python
table = pd.crosstab(survey["tier"], survey["shopped_this_month"])
chi2, p, dof, expected = stats.chi2_contingency(table)
print(f"chi2 = {chi2:.2f}, dof = {dof}, p = {p:.3f}")
# chi2 = 5.5, dof = 2, p = 0.064 -- suggestive, not established; reproduced
```

And the expected-count warning, mechanised: `expected.min() >= 5` is now an `assert` in your code — the cell-count rule enforced by the machine, not the memory.

**Correlation and the line (Ch. 28)**:

```python
r, p = stats.pearsonr(oil["price"], oil["bottles"])
slope, intercept, r_value, p_value, se = stats.linregress(oil["price"], oil["bottles"])
print(f"r = {r:.2f} (p = {p:.5f}); slope = {slope:.2f} bottles per dollar")

model = sm.OLS(oil["bottles"], sm.add_constant(oil["price"])).fit()
print(model.summary())     # the SPSS-grade table: CIs, R-squared, everything
```

`linregress` gives the slope sentence ("a dollar costs a bottle"); `model.summary()` gives the full argument — including the 95% confidence interval on the slope that Part IV's honest paragraph demanded ([−1.6, −0.7], say). Read that summary block once, unhurriedly: you now know every line in it (coef, std err, t, P>|t|, [0.025, 0.975] — statistic, surprise, interval: the courtroom's paperwork, complete).

## 36.3 The Bootstrap: A New Superpower

One Part IV idea gets *easier* in code than in theory: the confidence interval. The **bootstrap** — resample your data with replacement, recompute the statistic, watch its spread — is the sampling distribution of Chapter 25, *demonstrated instead of derived*:

```python
import numpy as np

means = [daily.sample(frac=1.0, replace=True)["amount"].mean()
         for _ in range(2000)]
lo, hi = np.percentile(means, [2.5, 97.5])
print(f"mean daily takings: {daily['amount'].mean():.0f} "
      f"(95% CI {lo:.0f} to {hi:.0f})")
```

Two thousand re-runs of the world (Chapter 25's phrase, now literal), and the interval falls out of the spread of re-run means — no formula, no normality assumption, the same logic working on medians, on ratios, on any statistic a formula finds difficult. The bootstrap is how modern statistics handles the awkward cases, and it is yours in five lines because you own the *concept*: the sampling distribution is a picture of "what my statistic would say across re-runs" — and the computer can simply *have the re-runs*.

## 36.4 Three Tools, Honestly

The question every learner asks: *if Python does all this, why learn statistics in SPSS or spreadsheets at all?* The honest answer, tool by tool — and it is a professional's answer, not a tribal one:

| Tool | Statistics for... | Its edge | Its cost |
|---|---|---|---|
| Spreadsheet | first looks, one-offs | zero friction, everyone has it | no audit trail, silent errors |
| SPSS/Stata | governed/research workflows | validated procedures, standard tables | licensing, point-and-click walls |
| Python | automated/repeatable analysis | free, programmable, scales, bootstrap | you must know what you're asking for |

The deep point is the last cell of the third row: **menus protect you from choices you don't know you're making; code exposes every choice you make.** `equal_var=False` is a decision you *saw*; the SPSS dialog's default is a decision you *missed*. Neither culture is safe by default — safety is knowing the six lines every test prints, whichever tool prints them. That fluency is now yours, three times over; Chapter 52's interview questions will test precisely it.

> **From Your Toolkit — the sixth instrument, everywhere:** this chapter is the bridge to everything remaining: Project 4's churn analysis is a t-test plus a groupby; Chapter 37's automated report embeds these exact lines; Chapter 58's machine learning *is* `model.summary()`'s descendants at scale; and the A/B-testing culture of tech companies (Chapter 57) runs these six lines at industrial size. The tests are six; the tools are many; the fluency is one.

## Key Takeaways

- scipy.stats to test, statsmodels to read everything; both ship with Anaconda; both print the six lines you already know.
- Every Part IV test reproduced in 1–3 lines (t, paired t, chi-square, correlation, regression) — reconcile against Part IV's numbers to complete the three-tool verification.
- Welch's t (equal_var=False) is the professional default; assert expected ≥ 5 for chi-square — decisions visible, assumptions mechanised.
- The bootstrap: 2000 re-runs, take the spread — CIs for anything, no formulas; Chapter 25's picture, computed.
- Menus hide choices, code exposes them; spreadsheet/SPSS/Python divide by workflow, and fluency — not tribe — is the safety.

## Practice Lab

1. The reconciliation run: re-run all four Part IV analyses (Sunday t, paired oil, chi-square, oil regression) on your data; build a Markdown table: Part IV result | SPSS-or-sheet result | Python result — three tools, one column of numbers; certify it.
2. The summary() read: from `model.summary()`, write the four-sentence finding (slope, its CI, R², p) in Chapter 28's professional-paragraph format; underline which sentence each summary number funded.
3. The bootstrap, twice: CI of the mean daily takings (above), then of the *median* basket — a statistic formulas find awkward, the bootstrap doesn't care; write one sentence on why the median's interval is the honest one for money.
4. The assumption audit: re-run the Sunday test with `equal_var=True` vs `False`; note the (small) difference; then write the one-paragraph "which did I choose and why" for the report — the visible-choice habit, practised.
5. The test-picker quiz (self-made): write five business questions from Tariro's world, each answerable by exactly one of the six instruments; shuffle them; answer them a week later without notes; grade yourself. This quiz is Chapter 52's interview, rehearsed.

## Further Reading

- Chapter 37 (the tests join the automated report), Chapter 58 (regression's descendants)
- *Think Stats* (Downey) — statistics *through* Python, free online; the natural continuation of this chapter
