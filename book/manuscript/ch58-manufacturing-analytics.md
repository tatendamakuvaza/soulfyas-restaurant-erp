# Chapter 58: Manufacturing Analytics — The Sabvura Industries Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "The factory already knows; the data's job is to get the knowledge out before the shift ends."

### In this chapter you will learn

- The manufacturing canvas: throughput, quality, and uptime as one OEE story.
- Overall Equipment Effectiveness: the three losses and the availability × performance × quality arithmetic.
- Statistical process control: control charts that separate signal from shop-floor noise.
- Predictive maintenance: the survival-model discipline for machines that age.
- From forecast to line: production scheduling under Chapter 47's optimisation.
- Failure modes: local OEE, the cherry-picked chart, and the sensor swamp.

## 58.1 The Manufacturing Question

**Sabvura Industries** is a fictional garment manufacturer: three production lines (cutting, sewing, finishing), 410 operators, an export contract with a European buyer whose audits arrive unannounced, and a factory manager who keeps a whiteboard she calls "the truth" — hourly counts, defects, and downtime, written by hand. The analytical questions: **are the lines producing what they could** (OEE), **is quality stable or drifting** (SPC), **which machines will fail and when** (maintenance), and **what should we make next week** (scheduling). The distinctive feature of manufacturing data: it is generated *on the line, in real time, by machines and operators who will tell you the truth if the system makes truth-telling easy* — and the analyst's first job is usually to make the whiteboard digital without killing its honesty.

| Slot | Sabvura's answer |
|---|---|
| Core question | Throughput, quality, uptime — where do the hours go? |
| Unit of analysis | The machine-hour; the lot/batch; the operator-shift |
| Key metrics | OEE and its three components, defect rate by defect class, mean time between failures, schedule adherence |
| Data reality | Machine counters, operator log sheets, QC inspections by lot, maintenance records in prose |
| First project | The downtime Pareto, machine-logged and reconciled |
| Failure mode | Local optimisation: a line that hits OEE by pushing defects downstream |

## 58.2 OEE: The Three Losses

Overall Equipment Effectiveness is the sector's headline metric because it multiplies the three ways a shift is lost:

- **Availability** — run time ÷ planned time. Losses: breakdowns, changeovers, waiting for material.
- **Performance** — actual output ÷ output at rated speed. Losses: micro-stops, slow cycles.
- **Quality** — good units ÷ total units. Losses: defects and rework.

The arithmetic is honest and humbling: a world-class 85% OEE is 0.90 × 0.95 × 0.995 — three decent numbers multiplied into an excellence few reach; Sabvura's finishing line runs 58%, which is three mediocre numbers multiplied into a management conversation. The craft is decomposition: OEE as a single number is a scoreboard, OEE *split into its three components by line and shift* is a diagnosis, and the downtime Pareto is where the first improvement project always lives.

```sql
SELECT line, shift_date, shift,
       SUM(run_minutes) / SUM(planned_minutes)          AS availability,
       SUM(actual_units) / NULLIF(SUM(rated_units), 0)   AS performance,
       SUM(good_units)  / NULLIF(SUM(actual_units), 0)   AS quality,
       SUM(run_minutes) / SUM(planned_minutes)
         * SUM(actual_units) / NULLIF(SUM(rated_units), 0)
         * SUM(good_units)  / NULLIF(SUM(actual_units), 0) AS oee
FROM line_counters
GROUP BY line, shift_date, shift;
```

## 58.3 Statistical Process Control

SPC is Chapter 14's inference, industrialised: a control chart is a hypothesis test drawn repeatedly through time, separating common-cause noise (leave it alone; tampering adds variance) from special-cause signals (find the reason, now). The discipline that survives every software fashion:

```python
def xbar_chart(measurements, subgroup=5, sigma_k=3):
    import numpy as np
    groups = [measurements[i:i+subgroup] for i in range(0, len(measurements), subgroup)]
    means = np.array([g.mean() for g in groups])
    cl, sigma = means.mean(), np.array([g.std(ddof=1) for g in groups]).mean()
    ucl, lcl = cl + sigma_k * sigma / np.sqrt(subgroup), cl - sigma_k * sigma / np.sqrt(subgroup)
    out = [g for g, m in zip(groups, means) if m > ucl or m < lcl]
    return cl, lcl, ucl, out   # out-of-control subgroups, each with its hours
```

