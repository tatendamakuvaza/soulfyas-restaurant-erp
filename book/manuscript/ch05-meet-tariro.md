# Chapter 5: Meet Tariro

*Part I — Beginning: You, the Data Analyst*

> "Every dataset is somebody's livelihood wearing columns. This one is Tariro's."

### In this chapter you will learn

- The running case that carries the whole book: Tariro's Grocery, Highfield, Harare.
- Her data — where it comes from, what is in each file, and what is wrong with it (on purpose).
- Her questions, which become every project in this book.
- Your role: hired analyst, with a notebook, a toolkit, and a boss who counts every dollar.
- The map: how each part of the book answers one of her questions.

## 5.1 The Shop

**Tariro** is thirty-four, runs a grocery store on a busy corner in Highfield, Harare, and has done so for six years — long enough to know her regulars by name, her suppliers' moods by voice, and her stock by walking past the shelves. She began with a paper notebook and a tin; today she has a secondhand laptop, a spreadsheet her nephew built in an afternoon two years ago, and a queue of decisions she makes by feel because "the numbers are somewhere but who has time".

Her dream is a second branch. Her bank manager, politely, wants evidence: *"Show me the numbers, Tariro. Which days earn? Which products pay? Who are your best customers? Then we talk about a second shop."*

You — having just installed a complete free analytics toolkit — are her new analyst. She can pay in thank-yous, story rights, and (Chapter 55) eventually a modest invoice, and she offers what every beginner analyst needs most: **a real business, real mess, real questions, and a boss who reads what you write.**

## 5.2 The Data

Tariro's nephew exported everything the till software remembers, and the book's data files are that export. Four tables, described the way you should always describe data (what one row *is*, and what the columns *mean*):

| File | One row is... | Key columns |
|---|---|---|
| `sales.csv` | one item sold, one time | date, time, item, category, units, unit_price, amount, payment_type |
| `stock.csv` | one item's stock count, one week | week, item, units_on_shelf, units_in_store_room |
| `customers.csv` | one loyalty member | joined_date, name_initial, suburb, age_band, points |
| `expenses.csv` | one shop expense, one month | month, type (rent, wages, power...), amount |

The data covers eighteen months of trading. And it is *deliberately imperfect*, because clean practice data teaches nothing but confidence:

