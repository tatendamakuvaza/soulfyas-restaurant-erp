# DESIGN — The Practical Data Analyst's Handbook

*The blueprint for this book. Every chapter is written against this page.*

## The One-Sentence Promise

**Take a reader with zero background — no statistics, no code, no tools — and walk them, step by friendly step, to their first data analyst job: Excel, SQL, statistics, Python, Power BI, real projects, a portfolio, interviews, and the career beyond.**

- **Title:** The Practical Data Analyst's Handbook
- **Subtitle:** From Zero to Your First Data Job — A Complete Beginner's Course
- **Author:** Tatenda Makuvaza — "The Big Data Analyst"
- **Edition:** First Edition, 2026
- **Target size:** ~450–500 print pages (62 chapters + 5 appendices)
- **Audience:** absolute beginners; career changers; students; the self-taught. Assumes nothing but literacy and willingness.
- **Voice:** a patient mentor. Plain English first, every term defined at first use, every formula arrives with its sentence version, small humour allowed, condescension never.

## Standing Rules (every chapter)

1. **From zero:** no prior chapter-of-the-world assumed; each tool is introduced as if the reader has never opened it.
2. **Everything free:** every tool used has a free version (Excel is the one paid exception — LibreOffice named as the free twin every time).
3. **Plain English first:** every technical term gets a one-sentence definition the moment it appears; the glossary is a safety net, not a prerequisite.
4. **Show, then do:** every concept appears first as a worked example on the running case, then as a Practice Lab for the reader.
5. **The toolkit bridges:** "From Your Toolkit" callouts connect each new tool back to the ones the reader already learned — the same join in Excel, then SQL, then Python.
6. **Honesty rules:** correlation ≠ causation, averages lie, samples have error — the honesty habits are taught in Part I and enforced everywhere after.
7. **Template:** H1 chapter title → italic part line → one-line epigraph → "In this chapter you will learn" → numbered sections (N.x) → Key Takeaways → Practice Lab (5–6 tasks) → Further Reading. Code lines ≤ 88 characters. Tables are pipe tables.

## The Running Case: Tariro's Grocery

**Tariro** runs a grocery store in Highfield, Harare. She began with a paper notebook and a memory for her regulars; she now has a secondhand laptop, a spreadsheet she half-trusts, and a dream of a second branch. In Chapter 5 the reader becomes her analyst — and stays hired for the whole book:

- **Part II:** her messy spreadsheet becomes the first monthly report (Excel).
- **Part III:** her sales, stock, and customers move into a real database (SQL).
- **Part IV:** her questions — "are Sundays worth it?", "did the price rise hurt us?" — become statistics.
- **Part V:** the monthly report rebuilds itself (Python).
- **Part VI:** her numbers become a dashboard her bank manager can read (Power BI).
- **Part VII:** three portfolio projects, all on Tariro's data, documented for employers.
- **Part VIII:** the reader's own job hunt, using Tariro as the story.
- **Part IX:** the gentle maps of what comes next.

She is fictional; her data is generated (Appendix recipe included) with planted patterns — weekly rhythms, payday spikes, a price-rise dip, a loyal-customer core — so every analysis can be scored against truth.

## The Structure — 9 Parts, 62 Chapters, 5 Appendices

### Part I — Beginning: You, the Data Analyst (Ch. 1–5)
1. What a Data Analyst Actually Does — a day in the life; the myths; the job in plain words.
2. The Analyst's Mindset — curiosity, skepticism, clarity; questions before data.
3. The Tools of the Trade — the guided tour; what each is for; free versions of everything.
4. Set Up Your Workspace — installing it all, free; folder discipline; the practice data.
5. Meet Tariro — the running case; her notebook, her spreadsheet, her first question.

### Part II — Excel: Your First Superpower (Ch. 6–13)
6. Thinking in Grids — cells, rows, tables; the anatomy of a spreadsheet.
7. Formulas from Zero — SUM, AVERAGE, IF; every formula in plain English.
8. Cleaning a Messy Sheet — sort, filter, find & replace, text tools, duplicates.
9. Joining Tables in Excel — VLOOKUP, XLOOKUP, INDEX-MATCH, without fear.
10. PivotTables — the analyst's best friend; five clicks to insight.
11. Charts That Tell the Truth — the five charts that matter; the lies charts tell.
12. Statistics in Excel — descriptives, quick analysis, the Analysis ToolPak.
13. Project 1: Tariro's First Monthly Report — guided end-to-end.

### Part III — SQL: The Language of Data (Ch. 14–21)
14. What a Database Is — tables vs files; SQLite and DB Browser, free.
15. Your First Queries — SELECT, WHERE, ORDER BY; reading a table.
16. Counting and Grouping — COUNT, SUM, AVG, GROUP BY; the aggregate habit.
17. Joins Without Fear — diagrams; the fan-out trap in plain words.
18. Queries in Steps — subqueries and CTEs; building big queries from small ones.
19. Window Functions — running totals, rankings, the power moves.
20. SQL in Real Life — workbenches; reading others' queries; the queries you'll actually write.
21. Project 2: Tariro's Database — import the CSVs; answer ten business questions.

