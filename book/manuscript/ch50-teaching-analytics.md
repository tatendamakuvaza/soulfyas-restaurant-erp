# Chapter 50: Teaching Analytics — A Course Design and Instructor's Guide

*Part IX — The Extended Curriculum: Special Topics and the Craft of Teaching*

> "If you cannot teach it simply, you do not understand it well enough. If you can teach it, you own it forever."

### In this chapter you will learn

- How to turn this book into a 14-week course — sequencing, pacing, assessment, and outcomes.
- The lecture-lab-feedback rhythm that keeps a technical course alive.
- How to grade analytics work honestly: rubrics for code, memos, and presentations.
- How to run studio sessions, project reviews, and a capstone showcase.
- How to teach the tools you already know — SQL, Excel, Python, Power BI, Stata, SPSS — as one discipline, not six.
- How to keep your own teaching current without drowning in tools.

## 50.1 Why Teaching Is the Best Way to Learn

The Feynman technique is famous for a reason. When you teach a concept, you are forced to retrieve it, organise it, confront its edge cases, and answer for its assumptions. Every "dumb question" from a student is a free audit of your understanding.

**From Your Toolkit — SPSS:** You have already taught, even if you have not called it that. Walking a manager through a crosstab in SPSS, explaining a chi-square result, defending a regression table in a meeting — these are teaching events. This chapter scales that instinct into a discipline.

This chapter is written for three audiences at once: the instructor building a formal course, the analyst running internal upskilling, and the self-learner who needs a syllabus. The mechanics are the same; only the venue changes.

## 50.2 Course Outcomes: Design Backwards

Before pacing or slides, answer: **what will students be able to do at the end?** Write outcomes as observable behaviours, not topics covered.

Strong outcomes for this course:

1. Frame a business question as an analytics question with a stated decision, metric, and baseline.
2. Build a trustworthy dataset from messy sources — joins, cleaning, validation — and document its lineage.
3. Choose and defend a statistical test or model, including its assumptions and limitations.
4. Build a dashboard or data product that a non-analyst can use unaided.
5. Communicate findings as a decision recommendation with quantified uncertainty.
6. Audit their own work: leakage checks, sensitivity analyses, and honest error accounting.

Every lecture, lab, and assessment maps to at least one outcome. If a session supports none, cut it. That is the discipline of backwards design: outcomes → assessments → activities → content. Most courses are built in the opposite direction and feel like it.

## 50.3 Sequencing: Follow the Book's Arc

The course follows the book's structure, which was designed as a syllabus:

- **Part I (weeks 1–2):** Foundations. Questions before data; data maturity; the Vs; data types; the six-tool bridge.
- **Part II (weeks 3–5):** Data engineering. Joins, grain, pipelines, warehousing, pandas-to-SQL, cleaning, quality.
- **Part III (weeks 6–8):** Statistics. Descriptives, probability, testing, sampling, regression.
- **Part IV (weeks 8–9):** Visualization and BI. Craft, metric trees, dashboards, storytelling.
- **Part V (weeks 10–12):** Machine learning foundations. Framing, leakage, baselines, models, evaluation, ethics.
- **Part VI (weeks 13–14):** Advanced ML — clustering, recommenders, NLP, deep learning, LLMs — taught selectively for a first course.

A 14-week term covers Parts I–VI in depth and Parts VII–VIII by immersion: governance, Spark, and careers slot into the capstone fortnight, where they belong (you teach pipelines best when students are suffering a broken one). In a two-semester design, the second semester runs Part IX's special topics (Chapters 46–50), Part X's ten industry playbooks as case-method seminars, Part XI's frontier chapters as honours reading, and Part XII's delivery craft as role-play. Teach eighty chapter/appendix units as a full-year course: the arc spans Parts I–XII, from first principles to the business of the craft, and it is coherent end to end.

**Teaching Tip — The bridge is the course.** Students arrive knowing tools — SPSS from a stats service course, Excel from an internship, SQL from a bootcamp. The course's job is to connect those tools into one discipline. Never say "forget Excel"; say "here is what Excel was doing all along, and here is where it runs out." Respect for prior knowledge is not politeness; it is pedagogy.

## 50.4 The Weekly Rhythm: Lecture, Lab, Feedback

A week that works:

