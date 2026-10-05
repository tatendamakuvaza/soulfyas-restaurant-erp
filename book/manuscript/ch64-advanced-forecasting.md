# Chapter 64: Advanced Forecasting — Hierarchies, Honest Intervals, and Intermittent Demand

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "A forecast is a promise with a range; most organisations only hear the point."

### In this chapter you will learn

- The reconciliation problem: why the outlet forecasts must add to the chain forecast.
- Bottom-up, top-down, and optimal (MinT) reconciliation — and the one-line idea behind each.
- Bootstrap prediction intervals: uncertainty that survives the real world.
- Croston's method and its successors: forecasting what is ordered rarely.
- Rolling-origin evaluation: the league table, season by season.
- Failure modes: the single-number forecast, the unbalanced hierarchy, and intervals nobody believes.

## 64.1 The Reconciliation Problem

Soulfya's forecasts the chain, each outlet, and each outlet's categories — and the first week the numbers meet in one spreadsheet, they disagree: the outlet forecasts sum to 112% of the chain forecast, and the category forecasts disagree with both. The organisation has three options, and every organisation with a hierarchy (chain → outlet → category → item) faces them: live with the inconsistency, force one level and lose the others' information, or **reconcile** — adjust all levels so they agree, each level informed by the others.

That is the reconciliation problem, and it is solved not by better point models but by a projection: whatever each level says, move the whole set onto the space of forecasts that sum correctly, weighting by how much you trust each level.

## 64.2 Bottom-Up, Top-Down, MinT

- **Bottom-up** — forecast the leaves, add them up. Respects local information; amplifies leaf noise; blind to the chain-level signal (the promotion, the macro shock).
- **Top-down** — forecast the top, split by historical shares. Stable; silent about every local pattern (the outlet with a new neighbour).
- **Optimal reconciliation (MinT)** — forecast *every* level independently, then combine them with weights that reflect each level's error structure, so the result sums correctly and borrows strength across levels. The intuition in one line: **the best estimate of any node is a weighted blend of its own forecast and the reconciled forecasts around it** — the same shrinkage instinct as Chapter 34's hierarchical means, applied to a forecast tree.

```python
# MinT, conceptually: reconcile with an identity-ish covariance
# (full MinT estimates the covariance; the shrinkage variant is robust)
import numpy as np
S = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0],
              [1, 1, 1, 0]])            # S: which leaves make which nodes
yhat = np.array([210, 180, 150, 600])    # independent base forecasts
P = np.diag([14, 12, 11, 40])            # each level's error variance
reconciled = yhat - P @ S.T @ np.linalg.inv(S @ P @ S.T) @ (S.T.T @ yhat - yhat)
```

In the Soulfya's case, reconciliation moves the chain forecast 4% below the naive sum — because the outlet-level models, each blind to the others, had collectively double-counted the promotion. The hierarchy is a measurement instrument, not just a reporting structure.

## 64.3 Honest Intervals: The Bootstrap

Point forecasts are half the product; the interval is the half that gets used (stock, staffing, cash). The textbook interval assumes normal, symmetric errors — and restaurant demand is neither. The bootstrap discipline: refit (or re-weight) many times, and read the distribution of the forecasts themselves.

```python
boot = []
for b in range(1000):
    sample = residuals[np.random.randint(0, len(residuals), len(residuals))]
    boot.append(point_forecast + np.cumsum(sample[:h]))   # h-step paths
lo, hi = np.percentile(np.array(boot), [10, 90], axis=0)
```

The intervals that matter are **asymmetric and widen honestly** — the p90 demand for Saturday dinner is further above the point than the p10 is below it, and the stocking decision lives in that asymmetry. If a forecast product shows one number, it is a rumour; if it shows an honest range, it is a decision instrument.

**From Your Toolkit — Excel:** the forecast sheet everyone knows produces a line; the bootstrap produces a fan — and the fan is buildable in a spreadsheet (a data table of 200 resampled paths is a classic Excel Monte Carlo). The bridge: the interval is not a specialist add-on; it is the part of the forecast your operations team actually needs.

## 64.4 Croston: Forecasting What Rarely Happens

