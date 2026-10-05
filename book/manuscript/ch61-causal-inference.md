# Chapter 61: Causal Inference — The Counterfactual Discipline

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "The question correlation cannot answer is the only question the business is asking: what would have happened anyway?"

### In this chapter you will learn

- Potential outcomes: the one idea under every causal method.
- The credibility ladder: randomisation, natural experiments, adjustment — in order of trust.
- Difference-in-differences, and the parallel-trends check you must show.
- Instrumental variables and synthetic control, with their failure modes.
- Sensitivity analysis as a first-class result, not an appendix.
- The National Street Levy case: one policy, four estimates, and the 2.4x spread that honesty demands.

## 61.1 The Counterfactual Question

Every chapter before this one has asked "what does the data show?" This chapter asks the harder question underneath every business request: **what would have happened without the thing we're studying?** Soulfya's ran a promotion (Case 1); members who received it visited 31% more. The number is a fact; the question is whether the promotion *caused* it — and the answer lives in the visits of a customer who does not exist: the same customer, un-promoted, in the same quarter.

That ghost is the **potential outcome**, and it is the single idea behind every method in this chapter. We never see both outcomes for the same unit (the fundamental problem of causal inference), so every method is a discipline for constructing a believable ghost: a control group, a counterfactual trend, a natural experiment. **From Your Toolkit — Stata:** this is the question your econometrics training kept asking — "identified by what?" — and this chapter is the field guide to the answers.

## 61.2 The Credibility Ladder

Order your trust like this, and say the order out loud in every write-up:

1. **Randomised experiment** — the ghost is the control arm, different only by luck. Chapter 67's discipline.
2. **Natural experiment** — assignment to treatment happens by forces that look like luck: a threshold, a cutoff, a strike, a boundary. DiD, regression discontinuity, instrumental variables.
3. **Adjustment** — statistical controls on observational data: regression, matching, weighting. Necessary, everywhere, and the least trustworthy — because the confounders you did not measure do not politely announce themselves.

The professional failure is inverting the ladder: presenting an adjusted observational estimate with experimental confidence. The honest practitioner states the rung before the result.

## 61.3 Difference-in-Differences

The workhorse. Two groups, two periods: the treated group's *change* minus the control group's *change* — the second difference removes both the group's permanent level and the period's common shock.

```python
import statsmodels.formula.api as smf
did = smf.ols("visits ~ treated * post + member_features",
              data=panel).fit(cov_type="cluster",
                              cov_kwds={"groups": panel["member_id"]})
effect = did.params["treated:post"]        # the DiD estimate
```

The assumption that must be **shown, not asserted**: parallel trends — before the treatment, the two groups moved together. Plot the pre-period lines; if they diverged before the treatment, the method is decorating confounding with arithmetic. Appendix J Case 4's tariff elasticity is this method at full scale, including the messy part real natural experiments refuse to hide.

## 61.4 Instrumental Variables

When treatment is entangled with the outcome (farms that adopt a programme are the farms that would have done well anyway), you need a variable that moves the treatment but has no other path to the outcome — rainfall moves fertiliser adoption but (arguably) affects yield only through farming inputs. The craft is the two tests you can run (the instrument strongly predicts treatment; the estimate is stable across specifications) and the one you cannot (exclusion — the instrument has no back door), which is why IV results always carry their "arguably" in the text. Weak instruments produce loud, wrong answers: check the first-stage F before trusting the second stage.

## 61.5 Synthetic Control

For the one treated unit — a district, a province, a flagship store — build the ghost as a weighted blend of untreated neighbours, chosen so the blend tracked the treated unit's past. When the levy hits one province, the synthetic province (weighted combination of its neighbours) continues the old trend, and the gap is the effect. The craft: donor pools that exclude contaminated units, weights that stay interpretable, and placebo checks — run the method on a never-treated unit and see how big a "effect" it fabricates.

## 61.6 The Case: The National Street Levy

The fictional National Street Levy funds road repairs with a 2% levy on fuel in four pilot provinces. Three years in, the ministry's question: did it reduce vehicle operating costs? The honest analysis produced four estimates, not one:

| Method | Comparison | Estimate |
|---|---|---|
| Naive before-after | Pilot provinces, pre vs post | -18.4% |
| DiD | Pilot vs matched non-pilot provinces | -9.1% |
| DiD + economic controls | Adds fuel-price and freight shifts | -7.6% |
| Synthetic control | Blended counterfactual provinces | -7.1% |

The naive estimate is more than double the most-defensible one — a **2.4x swing across specifications**, and the swing *is* the finding. The report's headline: "vehicle operating costs fell 7–9% in pilot provinces, with the naive 18% attributable mostly to the national freight downturn that hit both pilot and control provinces." The ministry's press office wanted 18%; the analysis delivered an interval with its reasons — and Chapter 76's audit would have found the 18% indefensible in a week.

## 61.7 Sensitivity as the Result

The discipline that separates this chapter from a textbook: **the sensitivity analysis is the result.** Report the estimate under every defensible specification, show the spread, and name what drives it. A finding that survives every reasonable specification is a finding; a finding that lives only in one model is a coincidence with a standard error. The one-page robustness table — methods down the rows, choices across the columns, the estimate repeated and its range highlighted — is the frontier chapter's signature artefact, and the one Part XII's memos are built to carry.

> **Teaching Tip — The anyway report:** have students write two reports from the same data: the advocacy report (one estimate, the biggest) and the anyway report (the range, with the assumptions named). Reading them side by side teaches more about analytical honesty than any lecture on causality — and the anyway report is, invariably, the more persuasive document.

## Key Takeaways

- Causality is the business question: what would have happened anyway? Every method is a way of building the ghost.
- Trust in order: randomisation, natural experiments, adjustment — and state the rung before the result.
- DiD's parallel trends must be displayed, not asserted; IV's exclusion is argued, never proven; synthetic control needs its placebos.
- The National Street Levy's 2.4x spread across specifications is the norm, not the exception — report the range.
- Sensitivity analysis is the result, not the appendix: one-page robustness table, every time.

## Practice Lab

1. Re-run Case 1's promotion analysis as a DiD (email vs non-email members, pre vs post); display the parallel-trends plot and write the paragraph a sceptic deserves.
2. Estimate the street-lighting effect (Chapter 57's data) three ways: before-after, DiD, DiD with controls; build the robustness table and highlight the range.
3. Build a synthetic control for one pilot province's operating costs; run the placebo test on a never-treated province and report the fake effect it fabricates.
4. Find the weak instrument: simulate a first stage with F = 4 and watch the second-stage estimate explode; then strengthen the instrument and watch it recover.
5. The anyway report: take any published claim (a news story citing a study) and write the anyway version — what comparison was made, what ghost was assumed, and the range the honest estimate would carry.
6. The Soulfya's menu redesign: design the experiment the founder should have run — randomise by outlet-week, define the metric, pre-register the analysis, and state the sample size needed.

## Further Reading

- *Causal Inference: The Mixtape* — Cunningham (free online; the field guide)
- *Mostly Harmless Econometrics* — Angrist and Pischke (the IV chapters)
- Appendix J Cases 1 and 4; Chapter 67 (where the top rung of the ladder is engineered); Chapter 76 (the audit that tests this chapter's habits)
