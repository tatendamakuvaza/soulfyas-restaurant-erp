# Chapter 53: Financial Services — The ZuvaPay Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "In lending, the model is not the product; the loss function is the product."

### In this chapter you will learn

- The financial services canvas: risk, fraud, and regulation as one analytical system.
- Credit scoring the modern way, with the classic scorecard as its interpretable core.
- Class imbalance done honestly: cost-based thresholds for fraud.
- Explainability as law, not preference — and what a regulator actually asks.
- Population stability and drift monitoring as a *prudential* habit.
- Failure modes: score gaming, threshold drift, and the excluded applicant.

## 53.1 The Financial Services Question

**ZuvaPay** is a fictional payments-and-credit fintech: 1.1 million wallet users, 40,000 merchant points, and a fast-growing nano-loan product — $10 to $150, 30-day terms, approved in seconds from wallet behaviour. Its analytical life is dominated by three questions: **who will repay** (credit risk), **who is stealing** (fraud), and **can we prove it** (regulation). The twist that makes this playbook distinct from every other chapter in Part X: the *cost of being wrong is asymmetric and regulated* — a declined good customer costs $4 of margin; a funded fraudster costs $150 of principal; and a model the regulator cannot understand is a model you cannot deploy, whatever its AUC.

| Slot | ZuvaPay's answer |
|---|---|
| Core question | Approve, price, and detect — at what thresholds, provable to whom? |
| Unit of analysis | The application (credit); the transaction (fraud) |
| Key metrics | Default rate, loss rate, approval rate, false-positive cost of fraud, model stability (PSI) |
| Data reality | Wallet histories, device signals, bureau thin-files for most applicants, adversarial fraud |
| First project | Vintage curves on the existing loan book |
| Failure mode | Accuracy that cannot survive an audit |

## 53.2 Credit Risk: Vintage Curves First

Before any model, the vintage analysis: group loans by origination month, track cumulative default through days-past-due windows (30/60/90), and read the curves. The vintage chart is the lending business's ECG — it shows whether the book is improving cohort by cohort, and it calibrates everyone (credit committee included) to the actual default base rates before a single score exists.

The scoring stack is then a Chapter 23–25 problem with domain clothing: features from wallet history (top-up rhythm, spend volatility, airtime borrowing, merchant mix), a binary target (90+ days past due within term), and a *business* metric — profit at threshold, not AUC. The classic scorecard remains the deployed core in most regulated lenders, and its craft is worth knowing:

```python
# Weight-of-evidence binning: the scorecard's interpretability engine
woe = (df.groupby("bin")["target"].agg(["sum", "count"]))
woe["good"] = woe["count"] - woe["sum"]
woe["woe"] = np.log(
    (woe["good"] / max(woe["good"].sum(), 1))
    / (woe["sum"] / max(woe["sum"].sum(), 1))
)
```

Each feature becomes a small table of bins and weights; the score is an addition; and "your recharge regularity contributed -12 points" is an explanation a call-centre agent can read aloud. **From Your Toolkit — SPSS:** this is the direct descendant of the SPSS scorecard tradition you met in training — the same binning logic, now fitted in Python and monitored like a system.

## 53.3 Fraud: Imbalance and the Cost Line

Fraud detection is the hardest imbalance problem in practice: 0.3% fraud prevalence, an adversary who adapts, and a threshold that is a *business decision* wearing a technical costume. The honest method:

1. Baseline rules first (velocity, device reuse, geo-inconsistency) — they catch the blunt fraud and they are explainable.
2. A model for the residue (gradient boosting on behavioural sequence features), evaluated on **precision at the review-queue size** the operations team can actually staff, not on accuracy or even AUC.
3. The threshold set from the cost matrix: review is worth it when `expected fraud caught × loss size > review cost × false-positive rate × queue size`. At ZuvaPay's numbers ($150 average loss, $2.20 per review, 30 minutes of customer friction), the queue that clears this line is 1.8% of transactions — and *that* number, not the model, is the deliverable.

