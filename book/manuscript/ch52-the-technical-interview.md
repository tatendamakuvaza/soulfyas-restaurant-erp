# Chapter 52: The Technical Interview

*Part VIII — Getting the Job*

> "The technical interview is not an exam about tools. It is a simulation of the job — with witnesses."

### In this chapter you will learn

- What technical interviews actually contain — the four formats, decoded.
- SQL tests: the classic question shapes, and how to pass them thinking aloud.
- Excel and case tests: what the spreadsheet exercise is really grading.
- Statistics questions: the six concepts tested, and the honest answers.
- The practice system: how to train for tests the way you trained this book.

## 52.1 The Four Formats

Technical interviews for analyst roles come in four shapes, often combined within one process. Knowing the shape tells you what is being graded — which is rarely what it looks like:

| Format | Looks like | Actually grades |
|---|---|---|
| **Live SQL/code screen** | "Write the query for top 3 per category" | Fluency *and* the thinking: clarifying, structure, checking |
| **Take-home task** | "Here's a dataset; send findings in 48h" | Craft judgement: scope, cleaning, honesty, communication — *not* model sophistication |
| **Spreadsheet exercise** | "In this sheet, find why revenue dropped" | Investigation process: hypothesis, pivot, verify — under time |
| **Rapid-fire knowledge** | "Inner vs left join? What's a p-value?" | Precision and honesty — can you say it in two sentences |

The universal truth across all four: **they are grading what it would be like to work with you** — do you ask sensible questions, state assumptions, check your work, admit uncertainty, communicate clearly? The candidate who reasons aloud, catches their own mistake, and fixes it *beats* the silent one who writes a perfect answer — because the first is showing the actual job.

## 52.2 The SQL Shapes

Live SQL screens draw from a small, stable repertoire. You have written every pattern in this book; here they are as questions:

