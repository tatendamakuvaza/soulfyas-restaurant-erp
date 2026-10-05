# Chapter 59: Transport and Logistics — The Kunaka Logistics Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Logistics is the mathematics of promises: an ETA is a contract signed by a queue."

### In this chapter you will learn

- The logistics canvas: routing, reliability, fleet health, and the cold chain.
- The constraint discipline of routing optimisation — and why the optimiser's world is not the world.
- ETA prediction: the regression that respects the road.
- Fleet analytics: utilisation, maintenance, and the cost per delivered case.
- IoT data engineering for cold-chain compliance: the temperature excursion ledger.
- Failure modes: average speed, the unmodelled constraint, and the dashboard that lies to the customer.

## 59.1 The Logistics Question

**Kunaka Logistics** is the fictional cold-chain operator you met in Appendix J Case 3: one depot, 62 retail drop points, 14 vehicles, and a dairy client whose product fails quality control if any drop arrives more than four hours after loading. Its analytical questions: **which stops on which vehicle in which order** (routing), **when will it actually arrive** (ETA), **what does each vehicle really cost** (fleet economics), and **did the cold chain hold** (compliance). The distinctive feature: logistics is the discipline of *constraints wearing costumes* — time windows, temperature ramps, loading order, driver hours — and the recurring failure of logistics analytics is building a beautiful model of a world without them.

| Slot | Kunaka's answer |
|---|---|
| Core question | Which routes, in what order, at what reliability and cost? |
| Unit of analysis | The stop; the trip; the vehicle-day |
| Key metrics | Cost per delivered case, on-time %, distance per drop, temperature excursions, fleet utilisation |
| Data reality | GPS traces, telematics temperature logs, drive-time matrices, driver manifests on paper, traffic by hour |
| First project | The on-time baseline and the excursion ledger |
| Failure mode | Optimising distance in a world that runs on time |

## 59.2 Routing: The Constraint Discipline

Vehicle routing is a canonical optimisation problem — and a canonical warning. Case 3's story is the sector in miniature: an 18% distance saving that became 11% once drive-times replaced distances and the four-hour constraint was enforced, then lost two routes entirely to the loading-order rule nobody wrote down. The practitioner's method:

1. **Write the constraints as a list, with owners.** Time windows, capacity, cold-chain ramps, driver hours, the customer's receiving dock that closes at 16:00. Each constraint gets a name and a source — the union rep's sentence about loading order is data.
2. **Solve with the simplest method you can explain.** Cluster-then-sequence (group stops by geography, then order each cluster greedily by time) is usually within a few percent of the optimum and can be explained to a driver — which is worth more than the missing percent.
3. **Validate by simulation, not assertion** (Chapter 67): Monte Carlo the plan under demand and traffic variance; read the p10 day. The plan that survives the p10 day is the plan; the rest is a diagram.
4. **Pilot on one route for two weeks** before signing the network. The pilot is where the unmodelled constraints introduce themselves.

## 59.3 ETA Prediction

