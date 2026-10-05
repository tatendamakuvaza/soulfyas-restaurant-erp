# Chapter 52: Marketing and Customer Analytics — The Zuva Mobile Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Marketing without analytics is spending; marketing with analytics is still spending, but you know which half."

### In this chapter you will learn

- The marketing playbook canvas, on a telecom's honest data reality.
- Acquisition analytics: CAC by channel, cohort curves, and the paid-growth trap.
- Churn, ARPU, and the CLV engine — the trio that values every subscriber.
- Uplift modelling for campaigns, revisited at telco scale.
- Attribution honesty: why last-click is a story, not a measurement.
- Failure modes: ROAS vanity, frequency fatigue, and the segment that cannot be saved.

## 52.1 The Marketing Question

**Zuva Mobile** is a fictional mobile network operator: 900,000 prepaid subscribers, 60,000 postpaid, a youth-heavy brand, and a marketing department that spends $2.4 million a year across above-the-line media, agent commissions, digital, and sponsorships. The CFO's question is the one every marketing analytics practice is built to answer: **which spending changes customer behaviour, and which merely accompanies it?**

The canvas:

| Slot | Zuva Mobile's answer |
|---|---|
| Core question | Which spend acquires, retains, and grows customers at positive lifetime value? |
| Unit of analysis | The subscriber × week; the campaign × cell |
| Key metrics | CAC, churn rate, ARPU, CLV, campaign incremental lift |
| Data reality | CDRs, recharges, campaign exposure logs with gaps, agent self-reports, no clean exposure truth |
| First project | The cohort retention curve by acquisition channel |
| Failure mode | Buying revenue with promotions and calling it growth |

## 52.2 Acquisition: CAC and the Cohort Curve

