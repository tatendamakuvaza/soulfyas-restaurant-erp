# Chapter 57: A Gentle Map of Machine Learning

*Part IX — Beyond the Basics*

> "Machine learning is not a new career. It is your regression chapter, fed more data, pointed at prediction instead of explanation."

### In this chapter you will learn

- What machine learning actually is — the one-paragraph demystification.
- The vocabulary map: supervised/unsupervised, classification/regression, training/testing.
- The three ML questions a shop like Tariro's actually has.
- When you need ML and (mostly) when you do not.
- The learning path from this book's base — without the course-industrial complex.

## 57.1 The Demystification

Strip the mystique: **machine learning is fitting a function to data so it can make predictions on new data.** You fit a function in Chapter 28 — a line through oil prices and bottles; give it a new price, it predicts bottles. That *was* machine learning in embryo: a model (the line), parameters (slope, intercept), fitted (least squares), used for prediction. ML is the same skeleton with (a) models flexible enough to capture curves and interactions a straight line cannot, (b) data big enough to justify them, and (c) a culture obsessed with proving predictions work on data the model hasn't seen. Nothing in this sentence requires a PhD; it requires the discipline you already have — plus one new idea, next section, which is the culture's core.

Why "learning"? Because the parameters are not written by a human (nobody typed the slope); they are *estimated from data* — the machine "learned" them. The honest framing: it is statistics, industrialised, pointed at prediction — and its dangers are your book's dangers, amplified: overfitting (the model that memorises noise — Chapter 26's p-hacking, at scale), data leakage (the test sneaking into the training — a broken reconciliation), and the causation trap wearing a robot suit.

## 57.2 The Vocabulary Map

The terms, translated into chapters you own:

