# Chapter 1: What Analytics Is — Decisions Before Data

*Part I — Foundations of Big Data Analytics*

> "Analytics is not the study of data; it is the study of decisions, with data as the instrument."

### In this chapter you will learn

- The definition that organises this book: analytics exists to change decisions.
- The question ladder: decision → question → data → analysis → decision again.
- The running case: Soulfya's Restaurant Group and its founder's first question.
- The failure mode that wastes most budgets: analysis without a decision attached.
- How your six tools already fit the discipline — starting with the one everyone underestimates.

## 1.1 The Definition That Matters

Ask ten people what analytics is and you will hear about dashboards, models, SQL, statistics. All true and all secondary. The definition that organises everything in this book: **analytics is the discipline of changing decisions with evidence.** If nothing anyone does will differ based on the answer, the work is not analytics — it is decoration. This is not a slogan; it is a triage rule you will apply in every chapter: before the query, before the model, before the beautiful chart, ask *what will someone do differently?*

## 1.2 The Question Ladder

Every analysis climbs (or should climb) the same five rungs, in order:

1. **The decision** — what is being decided, by whom, when?
2. **The question** — what would we need to know to decide well?
3. **The data** — what evidence exists, and what is its honesty?
4. **The analysis** — the methods that connect evidence to the question.
5. **The decision, again** — the recommendation, with its uncertainty, delivered to the decider.

The ladder's power is in its order. Teams that start at rung 3 ("what data do we have?") build dashboards nobody consults; teams that start at rung 4 ("we know a great model for this") answer questions nobody asked. Climbing down is always allowed — analysis often reveals the question was wrong — but climbing in order is what keeps the work honest.

## 1.3 The Running Case: Soulfya's Restaurant Group

**Soulfya's** is a three-outlet restaurant group in Harare — Avondale, Borrowdale, and Bulawayo — founded by **Azu**, a chef who bootstrapped from a single kitchen and now signs every invoice herself. The group has a loyalty programme (**Soul Circle**, 48,000 members), a growing delivery channel, and a founder with a question that will carry this entire book:

> "We have three outlets and everyone says open a fourth. I can read a spreadsheet. What I cannot do is tell the difference between *feeling busy* and *being ready*. Which is it?"

That question — a real decision, a real decision-maker, a real deadline — is the shape of every problem in this book. By Part II you will build Soulfya's data room; by Part V you will model its members; by the end, you will have answered the founder's question properly — and you will notice it was never really a data question at all.

**From Your Toolkit — Excel:** when Azu says "I can read a spreadsheet", she is describing the analyst's first instrument. Excel is where most real analytics careers start, and its disciplines — one row per thing, one column per fact, totals that reconcile — are the same disciplines this book will scale up to warehouses and models. Do not let anyone tell you it is not real analytics; it is analytics at grain one.

## 1.4 The Cost of Skipping Rung One

The industry's most expensive habit is analysis without a decision attached. Symptoms: the dashboard with forty tiles and no owner; the model that scores everything and changes nothing; the quarterly report that is "for information". The cost is not only the wasted effort — it is the **credibility tax**: every decorative artefact teaches the organisation that analytics is noise, and the tax is paid later, when a real analysis needs to be believed.

The professional discipline is Chapter 72's, learned on day one: *if the request has no decision, the honest response is a scoping conversation, not a project.* "What will you do differently once you know this?" is the most valuable sentence in the analyst's vocabulary — and the least used.

## 1.5 Analytics, Data Science, and the Rest of the Names

The job titles blur at the edges, and the honest mapping is by ladder position: **analysts** live between rung 3 and 5 (evidence to decision), **data scientists** extend rung 4 (models, experiments, causal claims), **data engineers** own rung 3's infrastructure, and **analytics engineers** (Chapter 69) industrialise the join between them. The names churn; the ladder does not. Learn the ladder and the titles become job descriptions rather than identities.

## 1.6 Failure Modes

- **Dashboard theatre** — measurement as performance; forty tiles, no decisions, full parking lot.
- **The orphan report** — a report that outlived its decision; archive it, and say so.
- **Question substitution** — the decision-maker's question ("are we ready?") quietly replaced by the analyst's preferred question ("can I forecast revenue?"). Name the substitution out loud or refuse it.
- **Rung-three gravity** — starting from the data because it is what you control; the ladder exists to fight this.

> **Teaching Tip — The decision journal:** open the course (or your practice) with one artefact: a page where every analysis starts with three lines — the decision, the decision-maker, the date the decision falls due. Students resist it for two weeks; by week six they refuse to start work without it, which is the entire chapter, internalised.

## Key Takeaways

- Analytics is the discipline of changing decisions with evidence; everything else is instrument.
- Climb the ladder in order: decision, question, data, analysis, decision again.
- "What will you do differently?" is the triage question that prevents decoration work.
- The titles blur; the ladder is the stable map of the craft.
- Soulfya's carries the whole book: a real founder, a real question, a real deadline.

## Practice Lab

1. Write the decision journal entry for Soulfya's fourth-outlet question: the decision, the decision-maker, the deadline, and the two questions the decision actually depends on.
2. Audit your own world (work, course, or a club you know): list five analyses or reports that exist; for each, name the decision it serves — or mark it for the archive.
3. Take one dashboard you can access and count its tiles; for each tile, write what someone would *do* differently based on it. Report the ratio of actionable to decorative.
4. The question substitution exercise: find a public "analysis" (a news graphic, a corporate tweet) and reconstruct the question it answers versus the question its audience actually holds.
5. Write Azu's question as three analytics questions, in one sentence each — the test of clarity being that a non-analyst can repeat them.

## Further Reading

- *How to Lie with Statistics* — Huff (the classic on evidence in the wild)
- Chapter 2 (the maturity ladder), Chapter 71 (the project discipline this chapter previews), Appendix J (five decisions, fully worked)
