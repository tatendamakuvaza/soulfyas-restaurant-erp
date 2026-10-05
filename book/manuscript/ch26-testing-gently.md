# Chapter 26: Testing, Gently — Hypothesis Tests by Counting

*Part IV — Statistics Without Fear*

> "A hypothesis test is a courtroom for a number. The null hypothesis is 'nothing happened' — and you, the analyst, are the prosecution."

### In this chapter you will learn

- The logic of testing: null hypothesis, evidence, and how surprising is too surprising.
- p-values, finally defined without flinching — and the two wrong readings of them.
- The Sunday question, formally closed: a two-sample t-test, by hand and by tool.
- The before/after question: paired tests, and why pairing is a gift.
- Significance vs importance, and the three honest questions every test should end with.

## 26.1 The Courtroom

The ledger's first question — *is Sunday genuinely weaker, or is that the noise of ordinary weeks?* — becomes a test. The logic, which is a courtroom's:

- **Null hypothesis (H₀)**: nothing happened — Sunday's *true* mean takings equal the weekday's. (Innocent until proven guilty: difference = 0.)
- **Alternative (H₁)**: something happened — Sundays differ.
- **Evidence**: the data — Sunday mean 2,150 vs weekday mean 2,990.
- **The question the test answers**: *if nothing were really happening, how surprising is evidence this strong?* If "very" — stronger than chance serves up, say, one time in twenty — we convict: reject H₀, declare the difference real.

That last clause is the **significance level**, α, chosen in advance (0.05 is the convention; 0.01 for stricter). It is the court's standard of proof, and choosing it *before* seeing evidence is not ceremony — it is the difference between testing and rationalising.

## 26.2 The p-Value, Without Flinching