- **Supervised learning** — the model learns from *labelled* examples (past sales with their outcomes; past customers with their churn outcomes). Two flavours: **regression** (predict a number — next month's revenue; Chapter 28's line, generalised) and **classification** (predict a category — will this customer churn: yes/no; the t-test's question, answered per-customer).
- **Unsupervised learning** — no labels; find structure. **Clustering** (customers who resemble each other — the segmentation your cross-tabs did manually, automated), **dimensionality reduction** (many columns → few, losing little — the `describe()` instinct, compressed).
- **Training/testing split** — hide part of the data; fit on the rest; grade against the hidden part. *The single most important practice in the field*, and it is Chapter 25 in costume: the test set is the sample of the future, and grading on data the model has seen is evaluating a student on the exam they were allowed to memorise.
- **Features** — the input columns (Chapter 33's derived columns — the feature shelf you built *is* feature engineering).
- **Overfitting / underfitting** — too flexible (memorised noise) vs too rigid (missed the pattern): the bias-variance trade-off, which is "which typical?" (Ch. 22) applied to models.
- **Cross-validation** — the train/test idea rotated several times, so the grade doesn't depend on one lucky split: the bootstrap's cousin (Ch. 36).
- **The metrics** — for classification: accuracy (misleading on imbalanced data — 99% accuracy by predicting "no churn" always, when 1% churn), precision/recall (the trade-off that matters), the confusion matrix (a cross-tab of predicted vs actual — literally Chapter 27's table). For regression: RMSE (typical size of the miss — standard deviation's costume), MAE (the median's costume).

## 57.3 Tariro's Three ML Questions

The shop's genuine ML-grade questions, each mapped to its method and its trap:

1. **"Which customers will churn next month?"** — classification on Project 4's data: features = recency, frequency, tenure, basket trend (the columns you built); label = churned-in-the-following-month; method = logistic regression (the honest, interpretable start) or a random forest (more power, less interpretable). The traps: class imbalance (few churners — accuracy lies; use precision/recall), and *leakage*: if a feature knows the future ("days since last purchase" computed *after* the prediction date), the model scores brilliantly and predicts nothing. The professional's question about any impressive ML result: *what did the features know, and when?*
2. **"How much will we sell next week?"** — regression/time-series forecasting: next week's revenue per item from lags and seasonality (your `shift`/`pct_change` features, Chapter 34). Traps: the split must respect *time* (train on the past, test on the future — random splits leak tomorrow into yesterday), and the baseline to beat is embarrassingly strong: "same as last week" wins more often than fancy models deserve. Always report the naive baseline beside the model's.
3. **"What kinds of shoppers do we have?"** — clustering on customer features (basket size, frequency, category mix, weekday pattern): the segments your eye found in cross-tabs (the humps of Chapter 23!) found automatically. Trap: clusters are *descriptive* — "segment 3" needs a human to name it ("Saturday bulk buyers") and a decision to serve it; the algorithm finds the groups, the analyst finds the meaning.

## 57.4 When You Need It (Mostly You Don't)

The professional's filter, applied honestly: you need ML when **(a) the question is genuinely predictive** (a per-entity forecast that recurs: churn, demand, risk), **(b) there is enough labelled data** (hundreds of examples minimum, realistically thousands), **(c) the pattern is too complex for rules and regressions you can read**, and **(d) a small improvement is worth real money** (1% better demand forecast at scale = real money; 1% better understanding of 18 months of one shop = a pivot table). Most business questions — *what happened, why, what should we do* — are this book's questions, and a t-test with a caveat beats a black box with a dashboard. The analyst who reaches for ML last, not first, is the senior one; the junior who reaches for it first is announcing tools before questions (Chapter 54's first trap, at scale).

## 57.5 The Learning Path

From this book's base, the honest sequence (months, not weekends): (1) **consolidate** — pandas, scipy, regression fluently (Parts V–VI plus Chapter 28; you have this); (2) **scikit-learn fundamentals** — the `fit/predict` API, train/test splits, the metrics, on *your own* project data (churn on Project 4 is the perfect first dataset — labelled, meaningful, small enough to understand every error); (3) **one course or book, done properly** — the classic applied-ML courses (Andrew Ng's; the *Hands-On Machine Learning* book; fast.ai for the top-down temperament) — *one*, finished, with notes, not five, sampled; (4) **one project, shipped to the portfolio** with the honesty section the field respects most: the baseline comparison, the leakage audit, the error analysis (which customers does the model get wrong — and yes, you will find it over-predicts churn for the founding cohort, because class balance shifts over time; that finding is worth more than the model). Then decide — Chapter 56's fork has a data-science branch, and this chapter is its trailhead.

> **From Your Toolkit — the constant is the honesty:** every ML practice is a habit you own wearing new clothes: the train/test split is sampling discipline; leakage is the broken reconciliation; the baseline is "compared to what?"; the metrics debate is "which typical?"; the error analysis is the drill-down. The models change; the analyst's conscience — check it, reconcile it, caveat it — is the same instrument, and it is rarer in ML than it should be, which makes it *your* edge.

## Key Takeaways

- ML = fitting a function to data for prediction on new data; your Chapter 28 line was the embryo; the culture's core is grading on unseen data.
- Vocabulary: supervised (regression/classification) vs unsupervised (clustering); features = your derived columns; metrics are your statistics in costume — accuracy lies on imbalanced data.
- Tariro's three: churn (classification; leakage and imbalance), demand (time-series; the naive baseline), segments (clustering; humans name the groups).
- The filter: predictive question + enough labels + complexity beyond readable models + money in the margin — most questions are this book's questions.
- Path: consolidate → scikit-learn on your own churn data → one course finished → one shipped project with the honesty section; then the fork, knowingly.

## Practice Lab

1. The vocabulary bridge, written: define each ML term of 57.2 in one line *and* its Chapter costume in a second line; keep the two-column table — it is your interview answer for "do you know ML?" (the honest answer: "the fundamentals, from statistics up").
2. The leakage hunt, hypothetical: for the churn model, list five features and audit each — which could know the future? Rewrite the leaky ones as of prediction-date; write the one-sentence audit rule you just invented.
3. The baseline drill, on real ground: forecast last month's revenue with "same as last month" and "same weekday average"; compute the misses; that number — the one every fancy model must beat — goes in your log with its formula.
4. The clustering, run lightly: k-means on customer features (three lines of scikit-learn in the notebook: `KMeans(n_clusters=4)` → `fit` → label the customers); plot the segments; *name* each cluster in business words; write the decision each name suggests — the human half of unsupervised learning.
5. The path, chosen: write your ML sequence with dates (consolidate-by, course-by, project-by); the project is Project 4's data with the error analysis as the deliverable; commit the plan to the portfolio repo as `ml-path.md`.

## Further Reading

- Chapter 58 (the other side of "beyond": big data), *The StatQuest Guide to Machine Learning* (Starmer) — the friendliest correct map in print
- scikit-learn's own tutorials — start with the "getting started" page, not the API
