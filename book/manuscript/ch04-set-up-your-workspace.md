# Chapter 4: Set Up Your Workspace

*Part I — Beginning: You, the Data Analyst*

> "Install once, learn forever: one afternoon of clicking, and your toolkit is complete."

### In this chapter you will learn

- How to install every tool in this book, free, on any Windows or Mac laptop.
- The folder discipline that will save you hours every month of your career.
- How to open and save the practice data that comes with this book.
- Your first checkpoint: five tools installed and test-driven, error messages included.
- What to do when an install misbehaves (spoiler: it is almost always one of three things).

## 4.1 The Plan

Today is logistics, not learning — but it is the most important logistics of the book. An uninstalled tool is an unlearned tool; the week-three dropout almost always traces back to "I never got it running". Budget ninety minutes, make tea, and install in this order (each step is independent — a failure at one step does not block the others):

| Step | Tool | Time | Your test that it worked |
|---|---|---|---|
| 1 | LibreOffice Calc (or use your Excel) | 10 min | Open it, type 2 + 2 in a cell, press Enter |
| 2 | DB Browser for SQLite (includes SQLite) | 5 min | Open it — you see an empty database window |
| 3 | Anaconda (Python + Jupyter + pandas) | 30 min | Open "Jupyter Notebook", a browser page opens |
| 4 | Power BI Desktop | 15 min | Open it — a big friendly welcome screen |
| 5 | The practice folder (this chapter) | 5 min | You can find it in ninety days, and so could a stranger |

Windows and Mac notes: take every default the installers offer — the defaults exist for people exactly like you today. If your laptop is old or full, the essentials are steps 1–3; Power BI can wait until Part VI, and its installer is the heaviest of the four.

## 4.2 The Folder Discipline

Before any practice file, the habit that separates professionals from the lost: **one home for your analytics work, with a fixed shape**. Create this once, on purpose, and use it for every chapter of this book:

```text
DataAnalyst/                      <- your home for everything
    01-Learning/                  <- one folder per part of this book
        Part02-Excel/
        Part03-SQL/
        ...
    02-Projects/                  <- the Part VII portfolio projects live here
        Tariro-Grocery/
    03-Data/                      <- every data file you download or receive
        raw/                      <- untouched originals, never edited
        clean/                    <- your cleaned copies
    04-Notes/                     <- the notebook habit from Chapter 2
```

Two rules give this structure all its power. **Rule one: `raw/` is sacred.** The original file you receive — downloaded, emailed, exported — goes in `raw/` and is *never edited*. You work on copies; the original is your escape hatch when (not if) a cleaning step goes wrong, and your evidence when someone asks "where did this number come from?" **Rule two: names are self-explanatory.** `tariro-sales-2025-03.csv` lives forever; `final2_REAL.csv` dies in a bad meeting. Dates in names (`YYYY-MM-DD` sorts correctly), no spaces (some tools dislike them), lowercase-and-dashes everywhere.

## 4.3 The Practice Data

This book's running case (Chapter 5 introduces her properly) comes with generated data files: sales, stock, and customer records for a grocery store, with realistic patterns planted so your analyses can be checked against the truth. Get them the same way every working analyst gets data — from one folder, with a note of where it came from:

1. Create `DataAnalyst/03-Data/raw/tariro/` and copy the book's data files into it (the files accompany the book's repository; Appendix and chapter labs reference them as `03-Data/raw/tariro/sales.csv` and friends).
2. Open `sales.csv` in LibreOffice Calc or Excel — accept the import defaults, and you are looking at your first real table: one row per sale, columns for date, time, item, amount, and more.
3. Do nothing to it except look. Notice: it opens in a spreadsheet, because a CSV is just a table in its simplest costume (Chapter 6 explains CSVs properly).

From now on, every Practice Lab assumes this structure, and every lab's first line names its data like a professional: *raw folder in, clean folder out.*

