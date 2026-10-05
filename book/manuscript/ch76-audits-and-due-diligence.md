# Chapter 76: Audits and Due Diligence — Ten Questions

*Part XII — The Practitioner's Path: Projects, Clients and the Craft of Delivery*

> "Every model is innocent until probed; the probe is ten questions long."

### In this chapter you will learn

- The audit mindset: health check, not inquisition — and the report that helps.
- The ten questions, with what each catches and what a good answer sounds like.
- Due diligence on someone else's model: the vendor version of the same probe.
- The findings report: ranked, evidenced, with effort and fix.
- Red flags that end audits early.
- Failure modes: the checkbox audit and the audit as warfare.

## 76.1 The Audit Mindset

You will be audited (your models, your dashboards, your numbers) and you will audit (inherited work, a vendor's claims, a predecessor's pipeline). Both go better with the same framing: **a health check that helps** — ranked findings, each with its evidence and its fix, delivered to make the work better rather than the auditor look smart. The audit that helps gets invited back; the audit that performs gets performed at.

The ten questions are the probe. They are ordered by the failure frequency of real practice — the top three catch most of what matters.

## 76.2 The Ten Questions

1. **What is the grain?** — one row of this table means what, exactly? The unanswerable version is the fan-out bug (Chapter 6) waiting to be rediscovered. Good answer: a sentence, instantly.
2. **Where did this data come from, and what was done to it?** — lineage from source to table (Chapter 42). Good answer: the data card plus the transformation trail, produced without a séance.
3. **How was the evaluation split, and is there leakage?** — time-based or grouped splits, the leakage checklist (Chapter 22), the definitional leaks Case 2 exposed. Good answer: "we split by member and by time; here are the three features we removed and why."
4. **What is the baseline?** — the seasonal-naive, majority-class, last-year comparison (Chapter 23). Good answer: the league table, model and baseline side by side. No answer: the finding that the model never beat the cheap alternative.
5. **Is it calibrated where it must be?** — thresholds and rationing decisions need calibrated risk (Chapter 25, 54). Good answer: the calibration curve by decile.
6. **How sensitive is the conclusion?** — the robustness table of Chapter 61: specifications down the rows, the estimate's range highlighted. Good answer: a range with its reasons. Bad answer: one number, defended.
7. **What is the privacy posture?** — minimisation, tiers, suppression, the harm test (Chapters 54, 68); consent and provenance for people-data. Good answer: the stated method, named limits.
8. **How is it monitored, and what has drifted?** — the PSI discipline, the drift dataset, the champion-challenger rhythm (Chapters 43, 53). Good answer: recent monitoring output, including something it caught.
9. **Who owns it now, and what breaks first?** — the named owner, the failure modes, the runbook (Chapters 43, 69). Good answer: an owner, an alert, a rehearsal.
10. **What would make you withdraw it?** — the pre-registered reversal condition (Chapter 71's measurement plan, sharpened). Good answer: specific, already written. No answer: work that has never considered its own death.

## 76.3 Due Diligence, the Vendor Edition

The same probe, pointed outward, with three additions:

- **The claims audit** — map every claim in the pitch ("30% better", "real-time") to its measurement: measured how, on what data, against what baseline, by whom? The unmeasurable claim is a wish.
- **The eval-set question** — Chapter 65's discipline, outward: whose evaluation, frozen when, annotated by whom? Vendors who cannot show their eval set cannot show their number.
- **The exit test** — if the vendor vanishes, what survives? Data export formats, model artefact portability, the documented schema. The answer prices the lock-in.

**From Your Toolkit — Stata:** the audit trail is the econometric tradition's gift — the do-file that runs top to bottom, producing every table in the output, is the audit question 3, 4, and 6 answered in artefact form. Demand the same of everything: the do-file, the notebook that runs clean, the pipeline with one command (Chapter 75).

## 76.4 The Findings Report

One page, ranked:

| Rank | Finding | Evidence | Fix | Effort |
|---|---|---|---|---|
| 1 | Churn target leaks via nightly status field | Feature availability timeline | Remove 3 features, refit; AUC 0.97 → expected ~0.80 | 2 days |
| 2 | No baseline in evaluation | Report lacks league table | Add seasonal-naive comparison | 1 day |
| 3 | Calibration untested for threshold use | No calibration output | Calibrate by decile; recalibrate quarterly | 2 days |

The report's rules: every finding carries its **evidence** (the artefact that proves it), its **fix**, and its **effort** — because the reader's next act is prioritisation, and findings without effort are anxiety, not aid. Severity is ranked by decision-risk, not technical elegance: the leak that flatters the model outranks the ugly code that works.

## 76.5 Red Flags

Findings that end audits early, because everything downstream is suspect:

- **The number that cannot be reproduced** — no seeds, no snapshot, "it was on the old laptop" (Chapter 75's moving target).
- **The evaluation that improved when it should not have** — accuracy up after a data change nobody can explain: leakage until proven otherwise (Case 2's law).
- **The refusal to show the data card** — the lineage question answered with adjectives ("clean", "comprehensive") instead of artefacts.
- **No owner** — question 9 answered with a team email address; the system is already an orphan.

## 76.6 Failure Modes

- **The checkbox audit** — ten questions, ten "yes"s, zero artefacts requested; the audit as ritual. Every yes should be *shown*, not said.
- **Audit as warfare** — findings deployed for politics; the audit that helps is the audit that gets told the truth next time.
- **The novelty bias** — findings about code style while the calibration failure (question 5) goes unasked; the probe's order is the shield.
- **The audited who performs** — preparing theatre for the audit instead of fixing the work; the artefact-yes rule makes theatre expensive.

> **Teaching Tip — Audit swap:** pair students; each audits the other's capstone with the ten questions, artefacts required for every yes. The debrief's question is not "what did you find?" but "what did you *fix* before handing it over?" — because the audit's approach changes how work is *built*: students start keeping logs, pinning environments, and writing reversal conditions when they know the probe is coming. The audit's greatest value is the work it prevents you from doing badly.

## Key Takeaways

- Audit as health check: ten questions, ranked findings, each with evidence, fix, and effort.
- The top of the probe catches the most: grain, lineage, and leakage — asked first, artefacts required.
- Questions 4–6 are the honesty core: baseline, calibration, sensitivity — the league table, the curve, the range.
- DD on vendors adds the claims audit, the eval-set question, and the exit test.
- Red flags end audits early: unreproducible numbers, unexplained improvements, adjective lineages, orphan systems.

## Practice Lab

1. Audit a model you built (Part V's churn, or any Kaggle submission) with the ten questions; write the findings report with evidence, fix, and effort for every failure you find in your own work.
2. Audit swap: exchange audits with a classmate; rank the severity of each other's findings by decision-risk and compare the rankings — where they differ is a lesson about what matters.
3. The vendor probe: take a published AI product's claims page; map each claim to its measurement and write the questions the sales call needs.
4. Question 10's test: take three live artefacts in your organisation and find whether any states its reversal condition; write the conditions they lack.
5. The red-flag drill: fabricate one red flag (a planted leak or an unreproducible number) in a classmate's audit bundle and see whether the probe catches it; debrief on which question did the catching.
6. The DD memo: Case 2's v2 model is a vendor pitch ("AUC 0.97, deploy Monday") — write the two-page due-diligence memo to Azu.

## Further Reading

- *The Flaw of Averages* — Savage (why unexamined numbers mislead)
- Model cards literature (Mitchell et al.) — the artefacts question 10 looks for
- Chapter 22 (leakage — the probe's favourite catch), Chapter 43 (monitoring), Chapter 75 (the artefacts every yes must show)
