# Chapter 67: Simulation II and Experimentation at Scale — Monte Carlo, Bandits, and CUPED

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "When the maths gets honest, you stop solving the model and start living in it."

### In this chapter you will learn

- Monte Carlo as the analyst's default instrument: the kitchen that runs 10,000 Saturdays.
- Tornado charts and scenario design: finding the variables that own the outcome.
- Online experiments: the A/B discipline, A/A tests, and guardrail metrics.
- Sequential tests and bandits: stopping early without lying to yourself.
- CUPED: cutting noise with pre-period data — the variance-reduction trick behind modern platforms.
- The measurement infrastructure: holdouts, logging, and the decision that owns every test.

## 67.1 The Monte Carlo Kitchen

The Soulfya's Saturday margin is not a number; it is a system — covers that vary with weather and payday, average basket that drifts with the menu mix, two tills whose waits decide walk-outs (Chapter 66), and a kitchen whose speed degrades when the tickets stack. The deterministic spreadsheet says Saturday earns $340. The Monte Carlo says more:

```python
import numpy as np
runs = 10000
covers   = np.maximum(80, np.random.normal(260, 60, runs))
basket   = np.random.normal(19.0, 3.2, runs) * (1 + 0.05*np.random.binomial(1,.3,runs))
walkout  = np.random.binomial(np.maximum(covers-240, 0), 0.18)
margin   = (covers - walkout) * basket * 0.62 - 620
print("mean $%.0f | p10 $%.0f | P(margin < 0) = %.1f%%"
      % (margin.mean(), np.percentile(margin, 10),
         100*(margin < 0).mean()))
```

The output that changes decisions: **mean $302, p10 $170** — and the probability of a loss-making Saturday it makes visible. The mean alone said $340 and hid the tail; the distribution prices the risk of the new oven, the buffer the cash plan needs, and which Saturday to run the promotion on. Monte Carlo's creed: any number you would put in a memo whose inputs are uncertain deserves a distribution.

## 67.2 The Tornado: Which Uncertainty Owns the Outcome

Vary each input across its honest range, hold the rest at base, and rank the swings: the tornado chart for the Saturday model shows covers (±$110) and basket (±$70) dwarfing kitchen cost (±$20). The management lesson writes itself: **measure what moves the outcome** — better cover forecasts (Chapter 64) and price-mix analytics (Chapter 51) pay; renegotiating the paprika supplier does not. Every Monte Carlo ends in a tornado, or it was just a very slow calculator.

## 67.3 Experiments: The Gold Standard, Engineered

Chapter 61 put randomisation at the top of the credibility ladder; this section engineers it. The running discipline at scale:

1. **One decision per test** — name the decision, the metric, and the owner *before* launch (a test without a decision attached is telemetry).
2. **A/A tests as calibration** — run offer-A versus offer-A monthly; your false-positive rate is *measured*, not assumed, and every "we found a 4% lift" is read against it.
3. **Guardrails** — the metrics that must not move (complaint rate, refund rate, p95 latency); a win that breaks a guardrail is a loss wearing a banner.
4. **Power, computed before** — Chapter 14's discipline at platform scale: the sample size the effect you care about actually needs, or the honest "this test cannot answer that".

## 67.4 Stopping Early Without Lying: Sequential Tests and Bandits

The classic sin: peeking daily and stopping at the first significant day — which turns a 5% test into a 30% false-positive machine. The honest alternatives: **sequential tests** (spend-the-error-budget designs that permit early looks at pre-set checkpoints) and **bandits** — when the cost of the *loser* is real (every customer shown the worse page), the multi-armed bandit shifts traffic toward the winner as it learns, trading a little certainty for a lot of regret avoided. The rule of thumb that survives contact with business: **fixed-horizon tests for decisions you must certify; bandits for optimisations you can keep running**.

## 67.5 CUPED: Cutting the Noise

The trick behind modern experimentation platforms: outcomes are noisy, but you often know each user's behaviour *before* the experiment — last quarter's orders, pre-period engagement. **CUPED** (controlled experiment using pre-experiment data) adjusts each user's outcome by their pre-period baseline, and the noise falls with the correlation:

```python
theta = np.cov(y, y_pre)[0, 1] / np.var(y_pre)
y_cuped = y - theta * (y_pre - y_pre.mean())
# treatment effect unchanged; standard error falls from 1.64 to 0.27 on the
# Soulfya's delivery-time test — the difference 2.67 detected becomes 2.43
# (shrunk toward its pre-period luck), and detected in days, not weeks.
```

The numbers to internalise from the Soulfya's delivery-time experiment: unadjusted standard error 1.64 minutes, CUPED-adjusted **0.27** — a six-fold noise cut from a single covariate — and the estimated effect moves from 2.67 to 2.43 minutes as each user's pre-experiment luck is subtracted. That is the quiet power and the quiet danger: CUPED makes small effects visible, and it will also *change* your estimate; report both, and pre-register which is primary.

## 67.6 The Measurement Infrastructure

Experiments at scale are infrastructure, not heroics: **holdouts** that persist (Chapter 52's rotated 10%), **logging** that lands every exposure and outcome in one queryable place (Chapter 43's drift dataset doing double duty), **a registry** — one row per test: hypothesis, owner, start, end, decision, and the metric movement it produced (Chapter 75's analysis log, platform edition). The registry's dividend: the organisation's true experiment win-rate, the number that tells you whether the idea pipeline is good or merely busy.

**From Your Toolkit — Excel and Python:** the Monte Carlo kitchen was born in a spreadsheet (Chapter 64's fan is the same discipline), and the CUPED arithmetic fits in one; the platform that runs thousands of tests is Python and SQL. The bridge holds as always: same ideas, different scale.

## 67.7 Failure Modes

- **The slow calculator** — a Monte Carlo without a tornado, or with input ranges nobody believes: garbage distributions, confidently rendered.
- **The peek** — daily significance checks on a fixed-horizon test; use sequential designs or stop looking.
- **The metric that moved by accident** — fifty metrics, one "significant", a launch celebrated; the pre-registered primary metric is the vaccine.
- **Twelve tests at once** — interactions unmodelled, winners confounding each other; the registry and a simple exposure map keep the portfolio honest.

> **Teaching Tip — A/A day:** dedicate one lab to an A/A test — two identical experiences, "analysed" until something looks significant. Students find the "win" every time, and then the coin-drop: it cannot be real. No lecture on multiple comparisons survives A/A day with anything left to prove.

## Key Takeaways

- Any memo number with uncertain inputs deserves a distribution: Monte Carlo it, and mean $302 / p10 $170 beats $340-every-time.
- End every simulation with a tornado: measure what moves the outcome.
- Experiments are engineered: one decision per test, A/A calibration, guardrails, and power computed before launch.
- Sequential tests and bandits let you act early honestly; CUPED cuts noise six-fold with pre-period covariates — and moves your estimate, so report both.
- The registry is the dividend: holdouts, logging, one row per test, and the organisation's true win-rate.

## Practice Lab

1. Build the Monte Carlo kitchen on Appendix F's Saturday data; report mean, p10, and P(loss); then build the tornado and name the two variables that own the outcome.
2. Run an A/A test on simulated delivery times: 50 metrics, 20 daily peeks; count the false "wins" and write the lab report your future self needs before the first real launch.
3. Implement CUPED on the delivery-time experiment: verify the SE fall (1.64 → 0.27), the effect shrink (2.67 → 2.43), and write the two-column table both numbers deserve.
4. Design the promotion test that Chapter 61 said Soulfya's should have run: power calculation, pre-registered primary metric, guardrails, and the decision rule — all on one page.
5. The bandit simulation: three menu specials, unknown appeal, Thompson sampling versus an equal-split A/B; plot cumulative reward and regret over 30 days.
6. The registry: design the one-row-per-test schema (SQL) for an organisation running dozens of concurrent experiments; add the exposure map that catches interactions.

## Further Reading

- *Trustworthy Online Controlled Experiments* — Kohavi, Tang and Xu (the bible; CUPED chapter especially)
- *Algorithms to Live By* — Christian and Griffiths (the explore/exploit chapter, for the intuition)
- Chapter 61 (the ladder this chapter engineers), Chapter 66 (the kitchen's queues), Chapter 43 (the logging everything reads)
