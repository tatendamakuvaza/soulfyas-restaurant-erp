# Chapter 45: The Anatomy of an Analysis

*Part VII — Real Projects and Your Portfolio*

> "Every good analysis you will ever do is the same five moves. The projects change; the moves do not."

### In this chapter you will learn

- The five-move anatomy: question → data → clean → analyse → communicate.
- The checklist that runs underneath each move — this book, condensed to one page.
- Time budgeting: the 80/20 of real projects, and where projects die.
- The case-study method: writing 150-word notes that get interviews.
- How Projects 1–6 map onto the anatomy — and what your own projects must add.

## 45.1 The Five Moves

Strip away the tools and the domains, and every analysis that ever changed a decision has the same skeleton:

```text
1. QUESTION     -- a decision or curiosity, stated, with its audience named
2. DATA         -- sourced, licensed, understood (the first hour, Ch. 44)
3. CLEAN        -- the liturgy: types, dupes, orphans, NULLs, the bridge
4. ANALYSE      -- describe, compare, test; effect sizes with intervals
5. COMMUNICATE  -- headline, findings with caveats, recommendations, artefacts
```

You have lived these moves nine times now (six Part-projects plus the Part IV and VI deliverables), always in this order, and the order is the anatomy's first law: **a question written before data is touched, and a communication designed before the analysis is finished.** Beginners run data → analysis → (maybe) a question that fits; the professional runs question-first and designs the deliverable *backwards from the reader* (Chapter 13's planning trick — which is this law, applied). The second law: **the moves iterate but never skip** — you will loop question→data when the data cannot answer the question (that is a *finding*: "unanswerable with current data"), but you never jump to 4 without 3, and you never start 5 without something worth saying.

## 45.2 The Checklist

This book, compressed to the page working analysts keep pinned (mentally) above every project — each line is a chapter, and the parentheses give you the trail back:

**QUESTION** ▢ One sentence, with a decision in it ▢ Audience named (who reads this?) ▢ Success state defined (what answer ends the project?) ▢ Scope fenced (18 months, one shop, this segment) (Ch. 2, 13)

**DATA** ▢ Licence checked, source cited ▢ Documentation read; collection method noted — its biases asked (Ch. 44) ▢ First hour run: instruments, reconciliation, plotted columns ▢ Questions log opened (Ch. 33, 44)

**CLEAN** ▢ Types verified; dates parsed ▢ Duplicates counted and resolved ▢ Orphans found and documented ▢ NULL census with meanings ▢ Bridge total reconciled against a second source ▢ Log of every cleaning decision (Ch. 8, 14, 21, 33)

**ANALYSE** ▢ Described before tested (five numbers, shapes) ▢ Compared against a baseline ▢ Tested where testing is owed — right test, assumptions checked, α pre-chosen ▢ Effect size + interval with every p-value ▢ Correlations read through the three explanations (Ch. 22–28, 36)

**COMMUNICATE** ▢ Headline that survives alone ▢ Findings with caveats attached ▢ Recommendations measurable, with owners ▢ Right format: report vs dashboard vs walkthrough, decided (Ch. 13, 43) ▢ Artefacts filed, named, versioned, with the log (Ch. 20, 37)

**THE THREE RULES, EVERYWHERE** ▢ average ≠ the answer ▢ correlation ≠ causation ▢ sample ≠ population

Print this page. It is the book's entire argument, operationalised — and it is the review checklist for every project remaining, including your own.

## 45.3 Time: the 80/20 of Real Projects

The time distribution nobody believes until their first job: **question and cleaning consume the majority of every real project; the glamorous analysis is the minority; communication is under-estimated by everyone.** A working budget for a two-week stake: framing and data 30%, cleaning and checking 30%, analysis 20%, communication 20% — and when something goes wrong (it will), the overruns eat analysis time, *never* cleaning or communication time. The corollary discipline: the cleaning 30% is where shortcuts poison everything downstream; the communication 20% is where good analyses go to die unnoticed. Projects fail at the edges, not the middle.

Where projects die, the three morgue drawers: **the unowned question** (no decision attached — the analysis wanders until abandoned); **the data that cannot answer it** (discovered at move 4 instead of move 2 — the first hour exists to kill this early); and **the unfinished tell** (analysis done, communication deferred, nothing shipped — the "portfolio" of dead notebooks). Each drawer has a door: a written question, a first hour, a delivery date.

