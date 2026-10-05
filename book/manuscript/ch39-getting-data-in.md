# Chapter 39: Getting Data In — Shaping and the Model

*Part VI — Dashboards and Storytelling with Power BI*

> "The dashboard is only as honest as the model beneath it — and the model is only as honest as the shaping."

### In this chapter you will learn

- Power Query: the recorded, replayable cleaning pipeline — Chapter 8 with a memory.
- Loading Tariro's four tables, shaped properly.
- The data model: the star schema, relationships, and cardinality.
- The fan-out guard, structurally: how the model view makes it visible.
- Date tables: the one special table every serious model has.

## 39.1 Power Query: Cleaning That Remembers

Click **Get data → Text/CSV**, and before Load, choose **Transform Data** — the door into **Power Query Editor**, and the most under-taught superpower in the whole Microsoft stack. Power Query is Chapter 8's cleaning liturgy, *recorded*: every step you take (remove blank rows, change a type, trim text, split a column) is written into an **Applied Steps** list on the right, and the whole chain replays automatically on every refresh. The part-time cashier's detached-sort disaster (Chapter 14's story) is structurally impossible here: raw data arrives, steps transform a *copy*, the original is never touched, and next month's CSV gets the same treatment by replay. It is exactly Chapter 37's pipeline — `data/raw` sacred, cleaning reproducible — as a visual editor.

The working session on Tariro's `sales.csv`, in Power Query's own buttons (each step lands in Applied Steps, and you should *name* steps by double-clicking them — the why-comments of Chapter 20, wearing a list):

1. **Home → Remove Rows → Remove Blank Rows** — the ghost rows.
2. Right-click `payment_type` → **Transform → Trim** (whitespace), then **Format → Capitalize Each Word** — the three-EcoCash-spellings fix, replayed monthly forever.
3. Right-click `amount` → **Change Type → Decimal Number** (and `date` → Date). Power Query *guesses* types on load — the Chapter 33 lesson: check every guess.
4. **Add Column → Column From Examples →** type "Mon" next to a Monday date: the weekday column, inferred.
5. Right-click a column → **Rename**; and **Choose Columns** to drop what the model does not need.
6. **Close & Apply** — the steps run, the table lands in the model.

Do the same for `customers`, `stock`, `suppliers` — four queries, four named step-lists, and a shaping layer you could hand to a successor with the words "read the steps top to bottom."

## 39.2 The Model

With data loaded, open **Model view** (the icon on the left edge): your tables float in a diagram — and here Power BI draws Chapter 17's boxes-and-lines picture *for you*. The work is arranging relationships by dragging keys onto keys: `customers.customer_id` → `sales.customer_id`; `stock.item` and `suppliers.item` → an items dimension (or a small `items` table if the design needs one). Three properties per relationship, and they are the Chapter 17 vocabulary exactly:

- **Cardinality** — One-to-many (1:*): the safe default (one customer, many sales). Many-to-many (*:*): Power BI permits it, flags it, and *you should treat the flag as Chapter 17's fan-out warning* — a many-to-many in your model means the design is asking for a bridge table.
- **Cross-filter direction** — Single (filters flow one way, from the "one" side) or Both. Single is the safe default; Both is for special patterns and quiet ambiguity.
- **Activate/Inactive** — multiple date relationships (order date vs ship date) exist; advanced DAX picks between them (beyond this book's brief).

The **star schema** is the shape you are aiming at: one **fact table** in the middle (sales — the events, many rows, the numbers) surrounded by **dimension tables** (customers, items, a date table — the context, fewer rows, the descriptors). Star schemas are why dashboards are fast and sane: measures aggregate the fact; dimensions filter and label it; every question is a path from a dimension through the fact. (Tariro's four tables are a small star already; most of your working life will be recognising, or building, this shape in bigger clothes.)

## 39.3 The Fan-Out Guard, Structurally

The old enemy returns, with a new weapon. In a spreadsheet, fan-out hides; in SQL, it is a doubled total; **in a model, it is visible in the diagram** — a relationship arrow whose wrong cardinality or whose many-to-many badge is the smoking gun. The defensive ritual, once per model, forever:

1. **Model view**: check every line's cardinality badge; any `*:*` is investigated (usually: the dimension has duplicate keys — fix in Power Query with a Group By/dedup step, or the relationship's key is not actually unique).
2. **The reconciliation card**: a card visual with `SUM(sales[amount])`, compared to the known bridge total (54,013.50). It must match *exactly* before any other visual is built — the same cent-for-cent bridge from every Part of this book, now standing guard on the dashboard itself.
3. **The no-relationship test**: a table visual of `customers` names next to `sales` amounts that computes *wrong* (repeating, inflated) is almost always a missing or misdirected relationship — the amputation/fan-out pair, visible at a glance.

## 39.4 The Date Table

One special table deserves its own section because serious models always have one: a **date table** — a calendar, one row per date, spanning (and exceeding) your data's range, with the columns every time question needs: date, year, month name, month number, weekday, weekend flag, quarter. Build it in Power Query (Home → Enter Data is too small; better: a small query generating dates, or `calendar.csv` from Python — Appendix C's generator emits one), relate it to `sales.date`, then **Mark as date table** (Table tools → Mark as date table).

Why the ceremony? Because "month" sliced from a raw date column is *text* ("2025-06") — it sorts, but it does not *know* things: it cannot tell you which months are which quarter, whether a day was a weekend, or what "the previous month" means across years. A marked date table gives DAX's time intelligence (Chapter 40's month-over-month and running totals) a true calendar to compute against — the difference between dates-as-strings and *time as a dimension*. The professional tell in any .pbix you inherit: look for the date table; its absence predicts every date-related bug you are about to find.