The customer-facing layer is a regression problem with one unusual property: **its error has a sign that matters**. An ETA five minutes early is a promise kept; five minutes late is a promise broken, and the asymmetric cost belongs in the loss function — predict the *quantile* that makes lateness rare enough to match the service promise (Chapter 25's quantile thinking, delivered). The features are the road's honest structure: distance and traffic by hour, stop durations learned from GPS dwell times, the dock queue at the receiving end, and the trip's own history at that hour.

```python
model = GradientBoostingRegressor(loss="quantile", alpha=0.85)  # 85th percentile
model.fit(features, arrival_deltas_minutes)   # positive = late
# The promise: "arrives by X" where X is the 85th-percentile arrival.
```

**From Your Toolkit — Excel:** the ETA *audit* is a pivot table the operations team can own: promised versus actual arrival by route and hour, the lateness rate, and the worst three stops — the analysis that keeps the model honest lives in the tool the dispatcher already has open.

## 59.4 Fleet Economics

The unit that disciplines everything is **cost per delivered case** — fuel, driver, maintenance, depreciation, and the cold-chain energy, divided by cases delivered — because it exposes the trade the fleet runs every day: an under-filled van at 40% capacity has a beautiful cost-per-kilometre and a terrible cost-per-case. The analytics: utilisation by day and route (the half-empty Tuesday run), maintenance cost per vehicle against age and odometer (Chapter 63's survival hazard, feeding the replace-or-repair decision), and the fixed-versus-variable split that answers the lease question. The quiet discipline: allocate costs to trips honestly (including the depot overheads), or the route-level profitability ranking is fiction with decimals.

## 59.5 The Cold-Chain Ledger

Cold-chain compliance is an IoT data engineering problem before it is an analytics one: temperature sensors stream intervals; excursions must be detected, attributed (which stop's door opening?), and reported to the dairy client within the contract's window. The artefact is the **excursion ledger** — every trip's temperature trace, every breach flagged with the stop, duration, and peak, and the reconciliation against the quality standard. The engineering is Chapter 9's pipeline discipline (validation gates on sensor data — stuck readings, gaps, clock drift) with Chapter 46's anomaly logic on top: the sensor that reports a perfectly flat 4.0°C for three hours is not a healthy freezer; it is a broken sensor, and the ledger must treat it as a data incident, not a compliance pass.

## 59.6 Failure Modes

- **Average speed** — routing on mean drive-times schedules the fleet for a world without the 16:00 truck; drive-time *distributions* by hour are the honest input.
- **The unmodelled constraint** — Case 3's lesson: constraints live in drivers' heads and unions' rules until they are written as data.
- **The dashboard that lies to the customer** — an on-time metric defined on departure rather than arrival; every customer-facing metric must name the clock it uses.
- **Sensor silence as health** — the flat line is an incident; validation gates make silence loud.

> **Teaching Tip — The drivers' meeting:** have students present a route redesign to a panel playing drivers, dispatchers, and the union rep (Case 3's cast). The panel's first question is always a constraint the model missed — and the lesson, that the person closest to the work knows the model's missing variable, lands as lived experience rather than a maxim. Rotate roles; the next cohort's modellers are this cohort's drivers.

## Key Takeaways

- Constraints are the logistics model: list them with owners, solve with methods you can explain, validate by simulation on the p10 day, and pilot before signing.
- ETA models predict service, not averages: fit the quantile that matches the promise, and audit promised-versus-actual in the dispatcher's own tool.
- Cost per delivered case disciplines the fleet; allocate overheads honestly or the route ranking is fiction.
- The cold-chain ledger treats sensor silence as an incident — validation gates first, compliance second.
- The person closest to the work knows the missing constraint; ask before optimising.

## Practice Lab

1. Build the on-time baseline and excursion ledger from the telematics extract (Appendix F generator); report on-time % by route and the three worst stops, naming the clock each metric uses.
2. Refit the Case 3 routing with drive-time distributions and the loading constraint; report the honest saving and the two assumptions you most want validated in the pilot.
3. Fit the ETA quantile model; choose the service quantile, and show the lateness rate it implies against the customer's contract threshold.
4. The fleet economics table: cost per delivered case by vehicle and route; identify the under-filled run and the replace-or-repair candidate from the maintenance hazard curve.
5. The sensor audit: run the validation gates on a month of temperature logs; document the flat-line sensors, the clock drift, and what the compliance number becomes once they are excluded.
6. Run the drivers' meeting on your own redesign; log every constraint the panel adds, and revise the model and its explanation in one page.

## Further Reading

- *Vehicle Routing* — Toth and Vigo (the reference; read Chapter 1 and the heuristics chapters)
- Appendix J Case 3 (the van in the wrong place) — this playbook's full worked case
- Chapter 47 (optimisation), Chapter 67 (simulation), Chapter 25 (quantiles for service promises)
