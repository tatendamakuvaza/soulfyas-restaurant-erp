# Chapter 8: Cleaning a Messy Sheet

*Part II — Excel: Your First Superpower*

> "Analysis is 10% cleverness and 90% gardening."

### In this chapter you will learn

- Why cleaning comes first, always — and why it is the analyst's real job, not a chore.
- Sorting and filtering: seeing the mess before fixing it.
- Duplicates: finding them, understanding them, deciding about them.
- Text tools: TRIM, PROPER, find & replace, text-to-columns — the three-Ecocash cure.
- Missing values: what to do, what never to do, and how to log everything.

## 8.1 The Gardener's Secret

Here is the sentence experienced analysts tell beginners in private: **you will spend more time cleaning data than analysing it, and the cleaning is where the value lives.** A flawless analysis on misunderstood data is a beautifully built house on a rumour; a modest analysis on honestly-cleaned data changes decisions. Tariro's data arrives with known, planted messes — this chapter finds and fixes them the way you will fix real messes for your whole career: *look, understand, fix, log.*

## 8.2 Look Before You Fix: Sort and Filter

Two clicks change your relationship with any table:

- **Sort** (Data → Sort): order the whole table by one column. Sort by `item` and you see every spelling variant of the same product huddled together — Tariro's tills know "Cooking Oil 2L", "cooking oil 2l", and "Cooking Oil 2L " (trailing space), and now so do you. Sort by `amount` and the smallest values rise to the top: the zero-amount rows, the missing prices.
- **Filter** (Data → AutoFilter — the funnel icon): puts a dropdown on every column header. Open `payment_type`'s dropdown and the *entire problem* appears as a list: `Ecocash`, `eco_cash`, `ECOCASH`, `Cash`, `card`, `Card `. Six categories that are really two.

Sorting and filtering are not yet cleaning — they are **seeing**. The professional sequence is always see → understand → fix: never fix what you have not seen whole, because the fix you cannot see is the fix you cannot trust.

## 8.3 Duplicates

