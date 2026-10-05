# Chapter 56: Energy Analytics — The Sable Energy Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "An electricity system has no warehouse: every kilowatt is consumed the instant it is made, forever."

### In this chapter you will learn

- The energy canvas: demand, supply, and money under a zero-inventory constraint.
- Load forecasting: the model that runs the company, from daily shape to tariff-sensitive peaks.
- Prepaid meters and collections analytics: revenue assurance as a first-class product.
- Losses: technical versus non-technical, and the anomaly discipline that tells them apart.
- Tariff and subsidy analysis with elasticity respected — the policy layer.
- Failure modes: the average day, the duck curve, and the meter that lies.

## 56.1 The Energy Question

**Sable Energy** is a fictional national distribution utility: 780,000 metered connections, a peak demand that has doubled in a decade, prepaid meters in most homes, and a generation mix it partly controls (two coal units, one hydro contract, growing solar) and partly prays over (rainfall for the hydro, evening for the solar). The defining constraint makes energy unique among this part's playbooks: **electricity cannot be stored at scale**, so supply must meet demand every minute — which makes forecasting not a reporting function but the operational spine. The analytical questions: **what will demand be** (load forecast), **is everyone paying** (collections and losses), **where is the power going that no one paid for** (loss analytics), and **what should it cost** (tariffs and subsidies).

| Slot | Sable Energy's answer |
|---|---|
| Core question | How much power, when; who is paying; where are the losses? |
| Unit of analysis | The connection × 30-minute interval; the feeder-day; the tariff band |
| Key metrics | Peak demand (MW) and timing, forecast MAPE at day-ahead, collection ratio, loss % (technical vs nontechnical), load factor |
| Data reality | Smart-meter interval data (partial), prepaid vending logs, SCADA feeds, feeder sensors, theft and tamper records |
| First project | The day-ahead load forecast with a published error, by region |
| Failure mode | Planning the average day and being destroyed by the peak |

## 56.2 Load Forecasting: The Model That Runs the Company

Demand is the most structured series in this book: strong daily shape (morning rise, evening peak), weekly shape (weekday/weekend), seasonal shape (winter heating, summer cooling), and event structure (paydays, public holidays, a national football final). The craft is treating those structures as features, then letting the model handle the residuals:

```python
features = pd.DataFrame({
    "hour":       ts.index.hour,
    "dow":        ts.index.dayofweek,
    "is_weekend": (ts.index.dayofweek >= 5).astype(int),
    "temp_c":     weather.reindex(ts.index)["temp"],
    "payday_0to2": payday_proximity(ts.index),   # 0,1,2 days after payday
    "lag_1d":     ts["mw"].shift(24 * 2),        # same interval yesterday
    "lag_1w":     ts["mw"].shift(24 * 2 * 7),    # same interval last week
})
```

The evaluation is Chapter 28's seasonal-naive discipline (the league table, always) and the metric that matters operationally: **day-ahead MAPE at the evening peak**, because a 3% average error that is 8% at 18:30 is a utility that buys emergency power at the worst prices. The forecast feeds the unit-commitment decision (which generators run tomorrow), so its error has a price tag — and Chapter 61's counterfactual language applies: the value of a better forecast is the avoided cost of the mistakes, computable and reportable.

## 56.3 The Prepaid Layer: Collections and Vending

