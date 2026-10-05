# Chapter 57: Government and Public Sector Analytics — The Harare Metro Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Public data answers to everyone at once: the minister, the auditor, the taxpayer, and the person in the queue."

### In this chapter you will learn

- The public-sector canvas: services, evidence, and scrutiny under permanent visibility.
- Programme evaluation culture: the DiD discipline and the null result that must be published.
- Operational analytics for public services: queues, registers, and the trust problem.
- Open data and privacy: publication as an engineering problem.
- Procurement analytics: the anomaly layer where public money leaks.
- Failure modes: Goodhart's law at national scale and the report nobody reads.

## 57.1 The Public-Sector Question

**Harare Metro** is the fictional metropolitan authority you met in Appendix J Case 4 (the water tariff) — but its analytical life is broader than one tariff: refuse collection, water and sanitation, road maintenance, licensing, and the social programmes it administers on behalf of national government. The public-sector pattern differs from every other playbook in Part X on three axes: **many masters** (the political principal changes, the permanent service endures, the public owns the data), **full scrutiny** (an auditor, a journalist, or an opposition councillor may read any number you publish), and **the null-result duty** (programmes must be evaluated whether or not they worked — a cancelled finding is a public wrong).

| Slot | Harare Metro's answer |
|---|---|
| Core question | Which services work, for whom, at what cost — provably? |
| Unit of analysis | The service interaction (permit, collection, connection); the ward-month; the programme-beneficiary |
| Key metrics | Service level (collections/permits per target), unit cost, programme coverage and leakage, citizen wait times |
| Data reality | Legacy systems, paper registers, ward-level politics in every count, periodic national surveys |
| First project | The service-level baseline: one service, measured honestly, published |
| Failure mode | Indicators that become targets (Goodhart) and evaluation that becomes advocacy |

## 57.2 The Service Baseline and the Trust Problem

The first project in any public analytics practice is establishing a *baseline anyone can check*: for one service — refuse collection is the classic — the fleet's GPS tracks, the ward collection schedule, and a complaint log, reconciled into a single published number: "86% of scheduled collections achieved, by ward, this quarter". The trust problem is the real opponent: public-sector data has been politicised before, and the analyst's craft is *showing the work* — methodology published, data extractable, numbers reconcilable by any journalist with a spreadsheet. Chapter 42's lineage discipline is not a nice-to-have here; it is the difference between a dashboard and a press release. **From Your Toolkit — Power BI:** the public dashboard is a Power BI (or open-source equivalent) product with one unusual requirement: every published figure must carry its provenance link, because the audience includes adversaries by design.

## 57.3 Programme Evaluation Culture

Chapter 61's methods belong here at full strength: difference-in-differences, synthetic control, and the interrupted time series are the public sector's workhorses, because randomisation is usually politically impossible. The Metro's discipline, learned the hard way:

1. **Pre-register the analysis** — the question, the comparison, and the success metric, dated before the data arrive. In politics, the temptation to redefine success afterwards is structural, and pre-registration is the structural answer.
2. **Respect the comparison's honesty** — the ward next door is not a control group until you show it trends in parallel (DiD's assumption, checked and displayed, per Chapter 61).
3. **Publish the nulls** — the street-lighting programme that did not move crime statistics is a finding the next budget needs; suppressing it converts an error into a tradition.
4. **Bound the estimate** — "reduced reported complaints by 15% ± 8, with reporting artefacts unquantified" is the honest register; point estimates without intervals are lobbying with extra steps.

## 57.4 Operational Analytics: Queues and Registers

The service layer is Chapter 66's queueing in civic clothing: the licensing office is a queue (the Wq arithmetic that turned "we feel busy" into staffing plans in Chapter 54 works verbatim here), and the register is the product — a permit tracked from application to issuance, with the stage-level timestamps that expose where the month of delay actually lives. The public-sector twist is *adversarial demand*: the queue includes people who will pay to skip it, so process analytics (where the bottlenecks are) must be paired with integrity analytics (who skips, how often, at which stage) — Section 57.5's toolkit applied inward.

