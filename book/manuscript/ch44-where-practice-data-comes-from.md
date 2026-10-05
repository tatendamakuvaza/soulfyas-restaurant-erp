# Chapter 44: Where Practice Data Comes From

*Part VII — Real Projects and Your Portfolio*

> "Tariro was invented so you could learn honestly. The world's real data is sitting right there, free, waiting for the same treatment."

### In this chapter you will learn

- The public-data landscape: where real, free practice data actually lives.
- How to choose a dataset that builds a career (and how not to).
- Generating your own data — the honesty of planted patterns, reversed.
- Reading a new dataset cold: the first hour, systematic.
- Building the data-habit that outlasts this book: one dataset a month.

## 44.1 The Public Landscape

The excuse that dies in this chapter is "I don't have data". Real, current, free data — government statistics, open city records, health data, sports, transport, World Bank indicators — is published deliberately for public use. The landmarks, with what each is *good practice for*:

- **Kaggle** (kaggle.com/datasets) — the supermarket of datasets: enormous variety, ratings, and (be careful) many over-cleaned "perfect" files. Good for: joining real-world mess with community notebooks to compare against.
- **Government open-data portals** — data.gov (US), data.gov.uk, and nearly every national statistics agency (ZimStat for Zimbabwe's official figures; Statistics South Africa; the UK's ONS). Censuses, prices, trade, health: authoritative, documented, and often gloriously messy. Good for: *serious* credibility — a portfolio project on national data reads professional.
- **The World Bank / UN / WHO** — indicators across countries and decades, clean APIs, well-documented. Good for: time-series and cross-country comparison projects (the gapminder tradition).
- **Open city data** — transport timetables and delays, air quality, property records, budgets. Good for: dashboards with a story a city-dweller instantly understands.
- **Blogs and academics who share** — FiveThirtyEight's archived datasets (politics, sports, culture), Tidy Tuesday's weekly community datasets, university data libraries. Good for: chart-practice reps with interesting questions attached.
- **APIs and scrapes** — weather, exchange rates, sports fixtures. Good for: the Python skills of Part V feeding a live dashboard (Chapter 61's stack makes this free).

The licensing note that keeps you professional: nearly all of the above are published under open licences permitting analysis and republication with attribution; check the licence page once per dataset, cite the source in your project README (the "says who?" habit, structural), and you are clean.

## 44.2 Choosing Data That Builds a Career

Not all practice data is equal. The selection criteria — the same criteria a hiring manager applies to your portfolio (Chapter 49):

1. **A question, not a dataset.** "Did the 2008 crisis change what Zimbabwe exports?" (World Bank trade data) is a project; "analysis of a CSV I found" is not. Choose data because it can answer something you actually wonder.
2. **Local relevance is gold.** A project on your *own city's* transport or your *own country's* prices stands out in a pile of US-flight-delays clones — it says "I look at the world around me", which is the analyst's actual job description.
3. **Messiness earns trust.** A dataset with real flaws (missing years, three spellings of one province — you know this world intimately from Part II) demonstrates cleaning craft. Perfect data demonstrates nothing.
4. **Two-table minimum.** Single-table projects cannot show joins — the model (Part III) and the relationships (Part VI) need at least two connected tables to exist. Prefer data with dimensions: who/what/where/when.
5. **A number a decision could rest on.** The best projects end in "therefore, X" — a recommendation, a verdict, a quantified gap. If you cannot imagine the last sentence of the analysis, the dataset may only be a toy.

## 44.3 Generating Your Own — the Reversal

You have spent a book learning on *generated* data (Tariro's), and there is a craft worth naming in that choice — because generating data is itself an analyst's skill, used for testing pipelines, teaching, and prototyping. The reversal of this chapter's title: when you generate, you *plant the truth*; when you analyse, you *hunt it*. The deepest lessons of this book came from that arrangement: you always knew the Sunday effect existed, so every method could be *scored against truth* — did the pivot find it? did the test close it? did the dashboard show it?

The generator's recipe (Appendix C carries the full code; the shape matters here): draw the honest noise first (amounts right-skewed around a lognormal; weekday counts varying), then *plant* the effects (Friday/Saturday +⅓; payday spikes; a month-9 price rise cutting oil quantity; a loyal core slowly churning), then record the truth in a `truth.md` file — "Sunday effect: −28%, planted" — so every analysis can be graded. That structure — noise + effects + truth file — is how professionals build test data for pipelines (does the anomaly detector fire on the planted anomaly *and only* on it?), and it is why Tariro's shop taught better than any open dataset could: **you were always scoring your methods against a known reality.** (One rule, ethical and absolute: generated practice data is labelled as generated, in the README, in capital letters if necessary. Synthetic data passed off as real is the portfolio's mortal sin — Chapter 59's territory.)

## 44.4 The First Hour on a New Dataset

The systematic approach to a dataset you have never seen — the skill this chapter actually installs, in the order the moves happen:

1. **Read the documentation first** (the data dictionary, the collection methodology, the licence). Ten minutes here saves an hour of misreading a column — and the methodology section is where you learn the *sample*'s biases (Chapter 25's questions, asked of the source).
2. **The four instruments** (Ch. 33): `head()`, `info()`, `describe()`, `value_counts()` — types, nulls, ranges, categories, and the surprises each one surfaces.
3. **The reconciliation sweep**: row counts vs the documented totals ("the file says 12,400 households; the data has 12,382 — why?"); duplicates on the key; orphans if multi-table. The loading liturgy, run cold.
4. **One plotted column of everything numeric** — histograms at scale; shape surprises (bimodal ages? a spike at round numbers?) become the first questions.
5. **Write the questions log** — the open questions the first hour raised, in a file that becomes the project's spine. Analysis is what happens between a questions log and its closure.

## 44.5 The Habit: One Dataset a Month

The compounding practice that separates the hired from the trained: **one new dataset a month, minimum** — an evening's first-hour, then whatever depth it earns. Twelve a year; by your first interview (Part VIII), you will have touched more real datasets than many working analysts touch in three years, and every tool-skill from this book will have been exercised on data that fought back. Keep a `data-journal.md`: date, dataset, one question asked, one thing learned, one surprise. The journal itself becomes portfolio evidence — of curiosity, which is the trait every interviewer probes for and none can teach.

> **From Your Toolkit — the supply chain:** every project in this Part (and the two jobs of Part VIII) is fed by this chapter: Project 4 and 6 run on Tariro's generated truth (scored!); Project 5 on a survey *you* collect; and your portfolio's "wild" project — the one that makes it three — comes from the public landscape here. The habit outlasts the book: the analyst with a supply of questions never lacks for work.

## Key Takeaways

- Free real data is abundant: Kaggle, national statistics agencies, World Bank/UN, city portals, community datasets — check the licence, cite the source.
- Choose by question, local relevance, messiness, multi-table shape, and decidable endings — the criteria hiring managers apply.
- Generated data = noise + planted effects + truth file; it scores your methods against known reality — and it must always be labelled synthetic.
- The first hour: documentation → four instruments → reconciliation sweep → plotted columns → questions log.
- One dataset a month, journaled — the compounding habit that makes every tool in this book permanent.

## Practice Lab

1. The first-hour drill, run on public data: pick a national-statistics dataset (ZimStat, ONS, or World Bank); run the full first hour including the questions log; save as `first-hour-<dataset>.md` — this file is the artefact.
2. The evaluation: score your chosen dataset against the five selection criteria, honestly; write the verdict — is it a project, a toy, or neither? If a toy, find a better one; if a project, open its questions log and leave it open for Project-time.
3. The generator, read: open Appendix C's Tariro generator; find each planted pattern in the code (payday, oil, churn); write the truth.md you would write for a generator of your own — then change one parameter and describe what an analyst would now find.
4. The journal, started: create `data-journal.md` with entries for every dataset this book has already made you touch (Tariro's four tables, the survey, your public pick); note the one-surprise line for each.
5. The question bank: write down five questions about your own city or country that public data might answer; rank them by how much the answer would matter to someone; the top one is your portfolio's wild-card project, queued.

## Further Reading

- Chapter 45 (the anatomy of the analysis these datasets feed), Appendix C (the generator)
- Tidy Tuesday (github.com/rfordatascience/tidytuesday) — a new dataset every week, community practice
