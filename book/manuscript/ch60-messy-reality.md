# Chapter 60: Messy Reality — Missing Data, Biased Samples, Deadlines

*Part IX — Beyond the Basics*

> "The book's data was planted so every method could find its answer. This chapter is about everything that happens when nobody planted anything."

### In this chapter you will learn

- Missing data, properly: the three mechanisms, and what to do for each.
- Working under deadline: the 80/20 delivery that survives scrutiny.
- The stakeholder realities: changing questions, missing owners, politics.
- The audit of reality: a checklist for the messy-project archaeology.
- How to keep learning from projects that go wrong.

## 60.1 Missing Data, Properly

Chapter 8 dropped rows and logged it; Chapter 15 counted NULLs; Part IV said "the missing are rarely missing at random" — now the full theory, compressed to what analysts need. The three mechanisms (Rubin's taxonomy, demystified):

- **MCAR** (missing completely at random) — the reason is pure chance (a till crashed Tuesday afternoon). Rare, and the least harmful: complete-case analysis (drop the missing) is *unbiased*, just smaller. What you did all book, and now you know when it is safe.
- **MAR** (missing at random — misleading name: missing *given* other data) — the reason is visible in your other columns: EcoCash sales missing more on Sundays; survey income missing more among older respondents. The common case; the honest tools: model the missingness (imputation by regression on the observed columns — "fill each gap with what similar rows show"), or better, *weight or stratify* by what predicts missingness. Dropping rows now *biases* the result (you systematically lose Sunday-EcoCash), and the bias is silent.
- **MNAR** (missing not at random) — the reason is the value itself: the biggest baskets unrecorded (voided to hide theft); dissatisfied customers never answering. The dangerous case: no statistical trick fully fixes it, because the data cannot tell you what it never saw. The honest responses: bound the damage (sensitivity analysis — "if missing sales average 1× the mean, revenue is X; if 2×, it's Y"), find a second source to triangulate, and *state the direction of the bias in the report* ("our estimate is conservative; theft-voided baskets are systematically large").

The working liturgy for any NULL-heavy column: **mechanism first, decision second** — chart the missingness (missing by day? by segment? by value of neighbours?) against every column that might explain it; classify MCAR/MAR/MNAR with your reasons written; then choose (drop / impute+flag / bound+declare). The imputation craft notes: impute with a *flag column* (`was_imputed`) so downstream honesty survives; prefer simple (median by segment) over clever (fancy models imputing fiction) unless the imputation itself is validated; and never, ever let imputed values silently become "real" in a report — the fence around them is a sentence in every finding: "12% of this column was imputed; the estimate without imputation is also shown."

## 60.2 The Deadline 80/20

The real project ships Friday, and the data arrived Thursday with 4,000 rows missing in the middle. The craft of delivery under constraint — the triage order that preserves both the deadline and the integrity:

1. **Scope to the question that matters**: not "the full analysis" but the decision this meeting makes; cut every branch that does not feed it (Chapter 13's kindness, weaponised against time).
2. **The honest core first**: the number the decision needs, computed on the *clean* subset — declared ("first 6 months only; the rest arrives verified Monday"). A verified partial beats an unverified whole.
3. **The checks that survive compression**: three survive every deadline — the bridge total, the missingness statement, and the known-flaw line. Twenty-minute checks that have saved careers; never traded away.
4. **The staged delivery**: the honest core Friday; the completed analysis Monday; the deep questions next cycle. Stakeholders *accept* staged truth remarkably well when offered it proactively and dated — what they never forgive is the confident Friday number that quietly changes.

The rule underneath: **under deadline, you cut scope, never rigor** — scope is negotiable (with the stakeholder, out loud), rigor is not (with reality, silently). The analyst who ships the small-true thing on Friday and the whole-true thing on Monday has a career; the one who ships the big-maybe thing has an incident.

## 60.3 The Stakeholder Realities

The human weather systems of real projects, with the working responses:

- **The question that changes mid-flight** ("actually, can we look at it by region?") — respond with scope arithmetic: "yes — that's a new cut; it adds two days, or replaces the price analysis; which would you prefer?" The question-changer is not the enemy; the *undisclosed* change in cost is. Make costs visible and you can absorb any number of new questions.
- **The missing owner** — the decision-maker who commissioned the analysis and then vanished; the finding lands in a meeting where nobody has authority to act. Response: name the decision in the first email ("this supports the pricing call — who owns it?"), and deliver to the decision, not the request.
- **The politically inconvenient finding** — your analysis is correct and unwelcome (the flagship product's numbers are bad; the director's project harmed revenue). The craft: the *finding* is delivered exactly as a welcome one would be — same rigour, same caveats, same channel — because the moment you soften it, you own the softening forever. The *framing* can serve the reader ("three options the data supports") without bending the data. And Chapter 59's refusal line applies when "reframe" means "reverse".
- **The repeat ad-hoc** — the same "quick question" weekly, from the same stakeholder, about the same data. This is not a workload problem; it is Chapter 37's pipeline problem wearing a person — and solving it (the tile, the saved query, the scheduled mail) is precisely the kind of quick win that builds a first-90-days reputation (Ch. 54).

## 60.4 The Reality Checklist

The messy-project audit — run it on any inherited or half-alive project, in place of the despair that usually accompanies both:

1. **What question was this trying to answer?** (Reconstruct from artefacts; if nobody can say, that is the first finding — and usually the reason the project died.)
2. **What data exists, what's missing, and which mechanism?** (60.1's liturgy, run as archaeology.)
3. **What checks were run — and what do they say now?** (Re-run the bridges; a stale reconciliation is the fastest autopsy.)
4. **What is actually finished?** (Notebooks that Restart-And-Run-All; queries with headers; reports with dates — the Ch. 45 anatomy, applied as triage.)
5. **What is the smallest honest deliverable?** (80/20: cut to a question someone owns, ship the verified core, stage the rest — resuscitation, not heroics.)

## 60.5 Learning From the Ones That Go Wrong

The failed projects are tuition paid — collect the learning: a **post-mortem in three paragraphs** (what happened, honestly; what I'd check earlier; what I'd say no to), filed in the same ledger as the successes, because Chapter 52's interviewers ask about failure deliberately and "tell me about a project that went wrong" is answered *best* by someone with a written archive of the answer ("the data arrived 40% missing at MNAR — I bounded it, delivered the honest core, and learned to ask about data completeness *before* accepting the timeline; here's what I ask now"). The careers that compound (Ch. 56) are built exactly this way — not on unbroken success, which does not exist, but on failures that were *processed*: what this book has done in miniature with every lab and every log, now as a lifelong habit.

> **From Your Toolkit — reality is the final tool:** the whole book has been rehearsal in a controlled world; this chapter is the patch notes for the uncontrolled one. Every item here is still the same instruments — the liturgy, the bridge, the caveat, the anatomy, the staged truth — played at speed, under fire, with humans in the room. The mess does not change the method; it is why the method exists.

## Key Takeaways

- Missingness: classify MCAR/MAR/MNAR with reasons written; drop only MCAR; impute with flags and simple models; bound MNAR and declare the direction of bias — never let imputed become silently real.
- Deadline craft: scope to the deciding question, ship the verified core with its three survival checks, stage the rest with dates — cut scope, never rigor.
- Stakeholder weather: make change-costs visible, deliver to the named decision, deliver inconvenient findings with unchanged rigour, and treat repeat ad-hocs as pipeline problems.
- The reality checklist: question, data state, checks re-run, finished-vs-dead triage, smallest honest deliverable.
- Post-mortem in three paragraphs, filed — processed failure is the raw material of compounding.

## Practice Lab

1. The missingness liturgy, run for real: on a dataset with genuine gaps (your stock table's missing weeks, or a public dataset's holes), chart missingness by every plausible predictor; classify the mechanism with reasons; apply the matching response; write the report sentence that discloses it.
2. The imputation clinic: impute the gaps two ways (median-by-segment; regression) with `was_imputed` flags; compare downstream findings across: original-dropped, imputed-A, imputed-B — three numbers, honestly different; write the disclosure line you would ship.
3. The Friday drill: simulate the deadline — a stakeholder question, a dataset with a hole, four hours on a clock; deliver the staged package (Friday core + Monday plan); note where the deadline pressure tried to eat a check, and that you refused.
4. The archaeology: find a dead project (yours, or a public abandoned notebook); run the reality checklist; write its three-paragraph post-mortem even though — especially because — it is uncomfortable.
5. The script library: from this chapter, write your four standing sentences (scope arithmetic, decision-naming, finding-delivery, no-with-alternative); rehearse them aloud once; they are now as portable as your SQL.

## Further Reading

- Chapter 61 (the free stack — practising all of this for $0), Chapter 62 (the decade view)
- *Missing Data* (Allison) — the little orange book; everything an analyst needs in 90 pages
