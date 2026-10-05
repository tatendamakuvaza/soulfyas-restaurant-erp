# Chapter 61: The Free Stack — $0 Toolkit, $200 Upgrade

*Part IX — Beyond the Basics*

> "Every tool in this book is free, or has a free twin. The profession's gate is not a credit card — it is the habits, and you have those."

### In this chapter you will learn

- The complete $0 analyst stack, tool by tool, matched to this book's Parts.
- The honest gaps in free — and the workarounds that hold until income.
- The $200 upgrade path: what to buy first, second, never.
- Working offline and on thin hardware: the craft that outlasts bandwidth.
- Tool-agnosticism as the permanent skill — switching accents, cheaply.

## 61.1 The $0 Stack

The full inventory, mapped to the Parts it serves — print this section if money is the constraint; it removes the excuse permanently:

| Part / need | The $0 tool | Notes |
|---|---|---|
| Spreadsheet (Part II) | **LibreOffice Calc**, Google Sheets, Excel for the web | Calc is genuinely sufficient: pivots, lookups, ToolPak-equivalents (Data → Statistics); this book was written with it in mind |
| Database (Part III) | **SQLite** + **DB Browser** | A complete relational engine and workbench; zero install drama (Ch. 14). **DuckDB** — the modern analytical cousin — is the $0 upgrade for warehouse-scale SQL on a laptop, and runs the same chapters |
| Statistics GUI (Part IV) | **PSPP** (GNU), **jamovi**, **JASP** | PSPP speaks SPSS syntax; jamovi is the friendliest menu-driven stats tool ever built, and free forever; JASP adds Bayesian options |
| Python (Part V) | **Python + Anaconda**, or lighter: plain Python + pip | Everything (pandas, matplotlib, scipy, statsmodels, jupyter) is free *by design*; Google Colab runs it on borrowed computers — no machine of your own required |
| BI / dashboards (Part VI) | **Power BI Desktop** (free), **Metabase** (free, self-hosted), **Apache Superset**, **Looker Studio** (Google, free), **Tableau Public** | Desktop is free and complete for building (Ch. 38); the others publish for free — Metabase on a $5 VPS or even a Raspberry Pi runs a real department dashboard |
| SQL at work-scale (Part III/58) | **PostgreSQL** (free, forever), DuckDB, **BigQuery sandbox** | Postgres is the industry's favourite open engine; the BigQuery sandbox is a real warehouse with free limits |
| Publishing / portfolio (Part VII) | **GitHub** free tier, **GitHub Pages**, **Streamlit Community** | The portfolio (Ch. 49), a personal site, and even Python-built interactive dashboards — hosted free |
| Data (Ch. 44) | The public landscape | Governments and agencies publish for free *on purpose* |

The point of the table is not the individual tools; it is the column header: **the profession runs on free software at its core** — Python, SQL engines, Git, the BI free tiers — because the expensive products (SPSS licences, Tableau Desktop, cloud at scale) are *employers'* purchases, not *practitioners'*. You can be fully, certifiably employable — portfolio, projects, dashboards, statistics — on $0. The book you just read was assembled that way.

## 61.2 The Honest Gaps

Where free genuinely falls short, stated so you plan rather than discover: **SPSS and Stata themselves** are paid (the trials are time-limited; PSPP covers the core menu statistics — Frequencies, Crosstabs, T-tests, regression — but not every procedure; Stata has no free twin: learn the concepts in jamovi, the syntax on the job, the "week not a year" argument of Ch. 29); **Power BI service sharing** needs a licence (Desktop files and export work around it — Ch. 43's ladder); **cloud scale** bills per use beyond the sandboxes (the sandbox tiers are enough to *learn* the dialect and the cost instinct — Ch. 58's lab); **collaboration platforms** (Slack, Notion, the office suites) are free-tier limited but fine for one. None of these gaps touches learning, practising, portfolio-building, or freelancing — they touch enterprise convenience, which is what salaries are for.

## 61.3 The $200 Upgrade Path

When income (or a first job, or a first client — Ch. 55) puts ~$200 in the toolkit budget, the order that buys the most capability per dollar:

