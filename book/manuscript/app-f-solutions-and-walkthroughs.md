# Appendix F: Solutions and Walkthroughs

*Appendices — The Cookbook*

> "Attempt the lab first — the struggle is the lesson. Then come here: full walkthroughs for the projects' key labs, the answers with their numbers, the common wrong turns, and the reconciliations that prove each answer. Selected chapter labs included where beginners most often stall."

## How to Use This Appendix

Do not read ahead of your attempt. The labs are where the book actually happens; a solution read instead of attempted is a chapter unlearned. Use this appendix three ways: to *unstick* (read only the first step, then return to your work); to *check* (finish, then compare numbers and reasoning); and to *repair* — when your answer differs, find where the paths diverge, because the divergence is a chapter you half-learned. Numbers below are from the book's generated datasets (your copies will match if you use the repo's files; the *methods* match always).

## Part II — Excel (Chapters 6–13)

### Ch. 8, Lab 3 — the three EcoCash spellings

**The trap:** cleaning with `=UPPER(D2)` fixes case but not the trailing space — "ECOCASH " ≠ "ECOCASH" and the pivot still shows two rows. **The full move:** a helper column `=TRIM(CLEAN(UPPER(D2)))`, filled down; then *paste-as-values* over the original column; then delete the helper. **The check:** `COUNTIF(D:D,"ECOCASH")` before and after — before: three values totalling 6,420; after: one value, same total. If the total moved, you deleted rows instead of cleaning them: undo.

### Ch. 13, Lab 1 — the one-page report

The walkthrough is Chapter 13.3's template filled with your numbers. **The five most common wrong turns, in order of frequency:** (1) the headline is a table of contents ("Monthly Report — June") instead of a finding — fix by writing the oil sentence there instead; (2) a recommendation without a measurement ("improve Sundays" — say *what* number, by *when*); (3) charts with furniture titles — every title should state the finding; (4) the caveat detached (a "limitations" paragraph at the bottom nobody reads — attach caveats to their claims, sentence by sentence); (5) two pages "because there was a lot" — the appendix sheet exists precisely so the page does not have to grow. **The check:** the readability test (Lab 2) — a friend recalls the three findings after ninety seconds or the page has failed, whatever it contains.

## Part III — SQL (Chapters 14–21)

### Ch. 17, Lab 4 — fan-out on purpose

**Build:** create `customer_discounts(customer_id, discount_note)`; insert two rows for member C0102. **Observe:** `SELECT COUNT(*) FROM sales` (their true count) vs the count after `JOIN customer_discounts` — every one of that member's ~180 sales now matches *both* discount rows: ~180 extra rows, and `SUM(amount)` inflated by exactly that member's revenue once over. **Fix:** aggregate first —

```sql
WITH one_row_per_customer AS (
    SELECT customer_id, COUNT(*) AS n_offers
    FROM   customer_discounts GROUP BY customer_id)
SELECT ... FROM sales s
LEFT JOIN one_row_per_customer o ON o.customer_id = s.customer_id;
```