1. **Top-N per group** — "top 3 selling items per category": aggregate → rank with ROW_NUMBER() OVER (PARTITION BY) → filter rn ≤ 3 (Ch. 19). *The* most common screen question in existence.
2. **The second-highest** — "second-largest sale": ORDER BY + OFFSET/LIMIT, or MAX with a WHERE < the max, or DENSE_RANK = 2 — they are testing whether you know *two ways* and can say why one is safer (ties).
3. **Join with a twist** — "customers with no orders": LEFT JOIN + WHERE right IS NULL (the anti-join, Ch. 17) — or "count customers *and* their orders even if zero" (LEFT + COUNT(column) vs COUNT(*), Ch. 15–16's two counts).
4. **The cumulative/running** — "running total by month": SUM() OVER (ORDER BY) (Ch. 19).
5. **Share of total** — "each category's % of revenue": grouped CTE + total, or SUM() OVER () (Ch. 18).
6. **The dedup** — "remove duplicate rows, keep latest": ROW_NUMBER() partitioned by key, ordered by date DESC, keep rn = 1 (Ch. 19 + 8 combined).

The *method* for the live version, as important as the answer: repeat the question in your own words; state one assumption out loud ("assuming 'selling' means revenue, not units — I'll note the alternative"); write it in readable steps (CTEs — the interviewer reads them like paragraphs); then *self-check*: "row counts before and after the join, and the total should reconcile." The candidate who says "I'd check the total didn't double" is performing Chapter 17's law, live, and every interviewer recognises it.

## 52.3 Excel and Case Tests

The spreadsheet exercise (usually 30–60 minutes, a "messy" workbook): a sales sheet with three spellings of a region, blanks, mixed date formats, and a question like "did the March dip hit all regions?". What they grade, in order: **do you profile before you touch?** (counts, duplicates, the shape — Chapter 8's liturgy); **do you build the checkable?** (a cleaned copy, formulas traceable, no hard-typed numbers); **do you answer as a sentence with a number and a caveat?** The case version (verbal, sometimes in the spreadsheet): "revenue is down 8% — walk me through how you'd investigate" — graded on hypothesis structure: *segment the fall* (region? channel? product? — the decomposition instinct), *find the movement* (trend vs step vs level shift), *check the data first* (a classic trick: the "drop" is a missing week's data — Chapter 44's reconciliation instinct catches it, and mentioning that possibility unprompted is the single strongest move available in a case interview).

## 52.4 Statistics Questions

The six concepts that account for nearly all statistics screening, with the two-sentence honest answers (all Part IV; the discipline is brevity *plus* correctness):

- **p-value**: "The probability of seeing evidence this strong if nothing were really happening. Small p means 'surprising under the null', not 'probably true'."
- **Statistical vs practical significance**: "Significance says it's not noise; practical says it's worth money. With big n, 2-cent differences are 'significant' — I always report effect size with the p."
- **Correlation vs causation**: "Three explanations — coincidence, confounding, causation — and only an argument (ideally an experiment) licenses the third. I name confounders before claiming causes."
- **Type I vs II**: "False alarm vs missed effect. α sets the first; sample size drives the second. In business, false alarms send teams chasing ghosts, so I guard Type I."
- **Which test**: "Compare means → t-test (paired if the same units measured twice); compare proportions/counts → chi-square; relationship between two numbers → correlation, then regression for the line. I check assumptions before running."
- **Sample vs population**: "My data is a sample of the process I care about — 18 months is not forever, this shop is not all shops. Intervals state how wrong the estimate might be."

Interviewers probe these with follow-ups ("so is 0.05 magic?" — no, convention; "what if the p is 0.06?" — same evidence, weaker label; pre-decide α and report the effect honestly). The candidates who answer *like analysts* — with the caveat attached, unprompted — are distinguishable within two questions.

## 52.5 The Practice System

Train as you trained this book — reps on real shapes, not passive rereading:

1. **SQL reps**: LeetCode/HackerRank SQL sets (the database medium tier ≈ this book's level; StrataScratch and DataLemur mirror real interview questions) — 30 minutes daily, *thinking aloud even alone*, and always the self-check line after each solve.
2. **The mock spreadsheet hour**: rebuild Project 1's cleaning-and-question flow on a fresh messy dataset weekly until it fits inside 45 comfortable minutes.
3. **The statistics drill, spoken**: a friend (or camera) asks the six questions randomly; you answer in two sentences; the grade is honesty + brevity, not vocabulary.
4. **The take-home rehearsal**: Project 4 *is* one — reread its deliverable folder as an interviewer would, 30 seconds per artefact, and note the first impression; that impression is what your next take-home must produce.
5. **Appendix E**: one hundred interview questions across tools and topics, with guidance — the practice bank; work it in batches of ten, aloud, and let it find your gaps the way this book's labs found them.

> **From Your Toolkit — the interview is the job, compressed:** every tested shape is a Part of this book performed under observation: the SQL screen is Part III with an audience; the spreadsheet case is Part II on a clock; the statistics questions are Part IV in two sentences; the take-home is Part VII's anatomy with a deadline. You have been rehearsing this interview since Chapter 6 — what remains is format fitness, and format fitness is bought with reps.

## Key Takeaways

- Four formats, one grade: what you'd be like to work with — clarify aloud, state assumptions, self-check, admit limits.
- SQL screens draw from six shapes; know two routes to each and always say the reconciliation check.
- Spreadsheet/case exercises grade the process: profile first, build checkable work, answer in sentences with caveats — and suspect the data before the story.
- Statistics screening is six concepts; two-sentence honest answers beat five-minute lectures.
- Train with reps and aloud-ness: daily SQL sets, weekly mock-spreadsheet hour, spoken stats drill, and Appendix E's bank in batches.

## Practice Lab

1. The six SQL shapes, timed: solve all six from memory in one sitting (your own data or DataLemur); note where you hesitated; drill that shape daily for a week.
2. The aloud drill: record yourself solving two SQL questions *narrating* the method (repeat, assume, build, check); listen back once; note the silences — those are the interview's dead air.
3. The case rehearsal, twice: "revenue is down 8%" — once as a spoken investigation (10 min), once with a sabotaged dataset where the drop is missing data; did you check the data first? (Now you always will.)
4. The statistics gauntlet: a friend/camera asks the six plus follow-ups; two sentences each; repeat weekly until the caveats arrive unprompted.
5. The take-home, redone: pick any Chapter 50 target posting's *plausible* take-home (or invent one from its duties); execute it in four hours with the full folder craft; score yourself against Chapter 45's checklist — this rehearsal is the closest thing to the real thing that exists.

## Further Reading

- Chapter 53 (cases, behaviour, and the offer), Appendix E (the 100-question bank)
- DataLemur and StrataScratch's free question sets — real interview shapes, explained