## 45.4 The Case-Study Method

The portfolio's atomic unit is not the project — it is the **150-word case-study note**, and its anatomy is the project's anatomy, compressed to five sentences (you have written three already, in the Part projects; here is the method, deliberate):

```text
[SITUATION] One line: who, what data, why it mattered.
[WORK]      One-two lines: the moves, with tools named.
[FINDING]   One line: the number and its verdict -- the headline
            that survives alone.
[IMPACT]    One line: the decision or the improvement, timed or
            measured ("an afternoon became twenty minutes").
[LIMITS]    One line: the honest caveat (sample, association,
            synthetic labelling).
```

Why 150 words: recruiters skim (Chapter 51 gives the eye-tracking reality); interviewers *lift* these notes as their questions ("tell me about the 31% growth finding" — and you are in your STAR story, Chapter 53, on ground you prepared). Write the note the day the project ships, while the numbers are vivid; a note written a month later is a different, worse artefact. And file the note with the artefacts it points to (repo, dashboard, PDF) — the note is the shop window; the artefacts are the shop.

## 45.5 The Ledger So Far, and What's Next

Where the six projects stand against the anatomy — this table is the portfolio's table of contents, and Chapter 49 publishes it:

| # | Project | Tools | The finding it owns | The craft it proves |
|---|---|---|---|---|
| 1 | Monthly report | Excel | Growth 31%, oil −40%, Sundays traffic-poor | The one-page deliverable |
| 2 | Shop database | SQL | Ten questions as a query pack | Schema, joins, reproducibility |
| 3 | Report that builds itself | Python | An afternoon → twenty minutes | The pipeline, automated |
| 4 | Customers and churn | Python + stats | The loyal core is drifting | Cohorts, survival thinking |
| 5 | The survey | SPSS/tools | Intent ≠ behaviour, measured | Survey craft, chi-square |
| 6 | Operations dashboard | Power BI | The always-on shop | Model, measures, story |

Projects 1–3 are done (Parts II, III, V); this Part builds 4, 5, and 6 on the running case, then Chapter 49 assembles the portfolio. Your own seventh project — the public-data wild card from Chapter 44 — completes the set with data nobody planted for you, and the anatomy you now hold is the method for all of it.

> **From Your Toolkit — the anatomy is the job:** job postings (Ch. 50) are this checklist in prose; interviews (Ch. 52–53) test its moves; your first 90 days (Ch. 54) will be scored by how naturally you run it. The tools were five languages; this — the five moves, the checklist, the honest rules — is the *profession*, tool-blind and permanent.

## Key Takeaways

- Five moves, in order: question → data → clean → analyse → communicate; question written first, deliverable designed backwards; iterate, never skip.
- The one-page checklist is the book condensed — run it on every project, including your own.
- Time's truth: framing+cleaning ≈ 60%, analysis 20%, communication 20%; projects die at the edges — unowned questions, unanswerable data, unshipped tellings.
- The 150-word case-study note (situation/work/finding/impact/limits) is the portfolio's atom; write it on shipping day, file it with artefacts.
- Six projects on one running case + your public-data wild card = the portfolio; the anatomy is the method for all seven.

## Practice Lab

1. The audit, retroactive: run the full checklist against Project 3 (the automated report); mark every box you genuinely earned and every one you skipped; fix the two most serious gaps in the artefact itself.
2. The anatomy, pre-written: for Project 4 (next chapter — customers and churn), write the question (one sentence, decision attached), the audience, the success state, and the planned deliverable *before reading further*; compare with the chapter's brief when you get there.
3. The note, retro-fitted: write the 150-word case-study note for Projects 1 and 2 (they shipped before this chapter formalised the method); lift the numbers from your logs; attach the artefact paths.
4. The morgue tour: recall (honestly) any analysis in your life that died in a drawer — a course assignment, a work file, a personal project; name the drawer (unowned question / unanswerable data / unfinished tell); write the one-line door that would have saved it.
5. The checklist, printed: format this chapter's checklist into your own one-page reference (your words, your trail-backs); pin it — physical or digital — where projects happen. It will be in use in Chapter 49 and in your first job's first week.

## Further Reading

- Chapters 46–48 (the three projects, built on this anatomy), Chapter 49 (the portfolio assembled)
- *The Art of Statistics* (Spiegelhalter) — the PPDAC cycle (Problem, Plan, Data, Analysis, Conclusion) — this anatomy's academic twin
