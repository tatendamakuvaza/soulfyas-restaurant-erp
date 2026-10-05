# Chapter 41: Your First Dashboard

*Part VI — Dashboards and Storytelling with Power BI*

> "A dashboard is not a chart collection. It is a page that answers a reader's next question before they finish asking it."

### In this chapter you will learn

- Page architecture: the grid, the reading order, the five-second rule.
- Building Tariro's dashboard page by page — every element from the brief.
- Bookmarks, drillthrough, and tooltips: the interactions that make a page feel alive.
- The data-age stamp and the reconciliation card — honesty, embedded.
- Performance basics: why the page is slow, and the three usual fixes.

## 41.1 The Architecture of a Page

Dashboard layout is a design discipline with rules you can learn in an afternoon (Chapter 42 deepens the craft). The core: **readers scan top-left to bottom-right, big to small** — so the page is a *deliberate* hierarchy:

```text
+--------------------------------------------------------------+
|  TITLE + DATA-AGE STAMP + the slicers (month, till, payment)  |
+------------------------------+-------------------------------+
|  THE HEADLINE NUMBER(S)      |  THE MOVEMENT                 |
|  Revenue (big card)          |  Revenue by month (line)      |
|  MoM % (with LY comparison)  |                               |
+------------------------------+-------------------------------+
|  THE MIX                     |  THE STORIES                  |
|  Payment type (100% bar)     |  Sunday verdict | Oil trend   |
|  Top items (ranked bar)      |  Member share trend           |
+------------------------------+-------------------------------+
|  THE DETAIL (small, bottom): the table for the person who    |
|  wants exact numbers                                         |
+--------------------------------------------------------------+
```

