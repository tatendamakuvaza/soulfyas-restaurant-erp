# Chapter 42: Chart Craft, Again — the Dashboard Edition

*Part VI — Dashboards and Storytelling with Power BI*

> "Chapter 11 taught you to draw one honest chart. A dashboard is twenty honest charts agreeing with each other — which is a different, harder honesty."

### In this chapter you will learn

- The dashboard editions of the three chart lies — new costumes, same crimes.
- Visual consistency: the system of colour, sort, and scale that makes a page readable.
- Choosing the visual by the question — the chooser's table, extended for BI.
- Small multiples and the "compare across" moves dashboards make possible.
- Accessibility: the craft rules that include every reader.

## 42.1 The Three Lies, Dashboard Edition

Chapter 11's three lies return wearing business-casual, and dashboards give them new room to work:

1. **The truncated axis** now arrives *by default*: BI tools auto-scale axes to the data's range, so a revenue line from 9,100 to 9,400 auto-truncates without anyone choosing to lie. Fix deliberately: start value axes at zero for bars (always) and consider it for lines (state the choice in the visual's header if not); the auto-scale is a decision you inherit — and you are responsible for inherited decisions (the Chapter 20 rule, now about pixels).
2. **The unlabelled scale** multiplies: twenty visuals is twenty sets of axes, and a reader cannot remember which is dollars and which is counts. Fix with a *system*: currency to two decimals with thousands separators on every money visual, percentages to one decimal, counts as integers — set once in the measure's formatting (Chapter 40), inherited everywhere. When formats are part of measures, this lie becomes impossible.
3. **The dual-axis trick** reappears as "combo charts" (columns + line, two axes) — legitimate for genuinely different units (revenue and *count*), treacherous when both axes are money scaled to cross at flattering angles. The dashboard rule: dual axes only for different units, labelled on both sides, and never the chart carrying the page's main claim.

## 42.2 Consistency Is a System

One page, one visual language. The craft rules, each worth adopting permanently:

- **Colour means something, once.** EcoCash is teal *everywhere on the page and in every tooltip*; Sunday is amber in every weekday visual. Colour-as-category must be stable across visuals, or the reader re-decodes each chart from scratch — the palette is a dictionary, not a decoration. (Tariro's dashboard: teal = primary series, amber = attention/comparison, grey = context. Three colours; a fourth requires a meeting with yourself.)
- **Sort is a statement.** Ranked bars sort by value; time charts run left-to-right by date; category tables sort by the page's primary measure. "Alphabetical" is a valid choice only when the reader looks things up (a matrix of *items*) rather than compares them.
- **Scale is comparable.** If two charts on a page show the same measure, their axes should agree — or the disagreement is a lie by juxtaposition. Small multiples (42.4) are the systematic fix.
- **White space is load-bearing.** The reader's eye needs rest stops; cramming is not density, it is noise. Twelve clean visuals beat twenty cramped ones on every measure that matters, including speed.

## 42.3 The Chooser's Table, Extended

Chapter 11's question→shape table, extended with the visuals BI adds (and the traps each carries):

| The question | The visual | Trap to avoid |
|---|---|---|
| "How does it move?" | Line | Truncated auto-axis; too many lines (>4 = spaghetti) |
| "Which is biggest?" | Ranked bar | Alphabetical sort (says nothing) |
| "What's the mix, and how does it shift?" | 100% stacked bar | Legends hiding the shift — label the ends |
| "Same measure, many groups, compared?" | Small multiples | Inconsistent per-tile scales |
| "Where does the total come from?" | Waterfall | Random order — sort contributions by size |
| "Two numbers per group (risk vs size)?" | Scatter (bubbles) | Unlabelled outliers — label the interesting dots |
| "Exactly what are the numbers?" | Matrix/table | No total row; thousand-row detail with no top-N |
| "Where in the journey do they drop?" | Funnel | Unequal stage definitions |
| "Is this number okay?" | KPI card **with sparkline** | The naked number: no baseline, no trend |

That last row is the dashboard-era addition: the **KPI card with context** — a big number alone says nothing (compared to what? says who? — the Chapter 2 questions, miniaturised). The craft pattern: number + comparison (+8.4% vs LY) + sparkline (the last 12 months) + target marker if a target exists. Every headline card on a serious dashboard is that quartet, because a number without context is furniture pretending to be a finding.

## 42.4 Small Multiples and the Compare Moves

The move dashboards make possible that single charts cannot: **small multiples** — the same chart repeated once per group (revenue by month, one tile per suburb, one per till, one per payment type), sharing axes so comparison is honest *by construction*. Power BI: the "Small multiples" well on line/bar charts (drop `suburb` into it). It is the most underused first-class visual in the tool, and it is Chapter 2's "compared to what?" answered structurally — the baseline is built into the grid. Use it whenever the question contains the words "across" or "each of the".

Its siblings: **decomposition tree** (drill a total into its contributions interactively — the explorer's funnel), and the humble **scatter with play axis** (two measures over time, animated — occasional, memorable). Each has exactly one question it answers best; the craft is matching, not collecting.

## 42.5 Accessibility Is Chart Craft

The rules that make charts work for *every* reader, which is simply professionalism: **colour is never the only carrier of meaning** — pair it with labels, position, or shape (the ~8% of men with colour-vision deficiency read your dashboard too; teal-vs-amber is a colourblind-safe pair, one reason this book chose it); **contrast** — dark text on light ground, 12pt minimum, which conveniently is also the "readable in a meeting-room projector" setting; **alt text** on visuals (Power BI: Alt text property — screen readers and the same text serves your PDF exports); and **keyboard paths** (Tab through slicers, Enter to apply — test it once). None of this is decoration; it is the same honesty as labelled axes, extended from the chart to the reader.

> **From Your Toolkit — the craft layer, permanent:** these rules are tool-blind: they govern matplotlib exhibits (Chapter 35 — where you set the palette in a constants cell for exactly this reason), SPSS output charts, the Tableau dashboards you will meet, and every slide in Chapter 53's presentation. Chart craft was learned once in Chapter 11; what this chapter added is *system* — consistency, context, and the recognition that a page of charts is itself one chart, read as a whole.

## Key Takeaways

- The three lies, dashboard edition: auto-truncated axes (inherit decisions deliberately), format confusion (fix formats in measures, once), and combo-chart crossings (different units only, both axes labelled).
- Consistency is a system: colour-as-dictionary, sort-as-statement, comparable scales, load-bearing white space.
- The extended chooser: 100% stacked for shifting mixes, waterfalls for contributions, small multiples for "across", KPI cards only with context (number + comparison + sparkline + target).
- Small multiples make comparison honest by construction — use for every "each of the" question.
- Accessibility is craft: never colour alone, contrast and size, alt text, keyboard paths — honesty extended to every reader.

## Practice Lab

1. The audit, inward: run this chapter's rules against your Chapter 41 page — every axis (zero-baseline where owed), every format (is it in the measure?), every sort (statement or lookup?), colour dictionary (stable across visuals?); fix everything found and log the before/after screenshots.
2. The KPI quartet: upgrade your three headline cards to number + comparison + sparkline + (where real) target; screenshot the difference a sparkline makes to "Revenue: 3,401".
3. Small multiples, deployed: revenue by month as small multiples of suburb (or till); write the sentence the grid makes visible that a single line chart hid; check every tile shares the axis scale.
4. The colourblind check: view your page through a colour-vision simulator (many free online; or squint-test the greyscale); find any meaning that colour alone was carrying; fix with labels or position.
5. The one-page critic: find one public dashboard (Power BI gallery, Tableau Public, a news site's data page) and write a ten-line audit — the three lies, consistency system, chooser matches, accessibility — praising what deserves it. Critiquing outward sharpens building inward.

## Further Reading

- Chapter 43 (the story — presenting the page and its findings), *Storytelling with Data* (Knaflic) — the craft classic, whole-book version of this chapter
- The Power BI visuals reference (Microsoft Docs) — every visual, one line each