The rule that gives SPC its power: **respond to signals, leave noise alone.** The classic manufacturing sin is adjusting a process that was stable — adding variance while feeling busy. The analyst's contribution is annotating the chart (which signal coincided with the fabric-batch change, the operator changeover, the humidity spike) so the investigation starts warm.

## 58.4 Predictive Maintenance

Machines age, and the honest model of aging is Chapter 63's survival analysis: each machine's hazard of failure as a function of age, run-hours, and condition signals (vibration, temperature, error codes). The discipline matters more than the model: survival curves give *probabilities over time windows* ("30% failure hazard in the next 200 run-hours"), not the false-precision "fails Thursday"; maintenance scheduling is then Chapter 47's optimisation (schedule the intervention to minimise expected downtime cost, given the hazard and the parts lead time). The cautionary tale every plant lives: the model that flags a failure risk the technicians already schedule around — predictive maintenance's value is over and above *experienced maintenance planning*, and proving that requires the same holdout discipline as any model (Chapter 23's league table, greasy edition).

**From Your Toolkit — Excel:** the maintenance backlog and the MTBF league table live happily in Excel pivot tables, and that is the right first home — the maintenance planners already work there. The survival model informs the planners; it does not replace them, and the interface is a table they trust.

## 58.5 From Forecast to Line

The scheduling layer closes the loop with the demand side: Chapter 28's order forecasts become Chapter 47's constrained schedule — lines, changeovers (whose cost in minutes is the real currency), operator rosters, and the export buyer's audit windows. The craft is making constraints explicit rather than implied: the intern's optimisation from Appendix J Case 3 failed not in its arithmetic but in its *unstated* constraint (the loading rule); the same lesson walks this factory's floor. A schedule no one can explain is a schedule the floor will quietly override — explainability is operational, not cosmetic.

## 58.6 Failure Modes

- **Local OEE** — the cutting line hits its target by passing borderline fabric to sewing; OEE must be measured at the *system* level, or the target destroys the plant.
- **The cherry-picked chart** — the control chart shown only in its stable months; keep the full run and the annotations, always.
- **The sensor swamp** — instrumenting everything and analysing nothing: start from the decision (which changeover? which intervention?) and instrument backwards from it.
- **The whiteboard's revenge** — the new digital system that operators feed garbage because truth-telling became harder than the paper it replaced; watch the reconciliation gap, and fix the form before blaming the floor.

> **Teaching Tip — The paper OEE:** run one class session entirely on a paper log sheet: students record a simulated line's hour (planned, run, units, defects, reasons for stops) by hand, then compute OEE and the Pareto themselves. The lesson is double: they internalise the arithmetic *and* they feel how data quality is won or lost at the point of entry — the whiteboard manager's problem, lived for an hour.

## Key Takeaways

- OEE is a scoreboard; its three components by line and shift are the diagnosis, and the downtime Pareto is the first project.
- SPC is repeated inference: respond to special-cause signals, leave common-cause noise alone — tampering is the industrial original sin.
- Predictive maintenance is survival curves plus scheduling optimisation, and must beat experienced planners in a fair holdout to count.
- Constraints belong in the model, not in the lore; a schedule the floor cannot explain is a schedule it will override.
- Data quality is won at the point of entry: make truth-telling easier than the paper it replaced.

## Practice Lab

1. Compute OEE and its components by line and shift from the line counters (Appendix F generator); build the downtime Pareto and name the first improvement project with its expected minutes.
2. Build the X-bar chart for seam strength by line; annotate the out-of-control subgroups against the batch and operator logs; write the two investigation memos the chart demands.
3. Fit the survival model for the cutting machines (age, run-hours, vibration); produce each machine's 200-hour hazard window, and the maintenance schedule that minimises expected downtime cost.
4. The league-table test: does your survival model beat the planners' existing PM calendar in a backtest? Design the fair comparison and report the result honestly.
5. The scheduling round: given the order book, changeover matrix, and rosters, produce next week's schedule — then write the one-page explanation the floor supervisor reads aloud at the shift briefing.
6. The reconciliation audit: compare the digital counters against the whiteboard's week; quantify the gap by reason code, and propose the form change that closes the largest one.

## Further Reading

- *Out of the Crisis* — W. Edwards Deming (SPC and the tampering doctrine)
- *OEE for Operators* — Nakajima (the source text, short and complete)
- Chapter 47 (scheduling optimisation), Chapter 63 (survival analysis), Chapter 14 (the inference beneath SPC)
