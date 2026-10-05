# Chapter 3: The Tools of the Trade

*Part I — Beginning: You, the Data Analyst*

> "Six tools, one grammar: tables in, answers out."

### In this chapter you will learn

- The guided tour of every tool in this book, each explained in one plain paragraph.
- What each tool is *for* — and what it is cheerfully bad at.
- The one idea (tables!) that connects all of them.
- The free version of everything, in one table.
- How the book's journey (Excel → SQL → statistics → Python → Power BI) is deliberately ordered.

## 3.1 The Big Idea First: Tables

Every tool in this book works on the same shape: **a table** — rows and columns, where each row is one thing (one sale, one customer, one answer) and each column is one fact about it (the date, the amount, the store). Learn to see the world as tables and every tool becomes a dialect of one language:

| tool | what it does with your table |
|---|---|
| Excel | shows it to you, lets you point and click at it |
| SQL | lives inside the database, answering questions about it at scale |
| Statistics | judges whether the table's patterns mean anything |
| Python | programs the table — anything you did by hand, automated |
| Power BI | turns the table into pictures a room can discuss |
| SPSS / Stata | the classic statistics packages — same questions, point-and-click or scripted |

This is why the book can promise "five tools, genuinely learned" without five times the effort: **you learn tables once (Chapter 6), joins once (first Excel, then SQL, then Python), charts once (Excel, then Python, then Power BI), and testing once (counting in Part IV, then every package agrees).** The "From Your Toolkit" callouts mark each reunion.

## 3.2 The Tour

**Excel** (Part II). The world's most-used analytics tool and the right place to start: you can see everything, touch everything, and break everything harmlessly. Formulas, pivot tables, and charts cover an enormous share of real working analytics — and every employer expects them. Its limit: it is one screen, one file, one user — slow or fragile when data gets big or updates daily. *Free twin: LibreOffice Calc, identical for everything in this book.*

**SQL** (Part III). "Structured Query Language" — the language of databases. Where Excel shows you the table, SQL *asks the table questions* ("total sales by store for March, excluding refunds") and returns only the answer, instantly, on tables far too big for any spreadsheet. It is the single most-tested skill in analyst interviews (Chapter 52), the one this book teaches most thoroughly, and — good news — the core is about twenty patterns you will reuse forever.

**Statistics** (Part IV). Not a software tool but a thinking tool: how to describe honestly (averages and their traps), and how to judge whether a pattern is real or luck. We teach it by *counting* — simulating coin flips and drawing the answers — before any formula appears. **SPSS** and **Stata** are the classic statistics packages you may meet in university courses, research offices, and government: same ideas, different buttons, both covered gently in Chapter 29.

**Python** (Part V). A full programming language, and the analyst's version of it is mostly one library — **pandas** — that puts your table in a notebook and lets you program it: "read the sales file, drop the duplicates, total by month, chart it, save the chart" as a short script that runs again next month without you. The beginner's fear — "programming" — dissolves in about three chapters, because analyst Python is mostly verbs you already know: `read`, `group`, `merge`, `plot`.

**Power BI** (Part VI). Microsoft's dashboard tool: it connects to your tables (Excel files, databases), remembers how they relate, and turns them into interactive pages — filters, drill-downs, monthly refreshes — that a manager can use without you. The **Desktop** edition is free, and the skill is in heavy demand because dashboards are how organisations breathe.

## 3.3 What Each Tool Is Bad At

Honesty works both ways:

- **Excel** is bad at *big* (hundreds of thousands of rows get slow) and *repeated* (manual monthly work drifts into errors) and *shared* (versions multiply by email).
- **SQL** is bad at *charts* (it answers; it does not draw) and *everything before the question* (it does not clean your notebook's coffee stains — that is Excel or Python).
- **Statistics** is bad at *deciding for you* — it quantifies doubt; the judgement stays human.
- **Python** is bad at *first contact* (a blank notebook is intimidating — for two weeks) and *pretty point-and-click* (nobody "just opens" Python to glance at something).
- **Power BI** is bad at *deep exploration* (it shows; it does not replace the analysis behind it) and *the last mile of polish* without its paid sharing service (your dashboard travels as screenshots or the free desktop file).

The working analyst runs the **relay**: Excel to meet and clean the data, SQL to query it at scale, statistics to judge it, Python to automate the repetition, Power BI to publish it. This book teaches the relay, in relay order.

## 3.4 The Free Table

| Tool | Free version | Where | Part |
|---|---|---|---|
| Excel (or its twin) | LibreOffice Calc | libreoffice.org | II |
| SQL | SQLite + DB Browser for SQLite | sqlitebrowser.org | III |
| Statistics | By counting (pen, paper, Python later) | — | IV |
| SPSS / Stata | Trial versions; university labs; every idea taught free in Python too | spss.com, stata.com | IV |
| Python | Anaconda (Python + Jupyter + pandas, one install) | anaconda.com | V |
| Power BI | Power BI Desktop | microsoft.com | VI |

Total cost of the complete toolkit: **$0**. Chapter 4 installs it all in one sitting; keep this page as your shopping list.

## 3.5 Why This Order

The book's order is deliberate, and worth knowing so you can trust the stairs:

1. **Excel first** because seeing and touching tables builds the mental model every other tool assumes.
2. **SQL second** because it is the most-tested interview skill and the one that makes spreadsheets' limits vanish — and it *needs* the table-thinking Excel gave you.
3. **Statistics third** because once you can pull real data, the questions "is this real or luck?" start coming at you — and are answerable by counting.
4. **Python fourth** because automation is most appreciated after you have done the work by hand at least twice.
5. **Power BI fifth** because a dashboard is only as good as the analysis behind it — and now there is one.

If you arrive with one tool already (many readers know some Excel), the callouts let you skim your strong tool and lean on your weak ones.

> **From Your Toolkit — future you:** every tool you learn makes the next one cheaper, because each is the same grammar in a new accent. The first tool is the hardest — which means the only one you must simply decide to start. Today, that is Chapter 4's afternoon of installing; by Chapter 13 you will have a working toolkit and a project to prove it.

## Key Takeaways

- One shape under everything: the table — rows are things, columns are facts.
- The relay: Excel meets and cleans, SQL queries, statistics judges, Python automates, Power BI publishes.
- Every tool is bad at something; the team of them is the toolkit.
- Everything is free (Excel has a twin), and Chapter 4 installs it all in one afternoon.
- The book's order is the relay's order — each tool pays for the next.

## Practice Lab

1. The table lens: write down three "tables" in your daily life (bank SMSs, WhatsApp messages, a shopping list). For each, define the row (one message? one conversation?) and three columns.
2. Match the tool to the job: for each request, name the part of the relay that owns it — "clean 500 rows of survey answers", "total sales by store for two years", "is the new shelf layout actually better?", "refresh this report every Monday", "show the board the trends".
3. The shopping list: open the free table in Section 3.4 and bookmark each download page — even before installing (Chapter 4 does that), knowing where they live is half the battle.
4. Tool autobiography: which tool are you already strongest in, and which scares you most? Write one sentence each — you will reread both in Chapter 62.
5. The relay audit: find one repetitive number-task in your work or studies and describe its five relay stages: how it is met, queried, judged, automated, and published today — or which stages are missing.

## Further Reading

- Chapter 4 (install everything, this afternoon), Chapter 5 (meet Tariro and her data)
- The "tool comparisons" videos everywhere online — notice how they all confirm the relay: none of them says "one tool only".
