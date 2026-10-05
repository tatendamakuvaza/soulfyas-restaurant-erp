# Chapter 30: Why Python, and How to Start

*Part V — Python: From Zero to Dangerous*

> "Spreadsheets repeat. SQL re-queries. Python *works* — the same file, every month, forever, on any data you point it at."

### In this chapter you will learn

- Why Python earns a whole part of this book — the three jobs no other tool does.
- Python and Jupyter: what they are, and how to install in under an hour.
- The notebook way of working — code, output, and story in one document.
- Your first five cells, on Tariro's real data.
- How this part is structured, and how to practise so it sticks.

## 30.1 The Three Jobs

Part II answered questions with clicks; Part III saved the clicks as queries; Part IV gave the conclusions machinery. What is left? The *labour*: every month, Tariro's CSVs arrive, and the whole chain — import, cleaning checks, joins, tests, charts, report — runs again. In tools so far, that means re-doing. Python's pitch is exactly the remainder:

1. **Automation** — write the chain once; every month it is one command. (The monthly pack of Project 2 becomes a script that never sleeps.)
2. **Scale** — Python reads data bigger than spreadsheets (pandas, the star of this Part, works in the hundreds of thousands to millions of rows on a laptop) and connects to anything: CSVs, databases (your `tariros.db`!), APIs, the web.
3. **Everything else** — Python is a *general* language: statistics (Part IV's tests, one line each), machine learning (Chapter 58's door), web apps, glue between systems. Skills compound beyond the dashboard.

And the honest counter-pitch, so you choose tools like a professional: Python is *code* — typos are errors, not silent cells; the learning curve is real (a weekend, not an hour); and for a quick one-off look at 500 rows, the spreadsheet is still the right tool. The working analyst's stack is all five tools of this book, each doing what it is best at — Python's slot is *repeatable work at scale*.

## 30.2 Python, Anaconda, and the Notebook

**Python** is the language; a **Jupyter notebook** is where you will live: a document of *cells*, each cell a few lines of code with its output directly beneath — code, result, and prose interleaved. The notebook is the analyst's lab bench: try something, see it, explain it, move on. (If you have seen a data-science tutorial, you have seen a notebook.)

Installation, the recommended path — **Anaconda** (anaconda.com, free): a Python distribution that arrives with the entire scientific stack pre-installed — pandas, matplotlib, scipy, statsmodels, jupyter — no dependency archaeology. Download, install, launch **JupyterLab** from the Anaconda Navigator (or type `jupyter lab` in a terminal). Total time: under an hour; total decisions: nearly zero. (Already have Python? `pip install pandas matplotlib scipy statsmodels jupyterlab` — but Anaconda spares you the archaeology, and this book recommends it for your first year.)

The environment note that saves confusion: Anaconda Navigator also offers **Jupyter Notebook** (the older single-document interface) — this book's screenshots assume JupyterLab, but every cell works identically in both, and in VS Code's notebook mode, and in Google Colab (the no-installation, in-browser option — perfect if your machine is borrowed or locked down). Pick one; the cells do not care.

## 30.3 The First Five Cells

Open JupyterLab, File → New → Notebook, and save it as `tariro-first-five.ipynb` in your `tariro-data` folder. Then run these — each in its own cell, Shift+Enter to execute, and *watch the output appear beneath*:

```python
# cell 1: the load -- pandas reads a CSV into a DataFrame
import pandas as pd
sales = pd.read_csv("sales.csv")
sales
```

A table appears — the whole sales history, neatly gridded, numbered. That object is a **DataFrame**: pandas' spreadsheet, and the centre of this entire Part. Note the last line: in a notebook, a bare name on the last line of a cell *displays* itself — the analyst's flashlight.

```python
# cell 2: the shape and the first rows
sales.shape          # (6420, 6) -- rows, columns
sales.head()         # first five rows
```

```python
# cell 3: the Part II statistics, wholesale
sales["amount"].describe()
```

One method, and the five-number summary plus count, mean, and standard deviation of the amount column print as a table — Chapter 22's entire chapter, one line. You will use `describe()` more than any other single line in this book.

```python
# cell 4: a question answered
sales.groupby("payment_type")["amount"].agg(["count", "sum", "mean"])
```

The Chapter 16 pivot — payment types down the side, count/sum/mean across — in one line. If you slow down and read that line as a sentence (*take sales, group it by payment_type, take amount, aggregate count sum mean*), you have just read your first fluent pandas.

