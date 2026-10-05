# Chapter 47: Project 5 — The Survey

*Part VII — Real Projects and Your Portfolio*

> "Chapter 27 taught the mechanics. A project is when the mechanics meet real humans — including you."

### In this chapter you will learn

- Running a real survey end-to-end: design, field, clean, analyse, report.
- Analysing survey data honestly: the n that arrives vs the n you dreamed of.
- The say/do gap: connecting survey answers to till behaviour.
- The report: findings, limitations stated loudly, the decision it feeds.
- Portfolio evidence #5, and the ethics review that comes with human data.

## 47.1 Design and Field

The brief, written before anything else (the anatomy's law): *Tariro needs to know whether a Sunday double-points promotion would bring shoppers in — and who would come. Decision: run the promotion or not. Audience: Tariro. Success: an estimate of Sunday intent by customer segment, with its margin of error, in two weeks.*

The design inherits Chapter 27's rules, now under project pressure. The instrument: seven questions, one per card — visit frequency ("How often do you shop with us?" — labelled bands, never "how many times per month on average", which humans answer badly); Sunday intent (the 5-point definitely/probably/unsure/probably-not/definitely-not scale); what would change the answer (multi-choice: nothing, double points, a hot-food counter, later hours); payment preference; suburb (to join to till data!); membership; and one open text ("anything you'd want us to stock?") — because one open question humanises the dataset and occasionally delivers a product idea in the customer's own words. The frame, stated and written down: shoppers in the shop, two Saturdays and two weekdays, every third customer approached (a system, not a vibe — convenience-with-rules, its limitation declared). The target n: 150 (the Chapter 25 arithmetic: ±8 points on a proportion — adequate for a run/don't-run decision, stated in the report).

Fielding reality, which is the education: refusals happen (~30% — logged, because refusal rate is itself a bias finding: who refuses? hurried weekday lunchers, mostly); the question that confuses ("double points *of what*?" — re-read the scale's wording, fix in the field, note the fix); and the response distribution that surprises (weekday respondents are *more* Sunday-interested than Saturday respondents — a selection story before the analysis even begins). Field notes are data: the log carries them.

## 47.2 Clean and Analyse

Responses arrive — 168 of them, because fielding overshot (good). The cleaning liturgy, survey edition: one row per response (no duplicate timestamps); the labelled scale kept as *categories* (1–5 with value labels, never averaged into a "2.7 attitude" — Chapter 27's rule, now load-bearing); the multi-choice parsed into separate yes/no columns; the open text read *by a human* (you) and thematically coded (three categories emerged: hot food, bulk staples, baby items — each becomes a countable column). Every cleaning decision logged, as always.

The analysis, in the order the anatomy prescribes:

1. **Describe**: the intent distribution (definitely 17%, probably 24%, unsure 21%, probably-not 23%, definitely-not 15%) — shown as counts *beside* percentages, n declared on every table.
2. **Segment**: the cross-tabs — intent by tier (members: 51% definite/probable vs non-members 33%), by suburb, by usual payment. Chi-square on each, expected-counts check, effect sizes read from the row percentages, not the p-values (Chapter 27's full method, now fluent).
3. **Margin of honesty**: every headline percentage carries its interval — 41% ± 7.5% for the pooled definite/probably share; the segment splits are wider (n = 61 members: ±12%), and the report says which comparisons the data can and cannot support.
4. **The weighting question, considered and answered**: weekday/Saturday balance is off (by fielding design); rather than statistically reweighting (defensible but fragile at this n), the report presents both field-days separately and lets the reader see the selection — transparency over sophistication, at this sample size, is the right professional call (stated as such).

## 47.3 The Say/Do Join

The project's signature move — the one that lifts it above a classroom exercise — is joining what people *said* to what people *do*: respondents' suburbs and tiers (collected precisely for this) are joined to their till-history segments from Project 4's frame. The finding that matters: among respondents who *said* "definitely would" shop Sundays, the ones who are *already* Sunday shoppers (in till data) are 2.3× more frequent than the ones who are not. Read carefully: stated intent is strongest exactly where behaviour already agrees — the survey is partly *measuring enthusiasm*, not forecasting change. That is the say/do gap, quantified on your own two datasets, and it converts the recommendation from "run it, 41% are interested!" to the honest form: *"interest is real but concentrated among existing Sunday shoppers; the promotion's incremental pull is likely nearer 15–20% than 41%; the four-Sunday trial with till-based measurement (baseline already in the dashboard) is the decisive, cheap test."* A survey that checks itself against behaviour is worth two surveys that don't.

## 47.4 The Report

`survey-report/` ships with: the instrument (questions + field protocol, so a successor could re-run it); the cleaned data; the analysis notebook; the four-exhibit findings (intent distribution; intent × tier; say/do table; the limitations box); and the one-page decision memo. The limitations box, loud and early rather than buried: convenience frame (in-shoppers only — the Sunday-stayers-at-home are the population the promotion targets and the survey *cannot see them*); n and margins by segment; self-report bias (measured, 47.3); no causal claims (intent is association with behaviour). Then the recommendation with its decision logic: run the four-Sunday trial if the cost of the trial is under the expected value of a 15–20% Sunday lift; measure in till data; kill or scale at the pre-agreed threshold (Chapter 26's pre-registered α, applied to a business test).

The 150-word note, written on shipping day: *Situation: promotion decision for a grocery, two weeks, 168 in-shop respondents. Work: designed and fielded the survey; cleaned and cross-tabbed; joined stated intent to till behaviour. Finding: 41% ± 7.5% expressed Sunday intent, but intent concentrates among existing Sunday shoppers — incremental pull nearer 15–20%. Impact: decision reframed from launch to a measured four-Sunday trial. Limits: convenience frame, self-report, survey-on-generated-data labelled.* — and note the last clause: this project runs on the book's synthetic till data plus *real human responses only if you truly fielded it*; either way the labelling is explicit (Chapter 44's rule, and Chapter 59's ethics preview).

## 47.5 The Ethics Review

Human data carries obligations, and this project is where the book makes them concrete: **consent** — respondents approached as such, told the purpose, free to refuse (the 30% refusals are the system working); **anonymity by design** — no names collected, only the join-columns (suburb, tier) the analysis needs, the minimum-data principle; **purpose limitation** — the data answers the Sunday question and nothing else; no repurposing into a "marketing list" beyond the consent given; **honest reporting** — the limitations box *is* an ethical artefact, not just a statistical one. At work, the formal versions arrive as review boards, data-protection law (GDPR-style regimes, POPIA, Zimbabwe's Cyber and Data Protection Act), and company policy; the professional habit starts here: *when humans are the data, the checklist grows a conscience section.* Chapter 59 builds the full map.

> **From Your Toolkit — asking, everywhere:** surveys are the only instrument that reaches the futures inside people's heads — intentions, satisfactions, reasons — and every analytics team eventually runs one (product NPS, employee pulse, customer exit). The craft constants: frame declared, scales labelled and kept categorical, counts beside rates, intervals attached, behaviour joined where possible, limitations loud. SPSS ran this project's cross-tabs; pandas or Stata could have — the *method* is the asset.

## Key Takeaways

- Design under project pressure: one question per card, labelled scales, frame and refusal rate logged, target n from the margin arithmetic — and field notes are data.
- Clean survey-style: categories stay categories; multi-choice splits to columns; open text human-coded; every step logged.
- Report counts beside percentages, χ² with effect sizes, intervals on every headline — and prefer transparency to fragile reweighting at small n.
- The say/do join is the signature: intent measured against behaviour reframes the recommendation (41% interest → 15–20% incremental) — surveys that check themselves are worth two that don't.
- Ethics is a checklist section: consent, minimum data, purpose limitation, honest limitations — the conscience the human-data projects require.

## Practice Lab

1. Field it for real (recommended): the instrument on friends, family, a class, a workplace — 30+ responses minimum; run the full pipeline and note where reality diverged from this chapter's fielding (it will; that divergence is the education).
2. Or simulate honestly: Appendix C's survey generator (labelled synthetic); run the identical pipeline; write the one-paragraph memo on what a simulated survey *cannot* teach (refusals, confusion, the field's surprises) — the meta-finding.
3. The say/do join, built: respondent segments × till behaviour; the 2.3× table with its counts and its chi-square; write the three sentences a decision-maker reads.
4. The limitations box, drafted twice: once where this chapter puts it (early, loud) and once where most reports put it (buried); hand both versions to a friend and ask which report they would trust more — then keep the loud version forever.
5. Portfolio evidence #5: the folder, the exhibits, the note, the STAR paragraph ("a time you changed a recommendation with better analysis"); the ledger now reads five — one project remains.

## Further Reading

- Chapter 48 (the operations dashboard — the trial's measurement instrument), Chapter 59 (ethics, the full map)
- *Asking Questions* (Bradburn et al.) — the survey craft bible, at project scale
