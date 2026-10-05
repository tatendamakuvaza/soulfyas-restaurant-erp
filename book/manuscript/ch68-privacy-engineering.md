# Chapter 68: Privacy Engineering — Sharing Data Without Sharing People

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "Anonymised" is a promise, not a method; differential privacy is a method.

### In this chapter you will learn

- Why anonymisation keeps failing: the re-identification graveyard and the matching game.
- k-anonymity and its cracks: homogeneity and background knowledge.
- Differential privacy's one idea: calibrate noise to the question, with a budget.
- The numbers to feel: what ε = 1 versus ε = 0.1 does to a count.
- Local versus central DP, and where each belongs.
- The practical programme: minimisation, tiered access, aggregation, and audits.

## 68.1 From the Floor to the Frontier

Chapter 54 set the privacy floor for the hardest case (health data): minimum necessary, the harm test, small-cell suppression. This chapter builds the floor into a discipline, because the floor keeps failing in a specific, repeatable way: **someone "anonymises" a dataset by deleting names, and a motivated stranger re-identifies it anyway.**

The graveyard is well-populated: the medical records distinguished by the trio of attributes in the classic studies; the "anonymous" browsing histories matched to public social media; the mobility traces where four spatio-temporal points identify most individuals. The pattern every case shares: **the attacker brings their own data** — a voter roll, a social graph, a newspaper's court reports — and matches it to yours. The lesson is structural, not procedural: privacy that depends on what the attacker *doesn't know* is not privacy; it is a waiting list.

## 68.2 k-anonymity and Its Cracks

