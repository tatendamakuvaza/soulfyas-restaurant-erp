# Chapter 7: Formulas from Zero

*Part II — Excel: Your First Superpower*

> "A formula is a sentence that starts with '=' and answers a question."

### In this chapter you will learn

- Your first formulas: SUM, AVERAGE, COUNT, MIN, MAX — each in plain English.
- The formula that thinks: IF.
- Cell references, ranges, and the dollar signs that lock them in place.
- Percentages and growth, computed honestly.
- Formula hygiene: how to write formulas a stranger (or future you) can read.

## 7.1 The Equals Sign

Every formula begins with `=`. That single character tells the sheet: *"what follows is a question — compute the answer, show me the result."* Type `=2+2` and press Enter; the cell shows `4`. Click the cell again and the formula bar shows the question. This split — the cell shows the answer, the bar shows the question — is the whole personality of spreadsheets, and the reason they are the friendliest tool in this book: **you can see the machinery**.

## 7.2 The Starter Set

Each formula below, in one plain-English sentence, on Tariro's data (your working copy from Chapter 6):

| Formula | Plain English | On Tariro's sales |
|---|---|---|
| `=SUM(H2:H50000)` | Add up everything in this stretch of column H | Total revenue for the range |
| `=AVERAGE(H2:H50000)` | The arithmetic middle: add up, divide by count | Average sale amount |
| `=COUNT(H2:H50000)` | How many cells contain numbers | How many priced sales |
| `=COUNTA(B2:B50000)` | How many cells contain anything | How many rows have an item name |
| `=MIN(H2:H50000)` / `=MAX(...)` | The smallest / largest | The smallest and biggest sale |

The stretch `H2:H50000` is a **range**: from cell H2 to cell H50000, everything between included. Ranges are how formulas talk about columns. Note `COUNT` versus `COUNTA`: the first counts numbers only, the second counts anything non-empty — and their difference is already a finding (rows where the amount is missing, the flaw you know was planted in Chapter 5; Chapter 8 fixes it properly).

## 7.3 The Formula That Thinks: IF

`=IF(question, answer_if_yes, answer_if_no)` — one question, two outcomes:

```text
=IF(H2 >= 20, "big basket", "small basket")
```

Read it aloud: *if the sale amount is 20 or more, write "big basket", otherwise "small basket".* Fill it down a column (select the cell, then the little square at its corner, and drag — or double-click the square to auto-fill to the bottom) and you have just *classified* eighteen months of sales into two groups. Classification is a real, professional act — the baby version of the "segmentation" you will meet in Chapter 34 — and it is three words long.

IF grows with you gently: `=IF(G2="Ecocash", "wallet", "cash")`, and nested versions later (`=IF(H2>=20, "big", IF(H2>=10, "medium", "small"))` — read as "if... otherwise if... otherwise"). Whenever a nested IF starts hurting your head, that is the instinct that SQL's `CASE` (Chapter 20) and Python's logic (Chapter 32) will formalize — same thinking, better syntax.

## 7.4 References and the Dollar Signs

Formulas rarely contain numbers; they contain **references** — addresses of cells, so the answer follows the data. `=H2*2` doubles whatever is in H2, and when copied down, the reference follows: row 3's copy says `=H3*2`, all the way down. This "relative reference" is why one formula can serve fifty thousand rows.

The dollar sign **locks** a reference. `$A$1` means "always exactly A1, even when copied" — an **absolute reference**. The classic use: a threshold stored in one cell (say, `P1` holds `20`), and every row's formula says `=IF(H2 >= $P$1, "big", "small")`. Tomorrow Tariro changes the threshold in one place — P1 — and every formula updates. *One fact lives in one place* is a professional instinct that will save you from the spreadsheet classic: five copies of the same number, four of them updated.

## 7.5 Percentages and Growth

The two percentage sentences you will use forever:

- **"What share?"** — part divided by whole: `=H2/SUM($H$2:$H$50000)` is this sale's share of revenue; format the cell as a percentage (the % button) so it reads naturally.
- **"How much did it grow?"** — new minus old, divided by old: if March total is in P5 and February's in P4, then `=(P5-P4)/P4` is the month's growth rate. Say the sentence aloud when you write it: *change, relative to where we started.* Growth on a tiny base is loud for unimpressive reasons ("sales doubled!" — from two customers to four), so the habit of asking *relative to what size?* starts here.

One warning from Chapter 2's honesty rules, now with tools: an AVERAGE over a wildly mixed table (Tariro's 2-cent airtime sachets next to $60 bulk maize meal) describes neither. The cure is a filtered average — coming in Chapter 12 as `AVERAGEIF`, and it is why this chapter ends by asking you to notice what your averages average.

## 7.6 Formula Hygiene

- **Write so the bar explains the cell**: `=SUM(sales_amount)` (a named range) or `=H2*$P$1` with a label beside P1 — future you is a stranger under deadline.
- **One fact, one place**: constants (thresholds, tax rates) live in labelled cells, referenced absolutely — never typed inside formulas.
- **Check the edges**: formulas filled to the bottom sometimes catch one row too many (a grand total row) — the classic doubled-total bug. Glance at the last row the formula reached.
- **Errors are messages**: `#DIV/0!` means you divided by an empty column (often: the range is one row off); `#NAME?` means a typo in a formula name; `#N/A` (coming in Chapter 9) means a lookup found nothing. Every error names its disease — treat them as the tool talking, not failing.

> **From Your Toolkit — the notebook:** keep your ten most-used formulas in the back of your notebook, each with its one-sentence translation. In six months, Chapter 34 will hand you the same ten as Python functions (`sum`, `mean`, `count`, `np.where` — IF's twin), and the notebook page is the moment you recognise an old friend.

## Key Takeaways

- A formula is a question after `=`; the cell shows the answer, the bar shows the question.
- The starter set answers real questions immediately: totals, averages, counts, extremes — on real data, today.
- IF classifies; nested IF is the seed of CASE and Python logic.
- References make formulas portable; `$` locks them; constants live in one labelled place.
- Percentages are two sentences (share, growth) — always asked "relative to what?"

## Practice Lab

1. On your working copy: total revenue, average sale, count of sales, biggest and smallest sale — five formulas, five numbers on a new `answers` sheet, each labelled in plain English.
2. The IF drill: classify every sale into small/medium/big baskets using a threshold held in its own labelled cell; then change the threshold once and watch the column update.
3. The missing-count finding: write `=COUNTA(B2:B50000)-COUNT(H2:H50000)` and explain in one sentence what the answer tells Tariro about her data's health.
4. Growth: monthly revenue for the last six months (peek ahead: a small pivot or manual SUMs over date ranges), then the month-over-month growth rates; note which month looks odd and guess why (the planted price rise, month 9, may be near).
5. Break three formulas on purpose (`#DIV/0!`, `#NAME?`, a filled-range overshoot) and write down each error's disease and cure in your notebook's formula page.

## Further Reading

- Chapter 8 (cleaning — fixing the rows your formulas just exposed), Chapter 12 (statistics in Excel)
- Excel/LibreOffice help: "Fill a formula down" — the drag-and-double-click habit that makes one formula serve a whole column
