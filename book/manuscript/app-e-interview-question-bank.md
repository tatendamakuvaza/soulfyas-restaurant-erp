# Appendix E: Interview Question Bank

*Appendices — The Cookbook*

> "One hundred questions across the stack — the shapes actually asked, each with a line of guidance pointing at the chapter that owns it. Work them aloud, in batches of ten; the ones that make you hesitate are your revision syllabus."

## Mindset and Honesty (1–8)

**1.** What does a data analyst actually do all day? — *Five moves: question, data, clean, analyse, communicate; a day is these plus stakeholder time (Ch. 1, 45).*
**2.** How do you handle being given a vague request? — *Clarify the decision behind it: "what will you do with the answer?" Half of all requests dissolve or transform (Ch. 54).*
**3.** Your analysis contradicts what the stakeholder believes. What do you do? — *Deliver with unchanged rigour, frame options not verdicts, be ready to be wrong yourself (Ch. 60).*
**4.** What's the difference between an average and a median, and when do you use each? — *Totals logic vs typicality; money is skewed; report both when they disagree (Ch. 22).*
**5.** What questions do you ask of every analysis? — *The five: compared to what, says who, what's missing, what was counted, could it be luck (Ch. 2).*
**6.** Tell me about a time you made a mistake with data. — *Fan-out, detached sort, the missing week — any real error plus the check you now run forever (Ch. 8, 17).*
**7.** How do you know when you can trust a number? — *Reconciled bridge, method known, caveats attached, source named — trust is earned by checks (Ch. 21, 45).*
**8.** What's more important: accuracy or deadline? — *The staged answer: cut scope, never rigor — verified core on time, whole truth dated (Ch. 60).*

## Excel (9–23)

**9.** VLOOKUP vs XLOOKUP vs INDEX-MATCH? — *Exact-match joins; XLOOKUP modern, INDEX-MATCH insertion-proof; know why FALSE matters (Ch. 9).*
**10.** What does #N/A mean and what do you do? — *Three causes: genuine non-match, spelling/type mismatch, broken key — count them, don't hide them (Ch. 9).*
**11.** Walk me through building a PivotTable. — *Select, Insert, four shelves; values re-aimable; % of total; drill by double-click (Ch. 10).*
**12.** What's the difference between SUMIF and SUMIFS? — *One criterion vs pairs of (range, criterion); order of arguments flips (App. B).*
**13.** How would you clean a column with inconsistent text entries? — *TRIM/CLEAN/case unification on a helper, paste values back, count before/after (Ch. 8).*
**14.** How do you handle duplicates in a spreadsheet? — *COUNTIF flag, then decide: dedupe on which key, keep which copy — documented (Ch. 8).*
**15.** Explain absolute vs relative references. — *The $ anchors; F4 cycles; ranges drift when copied unless anchored (App. B).*
**16.** What Excel function would you use for a weighted average? — *SUMPRODUCT/SUM — and ask "weighted by what?" before answering (Ch. 22).*
**17.** How do you find outliers in Excel? — *QUARTILE + 1.5×IQR fence; never silently delete; investigate, report separately (Ch. 12).*
**18.** What's the difference between STDEV.S and STDEV.P? — *Sample (n−1) vs population (n); your default is .S (Ch. 23).*
**19.** Text dates are being read as text. Fix? — *DATEVALUE/Text-to-Columns, ISO format, check the locale, reformat real dates (Ch. 8).*
**20.** How would you show month-over-month change? — *Pivot by month, % difference from previous — or LAG in SQL; name the tool by audience (Ch. 10, 19).*
**21.** What's your reconciliation habit after a lookup join? — *Totals before = totals after; row counts; the fan-out check (Ch. 9, 17).*
**22.** Conditional formatting for data quality — how? — *Duplicate values, blank-cell rules, above-fence: the liturgy made visible (App. B).*
**23.** When would you NOT use Excel? — *Beyond ~1M rows, multi-table joins at scale, reproducibility requirements, automation — the honest limits (Ch. 14, 58).*

