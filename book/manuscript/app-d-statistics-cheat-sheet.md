# Appendix D: Statistics Cheat Sheet

*Appendices — The Cookbook*

> "Which test when, in plain English — plus the formulas, the tool translations, and the reading rules. One page per spread, in bookmark form."

## The Decision Table — Which Test When

| Your question | The instrument | The tool calls |
|---|---|---|
| "What's typical?" | mean (totals logic) / median (skewed money) / mode (categories) | `AVERAGE` `MEDIAN` · `AVG` SQL · `df.mean()` · SPSS Descriptives |
| "How spread out?" | sd (individuals) / IQR (robust) | `STDEV.S` `QUARTILE` · `df.std()` · Explore |
| "Is this value unusual?" | z-score (if bell) / percentile rank (always) / IQR fence (skewed) | `(x-x̄)/s` · `PERCENTRANK` · `PERCENTILE_CONT` |
| "Two groups differ? (independent)" | Welch's two-sample t-test | `T.TEST(r1,r2,2,3)` · `ttest_ind` · SPSS Independent T · Stata `ttest y, by(g)` |
| "Same units, before/after? (paired)" | paired t-test | `T.TEST(r1,r2,2,1)` · `ttest_rel` · Paired-Samples T · `ttest a==b` |
| "Counts/proportions across categories?" | chi-square (+ Fisher's exact if cells < 5) | `CHISQ.TEST` · `chi2_contingency` · Crosstabs · `tabulate x y, chi2` |
| "Two numbers move together?" | Pearson r | `CORREL` · `pearsonr` · Correlate · `pwcorr` |
| "The line through them?" | regression (slope is the finding) | `SLOPE` `RSQ` · `linregress`/`ols` · Regression · `regress` |
| "How wrong might my estimate be?" | CI = estimate ± 2×SE | `CONFIDENCE.T` · bootstrap (App. C #24) · every SPSS/Stata table |
| "What fraction survive to month k?" | survival curve / cohort retention | pandas groupby-unstack (App. C) · KM in any stat package |
| "Which group does this belong to? (predict)" | logistic regression / classification | Ch. 57 — beyond this sheet's scope |

**Before any test:** histogram first (bell → z/t; skewed → fences, percentiles, or transform); α chosen *before* looking (0.05 default); effect size and CI reported with every p; the three explanations of any correlation (coincidence, confounding, causation) — only an argument licenses the third.

## The Formulas (the ones worth owning)

```text
mean          x̄ = Σx / n
sample sd     s = sqrt( Σ(x − x̄)² / (n − 1) )        -- n−1 for samples
z-score       z = (x − x̄) / s
IQR fence     Q1 − 1.5×IQR  and  Q3 + 1.5×IQR        -- flags ~ the outer 0.3% of a bell
SE of mean    SE = s / √n                            -- quadruple n, halve the error
95% CI        x̄ ± 2 × SE                             -- the "2" is the bell's gift (1.96 exact)
Welch's t     t = (mean₁ − mean₂) / sqrt(s₁²/n₁ + s₂²/n₂)
paired t      t = mean(differences) / (sd(diff)/√n)  -- test the differences
chi-square    χ² = Σ (O − E)² / E ;  E = row×col/grand ;  df = (r−1)(c−1)
Pearson r     r = Σ(zx·zy) / (n−1)
regression    y = a + b·x ;  b = r·(sy/sx)            -- b is the finding
margin (prop) ME = 2 × sqrt( p(1−p)/n )               -- worst case p=.5: n≈96 for ±10%, 385 for ±5%
```

## Reading Any Test Output (the six lines)

Every statistics package prints the same six lines, in every costume — read them in this order: **1)** the group/effect sizes (the finding's *size* — read first, before any p); **2)** the statistic (t, χ², F — the evidence's strength); **3)** the df (the sample's contribution); **4)** the p-value (the surprise score *if nothing were happening* — never "the probability the null is true"); **5)** the confidence interval (the honest range of the effect); **6)** n (what all of the above is worth). Report in the order: **effect (with CI), then p, then n** — "Sundays are 840 lower (95% CI: 750–930), t(206) = 18.4, p < 0.001."

## Percentile Method Defaults (the Ch. 24 footnote, in full)

Tools compute percentiles differently on finite data (interpolation vs nearest-rank): **Excel/Calc** `PERCENTILE.INC` and `QUARTILE.INC` (interpolate, inclusive); `PERCENTILE.EXC` (exclusive — can error on small n); **pandas/NumPy** default linear interpolation (≈ `INC`); **SQL** `PERCENTILE_CONT` (continuous interpolation) vs `PERCENTILE_DISC`; **SPSS/Stata** offer several (SPSS's EXAMINE defaults are documented in output footnotes — read them). Differences vanish on large n and can move a quartile on n<20: **state the method when precision matters; never compare percentiles across methods without checking.**

## The Tool Translation Table (Ch. 29's Rosetta Stone, extended)

| Task | Spreadsheet | SQL | SPSS (menus) | Stata (commands) | Python |
|---|---|---|---|---|---|
| Descriptives | `AVERAGE` `MEDIAN` `STDEV.S` | `AVG`, `PERCENTILE_CONT` | Descriptives / Explore | `summarize`, `summarize, detail` | `.mean() .median() .std()` |
| Frequencies / five-number | `QUARTILE.INC` | quartile query | Frequencies / Explore | `tabstat` | `.describe()` |
| Cross-tab | PivotTable | `GROUP BY` two cols | Crosstabs (+Chi-square) | `tabulate x y, chi2` | `pd.crosstab` |
| Independent t | `T.TEST(...,3)` | CTE arithmetic | Independent-Samples T | `ttest y, by(g)` | `ttest_ind` |
| Paired t | `T.TEST(...,1)` | CTE arithmetic | Paired-Samples T | `ttest a==b` | `ttest_rel` |
| Chi-square | `CHISQ.TEST` | hand-built E/O | Crosstabs Statistics | `tabulate, chi2` | `chi2_contingency` |
| Correlation | `CORREL` | dialect-dependent | Correlate (Pearson) | `pwcorr` | `pearsonr`, `.corr()` |
| Regression | `SLOPE` `RSQ` `INTERCEPT` | dialect-dependent | Regression | `regress` | `linregress`, `sm.OLS` |
| z-scores | formula | window arithmetic | Descriptives: "Save standardized" | `egen z = std(x)` | `(x−x̄)/s` |
| CI of mean | `CONFIDENCE.T` | arithmetic | printed by every procedure | printed / `ci` | `sem()` / bootstrap |
| Reproducible script | workbook+log | `.sql` files | Paste → Syntax `.sps` | Do-file `.do` | notebook/script |

**SPSS menu paths (Ch. 27/29's walkthrough, compact):** Frequencies (Analyze → Descriptive Statistics → Frequencies); Explore with plots (Analyze → Descriptive Statistics → Explore); Crosstabs with χ² and row % (Analyze → Descriptive Statistics → Crosstabs → Statistics → Chi-square; Cells → Row); Independent t (Analyze → Compare Means → Independent-Samples T Test — read the Levene line; if "equal variances not assumed", read that row); Paired t (Compare Means → Paired-Samples); Correlation (Correlate → Bivariate); Regression (Regression → Linear — the coefficients table is the six lines again). Paste every dialog to Syntax instead of clicking OK — the query pack, SPSS edition.

**The Stata beginner's kit (Ch. 29, with the verbs):** `import delimited`, `describe`, `summarize, detail`, `generate`, `egen`, `keep/drop`, `tabulate x y, chi2`, `ttest, by()`, `regress`, `save`; comments `*` or `//`; run via do-file; the log *is* the output trail.

## Worked Examples (the arithmetic, end to end)

### The Sunday test, every step

```text
Data: 78 Sundays, mean takings 2,150, sd 590
      390 weekdays, mean takings 2,990, sd 655

1. H0: Sunday mean = weekday mean   (α = 0.05, chosen in advance)
2. Difference: 2,150 − 2,990 = −840
3. SE of difference (Welch):
   sqrt(590²/78 + 655²/390) = sqrt(4,468 + 1,099) = sqrt(5,567) ≈ 45.7
4. t = −840 / 45.7 ≈ −18.4
5. df (Welch–Satterthwaite): ≈ 101 → look up t=−18.4 at 101 df: p < 0.0001
6. Verdict: reject H0. Sundays are lower by 840 (95% CI: −840 ± 2×45.7
   = −931 to −748). Report: "Sundays average $840 below weekdays
   (95% CI $748–$931 lower), t(101) = −18.4, p < 0.001."
```

### Chi-square, every step

```text
Cross-tab (tier × shopped this month):
             Yes   No  | row total
Gold          34    6  |  40
Silver        90   50  | 140
None         310  150  | 460
cols         434  206  | 640

E(cell) = row × col / grand:
  Gold/Yes:  40 × 434/640 = 27.1
  Gold/No:   40 × 206/640 = 12.9
  Silver/Yes: 140 × 434/640 = 94.9   Silver/No: 140 × 206/640 = 45.1
  None/Yes:  460 × 434/640 = 312.0   None/No:  460 × 206/640 = 148.0

χ² = Σ(O−E)²/E = (34−27.1)²/27.1 + (6−12.9)²/12.9 + (90−94.9)²/94.9
    + (50−45.1)²/45.1 + (310−312)²/312 + (150−148)²/148
    = 1.76 + 3.69 + 0.25 + 0.53 + 0.01 + 0.03 ≈ 5.5 + smaller terms ≈ 6.3
df = (3−1)(2−1) = 2 → p ≈ 0.04–0.06 (check every cell: all E ≥ 5 ✓)
Verdict at α = 0.05: borderline — report the effect (Gold 85% vs None 67%)
with the p and the small-cell caution, and recommend more data (Ch. 27).
```

### Reading a regression table (the SPSS/Python shape, decoded)

```text
                 coef    std err   t      P>|t|   [0.025   0.975]
const            6.24    0.81      7.70   0.000   4.66     7.82
price           −1.12    0.24     −4.67   0.000   −1.59    −0.65
R-squared 0.76   n = 18

Read, in order:
1. slope −1.12: each extra dollar of price ≈ 1.1 fewer bottles/month
2. its CI [−1.59, −0.65]: excludes zero — the effect's honest range
3. R² 0.76: 76% of bottle variation tracks price
4. p < 0.001: not noise (surprise score)
5. n = 18: one shop, 18 months — the sample-not-population caveat rides along
```

## The Honesty Rules (the ones this book enforces, final form)

1. **An average is an answer, not the answer** — mean, median, or weighted: say which, and why; check the shape first; report both when they disagree.
2. **Correlation is not causation** — three explanations always; confounders named; the experiment is the licence.
3. **A sample is not a population** — every number from data is an estimate with an error; the CI is the honest form; "is it narrow enough to decide?" is the analyst's question.
4. **Significance is not importance** — effect size + CI + p, always; the 20th test on nothing is "significant" once; declare the question before running.
5. **Missing data is data about the data** — MCAR you may drop, MAR you must model, MNAR you must bound and declare; imputed values carry flags and disclosure sentences.

*Print this appendix if you print one thing: the decision table for the question, the formulas for the arithmetic, the six lines for the output, the five rules for the conscience.*
