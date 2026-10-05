# Chapter 46: Project 4 — Customers and Churn

*Part VII — Real Projects and Your Portfolio*

> "Revenue tells you what happened. Customers tell you what happens next."

### In this chapter you will learn

- Churn, cohorts, and retention: the vocabulary of customer analysis.
- Building the cohort grid: customers by join-month, tracked month by month.
- Survival thinking and the metric that beats averages: lifetime by cohort.
- Finding Tariro's drifting loyal core — the planted pattern, hunted with everything you know.
- The deliverable: a churn report with a save-campaign recommendation.

## 46.1 The Question

Chapter 5 planted it; the design's truth file holds it: *a loyal core is slowly churning.* The business translation, written the Chapter 45 way — one sentence, decision attached: **"Which customers are drifting away, how fast, and what would it cost to lose them — so Tariro can decide whether a save-campaign is worth running?"** Audience: Tariro, this month. Success state: a named list of at-risk valuable customers, a quantified drift, and a recommendation with a budget attached.

The vocabulary first, because customer analysis has a small precise dictionary: **churn** — a customer who stops buying (defined, always: no purchase in N days; we will use "no purchase in 60 days" for a grocery, stated); **cohort** — a group sharing a start (customers who joined in the same month); **retention** — the share of a cohort still active after k months; **CLV** (customer lifetime value) — what a customer is worth across the whole relationship. The reason cohorts rule this domain: averages hide time. "Average customer lasts 9 months" blends the one-visit tourist with the decade-loyal neighbour; cohorts unblend them — and Chapter 22's "which typical" lesson becomes, here, *whose* typical.

## 46.2 The Cohort Grid

The core artefact of customer analysis — a grid: rows = join-month cohorts, columns = months since joining, cells = the share of the cohort still shopping. Build it in pandas (Part V's kit, assembled; every line is a chapter you own):

```python
import pandas as pd

sales = pd.read_csv("sales.csv", parse_dates=["date"])
customers = pd.read_csv("customers.csv", parse_dates=["joined"])

# last purchase per customer: the "active until" stamp
last_seen = sales.groupby("customer_id")["date"].max()

# month of join and month of last purchase -> lifetime in months
cust = customers.set_index("customer_id")
cust["last_seen"] = last_seen
cust["life_months"] = ((cust["last_seen"] - cust["joined"])
                       .dt.days / 30.4).round()

# the cohort grid: retention by join cohort and age
cust["join_cohort"] = cust["joined"].dt.to_period("M")
active = sales.assign(month=sales["date"].dt.to_period("M")).merge(
    cust["join_cohort"], left_on="customer_id", right_index=True)
active["age"] = (active["month"] - active["join_cohort"]).apply(lambda x: x.n)
grid = (active.drop_duplicates(["customer_id", "age"])
             .groupby(["join_cohort", "age"])["customer_id"].count()
             .unstack(fill_value=0))
grid_pct = grid.div(grid[0], axis=0)        # % of cohort still active
```

Read `grid_pct` as the shop's leak diagram: column 0 is everyone (100%); column 3 is who remained after a quarter; the *slope down the columns* is churn, cohort by cohort. On Tariro's data the pattern Chapter 5 planted shows up as it was designed to: early cohorts (the founding neighbours) hold flat at high retention for their first year — then, from around month 12, the top rows thin faster than the rows below them. The loyal core is drifting, and the grid caught it in the only way it *could* be caught: by keeping time separate instead of averaging it away.

## 46.3 Survival Thinking and CLV

The cohort grid's more rigorous sibling, one idea deeper: **survival analysis** — the study of *time until an event* (here, churn; in medicine, relapse; in machinery, failure — the same statistics across worlds). The beginner-friendly version: the **survival curve** — for each month k, the share of customers still active — plotted as one line per cohort, or one overall line (the Kaplan-Meier estimator is its formal name; the intuition is the grid's last row read as a curve). Why it beats averages: it answers the question the business actually asks — *"if we acquire a customer today, what fraction survives to month 12?"* — directly, from data, without assuming everyone is average.