## SQL (24–43)

**24.** Write: total revenue by payment type. — *GROUP BY with SUM and COUNT side by side; sort by revenue (Ch. 16).*
**25.** Write: top 3 items by revenue per category. — *Aggregate → ROW_NUMBER() OVER (PARTITION BY) → filter rn ≤ 3 — the interview classic (Ch. 19).*
**26.** Find the second-highest sale. — *OFFSET/LIMIT or MAX-below-MAX or DENSE_RANK=2; mention ties (Ch. 52).*
**27.** INNER vs LEFT JOIN — when each? — *Matches only vs all-left-rows; the choice is an analysis decision, not syntax (Ch. 17).*
**28.** How do you find customers with zero orders? — *LEFT JOIN + WHERE right IS NULL — the anti-join (Ch. 17).*
**29.** What is a fan-out and how do you catch it? — *Keys repeating both sides; row counts before/after, totals reconcile, aggregate-then-join (Ch. 17).*
**30.** WHERE vs HAVING? — *Rows before grouping vs groups after; execution order FROM→WHERE→GROUP→HAVING→SELECT (Ch. 16).*
**31.** What does NULL mean? How do you test it? — *Unknown, not zero; IS NULL; fails every comparison; COUNT(*) vs COUNT(col) (Ch. 15).*
**32.** Explain a CTE and why you use one. — *Named step; readable pipelines; testable layers; reusable — the professional default (Ch. 18).*
**33.** Write: each category's % of total revenue. — *Grouped CTE + SUM() OVER() or grand-total CTE; 100.0 decimal division (Ch. 18).*
**34.** Running total by month? — *SUM() OVER (ORDER BY ...); tie-break key; the frame if partial (Ch. 19).*
**35.** Month-over-month change? — *LAG(revenue) over ordered months; pct with decimal division; first row NULL is honest (Ch. 19).*
**36.** Deduplicate a table keeping the latest row per id. — *ROW_NUMBER() PARTITION BY id ORDER BY date DESC, keep rn=1 (App. A).*
**37.** What's a window function vs GROUP BY? — *Annotate every row vs collapse to one row per group (Ch. 19).*
**38.** A query is slow. What do you do? — *Read the shape (sargability), EXPLAIN the plan, know what an index does (Ch. 20).*
**39.** What does this inherited query do? (given a multi-join) — *Diagram FROM first: tables, lines, join types, which side is many (Ch. 17, 20).*
**40.** LEFT JOIN with a WHERE on the right table — what happens? — *Silently becomes INNER; move the condition into ON or accept it deliberately (Ch. 20).*
**41.** Write: count of sales per customer, including customers with none. — *LEFT JOIN from customers + COUNT(s.sale_id) — the column count, not COUNT(*) (Ch. 16–17).*
**42.** NULL in NOT IN — the trap? — *NOT IN against a set containing NULL returns nothing; use NOT EXISTS (App. A).*
**43.** How do you document SQL? — *Filename = question; header with purpose/author/expected totals; comment the why; version (Ch. 20).*

## Statistics (44–63)

