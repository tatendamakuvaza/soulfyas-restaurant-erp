# Chapter 48: Project 6 — The Operations Dashboard

*Part VII — Real Projects and Your Portfolio*

> "The trade dashboard asked 'how are we doing?'. The operations dashboard asks 'what do we do on Monday morning?'"

### In this chapter you will learn

- Operations analytics: the shift from describing trade to running the shop.
- Stock analytics: days-of-cover, the reorder signal, and the missing-week problem.
- Staffing analytics: the weekday×hour heat map, and Sundays, finally acted upon.
- Building the operations dashboard: the page, the alerts, the drill paths.
- Portfolio evidence #6: shipping the full stack, end to end.

## 48.1 The Brief

Tariro's Part VI dashboard serves the quarterly meeting. This project serves the *back office* — the weekly operational rhythm: what to order, how to staff, what to watch. The brief, anatomy-first: *build the page Tariro opens on Sunday evening to plan the week: stock risk (what runs out before the next delivery), staffing (how many hands, which hours), and the live trials (the Sunday promotion and the oil shelf test, both from earlier chapters) with their pre-agreed thresholds. Audience: Tariro, weekly. Success: order and roster decisions made from the page in fifteen minutes.*

Note what changed from the trade dashboard: the reader's *action horizon* collapsed from a quarter to a week — so the page's centre of gravity moves from trends to *thresholds*: numbers against lines, alerts against amber, "days remaining" against "days until delivery". Operations analytics is description converted into triggers.

## 48.2 Stock: Days of Cover

The core stock metric, small and mighty: **days of cover** = quantity on hand ÷ average daily quantity sold. Forty-five bottles of oil against an average 4.2/day ≈ 10.7 days of cover; the next delivery is in 7 days; therefore order enough for the *gap plus* a safety margin (cover target 14 days: order = (14 − 10.7) × 4.2 ≈ 14 bottles). One formula, one reorder logic — and in pandas, one more pipeline (the stock table joined to item daily averages; a `days_cover` column; a `reorder_flag` where cover < days-to-delivery + safety):

```python
stock["avg_daily"] = stock.merge(
    item_daily, on="item", how="left")["qty_sold_daily"]
stock["days_cover"] = stock["qty_on_hand"] / stock["avg_daily"]
stock["reorder"] = stock["days_cover"] < (days_to_delivery + 2)
```

