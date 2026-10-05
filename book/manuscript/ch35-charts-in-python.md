# Chapter 35: Charts in Python — matplotlib, Honestly

*Part V — Python: From Zero to Dangerous*

> "The grammar of honest charts is finished (Chapter 11). What remains is learning a second pen."

### In this chapter you will learn

- matplotlib's mental model: figure, axes, plot — and the three lines that cover 80% of needs.
- The five charts of Chapter 11, redrawn: line, bar, scatter, histogram, stacked bar.
- The one-liner vs the craft version — when `.plot()` is enough and when it is not.
- Saving charts as files — the report's exhibits, generated.
- When to stay in Excel — the honest tool-choice rule.

## 35.1 The Model

matplotlib feels baroque until you hold its one mental model: a chart is a **figure** (the page) containing **axes** (one chart's frame — its x, its y), on which you **plot** marks, then decorate:

```python
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(10, 4))     # one page, one frame
ax.plot(monthly.index, monthly.values)      # the marks
ax.set_title("Monthly revenue")
ax.set_ylabel("Revenue (USD)")
plt.show()
```

The `fig, ax = plt.subplots()` incantation is the doorway you walk through a thousand times; everything else is marks plus decoration. (You will also meet — and use freely — pandas' shortcut `series.plot()` and `df.plot(kind="bar")`, which builds figure-and-axes for you and hands back the `ax` for decorating: `ax = monthly.plot(); ax.set_title(...)`. Use the shortcut for speed, the full form for control; they are the same machine.)

## 35.2 The Five, Redrawn

Chapter 11's five shapes, each in its working form on Tariro's data — find the same arguments hiding in different clothes:

```python
# 1. LINE -- "how does it move through time?"
ax = daily.resample("ME").sum().plot(figsize=(10, 4))
ax.set_title("Monthly revenue: steady growth, one dip"); ax.set_ylabel("USD")

# 2. BAR (ranked, horizontal) -- "which is biggest?"
top10 = sales.groupby("item")["amount"].sum().nlargest(10)
ax = top10.sort_values().plot(kind="barh", figsize=(8, 5))
ax.set_title("Top 10 items by revenue"); ax.set_xlabel("USD")

# 3. SCATTER -- "are these two related?"
ax = sales.plot(kind="scatter", x="amount", y="hour_of_day", alpha=0.2, figsize=(8, 5))
ax.set_title("Basket size vs time of day")

# 4. HISTOGRAM -- "what is the shape of this column?"
ax = sales["amount"].plot(kind="hist", bins=50, figsize=(8, 4))
ax.set_title("Basket sizes: right-skewed (whales live in the tail)")

# 5. STACKED BAR -- "what is it made of, over time?"
mix = sales.pivot_table(index="month", columns="payment_type",
                        values="amount", aggfunc="sum")
ax = mix.plot(kind="bar", stacked=True, figsize=(10, 4), width=0.8)
ax.set_title("Payment mix by month: EcoCash share rising")
```

Details that carry the craft: `alpha=0.2` makes scatter points translucent (overplotting defeated — 6,420 solid dots is a black rectangle); `bins=50` tunes histogram resolution (too few hides shape, too many makes noise); `nlargest(10)` is the top-list; `sort_values()` before a horizontal bar makes the ranking read top-down like a league table; and `pivot_table` is the pivot — `index`/`columns`/`values`/`aggfunc` are the four shelves by name.

## 35.3 The Craft Version

The one-liner gets a chart on screen; the craft version gets a chart *into a report* — and the difference is exactly the Chapter 11 rules, now as code:

```python
fig, ax = plt.subplots(figsize=(9, 5))

ax.plot(monthly.index.astype(str), monthly.values, color="#0F766E", linewidth=2)
ax.set_title("Monthly revenue grew 31% over 18 months\n(dip after the month-9 oil price rise)",
             fontsize=13, fontweight="bold")
ax.set_ylabel("Revenue (USD)")
ax.set_xlabel("Month")
ax.spines[["top", "right"]].set_visible(False)          # delete the furniture
ax.grid(axis="y", alpha=0.3)                            # subtle guides only
ax.tick_params(axis="x", rotation=45)

fig.tight_layout()
fig.savefig("exhibit-monthly-revenue.png", dpi=150)     # the file, for the report
```

Line by line, it is Chapter 11's checklist compiled: the finding title (with the number in it), labelled axes with units, furniture deleted (spines off), subtlety in the grid, and — the part one-liners cannot do — **`savefig`**: the exhibit as a file, at report resolution, ready for the PDF. A chart that regenerates from data every month *and* lands in the report automatically is the whole automation story in one function call. (Colours: name them (`"teal"`) or hex them (`"#0F766E"`); a consistent two-or-three-colour palette per report is the professional tell — Tariro's reports use teal and amber, matching this book's cover.)

## 35.4 The Notebook Dialogue

The chart's greatest notebook power is not beauty — it is *iteration*: see it, adjust, see it again, three cells a minute. The dialogue that produces good charts is only possible when the loop is seconds long, which is why analysts chart *inside* the analysis (spreadsheet too: the pivot and the chart are adjacent tabs) rather than exporting data to a separate charting tool. And a seaborn glimpse, honestly flagged as a taste of Chapter 58's world: `import seaborn as sns; sns.scatterplot(data=sales, x="amount", y="hour_of_day", hue="payment_type")` — statistical charts (with regression lines, distributions, categorical splits) in one line, built *on* matplotlib. When you need the statistics drawn, seaborn; when you need control, matplotlib; both ship with Anaconda.

## 35.5 When to Stay in Excel

The honest tool rule, stated once and applied forever: **the chart's audience decides the tool.** Exploring, iterating, one-off questions → the notebook (speed of iteration). A monthly PDF exhibit that must regenerate identically → matplotlib + `savefig` (automation). A chart the boss wants tweaked *in the meeting* ("make it blue, show March only") → the spreadsheet, because drag-and-drop beats re-running code when the requirement is changing live. And Part VI adds the fourth case: charts that must *filter themselves* when the reader clicks → Power BI. One grammar, four pens, chosen by the audience — the analyst who insists on a single tool for every chart is choosing their comfort over the reader's need, and Chapter 2's "says who?" applies to tools too.

> **From Your Toolkit — the report pipeline completes:** load (33) → analyse (34) → **chart (35, savefig)** → report. Chapter 37 wires these stages into the monthly pack, and Project 6's dashboard inherits the same exhibits. The five shapes and three lies never change; the pen does — and you now hold two of the four pens this book teaches.

## Key Takeaways

- Model: figure (page) → axes (frame) → marks → decoration; `fig, ax = plt.subplots()` is the doorway; pandas' `.plot()` is the shortcut.
- The five shapes transfer directly — line, ranked barh, scatter (alpha!), histogram (bins), stacked bar via pivot_table (the four shelves by name).
- Craft version = Chapter 11 compiled: finding title, units, spines off, and savefig — the exhibit as a regenerating file.
- The notebook's iteration speed is charting's real superpower; seaborn for statistical charts when needed.
- Audience picks the pen: notebook to explore, matplotlib to automate, spreadsheet for live tweaks, Power BI for interactive — one grammar, four pens.

## Practice Lab

1. The five, redrawn: run all five working-form charts on your data; then pick the two best and upgrade them to craft versions (finding titles, units, furniture deleted, savefig) — the PNGs are report exhibits; file them in your project folder.
2. The lie, reproduced in code: rebuild the truncated-axis lie from Chapter 11's lab (`ax.set_ylim(9000, 9500)` does it); save both versions; write the caption pair for the log/audit trail.
3. The alpha lesson: scatter of amount vs hour with `alpha=1` then `alpha=0.2` on the same data; paste both; write one sentence on what the translucent version reveals that the solid one hides.
4. The palette: re-colour your two craft exhibits with a consistent two-colour palette (hex codes in a constants cell at the top of the notebook — the named-constant habit, applied to design); note the palette in the header Markdown.
5. The regeneration test: change one month's data in the CSV (copy it first), re-run the notebook Restart & Run All, and confirm the exhibit PNG changed accordingly — then restore. You have just demonstrated the monthly-report promise: charts that rebuild themselves.

## Further Reading

- Chapter 36 (statistics in Python — the tests join the charts), Chapter 37 (the pack, assembled)
- matplotlib's official gallery — copy the nearest example, adjust to your data (the professional's method, openly admitted)
