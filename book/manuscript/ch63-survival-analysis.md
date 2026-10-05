# Chapter 63: Survival Analysis — Time Until the Event

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "'Did they churn?' is the wrong question. 'When — and while we watched?' is the truth."

### In this chapter you will learn

- Why churn flags lie, and censoring is the honest alternative.
- The Kaplan-Meier estimator: the retention curve, done properly.
- Reading survival curves: medians, quantiles, and the danger of the average.
- Cox regression: hazards, covariates, and the proportional assumption you must check.
- Where survival belongs: churn, machines, patients, farmers, loans.
- Failure modes: immortal time, competing risks, and averaging hazards.

## 63.1 The Wrong Column

Every churn model you have met (Chapters 27 and 32) ended in a flag: churned, yes or no, at the data freeze. The flag is a convenience that costs the truth three ways: it throws away *when*, it treats a member who left in week 1 the same as one who left in week 51, and it silently drops the members who are simply not yet gone. The honest framing is survival analysis: model **time until the event**, with the event defined in advance and the un-evented members **censored** — observed until they were observed, no longer.

The Soul Circle makes the stakes concrete. "Churned in 60 days" hides the curve's shape: a steep early drop (the trial-and-leave members), a long plateau (the habit members), and a late sag (the defected-to-competitor members). Retention campaigns, CLV arithmetic, and the win-back budget all depend on the shape — not the flag.

## 63.2 Kaplan-Meier: The Retention Curve, Done Properly

The estimator is one multiplication done in order: at each event time, multiply the survival probability by the share of those still at risk who survived the moment.

```python
from lifelines import KaplanMeierFitter
kmf = KaplanMeierFitter()
kmf.fit(durations=members["weeks_active"],
        event_observed=members["churned"])
kmf.plot_survival_function()          # the retention curve, with bands
print(kmf.survival_function_at_times(15))   # S(15)
print(kmf.median_survival_time_)            # the honest "typical lifetime"
```

Reading discipline, in three rules. **Report the quantiles, not the mean** — survival is skewed, and the mean of a censored distribution is a guess about the unobserved future wearing a formula. In the Soul Circle cohort, S(15) = 0.389: 38.9% of members remain active at week 15, and the median lifetime falls in the interval (9, 15] — stated as an interval, because that is the resolution the data supports. **Read the curve, not a point** — the early cliff and the late sag are different businesses. **Respect the bands** — where few members remain at risk, the confidence interval widens and the curve becomes suggestion; stop narrating before the data runs out.

## 63.3 Cox Regression: Hazards with Covariates

The Kaplan-Meier describes one group; the Cox model asks what moves the curve: each covariate's exponentiated coefficient is a **hazard ratio** — how much faster (or slower) the event comes, multiplicatively, for that characteristic.

```python
from lifelines import CoxPHFitter
cph = CoxPHFitter()
cph.fit(member_covariates, duration_col="weeks_active",
        event_col="churned")
print(cph.summary[["coef", "exp(coef)", "p"]].sort_values("p"))
# exp(coef) = 1.62 on delivery_share: heavy delivery users churn 62% faster.
```

The assumption to check, always: **proportional hazards** — that the covariate's effect is constant over time. Plot the scaled Schoenfeld residuals; when a covariate's effect fades or flips (a welcome-offer that delays churn for eight weeks and then stops working), the single hazard ratio is an average of two different stories — and the two stories are the finding.

## 63.4 Where Survival Belongs

The method migrates further than any other in this part:

- **Members and subscribers** — churn curves, CLV inputs (Chapter 52's expected periods, now honest).
- **Machines** — time to failure as a function of age and condition (Chapter 58's maintenance hazard).
- **Patients** — time to readmission (Chapter 54); time to recovery; the curves stratified by ward.
- **Farmers** — time to co-operative exit (Appendix J Case 5's converging curves: the grant *delayed* exit, a different finding from preventing it).
- **Loans** — time to default, which beats a 30-day flag for the same reason churn flags lie (Chapter 53's vintage curves are survival's cousin).
- **Employees** — time to attrition, in the HR analytics you will be asked for eventually.

**From Your Toolkit — SPSS and Stata:** survival analysis is the classical stats packages' home turf — SPSS's Kaplan-Meier dialogs and Stata's `stset`/`stcox` taught this method to a generation before Python wrapped it. The bridge is exact: the same estimator, the same log-rank test, now with `lifelines` on the other side of the click.

## 63.5 Competing Risks, Briefly

Sometimes the event you model is not the only way out. A member can churn — or move cities, or be absorbed into a household account; a patient can be readmitted — or die. Treating every exit as your event biases the curve; treating every other exit as censored biases it differently. The honest-lite discipline: define the competing events, report their shares, and where they are material, model the cumulative incidence for each cause rather than one Kaplan-Meier for all exits combined.

## 63.6 Failure Modes

- **Immortal time** — members must be alive (active) to receive the "treatment" (the loyalty tier, the clinic programme); the window between enrolment and treatment is time they could not have churned, and counting it inflates the programme's effect. Align the clock at the treatment, always.
- **Averaging hazards** — one hazard ratio over a covariate whose effect changes sign (early retention, late churn) reports a confident nothing.
- **The censored-as-gone error** — treating members lost to follow-up as churned; censoring means "we stopped watching", which is information about the watcher, not the watched.
- **Reading past the data** — narrating the curve's tail where three members remain at risk and the confidence band is a road.

> **Teaching Tip — Draw the day-30 cliff:** give students a raw activity table and ask them to sketch the retention curve *before* computing it. The sketches disagree wildly; then Kaplan-Meier settles it in one line, and the class sees the estimator as the resolution of an argument they were just having. It is the fastest lesson in why the method exists.

## Key Takeaways

- Churn flags discard timing and censoring; survival analysis keeps both — and the shape of the curve is the business.
- Kaplan-Meier with confidence bands; report quantiles as intervals (S(15) = 0.389, median in (9, 15]), never a false-precision mean.
- Cox gives hazard ratios; proportional hazards must be checked, and its violations are findings.
- The method migrates everywhere: members, machines, patients, farmers, loans, employees.
- Align the clock at treatment (immortal time), define competing risks, and stop reading where the data runs out.

## Practice Lab

1. Build the Soul Circle survival curve; report S(15), the median interval, and the early-cliff/plateau/late-sag reading in three sentences a marketing manager can repeat.
2. Fit the Cox model on member covariates; check proportional hazards; find the covariate whose effect changes over time and write the two stories it averages.
3. Stratify the curves by acquisition channel (Chapter 52's cohort logic, deepened): do channels differ in *shape* or only in *level*? Test with the log-rank statistic.
4. The machines: fit time-to-failure on Sabvura's maintenance data (Appendix F); produce the 200-hour hazard window per machine and compare with Chapter 58's schedule.
5. The competing-risks audit: define the Soul Circle's non-churn exits, report their shares, and recompute the churn curve as cumulative incidence; note where the naive curve lied.
6. The immortal-time hunt: take Case 5's grant data and show how the naive comparison (treatment defined at grant end) inflates the effect; align the clock at grant start and report both.

## Further Reading

- *Applied Survival Analysis* — Hosmer, Lemeshow and May
- `lifelines` documentation (the best tutorial in the Python ecosystem)
- Chapters 52, 54, 58 (the domains this method serves); Appendix J Case 5 (converging curves, and what they mean for a grant renewal)