## 57.5 Procurement Analytics

Public procurement is where the money leaks, and the anomaly discipline (Chapter 46) has its highest civic value here: contracts clustered just below the tender threshold, single-bidder patterns by supplier, price drift against market indices, and the "split purchase" signature (one requirement, many small awards). The craft is the same three-layer stack as fraud: rules that catch the blunt patterns (explainable, auditable, publishable), a model for the residue, and a *human investigation* layer — because in the public sector, a flagged case that survives review must be presentable to an audit committee, and explainability is the law of the genre. Chapter 53's decline-letter discipline transposes: every flag carries its reasons, in language a non-technical councillor can repeat.

## 57.6 Open Data and Privacy as Engineering

Publication is the public sector's default and its hardest engineering problem: aggregate enough to protect (Chapter 54's small-cell suppression), document enough to verify (methodology, extract dates, known gaps), and version enough to trust (yesterday's number must still be reconstructable when the auditor asks — Chapter 42 again). The rare-data floor: administrative data on citizens carries the same harm test as health data (Chapter 54), and Chapter 68's formal techniques are the far end of the same road. The practitioner's rule: **publish the aggregate, protect the row, and write down which is which.**

## 57.7 Failure Modes

- **Goodhart at national scale** — collections-per-ward targets met by redefining "scheduled"; every indicator needs its companion audit metric (Chapter 45's pairing, now with an audit committee in the room).
- **Evaluation as advocacy** — the programme evaluation written to survive a cabinet meeting rather than an audit; pre-registration and published nulls are the antidotes.
- **The dashboard nobody uses** — the beautiful expenditure dashboard the councillors never open, because it answers no question anyone holds; Chapter 19's audience discipline is civic, not corporate.
- **The extract that becomes the record** — a one-off data pull, exported and quoted, drifting from the live system; version and date everything.

> **Teaching Tip — The adversarial reading:** have students publish (in class) a one-page service baseline, then assign a third of the room to attack it as the opposition councillor: What is hidden? What is redefined? What would you FOA-request? The defending team learns more about methodology documentation in twenty minutes of adversarial reading than in a week of lectures — and it is exactly the muscle the job requires.

## Key Takeaways

- Public analytics has many masters and permanent scrutiny: show the work — lineage, methodology, extractable data — because the audience includes adversaries by design.
- The first project is one honest, published service baseline; trust is the deliverable as much as the number.
- Evaluation culture: pre-register, check the parallel-trends assumption, publish the nulls, and bound every estimate.
- Procurement anomaly analytics is civic work: explainable flags, auditable reasons, presentable cases.
- Publish the aggregate, protect the row, and write down which is which.

## Practice Lab

1. Build the refuse-collection service baseline from the fleet GPS and ward schedules (Appendix F generator); publish the methodology page and the reconciliation table, then run the adversarial reading exercise on a classmate's baseline.
2. DiD practice: evaluate the street-lighting expansion on ward-level incident data; display the parallel-trends check honestly and write the finding — including the null if that is what the data says.
3. Queueing at the licensing office: given arrival and service logs, compute the stage-level delays and the Wq arithmetic for two staffing options; write the memo with the p90 wait, not the mean.
4. Procurement anomalies: run the threshold-clustering and split-purchase rules on three years of awards; produce three flags with written reasons, each presentable to a non-technical committee.
5. The open-data release: take a service register and produce the publishable aggregate — suppression applied, methodology written, version dated — plus the internal note on what was withheld and why.
6. The indicator redesign: pick one current civic target, describe its Goodhart failure mode, and propose the paired metric that closes it.

## Further Reading

- *Public Sector Analytics* literature: the What Works centres (the UK's movement is the reference model)
- Chapter 61 (causal inference), Chapter 42 (lineage), Chapter 46 (anomaly detection), Chapter 68 (formal privacy)
- Appendix J Case 4 (the tariff evaluation) — this playbook's deepest worked case