Some rows in `sales.csv` appear twice — planted, and realistic (till restarted, export run twice). The tool: Data → Detect Duplicates (LibreOffice walks you through which columns to compare; Excel's Remove Duplicates is on the Data ribbon). But the professional questions come *before* the click:

- **Exactly duplicated?** — every column identical? Then it is almost certainly an export ghost: safe to remove *after counting them*.
- **Same sale, slightly different?** — same timestamp and item but different amount? Now it might be a genuine second item, or a corrected re-entry. **Deleting is now a decision, not a click** — and the decision gets logged.

Never remove duplicates silently. The cleaning log entry (your `notes` sheet, from Chapter 6) reads like this:

```text
2026-03-12  Removed 412 exact duplicate rows from sales.csv
            (till export run twice on 2025-06-14 and 2025-09-02).
            Kept first occurrence. File: clean/sales-v2.xlsx
```

Four lines, and any future question — "why do last year's numbers differ from the report?" — has an answer with a date on it.

## 8.4 Text Tools: The Three Ecocashes

Text messes are so universal that the toolbox is small and permanent:

- **TRIM** — `=TRIM(D2)` removes sneaky leading/trailing spaces: "Card " becomes "Card". Invisible, rampant, and the cause of half of all "why won't these group together?" mysteries.
- **PROPER / UPPER / LOWER** — standardise capitalisation: `=PROPER("ecocash")` → "Ecocash". (Careful with names and codes: PROPER turns "mcdonald" into "Mcdonald" — standardise *deliberately*, not blindly.)
- **Find & Replace** (Ctrl+H) — the bulk cure: replace `eco_cash` → `Ecocash`, then `ECOCASH` → `Ecocash`. Two replacements, three categories become one. Do this on a copy, with the log entry.
- **Text to Columns** (Data → Text to Columns) — splits one column into several on a separator: the `date_time` column holding "2025-03-01 13:45" splits into a date and a time; "Chikafu,Maize Meal" splits into product and category. One fact per column (Chapter 6's rule) is often *achieved* here, not found.

The general law: **standardise to exactly one spelling per thing, and write the chosen spelling down.** The list of chosen spellings is Tariro's first *data dictionary* — five categories, one line each, on your `notes` sheet — and it is the beginner version of what professional teams call a data contract.

## 8.5 Missing Values: What and What Never

The zero and blank amounts (planted in Chapter 5, found by your COUNT gap in Chapter 7) are the classic first missing-data problem. The honest options:

1. **Leave blank, count them** — often correct: blanks mean "unknown", and unknown is information.
2. **Fix from evidence** — if `units × unit_price` can be reconstructed from the row itself (`=C2*D2` where both survive), the fix is arithmetic, and it gets logged.
3. **Flag, don't invent** — a helper column `=IF(H2="", "check", "ok")` marks the rows for Tariro's human knowledge (she remembers the till's bad afternoon).

The forbidden option: **silently replacing blanks with zeros** — it makes "we do not know" look like "nothing was sold", and the resulting average quietly lies. This is the spreadsheet version of Chapter 2's honesty rules, and (much later, Chapter 60) you will meet the professional typology of missingness — but the beginner's version fits in one line: **never turn a question mark into a zero.**

## 8.6 The Clean Copy and the Log

The workflow that ties the chapter together, and that you will repeat professionally forever:

1. **Copy** the raw original into `clean/`, versioned: `sales-v2.xlsx` (v1 was the straight import).
2. **See** (sort/filter) → **understand** (why does this mess exist? tills restart, exports double, humans type) → **fix** (dedupe, standardise, reconstruct) → **log** (every change, dated, in `notes`).
3. **Sanity-check the totals**: revenue after cleaning differs from before by exactly the removed duplicates' value — verify that arithmetic. A clean file whose totals cannot be reconciled to its raw parent is not clean, it is *mysterious*, and mysterious is a failure state.

> **From Your Toolkit — future tools:** every fix in this chapter has a twin in your future stack. TRIM and the dedupe click return in SQL as `TRIM()` and `DISTINCT` (Chapter 16); pandas names them `.str.strip()` and `.drop_duplicates()` (Chapter 33); and the professional end-state — fixes written as code that reruns automatically — is Chapter 37's whole point. The buttons change; the gardening is forever.

## Key Takeaways

- Cleaning is the job, not the chore — value lives in trustworthy data.
- See → understand → fix → log: sort and filter to see; never fix blind; never fix silently.
- Duplicates are a decision with a count; text messes are cured by standardising to one documented spelling.
- Missing means unknown: reconstruct from evidence, flag for humans, never fake a zero.
- Reconcile clean totals to raw — clean files must be explainable, not just tidy.

## Practice Lab

1. Run the full workflow on `sales.csv`: find and remove the exact duplicates (log the count and dates), cure the three Ecocashes, TRIM the payment column, and reconcile the revenue total to the raw file — show the arithmetic.
2. Sort by `item` and list every spelling variant of the three messiest products; write Tariro's first data dictionary entry for one of them (chosen spelling, common variants, decision).
3. The missing amounts: count them, reconstruct what can be reconstructed with `units × unit_price`, and flag the rest; write the log entry that explains what a future reader sees.
4. Split a combined column (or manufacture one by merging date and time, then splitting) with Text to Columns; note one case where the split needs a second tool (e.g., trailing spaces after the comma).
5. The blank-to-zero trap, demonstrated: compute the average sale with blanks left blank, then again with blanks replaced by zero; write the two averages and one sentence to Tariro about which one is honest and why.

## Further Reading

- Chapter 9 (joining tables — now that the sheets are clean), Chapter 60 (the professional missingness typology, when you are ready)
- "Data cleaning" chapters of any analytics text — you will recognise every page from this one afternoon.