| Slot | Length | Activity | Failure mode it prevents |
|---|---|---|---|
| Lecture | 60–90 min | Concepts, live demos, toolkit bridges | Pure theory with no grip |
| Lab | 90–120 min | Students work the chapter's Practice Lab in pairs | Watching demos without doing |
| Feedback | 15–30 min | Instructor reviews 2–3 student artefacts live | Students repeating errors all term |
| Memo | Homework | One-page write-up of the lab's finding | Analysis that cannot be communicated |

The feedback slot is the engine. Reviewing real student work publicly — kindly, specifically — teaches more than any slide, because every student recognises their own errors in someone else's artefact. Rotate whose work is reviewed so everyone is showcased and everyone is polished.

**Teaching Tip — Live coding beats slides.** Type the SQL. Make the syntax error. Debug it. Students learn that errors are the job, not the exception. Prepare a backup notebook for when the live demo truly dies, but let small failures happen on purpose: the recovery is the lesson.

## 50.5 Pacing: Where Students Struggle

The known pain points, and the responses that work:

| Concept | The struggle | The response |
|---|---|---|
| Joins and grain (Ch. 6–8) | Fan-out feels arbitrary until it bites | The duplicated-orders lab: let them find the 3x revenue inflation themselves |
| Hypothesis testing (Ch. 14) | p-value as ritual, not reasoning | The coin-flip simulation: see 5% of fair coins "significant" at n=20 |
| Leakage (Ch. 22) | Everyone nods, everyone leaks | The leaky-feature audit: give them a dataset with a planted leak |
| Baselines (Ch. 23) | Skipping straight to XGBoost | The league table: naive baseline first, model second, side by side |
| Interpretation (Ch. 25, 33) | Reading coefficients as causes | The confounded coffee example: same data, two stories |

Budget extra weeks for joins and testing; steal them from dashboards and deep learning if you must. A student who can grain a table and read a p-value honestly can learn Plotly next week. The reverse is not true.

The second semester's pain points are different: case-method seminars (Part X) struggle until students stop summarising and start deciding ("what would you do Monday morning?"); frontier chapters (Part XI) struggle when taught as surveys — one chapter, one paper, one replication keeps depth honest; and the delivery role-plays (Part XII) feel theatrical until the first hostile-question round lands, after which nobody mocks them again.

## 50.6 Assessment: Grade the Artefacts

Grade what analysts produce, not what exams can measure. A scheme that has survived many cohorts:

| Component | Weight | Artefact | Graded on |
|---|---|---|---|
| Weekly memos | 25% | One-page lab write-up | Decision framing, honest uncertainty, clarity |
| Midterm project | 25% | Cleaned dataset + EDA memo | Lineage, validation, quality checks |
| Capstone | 40% | End-to-end analysis + presentation | Outcome rubric below |
| Participation | 10% | Labs, reviews, showcase | Presence and contribution |

Draw viva questions from each part's Practice Labs and Key Takeaways, and use them where students defend their capstone choices aloud. Oral defence is the only assessment that reliably catches borrowed work and missing understanding simultaneously.

The capstone rubric, shared with students on day one:

| Criterion | Weight | Excellent looks like |
|---|---|---|
| Framing | 20% | Decision question stated; stakeholder named; success metric chosen and defended |
| Data craft | 20% | Lineage documented; validation gates; no leakage |
| Analysis | 25% | Baseline → model → comparison; assumptions checked; sensitivity run |
| Communication | 25% | Memo a manager reads; charts follow Ch. 17; executive summary passes the stranger test |
| Reproducibility | 10% | A classmate can rerun it from the repo |

For honours/second-semester students, extend the capstone with one Part X playbook applied to a local organisation, one Part XI method replicated on public data, or one Part XII engagement role-play — one extension, done deeply, beats three done thinly.

## 50.7 Running the Studio: Reviews and Showcases