### Part IV — Statistics Without Fear (Ch. 22–29)
22. Numbers That Describe — mean, median, mode; when each one lies.
23. Spread and Shape — range, deviation, skew; the bell curve, gently.
24. Percentiles and Standards — z-scores, "above average", plainly.
25. Samples and Populations — why we sample; margins of error without the trauma.
26. Testing, Gently — hypothesis tests by counting; what a p-value really says.
27. Categories and Surveys — percentages, cross-tabs, chi-square in SPSS step by step.
28. Relationships — correlation, the line of best fit, and the causation trap.
29. SPSS and Stata, Gently — the classic statistics tools; menus, do-files, when you'll meet them.

### Part V — Python: From Zero to Dangerous (Ch. 30–37)
30. Why Python, and How to Start — Anaconda, Jupyter, the notebook way.
31. Your First Lines — variables, numbers, text; printing; errors as friends.
32. Lists, Loops, and Logic — if, for, and thinking in steps.
33. DataFrames from Zero — pandas; loading Tariro's CSVs; the spreadsheet you program.
34. pandas Power Moves — groupby, merge, pivot; everything you did in Excel, again.
35. Charts in Python — matplotlib basics; when to stay in Excel.
36. Statistics in Python — the same answers as SPSS, in six lines.
37. Project 3: The Report That Builds Itself — the monthly report, automated.

### Part VI — Dashboards and Storytelling with Power BI (Ch. 38–43)
38. What Power BI Is — the free Desktop edition; the workflow in one page.
39. Getting Data In — loading, shaping, and the data model; relationships gently.
40. Measures and DAX — the ten formulas that cover 90% of the work.
41. Your First Dashboard — Tariro's dashboard, built page by page.
42. Chart Craft, Again — the dashboard edition of Chapter 11's rules.
43. Telling the Story — the one-page summary; presenting to non-analysts.

### Part VII — Real Projects and Your Portfolio (Ch. 44–49)
44. Where Practice Data Comes From — public datasets; generating your own; the honesty of planted patterns.
45. The Anatomy of an Analysis — question → data → clean → analyze → communicate; the checklist.
46. Project 4: Customers and Churn — who is drifting away, and what to do.
47. Project 5: The Survey — questions, cleaning, cross-tabs, the honest report.
48. Project 6: The Operations Dashboard — stock, staffing, and the Sunday question.
49. Your Portfolio — GitHub for absolute beginners; the three-project portfolio; the walkthrough that gets you hired.

### Part VIII — Getting the Job (Ch. 50–56)
50. The Job Landscape — titles, roles, and what employers actually want.
51. Your CV and LinkedIn — the analyst's CV, line by line.
52. The Technical Interview — SQL tests, Excel tests, case questions; the practice bank.
53. Cases and Behaviour — STAR stories; the take-home; presenting your work.
54. Your First 90 Days — what to learn, whom to meet, the quick win.
55. Freelancing and Side Income — first clients, pricing small jobs, delivering.
56. The Career Ladder — analyst → senior → lead; specializing; staying current, cheaply.

### Part IX — Beyond the Basics (Ch. 57–62)
57. A Gentle Map of Machine Learning — what it is, the vocabulary, when you need it.
58. A Gentle Map of Big Data — when data is actually big; the cloud in plain words.
59. Ethics and Privacy, Essentials — consent, bias, honesty; the rules that protect you.
60. Messy Reality — missing data, biased samples, deadlines; the 80/20 of practice.
61. The Free Stack — the $0 toolkit, and the $200 upgrade; working offline.
62. Your Next Decade — the learning roadmap; community; the compounding career.

### Appendices — The Cookbook
- **A. SQL Cookbook** — the 25 most useful queries, commented line by line.
- **B. Excel Cookbook** — the 25 most useful formulas and tricks.
- **C. Python Cookbook** — the 25 most useful pandas snippets.
- **D. Statistics Cheat Sheet** — which test when; the plain-English decision table.
- **E. Interview Question Bank** — 100 questions with guidance, by tool and topic.

## Production Plan

Built and delivered in batches, every batch committed to git and pushed (the lesson of the resets, learned twice):

| Batch | Contents |
|---|---|
| 1 | This design + front matter + Part I (Ch. 1–5) |
| 2 | Part II (Ch. 6–13) |
| 3 | Part III (Ch. 14–21) |
| 4 | Part IV (Ch. 22–29) |
| 5 | Part V (Ch. 30–37) |
| 6 | Part VI (Ch. 38–43) |
| 7 | Part VII (Ch. 44–49) |
| 8 | Part VIII (Ch. 50–56) |
| 9 | Part IX (Ch. 57–62) + appendices A–E |

Both editions rebuild on every batch: print-ready PDF (7×10", cover, TOC, bookmarks) and single-file HTML. Acceptance: ~62 chapters, ~5 appendices, ~450–500 pages, author name **Tatenda Makuvaza** everywhere.
