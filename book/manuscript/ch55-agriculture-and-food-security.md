# Chapter 55: Agriculture and Food Security — The Chikafu Foods and NGA Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Farming is a weather hedge wearing overalls; food security analytics is the hedge book."

### In this chapter you will learn

- The agriculture canvas: yield, logistics, and markets as one food-system problem.
- Yield forecasting that combines agronomy, weather, and remote sensing — with honest error bars.
- Grain logistics and the buffer stock: seasonality, storage economics, and the import decision.
- Smallholder data: satellite plus surveys, and the bias in every convenient source.
- The co-operative evaluation pattern: Sable Fields and the missing-data discipline.
- Failure modes: the average farm, the planting-date fallacy, and precision without coverage.

## 55.1 The Food-System Question

**Chikafu Foods** is a fictional grain miller and food processor: it buys maize and small grains from 40,000 smallholders and three commercial estates, mills for retail, and holds a supply contract with the **National Grain Authority (NGA)** — the fictional state buyer that runs the strategic reserve. Their analytical questions chain together: **how much will grow** (yield forecast), **where and when will it move** (logistics), **what should we pay and stock** (markets and the buffer), and **what did the programmes actually do** (evaluation). Agriculture is the playbook where the *system* is the unit: a miller's forecast error becomes the NGA's storage decision becomes the consumer's price — and the analyst who sees only their own link optimises the wrong thing.

| Slot | Chikafu / NGA's answer |
|---|---|
| Core question | How much grain, where, when — and what should the reserve do about it? |
| Unit of analysis | The field/plot for yield; the depot-week for logistics; the district-season for food security |
| Key metrics | Yield (t/ha), forecast error at lead time, depot stock weeks, price seasonality, food-security coverage |
| Data reality | Remote sensing pixels, sparse weather stations, farmer registers with staleness, market price boards |
| First project | The yield forecast with published, scored error — plus the error history |
| Failure mode | Confident averages: the mean yield that describes no farm and the reserve that trusts it |

## 55.2 Yield Forecasting with Honest Error Bars

The yield forecast is the sector's headline model, and its craft is layering information sources with their uncertainties:

- **Agronomic structure first**: planted area × trend yield, adjusted for season start (planting dates are a strong signal — late onset means lower yield potential, and the adjustment is bounded by agronomy, not fit).
- **Weather on top**: rainfall accumulation and distribution by dekad (ten-day period) from the sparse station network plus gridded products; distribution matters — three well-spaced rains beat one deluge.
- **Remote sensing**: vegetation indices (NDVI-type) from public satellites give a canopy-health read per pixel, aggregated to district — the pixel sees every field, including the ones nobody reported.
- **Ground truth**: crop-cut surveys on sampled plots — small, expensive, and the only anchor that keeps the satellite honest.

The forecast is published with the *history of its errors*: "district maize yield, 1.9–2.3 t/ha, past-April error ±0.4". A forecast without its scored error history is a rumour with decimals — and the NGA's storage decisions are exactly the kind of decision (Chapter 61's language) that deserves an interval, not a point.

```python
# Layered yield forecast: agronomic base, weather adjustment, NDVI residual
base = planted_area * trend_yield              # agronomic anchor
weather_adj = 1.0 + (-0.35) * late_onset_frac  # bounded by agronomy
ndvi_adj = 1.0 + 0.5 * (ndvi_z - ndvi_clim_z)  # canopy anomaly
forecast = base * weather_adj * ndvi_adj
err = forecast - crop_cut_yield                # scored against ground truth
```

## 55.3 The Buffer Stock and the Logistics Layer

The NGA's reserve problem is seasonal by construction: buy at harvest when prices sag, release in the hungry months when prices spike, hold enough to smooth but not so much that storage and losses eat the budget. The analytics are Chapter 28's forecasting (price seasonality with its shocks), Chapter 47's optimisation (depot siting and movement minimisation — grain is heavy and fuel is dear), and one accounting discipline: **carryover cost per tonne per month** (storage + interest + shrinkage), because the release decision is "sell now versus hold", and that number is the whole trade. The failure to fear is the reserve that becomes a hoard: bought for price smoothing, held for prestige, financing itself out of existence.