Most forecasting assumes demand arrives every period. Spare parts, slow menu items, and intermittent delivery routes do not: weeks of zeros, then an order of 14. Averaging produces "0.8 units per week" — a number that is wrong every week. Croston's method separates the two questions — *how often* (a smooth estimate of the inter-arrival interval) and *how big* (a smooth estimate of the size when it comes) — and the forecast is size-over-interval. Its successors (SBA's bias correction; the more recent intermittent-demand models) improve the edges; the discipline is the separation. The Soulfya's kitchen applies it to slow-moving packaging SKUs, where it cut stock-outs at *lower* inventory — the rare case where the fancy method wins on both axes at once.

## 64.5 Rolling-Origin Evaluation

One train/test split flatters whatever period you chose. The honest league table (Chapter 28's discipline, extended) rolls the origin: fit to everything through March, forecast April; through April, forecast May; and so on across seasons — so the league table is earned across a year of changing conditions, including the promotions and the shocks.

```python
from sklearn.metrics import mean_absolute_error
def mase(actual, forecast, naive):
    return (mean_absolute_error(actual, forecast)
            / mean_absolute_error(actual, naive))
# rolling table: seasonal-naive, ETS, ARIMA, reconciliation — every month, MASE
```

The rule that keeps it honest: **the seasonal-naive baseline appears in every table**, and any method that cannot beat it on the organisation's real loss (stock-out cost, not MAPE) is not deployed, however elegant its mathematics.

## 64.6 Failure Modes

- **The single-number forecast** — the point estimate without an interval, delivered to a team that will make a stock decision with it.
- **The unbalanced hierarchy** — reconciling chain and outlets but not categories, so the disagreement just moves to the level you ignored.
- **Intervals nobody believes** — bands so narrow they are broken weekly (fit to calm periods) or so wide they are useless (fit to the shock year); the bootstrap on rolling residuals is the cure for both.
- **Averaging intermittent demand** — the 0.8-units-per-week trap; separate frequency and size.

> **Teaching Tip — Make the sum work:** give students three levels of a hierarchy with deliberately inconsistent forecasts and one instruction: "the board will see all three; make them agree, and be able to defend every change." The debate that follows — bottom-up versus top-down versus blend — teaches MinT's motivation better than the matrix algebra ever will, and the reconciliation formula then lands as the resolution of an argument they personally had.

## Key Takeaways

- Hierarchies must reconcile: forecast every level, then blend so they agree — MinT formalises what a good analyst does by hand.
- The interval is the product: bootstrap the paths, report asymmetric p10/p90, and let the stocking decision live in the fan.
- Intermittent demand needs Croston's separation: how often, and how big.
- League tables roll: seasonal-naive in every table, evaluated on the organisation's real loss.
- A forecast without a range is a rumour; a range without a baseline is unfalsifiable.

## Practice Lab

1. Build the three-level hierarchy for Soulfya's (chain, outlets, categories); reconcile bottom-up, top-down, and MinT-style; report how much each level moved and why.
2. Bootstrap the Saturday-dinner forecast: 1,000 resampled paths, the p10/p50/p90 fan, and the stocking decision the asymmetry implies.
3. Fit Croston (and SBA) on the slow-moving packaging SKUs; compare against the moving average on stock-out rate *and* inventory value — the two-axis win.
4. Run the rolling-origin league: seasonal-naive, ETS, and your model across twelve months; report MASE per month and name the month your model lost and why.
5. The promotion double-count: show how independent outlet forecasts sum to more than the chain signal, and how reconciliation resolves it; write the memo the ops meeting needs.
6. Interval audit: take any forecast your organisation produces; backtest its stated interval over the last year — how often did reality fall outside it? (For an honest 80% interval: about one week in five.)

## Further Reading

- *Forecasting: Principles and Practice* — Hyndman and Athanasopoulos (free online; the hierarchical chapters)
- Hyndman et al., "Optimal forecast reconciliation for hierarchical and grouped time series"
- Chapter 28 (the foundations this part extends), Chapter 67 (simulation that consumes these fans), Chapter 58 (where intermittent demand bites)
