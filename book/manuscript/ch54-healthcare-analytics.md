# Chapter 54: Healthcare Analytics — The Batanai Health Trust Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "In healthcare the error costs are not symmetric, the ethics are not optional, and the chart is someone's mother."

### In this chapter you will learn

- The healthcare canvas: outcomes, flow, and cost under a duty of care.
- Readmission risk: the canonical clinical prediction problem, done honestly.
- Patient flow and staffing: queueing and simulation for wards and clinics.
- Survey and epidemiology analytics with sampling weights respected.
- Privacy beyond compliance: consent, minimum necessary, and the harm test.
- Failure modes: the risk score as a gate, Goodhart on clinical targets, and the average patient.

## 54.1 The Healthcare Question

**Batanai Health Trust** is a fictional non-profit health network: three clinics and a 60-bed district hospital, 140,000 patients on file, donor-funded, and measured by the Ministry and the donors on a scorecard it did not choose. Its analytical questions: **who needs care before they return deteriorating** (risk), **how do we flow patients through scarce beds and staff** (operations), **what is actually happening in the population** (epidemiology), and **what can we honestly claim to our funders** (evaluation). The distinctive constraint is the duty of care: an error here is not a lost sale; it is a person.

| Slot | Batanai's answer |
|---|---|
| Core question | Which patients need which intervention, when — and does it work? |
| Unit of analysis | The patient-episode; the clinic-day; the catchment sector |
| Key metrics | Readmission rate, time-to-treatment, bed occupancy, programme yield, cost per outcome |
| Data reality | An EMR with coding gaps, paper registers at two clinics, staff logs, DHIS2 reports to the Ministry |
| First project | The missed-appointment and readmission register, unified |
| Failure mode | A model that gates care instead of guiding it |

## 54.2 The Unified Register First

The first project is deliberately unglamorous: one patient-level register unifying EMR extracts, the clinics' paper registers (photographed, keyed, and *validated* — Chapter 11's discipline, because a register nobody trusts is a rumour with columns), and follow-up call logs. The register's columns are the analytics agenda: patient key, episode dates, diagnoses (coded, with an "uncoded" bucket that is itself a finding), discharge destination, appointment dates, attendance, and outcomes. Every later model, dashboard, and donor claim stands on this register — which is why it is a governance artefact (Chapter 42) with a named steward, not a spreadsheet on someone's laptop.

## 54.3 Readmission Risk, Honestly

The canonical problem: predict 30-day readmission, so that discharge planning and follow-up can concentrate where risk is highest. The honest version has four features that distinguish it from the Kaggle costume:

1. **The baseline is clinical, not algorithmic.** Nurses already know the highest-risk patients by diagnosis, age, and social circumstance. The model must beat clinical judgement (or, more realistically, *augment* it by surfacing non-obvious risk — the young patient with a chaotic visit history).
2. **The target is defined by operations, not purity.** "Readmission to any facility within 30 days of discharge" — and the register must be able to see transfers, or the target is silently wrong.
3. **Calibration beats discrimination.** A risk score that says 20% must mean 20%, because the intervention (a follow-up call, a review slot) is rationed by threshold; miscalibrated risk rations it wrong (Chapter 25's calibration discipline, now clinical).
4. **The intervention defines the metric.** The point is not AUC; it is whether flagged patients who received the follow-up bundle readmit less — an uplift question (Chapter 32) wearing scrubs. Deploy with a randomised holdout of flagged patients from day one; it is both ethical and the only proof that works.

## 54.4 Flow, Beds, and Staffing

The operations layer is Chapter 66's queueing and Chapter 67's simulation, in a hospital's clothing. The ward is a queue: arrivals (admissions by hour and day), servers (beds and nurses), and a waiting discipline with clinical priority. Batanai's maternity ward runs at 92% peak occupancy — past the ρ-cliff where Chapter 66's waiting times explode — and the analyst's contribution is the queueing arithmetic that turns "we feel busy" into "at 92% utilisation your expected wait is four hours; at 80% it is ninety minutes; here is the staffing plan that buys the difference". The simulation then tests the plan against reality: elective-schedule changes, a flu week, one nurse absent — the p90 day, not the average day, is what the ward manager lives.

## 54.5 Population and Survey Analytics

The epidemiology layer answers "what is happening in the catchment": prevalence estimates from clinic data (biased toward the sick who attend — the classic selection problem, Chapter 15), corrected by community surveys with proper sampling. **From Your Toolkit — Stata:** this is Stata's home ground — `svyset` with the sampling design, `svy: proportion` for prevalence with design-corrected confidence intervals, and `svy: logistic` for the risk-factor models. The same discipline in Python (`statsmodels` with survey weights) gives the same answers; what must never happen is the unweighted crosstab presented as a population estimate — the single most common published error in programme reporting.

## 54.6 Privacy Beyond Compliance

Health data is the hardest privacy case: re-identification is easy (rare diagnosis + suburb + age = one person), consent was often gathered pre-analysis, and the harm from leakage is direct. The practitioner's floor, beyond every regulation: **minimum necessary** (the analysis extract carries only the columns the question needs — the full EMR never leaves the clinical system), **the harm test** (before any release, ask what the worst reader could do with it), and **aggregate-only reporting** for anything leaving the Trust — with small-cell suppression (no cell below 5) as the default rule. Chapter 68's formal privacy engineering is the frontier; this section is the floor beneath it.

## 54.7 Failure Modes

- **The risk score as a gate** — a model intended to *guide* discharge planning quietly becomes the rule that denies the follow-up call to the "low-risk"; monitor what decisions the score actually feeds.
- **Goodhart on clinical targets** — time-to-treatment targets met by a triage queue that starts *after* registration; every operational metric needs its companion audit (Chapter 45's discipline, clinically applied).
- **The average patient** — clinical subgroups (age bands, comorbidities, distance) differ enough that one model or one threshold mis-serves them; stratify evaluation, not just training.
- **The donor-pleasing estimate** — unweighted clinic data reported as population prevalence; the error of Section 54.5, published.

> **Teaching Tip — The chart is someone's mother:** run the ethics round before the lab. Give students a de-identified extract and the local newspaper's court report page; thirty minutes to attempt re-identification of one patient. The exercise lands harder than any lecture on privacy — and it motivates small-cell suppression, minimum necessary, and aggregate-only reporting as *craft*, not compliance theatre.

## Key Takeaways

- Start with the unified register: every model, dashboard, and donor claim stands on it; it is a governance artefact with a steward.
- Readmission models must beat or augment clinical judgement, calibrate (not just discriminate), and be evaluated as an intervention with a randomised holdout.
- Queueing arithmetic and simulation turn "we feel busy" into staffing plans tested against the p90 day.
- Survey analytics respects the design: unweighted clinic data is not population prevalence.
- The privacy floor is minimum necessary, the harm test, and small-cell suppression — Chapter 68 is the frontier, not the floor.
- Watch what decisions each score feeds: gates are the failure mode of guides.

## Practice Lab

1. Build the unified register's validation report on the Batanai extract (Appendix F generator): duplicate patient keys, uncoded diagnoses, appointment dates after discharge, and the paper-register reconciliation table.
2. Fit the readmission model; evaluate against the clinical baseline, report calibration by decile, and write the deployment note that includes the randomised holdout design.
3. Queueing arithmetic: given arrival and service rates by shift, compute expected waits at current staffing and at two alternatives; present the staffing memo with the p90 simulation results beside the means.
4. The survey correction: estimate prevalence from clinic data, then re-estimate with the community survey's design weights; write the two sentences a donor report needs explaining the difference.
5. Run the re-identification exercise on your own extract; document the three easiest attacks and the specific controls that block each.
6. The Goodhart audit: pick one Ministry indicator, describe how it could be met while care worsens, and design the companion metric that catches it.

## Further Reading

- *Clinical Prediction Models* — Steyerberg (the honest textbook of the genre)
- Chapter 32 (uplift as intervention evaluation), Chapter 63 (survival curves for time-to-readmission), Chapter 66–67 (queueing and simulation)
- Appendix J Case 4 for the policy-evaluation pattern that donor claims should follow
