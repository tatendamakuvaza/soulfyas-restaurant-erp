# Chapter 11: Charts That Tell the Truth

*Part II — Excel: Your First Superpower*

> "A chart is an argument drawn in ink: it claims something, and its axes are its evidence."

### In this chapter you will learn

- The five charts that cover almost everything, and which to reach for first.
- How to build each in Calc/Excel, step by step, on Tariro's data.
- The three lies charts tell — and how to never tell them by accident.
- Titles that state the finding, not the furniture.
- The one-minute chart audit you will run forever.

## 11.1 Five Charts, Honestly

Almost every working chart is one of five shapes. The question in your head picks the shape:

| Question you are answering | Chart | On Tariro's data |
|---|---|---|
| "How do these compare?" | Column (vertical bars) | Revenue by category |
| "How does it move through time?" | Line | Monthly revenue, the bank-manager chart |
| "Which is biggest, ranked?" | Bar (horizontal) | Top 10 items by revenue |
| "Are these two related?" | Scatter | Basket size vs time of day |
| "What is it made of?" | Stacked bar (rarely pie) | Payment types per month |

The pie chart's demotion is deliberate: human eyes judge length well and angle poorly, so a bar of the same data is almost always clearer. Pies survive only for two-to-four slices where exact size matters less than the existence of shares ("about half Ecocash"). The scatter plot is the sleeper — Part IV's correlation chapter (28) lives inside it — and the line chart is the most-abused (its crimes are next).

## 11.2 Building Them

The universal recipe, twice practised and then yours:

- **Monthly revenue line:** pivot `date` (grouped by month) against Sum of `amount`; select the pivot; Insert → Chart → Line. Done: eighteen months of trading in one picture. Now the polish that matters: click the title and *replace the furniture with the finding* — "Revenue: steady growth, payday rhythm, one dip" beats "Sum of amount by Month" the way a sentence beats a cough. Add axis labels (the chart tool's side panel) with units: "Revenue (USD)".
- **Category column chart:** pivot category by Sum of amount, Insert → Column. Sort the source pivot descending so the story ranks itself. When labels collide (15 categories), rotate to the horizontal bar — long names fit on the left edge, and ranking reads top-to-bottom like a league table.

Two build habits worth their weight in meetings: **delete what you are not using** (legends for single-series charts, gridlines competing with your data, 3-D effects — which distort every comparison they decorate); and **put the number where the eye lands** (data labels on the top three bars only; the rest is furniture).

## 11.3 The Three Lies

The three classic chart lies, each of which you will now recognise in the wild for the rest of your career — and never commit:

1. **The truncated axis.** A line chart of revenue from 9,100 to 9,400 looks like a rollercoaster if the y-axis starts at 9,000 — the *absolute* truth, the *relative* lie. Line charts of change should usually start from zero, or clearly flag that they do not; if a small move matters (control charts, Chapter 60's world), say so in the title.
2. **The unlabelled scale.** "Revenue (units? USD? thousands?)" — a chart whose axes are anonymous is a rumour with nice typography. Every axis: what, and in what units.
3. **The dual-axis trick.** Two lines, two axes, scaled until they cross wherever the author wishes — the most convincing lie in business. Dual axes are occasionally honest (very different units), but they demand a visible warning; mostly, two separate small charts tell the truth more cleanly.

## 11.4 Titles Are Findings

The professional rule, worth the whole chapter: **the title states what the chart shows, not what the chart is.**

- Furniture: "Monthly Sales 2025"
- Finding: "Sales grew 30% across 2025 — with a two-month dip after the oil price rise"

Write the finding title and the chart's purpose enters the room before you do; a deck of finding-titled charts can be *read* by someone who skips the meeting (Chapter 43's whole philosophy, learned here at small scale). If you cannot write a finding title, you may not yet have a finding — the title is a test, not a decoration.

## 11.5 The One-Minute Audit

Run this on every chart you make or meet — the same five questions as Chapter 2, in chart form:

1. **Compared to what?** — does the axis start where it should; is there a baseline series?
2. **Says who?** — where did the data come from (your title can carry it: "18 months of till data").
3. **What is missing?** — months absent, a category excluded, a legend doing quiet surgery.
4. **What was counted?** — revenue or transactions; members or sales; the chart's noun must be named.
5. **Could it be luck?** — the visible dip: real pattern or ordinary wobble? (The honest chart says "dip"; Part IV gets to say "significant".)

> **From Your Toolkit — the five forever:** these five shapes and three lies are chart craft entire — Python's matplotlib (Chapter 35) draws them with different clicks, Power BI (Chapters 41–42) animates them with filters, but the grammar is this chapter's, permanently. Learn the argument once; every tool afterwards merely holds the pen.

## Key Takeaways

- Five charts cover the working world: column, line, bar, scatter, stacked — the question chooses the shape.
- Build habit: finding titles, labelled axes with units, delete the furniture, numbers where the eye lands.
- The three lies: truncated axes, unlabelled scales, dual-axis crossings — recognise, avoid, call out.
- A finding title is a test: if you cannot title the finding, you may not have one.
- Audit every chart with the five questions — the same honesty habits, now drawn in ink.

## Practice Lab

1. Build the two core charts on your cleaned data — monthly revenue line and ranked category bar — with finding titles, labelled axes, and furniture deleted. Paste both into a `report` sheet (they are Projects 1 and 6's opening exhibits).
2. Build the truncated-axis lie on purpose: your revenue line with the axis starting at 90% of its minimum; screenshot or print both versions and write the one-sentence warning you would give a reader of the lying version.
3. The scatter: basket amount vs hour of day; describe the relationship you see in one sentence (and hold your conclusion loosely — Chapter 28 teaches why).
4. The audit, outward: find one published chart (news, social, a report) and run the five questions on it; write your audit in five lines.
5. The title test: take your three lab charts and write a furniture title and a finding title for each; give both versions to a friend for thirty seconds each and ask what the chart "says" — record which title won.

## Further Reading

- *How Charts Lie* — Alberto Cairo (the friendly, complete version of this chapter)
- Chapter 42 (chart craft's dashboard edition), Chapter 28 (the scatter plot grows up into correlation)