## 39.5 Where You Are

The model is the deliverable of this chapter, even though nothing visual exists yet: four shaped, replayable queries; a star with correct cardinality; the bridge reconciled; the calendar marked. Everything Chapters 40–43 build — measures, visuals, pages, the story — stands on this, and the industry's hardest BI bugs live exactly here, which is why this chapter spent its length on keys, badges, and the bridge. Tariro's brief has its foundation; the next chapter teaches it to calculate.

> **From Your Toolkit — the model is forever:** the star schema is the same shape behind every BI tool (Tableau's relationships, Looker's views, a warehouse's dims and facts — Chapter 57's world is this chapter industrialised); Power Query's step-list is Chapter 37's pipeline and Chapter 20's header block in visual form; and the date table is the calendar that pandas' `.dt` accessor was quietly being for you all along. Learn it once here, recognise it everywhere.

## Key Takeaways

- Power Query records and replays every cleaning step: raw data sacred, steps named, next month's CSV transformed identically — the pipeline as an editor.
- The model is Chapter 17 drawn: relationships with cardinality and direction; star schema (facts in the middle, dimensions around); treat many-to-many badges as fan-out warnings.
- The reconciliation card (SUM vs the known bridge) guards every model before the first visual is built.
- Build and mark a date table: time as a dimension — the precondition for time intelligence.
- The hardest BI bugs live in the model; an afternoon here prevents a quarter of confusion later.

## Practice Lab

1. Shape all four tables in Power Query with named steps (trim, case, types, weekday-from-example, renames); write the step-list for `sales` into your log as prose ("what the pipeline does, in order") — the successor's document.
2. Build the star: relate customers→sales, items→sales, date→sales; screenshot the model diagram with cardinality badges visible; annotate the screenshot with the one-to-many arrows in your own words.
3. The bridge card: total revenue visual vs 54,013.50; then break it on purpose (delete the customers relationship, note what changes; mis-set a cardinality to *:*, note the badge) — the fan-out museum, BI wing.
4. The date table: build or import the calendar, mark it, and confirm the weekday column matches `sales`' own weekday derivation for ten sample dates.
5. The refresh rehearsal: add next month's rows to a copy of `sales.csv`, point the query at it (or replace the file), hit **Refresh**, and watch the steps replay and the bridge card update — then write the two-paragraph runbook ("how this dashboard's data refreshes") for the README you will publish in Chapter 49.

## Further Reading

- Chapter 40 (DAX measures — the model learns to calculate)
- Microsoft Learn: "Model data in Power BI" — the official depth behind this chapter