And the missing weeks — the design's planted data flaw (three stock weeks absent) — return as an *operations* lesson, not just a cleaning one: the Sunday stock count is a *process*, and processes skip. The dashboard's stock page therefore carries a **count-freshness flag** (weeks since last count, from the data's own timestamps — the data-age stamp of Chapter 41, applied to a business process): a stale count must not masquerade as a current position. The professional insight this plants: *operational dashboards must monitor their own inputs' health* — the missing weeks are a finding about the shop, surfaced as a visible alert rather than silently interpolated away.

## 48.3 Staffing: the Heat Map

The staffing question — how many hands, which hours — is answered by one visual: the **weekday × hour heat map** of customer counts (transactions per hour, from the till timestamps). Build it in pandas (`pivot_table` weekday × hour, matplotlib `imshow`/heatmap) and then as the Power BI matrix with conditional formatting — the shop's whole weekly rhythm in one rectangle: the Saturday 10:00–13:00 block glowing; the weekday 16:00–18:00 after-work shoulder (school runs, dinner ingredients); the Sunday flatness, now quantified *hour by hour*.

The staffing rules that fall out (with numbers attached): two hands for any block averaging >30 customers/hour (the after-work shoulder needs them too — the finding the monthly average hid); one hand suffices Sundays 14:00+ (traffic, not baskets — Project 1's verdict, operationalised); and the payday Friday exception (the +⅓ spike): the roster template carries a payday variant. Each rule is a threshold on the heat map — and the honest caveat rides along: 18 months of averages recommend; the actual Saturday (a funeral, a football crowd, rain) decides. Averages staff the *usual*; humans staff the day.

And the Sunday promotion — the running trial from Projects 4–5 — gets its tile: this Sunday's revenue against the pre-agreed baseline weeks, the four-Sunday threshold visible as a target line, the kill/scale decision date printed. The dashboard closes the loop this book opened in Chapter 5: a question became a test; the test's instrument is now a live tile; the decision will be made on data, on schedule.

## 48.4 Building the Page

The operations page in Power BI, on the Part VI model plus the stock table (a second fact table — the model grows a constellation: sales facts and stock facts around shared dimensions — the shape you will inherit at every employer):

- **Header**: "Operations — week of [date]" + the input-health strip (last stock count age, last till sync, data through).
- **Left third — stock risk**: table of items by days-cover ascending, `reorder` flag as conditional-format colour, a suggested-order column (the 48.2 arithmetic, as a measure), the count-freshness flag on top.
- **Centre — the heat map**: weekday × hour matrix of customer counts; drillthrough to the item-level transactions for any hot block.
- **Right third — staffing rules + trials**: the threshold tiles (blocks needing two hands, this week's payday variant), and the Sunday-trial tile with its target line and decision date.
- **The checks page**, inherited and extended: bridge totals, nulls, orphans, stock-count age — the honesty layer, watching a busier shop.

The build session is Chapter 41's method repeated at higher fluency — and if you follow the labs, the page ships in a long evening, because every component is a chapter you have already lived. That fluency *is* the portfolio claim: not "I have used Power BI" but "I can take a warehouse-shaped model to an operational page with alerting thresholds in a day."

## 48.5 Shipping the Stack

Portfolio evidence #6, and the capstone of the project set. The folder: `operations-dashboard/` — the `.pbix` (with the checks page), the stock-analysis notebook (the days-of-cover pipeline, restart-clean), the heat-map exhibit, the staffing-rules memo (one page, thresholds with numbers), and the 150-word note: *Situation: a grocery's weekly order/roster decisions, made monthly in a spreadsheet. Work: days-of-cover reorder logic; weekday×hour heat map; trials with pre-agreed thresholds; BI page with input-health alerts. Finding: two-handed staffing needed on the weekday shoulder the averages hid; stock reorder signal with count-freshness honesty. Impact: weekly planning in fifteen minutes on one page. Limits: synthetic-labelled; averages staff the usual, humans staff the day.*

The six-project ledger is complete — Excel, SQL, Python, statistics, SPSS-adjacent survey craft, Power BI — one shop, one story, every tool, every honesty rule, every artefact versioned and logged. Chapter 49 assembles it into the portfolio that gets you hired; Part VIII arms you for the hunt itself.

> **From Your Toolkit — thresholds, everywhere:** operations analytics — stock, staffing, queues, capacity, on-call alerts — is the same move in every industry: a metric, a threshold, a freshness flag, and a drill path to the evidence. Retail runs it on days-of-cover; hospitals on bed occupancy; factories on downtime; SaaS on error rates. The dashboard you just built is a *pattern* with retail nouns; substitute the nouns and it is every operations page you will ever be paid to build.

## Key Takeaways

- Operations analytics = description converted into triggers: metrics against thresholds, alerts against amber, freshness flags on inputs.
- Days of cover (on hand ÷ daily rate) + delivery gap + safety margin = the reorder signal; missing stock counts become input-health alerts, not silent interpolations.
- The weekday × hour heat map answers staffing; thresholds with numbers, plus the payday variant; averages staff the usual, humans staff the day.
- The page: stock risk (left), heat map (centre), staffing + live trials with target lines and decision dates (right), checks page inherited.
- Six projects, one dataset, every tool — the portfolio's raw material is complete; Chapter 49 builds the shop window.

## Practice Lab

1. The stock pipeline: days-of-cover for every item, the reorder flag, the suggested-order column; reconcile three items by hand (bottles, math, log); export this week's order list as CSV — an artefact a real shop could act on.
2. The heat map, both ways: pandas/matplotlib exhibit *and* the Power BI matrix with conditional formatting; compare the two builds in five lines of log notes (effort, fidelity, refresh).
3. The staffing memo: one page — the thresholds, their numbers, the payday variant, the Sunday decision (with the trial tile's current status); write it for Tariro's fridge door, not for an analyst.
4. The page, built: the full operations dashboard with input-health strip, drillthroughs, and the trials tile; screenshot; five-minute walkthrough rehearsed (Ch. 43) with the order/roster decisions as the ask.
5. The ledger closed: all six 150-word notes in one file, STAR paragraphs beside them; the Chapter 45 checklist run once more across the project set. Read the ledger top to bottom — that hour is the fastest career-confidence you will ever buy.

## Further Reading

- Chapter 49 (the portfolio — the ledger becomes a shop window), Chapter 57 (the industrial versions of these patterns)
- "Retail ops analytics" case studies on any BI vendor's blog — recognise your own work in enterprise clothing
