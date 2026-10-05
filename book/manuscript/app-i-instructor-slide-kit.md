# Appendix I: Instructor Slide Kit

*Twelve starter decks — one per part — for teaching the course*

> "Slides are promises about time: each one says 'this many minutes, this one idea'."

## How to Use This Kit

Each deck below is a skeleton: slide titles, the one message per slide, and the teaching note that anchors it. Build them in PowerPoint, Google Slides, or (for the reproducible) Marp or Quarto — the structure survives any medium. The decks are deliberately short: 8–12 slides each, one idea per slide, so that the lecture's remaining minutes belong to the live demo and the lab, where learning actually happens.

General deck rules (Chapter 17 applies to slides too):

- One message per slide, stated as the slide's title — a claim, not a label ("Joins duplicate fact rows" beats "Joins").
- Evidence on the slide: one chart or one table, never both.
- Speak the takeaway; the slide carries only what words cannot — numbers, shapes, structure.
- End every deck with the lab brief: what students do in the next ninety minutes.

## Deck 1 — Part I: Foundations of Big Data Analytics

1. **Title.** Course name, your name, the promise: from six tools to one discipline.
2. **Analytics is decisions, not data.** The question ladder: decision → question → data → analysis → decision again.
3. **The maturity ladder.** Descriptive → diagnostic → predictive → prescriptive; where the value and the difficulty both live.
4. **When is data big?** The Vs, honestly: most "big data" problems are big-*mess* problems.
5. **Data types and where they hide.** Structured, semi-structured, unstructured; JSON in the wild.
6. **The six-tool bridge.** SQL, Excel, Python, Power BI, Stata, SPSS — one grammar, six dialects.
7. **Soulfya's Restaurant Group.** Meet the running case: three outlets, one loyalty programme, a delivery channel, and every pattern in this course.
8. **Lab brief.** The data inventory.

*Teaching note: the whole deck is one idea — questions before data. Everything else in Part I is vocabulary for that idea.*

## Deck 2 — Part II: Data Engineering for Analysts

1. **Title.** Part II — where trustworthy data comes from.
2. **Grain first.** The single question that prevents most analysis errors: what does one row mean?
3. **Joins.** Inner/left/anti — and the fan-out that multiplies revenue.
4. **Star schemas.** Facts and dimensions; why analysts build wide tables from narrow ones.
5. **Pipelines.** Extract, validate, load; the pipeline that runs is worth ten that are elegant.
6. **The pandas-to-SQL bridge.** Same grammar, different engine; push work to the data.
7. **Cleaning is contract negotiation.** Names, nulls, duplicates, units — each one a business question.
8. **Quality gates.** Validation as code; trust is a pipeline property.
9. **Lab brief.** Build Soulfya's star schema.

*Teaching note: run the duplicated-orders demo live — the gasp when revenue triples is the whole part.*

## Deck 3 — Part III: Mathematics and Statistics

1. **Title.** Part III — how to argue with numbers.
2. **Descriptives lie honestly.** Mean/median/spread; Anscombe's lesson in four datasets.
3. **Probability by counting.** The joint table; Bayes as arithmetic on a grid.
4. **The logic of a test.** Hypothesis, statistic, p-value, decision — and what a p-value is not.
5. **Simulation over formula.** The coin-flip lab: watch false positives appear.
6. **Sampling.** Random, stratified, weighted; the exit poll that went wrong.
7. **Regression.** One line, three stories; slope as rate, residuals as information.
8. **Lab brief.** The Bayes table; the permutation test.

*Teaching note: never teach the formula first. Count first, simulate second, formula third — the formula then arrives as a shortcut, not a mystery.*

## Deck 4 — Part IV: Visualization and BI

1. **Title.** Part IV — charts that change decisions.
2. **Form follows question.** The chart-choice matrix: comparison, distribution, composition, relationship, trend.
3. **Pre-attentive craft.** Colour, position, length; ink spent on the message.
4. **The metric tree.** Goals → drivers → metrics; dashboards as forests, not trees.
5. **Dashboard genres.** Operational, tactical, strategic — one audience, one question, one screen.
6. **Power BI as product.** The toolkit bridge: relationships, measures, bookmarks.
7. **Storytelling.** Context → conflict → resolution; the executive summary that survives the stranger test.
8. **Lab brief.** The one-page dashboard.

*Teaching note: bring bad charts (there are repositories of them) and let students perform the audit — critique teaches faster than admiration.*

## Deck 5 — Part V: Machine Learning Foundations

1. **Title.** Part V — the modelling loop.
2. **Framing.** Classification, regression, ranking, clustering — which question is this?
3. **Data before models.** Split logic, target leakage — the leak that flatters and lies.
4. **Baselines.** Majority class, seasonal naive, last year: the cheapest honest competitor.
5. **Linear models.** The line, regularized; interpretability as a feature.
6. **Evaluation.** The metric matches the decision: precision/recall trade-offs, calibration, cost curves.
7. **Trees and ensembles.** Splits, forests, boosting; variance and bias made visible.
8. **Ethics from day one.** Fairness metrics, disparate impact, the model card.
9. **Lab brief.** The leaky-feature audit; the baseline league table.

*Teaching note: the planted-leak dataset (Appendix F) is the part's centrepiece — let students discover the AUC of 0.99 and then take it apart.*

## Deck 6 — Part VI: Advanced Machine Learning

