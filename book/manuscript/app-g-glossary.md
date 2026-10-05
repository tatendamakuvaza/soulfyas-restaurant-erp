# Appendix G: Glossary

*Appendices — The Cookbook*

> "Every term this book taught, one line each — the definitions as the chapters used them, not as dictionaries do. Bold cross-references point to their home chapters."

**ad-hoc analysis** — one-off questions answered by hand, as opposed to automated reporting; the recurring ad-hoc is a pipeline waiting to be built (Ch. 54, 60).

**aggregate** — a function that collapses many rows into one number: COUNT, SUM, AVG, MIN, MAX (Ch. 16).

**aggregation, conditional** — SUM(CASE WHEN...) — building columns-of-conditions in one pass (App. A).

**alias** — a short name for a table (`sales s`) or a computed column (`AS revenue`) (Ch. 17).

**α (alpha)** — the significance level chosen *before* testing; the standard of proof; 0.05 by convention (Ch. 26).

**anti-join** — LEFT JOIN + WHERE right-key IS NULL; the rows with no match (Ch. 17).

**appendix-driven development** — not a real term; if you looked it up, you are thorough, and that is the trait (Ch. 2).

**API** — a programmatic doorway into a system or data source (Ch. 44, 57).

**ATP/ATS** — the systems that parse and screen CVs; mirror honest keywords, keep layouts plain (Ch. 51).

**average (mean)** — the balance point; the only typical that interacts correctly with totals (Ch. 22).

**average, weighted** — Σ(value × weight)/Σ(weight); every "average" hides a choice of weights (Ch. 22).

**baseline** — the comparison a number needs to mean anything; "compared to what?" (Ch. 2, 52).

**bias (statistics)** — systematic error in one direction; enters at sample, measurement, or model (Ch. 59).

**BI (business intelligence)** — the dashboarding discipline: models, measures, pages, refresh (Part VI).

**bookmark** — a saved state of a dashboard page (filters, visibility) (Ch. 41).

**bootstrap** — resample with replacement, recompute, take the spread; CIs for anything (Ch. 36).

**bridge total** — a known total reconciled at every step of a pipeline; the trust anchor (Ch. 21).

**calendar/date table** — a marked dimension of dates that makes time intelligence possible (Ch. 39).

**CALCULATE** — DAX's context-steering function; a hand-written WHERE for a measure (Ch. 40).

**cardinality** — the one-to-many shape of a relationship; the model's fan-out guard (Ch. 39).

**case study note** — the 150-word portfolio atom: situation, work, finding, impact, limits (Ch. 45).

**caveat** — the honesty attached to a claim at the moment of claiming; travels with the number (Ch. 13).

**Chebyshev's inequality** — the shape-free promise: ≥75% within 2 sd, whatever the distribution (Ch. 24).

**chi-square (χ²)** — the association test for categories; expected counts ≥ 5 per cell (Ch. 27).

**churn** — a customer stopping, by a stated definition (no purchase in N days) (Ch. 46).

**CLT (Central Limit Theorem)** — means of 30+ are near-normal whatever the raw shape (Ch. 25).

**cohort** — a group sharing a start; the unit that keeps time honest (Ch. 46).

**confidence interval (CI)** — estimate ± 2×SE; the procedure captures truth in 95% of uses (Ch. 25).

**confounder** — the third variable driving two others; the reason correlation ≠ causation (Ch. 28).

**confusion matrix** — predicted vs actual: a cross-tab of a classifier's performance (Ch. 57).

**correlation (r)** — straight-line association strength, −1 to +1; not causation (Ch. 28).

**COUNT(*) vs COUNT(column)** — all rows vs non-NULL rows; the difference is an analysis (Ch. 15).

**cross-tab** — counts of two categorical variables; the pivot's statistical soulmate (Ch. 27).

**CTE (Common Table Expression)** — a named query step (`WITH monthly AS (...)`); the readable pipeline (Ch. 18).

**dashboard** — an interactive page of live measures answering recurring questions (Part VI).

**data dictionary** — the documentation of columns and their meanings; read before touching (Ch. 44).

