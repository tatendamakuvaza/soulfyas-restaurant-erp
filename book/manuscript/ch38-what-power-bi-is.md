# Chapter 38: What Power BI Is

*Part VI — Dashboards and Storytelling with Power BI*

> "A report tells you what happened. A dashboard waits to be asked — and answers in the time it takes to wonder."

### In this chapter you will learn

- What Power BI is (and is not), and the free-vs-paid line that matters.
- The three surfaces: report, dashboard, and the workflow that connects them.
- Why dashboards change the analysis job — from answering to *anticipating*.
- The Power BI workflow in one page — get data, model, measure, visual, publish.
- Installing Power BI Desktop and taking the ten-minute tour.

## 38.1 The Tool and Its Place

Power BI is Microsoft's business-intelligence platform: load data, build a **data model** (tables and relationships — you know these), define **measures** (calculations with names — you know these too), arrange visuals into an interactive **report**, and publish it so readers can explore with filters and slicers instead of waiting for next month's PDF. Its siblings in the wider world — Tableau, Looker, Qlik, Metabase, Superset — share the same skeleton; Power BI is the most common in Microsoft-world business, and the one this book teaches (Chapter 61 maps the free alternatives).

The free/paid line, stated precisely because it decides your learning path: **Power BI Desktop is completely free** — the full authoring experience, unlimited local reports, everything this Part needs. What costs money is **sharing**: the Power BI service (publishing to the web, app workspaces, scheduled refresh, row-level security) is where licences enter. Learning, building, and demonstrating a portfolio on Desktop: free. Publishing to an organisation: your employer's licence problem, solved on day one by IT. Download Desktop from microsoft.com (Windows; Chapter 61 covers the macOS and browser paths honestly).

## 38.2 What Changes When You Build Dashboards

Everything so far in this book answered *questions you were asked*: this month's revenue, the oil collapse, Sunday's verdict. A dashboard inverts the relationship — you must *anticipate* the questions. The reader (Tariro, her bank manager, a department head) will open the page at any moment, click any filter, and expect an answer *now*. Three consequences, and they are thePart's real syllabus:

1. **The numbers must be right for every slice.** Revenue filtered to March, to EcoCash, to Tuesdays — every combination must compute correctly, which means the *model* must be right (Part III's keys and fan-out lessons, now structural) and the *measures* must handle every context (DAX's specialty, Chapter 40).
2. **The page must answer in five seconds.** Not performance (though that too) — *reading speed*: the reader glances, clicks, glances. Chapter 11's chart grammar becomes Chapter 42's page grammar: layout, hierarchy, the headline that survives a skim.
3. **The data must refresh itself.** A stale dashboard is a lie with a date on it. Part V's automation mindset returns as scheduled refresh — the pipeline feeds the dashboard.

And the honest boundary, said now and repeated in Chapter 43: **a dashboard does not replace the report.** Dashboards answer the recurring questions ("how are we doing?"); reports answer the deep ones ("*why* did oil collapse and what should we do?"). The monthly report of Project 3 survives; the dashboard absorbs the questions it was being asked repeatedly.

## 38.3 The Workflow in One Page

The whole of Part VI is this loop, six stages, every one an old friend in a new accent:

```text
1. GET DATA      -- CSV, database, web: the loading liturgy (Ch. 39)
2. SHAPE         -- Power Query: clean, typed columns, the Chapter 8 work, recorded
3. MODEL         -- tables + relationships: the star, the keys (Ch. 39)
4. MEASURE       -- DAX: named calculations like revenue, MoM %, member share (Ch. 40)
5. VISUAL        -- charts on a page, filtered, interactive (Ch. 41–42)
6. PUBLISH       -- to the service, scheduled refresh, shared (Ch. 43)
```

Notice what is *not* in the loop: ad-hoc cell edits, hand-typed numbers, copy-paste between files. The dashboard is compiled from a model, the model from sources, the sources checked by queries — the audit trail Chapter 20 demanded, embodied in a tool. When your manager asks "where does this number come from?", the answer is a *lineage view*: visual → measure → table → source, clickable. That is the professional difference between a dashboard and a spreadsheet emailed on Mondays.

## 38.4 The Ten-Minute Tour

