# Chapter 25: Samples and Populations

*Part IV — Statistics Without Fear*

> "You will never see the population. Everything you will ever do as an analyst is peek at a sample and argue, carefully, about the whole."

### In this chapter you will learn

- Population vs sample — the distinction that gives statistics its purpose.
- Sampling distributions: what a statistic *does* when you repeat it — the deep idea.
- The Central Limit Theorem, plainly stated, and why it is the luckiest fact in the field.
- Standard error: the standard deviation of a statistic; the ruler of "how wrong might this be".
- Confidence intervals and margins of error — built from the above, not memorised.

## 25.1 The Distinction That Runs Everything

Honesty Rule 3, from Chapter 2, now gets its theory. The **population** is every unit you *want* to speak about: every sale Tariro would ever make, every customer she will ever serve, every basket in every shop like hers. The **sample** is the part you can actually see: eighteen months of one shop's till. Statistics exists because these are different — and its entire architecture is the careful argument from the seen to the unseen.

The vocabulary you must own cold: **parameter** — a number about the population (μ, σ; fixed, unknown); **statistic** — a number computed from the sample (x̄, s; known, but it *varies* if you re-draw the sample). A statistic is an *estimator* of its parameter: x̄ estimates μ. The professional's mental tag on every reported number: *this is a sample statistic standing in for a population parameter — with what care?*

Tariro's data is, technically, a *complete census* of her shop's past — but the moment she asks "will my Sundays stay weak?", the past becomes a sample of the shop's *ongoing behaviour* (the population). Almost every business question quietly converts history into a sample of the future; noticing the conversion is the analysis.

## 25.2 What a Statistic Does When You Repeat It

The deep idea, built by hand. Suppose we treat Tariro's 6,420 sales as a population, and we estimate the average basket from samples of 50 sales each. Take sample 1: x̄₁ = 8.10. Sample 2: x̄₂ = 8.95. Sample 3, 4, 5... each sample gives a *different* mean. Now — the pivot — collect those sample means and histogram *them*: they have their own distribution (the **sampling distribution** of the mean), their own centre (it clusters on μ, the population mean — the estimator is *unbiased*), and their own spread (much tighter than the raw data: means wobble less than individuals).

You will never, in a job, actually draw a hundred samples. But every formula in the rest of this book is a shortcut *predicting* what that histogram would look like — so you must be able to picture it, and now you can: **the sampling distribution is the histogram of "what my statistic would say if I re-ran the world", and statistics is the science of its shape.**

## 25.3 The Luckiest Fact

The **Central Limit Theorem** (CLT): the sampling distribution of the mean approaches a **normal distribution** as the sample size grows — *whatever the shape of the raw data*. This is the luckiest fact in the field and the reason the bell runs the world: baskets themselves are viciously right-skewed (whales) — but *averages of baskets* are nearly normal, at n around 30+.