**Data age stamp** — the freshness marker every honest dashboard displays (Ch. 41).

**data frame (pandas)** — the programmable table; a dict of Series sharing an index (Ch. 33).

**dbt** — SQL-as-modules: versioned, tested transformations; analytics engineering's tool (Ch. 58).

**DAX** — Power BI's formula language; measures evaluated in filter context (Ch. 40).

**degrees of freedom (df)** — the sample's contribution to a test's distribution (Ch. 26, 27).

**descriptive statistics** — numbers that describe what is (typical, spread, shape) without concluding (Ch. 22).

**dimension table** — the who/what/where/when context around a fact table; star schema's points (Ch. 39).

**drillthrough** — right-click into a detail page, pre-filtered; summary to evidence (Ch. 41).

**drill-down** — exploding a summary back into its rows (double-click a pivot number) (Ch. 10).

**DuckDB** — the analytical database engine that queries files directly; the laptop warehouse (Ch. 61).

**effect size** — how big the difference is, with its interval; what business decisions need (Ch. 26).

**empirical rule (68–95–99.7)** — the bell's promise; needs the bell to be true (Ch. 23).

**evaluation context** — the rows a DAX measure can see; clicks become contexts (Ch. 40).

**Excel** — the universal first tool; the whiteboard where everyone starts (Part II).

**expected count (E)** — what a chi-square cell would contain under independence (Ch. 27).

**experiment** — deliberately changing X to watch Y; the licence for causation claims (Ch. 28).

**fact table** — the events in the middle of a star schema; many rows, the numbers (Ch. 39).

**fan-out** — the join trap: keys repeating on both sides multiply rows and totals (Ch. 17).

**feature** — an input column for a model; derived features are the analyst's crafted inputs (Ch. 57).

**field** — a column, in database/BI vocabulary (Ch. 14).

**filter context** — the WHERE a measure evaluates inside (Ch. 40).

**filter propagation** — filters flowing across relationships through the model (Ch. 39).

**five-number summary** — min, Q1, median, Q3, max; the fastest honest portrait (Ch. 12).

**five-second rule** — what a page must communicate in a glance (Ch. 41).

**frame (window)** — the rows a window function can see: 6 PRECEDING, CURRENT ROW... (Ch. 19).

**free stack** — the $0 toolkit: Calc, SQLite, jamovi, Python, Power BI Desktop, GitHub (Ch. 61).

**GDPR / POPIA / data-protection acts** — the laws built on consent, purpose, minimisation (Ch. 59).

**gateway** — the on-premises agent that lets a cloud service refresh from local sources (Ch. 43).

**GROUP BY** — "for each what"; the aggregate habit (Ch. 16).

**HAVING** — filtering groups after they are built; WHERE cannot (Ch. 16).

**histogram** — the shape of one column; read before any average (Ch. 23).

**honesty rules (the three)** — average ≠ the answer; correlation ≠ causation; sample ≠ population (Ch. 2).

**hypothesis test** — the courtroom for a number: H0 "nothing happened", evidence, surprise score (Ch. 26).

**imputation** — filling missing values, with flags and disclosure; model the mechanism first (Ch. 60).

**INDEX-MATCH** — the insertion-proof lookup pair (Ch. 9).

**index (database)** — the lookup structure that makes key-seeks fast (Ch. 20).

**inner join** — matches only; amputates the unmatched (Ch. 17).

**IQR** — Q3 − Q1; the robust spread; powers the outlier fence (Ch. 12, 23).

**join** — match the keys, bring the facts across, check the totals (Ch. 9, 17).

**JSON** — the web's data format; appears when APIs feed your pipelines (Ch. 44).

**Kaplan-Meier / survival curve** — the fraction surviving to each time k (Ch. 46).

**key (primary/foreign)** — the identifier that makes relationships possible (Ch. 14).

**lag/lead (SQL)** — the previous/next row's value; month-over-month's engine (Ch. 19).

**leakage** — features knowing the future; the silent killer of ML results (Ch. 57).

**LEFT JOIN** — keep all left rows, fill the unmatched with NULLs (Ch. 17).