**44.** What's a p-value, in one sentence? — *Probability of evidence this strong if nothing were happening; not the probability the null is true (Ch. 26).*
**45.** 0.05 — magic? — *Convention, chosen in advance; 0.06 is weaker-labelled evidence, not failure (Ch. 26).*
**46.** Statistical vs practical significance? — *Not-noise vs worth-money; big n makes trivial significant; report effect sizes (Ch. 26).*
**47.** Type I vs Type II error? — *False alarm vs missed effect; α guards the first; n drives the second (Ch. 26).*
**48.** When do you use a paired test? — *Same units measured twice; test the differences; pairing cancels noise (Ch. 26).*
**49.** Chi-square — what's it for, and its assumption? — *Association between categories; expected counts ≥ 5 per cell, else Fisher's exact (Ch. 27).*
**50.** Correlation is 0.9. What can you conclude? — *Strong straight-line association; three explanations; not causation without an argument (Ch. 28).*
**51.** What's R²? — *Share of y's variance the line explains; 0.76 = 76% tracked by x (Ch. 28).*
**52.** What's a confidence interval, and how do you read it? — *x̄ ± 2×SE; the *procedure* captures truth in 95% of uses — and "is it narrow enough to decide?" (Ch. 25).*
**53.** Standard deviation vs standard error? — *Individuals vs statistics; "sales vary by 12" vs "the mean is wrong by ~1.7" (Ch. 25).*
**54.** Why does the CLT matter? — *Means of 30+ are near-normal whatever the raw shape; skew in, bell out (Ch. 25).*
**55.** What's the Central Limit Theorem's practical use? — *Intervals and tests on averages from skewed data — daily takings from skewed baskets (Ch. 25).*
**56.** Your data is right-skewed. What do you report? — *Median headline, fence-based outliers, percentiles; or transform; name the shape (Ch. 22–23).*
**57.** Multiple comparisons — why care? — *20 tests on nothing yields one "significant"; declare questions first (Ch. 26).*
**58.** Sampling bias example from your own work? — *The in-shop survey missing Sunday-stayers; refusal rates; the frame declared (Ch. 27, 47).*
**59.** What's selection bias in a metric? — *Loyalty members self-selected; gym-club salad-eaters; measured instrument vs world (Ch. 28, 59).*
**60.** Regression slope interpretation? — *Effect of x per unit, holding others constant — "a dollar costs a bottle" (Ch. 28).*
**61.** Why not extrapolate the line? — *No data there; the line doesn't know; −3.7 bottles is a confidence lie (Ch. 28).*
**62.** What's a bootstrap? — *Resample with replacement, recompute, take the spread — CIs for anything (Ch. 36).*
**63.** Which test: compare churn rate between two plans? — *Two proportions — chi-square (or z-test of proportions); state expected counts (App. D).*

## Python (64–78)

**64.** Why pandas for analysis? — *Reproducible pipeline, scale beyond sheets, joins/stats/charts in one place; automation compounding (Ch. 30).*
**65.** DataFrame vs Series? — *The table vs one labelled column; df is a dict of Series (Ch. 33).*
**66.** How do you handle missing values in pandas? — *Classify the mechanism first; drop (MCAR), impute-with-flag (MAR), bound+declare (MNAR) (Ch. 60).*
**67.** merge — what's `how=` doing? — *Join direction: left keeps all left rows; indicator=True gives the anti-join (Ch. 34).*
**68.** groupby-agg pattern, write it. — *`df.groupby(k)[v].agg([...])`; named aggregations are the aliases (Ch. 34).*
**69.** What's vectorisation? — *Column-at-once operations at C speed; loops explain, one-liners work (Ch. 32).*
**70.** When would you use .apply? — *Last resort: row-wise logic with no column idiom; slow and less searchable (Ch. 33).*
**71.** How do you make a month column from dates? — *`.dt.to_period("M")`; parse with to_datetime at load; .dt accessor is the cleaning kit (Ch. 33).*
**72.** Resample vs groupby for time? — *Calendar-aware grouping: ME/W/Q; unequal months handled (Ch. 34).*
**73.** Rolling average and MoM in pandas? — *`.rolling(7).mean()`; `.pct_change()` — LAG pre-assembled (Ch. 34).*
**74.** What's a notebook's biggest danger? — *State: cells run out of order; Restart & Run All before trusting (Ch. 30).*
**75.** How do you test your pandas analysis? — *Reconcile against a second route (SQL, sheet); assert on known totals; small cases by hand (Ch. 33–34).*
**76.** t-test in Python? — *`stats.ttest_ind(a, b, equal_var=False)` — Welch; read t, p; report effect+CI (Ch. 36).*
**77.** Your script must run monthly unattended. What changes? — *Checks with consequences, config constants, dated outputs, logs, fail loudly (Ch. 37).*
**78.** What is `assert` doing in your pipeline? — *The abort guard: nulls, orphans beyond tolerance — never report from untrusted data (Ch. 37).*