1. **Title.** Part VI — beyond the first model.
2. **Clustering.** Segmentation as hypothesis generation, not truth.
3. **Recommenders.** Collaborative filtering; the cold start and the popularity trap.
4. **NLP.** Text as features: bag-of-words to embeddings.
5. **Deep learning.** When depth earns its keep; data, compute, and the humility curve.
6. **LLMs.** Tokens, prompts, fine-tuning; the analyst's assistant, not the analyst.
7. **Explanation.** SHAP, permutation importance — explaining models to the people who live with them.
8. **Lab brief.** The segmentation and recommender double lab.

*Teaching note: keep the deep-learning segment honest with the "when NOT to" slide — the discipline is the lesson.*

## Deck 7 — Part VII: Big Data Technologies and the Cloud

1. **Title.** Part VII — what actually changes at scale.
2. **The decision test.** Size, speed, structure, spend — most problems are single-node problems.
3. **DuckDB.** The analytical database on a laptop; push the work down.
4. **Spark.** Partitions, the shuffle, lazy execution — distributed thinking.
5. **Streaming.** Windows, watermarks; the dashboard that is always now.
6. **Cloud economics.** Storage, compute, egress; the bill as design feedback.
7. **Lab brief.** The Spark job on Soulfya's delivery events.

*Teaching note: open with the same dataset in pandas and DuckDB and let the stopwatch make the argument for the part.*

## Deck 8 — Part VIII: From Insight to Impact

1. **Title.** Part VIII — running analytics responsibly, forever.
2. **Governance.** Stewardship, lineage, privacy; trust as infrastructure.
3. **MLOps.** The pipeline, the registry, the smoke test; reproducibility as a habit.
4. **Monitoring.** Drift, decay, the champion-challenger rhythm.
5. **Ethics under load.** Consent, harm, the refusal clause.
6. **Careers.** The craft ladder: analyst → senior → lead → principal; the T-shaped professional.
7. **Lab brief.** The model card and the monitoring plan.

*Teaching note: this deck lands best after the capstone has broken something — governance reads differently mid-incident.*

## Deck 9 — Part IX: The Extended Curriculum

1. **Title.** Part IX — special topics and the craft of teaching.
2. **Anomaly detection.** Rules, distances, isolation; the two error costs of fraud.
3. **Optimization.** From prediction to prescription; the roster that writes itself.
4. **Graph analytics.** Entities, edges, communities; influence beyond the average.
5. **Data products.** The rung ladder: report → dashboard → app → API.
6. **Teaching.** Backwards design; the lecture-lab-feedback rhythm.
7. **Lab brief.** Ship one data product.

*Teaching note: this part is where students become colleagues — teach it as a seminar, not a lecture.*

## Deck 10 — Part X: Analytics Across Industries — Domain Playbooks

1. **Title.** Part X — ten industries, one grammar.
2. **The playbook canvas.** Core question, unit of analysis, key metrics, data reality, first project, failure mode — six slots, every industry.
3. **Retail and marketing.** Basket, churn, CLV, uplift; the promotion that pays for itself.
4. **Financial services and health.** Credit risk, fraud, readmission; the regulated industries, where explanation is law.
5. **Agriculture and energy.** Yield, weather, load, tariffs; forecasting where the weather is a feature.
6. **Transport, manufacturing, government, media.** Routing, OEE, programme evaluation, attention; each playbook in six slots.
7. **The pattern across playbooks.** Same grammar, different data realities — the analyst's real skill.
8. **Lab brief.** Fill the canvas for a local organisation.

*Teaching note: run this part as case-method seminars — Appendix J's five cases are the syllabus; the deck only frames the method.*

## Deck 11 — Part XI: The Frontier — Advanced Methods and Emerging Practice

1. **Title.** Part XI — where the working core ends.
2. **Causal inference.** DiD, IV, synthetic control; the question correlation cannot answer.
3. **Space and time.** Moran's I, survival curves, hierarchical forecasts; the structures between rows.
4. **Language and simulation.** Low-resource NLP, synthetic data, agent-based markets.
5. **Experimentation at scale.** Bandits, CUPED, sequential tests; the infrastructure of learning.
6. **Privacy engineering.** Differential privacy; sharing data safely.
7. **Staying current.** The reading discipline; ten predictions to track.
8. **Lab brief.** One frontier replication.

*Teaching note: one chapter, one paper, one replication — depth over survey; the frontier changes, the discipline of entering it does not.*

## Deck 12 — Part XII: The Practitioner's Path — Projects, Clients and the Craft of Delivery

1. **Title.** Part XII — analytics as a delivered service.
2. **The project arc.** Scope, plan, analyse, deliver; the stranger test at every phase.
3. **Engagements.** The options paper; pricing and the refusal clause.
4. **Stakeholders.** The question ladder; the no-surprises rule.
5. **Storytelling and documentation.** Three structures; the four artefacts; the analysis log.
6. **Audits, constraint, onboarding.** Ten audit questions; the $200 stack; the first ninety days; the trust ledger.
7. **The business of the craft.** The value ledger; productization; compounding practice.
8. **Lab brief.** The full engagement role-play.

*Teaching note: the role-play is the assessment — hostile questions, scope creep, a pricing decision, and a refusal, all in one session.*

## Deck Hygiene Checklist

Before any deck ships:

- [ ] One message per slide, stated in the title
- [ ] Every chart follows Part IV's craft rules
- [ ] Code screenshots never exceed half a slide
- [ ] The lab brief is the final slide
- [ ] You have spoken the deck aloud once, with a timer

Twelve decks, one course, roughly 110 slides — about two semesters of teaching material when each deck anchors a lecture and the labs carry the rest. Adapt freely: the skeletons are yours. The course, like the book, ends where your own practice begins.