**lineage** — the clickable path from visual to measure to table to source (Ch. 38).

**loading liturgy** — row counts, key census, orphans, totals, NULLs — every load, forever (Ch. 21).

**log (the)** — the record of cleaning decisions and method notes; the senior-looking part (Ch. 13).

**many-to-many** — keys repeating both sides; fan-out waiting to fire; bridge tables resolve it (Ch. 17).

**margin of error** — the ± of a survey estimate; ±2×SE of a proportion (Ch. 25, 27).

**MAR / MCAR / MNAR** — the three missingness mechanisms and their matching responses (Ch. 60).

**marketplace of questions** — not a term either; but your questions ledger is an asset (Ch. 2, 44).

**matplotlib** — Python's chart engine; the second pen this book taught (Ch. 35).

**mean** — see average; the totals-logic typical (Ch. 22).

**measure (DAX)** — a named formula evaluated in context; "how much" lives here (Ch. 40).

**median** — the middle value; the robust typical for money (Ch. 12, 22).

**merge (pandas)** — the join, with how= and indicator= (Ch. 34).

**metric** — a defined number worth tracking; always ask what it really measures (Ch. 59).

**mode** — the most common value; the only typical for categories (Ch. 22).

**model (data model)** — tables + relationships; where BI correctness is decided (Ch. 39).

**NULL** — unknown, not zero; fails every comparison; test with IS NULL (Ch. 15).

**n** — the count; the denominator; what every percentage owes its reader (Ch. 22, 27).

**notebook (Jupyter)** — code, output, prose in one reproducible document (Ch. 30).

**one-pager** — the report format: headline, findings with recommendations, appendix (Ch. 13).

**orchestrator** — the scheduler of pipelines at scale (Airflow and kin) (Ch. 37, 58).

**outlier** — beyond the fence; investigate, report separately, never silently delete (Ch. 12).

**p-value** — probability of evidence this strong if nothing were happening; a surprise score (Ch. 26).

**paired test** — same units measured twice; test the differences (Ch. 26).

**parameter vs statistic** — the population's fixed truth vs the sample's varying estimate (Ch. 25).

**pandas** — Python's analysis library; the engine of Part V (Ch. 33–34).

**partition (window)** — the group-within-which a window function restarts (Ch. 19).

**Pearson r** — the correlation coefficient (Ch. 28).

**percentile** — the value below which p% of data lies; the shape-free ruler (Ch. 24).

**pivot table** — totals of something for each something else, without formulas (Ch. 10).

**p-hacking** — running many tests until one is significant; prevented by declaring questions first (Ch. 26).

**pipeline** — inputs → checks → analysis → outputs; runs identically, unattended (Ch. 37).

**population** — every unit you want to speak about; you never see it (Ch. 25).

**Power Query** — Power BI's recorded, replayable cleaning editor (Ch. 39).

**practice lab** — the end-of-chapter exercise set; where the book actually happens (every chapter).

**prediction interval** — the honest range around a line's forecast (Ch. 28).

**principal vs manager** — the two senior ladders: hardest problems vs people and priorities (Ch. 56).

**purpose limitation** — data collected for X is used for X (Ch. 59).

**q (quartile)** — the 25th/50th/75th percentiles (Ch. 12).

**query pack** — the folder of saved, headered queries that regenerates a report (Ch. 21).

**R²** — the share of y's variance the line explains (Ch. 28).

**rank trio** — ROW_NUMBER (exact N), RANK (ties, gaps), DENSE_RANK (ties, no gaps) (Ch. 19).

**reconciliation** — checking a number against a second route to it; the trust habit (Ch. 8, 21).

**refresh (scheduled)** — the data updating itself on a timer, with a gateway where needed (Ch. 43).

**regression** — the line of best fit; the slope is the finding (Ch. 28).

**resample (pandas)** — calendar-aware grouping of time series: ME, W, Q (Ch. 34).

**residual** — the vertical miss between point and line; where the next question lives (Ch. 28).

**rolling window** — the moving neighbourhood: 7 PRECEDING and the rest (Ch. 19, 34).

**row context** — the single row a calculated column sees (Ch. 40).