## 53.4 Explainability as Law

The regulatory layer is not optional garnish. A ZuvaPay decline triggers, in most markets, a right to explanation: the principal reasons, in human language, in a regulated format. The practical stack is Chapter 33's: reason codes from the scorecard bins (native), SHAP-style attributions for the model layer (Chapter 33), and a documented mapping from every feature to its data lineage (Chapter 42's governance, enforced by the regulator rather than chosen by taste). The discipline to internalise: **explanation artefacts are part of the model artefact**, versioned together, tested together — an explanation that lags the model is a compliance incident waiting for its auditor.

## 53.5 Monitoring: PSI and the Champion-Challenger Rhythm

Credit models decay as the population and the economy move. The standard vigilance is the **population stability index** on every feature and the score itself, monthly:

```sql
SELECT score_band,
       COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS share_now,
       expected_share,
       ROUND((share_now - expected_share)
             * LN(share_now / NULLIF(expected_share, 0)), 4) AS psi_part
FROM scored_applications
GROUP BY score_band, expected_share;
```

PSI above 0.25 on a feature or the score is the alarm: the world the model learned has moved. The response is Chapter 43's champion-challenger: refit as challenger, shadow-score live, swap only when the challenger beats the champion on recent data — with the swap itself documented, because the regulator will ask.

## 53.6 Failure Modes

- **Score gaming** — applicants (and agents) reverse-engineer the scorecard and manufacture the signals; monitor feature distributions for spikes at bin edges.
- **Threshold drift** — the model is stable, the queue is not: a review queue allowed to grow silently changes the product's economics and its customer experience.
- **The excluded applicant** — thin-file applicants score low by absence of data, not absence of worth; the fair-lending audit (Chapter 29's disparate-impact discipline) is a prudential duty, and alternative-data features must justify themselves against it.
- **Accuracy without auditability** — the 0.87-AUC deep model that cannot ship; in regulated credit, the explainable 0.84 wins the right to exist.

> **Teaching Tip — The decline letter:** give students a scored applicant (features, bins, points) and have them write the regulated decline letter — principal reasons, plain language, the applicant's rights. Nothing exposes a shallow understanding of a scorecard faster than trying to explain one to the person it rejected. Pair it with the mirror exercise: the letter the *falsely declined* applicant deserves.

## Key Takeaways

- Lending analytics starts with vintage curves, not models — the book's ECG before its engine.
- The scorecard's binning-and-addition design is not nostalgia; it is explainability engineered into the artefact.
- Fraud thresholds are business decisions: staff the queue from the cost line, and evaluate on precision-at-queue-size.
- Explanations are part of the model artefact — versioned, tested, regulated.
- PSI monthly, champion-challenger always; and the fair-lending audit is not optional.

## Practice Lab

1. Build vintage curves on ZuvaPay's loan book (Appendix F generator); identify the deteriorating cohort months and hypothesise (with evidence) why.
2. Fit a scorecard: WOE-bin five features, fit a logistic regression on the WOEs, produce points, and write the decline letter for three named applicants.
3. Set the fraud queue: given the cost matrix and the model's precision-recall curve, choose the queue size, defend it in dollars, and show what the queue costs in customer friction.
4. Compute monthly PSI on the score and top features; find the feature that broke 0.25 and write the incident note.
5. Run the fair-lending audit: approval rates and score distributions by applicant segment (urban/rural, age band); document any gap and propose the investigation.
6. The credit-committee memo: raise approval rate 5 points without raising loss rate — what lever do you pull, what would prove you wrong, and what does the regulator need to see?

## Further Reading

- *Credit Risk Scorecards* — Siddiqi (the scorecard bible)
- Chapter 23 (evaluation and cost), Chapter 29 (fairness), Chapter 33 (explanation), Chapter 43 (monitoring)
- Appendix J Case 2 for the leakage post-mortem pattern that applies to credit models verbatim