## 55.4 Smallholder Data: Satellite and Survey

The sector's hardest data problem: the average farm is 1.5 hectares, transactions are informal, and every convenient source is biased. Farmer registers overcount active farmers (dead entries never leave); purchases undercount sales to informal traders; satellite sees canopy but not crop (maize and weeds are both green). The craft is triangulation with explicit bias accounting — satellite area as the coverage layer, register+survey as the behaviour layer, and the gap between them *reported* as a finding, not patched silently. **From Your Toolkit — Stata:** the crop-cut and household survey analysis is Stata territory — design-based estimates, panel regressions for programme effects, and the robust standard errors that keep small-sample honesty — with Chapter 15's missing-data discipline standing behind it.

## 55.5 The Evaluation Pattern: Sable Fields

The co-operative evaluation of Appendix J Case 5 (Sable Fields Co-operative: 2,400 farmers, a four-year productivity grant, and a year of missing records) is the sector's canonical evaluation shape: treatment that was not randomised, data with gaps that are informative, outcomes complicated by exit. The pattern — quantify the missingness, choose the strategy, bound the estimate, model the exits with survival curves (Chapter 63), and publish the gap in the first paragraph — is the discipline every agriculture programme report owes its funders. Agriculture is where evaluation honesty is most tested, because the funders want transformation stories and the data usually offers bridges.

## 55.6 Failure Modes

- **The average farm** — mean yield over a right-skewed distribution of 1.5-hectare plots; median and deciles are the sector's honest descriptors.
- **The planting-date fallacy** — late planting correlates with poorer farmers, so "late planters yield less" is partly poverty, not delay; the covariate structure must be respected before advising on timing.
- **Precision without coverage** — a beautiful model on the three commercial estates' clean data, extrapolated to 40,000 smallholders it never saw; the coverage audit belongs in every agriculture report.
- **The prestige reserve** — Section 55.3's hoard; the buffer stock needs its own dashboard, with carryover cost and release triggers, before it needs a forecast.

> **Teaching Tip — The two-map exercise:** hand students two district maps side by side — satellite greenness and crop-cut yield — and ask what the differences mean. The discussion discovers every section of this chapter: coverage versus ground truth, canopy versus crop, and why the reserve needs both maps plus a survey. It is the whole playbook in one visual, and it teaches the humility of remote sensing better than any lecture.

## Key Takeaways

- Agriculture is a system: yield, logistics, and markets chain together, and optimising one link in isolation mistimes the whole.
- Yield forecasts layer agronomy, weather, and remote sensing — and publish their scored error history or count as rumours.
- The buffer stock is a smoothing instrument with a carrying cost; give it triggers and a dashboard, not prestige.
- Every convenient smallholder source is biased; triangulate and report the gaps instead of patching them silently.
- Programme evaluations follow the Sable Fields pattern: missingness quantified, estimates bounded, exits modelled, honesty in the first paragraph.

## Practice Lab

1. Build the layered district yield forecast on the season's data; score it against crop-cut plots, and write the release note with the interval and the error history attached.
2. Price seasonality: decompose five years of market maize prices into trend, seasonal, and shock components; recommend the reserve's buy window and the release trigger.
3. The carryover audit: compute storage, interest, and shrinkage per tonne per month for each depot; identify the depot where holding grain is destroying value.
4. Coverage audit: compare register-reported planted area against satellite-derived area by district; map the gap and write the two hypotheses it most plausibly supports.
5. Design the Sable Fields successor evaluation: a grant renewal where you control the design from day one — specify the randomisation (or its honest alternative), the measurement plan, and the pre-registered analysis.
6. The food-security memo: the forecast comes in 12% below trend — what does Chikafu do, what does the NGA do, and what does each need to know that the other holds?

## Further Reading

- *Agricultural Production Economics* — the yield-response foundations
- Appendix J Case 5 (Sable Fields) for the full evaluation; Chapter 63 (survival for exits); Chapter 68 (privacy for farmer registers)
- FAO's seasonal forecast methodology papers — the best public example of error-scored forecasting