## 4.4 Test-Driving: Your First Error Messages

Installers are done; now the five-minute test drive that makes each tool "yours". Crucially, **each test includes its failure mode** — because meeting your first error message today, in a safe room, is worth three hours of future panic.

- **Calc/Excel:** type `=2+2` — press Enter — `4` appears. Now type `=2+` — Enter — you get an error, something like `#NAME?`. Congratulations: you have broken a spreadsheet. The error is not punishment; it is the tool answering "I do not understand". Fix it, and note the feeling: error → read → fix is the analyst's heartbeat, in every tool, forever.
- **DB Browser:** open it, click "New Database", save `practice.db` anywhere in your `03-Data` folder. You now own a real database. Close it. That is all for today.
- **Jupyter:** open "Jupyter Notebook" (from the Anaconda menu). A browser tab opens with a file listing — click "New → Notebook: Python 3". In the empty box (a *cell*), type `2 + 2` and press Shift+Enter. The answer `4` appears below, and a new empty box waits. You have written a program. Deliberately type `2 +` and Shift+Enter now: read the red wall of text — the *bottom line* of a Python error always names the problem in plain words. This is the last time an error message is new to you.
- **Power BI:** open it, click "Get data → Text/CSV", point it at `sales.csv`, click Load. A table appears in a side panel. You have imported data into a professional BI tool. Close without saving.

If all five worked: your toolkit is complete, free, and paid for with one afternoon. That was the hardest purely-technical day of this book.

## 4.5 When Installs Misbehave

Almost every installation problem is one of three things, in this order of likelihood:

1. **The download was interrupted** — the file is partial. Fix: delete it, re-download, watch it finish.
2. **Your laptop said no** (permissions, disk space, an old operating system). Fix: right-click the installer and "Run as administrator" (Windows); free 10 GB of space; or update the OS if it is truly ancient.
3. **Antivirus enthusiasm** — a security tool "quarantined" something it did not understand. Fix: allow the app, or temporarily pause protection during the install.

Only after those three: search the exact error text with the tool name — the fix is almost always the first result, because a hundred thousand beginners hit the same wall this year and someone answered them kindly. Chapter 4's real lesson: **the answers exist, and reading error messages is a skill you have now started.**

## Key Takeaways

- One afternoon installs everything: Calc/Excel, DB Browser (SQL), Anaconda (Python), Power BI Desktop — all free.
- Folder discipline from day one: `raw/` is sacred, names explain themselves, one home for everything.
- The practice data lives in your new structure; every lab starts by naming its files like a professional.
- Test-drive every tool *including* its error messages — you have now met the error-fix-fix heartbeat in the safest possible room.
- Install problems are almost always: partial download, permissions/space, or antivirus — in that order.

## Practice Lab

1. Install all five steps and keep a log: for each tool, the time it took, and one thing that surprised you. (The log is your first notebook entry — Chapter 2's habit, running.)
2. Build the full folder structure from Section 4.2, by hand, exactly as drawn. Then move the practice data into `03-Data/raw/tariro/`.
3. The rename drill: five files with terrible names (`New folder (2).csv`, `SALES final FINAL.xlsx`...) — rename each to the standard: lowercase, dashes, date `YYYY-MM-DD`, no spaces.
4. Error safari: in Jupyter, deliberately cause three different errors (bad math, an unclosed quote, an undefined name) and write down what the *last line* of each message says. You are building the error-reading reflex early.
5. The ninety-day test: close everything, then try to find `sales.csv` in under thirty seconds without hunting. If you passed, your folder discipline is already paying.
6. Back it up: copy your whole `DataAnalyst/` folder to a memory stick or a cloud drive. Chapter 49 turns this habit into a portfolio; today it is just professional survival.

## Further Reading

- Chapter 5 — meet Tariro, and start work as her analyst
- Anaconda's beginner tutorial (optional, 20 minutes — anything unfamiliar there returns in Part V anyway)