Cost per acquisition by channel is arithmetic; it becomes analysis when paired with what happens after acquisition. The cohort curve is the method (Chapter 23's discipline applied to growth): group subscribers by acquisition month and channel, then plot retention and ARPU forward.

```sql
SELECT acquisition_cohort, channel,
       DATE_DIFF('week', acquisition_date, activity_week) AS weeks_in,
       COUNT(DISTINCT subscriber_id) AS active,
       ROUND(SUM(recharge_amount) / COUNT(DISTINCT subscriber_id), 2) AS arpu
FROM subscriber_activity
GROUP BY 1, 2, 3
ORDER BY 1, 2, 3;
```

The curve exposes what CAC alone hides: agent-acquired subscribers cost $3.10 each and half are gone in six weeks; digital-acquired cost $7.80 and hold 71% at week 26. **CAC without the cohort curve is a price tag on a mystery.** The channel that looks expensive per head is often the cheap one per *retained* head — and the metric that settles it is CAC amortised over surviving subscribers, or bluntly, payback weeks: months until cumulative margin covers acquisition cost.

## 52.3 The CLV Engine

The three numbers that value a subscriber base — churn, ARPU, CLV — form one engine:

- **Churn** (Chapter 27's survival view is the honest one): weekly active-churn for prepaid, where "active" must be *defined* (days since last recharge against the subscriber's own rhythm — a 30-day-absence means different things for a $1-a-day user and a $20-a-month user).
- **ARPU** (average revenue per user): revenue over subscriber-weeks, watched as a distribution, not an average — prepaid ARPU is bimodal.
- **CLV**: `margin per period × expected periods remaining`, where expected periods comes from the retention curve of the subscriber's segment, discounted if the horizon is long. The formula is one line; the craft is the segmentation that feeds it, because CLV computed on the whole base is a single number that describes no one.

**From Your Toolkit — Power BI:** the CLV engine is the classic three-page Power BI model: a cohort matrix visual (acquisition month × months-since, shaded by retention), a decomposition tree for ARPU, and a card row for payback weeks by channel. The toolkit bridge matters because the marketing team will *live* in this report; build it where they already work.

## 52.4 Campaigns: Uplift at Scale

Chapter 32 taught the four cells (persuadables, sure things, lost causes, sleeping dogs); telco scale makes the economics brutal. Zuva Mobile's airtime-bonus campaign reaches 300,000 subscribers per blast. Treating everyone wastes three-quarters of the spend and actively harms the sleeping dogs. The uplift discipline: run the campaign as a permanent 10% holdout (random, rotated monthly so no subscriber is forever untreated), model the *difference* in outcome between treated and untreated by segment, and target only segments whose uplift clears the cost line. The holdout is not lost revenue; it is the measurement budget, and it pays for itself the first time it kills a campaign that was buying revenue Zuva already had.

## 52.5 Attribution Honesty

Digital attribution is where marketing analytics goes to feel scientific. The honest position: **last-click attribution is a convention, not a measurement** — it assigns the conversion to the final touch, which systematically over-credits search and retargeting (the closers) and under-credits the media that created demand (the openers). The alternatives are all imperfect: multi-touch models are assumptions arranged in a funnel; media-mix modelling (Chapter 62's regression discipline at weekly granularity) is slow but honest about offline; and geo-experiments — splitting regions into treatment and control — are the closest to truth a big brand can buy. Zuva Mobile's practical stack: last-click for tactical optimisation within a channel, geo-experiments for the big budget questions, and the humility to say "unattributed" out loud.

## 52.6 Brand and Survey Analytics

Surveys are marketing's second dataset: aided/unaided awareness, consideration, and intent, sampled properly (Chapter 15) and tracked quarterly. The craft is refusing the vanity read: awareness that does not move consideration is not working, and intent questions need the stated-vs-revealed caveat. **From Your Toolkit — SPSS:** the tracking study is where your SPSS crosstab-and-chi-square training applies directly — significance tests on awareness by region and age band, with the sampling weights respected (Stata's `svy` discipline, same idea).

## 52.7 Failure Modes

- **ROAS vanity** — return on ad spend computed without a holdout: revenue that would have arrived anyway, booked as marketing's achievement.
- **Frequency fatigue** — reaching the same subscribers weekly until they churn to escape the campaign; watch opt-outs per exposure.
- **The unsaveable segment** — churn models that concentrate spend on the highest *risk* rather than the highest *uplift* (Chapter 32 again: some churners are lost causes; spend on the persuadables).
- **The average subscriber** — bimodal prepaid ARPU averaged into meaninglessness.

> **Teaching Tip — The holdout debate:** stage it. Assign half the class to defend "every impression should be monetised, holdouts waste reach" and half to defend "unmeasured spend is unmanaged spend". Ten minutes, then show a real campaign's incremental lift beside its last-click ROAS. The gap between the two numbers is the whole section, seen rather than told.

## Key Takeaways

- CAC is a price tag; the cohort retention curve is the product. Never quote one without the other.
- CLV is one formula over three honest inputs: segmented churn curves, ARPU as a distribution, and expected periods from the retention curve.
- Campaigns run on uplift with permanent holdouts — the holdout is the measurement budget, not lost revenue.
- Attribution conventions are not measurements: last-click for tactics, geo-experiments for truth, and "unattributed" as a respectable answer.
- Target uplift, not risk; watch frequency fatigue; and never average a bimodal base.

## Practice Lab

1. Build the cohort retention matrix (acquisition month × weeks-in) for Zuva Mobile's data; identify the channel whose CAC looks cheapest per head and most expensive per survivor.
2. Compute payback weeks by channel; write the investment memo: which channel gets next year's incremental $500,000, with the reversal condition stated.
3. Fit the CLV engine on segmented retention curves; produce the base valuation under three churn scenarios (base, +2 points, -2 points) and comment on the swing.
4. Design the uplift campaign: which segments get treated, what the holdout is, and what the success metric is before launch. Then compute the campaign's incremental profit from the (planted) results in Appendix F's campaign dataset.
5. Run the attribution audit: take a month of exposure and conversion logs, compute last-click ROAS, and list every assumption it makes in one table; mark which ones a geo-experiment would test.
6. The Zuva memo: the marketing budget is cut 15% — what do you cut, what do you protect, and what measurement survives the cut?

## Further Reading

- *Marketing Analytics* — Wayne Winston (the operations-research view)
- Chapter 32 (uplift), Chapter 15 (sampling, for the survey layer), Chapter 62 (regression and causality for media mix)
- Zuva Mobile returns in Chapter 65 (Kumba's language services on Zuva's zero-rated bundle) and Appendix J