Prepaid metering turns the revenue question inside-out: instead of billing after consumption, the utility collects *before* it — and analytics shifts from receivables to vending behaviour. The questions are behavioural and operational: purchase frequency and size by segment (a household's vending rhythm is its energy fingerprint), disconnection-and-reconnection patterns, and the *timing* load — paydays, school fees season, harvest income in rural feeders. **From Your Toolkit — Excel and Power BI:** the vending analytics layer is a classic Excel-to-Power-BI product: purchase registers aggregated to connection-week, a decomposition view for seasonality, and a collections dashboard the commercial team lives in. The distinctive energy lesson for the analyst: in prepaid systems, **demand data doubles as payment-capability data**, and the two must be read together — a feeder whose consumption falls while its vending rises is telling you something about metering, not weather.

## 56.4 Losses: Technical and Non-Technical

Losses are the gap between energy bought (or generated) and energy sold, and the analytics exist to split that gap in two: **technical losses** (physics — resistance in lines and transformers, computable from network models and loading) and **non-technical losses** (theft, tampering, metering error, billing gaps — the human share). The method is Chapter 46's anomaly discipline at feeder granularity:

- Energy balance per feeder-day: energy in (substation) versus energy vended plus estimated unmetered use — the residual is the loss.
- Profile the residuals: technical losses rise smoothly with load squared; tampering leaves step changes and consumption-collapse signatures that physics cannot explain.
- Rank and investigate: feeders ranked by unexplained residual per connection, crossed with tamper-inspection outcomes, produce the inspection schedule — and the *audit* of whether inspections are working.

The quiet trap: an aggressive loss-reduction campaign can chase the physics. The split — modelled technical loss versus residual — is what keeps the campaign aimed at the human share.

## 56.5 Tariffs, Subsidies, and the Elasticity Layer

The policy layer is where energy analytics meets Chapter 61 head-on: tariffs change behaviour, and a tariff modelled with zero elasticity is a plan for a world that does not exist. The pattern is Appendix J Case 4's (Harare Metro Water) transposed: cross-subsidy designs (lifeline blocks funded by higher bands) evaluated under elasticity estimated from historical tariff shocks, with revenue-neutrality checked as a *range*, never a point. Sable Energy's version: the lifeline block (first 50 kWh cheaper) whose true cost depends on how many high-band customers respond to their price rise by installing solar — the elasticity term, wearing panels.

## 56.6 Failure Modes

- **Planning the average day** — capacity is sized and committed against peaks; every average-based report understates the risk by construction.
- **The duck curve** — solar shifts net demand's shape (deep midday trough, steep evening ramp); a forecast trained on gross consumption miscommits the evening units exactly when they are dear.
- **The meter that lies** — smart-meter data is sensor data: gaps, drift, and stuck registers are findings to model (Chapter 11's validation gates, per interval), not background noise to average through.
- **Loss theatre** — reporting total losses without the technical split, then celebrating reductions that were physics all along.

> **Teaching Tip — The zero-inventory hour:** open the class by asking what a warehouse is for, then deleting it from the electricity system. Everything in the chapter follows from that one absence: forecasting becomes operations, storage becomes the most expensive product on earth (batteries), and the evening peak becomes the moment the company lives or dies. Students who feel the constraint stop treating load forecasting as "just a time series".

## Key Takeaways

- Electricity's zero-inventory constraint makes the load forecast the operational spine: evaluate at day-ahead peak MAPE, and price the forecast's errors.
- Prepaid systems shift analytics from receivables to vending behaviour — and consumption data doubles as payment-capability data.
- Loss analytics exists to split physics from people: model technical loss, then investigate the residual, and audit the investigations.
- Tariff and subsidy analysis respects elasticity — revenue neutrality is a range, and the lifeline block has a solar-panel term.
- Every average is a trap: peaks, ramps, and p90 days are the utility's real calendar.

## Practice Lab

1. Build the day-ahead load forecast for one region (Appendix F generator supplies interval demand and weather); run the league table including seasonal-naive, and report MAPE overall and at the evening peak.
2. Price the forecast: given balancing costs, translate the forecast error distribution into an expected cost, and the 2-point MAPE improvement into its avoided-cost value.
3. The vending layer: build connection-week vending aggregates, find the payday signature, and identify three feeders whose consumption-vending divergence suggests metering problems.
4. The loss split: compute feeder-day residuals, estimate the technical loss model, rank feeders by unexplained residual per connection, and design the inspection experiment that tests whether the ranking works.
5. The tariff memo: evaluate the lifeline design under elasticity bounds from the last tariff shock; show the revenue range and name the political question the range hides.
6. The resilience test: simulate the p10 hydro-rainfall year against your demand forecast — what breaks first, and what would you pre-negotiate?

## Further Reading

- *Electricity Economics* — the tariff and peak-pricing foundations
- Chapter 28 (forecasting), Chapter 46 (anomaly detection for losses), Chapter 61 (elasticity and counterfactuals)
- Appendix J Case 4 for the cross-subsidy evaluation pattern this chapter borrows