## Power BI and Dashboards (79–88)

**79.** Calculated column vs measure? — *Row label vs in-context number; "how much" = measure (Ch. 40).*
**80.** What is filter context? — *The rows visible to the measure; clicks are WHERE clauses through the model (Ch. 40).*
**81.** What does CALCULATE do? — *Evaluates a measure in a context you steer — the hand-written WHERE (Ch. 40).*
**82.** Explain a star schema. — *Facts in the middle, dimensions around; why BI models are fast and sane (Ch. 39).*
**83.** Many-to-many warning — what's it telling you? — *Fan-out risk; the design wants a bridge table (Ch. 39).*
**84.** Why a date table? — *Time as a dimension; time intelligence needs a marked calendar (Ch. 39).*
**85.** Your dashboard is slow. Diagnose. — *Too much shown, repeated heavy measures, too many visuals — Performance analyzer (Ch. 41).*
**86.** How do you keep a dashboard honest? — *Data-age stamp, reconciliation card, checks page, caveat sentences (Ch. 41, 43).*
**87.** Dashboard vs report — how do you choose? — *Recurring slices vs one argued finding; the brief decides (Ch. 43).*
**88.** How would you present findings to non-analysts? — *Headline first, movement, stories with caveats, one interaction, the ask (Ch. 43).*

## Projects and Behaviour (89–100)

**89.** Walk me through a project you're proud of. — *STAR, 90 seconds, action-majority, the number in the result (Ch. 53).*
**90.** Tell me about a time you automated something. — *An afternoon → twenty minutes; checks that abort; the before/after is the punchline (Ch. 37).*
**91.** A time an analysis changed a decision. — *The save-campaign design; measurable, budgeted, honest about cause (Ch. 46).*
**92.** A time you found something others missed. — *The say/do gap; 41% reframed to 15–20% by joining to behaviour (Ch. 47).*
**93.** How do you scope a take-home? — *Question first, cut to the deciding finding, ship the honest limits, deliverables foldered (Ch. 45, 53).*
**94.** "Isn't this just seasonality?" — hostile Q&A. — *Receive as a gift; show the split; the three explanations in action (Ch. 53).*
**95.** What data-quality checks do you run habitually? — *The liturgy: counts, dup keys, orphans, NULLs, the bridge — every load (Ch. 21).*
**96.** How do you handle changing requirements mid-project? — *Scope arithmetic aloud: adds X days or replaces Y — costs visible (Ch. 60).*
**97.** What's your experience with SPSS/Stata? — *The translation table answer: statistics transferable, syntax a week not a year, artefacts as proof (Ch. 29).*
**98.** Why this company / this role? — *Their domain + your portfolio's nearest project; specific duties, specific evidence (Ch. 50–51).*
**99.** Where do you want to be in five years? — *The fork answered honestly: craft depth or team — with the compounding habits (Ch. 56).*
**100.** What would you do in your first 90 days here? — *The three maps, the first deliverable, the quick win, the self-review — offer it as a plan (Ch. 54).*

## Using the Bank

Work it in batches of ten, *aloud* — the fluency being trained is the spoken sentence, not the known answer. The hesitation list is your revision syllabus: each hesitated question names a chapter; reread that chapter's Key Takeaways, then re-attempt the question cold a week later. Before interviews, rerun the sections matching the round (SQL screens → 24–43; a stats-heavy role → 44–63; the behavioural hour → 89–100 with your own STAR stories beside each). The bank's promise is the book's promise inverted: 62 chapters taught the method; 100 questions prove you can *say* it — which is the interview's whole game.