Verify it in your spreadsheet in ten minutes (this exercise is the single best ten minutes in Part IV): take 200 random samples of 50 sales each (sample rows with `=RANDBETWEEN` picks or your tool's sampling function), compute each x̄, histogram the 200 x̄'s. The raw amounts histogram is a skewed mess; the sample-means histogram is a *bell*, centred on 8.42. You have just watched the CLT turn skew into symmetry — the raw material of Chapter 23's "bells fit sums, not money" rule, now demonstrated by your own hand.

## 25.4 Standard Error

The sampling distribution's spread has its own name: the **standard error** (SE), and for a mean:

```text
SE = s / √n        (s = sample standard deviation, n = sample size)
```

On Tariro's data: s ≈ 12.10, n = 50, so SE = 12.10/7.07 ≈ **1.71**. Read it as a sentence: "sample means of 50 baskets typically land about 1.71 dollars from the true mean." The formula's two levers are the whole of practical statistics: **bigger n shrinks error** (with the square root — quadruple your data, halve your error: the most important business fact about data collection); **noisier data (bigger s) inflates it**.

Distinguish coldly: **standard deviation** describes individuals; **standard error** describes statistics. "Sales vary by about 12 dollars" (s) vs "our average-basket estimate is wrong by about 1.7 dollars" (SE). Mixing these two is the most common statistical sentence-error in business reporting, and now you cannot unsee it.

## 25.5 Confidence Intervals

The standard error plus the bell gives the **confidence interval** — the honest answer to "what is the average basket?":

```text
x̄ ± 2 × SE   (the "95% interval"; 2 is the CLT's gift from the 95% rule)
```

8.42 ± 2(1.71) → **(5.00, 11.84)** for n = 50. With the full 6,420 sales (SE = 12.10/√6420 ≈ 0.15): 8.42 ± 0.30 → **(8.12, 8.72)**. Same data, more of it, tighter honest claim — the interval *earns* its narrowness by n.

The correct reading, stated once and forever: a 95% CI means *the procedure* captures the true mean in 95% of its uses — not "95% probability that μ is in this particular interval". Precision here is not pedantry; the sloppy reading is how CIs get abused into certainty they never promised (a Chapter 2 skepticism target, now with machinery). The **margin of error** is just the ± part (2×SE, or 1.96×SE exactly); the news's "±3 points" is this chapter, every night, uncredited.

And the honest question every interval should provoke: *is my interval narrow enough to decide?* (8.12, 8.72) supports "charge for bags at 9.00 thresholds"; (5.00, 11.84) supports nothing but "collect more data". Statistics does not just measure uncertainty — it tells you when to go get more data, which is a budget decision.

> **From Your Toolkit — the argument's engine:** SE and CI appear as `CONFIDENCE.T` in spreadsheets, confidence intervals printed by every SPSS/Stata procedure (Chapter 29), pandas' `.sem()` and statsmodels' full outputs (Chapter 36), and the error bars on every serious dashboard chart (Chapter 42). The A/B tests of Chapter 26, the survey margins of Chapter 27, and the forecast bands of Chapter 60 are all this chapter in costume — a statistic, its SE, and the bell's arithmetic.

## Key Takeaways

- Population (parameters, fixed, unseen) vs sample (statistics, seen, varying); almost every business question silently samples the future.
- The sampling distribution is "what my statistic would say across re-runs" — the picture behind every remaining formula.
- CLT: means of 30+ items are near-normal regardless of raw shape — skew in, bell out; verify it once by hand and own it.
- SE = s/√n: bigger n tightens (√n), noisier s loosens; SD describes individuals, SE describes statistics — never mix the sentences.
- CI = x̄ ± 2×SE, read as procedure reliability; and the decision question: is the interval narrow enough to act, or is more data the answer?

## Practice Lab

1. The ten minutes: the 200-samples-of-50 exercise; paste both histograms (raw amounts; sample means) into your log with the two caption sentences. This pair of pictures is the CLT, owned.
2. The lever drill: compute SE for n = 10, 50, 200, 1000 on the basket data; write the sentence comparing how much data each quadrupling buys; and answer: to halve the error again after n=1000, how many sales do you need?
3. The interval ladder: 95% CIs for average basket at n = 50, 200, and the full dataset; write the three intervals and, for each, one decision it could and could not support.
4. The sentence audit: find three "average" claims in any report (Tariro's, a news article, your own Part II report — be honest) and restate each with its interval or an explicit "no interval computed"; note how the claims' persuasiveness changes.
5. The design question (ledger): Tariro wants to survey 30 customers about a planned Sunday promotion; using the s of individual baskets, what margin of error will her sample proportion carry (SE of a proportion: √(p(1−p)/n), worst case p=0.5)? Write the "is 30 enough?" memo — this exact calculation returns in Chapter 27.

## Further Reading

- Chapter 26 (the tests — SE plus a null hypothesis), Chapter 27 (surveys, where sampling is the whole job)
- *The Art of Statistics* (Spiegelhalter) chapter 8 — sampling, from the master