```python
# cell 5: the chart
sales.groupby("date")["amount"].sum().plot(figsize=(10, 4), title="Daily takings");
```

A chart of daily takings renders in the notebook — Chapter 11's line, no menus, no spreadsheet, and (this is the point) re-runnable on next month's CSV by changing nothing.

Five cells, and the pitch is made: load, inspect, summarise, question, chart — the whole analytical arc, in a document you can re-run forever. Everything else in this Part is these five cells with more vocabulary.

## 30.4 The Way of Working

Notebook craft, learned early, saves months:

- **Run cells top to bottom.** A notebook has *state* — cell 4 remembers what cell 1 loaded. Running cells out of order is the classic notebook bug (numbers from stale data); the fix is the discipline, and *Restart & Run All* is the truth test — run it before trusting, sharing, or delivering any notebook.
- **Prose cells** (the `+` button, then switch the cell to Markdown) carry the story: what you are asking, what you found. A notebook that alternates prose and code is a *report that computes itself* — the deliverable format of Part VII's projects and of modern analytics teams.
- **Small cells, often.** Ten lines, run, look; not a hundred lines and a prayer. Errors (next chapter makes them friends) are cheap when cells are small.
- **Name files like the question** (`oil-price-analysis.ipynb`, not `untitled7.ipynb`) — Chapter 20's etiquette, unchanged by the tool.

## 30.5 How This Part Runs

Seven chapters, each a working session on Tariro's data, each ending in the Practice Lab you now expect: **31** variables and data types; **32** the analyst's control flow (loops, functions, and when *not* to loop — the pandas way); **33** pandas properly — the DataFrame grammar; **34** the analysis kit — groupby, join, time series (the whole book so far, re-expressed); **35** charts in matplotlib; **36** the statistics of Part IV, one line each; **37** the capstone — Tariro's monthly pack, automated, plus a professional project structure.

The method that makes it stick, the same method this book has used since Part I: *every concept arrives attached to Tariro's questions; every lab re-uses the artefacts you already built.* You are not learning Python and then applying it — you are re-doing work you understand, in a tool that makes it permanent. That is also the least frightening way to learn a language: the analysis is already in your head; only the accent is new.

> **From Your Toolkit — the permanent bench:** the notebook becomes your default workspace for the rest of the book: Part VI feeds Power BI from Python-cleaned data; Chapter 58's machine learning lives here; the portfolio (Part VII) is notebook-driven; even this book's datasets (Appendix E) come with a starter notebook. The five cells of this chapter are the bench's five drawers — load, inspect, summarise, question, chart — and every chapter ahead opens them in different orders.

## Key Takeaways

- Python's three jobs: automation (the monthly chain, once), scale (beyond spreadsheets, into databases/APIs), and generality (statistics, ML, glue) — its slot in the stack is repeatable work at scale.
- Anaconda + JupyterLab: one free install, whole scientific stack; notebook = code, output, prose, one document.
- The five-cell arc — read_csv, head/shape, describe, groupby, plot — is the whole Part in miniature.
- Notebook craft: run top-to-bottom, Restart & Run All before trusting, prose cells tell the story, small cells always.
- Learning method: re-do the analyses you already understand, in the new accent — the analysis is in your head; only the accent is new.

## Practice Lab

1. Install: Anaconda (or Colab if installation is impossible), launch JupyterLab, and screenshot your first empty notebook for the log — the workspace milestone from Chapter 4, levelled up.
2. The five cells, typed by hand (no copy-paste — the fingers learn too), on `sales.csv`; caption each with a Markdown prose cell in your own words. Save as `tariro-first-five.ipynb`.
3. The describe() reconciliation: `sales["amount"].describe()` against your Part II five-number summary and STDEV.S values — every number must match to the decimal, and a one-line note certifies the bridge.
4. The groupby tour: re-run cell 4 for `till`, for `payment_type`, and for a `date`-derived month (hint: `sales["date"].str[:7]`) — three pivots, three sentences, same as Chapter 10's lab but re-runnable.
5. The permanence test: close the notebook, close Jupyter, reopen, *Restart & Run All* — everything must re-emerge untouched. Then add one Markdown cell at the top: what this notebook does, data source, date run. That header cell is the notebook edition of the query-pack README, and it is now your habit.

## Further Reading

- Chapter 31 (variables and types — the vocabulary begins)
- *Python for Data Analysis* (McKinney) — by pandas' creator; this Part's natural next step