**running total** — SUM OVER (ORDER BY ...); the cumulative line (Ch. 19).

**R² vs r** — the line's share vs the association strength; r² = R² for one predictor (Ch. 28).

**sample** — the part you can see; the argument from seen to unseen is statistics (Ch. 25).

**sampling distribution** — what a statistic would say across re-runs (Ch. 25).

**sargable** — a filter the engine can seek (bare columns), not scan (functions on columns) (Ch. 20).

**scatter plot** — two numeric variables, one point each; where relationships live (Ch. 11, 28).

**schema** — the structure: tables, columns, types, relationships (Ch. 14).

**SE (standard error)** — s/√n; the typical distance between estimate and truth (Ch. 25).

**seasonality** — the repeating calendar pattern; the baseline for honest comparisons (Ch. 34, 53).

**self-selection** — when the members chose themselves (loyalty schemes, gyms, surveys) (Ch. 28).

**sensitivity analysis** — computing the answer under best/worst assumptions; MNAR's honest response (Ch. 60).

**SERIES (pandas)** — one labelled column; the DataFrame's building block (Ch. 33).

**share of total** — each group's slice with its denominator declared (Ch. 18).

**significance vs importance** — not-noise vs worth-money; report effect sizes (Ch. 26).

**skew** — the lopsidedness; right-skew is money's shape (Ch. 23).

**slicer** — the reader-facing filter; a click that becomes a WHERE (Ch. 38, 41).

**small multiples** — the same chart per group, shared axes; comparison by construction (Ch. 42).

**snowflake vs star** — the warehouse shapes; star is the analyst's default (Ch. 39).

**SQL** — the language of data; fifty years the lingua franca (Part III).

**SPSS / Stata** — the classic statistics packages; menus vs do-files (Ch. 29).

**squared error** — deviation²; severity plus positivity (Ch. 23).

**standard deviation (s / σ)** — the typical distance from the mean; individuals' spread (Ch. 23).

**standardisation (z)** — (x − x̄)/s; units dissolved (Ch. 24).

**STAR interview method** — Situation, Task, Action, Result; 90 seconds (Ch. 53).

**star schema** — facts in the middle, dimensions around (Ch. 39).

**substring/slice** — text by position: substr, [start:end], LEFT/MID/RIGHT (Ch. 15, 31).

**supervised learning** — models fitted to labelled examples: regression, classification (Ch. 57).

**t-test** — the mean-comparison courtroom; Welch's version is the default (Ch. 26).

**take-home** — the interview analysis task; graded on craft and honesty, not sophistication (Ch. 52).

**three explanations** — coincidence, confounding, causation; the correlation triage (Ch. 28).

**time intelligence** — DAX's date-aware calculations: MoM, YTD, same-period-LY (Ch. 40).

**top-N per group** — aggregate, rank, filter; the interview classic (Ch. 19).

**tool-agnosticism** — the method transfers; the accents are cheap (Ch. 29, 61).

**TRIM/clean** — killing the whitespace and case ghosts before they become joins' #N/As (Ch. 8).

**t-test, paired** — see paired test.

**Type I / Type II error** — false alarm vs missed effect (Ch. 26).

**unsupervised learning** — structure without labels: clustering, reduction (Ch. 57).

**validation (cross-)** — rotating the train/test split so the grade is not luck (Ch. 57).

**VAR / RETURN** — DAX's named intermediate steps; CTE habits in formula form (Ch. 40).

**variable (Python)** — a labelled box; names mean things; snake_case (Ch. 31).

**vectorisation** — column-at-once operations; loops explain, one-liners work (Ch. 32).

**VLOOKUP / XLOOKUP** — the spreadsheet join; exact match always (Ch. 9).

**warehouse (data)** — the rented, columnar, cloud-scale database: BigQuery, Snowflake (Ch. 58).

**weighted mean** — see average, weighted.

**window function** — annotate every row without collapsing any (Ch. 19).

**XLOOKUP** — see VLOOKUP; the modern form (Ch. 9).

**z-score** — the standard ruler; +2.0 is a once-in-twenty value if the bell holds (Ch. 24).
