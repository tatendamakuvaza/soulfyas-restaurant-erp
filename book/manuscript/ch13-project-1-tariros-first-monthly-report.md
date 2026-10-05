# Chapter 13: Project 1 — Tariro's First Monthly Report

*Part II — Excel: Your First Superpower*

> "Analysis unwritten is analysis undone. The report is where numbers become decisions."

### In this chapter you will learn

- How to plan a deliverable backwards from the decision it must support.
- The structure of the one-page monthly report: headline, three findings, one recommendation, appendix.
- How to assemble it from the work of Part II — no new analysis, all new craft.
- A self-review checklist that catches weak reports before your reader does.
- How to publish the artefacts (PDF, Excel file, one folder) like a professional.

## 13.1 Plan Backwards from the Decision

Tariro will read this report once, on Sunday evening, tired, deciding three things: **what to order more of, what to do about Sundays, and whether the loyalty scheme pays.** Every choice you make — every chart, every sentence — either serves one of those decisions or is furniture. That is the professional's planning trick, used on every deliverable for the rest of this book: **start from the decision, work backwards to the analysis, and let the audience's questions write your outline.** (Chapter 45 turns it into the portfolio case-study method; Chapter 52 into interview answers.)

The deliverable: **one page** (paper or PDF), three findings, one recommendation each, two charts, and an appendix sheet for the evidence. One page is not a limit — it is a kindness. If the reader wants more, the appendix exists; if they do not, you have still told them everything that matters.

## 13.2 The Analysis You Already Own

Nothing new is needed — Part II was the analysis; this chapter is assembly. Your evidence shelf:

- **Growth**: monthly revenue pivot and line chart (Ch. 10–11) — the steady climb, the payday rhythm visible as sawtooth.
- **The dip**: category × month pivot — cooking oil's slide from month 9, quantity-led (Ch. 8's split of the 8.42 into price × quantity).
- **Weekdays**: day-of-week statistics (Ch. 12) — Sundays are traffic-poor, not basket-poor.
- **Loyalty**: member vs non-member comparison (Ch. 9–10) — members' share of revenue and their bigger average basket, with the self-selection caveat.
- **Whales**: the outlier list (Ch. 12) — bulk buyers as a segment, concentrated in two suburbs.

## 13.3 The One-Page Structure

The template that carries every one-page report you will ever write — and Project 4's quarterly edition, and most of your first job's weekly output:

```text
TARIRO'S GROCERY — MONTHLY REPORT
Month 18, compiled from 18 months of till data

HEADLINE (one sentence, a number in it)
  Revenue grew 31% over 18 months; growth is broad-based
  but cooking oil has fallen 40% since the price rise.

FINDING 1 — What to order more of        [chart: top items bar]
  Staples drive 62% of revenue (top 3 categories). Maize meal
  and rice trend with the growth. RECOMMEND: increase standing
  order for top 5 items 20%; watch supplier terms.

FINDING 2 — The cooking-oil problem      [chart: category x month]
  Cooking oil revenue −40% since month 9, all quantity-led:
  customers buy 1.8 bottles/month vs 3.1 before. RECOMMEND:
  trial a cheaper brand for one month; measure switch rate.

FINDING 3 — Sundays and loyalty         [chart: weekday columns]
  Sunday revenue is 28% below the weekday average, entirely
  from fewer customers (baskets are normal). Members are 23%
  of customers but 31% of revenue. RECOMMEND: Sunday-only
  loyalty double-points; measure after 4 Sundays.

APPENDIX (separate sheet): method notes, data-quality log,
  full tables, the 412.00 sale's verification note.
```

