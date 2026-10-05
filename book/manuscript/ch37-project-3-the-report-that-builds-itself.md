# Chapter 37: Project 3 — The Report That Builds Itself

*Part V — Python: From Zero to Dangerous*

> "The best monthly report is the one you read with coffee, not the one you build with overtime."

### In this chapter you will learn

- The automation mindset: pipeline, not performance — inputs → checks → analysis → outputs.
- Building Tariro's automated monthly report, end to end, in one script.
- The professional project structure: files, folders, config, README.
- Scheduling: cron and Task Scheduler — the report that runs while you sleep.
- Failure handling: what a good automation says when data is missing.

## 37.1 The Pipeline Mindset

Every analysis so far in this book was a *performance* — you, present, running cells. Automation converts the performance into a **pipeline**: a fixed sequence — *inputs → loading checks → analysis → outputs* — that runs identically every time, unattended, and says something sensible when the world misbehaves. The mindset shift is the analyst's rite of passage: from *doing the analysis* to *building the thing that does the analysis*. Employers pay generously for the second (Chapter 50's job listings will say "automate recurring reporting" almost verbatim), because a pipeline's work compounds: build once, collect every month.

Tariro's monthly report — the one you assembled by hand in Project 1 (Chapter 13) and re-analysed in SQL (Project 2) — is the target. It will now build itself: fresh CSVs in, checked; analysis computed; charts drawn; a text report written; everything saved to a dated folder, with a log of exactly what happened.

## 37.2 The Structure

Professional Python projects live in folders, not lone notebooks — the structure now, because Project 4–6 and your portfolio (Chapter 49) inherit it directly:

```text
tariro-monthly/
  README.md            -- what this is, how to run it, the data contract
  config.py            -- paths, thresholds, the fence, all constants
  toolkit.py           -- the reusable functions (fences, z-scores, checks)
  build_report.py      -- THE PIPELINE: one command, everything happens
  data/
    raw/               -- CSVs as received (never edited by hand)
    processed/         -- cleaned parquet/CSV, written by the pipeline
  output/
    2025-06/           -- one dated folder per run
      report.md        -- the findings, written by the machine
      exhibits/        -- the PNG charts
      run_log.txt      -- what was checked, what was found, what failed
```

Three conventions carry all the professionalism: **raw data is sacred** (the pipeline reads `data/raw/`, never modifies it — cleaning happens *to a copy*, in code, reproducibly; hand-edited raw data is the original sin of Part II, never again); **constants live in config** (`WHALE_FENCE = 21.50` in one place — the named-constant habit, now load-bearing); and **every run writes its own dated folder plus log** — the audit trail Chapter 20 demanded of SQL, generated automatically.

## 37.3 The Toolkit and the Checks

`toolkit.py` — the functions you have already written in Practice Labs, gathered to be imported forever:

```python
# toolkit.py
import pandas as pd

def iqr_fences(values):
    q1, q3 = values.quantile([0.25, 0.75])
    iqr = q3 - q1
    return q1 - 1.5 * iqr, q3 + 1.5 * iqr

def loading_checks(sales, customers):
    """The liturgy: row counts, key census, orphans, totals, NULLs.
    Returns a list of check-result strings for the run log."""
    lines = []
    lines.append(f"sales rows: {len(sales):,}")
    lines.append(f"duplicate customer ids: {customers['customer_id'].duplicated().sum()}")
    orphan = sales.loc[sales["customer_id"].notna()
                       & ~sales["customer_id"].isin(customers["customer_id"])]
    lines.append(f"orphan sales: {len(orphan)}")
    lines.append(f"total revenue: {sales['amount'].sum():,.2f}")
    lines.append(f"null amounts: {sales['amount'].isna().sum()} (must be 0)")
    return lines, len(orphan)

def z(series):
    return (series - series.mean()) / series.std()
```

And the pipeline's first stage — the checks with *consequences*: a run whose totals do not reconcile with last month's bridge, or whose null amounts are non-zero, must **stop and say so**, not produce a beautiful report from broken data. Automation without failure-handling is a rumour generator:

```python
# inside build_report.py -- the guard
lines, n_orphan = loading_checks(sales, customers)
if sales["amount"].isna().sum() > 0:
    raise SystemExit("ABORT: null amounts in sales -- investigate before reporting")
if n_orphan > 20:                       # config: the documented tolerance
    raise SystemExit(f"ABORT: {n_orphan} orphan sales (tolerance 20)")
```

`raise SystemExit` stops the run with a message — crude, honest, and exactly right for a first pipeline. (The professional pattern is logging with levels and email alerts; you will meet `logging` in Chapter 58's world. The principle is already here: **fail loudly, never report from data you don't trust.**)

## 37.4 The Pipeline

The heart of `build_report.py`, abridged to its moves (the full listing is in Appendix C; every line is a chapter you own):