CLV, computed honestly on the same frame: average monthly spend (members only, by cohort) × expected lifetime (from the survival curve, say 11 months for recent cohorts vs 14 for the founding one) — a number per cohort, with its caveat spoken: *computed from past behaviour, assuming the future resembles the past, churn-styled by definition of the 60-day rule* (Chapter 2's "says who?", aimed at our own arithmetic). The finding this yields on Tariro's data: the founding cohort's CLV is roughly 1.4× the newer cohorts' — *losing one founding customer costs what losing one-and-a-half new ones does* — which reframes the whole save-campaign question: the drift is small in *customer count* and large in *value*.

## 46.4 The Drift, Found and Named

The analysis converges on the deliverable the question demanded — the named list. Definition (stated in the report, as always): a customer is **at-risk** if they were ever a monthly shopper (≥3 purchases/month for 3+ months) and have not purchased in 45 days. In pandas: filter customers by their historical monthly frequency, join to last-seen, compute days-silent, filter — and out comes the list: on the generated data, about 60 customers, average lifetime value 40% above the shop's mean, concentrated — as the design planted — among the founding cohort. Each row: name, suburb, tier, lifetime value, days silent. That list is the save-campaign's mailing list, and its existence is the difference between "some churn is happening" (a vibe) and "these sixty people, worth this much, are leaving" (a decision).

The recommendation, written the Chapter 13 way: *run a targeted win-back for the 60 at-risk high-value customers (personal SMS + a voucher worth ~2% of their annual value); measure redemption after 3 weeks; success = 25% return rate, which on the CLV arithmetic pays for the campaign roughly 8×.* Measurable, budgeted, with a kill-line — and the caveat that this is *association observed, not cause established*: the drift's *cause* (a competitor? prices? life events?) is unknown, which is exactly why the campaign is a test with a measurement, not a certain fix (Chapter 28's discipline, applied to a business action).

## 46.5 The Deliverable and the Evidence

Ship it as the anatomy prescribes: `churn-report/` — the notebook (`churn-analysis.ipynb`, prose-celled, Restart & Run All clean), the cohort grid as a chart exhibit (a heatmap: cohorts down, age across, retention shaded — one picture that tells the whole story), the survival curves, the at-risk list as CSV, the one-page report with the recommendation, the 150-word case-study note ("Situation: grocery shop, 18 months, 640 customers… Work: cohort retention, survival curve, CLV by cohort… Finding: founding cohort churning 2× fast, 60 named at-risk worth 1.4× mean… Impact: save-campaign designed, 8× payback if 25% return… Limits: synthetic-labelled, cause unknown, 60-day churn rule stated").

And the interview line it funds, added to the ledger from Project 2: "tell me about a time your analysis changed a planned action" — the campaign design, the CLV arithmetic, the honest unknown-cause caveat. Employers in *every* industry run churn questions (telecoms, banks, streaming, retail — the vocabulary transfers whole), and Project 4 is the proof you have run one end-to-end.

> **From Your Toolkit — time in the rows:** cohort grids and survival curves are the general answer to "how does a group move through time?" — retention in product analytics, dropout in education, default in lending, relapse in health: same grid, different nouns. pandas' groupby-unstack built it; SQL's window functions could have (Appendix A carries the pattern); even a spreadsheet can, painfully. The *idea* — never average across time when time is the question — is the transferable instrument.

## Key Takeaways

- Churn needs a stated definition (no purchase in N days); cohorts unblend the averages that hide time.
- The cohort grid (join-month × age → retention) is customer analysis's core artefact; build it with groupby + unstack; read the slopes.
- Survival thinking answers "what fraction survives to month k?" directly; CLV = monthly spend × expected lifetime, per cohort, caveats spoken.
- The deliverable is a named list with values and a measurable, budgeted recommendation — association observed, cause unknown, so the campaign is a test.
- Ship the folder: notebook, exhibits, at-risk CSV, one-pager, 150-word note — the portfolio's fourth evidence and a story every industry recognises.

## Practice Lab

1. Build the cohort grid and the retention heatmap on your data; read the founding-cohort thinning with your own eyes; write the three-sentence story the heatmap tells (include the numbers).
2. The survival curves: one line per join-year cohort (or founding vs later), retention vs months-since-join; annotate where the founding line bends; state the 12-month survival for each cohort with its interval (bootstrap, Ch. 36 — you own it).
3. CLV by cohort with the arithmetic shown; then the sensitivity check: recompute at ±20% monthly spend and note how the campaign payback changes — the "is my interval narrow enough to decide?" question, applied.
4. The at-risk list: implement the stated definition; reconcile the count by hand for five customers (their last purchase dates, their frequency history); export the CSV and check it opens clean in a spreadsheet.
5. The report and the note: assemble `churn-report/` complete; run the Chapter 45 checklist against it; write the 150-word note and the STAR paragraph; update the portfolio ledger — two projects remain.

## Further Reading

- Chapter 47 (surveys — asking the customers who are leaving), Chapter 58 (churn's machine-learning sequel)
- *Survival Analysis* (Kleinbaum) ch. 1–2 — if the Kaplan-Meier idea grabbed you