**Project reviews.** At weeks 4, 8, and 12, students present work-in-progress for ten minutes and receive structured critique: two strengths, two risks, one recommendation. This mirrors real practice (Ch. 71's project reviews) and teaches the hardest professional skill — receiving critique without defending.

**The showcase.** The final session is public: students present capstones to a real audience — managers from local businesses, other faculty, family. Real audiences raise the stakes productively; students polish slides that would have stayed rough for classmates. Invite a working analyst to give one sentence of feedback per presenter: practitioners' praise is remembered for years.

**From Your Toolkit — Power BI:** the showcase *is* a dashboard demo, so coach it as one: one screen, one message, thirty seconds to the point. Students who have presented a Power BI report to a manager already know the genre; name that knowledge.

**Slide kits for every part.** Appendix I holds a starter slide deck for each of the twelve parts — twelve decks, 8–12 slides each, with the one diagram that anchors each part: the analytics question ladder (Part I), the star schema (Part II), the testing logic tree (Part III), the chart-choice matrix (Part IV), the modelling loop (Part V), the represent-learn-predict map (Part VI), the scale decision test (Part VII), the insight-to-impact chain (Part VIII), the teach-back cycle (Part IX), the playbook canvas (Part X), the frontier map (Part XI), and the engagement arc (Part XII). Adapt them; do not merely display them. If you prepare eighty chapter maps from the deck skeletons you will never wonder what to say.

## 50.8 Teaching the Tools as One Discipline

The six modules of your foundation are not six subjects. Taught as one discipline, they become a grammar:

- **SQL** is the language of *what happened* — selection, aggregation, joins, windows.
- **Excel** is the language of *business arithmetic* — the model of the business everyone shares.
- **Python** is the language of *anything, at any scale* — the glue that connects every other tool.
- **Power BI** is the language of *what everyone sees* — the interface between analysis and organisation.
- **Stata** is the language of *econometric caution* — the tool that asks "identified by what?"
- **SPSS** is the language of *classical statistics* — the hypothesis-testing ritual, done properly.

When you teach joins, show them in SQL, then Excel-VLOOKUP, then pandas-merge, then the Power BI relationship model — same concept, four syntaxes. When you teach testing, show SPSS's crosstab, Stata's `prtest`, and the Python simulation of the same question. Transfer, not coverage: students who see one idea in four tools stop believing tools are knowledge.

**Teaching Tip — Retire the syllabus, not yourself.** Tools churn; the grammar does not. When a student asks about a tool this book does not cover, the honest answer is: "Here is the grammar it implements; find which parts it changes." Model that answer and you have taught Chapter 47's final lesson — how to stay current — as a living practice.

## 50.9 Your Own Development as an Instructor

Three habits keep a course alive:

1. **Teach one new thing every term** — a new dataset, a new method, a new failure story from practice. The course that never changes is the course that dies.
2. **Keep a teaching log** — what worked, what died, the questions that stumped you. Chapter 45's career habit, applied to the classroom.
3. **Bring practice in** — guest practitioners, your own consulting war stories, the Appendices E and J case portfolio. Students can smell the difference between a course about analytics and a course from analytics.

## 50.10 A Closing Note from the Author

If you have taught through this book, you have given eighty chapters of grammar, practice, and judgement to people who will use them in ways you will never see. That is the compounding of teaching: every analyst you train multiplies the honesty and the craft of every decision they touch. This chapter closes the taught syllabus, but not the book: Part X walks the industries where your students will work, Part XI pushes to the frontier they will extend, and Part XII teaches the delivery craft they will practise. Teach on.

*— Tatenda Makuvaza, "The Big Data Analyst"*

## Key Takeaways

- Design backwards: outcomes first, assessments second, activities third. If a session maps to no outcome, cut it.
- The weekly rhythm is lecture → lab → live feedback → memo; the feedback slot is the engine.
- Grade artefacts, not exams: memos, projects, defences. The viva catches what written work hides.
- Students struggle predictably — at joins, testing, leakage, baselines, and interpretation. Budget time there, and let the pain points teach.
- Teach the six tools as one grammar, shown in four syntaxes. Transfer, not coverage.
- Teach one new thing every term, keep a log, bring practice in — a course is a product with users, and it deserves the same craft.

## Practice Lab

1. Write the six course outcomes for your own context (your team, your classroom, your self-study) as observable behaviours — then audit this book's chapters against them: which chapters serve which outcomes?
2. Design your 14-week pacing grid: chapters to weeks, labs to chapters, one review week, one showcase week. Mark the two weeks you expect joins and hypothesis testing to eat.
3. Draft the capstone rubric adapted to your audience, and write the one-page handout version students receive on day one.
4. Run one studio review — a colleague or classmate presents work-in-progress for ten minutes; you deliver two strengths, two risks, one recommendation; write down what the format caught that informal feedback would not.
5. Prepare a ten-minute live-coded lesson on one concept from this book, deliberately including one recoverable error; teach it, then log what the error taught.
6. Take the Part XII hostile-question protocol and run it against your own capstone: present to a friend who must ask the three hardest questions from Chapter 74. Survive, then repeat.

## Further Reading

- *Understanding by Design* — Wiggins and McTighe (backwards design)
- *Teaching Naked* — José Antonio Bowen (technology outside the classroom)
- Appendix I (slide kits), Appendix J (case portfolio)