The first formal answer: ensure every record is indistinguishable from at least k−1 others on every combination of quasi-identifiers (age band, suburb, admission date). It is a real discipline — generalise and suppress until the crowd is thick. But two cracks: **homogeneity** (all k records share the sensitive value, so the crowd protects nothing) and **background knowledge** (the attacker's extra data thins the crowd from outside). l-diversity and t-closeness patch the cracks and open others; the family's honest summary is that k-anonymity is a strong *process* discipline (it forces you to think in crowds) with an unfixable *guarantee* problem (the guarantee depends on the attacker's ignorance).

## 68.3 Differential Privacy: Calibrated Noise

Differential privacy flips the guarantee: instead of promising the attacker knows little (unprovable), promise that **any single person's presence changes the output by at most a bounded amount, no matter what else the attacker knows.** The mechanism for a count is almost insultingly simple — add random noise scaled to 1/ε:

```python
def dp_count(rows, predicate, epsilon):
    true_n = sum(1 for r in rows if predicate(r))
    scale = 1.0 / epsilon
    return true_n + np.random.laplace(0, scale)
```

And the budget ε (epsilon) is the honesty dial — smaller ε, more privacy, more noise. The numbers to feel, on a query for a rare subgroup:

| Setting | Noise (std ≈ 1.4/ε) | A true count of 20 comes back as... |
|---|---|---|
| ε = 1.0 | sd ≈ 1.4 | 18–22 (usually usable) |
| ε = 0.1 | sd ≈ 14 | 6–34 (the signal drowns) |

The trade is now explicit and quantitative: **stronger privacy buys noisier answers, and the noise is a price you can compute before you pay it.** The second, subtler idea is the **budget**: each query spends ε, and the spend composes — an analyst asking 50 questions is 50 leaks, so the system metering the budget (not the analyst) is the architecture. This is why real deployments wrap a **privacy accountant** around the query layer: per-user, per-day budgets, and answers that degrade loudly rather than silently.

## 68.4 Local versus Central

- **Central DP** — the curator holds raw data and adds noise to answers. Accurate; requires trusting the curator completely.
- **Local DP** — each user randomises *before* sending (the "coin flip" protocols: answer honestly with probability p, randomly otherwise). No curator to trust; much more noise for the same ε — the price of removing trust.

The mapping to products is direct: central DP for a statistics office publishing tables (the census pattern), local DP for telemetry where the collector should never see the raw answer (browser vendors' usage stats). **From Your Toolkit — SQL:** the practical bridge from where you already work — most "DP" work in an organisation starts as *aggregation discipline in the query layer*: pre-built aggregate views, suppression rules, and query logs, which is exactly the plumbing an accountant needs when real budgets arrive.

## 68.5 The Practical Programme

For the practitioner who will not deploy a DP system this quarter but holds data this afternoon:

1. **Minimise at extract** — the analysis extract carries only the columns the question needs (Chapter 54's floor, now policy).
2. **Tier the access** — raw data to named stewards; aggregates to everyone; row-level access logged and justified, with the log itself audited.
3. **Aggregate by default, suppress by rule** — no cell below 5, complements suppressed with it; make the rule code, not judgement.
4. **Meter the mosaic** — log query patterns per analyst; the re-identification attack is *differential* (many small queries), and the audit that catches it is differential too.
5. **Test like an attacker** — the red-team extract exercise (Chapter 54's lab) run annually; what the strongest internal attacker can join is the real k.
6. **Say what you did** — every release states its protection method and its limits; "anonymised" alone is a word, not a method.

## 68.6 Failure Modes

- **The zip-code trap** — deleting names and keeping the combination that identifies (birth date + suburb + gender); quasi-identifiers are defined by the attacker's join keys, not your column names.
- **Spending the budget in slices** — "just one more query" fifty times; composition is the attack's best friend and the accountant's whole job.
- **Synthetic data as absolution** — synthetic datasets generated without formal guarantees leak the rare rows they overfit; synthesis is a modelling discipline (Chapter 61's honesty), not a privacy spell.
- **Utility theatre in reverse** — choosing ε = 10 to keep answers clean, which is privacy's equivalent of p = 0.2; publish ε with every release or the number means nothing.

> **Teaching Tip — The noisy counter:** run a live vote ("who has ever broken a promise?") with the local-DP coin flip, then estimate the true rate as a class. Students watch the honest answer emerge from everyone's noisy one — and the follow-up ("what if we ask each of you 20 questions?") teaches composition as budget arithmetic they have personally spent. Privacy engineering stops being compliance the moment you have felt the dial.

## Key Takeaways

- Anonymisation fails because attackers bring their own data; guarantees that depend on their ignorance are waiting lists.
- k-anonymity is good process with an unfixable guarantee; use it as a crowd-thinking discipline, not a promise.
- Differential privacy prices the trade: noise scales 1/ε (sd ≈ 1.4 at ε = 1; ≈ 14 at ε = 0.1), and the budget composes — the accountant must own it.
- Central DP for trusted curators; local DP where trust is what you are removing.
- The programme you can run now: minimise, tier, aggregate with rules, meter the mosaic, red-team annually, and state the method — never just "anonymised".

## Practice Lab

1. The re-identification exercise: take a "de-identified" extract and the local voter roll; find three join keys and name the k your extract actually delivers.
2. Implement the DP counter; for a true count of 20, plot the distribution of answers at ε = 1 and ε = 0.1; write the one-paragraph explanation a data owner can repeat about the dial.
3. The budget meter: build the query-layer accountant (per-analyst daily ε, logged); show how 50 small queries exhaust it and what the system does next.
4. Local DP vote: run the coin-flip protocol in class or in code; estimate the true rate with confidence intervals; then double the question count and watch certainty degrade.
5. The suppression rule as code: implement no-cell-below-5 with complement suppression in SQL; document the rule on the release's methodology page.
6. The synthesis audit: generate a synthetic dataset from a rare-heavy table; measure which rows are memorised, and write the honest limits paragraph that ships with it.

## Further Reading

- *The Algorithmic Foundations of Differential Privacy* — Dwork and Roth (free online)
- OpenDP and Google's DP library documentation
- Chapter 54 (the floor), Chapter 42 (lineage — privacy's memory), Chapter 68's siblings: 61 (honesty under uncertainty) and 75 (documentation that states the method)