- Some sales rows are duplicated (the till was restarted on two bad afternoons).
- Some amounts are missing or zero (a price was never entered).
- Payment types include three spellings of the same word (`Ecocash`, `eco_cash`, `ECOCASH`).
- The stock table is missing three weeks (the nephew's exam season).
- One month's expenses were recorded in a different currency order of magnitude — the rent row lost a zero.

Every one of these is a lesson you will meet in real employment within a month of starting: this book teaches you to *find* them (Chapter 8), *fix* them honestly (Chapters 8, 33), and *document* them (Chapter 45) so Tariro never doubts which number is which.

And underneath the mess, the data carries **planted patterns** — real, findable business truths, written down before the data was generated, so every analysis you do can be scored against the truth (the way no real job ever can):

- Sales spike on **payday weekends** (month-end and mid-month).
- **Fridays and Saturdays** out-earn other days by about a third.
- The **price rise on cooking oil** in month 9 caused a dip that partly recovered.
- **Sundays are marginal** — Tariro's biggest personal question.
- A core of **loyalty members** drives a disproportionate share of revenue, and some are drifting away.

## 5.3 Her Questions

Tariro's list, in her words — the questions every part of this book will answer with tools:

1. *"Am I actually making money, or just busy?"* — the monthly report (Part II: Excel).
2. *"Which products should I stock more of, and which are dead weight?"* — stock and sales analysis (Parts II–III).
3. *"Are Sundays worth opening?"* — comparing days honestly, including whether differences are luck (Part IV).
4. *"Did the cooking-oil price rise hurt me, or did it save me?"* — before-and-after, done properly (Part IV).
5. *"Who are my best customers — and am I losing them?"* — the customer analysis (Part VII, Project 4).
6. *"Can the report build itself? I asked you twice already."* — automation (Part V: Python).
7. *"Can I show the bank something they'll actually read?"* — the dashboard (Part VI: Power BI).

Notice: not one of her questions names a tool. That is the correct order of the world — **questions first, tools second** — and it is why Chapter 2's notebook habit exists. Write her list into your `04-Notes/` folder now, in her words; you will cross items off with satisfaction for four hundred pages.

## 5.4 Your Role and Your Rules

You are hired. The terms of your employment, agreed over a cold drink:

- **You work on copies** — her originals are sacred (Chapter 4's `raw/` rule; her nephew already lost one term's data to a mis-click).
- **You tell her what you did** — every cleaned file, every assumption, written in one page a human can read (this becomes Chapter 45's project documentation, practised from Part II onward).
- **You say when you do not know** — the beginning of the trust she will eventually send you to her bank manager with.
- **You charge nothing until Chapter 55** — when, properly skilled, you will price your first real invoice.

And one rule from her side that is a gift: **she asks "why?" about everything.** Not to doubt you — because she genuinely wants to learn. It will make you a better explainer than any course exercise ever could, which is Part VI's quiet goal.

## 5.5 The Map of the Journey

Where each part of the book touches her shop:

| Part | Tariro's story | Your deliverable to her |
|---|---|---|
| I (now) | The meeting, the deal, the data | Your notebook, her question list |
| II — Excel | The messy spreadsheet, the first report | Project 1: the monthly report (Ch. 13) |
| III — SQL | Her data grows into a real database | Project 2: ten questions, answered (Ch. 21) |
| IV — Statistics | "Is that real, or just the way weeks go?" | The Sunday verdict; the price-rise verdict |
| V — Python | "You asked me twice" — the report automates | Project 3: the report that builds itself (Ch. 37) |
| VI — Power BI | The bank meeting | Her dashboard, and the story to go with it |
| VII — Projects | The deep questions | Projects 4–6, your portfolio |
| VIII — The Job | Your story, told with hers | CV, interviews, first 90 days |
| IX — Beyond | "What's next for you — and for my second shop?" | The gentle maps; the roadmap |

> **From Your Toolkit — your notebook, again:** before the next chapter, write the entry that every real engagement starts with: the client, the questions (her words), the data (the four files and what a row is in each), and the date. Sixty chapters from now, this page will be the first exhibit in your professional story — keep it.

## Key Takeaways

- Tariro's Grocery is the book's client: real questions, messy data, planted answers — a safe rehearsal for employment.
- Four tables — sales, stock, customers, expenses — with documented flaws and documented truths.
- Her seven questions map to the whole book: reports, stock, Sundays, pricing, customers, automation, the bank dashboard.
- Your terms: copies only, document everything, admit unknowns — the professional habits, started free and cheap.
- Questions first, tools second: her list, in her words, is now in your notebook.

## Practice Lab

1. Open each of the four data files and just *look* — five minutes each, no changes. For each, write one thing you noticed and one question it raises. (Find the duplicated afternoons. Find the missing weeks.)
2. Write Tariro's seven questions into your notebook in your own handwriting; add one question of your own that her data could answer.
3. The data card (your first professional document, 10 lines): for `sales.csv`, write the file's row-definition, its columns with meanings, the date range it covers, and its three flaws. You will update this card in every part of the book.
4. The first estimate, on purpose wrong: eyeball `sales.csv` and guess — which day of the week is biggest? Write it down and date it. Part IV will settle it statistically, and the comparison of your eyeball to the truth is itself a statistics lesson.
5. The contract: write the four terms of your employment from Section 5.4 as a one-page memo to Tariro, in plain language. Keep it — Chapter 55 prices the real version.

## Further Reading

- Chapter 6 — thinking in grids; Tariro's spreadsheet gets its first cleanup
- Every part opener from here returns to the shop: keep her questions within reach.
