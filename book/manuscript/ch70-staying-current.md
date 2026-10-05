# Chapter 70: Staying Current — A Reading Discipline and Ten Predictions

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "The tools will churn; the grammar will not; your job is to know which one a new thing is."

### In this chapter you will learn

- The reading discipline: a weekly rhythm that survives a full-time job.
- The triage question: grammar or fashion — and the test that tells them apart.
- Learning by replication: the one-paper-per-week frontier habit.
- Communities, teaching, and the compounding of being slightly early.
- Ten predictions to track — the book's wager on the next five years.
- Failure modes: tool collector syndrome and the frozen practitioner.

## 70.1 The Churn Is the Job

The half-life of a specific tool is short; the half-life of the discipline is long. You trained on SPSS; the industry moved to Python; Python's libraries reshuffle yearly; and underneath it all, the join, the hypothesis test, the baseline, and the memo have not moved in decades. Staying current is therefore not tool-chasing — it is a **triage discipline**: separating the rare changes to the grammar from the constant churn of fashion, and spending your scarce learning hours accordingly.

## 70.2 The Reading Rhythm

A rhythm that survives a full-time job (Chapter 45's habit, made specific):

- **Weekly (90 minutes)** — two newsletters you trust (one technical, one industry), skimmed with the triage question; one paper or post *read*, not skimmed.
- **Monthly (half a day)** — the release notes of your core stack, actually read; one tutorial *run*, not watched.
- **Quarterly (a weekend)** — one replication: pick a paper or a new method, rebuild its smallest claim on data you know; the frontier discipline of Part XI's teaching guide.
- **Annually** — the audit: what did you learn this year that changed how you work? (Not "what did you skim?") If the list is empty, the rhythm has become theatre.

The subscriptions matter less than the **decisions they trigger**: every reading session ends with one line — *act, watch, or drop*. "Watch" items go on a list with a review date; the list is pruned quarterly without mercy.

## 70.3 The Triage Question

When a new thing announces itself, ask: **what part of the grammar does it change?**

- It changes the grammar if it changes *how questions are answered*: the transition from file-based data to query engines (DuckDB), from hand-built features to learned representations, from point estimates to causal or distributional thinking. These are rare — a few per decade — and worth a deep investment.
- It is fashion if it changes *who or where, but not what*: a new BI tool with the same chart grammar, a new AutoML wrapper around the same models, a new notebook skin. These are learned in a week when needed, never before.

The test that separates them: **can you name a question you could not answer well last year that this answers better?** If yes, replicate the answer on data you know — grammar candidate confirmed or killed in a weekend. If no, file under watch and move on.

**From Your Toolkit — all six tools:** this is where the six-tool grammar pays its final dividend. SQL, Excel, Python, Power BI, Stata, SPSS — every new tool you will ever meet implements some subset of that grammar, and your fluency in the grammar is what makes a week of learning sufficient. The practitioner who learned *dashboards* can adopt any BI tool; the practitioner who learned *one BI tool* must start over every time.

## 70.4 Communities and Teaching

You cannot read your way to the frontier alone; the frontier is a conversation. The disciplines: one community you *belong* to (a local meet-up, a professional group, an open-source project), one you *contribute* to (answers, review notes, a small library), and the teaching habit of Chapter 50 — because explaining this year's grammar to someone else is the only reliable test that you learned it. Being slightly early — one replication ahead of your market's demand — compounds quietly: Chapter 80's value ledger has a line for it.

## 70.5 Ten Predictions

The book's wager — scored annually, in public, as your model of how to hold opinions:

1. **SQL returns as the analytical lingua franca** — engines like DuckDB make "just query the files" the default; the notebook generation learns window functions.
2. **Causal inference becomes a default expectation** — "what would have happened anyway?" moves from the frontier chapter to the standard business question, as experimentation culture spreads.
3. **LLMs become the analyst's pair, not the analyst** — draft memos, first-pass code, synthesis of documentation; the judgement layer (this book) stays human.
4. **The analytics engineer role consolidates** — the layer cake of Chapter 69 becomes a standard organisational function with its own ladder.
5. **Small models hold the middle** — fine-tuned small models (Chapter 65's discipline) beat frontier models on cost, latency, and sovereignty for most production tasks.
6. **Differential privacy gets regulated into deployment** — a privacy budget becomes a compliance artefact, as Chapter 68's accountants ship in mainstream platforms.
7. **Synthetic data grows up** — from demo trick to governed technique, with formal guarantees and honest limits pages.
8. **Local-first analytics persists** — constrained environments (Chapter 77's offline-first world) drive tooling that treats connectivity as a bonus, not a requirement.
9. **Geospatial goes default** — every warehouse grows geometry types, as Chapter 62's missing feature becomes a column everyone has.
10. **The craft premium widens** — as generation gets cheap, the practitioners who price and deliver *judgement* (Part XII) command the premium; the ones who price tool operation do not.

Scorecard discipline: each prediction gets a verdict every year — *hit, miss, or too early* — and the misses are the interesting ones. Predictions are how you force yourself to have falsifiable opinions.

## 70.6 Failure Modes

- **Tool collector syndrome** — twenty "watch" projects, no replications; the GitHub stars as a substitute for the grammar.
- **The frozen practitioner** — the opposite failure: the stack of five years ago, defended with increasing energy; the triage question asked of nothing, ever.
- **The skimming treadmill** — 100% newsletter coverage, 0% decisions triggered; the rhythm's one-line rule exists to kill this.
- **Prediction without a scorecard** — opinions held publicly but never scored; hold them like Chapter 61 holds estimates, with the range and the reversal condition.

> **Teaching Tip — The tool autopsy:** assign each student a dead tool (or a dying one) — a BI platform, a library, an entire paradigm — and have them present: what grammar did it change, what did it get right, why did it die, and what absorbed its ideas? Nothing teaches triage faster than an autopsy, and nothing inoculates against fashion harder than watching a "revolutionary" become a footnote that still influences everything.

## Key Takeaways

- Staying current is triage: grammar changes get deep investment, fashion gets a week when needed — and the grammar you already own makes that possible.
- The rhythm: weekly reads with a decision, monthly runs, quarterly replications, annual audit.
- The test: name the question this answers better, then replicate it on data you know.
- Communities and teaching compound; being one replication early is a career asset.
- Ten predictions, scored annually in public — falsifiable opinions, held honestly.

## Practice Lab

1. Build your reading system: choose the two newsletters, the paper cadence, and the watch-list with review dates; run it for a month and write the audit of what changed.
2. Run the triage test on the last three tools you heard about: for each, the question it answers better, the grammar-or-fashion verdict, and the act/watch/drop decision.
3. One replication: pick a paper from this part (CUPED, MinT, Croston, or a Masakhane model), rebuild its smallest claim on Appendix F data, and write the two-page replication note.
4. Join and contribute: one community joined, one contribution made (an answer, a review, a fix); write the paragraph on what teaching taught you.
5. Score the ten predictions for this year: hit, miss, or too early — with one sentence of evidence each; then write your own prediction to add to next year's card.
6. The tool autopsy: research one dead analytics tool and present its grammar legacy in five slides; name which of its ideas you use weekly without knowing their origin.

## Further Reading

- Your two newsletters — chosen, triaged, and actually read
- Papers With Code (the replication habit's home)
- Chapter 50 (teaching as the test), Chapter 45 (the career habit), Chapter 80 (where being early gets priced)
