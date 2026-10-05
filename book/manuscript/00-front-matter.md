# Front Matter

## About This Book

**Big Data Analytics and Machine Learning — The Complete Practitioner's Course: From SQL, Excel and SPSS to Spark, Deep Learning and Production AI**

**Tatenda Makuvaza — "The Big Data Analyst"**

First Edition, 2026

### How This Book Came to Be

I completed a six-module data analytics course — SQL, Excel, Python, Power BI, Stata and SPSS — and then faced the question every graduate faces: *what now?* The tools were in my hands, but the path from "I know some SQL and I can build a dashboard" to "I can run an analytics practice, teach a class, and ship a machine-learning system people trust" was nowhere written down. This book is the path, written down — twelve parts, eighty chapters, and a set of appendices designed to be taught from as readily as they are read.

Every chapter is built on the same bridge: **From Your Toolkit** callouts connect each new idea back to the six foundation modules, because you never learn analytics by abandoning what you know — you learn it by extending it. And every concept lives in one running world: **Soulfya's Restaurant Group**, a fictional three-outlet restaurant chain in Harare whose data carries the whole book, from its first spreadsheet to its production ML systems.

### Who This Book Is For

- **Graduates of foundation courses** who know the six tools and need the disciplines that turn tools into practice.
- **Working analysts** who want to move from reports to models, and from models to systems.
- **Instructors** building a course: the book is sequenced as a full syllabus (below), with a slide kit, an assessment bank, worked solutions, and a complete instructor's guide in Chapter 50.
- **Self-taught practitioners** who want their knowledge to have the same foundations a degree would have given them.

### The Arc of the Book

| Part | Question it answers | What it holds |
|---|---|---|
| I — Foundations | What is analytics, and when is data actually big? | Questions, maturity, the Vs, data types, your six tools |
| II — Data Engineering | Where does trustworthy data come from? | Grain, joins, pipelines, warehouses, cleaning, quality |
| III — Math and Statistics | How do I argue with numbers honestly? | Descriptives, probability, sampling, testing, regression |
| IV — Visualization and BI | How do I make numbers change minds? | Chart craft, metric trees, dashboards, storytelling |
| V — Machine Learning | How do I make data predict? | Framing, leakage, baselines, models, evaluation, ethics |
| VI — Advanced ML | What lies beyond the first model? | Clustering, recommenders, NLP, deep learning, LLMs, explanation |
| VII — Big Data and Cloud | What changes at scale? | The decision test, DuckDB, Spark, streaming, cloud economics |
| VIII — Insight to Impact | How do we run this responsibly, forever? | Governance, MLOps, monitoring, ethics, careers |
| IX — Extended Curriculum | How do we go further — and teach it? | Anomaly detection, optimization, graphs, data products, teaching |
| X — Domain Playbooks | How is analytics actually used, industry by industry? | Ten sector playbooks with metrics, methods and running cases |
| XI — The Frontier | What lies beyond the working core? | Causality, space, time, language, simulation, privacy, staying current |
| XII — The Practitioner's Path | How is analytics actually delivered? | Projects, engagements, interviews, storytelling, documentation, audits, constraint, onboarding and the business of the craft |

The book has twelve parts and eighty chapters. Parts build on each other, but each part is designed to be coherent on its own, so a course can enter at Part III (statistics) or Part V (machine learning) if the foundations are already in place. Part IX (Chapters 46–50) extends the curriculum with special topics — anomaly detection, optimization, graph analytics, and data products — and closes with a complete instructor's guide. Part X (Chapters 51–60) is a set of ten industry playbooks — retail, marketing, financial services, healthcare, agriculture, energy, transport, manufacturing, government, and media and sport. Part XI (Chapters 61–70) is the frontier: causal inference, geospatial analytics, survival modelling, hierarchical and probabilistic forecasting, language analytics for low-resource languages, simulation and synthetic data, experimentation at scale, privacy engineering, analytics engineering, and staying current. Part XII (Chapters 71–80) is the practitioner's path — the delivery craft.

### How to Read This Book

Three habits, sustained across eighty chapters, are worth more than any tool in it:

1. **Ask the decision question before the data question.** Every chapter's first move is "what will someone do differently?"
2. **Name a baseline before praising a result.** Seasonal-naive, majority class, last year: if you cannot beat the cheapest alternative, use the alternative.
3. **Write for a reader who is not you.** Memos, model cards, logs: the artefact is the analysis.

Read with a lab open. Every chapter ends with a Practice Lab, and the labs are load-bearing: the prose is scaffolding for the labs, not the other way around.

### A Fourteen-Week Course Plan

| Week | Chapters | Theme | Lab focus |
|---|---|---|---|
| 1 | 1–3 | Questions, maturity, the Vs | Data inventory |
| 2 | 4–5 | Data types; your six tools bridged | JSON and sources |
| 3 | 6–7 | Joins and SQL craft | Fan-out demo |
| 4 | 8–9 | Grain, pipelines | Star schema |
| 5 | 10–11 | pandas-to-SQL; cleaning and quality | Validation gates |
| 6 | 12–13 | Descriptives; probability by counting | Bayes table |
| 7 | 14–15 | Testing; sampling and resampling | Simulation lab |
| 8 | 16–17 | Regression; visualization craft | Chart audit |
| 9 | 18–20 | Metric trees, dashboards, storytelling | One-page dashboard |
| 10 | 21–23 | Framing, leakage, linear models | Framing artefact |
| 11 | 24–25 | Evaluation; regularized regression | Baselines and metrics |
| 12 | 26–28 | Forecasting; trees; logistic models | MASE league table |
| 13 | 29 + 30–32 | Ensembles; clustering, recommenders | League table; segments |
| 14 | 33–36 (skim 37–45) | Uplift, forecasting depth, NLP, deep learning, LLMs | Capstone presentation |
| Extension term | 46–80 + Apps I–J | Special topics, domain playbooks, frontier methods and the delivery craft; case-method seminars from Appendix J | Extended capstone or honours seminar |

Chapters 37–80 make an excellent second-semester or honours extension: Spark, streaming, cloud, governance, MLOps, case studies and careers; Part IX's special topics with the full instructor's guide of Chapter 50; Part X's ten domain playbooks, best taught as case-method seminars with Appendix I's slide kits and Appendix J's five end-to-end cases; Part XI's frontier chapters for honours students, one chapter and one paper per week; and Part XII's delivery craft, best taught through its role-plays.

### The Appendices

Ten appendices back the course: **A** a Python crash course; **B** a SQL reference card; **C** an algorithm quick-reference; **D** a glossary; **E** datasets and resources; **F** the Soulfya's practice-dataset generator (a script that fabricates the entire running case study's data with planted patterns); **G** worked solutions to selected practice labs; **H** the assessment bank (midterm, final and viva questions with marking guidance); **I** the instructor slide kit; and **J** the extended case portfolio.

### A Note on the Running Case

Soulfya's Restaurant Group is fictional, and so is everyone in it — but nothing about its data is arbitrary. Its outlets (Avondale, Borrowdale, Bulawayo), its Soul Circle loyalty programme, its delivery channel and its reviews carry every pattern this book teaches: weekly seasonality, payday spikes, promo lifts, outlet differences, a genuine churn signal. By Part V you will model its customers; by Part VII you will scale its pipelines; by Part XII you will run its projects. If the chain feels real by Chapter 10, the book is working.

*— Tatenda Makuvaza, "The Big Data Analyst", Harare, 2026*