1. **A comfortable second-hand laptop with 16 GB RAM** (~$150–250 if your current machine is the constraint) — RAM is the analyst's laptop spec: it is the difference between pandas struggling and pandas shrugging (Ch. 58's thresholds). Nothing else on this list matters if the machine swaps.
2. **A domain name (~$15/yr)** — `yourname.dev` pointed at GitHub Pages: the portfolio stops being a github.com path and becomes a destination (Ch. 49's shop window, upgraded).
3. **A VPS (~$5–10/mo)** — Metabase or Superset publicly visible, plus scheduled scripts (Ch. 37's cron, hosted): a *running* dashboard in your portfolio that a recruiter can click.
4. **One exam certificate** (Ch. 51's rule: only with exams — e.g. Microsoft's PL-300 Power BI Data Analyst, the one certification this book's Part VI maps to, exam fee ~$165 — often less with vouchers) — *after* the portfolio exists, never instead of it.
5. **Never**: paid course subscriptions as a first resort (the free moocs and vendor learning paths cover this book's entire territory), "premium" data (the public landscape exists), or tool licences a job will buy for you on day one.

## 61.4 Working Offline and on Thin Hardware

Constraints this book's readers may know well — intermittent power, metered data, shared machines — and the craft that keeps the profession open: **local-first tools** (Calc, SQLite/DuckDB, Python — all work fully offline; only the cloud chapters need a connection, and the sandboxes are patient); **small-footprint workflows** (Jupyter is heavier than plain `.py` scripts; VS Code runs lighter than full IDEs; DuckDB queries gigabytes where a spreadsheet cannot even open them — *light hardware with DuckDB outperforms heavy hardware with the wrong tool*); **batch the connectivity** (download datasets and documentation in one café session; git commits queue offline and push when the signal returns); **version everything** (the habit that makes shared machines safe: your work is the repo, not the machine — pull to any borrowed laptop and continue). And the perspective that is also a truth: **intermittent infrastructure builds better habits than abundant infrastructure** — the analyst who logs, scripts, and versions because re-doing is expensive has accidentally adopted the professional discipline that offices pay consultants to teach.

## 61.5 Tool-Agnosticism, the Permanent Skill

The final word on tools, from a book that taught five of them: **the tool is an accent; the language is the method.** Evidence: the translation table of Ch. 29 (six instruments, five dialects); the anatomy of Ch. 45 (tool-blind); the interview chapters (the tests probe the method, and the method transfers). The professional who *cannot* switch tools is a liability the day the employer switches; the professional who can, reads a new stack's documentation like a menu ("ah — this is GROUP BY with different brackets"). Practise the switch deliberately, once a year (Ch. 56's annual stretch): rebuild one portfolio project in a tool you have never used, in a weekend. The rebuild is always faster than the original — and the speed of that rebuild, felt firsthand, is the permanent, portable, $0 confidence this book has been building toward.

> **From Your Toolkit — the stack is free; the career is built:** the constraints chapter closes with its own inversion — you were never waiting on software licences. The stack above plus the habits of Parts I–VIII is a *complete* professional toolkit: Tariro's shop went from CSV to dashboard on it, and so did this book. What remains — the tenth part of nothing, the everything of it — is the decade, next chapter.

## Key Takeaways

- The $0 stack covers every Part: Calc/Sheets, SQLite/DuckDB, jamovi/PSPP, Python, Power BI Desktop + free publishers, GitHub — the profession's core is free by design.
- The honest gaps are employers' purchases: SPSS/Stata licences, service sharing, cloud scale — none touch learning or the portfolio.
- $200 order: RAM-comfortable laptop first, domain, VPS, then one exam certificate (PL-300) — never paid courses as first resort.
- Offline craft: local-first, light-but-right tools (DuckDB), batched connectivity, the repo as your working identity — constraints build the professional habits.
- Tool-agnosticism is permanent: rebuild one project in a new stack yearly — the method is the career; the accents are cheap.

## Practice Lab

1. The stack audit: build your personal $0 inventory table (what you have, what you'd add, from 61.1); install the two gaps; run one operation in each tool to verify — the shelf, verified.
2. The DuckDB hour: install it (single binary), point it at your biggest CSV, and run three of your saved SQL queries on it directly; note what "analytical database engine" means for a file you used to open in Calc.
3. The jamovi rebuild: redo Chapter 27's survey analysis in jamovi (menus only); confirm the identical χ² and p; write the three-line translation note (SPSS → jamovi) in your dialects file.
4. The publish, for free: get one interactive thing publicly online at $0 — Metabase/Superset screenshot export, a Looker Studio report, or a Streamlit app on the Community tier; link it from the portfolio README (and verify the link from someone else's phone).
5. The annual switch, rehearsed early: pick one tool you have *never* used from 61.1 (say, Superset or R); rebuild Project 1's one-pager in it over a weekend; time the rebuild vs the original; write the one-paragraph "switch cost" note — your personal evidence for Ch. 61.5's claim.

## Further Reading

- Chapter 62 (the decade — where this stack compounds), the tools' own sites (all linked from the free-tier philosophy above)
- duckdb.org's "why DuckDB" essay — fifteen minutes that will change your CSV life