```python
"""Tariro's monthly report -- builds itself. Run: python build_report.py"""
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import toolkit, config

# 1. INPUTS
sales = pd.read_csv(config.RAW / "sales.csv", parse_dates=["date"])
customers = pd.read_csv(config.RAW / "customers.csv")
sales["month"] = sales["date"].dt.to_period("M")
latest = sales["month"].max()

# 2. CHECKS (fail loudly -- see 37.3)
# 3. ANALYSIS -- the Chapter 34 re-run, as functions
monthly = sales.groupby("month")["amount"].sum()
by_weekday = sales.groupby(sales["date"].dt.day_name())["amount"].agg(["count", "sum", "mean"])
member_share = sales.assign(m=sales["customer_id"].notna()).groupby("month")["m"].mean()
prev, this = monthly.iloc[-2], monthly.iloc[-1]

# 4. EXHIBITS
fig, ax = plt.subplots(figsize=(9, 4))
ax.plot(monthly.index.astype(str), monthly.values, color=config.TEAL)
ax.set_title(f"Monthly revenue: {this:,.0f} this month ({(this/prev-1)*100:+.1f}% MoM)")
fig.savefig(config.OUT / str(latest) / "exhibits" / "revenue.png", dpi=150)

# 5. THE REPORT -- f-strings assemble the findings
report = f"""# Tariro's Grocery -- Monthly Report {latest}

Revenue: ${this:,.2f} ({(this/prev-1)*100:+.1f}% vs last month).
Member share of sales: {member_share.iloc[-1]*100:.1f}%.
Sunday takings averaged ${by_weekday.loc['Sunday','mean']:,.0f}
vs weekday ${by_weekday.drop('Sunday')['mean'].mean():,.0f}.

_Caveats: member share is association, not causation (Ch. 28);
18 months is one shop, not all shops (Ch. 25)._
"""
(config.OUT / str(latest) / "report.md").write_text(report)
print(f"Built: output/{latest}/report.md")
```

Run it: `python build_report.py`. A dated folder appears with an exhibit and a report whose numbers you did not type. **Read the report critically anyway** — automation relieves the typing, never the judgment; the caveats are in the template *because* the machine won't add them unprompted. That sentence is the ethics of automation, and it matters more every year.

## 37.5 Scheduling and the Compounding

The last step removes you entirely. **Windows:** Task Scheduler → Create Basic Task → weekly → `python C:\...\tariro-monthly\build_report.py`. **macOS/Linux:** cron — `crontab -e`, add `0 7 1 * * cd /path/tariro-monthly && python build_report.py` (the syntax: minute hour day-of-month month day-of-week — this line runs at 07:00 on the first of each month). On the first of next month, the report builds itself before Tariro's coffee. (Chapter 57's world industrialises this same idea with workflow orchestrators; the principle is identical and starts here.)

And so the promise of Part V closes: the analysis that took a spreadsheet afternoon (Part II) became a SQL pack of queries (Project 2) and is now a *program* — checked, charted, written, scheduled, logging itself. The before/after timing — an afternoon vs zero minutes — is the portfolio's most persuasive number, and Project 3 is its artefact.

> **From Your Toolkit — the pipeline is the profession:** this exact structure — config, toolkit, pipeline script, sacred raw data, dated outputs, run logs, failure guards — is how every serious analytics deliverable is built, from a corner shop to a data platform. Projects 4–6 reuse it; Chapter 49 publishes it; employers' "automate recurring reporting" is it. You have not just learned Python; you have learned *how the work works*.

## Key Takeaways

- Automation = pipeline: inputs → checks → analysis → outputs, identical every run, sensible when the world misbehaves.
- Structure carries the professionalism: README, config constants, toolkit functions, sacred raw data, dated output folders, run logs.
- Checks must have consequences: fail loudly (abort with a message) rather than report from data you don't trust.
- The pipeline is every chapter assembled: loading checks (33), analysis (34), exhibits (35), tests (36), findings with caveats as f-strings.
- Scheduling (Task Scheduler / cron) completes the compounding: build once, collect monthly — an afternoon becomes zero minutes.

## Practice Lab

1. Build the full structure and get `build_report.py` running end-to-end on your data: raw CSVs, checks, three findings, two exhibits, the dated output folder, the run log. (Appendix C's listing is your scaffold; type it, don't paste it.)
2. The failure drill, twice: (a) corrupt a copy of `sales.csv` (delete an amount, duplicate a customer_id) and watch the guard abort; (b) add a new month's plausible rows and watch the report roll forward unchanged in effort. Log both runs' messages — the pair is the automation's character reference.
3. The human review: read the machine's report and mark every place the numbers are right but the *telling* needs you (missing caveats? a finding the template doesn't know to look for?); extend the template by one finding — your judgment, encoded.
4. The scheduling, done for real: schedule the script (or simulate it: run it twice a day for three days) and collect the run logs; write the one-paragraph runbook ("if it fails, do this") in the README — the handover document you would leave a successor.
5. Portfolio evidence #3: README with before/after timing, the folder tree, two exhibits, a screenshot of the run log; update the 150-word case-study note and the STAR paragraph ("tell me about something you automated"). Three projects in the ledger — the portfolio (Chapter 49) is nearly ready to assemble.

## Further Reading

- Chapters 38–43 (Power BI — the report becomes a dashboard), Chapter 49 (the portfolio)
- Appendix C (the full pipeline listing + the Python cookbook)