The **p-value**: the probability of seeing evidence at least this strong, *if the null were true*. Not "the probability the null is true" (wrong reading #1 — it assumes the null to compute, so it cannot measure the null's own chances). Not "the probability the result is a fluke" (wrong reading #2, the same error in casual clothes). It is a *conditional surprise score*: p = 0.03 means "in the nothing-happened world, a gap this big shows up 3% of the time."

The decision rule, mechanical and safe: **p < α → reject H₀; p ≥ α → fail to reject** (never "accept the null" — failing to convict is not proving innocence; absence of evidence is evidence of absence's *weakness*, nothing more). Two error types, named once, remembered by asymmetry: **Type I** = convicting the innocent (false alarm, false positive — a "significant" Sunday effect that isn't); **Type II** = acquitting the guilty (missed effect). α controls Type I directly; sample size and effect size control Type II. Analysts guard Type I like a budget, because a false alarm sends the business chasing ghosts.

## 26.3 The Sunday Test, Closed

Two independent groups (Sunday days vs weekday days), comparing means: the **two-sample t-test** — the z-machinery of Chapter 24 wearing a small-sample correction (Student's t: slightly wider than the normal for small n, converging to it as n grows — every tool has it built in; Appendix C states the formula). The arithmetic skeleton, computed honestly:

```text
Sunday days:  n₁ = 78,  mean₁ = 2,150, s₁ = 590
Weekday days: n₂ = 390, mean₂ = 2,990, s₂ = 655
difference = 840
SE of difference = √(s₁²/n₁ + s₂²/n₂) = √(4468 + 1099) ≈ 45.7
t = 840 / 45.7 ≈ 18.4
```

A t of 18.4 against roughly 200 degrees of freedom: p < 0.0001 — far past any α you would ever set. **Verdict: reject H₀. Sunday's shortfall is real** — in the nothing-happened world, a gap this consistent across 78 Sundays essentially never occurs. The ledger's first formal closure, and notice what the test added to the Chapter 24 informal z: a *probability attached to the surprise*, which is what "significance" means — nothing mystical, just surprise, measured.

In a tool, the same test is three clicks (Analysis ToolPak → t-Test: Two-Sample; SPSS → Analyze → Compare Means → Independent-Samples T Test; Python/Excel functions in Appendix C) — but you can now *read the output*, which is the skill: the t, the df, the p, and the group means it was all computed from.

## 26.4 Pairing: Before and After

The price-rise question has a different shape: *the same items*, before and after month 9 — two measurements on one subject. That is the **paired** design, and pairing is a gift: each item serves as its own control, the week-to-week noise cancels, and the test sharpens. Cook oil quantities per month per item, before vs after: compute each item's *change*, then test whether the mean change is zero (a one-sample t-test on the differences — that is all a paired t-test is):

```text
mean change in monthly quantity: −1.3 bottles per item
SE of change ≈ 0.28,  t = −1.3/0.28 ≈ −4.6,  df = 11  →  p ≈ 0.0008
```

Reject H₀: **the price rise cut quantities, really** — closing ledger question #2 (the quantity-led collapse from Q4, now with a p-value on it). The rule of craft: *if your data has a natural pairing (before/after, matched stores, same customer twice), never unpair it* — the unpaired test pays for its independence with noise, and noise is paid for in missed findings.

## 26.5 Significance Is Not Importance

The discipline that separates statisticians from significance-spitters:

- **A huge n makes trivial differences significant.** 6,420 sales will "significantly" detect a 2-cent basket difference. So what? The effect size — the difference itself (840 dollars per Sunday; −1.3 bottles per item) — is the business number; the p-value only certifies it is not noise. Report both, always: *"Sundays are 840 dollars lower (95% CI: 750–930), p < 0.001."*
- **A tiny n hides real effects** (Type II): "not significant" on 12 observations is a shrug, not a verdict.
- **The three honest questions** ending every test: (1) *How big is the effect, with its interval?* (2) *Was α chosen before looking?* (3) *Is this the first test of this question, or the fourth attempt to find something?* — the multiple-comparisons problem, probed gently: run 20 tests on nothing and one will be "significant" at 0.05 by luck (p-hacking's mechanism; Chapter 29's SPSS output makes it easy to commit accidentally; the professional defence is declaring the question before running the numbers).

> **From Your Toolkit — the courtroom travels:** every tool in this book runs these tests from menus or one-liners — `T.TEST` in spreadsheets, SPSS/Stata dialogs (Chapter 29), `scipy.stats.ttest_ind`/`ttest_rel` in Python (Chapter 36), and the A/B-testing world of tech is this chapter industrialised (Chapter 57). The t, the p, the effect size, the CI: learn to read them once, and every output you ever meet is the same six lines.

## Key Takeaways

- Testing is a courtroom: H₀ "nothing happened", evidence, and "how surprised should we be?" — with α set in advance.
- p-value = probability of evidence this strong *if H₀ is true*; p < α rejects; failing to reject is not accepting.
- Type I (false alarm) is guarded by α; Type II (missed effect) by n and effect size; Sunday's t = 18.4, p < 0.0001 — closed.
- Paired data: test the differences — pairing cancels noise; the price rise cut quantity (t = −4.6, p ≈ 0.0008) — closed.
- Effect size + CI + p, always; significance ≠ importance; and beware the twentieth test.

## Practice Lab

1. By hand, then by tool: recompute the Sunday t-test on your own data (the group stats, SE, t); then run `=T.TEST(...)` or the ToolPak and reconcile the p-value; paste both into the log with the ledger's question number it closes.
2. The paired version: before/after month-9 *revenue* per item (not just oil) as a paired test; write the finding with effect size, CI, and p — and one sentence on which framing (paired on items vs unpaired on months) you trust more, and why.
3. The significance-importance drill: invent two findings — one significant-but-trivial, one important-but-insignificant (small n) — written exactly as you would report them; hand both to a friend and ask which decision they would change. (The correct answer: neither, until effect size is read.)
4. The p-hacking demonstration: take 20 random splits of weekday takings (e.g., odd vs even sale_ids) and test each; count your "significant" results; write the one-sentence lesson and pin it above your desk.
5. Ledger day: every question opened since Chapter 2 gets a status — closed with a test (cite it), closable with a test (name it), or descriptive-only (say so). This document is Part IV's real deliverable and Project 3's spine.

## Further Reading

- Chapter 27 (categories and surveys — chi-square and proportions), Chapter 29 (the same tests in SPSS and Stata)
- *The Art of Statistics* (Spiegelhalter) chapter 13 on p-values; the American Statistical Association's six principles on p-values (short, sobering)