The **five-second rule** governs every placement: glance at the page for five seconds; what did you learn? (Revenue, whether it's up, one thing that needs attention — if not, the top of the page is wrong.) The detail table at the bottom serves the reader who wants precision — the appendix instinct from Chapter 13, transposed. And nothing decorates: every visual earns its pixels by answering part of the brief, or it goes.

## 41.2 Building It, Page by Page

Open your `.pbix` from Chapter 40 — model built, measures named — and build the brief in order. The session, element by element (each element names the measure or chapter that powers it):

**The header.** A text box: "Tariro's Grocery — Trade Dashboard". Beside it, the **data-age stamp**: a card visual on a measure —

```dax
Data Age =
"Data through " & FORMAT(MAX('Calendar'[Date]), "d MMM yyyy")
```

— the brief's honesty requirement, implemented: a reader instantly knows whether they are looking at this month or last quarter's ghost. (This measure is text, so it lives as a card; it is also your staleness *monitor* — see 41.4.)

**The slicer rail.** Three slicers across the top (month from `Calendar`, till, payment type); Format → Single select off (readers combine); give them a consistent style. Every visual below respects them automatically — the model's filter propagation doing the work.

**The headline cards.** `[Revenue]`, `[Revenue MoM %]`, `[Revenue LY]` beside it — three cards, one row: *what, which way, against what baseline.* (Card visual, callout value formatted; the MoM card coloured conditionally — green above 0, red below — via Conditional formatting on the card: the glance-friendly version of Chapter 11's finding-title rule.)

**The movement.** Line chart: Axis = `Calendar[Month]`, Values = `[Revenue]`. Add `[Revenue LY]` as a second line — the year-over-year comparison the bank manager actually wants, on the chart itself.

**The mix.** A **100% stacked bar** of payment type by month (Axis = month, Legend = payment type, Values = `[Revenue Share]`-style percentage) — the EcoCash-share-rising story as a visible current; or simpler first pass: stacked bar with the mix measure. Beside it, **top items**: a ranked horizontal bar (`Top N` filter on the visual: Top 10 by `[Revenue]`) — Chapter 34's `nlargest`, clicked.

**The story tiles.** Two or three small visuals carrying the named stories: the Sunday verdict (weekday bar with Sunday highlighted — a weekday table + `[Revenue]`, Sunday's bar coloured via data labels), and the oil trend (line of oil revenue by month, showing the month-9 cliff). These are the dashboard's *sentences* — the brief's items that are stories, not statuses.

**The detail floor.** A matrix visual: rows = items, values = `[Revenue]`, `[Sales Count]`, `[Average Basket]`, sorted by revenue. The precision layer, for the reader who wants to quote a number in a meeting.

Then the polish pass, ten minutes that double the page's quality: align everything to a grid (Format → Align); consistent fonts and two colours (Tariro teal + amber, matching the report exhibits); visual headers phrased as findings-in-waiting ("Revenue by month — growth and the month-9 dip", not "Sum of amount by Month"); and the page named "Trade Overview" (a dashboard with more than one page is a navigation problem — see 41.3).

## 41.3 The Interactions

Three Power BI features turn a static page into a tool — implement at least the first two:

- **Tooltips.** Hover on any bar/point: the default shows values. Better: Format → Tooltip → place a small extra visual (the payment mix for the hovered month) — a reader's question answered *on hover*.
- **Drillthrough.** Right-click any month → Drill through → "Item detail" — a second page, pre-filtered to that month, showing the item-level table and the top-N bars. The Chapter 10 double-click drill-down, reborn: summary to evidence in one right-click. Build the target page once, set its drillthrough field (`Calendar[Month]`), and every visual gains the path.
- **Bookmarks.** Saved states of the page (filters, visibility) — "Reset" (clears slicers; the small kindness every reader appreciates) or toggled focus views. Optional craft; the Reset bookmark alone is worth it.

## 41.4 The Honesty Layer

Two small elements, permanent policy on every dashboard you ever ship: the **data-age stamp** (built above) and the **reconciliation card** — the `[Revenue]` card, checked once against the bridge total whenever the data refreshes (Chapter 39's guard, kept visible or at least kept in a "Checks" hidden page). Together they answer the two questions every honest dashboard owes its readers: *how fresh is this?* and *can I trust the total?* A third belongs in your publishing checklist: **the checks page** — a hidden page with the bridge, the null counts, the orphan count as card visuals — so that *you* can open the file on refresh day and see the whole liturgy at a glance. (Chapter 37's fail-loudly guards, transposed: the pipeline aborts on broken data; the dashboard *displays* its health.)

## 41.5 Performance, the Short Version

If the page is slow (spinner on every click), the causes are almost always three, in this order: **visuals showing too much** (a table of 6,420 rows rendered — top-N it or aggregate); **measures that scan repeatedly** (the same ALL/CALCULATE pattern in ten visuals — simplify the model, or pre-aggregate in Power Query); **too many visuals** (each one is a query; twenty visuals is twenty queries per click — cut to the ones that answer the brief). The debugging tool is **View → Performance analyzer**: record a refresh, see per-visual timings, fix the slow one — the EXPLAIN habit of Chapter 20, pointing at pixels instead of queries.

> **From Your Toolkit — the deliverable template:** this page — header/stamp, slicer rail, headline cards, movement, mix, stories, detail floor, checks page — is the skeleton of every operational dashboard you will ever build (Project 6 extends it; your first job's "can you improve our weekly dashboard?" inherits it). The visuals change; the architecture — hierarchy, honesty layer, drill paths — is the craft that transfers.

## Key Takeaways

- A page is a hierarchy, not a gallery: five-second headline, movement, mix, stories, detail floor — reading order is design.
- Build the brief in order: stamp and slicers first, cards, line with LY, mix, top-N, story tiles, matrix floor; then the polish pass (grid, palette, finding-phrased headers).
- Tooltips, drillthrough, and the Reset bookmark are the interactions that make a page feel alive — implement at least tooltips and drillthrough.
- The honesty layer ships always: data-age stamp, reconciliation card, hidden checks page — freshness and trust, visible.
- Slow pages: too much data shown, repeated heavy measures, too many visuals — Performance analyzer is EXPLAIN for pixels.

## Practice Lab

1. Build the full Trade Overview page on your model — every element from the brief, the polish pass included; save `tariro-trade.pbix`. Screenshot the finished page for the log and the portfolio.
2. The five-second test: hand the file (or screenshot) to a friend for five seconds; ask what they learned. Whatever they missed, move up or enlarge. Iterate until the headline survives the glance.
3. The drillthrough build: an "Item detail" page (matrix + top-N bars + month context card), drillthrough on month; test the path from three different visuals; write the two-line note a reader would need (or does the page explain itself?).
4. The checks page, built: bridge card, null-count cards, orphan count, data age — hidden but complete; open it after a refresh rehearsal (Ch. 39's lab data) and log what you see.
5. Performance analyzer run: record, sort by duration, screenshot the slowest visual, and fix it (top-N, simplify, or cut); record before/after — a portfolio-ready micro-story: "dashboard interaction from 3.2s to 0.4s by removing two visuals and top-N-ing the table".

## Further Reading

- Chapter 42 (chart craft at dashboard scale — the rules, intensified), Chapter 43 (presenting the story)
- Microsoft Learn: "Create and use analytics reports in Power BI" — the official companion