Notice what the structure enforces: **every finding ends in a recommendation, every recommendation is measurable** ("measure switch rate", "after 4 Sundays") — because a recommendation nobody can check is a wish. And the headline is a *finding*, not a table of contents: the reader learns the story even if they read nothing else (Chapter 11's finding-title rule, promoted to a whole page).

## 13.4 Write the Sentences

The craft moves that separate your report from a spreadsheet printout:

- **Numbers in every sentence, units attached.** "Cooking oil has fallen 40% since the price rise" — not "cooking oil has declined significantly."
- **The caveat travels with the claim.** "Members are 23% of customers but 31% of revenue" is followed immediately by "members may always have been bigger spenders — the scheme's *causal* effect is unknown until Part IV's tests." One sentence of honesty, forever attached.
- **Past tense for what happened, present for what is true, future tense only under the word "recommend".** Grammar that keeps you out of trouble.
- **No chart without a finding title; no finding without a number; no number without its source** ("18 months of till data, cleaned per log").

## 13.5 The Self-Review Checklist

Before any report leaves your hands — this one, and every deliverable in this book, and your first job's work — run the checklist. It is Chapter 2's habits, assembled into a quality gate, and it is the closest thing this book has to a professional conscience:

1. **Could Tariro act on this?** (every finding → a recommendation → a measurable next step)
2. **Does the headline survive alone?** (read only the headline: is the story there?)
3. **Can every number be traced?** (appendix method notes; the reader could rebuild it)
4. **Are the caveats attached, not buried?** (self-selection, 18-month window, the data log's unresolved items)
5. **Is anything a chart that should be a table — or a sentence?** (charts show shapes; tables give exact values; sentences give verdicts)
6. **The three rules**: an average is an answer not the answer (median shown beside mean); correlation is not causation (the loyalty caveat); sample is not population (18 months is this shop, not all shops).
7. **One page?** (if it spilled, cut a finding, not a caveat.)

## 13.6 Publish Like a Professional

Artefacts, in one folder named for the deliverable and date (`tariros-monthly-report-m18/`):

- `report.pdf` — the one-pager, exported (File → Export as PDF), charts embedded.
- `analysis.xlsx` — the workbook: `raw`, `clean`, `customers`, `analysis` (pivots), `report` (layout) — one tab per stage, named, so a colleague could follow the trail.
- `log.txt` (or a `log` tab) — the data-quality log and method notes: every cleaning decision, the verification note for the 412.00 sale, the fence computation, the join checks. **The log is the part that makes you look senior.** Juniors deliver numbers; professionals deliver numbers plus the story of how much to trust them.
- A filename convention that sorts: `tariros-monthly-report-m18` — not `final`, not `final2_REAL`. (Version like a professional: `v1`, `v2`, or dates; "final" is a lie we have all told.)

## 13.7 Where You Stand

Close the workbook for a second and look at what happened: eighteen months of messy, human till data became three decisions a shop owner can make on Sunday evening. You did it with one tool, no code, no statistics beyond descriptives — and every habit that will carry you through SQL, Python, and Power BI is already in your hands: clean first, reconcile totals, join and check, summarise honestly, chart the finding, recommend something measurable, and log the whole journey.

Tariro's shop is about to get a second till and a supplier database — and the data is about to outgrow the spreadsheet. Time for a bigger engine.

> **From Your Toolkit — the report spine:** this one-page structure — headline, findings, recommendations, appendix, log — is the deliverable format of every project chapter remaining (Projects 1–6 and the portfolio). The tools underneath change (SQL, Python, Power BI); the page does not. Master this page and you have mastered the shape of the job.

## Key Takeaways

- Plan backwards from the decision the reader must make; the audience's questions write your outline.
- One page: headline finding, three findings each with a measurable recommendation, appendix for evidence.
- Numbers with units, caveats attached to claims, finding titles on charts — sentence craft is analysis craft.
- The self-review checklist is your quality gate: actionable, traceable, caveated, one page.
- Deliver artefacts like a professional: PDF + workbook + log, versioned, in one named folder.

## Practice Lab

1. Build the full deliverable on your Part II workbook: the one-page report (headline, three findings with recommendations, two charts with finding titles), the appendix sheet, and the log tab. Export to PDF.
2. The readability test: hand it to a friend for ninety seconds; ask them to state the three findings back. What they recall is what you communicated; what they miss is what you must fix.
3. The decision test: for each recommendation, write the measurement that would prove it right or wrong, and when that measurement will exist. A recommendation without a measurement date is a wish — fix any wishes.
4. Run the full self-review checklist on your own report, writing one line per item; fix everything the checklist catches, then re-export.
5. Portfolio seed: write the 150-word case-study note for this project now, while it is fresh (what, how, finding, impact) and store it with the folder — Chapter 45 will want it.

## Further Reading

- Chapters 44–45 (this deliverable becomes a portfolio case study)
- *The Pyramid Principle* — Barbara Minto (the deep theory of headline-first structure)
