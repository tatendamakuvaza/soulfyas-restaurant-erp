# Chapter 29: SPSS and Stata, Gently

*Part IV — Statistics Without Fear*

> "Some tools you choose. Some tools you inherit. SPSS and Stata are the family silverware of statistics — and you will be invited to dinner sooner than you think."

### In this chapter you will learn

- What SPSS and Stata are, where you will meet them, and how they differ in spirit.
- The SPSS workflow, complete: data view, variable view, menus, output, syntax.
- Stata for beginners: the command line, the do-file, and why it is loved.
- Reproducing Part IV's analyses in both — a translation table you keep.
- What employers mean by "SPSS/Stata experience" — and how to get it honestly.

## 29.1 The Classic Tools

Python (Part V) is the general-purpose language of modern data; **SPSS** and **Stata** are the *specialised* statistics packages — decades old, beloved in the fields that grew up with them, and still running the numbers in governments, hospitals, universities, central banks, and market-research houses across the world. The geography of encounter, so it never surprises you:

| Tool | Where you'll meet it | Spirit |
|---|---|---|
| **SPSS** (IBM) | Social sciences, health research, market research, survey shops, psychology | Menus and dialogs; point-and-click statistics; output as pretty tables |
| **Stata** | Economics, epidemiology, policy evaluation, academia | Command line; everything scripted in "do-files"; reproducibility as religion |
| (SAS, R) | Pharma/clinical trials; statistics research & data science | Mentioned for completeness — R appears again in Chapter 57's world |

The one-sentence contrast you can say in an interview: *SPSS is the tool that puts statistics in menus; Stata is the tool that puts statistics in sentences.* You have already used SPSS's menus (Chapter 27's cross-tab); this chapter completes the picture and gives Stata its first honest hour.

## 29.2 SPSS, the Complete Workflow

Everything SPSS does happens in four windows, and this book's habits map onto them one-to-one:

1. **Variable View** (the data dictionary, made visible): every column has Type, Label, **Values** (the value labels — 1 = "Gold", 2 = "Silver" — categorical hygiene lives here), Missing (declared missing codes — the Chapter 15 NULL discipline, GUI edition), and Measure (Nominal/Ordinal/Scale — you declaring what each column *is*, which SPSS uses to offer sensible menus). Fifteen careful minutes here saves every hour after; skipping it is how "averaged the suburb codes" is born.
2. **Data View**: the grid — one row per unit (respondent, sale, patient). SPSS will happily let you type in it; the professional reads it, cleans elsewhere, and documents.
3. **The dialogs** (Analyze menu): Descriptives and Frequencies (Ch. 22), Explore with plots (Ch. 23's histograms and the five-number summary), Crosstabs with chi-square (Ch. 27), Compare Means → T tests (Ch. 26), Correlate and Regression (Ch. 28). Each dialog is a chapter you have already lived; the buttons are in Appendix C's walkthrough.
4. **The Output Viewer**: results as formatted tables with significance stars and footnotes — the tables you now *read fluently* because this Part taught the six lines every test prints (statistic, df, p, effect, interval, n).

And the feature that elevates SPSS from calculator to profession: **Syntax**. Every menu run can Paste (instead of OK) its commands to a syntax window, saved as a `.sps` file, and re-run — SPSS's version of the query pack from Chapter 21. The working habit, identical to SQL etiquette: *menus to explore, syntax to deliver.* Your Chapter 27 cross-tab, pasted as syntax, is two lines that reproduce the finding on next month's data:

```text
CROSSTABS TABLES=sunday_intent BY tier
  /CELLS=COUNT ROW /STATISTICS=CHISQ.
```

## 29.3 Stata, the First Honest Hour

Stata has no menu-first culture; it has a **command line** and the **do-file** — and the culture is this book's culture (reproducible steps, named files, documented decisions) in its purest form. The canonical session:

```stata
* tariro_analysis.do -- monthly pack, Stata edition
import delimited "sales.csv", clear
describe
summarize amount, detail

* the Sunday test (Ch. 26): two-sample t
gen weekend = cond(dayname == "Sun", 1, 0)
ttest takings, by(weekend)

* the price relationship (Ch. 28)
regress bottles price
```

Read the shape of it: `*` comments (the why, as always), one command per line, each command an English verb with options after the comma. `summarize, detail` is Chapter 22's five-number summary; `ttest, by()` is the Sunday courtroom; `regress` is the line of best fit. Results print to a log; the do-file plus the log *is* the analysis — an auditor (or your successor) re-runs the do-file and watches your numbers re-emerge. That is Stata's beloved property, and it is the destination this book has been steering you toward since Chapter 8's log: **analysis as a document, not a performance.**

The beginner's Stata kit (Appendix C expands): `import delimited`, `describe`, `summarize`, `generate` (new variables), `keep`/`drop` (rows and columns), `tabulate` (cross-tabs, with `chi2`), `ttest`, `regress`, `save`. Every one maps to a chapter behind you — the translation table below is the proof.

## 29.4 The Translation Table

The deepest lesson of this chapter: you have already learned the analysis; the tools are accents. Keep this table; it is the Rosetta Stone of interviews (Chapter 52 will quiz it):

| The task | Excel/Sheets | SQL | SPSS | Stata | Python (ahead) |
|---|---|---|---|---|---|
| Typical value | AVERAGE/MEDIAN | AVG, PERCENTILE_CONT | Descriptives/Frequencies | summarize | .mean()/.median() |
| Five numbers | QUARTILE | PERCENTILE_CONT | Explore | summarize, detail | .describe() |
| Cross-tab | PivotTable | GROUP BY two cols | Crosstabs | tabulate x y, chi2 | pd.crosstab |
| Two-group test | T.TEST | (CTE + arithmetic) | Independent-Samples T | ttest, by() | ttest_ind |
| Paired test | T.TEST paired | (CTE + arithmetic) | Paired-Samples T | ttest a=b | ttest_rel |
| Association | CORREL | (arithmetic) | Correlate | correlate/pwcorr | .corr() |
| The line | Trendline | (arithmetic) | Regression | regress | linregress/ols |
| Reproducible pack | Workbook+log | .sql files | Syntax .sps | Do-file .do | Notebook/script |

Two columns you have not yet earned (Python's) fill in during Part V; the table is the syllabus's own map. When an interviewer asks "you know Stata, not SPSS — how long to be useful?", the honest, winning answer is built from this table: *the statistics are the same six instruments; the syntax is a week, not a year.*

## 29.5 Getting Experience, Honestly

Employers in SPSS/Stata worlds ask for "experience with the package" — and the honest way to have it is to have *done the analyses*, because the package is 10% of the difficulty. The plan, all free or cheap:

1. **SPSS**: IBM's free trial (full package, time-limited) and many universities' free student licences; PSPP (the GNU clone) runs Frequencies/Crosstabs/T-test if licensing blocks you. Rebuild Chapter 27's survey analysis end-to-end, in syntax, saved.
2. **Stata**: no free full version, but the affordable student licence and the free **Stata tutorial datasets** (`sysuse auto`) make the first hour real; rebuild the Sunday test and the oil regression as a do-file, commented, logged.
3. **The portfolio line, earned**: "Statistics in Excel, SQL, SPSS and Stata: hypothesis tests, cross-tabs, chi-square, regression — same analyses, four tools" — and Projects 2–3's artefacts as evidence. That sentence, *backed by artefacts*, is worth more than any course certificate, and Chapter 46 will show you how to display it.

Part IV closes here. You can describe (typical values, spread, shape), standardise (z, percentiles), argue from samples (SE, CI), and conclude (tests, chi-square, correlation, regression) — in four tools, with the honesty rules enforced throughout. Tariro's ledger is closed: Sundays are real (t = 18.4), the price rise bit (p ≈ 0.0008, ≈1.1 bottles per dollar), loyalty is suggestive-not-proven (χ² p ≈ 0.064) and pending its trial. What remains is the *labour*: every month, the same cleaning, joining, testing, charting, reporting — by hand. Part V's Python automates exactly that.

> **From Your Toolkit — the family silver:** SPSS and Stata are not detours from this book's path; they are the same road wearing older asphalt. Every habit — the dictionary before the analysis, syntax over menus, the do-file as deliverable, the six-line output read — is a habit you already own from spreadsheets and SQL. The table above is your certificate of transfer.

## Key Takeaways

- SPSS = menus and pretty output (surveys, social science, health); Stata = commands and do-files (economics, policy); both run the same six instruments you now command.
- SPSS workflow: Variable View dictionary → Data View → Analyze dialogs → Output; Paste-to-Syntax turns menus into the reproducible pack.
- Stata: verbs with options, do-file plus log = the analysis as document — reproducibility as religion, this book's habits in purest form.
- The translation table: statistics is the skill; tools are accents — a week, not a year, to convert.
- "Package experience" is earned by rebuilding the analyses you already understand, in syntax/do-file form, and filing the artefacts as portfolio evidence.

## Practice Lab

1. SPSS hour: install (trial/university/PSPP), rebuild the survey analysis of Chapter 27 end-to-end — variable labels, Frequencies, Crosstabs + χ² — then Paste it all to syntax, save `survey_ch27.sps`, and re-run it from a blank output viewer. Log the two minutes the re-run took.
2. Stata hour (or Stata-in-spirit): with `sysuse auto` (or any CSV), run describe, summarize detail, a tabulate with chi2, and one regress; save as `first_hour.do` with a header block and why-comments; save the log beside it. Two files, portfolio-grade.
3. Translation drill: pick three analyses from your Part IV log; write each in *two* tools from the table (spreadsheet+SPSS, SQL+Stata, any pair); reconcile the p-values and coefficients to three decimal places; note every discrepancy and its cause.
4. The conversion memo: a half-page to a hiring manager (Chapter 51's audience) — "my statistics are tool-agnostic; here is the translation table and three artefacts proving it"; attach the table. This is a CV paragraph rehearsed as a document.
5. Part IV retrospective: one page — the three findings you closed, the two habits that caught the most errors, and the one idea (sampling distributions? the three explanations?) you would explain to a colleague tomorrow. File it with the portfolio; Project 3's write-up begins here.

## Further Reading

- Part V (Python — the automation of everything this Part did by hand)
- UCLA's IDRE "Which test?" pages and Stata/SPSS learning modules — the internet's best free companions to this chapter