**The numbers to log:** revenue before (54,013.50), revenue doubled at the join (+~1,940, the member's lifetime spend), revenue restored after the fix. Three numbers; one permanent instinct.

### Ch. 21, Q4 — the price-rise answer

The question: what did the month-9 rise actually do? **The shape:** monthly oil quantity, before vs after, as a paired comparison. **The walkthrough:** CTE 1 — oil sales only, monthly, count and sum; CTE 2 — the price from `suppliers.last_price_change` joined by month; then compare averages: before ≈ 3.1 bottles/customer-month, after ≈ 1.8 — a −1.3 change; the paired t on per-item differences (Ch. 26) gives t ≈ −4.6, p ≈ 0.0008. **The common wrong turn:** comparing *revenue* before/after and concluding "revenue fell 40%" — true but not the answer; revenue = price × quantity, and the price *rose*: the collapse is quantity-led, which recommends a *different* action (cheaper brand trial) than a price-cut reflex. **The sentence to ship:** "The 0.80 price rise cut per-customer quantity from 3.1 to 1.8 bottles/month (t = −4.6, p < 0.001); the wholesaler's increase was not passed through volume — see the shelf trial proposal."

## Part IV — Statistics (Chapters 22–29)

### Ch. 25, Lab 1 — the CLT by hand

**The setup:** 200 samples of 50 sales; the x̄ of each. **What you should see:** the raw `amount` histogram — a right-skewed spike near 5 with a long tail to 400+; the sample-means histogram — a symmetric bell centred on 8.42 with sd ≈ 1.7 (= s/√50 ≈ 12.10/7.07, the SE formula *confirmed by your own simulation*). **The common wrong turns:** sampling *with replacement from the sample means* (nonsense — resample the data); forgetting to reset the sample each draw (one giant drifting sample); and reading the means' spread as "the spread of sales" (it is the spread of *estimates* — the whole point). **The caption pair to paste in your log:** "Left: baskets — skewed, whales visible. Right: averages of 50 — a bell. The Central Limit Theorem, demonstrated in ten minutes."

### Ch. 26, Lab 1 — the Sunday test, reconciled

By hand: group stats → SE → t → verdict, exactly as Appendix D's worked example (t ≈ −18.4, p < 0.0001). **Then by tool:** `=T.TEST(sun_range, week_range, 2, 3)` returns the p alone — *write the t yourself*; the tool's job is confirmation, not understanding. **The reconciliation that matters:** your hand-computed t vs the ToolPak/SPSS output to three decimals. **The common wrong turn:** pooling all days into one giant two-group test *including* the promotion Sundays (a mixture) — state your exclusions, always.

### Ch. 28, Lab 1 — the correlation paragraph

**The number:** r ≈ −0.87, p < 0.001 on 18 months of oil. **The paragraph structure** (five clauses, each one clause — this is the template for every correlation you ever report): the correlation with its test; the fitted line's slope as a sentence; the R² as a share; the mechanism making causation plausible (a known wholesaler increase — not a mysterious co-drift); and the trial that would close the argument. **The common wrong turns:** reporting r and stopping (no size — the slope is the business number); claiming causation outright (confounders unexamined — the harvest year, rivals' prices); and extrapolating the line to price 9 (the impossible −3.7 bottles — Appendix D's regression-table reading covers why the CI widens at the edges).

## Part V — Python (Chapters 30–37)

### Ch. 34, Lab 1 — the pivot tour, reconciled

**The work:** five Chapter-10 pivots as one chained block each. **The reconciliation table to build** (this is the lab's actual deliverable):

```text
pivot (workbook)      pandas                SQL               match?
revenue by month      monthly.sum()         GROUP BY month    ✓ to the cent
category revenue      by_cat["revenue"]     GROUP BY category ✓
weekday counts        by_day["n"]           GROUP BY weekday  ✓
payment mix           mix.sum(axis=?)       GROUP BY payment  ✓
member share          member_share.mean()   AVG(is_member)    ✓
```

**The common wrong turns:** a `.mean()` where the workbook had a *share* (different questions — reread the pivot's Values shelf); month as text sorting "2025-10" before "2025-2" (use `to_period`, not string slicing, for ordering); and reconciling *after* adding derived columns (reconcile at each step, or you cannot localise the drift).

### Ch. 37, Lab 1–2 — the pipeline, built and broken

**The build:** Appendix C's full listing, typed. **The failure drill, expected outputs:** (a) deleting one amount from the CSV → the run aborts with "null amounts -- investigate first" *before* writing any output — this is the guard earning its keep; (b) the corrupted key census → abort on duplicates; (c) next month's rows appended → the report regenerates with the new month's headline, and the data-age stamp moves. **The common wrong turns:** catching the SystemExit and continuing anyway (the abort is the feature — never wrap it in try/except-and-carry-on); paths that only work from one directory (use the `Path(__file__).parent` pattern or run from the project root, and note it in the README); and no dated output folder (overwritten history — the folder-per-run *is* the log).

## Part VI — Power BI (Chapters 38–43)

### Ch. 39, Lab 3 — the fan-out museum, BI wing

**The exhibits:** (1) delete the customers relationship → the table visual shows every sale beside every customer (a cross-join's nonsense — massive row inflation, totals wildly wrong); (2) set cardinality many-to-many on a dimension with duplicate keys → the badge warns, and slicers start double-counting; (3) the fix — deduplicate the dimension in Power Query (Group By on the key), restore one-to-many, and watch the reconciliation card return to 54,013.50. **The lesson to write under the screenshots:** in BI tools the fan-out lives in *cardinality badges* and *missing lines* — the model view is the debugging view.

### Ch. 41, Lab 2 — the five-second test, scored

**What friends typically miss first** (in order): the MoM % (too small), the data-age stamp (too grey), the Sunday story (buried bottom-left — move it up). **The iteration rule:** whatever two of three viewers missed, change *position or size* — not colour. Position is comprehension; colour is decoration. **The finished page's benchmark:** revenue (big, top-left), direction (the MoM, beside it, coloured), one story visible without scrolling. If your page passes three consecutive five-second tests unchanged, it is done — ship it.

## Part VII — The Projects (Chapters 44–49)

### Ch. 46, Lab 1–2 — the cohort grid and the bend

**The grid walkthrough:** last-seen per customer (`groupby().max()`), months-since-join per active month (`(month - join_cohort).n`), dedupe customer×age, count, unstack, divide by column 0. **What you should see:** column 0 all 100%; early-cohort rows holding 80%+ through month 10; the founding row thinning from month ~12 (−8%/month planted). **The survival curve's honest annotation:** founding cohort 12-month survival ≈ 0.71 vs newer cohorts ≈ 0.84 — *the drift is value-concentrated*: the founding cohort's CLV (higher spend × longer life) makes its churn the expensive one. **The common wrong turns:** counting *sales* not *customers* in the grid (deduplicate first — the grid counts people); including non-members (no join date — filter `notna`); and averaging retention across cohorts into one number (the entire point is that cohorts differ — never average the time dimension).

### Ch. 47, Lab 3 — the say/do table

**The build:** respondent segments (tier, suburb) joined to till history; within the "definitely would" group, compare Sunday-shopping frequency of *already-Sunday* shoppers vs not. **The expected finding:** ~2.3× — stated intent concentrates among existing Sunday shoppers. **The sentence to ship:** "Stated Sunday intent is real but concentrated where behaviour already agrees; the promotion's *incremental* pull is nearer 15–20% than 41% — the four-Sunday till trial is the decisive test." **The common wrong turn:** reporting the 41% headline straight (it is *true* and *misleading* — the gap between those two words is this project's whole lesson).

## Part VIII–IX — The Hunt and Beyond (Chapters 50–62)

### Ch. 52, Lab 1 — the six SQL shapes, with the self-check line

Model answers are Appendix A: top-N-per-group (#20/#25), second-highest (OFFSET or DENSE_RANK), anti-join (#16), running total (#21), share-of-total (#19), dedupe-keep-latest (#23). **What to add to each in a live interview:** the assumption ("revenue, not units"), and *the check* — "I'd confirm the total didn't double after the join." That one sentence, spoken habitually, is the difference between a candidate who has used SQL and one who ships SQL.

### Ch. 54, Lab 1 — the 90-day plan, a model skeleton

```text
Days 1–30: run the first hour on the main datasets; 8 coffees
  (manager, senior, 3 stakeholders, 2 engineers, the report's readers);
  collect the existing reports + the questions map.
Days 31–60: rebuild the monthly pack with checks (ship 2 days early);
  quick win: automate the "can you pull" of the week
  (state the before: "3 hours" / deliver: "10 minutes").
Days 61–90: runbook tested by handing over one cycle; schedule the
  second-time tasks; answer the top recurring question permanently;
  write the self-review with numbers and book the 90-day meeting.
```

**The common wrong turn:** a plan with no *numbers* (coffees counted, days early, hours saved) — the plan is a deliverable, and deliverables carry numbers. That habit — this book's oldest habit — is what the whole appendix has been demonstrating: *the answer, the method, the wrong turn, the check.*

## Chapter Labs — the Second Wave

### Ch. 2, Lab — the five questions, on a real chart

Take any published business chart. **The audit you should produce** (five lines, one per question): *compared to what* — does the axis start at zero (or flag that it doesn't); *says who* — is the source named; *what's missing* — absent months, an excluded segment, a legend doing surgery; *what was counted* — revenue or transactions, members or sales; *could it be luck* — is a wobble being narrated as a trend. **The most common finding on published charts:** the missing denominator — "80% of customers prefer X" with no n, no comparison, and no interval. That single audit habit, applied weekly to the charts you meet, is the entire mindset chapter in maintenance mode.

### Ch. 5, Lab — the questions ledger, graded

After drafting Tariro's ten questions, grade each on three axes: *decidable* (does a number exist that would settle it?), *affordable* (can this data be had for a reasonable effort?), and *valuable* (does the answer change an action?). The book's arc was built by exactly this grading: the Sunday, oil, and loyalty questions scored high on all three and got Parts; "which suburb has the nicest customers" scored one-of-three and stayed a curiosity. **Your own career version:** keep the graded ledger for your domain — it is Chapter 45's anatomy, pre-step-one.

### Ch. 7, Lab — the order-of-operations trap, built and escaped

The formula `=2+3*4` is 14, not 20; `=(2+3)*4` is 20. The spreadsheet formula that bites analysts: averaging a column of per-row products — `=AVERAGE(B2:B100*C2:C100)` typed hopefully into one cell is an error or a silent wrong (depending on the tool and array settings), while `=SUMPRODUCT(B2:B100,C2:C100)/SUM(C2:C100)` is the weighted mean, correct by construction. **The lesson in one line:** multiplication belongs *inside* the aggregation, not outside it — the same law as SQL's "aggregate, then join".

### Ch. 10, Lab — the refresh lesson, experienced

Change one amount in the source, watch the pivot *not* change, feel the instinct to distrust the tool — then Data → Refresh and watch it catch up. The lesson is not "remember to refresh" (you will remember after this happens in front of someone); it is *the pivot is a view, not a copy* — and every tool in this book has its own version of the stale-view moment (the dashboard browser cache, the notebook's old kernel state, Power BI's "apply pending changes" warning). Write down which tool staled on you and how you noticed; that entry is your future debugging instinct.

### Ch. 15, Lab — the NULL census, read as a story

Two queries: `COUNT(*)` (6,420) and `COUNT(customer_id)` (~4,900). The difference — ~1,520 — is the non-member sales, and the number itself is a finding: *a quarter of sales are anonymous*. The professional next move is a sentence in the report ("member analysis covers 76% of sales; the anonymous quarter is analysed separately"), not a silent filter. **The trap this lab prevents:** the query that quietly drops the NULL rows and reports "average member basket" as if it were the average basket.

### Ch. 18, Lab — the refactor drill, timed

Rebuild your longest flat query as named CTEs, then hand both versions to a friend. Typical timing: the flat version takes 3–4× longer to explain back, and the explainer invents errors in the flat version ("so it filters *after* the join? which join?"). The one-sentence conclusion for your log: *the CTE version is documentation that cannot go stale* — the query documents itself, or it isn't done.

### Ch. 22, Lab — the two-typical gap, explained to a shop owner

Mean 8.42, median 6.50 on the same data. The sentence that lands with a non-analyst: "half of all sales are under 6.50, but the *average* is 8.42 — bulk buyers drag it up; when you plan for the average customer, you're planning for someone bigger than three-quarters of your customers." That sentence — a number, its partner, and the business consequence — is the two-typical gap fully exploited.

### Ch. 24, Lab — the Sunday pre-analysis, closed one chapter early

Mean Sunday takings 2,150, weekday 2,990, sd of daily takings ~640: the gap (840) is 1.3 sd — every single week. Informally: too consistent to be weather, too large to be noise. The z you computed here becomes t = 18.4 in Chapter 26 because *78 Sundays* of consistency compound: the per-week z is modest; the accumulated evidence is overwhelming. **The transferable insight:** one observation's surprise and a year's surprise are different arithmetic — the test exists to compound them honestly.

### Ch. 31, Lab — the error museum, curated

The four regulars, deliberately raised and pasted: NameError (the typo — "customer_id" vs "cutomer_id"), TypeError ("sales: " + 8.42 — the fix is the f-string), SyntaxError (the missing quote), KeyError (asking `sales["Amount"]` — capital A — the data question in disguise). The museum's value is speed: your debugging time drops the moment error messages become *recognised faces* instead of red walls. Add a fifth wing when you meet it — every analyst's museum grows a personal collection.

### Ch. 33, Lab — the dtype surprise, hunted

`info()` on customers shows `joined` as object, not datetime: somewhere in the column a value failed to parse (a blank, a "2025/06/14" slash-date, a note someone typed into a date field). The hunt: `customers[customers["joined"].apply(lambda x: not str(x)[:4].isdigit())]` — find the offenders, fix or exclude them *with a logged decision*, re-parse. **The rule the lab installs:** dtype `object` on a column that should be numeric or date is not a technicality — it is a data-quality finding wearing a type system's clothes.

### Ch. 36, Lab — the three-tool verification, certified

The same Sunday test in spreadsheet, SPSS-or-Stata, and scipy: t to three decimals, p identical to the displayed precision. When all three agree, you have verified not the *answer* but the *understanding* — three implementations of one courtroom, one verdict. The certification line for your log: "t = −18.43 across tools; differences in default Welch/Student handling checked and stated." That single sentence, in an interview, signals a professional upbringing.

### Ch. 42, Lab — the greyscale test

View your dashboard page through a colour-vision simulator (or screenshot → greyscale): the finding that survives is carried by position, label, and length — the honest carriers. What disappears was carried by colour alone — the lie you didn't intend. Typical casualty: the red/green conditional formatting on the MoM card, which in greyscale reads as two identical grey numbers — fix by adding the sign character (+/−) or an arrow, which carries the meaning redundantly. Accessibility fixes are almost always *clarity* fixes for everyone: the labelled, signed, positioned chart is simply the better chart.

### Ch. 44, Lab — the first hour, on national data

The typical surprises in your first real government dataset: totals that don't match the published summary (revisions, exclusions — a documentation read resolves it); codes as numbers (region "1"–"10" — keep them strings, map them with the codebook); implicit missing years (the survey skipped 2020 — a limitation to declare, not a gap to fill). The first hour's real lesson: *documentation is data too* — the methodology PDF you skim is where the dataset tells you its secrets.

### Ch. 49, Lab — the link-check that found the dead exhibit

The monthly link-check (first Friday) on a portfolio typically finds: the screenshot whose file was renamed, the notebook link that points to a local path, and — the expensive one — the project whose README says "report coming soon" from three months ago. Each is a five-minute fix on discovery and a silent credibility leak until then. The portfolio's real maintenance law: *links rot faster than skills* — schedule the check, or the shelf lies about you while you sleep.

### Ch. 55, Lab — the first pitch, whatever the outcome

You approached one real prospect with one specific offer. Outcomes, all four of them, are wins: *yes* — your first engagement, price it at the slightly-uncomfortable number; *no* — log the reason (wrong product? wrong time? wrong price?) — that reason is your market research; *not now* — a warm follow-up date, which is a pipeline, which is the entire discipline; *silence* — also data (the offer wasn't specific enough; make the next one narrower). The freelancer's ledger converts all four into progress; the amateur only counts the yeses.

### Ch. 61, Lab — the switch cost, measured

You rebuilt Project 1's one-pager in a tool you had never used, and it took — typically — 60–70% of the original time, most of it spent on the two or three idioms the new tool names differently. That measured number is your permanent answer to "do you know tool X?" — *the method transfers in a weekend; here is the rebuild I timed.* Tool-anxiety dies at that moment, and employers can hear that it has.

## The Common Wrong Turns, Consolidated

Across every lab in this appendix, five wrong turns account for most of the struggle: **missing parentheses** (in pandas booleans, in spreadsheet formulas, in SQL's AND/OR chains — the fix is always the same: wrap the units of meaning); **the unexamined denominator** (percentages, averages, shares — ask of what, weighted by what); **the silent filter** (NULLs dropped, rows amputated by INNER, the selection you forgot you made — the count-before/after habit catches them all); **skipping the reconciliation** (every doubled total in this appendix traces to it); and **narrating before checking** (the chart's wobble, the model's brilliance, the "significant" — all stories told before the data was asked). Notice that none of the five is a tool problem. The labs teach tools; the wrong turns teach the profession.