Install Desktop (free, from Microsoft's site), open it, and take the tour before Part VI begins properly — hands on the wheel for ten minutes:

1. **Get data → Text/CSV** → your cleaned `sales.csv`. The preview appears; click Load. (Transform Data — Power Query — waits for Chapter 39; Load is fine today.)
2. The **Fields** pane (right) lists your table and columns. Drag `amount` onto the blank page: a table visual appears. Now drag `payment_type` onto it — a pivot, instantly.
3. With the visual selected, open the **Visualizations** pane and click the clustered-column chart icon: it becomes a bar chart of revenue by payment type. You have just built the pivot → chart pipeline of Chapters 10–11 with two drags.
4. Drag `date` into the visual's **Axis** area and watch it group by month automatically — the time intelligence beginning.
5. **Insert → Slicer**, drag `payment_type` into it: a clickable filter. Click EcoCash; the chart obeys. *That click is the entire meaning of "interactive" — the reader is now querying your model themselves.*

Ten minutes, five moves, and the shape of the Part is in your hands. Everything remaining is depth: shaping properly (39), measuring properly (40), pages that read fast (41–42), and telling the story when the dashboard's job is done (43).

## 38.5 Tariro's Brief

The Part's running brief, from Tariro and her bank manager, gives the next six chapters their spine — a real deliverable, specified like a work request:

> *"We want a dashboard the bank manager can open the morning of the quarterly meeting, and Tariro can open any evening: revenue and how it's moving, the payment mix, the Sunday situation, the oil story, the loyalty share, and the top items — with the ability to look at any month, any till, any payment type. And it must show its own data age — no stale numbers."*

Read the brief and see the syllabus: movement (time intelligence), mix (percent-of-total), the Sunday situation (a test's verdict, displayed), top-N (ranking), slicing (filters), and *data age* — the refresh stamp, the honesty requirement. By Chapter 43 it exists; Project 6 (Chapter 48) extends it into the operations dashboard — the portfolio piece that shows employers you can build for a *reader*, not just compute for yourself.

> **From Your Toolkit — the fifth tool, the same atoms:** Power BI is the book's fifth language, and its nouns are all borrowed: relationships are Chapter 17's keys (the model view *is* the diagram you learned to draw); measures are named formulas with Chapter 34's semantics; the slicer is a WHERE the reader types with their hand; the refresh is Chapter 37's cron wearing a GUI. Nothing new to understand — only a new accent to speak, and a genuinely new discipline: designing for readers you will never watch.

## Key Takeaways

- Power BI Desktop is free and complete for learning, building, and portfolio; only *sharing* (the service) costs licences.
- Dashboards invert the job: anticipate questions, be right for every slice, answer in five seconds, refresh yourself — and they complement, not replace, reports.
- The workflow: get data → shape (Power Query) → model → measure (DAX) → visual → publish — the audit trail embodied, lineage clickable.
- The ten-minute tour already covers pivot→chart→slicer: the reader is querying your model with clicks.
- Tariro's brief is the Part's deliverable: movement, mix, Sunday, oil, loyalty, top-N, slicing — plus the data-age stamp.

## Practice Lab

1. Install Power BI Desktop (or set up the browser alternative from Chapter 61's notes); take the ten-minute tour on `sales.csv`; save as `tariro-tour.pbix`.
2. Slicer drill: build the payment-type slicer plus a month slicer; click combinations and watch the chart recompute; write down three questions a reader could now answer *without you* — the inversion, experienced.
3. The lineage hunt: with your visual selected, use View → Performance/lineage features (or Model view) to trace visual → table → source; screenshot the lineage for your log — the "where does this number come from" answer, embodied.
4. The brief, annotated: re-read Tariro's brief; for each requirement, write which chapter of Part VI you expect to deliver it; keep the page — Chapter 43 checks it off.
5. The competitor skim (30 minutes): look at Tableau Public and Metabase's demo pages; write one paragraph: what all three tools share (the skeleton), and one thing each does differently — the tool-agnosticism of Part III's Chapter 20, applied to BI.

## Further Reading

- Chapter 39 (getting data in and the model — where correctness is decided)
- Microsoft's "Get started with Power BI Desktop" learning module — free, and painless after this chapter
