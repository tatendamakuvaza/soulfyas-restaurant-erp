# Chapter 75: Documentation That Outlives You

*Part XII — The Practitioner's Path: Projects, Clients and the Craft of Delivery*

> "The analysis you cannot reconstruct is a rumour you happened to compute."

### In this chapter you will learn

- The four artefacts: the README, the analysis log, the methodology note, the handover memo.
- The analysis log: a dated record of decisions and dead ends, kept as you work.
- Reproducibility as habit: seeds, environments, and data snapshots.
- Where documentation lives, and why "in the same repo" is the whole answer.
- The doc-debt audit, run quarterly.
- Failure modes: the tribal-knowledge project and the retrospective novel.

## 75.1 Four Artefacts

Every engagement produces four documents, and three of them are written *during* the work, not after:

- **The README** — the project's front door: the question, the decision it served, the data sources, how to run the code, and where everything else lives. Two minutes to read; the test is that a stranger can start work from it.
- **The analysis log** — the dated, running record: what was tried, what was decided, what died and why. The part's signature artefact; Section 75.2.
- **The methodology note** — the how-it-was-done: definitions, assumptions, the sensitivity table (Chapter 61), the limitations stated without shame. The document Chapter 76's audit reads first.
- **The handover memo** — the end-of-engagement document: what was delivered, what was not, what to watch (the measurement plan), who owns it now, and the three things the next practitioner should know.

## 75.2 The Analysis Log

The discipline that separates the practitioners from the tourists. The log is a plain file (markdown, one per project), appended as work happens, in four kinds of entry:

```text
2026-03-04  Chose 30-day churn window (not 60). Reason: retention team
           calls at day 21; the window must match the intervention.
2026-03-06  DEAD END: outlet-level features in the member model. Leakage
           suspicion correct? No - dropped for grain mismatch, not leakage.
2026-03-09  Review 1: sponsor flagged price-sensitivity question. Added
           elasticity bound (ch61 method) to plan; memo updated.
2026-03-11  Data issue: 2022 gap is 78% missing, MAR on plot size.
           Strategy: MI + IPW bound (case 5 pattern). Logged for note.
```

The log's value is exactly the entries that feel wasteful: **the dead ends**. Six months later, the dead end re-suggested by a colleague costs a week to re-die — unless the log says it already died, with its reason. The log is also Chapter 71's drift detector made continuous, and the raw material the methodology note is distilled from. Write it at the end of the day, every day; five minutes buys the project's memory.

## 75.3 Reproducibility as Habit

- **Seed everything** — every script that samples, splits, or initialises takes an explicit seed, recorded in the log; "the numbers moved slightly" is a bug report, not a mystery.
- **Environment as file** — `requirements.txt`, pinned; the environment is part of the artefact, versioned beside the code.
- **Data snapshot as data card** — the extract date, source, row counts, and checksums; Chapter 42's lineage, made physical. The analysis reproduces against *the data it analysed*, with today's data as a documented refresh.
- **One command to rerun** — the README's promise: `make all` (or its equivalent) rebuilds every table, figure, and number in the memo. If it cannot, the memo is a claim, not an artefact.

**From Your Toolkit — SQL:** commented queries *are* documentation when they live in the repo — the craft habit is writing the query as its own methodology note (grain stated at the top, assumptions inline, the why beside the what). The uncommented 200-line query is the tribal-knowledge project in miniature.

## 75.4 Where It Lives

One answer: **in the repository, beside the code, versioned with the work.** Not in a documents drive, not in email, not in the wiki that the last person who updated it left in 2023. The README points to everything; the log and the note travel with the analysis they describe; the handover memo is the last commit's companion. The "where does documentation live?" question is answered by the same discipline that answers "where does code live?" — and the answer's power is that search, diff, and blame then work on the documentation too.

## 75.5 The Doc-Debt Audit

Quarterly, one hour, per project: the four artefacts exist and pass their tests?

| Artefact | Test | Fail = debt item |
|---|---|---|
| README | Stranger starts work in ten minutes | Rewrite front door |
| Analysis log | Last week's decisions findable | Backfill from memory (costly, do now) |
| Methodology note | A peer could defend it to an auditor | Distill from log |
| Handover | Owner named, watch-items dated | Write before the exit, not after |

The audit's rule: debt items get owners and dates — undocumented is a state with a repair plan, not a permanent condition.

## 75.6 Failure Modes

- **The tribal-knowledge project** — everything worked and only the departed analyst knows why; the four artefacts are the vaccine, and the audit is the booster.
- **The retrospective novel** — documentation written in a heroic weekend *after* the work: no dead ends (forgotten), no real reasons (reconstructed), no trust. Three of the four artefacts exist because they are written *during*.
- **Documentation as monument** — the 60-page methodology note nobody reads; the note is distilled, the log is complete, and confusing the two wastes both.
- **The moving target** — numbers quoted in the memo that the pipeline no longer produces; the snapshot card and the one-command rerun keep memo and pipeline married.

> **Teaching Tip — The two-years-later test:** hand students a project bundle (code, data card, and either a real log or a fabricated gap) and give them one question to answer from it ("why did we drop the outlet features?"). The bundle with the log answers in thirty seconds; the bundle without burns the hour — and the hour *is* the lesson: documentation is time travel, and the person you are doing the favour for is you.

## Key Takeaways

- Four artefacts, three written during: README (front door), log (memory), methodology note (defence), handover (continuity).
- The analysis log's value is its dead ends — five minutes a day buys the project's memory and the note's raw material.
- Reproducibility is habit: seeds, pinned environments, snapshot cards, and one command to rerun everything.
- Documentation lives in the repo, versioned with the work — search, diff, and blame for prose too.
- Audit the debt quarterly: each artefact with its test, each failure with an owner and a date.

## Practice Lab

1. Start an analysis log for your current project; write today's entry including one dead end you have already forgotten the reason for (reconstruct it, and note the cost of the reconstruction).
2. Write the README for a project you have finished: front door test — hand it to a classmate and watch where they stall.
3. The reproducibility pass: pin the environment, seed every random step, snapshot the data card, and get to one command; document the gap you cannot close and why.
4. Distill a methodology note from an analysis log (yours or Appendix F's planted log): definitions, assumptions, the sensitivity table, limitations without shame.
5. Run the doc-debt audit on two projects; produce the debt list with owners and dates.
6. The handover memo for Case 5's evaluation: what was delivered, what to watch, who owns it, and the three things the next evaluator must know.

## Further Reading

- *The Art of Doing Science and Engineering* — Hamming (the log-keeping habit's pedigree)
- Reproducible research literature (the "one command" tradition)
- Chapter 71 (the plan the log audits), Chapter 42 (lineage), Chapter 76 (the audit that reads your note)
