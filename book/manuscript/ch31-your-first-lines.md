# Chapter 31: Your First Lines — Variables, Numbers, Text

*Part V — Python: From Zero to Dangerous*

> "Programming is talking to a very fast, very literal friend. It does exactly what you said — which is why you must learn to say what you meant."

### In this chapter you will learn

- Variables: labelled boxes, and the naming habits of professionals.
- Numbers and text (strings): the two workhorse types, with their operations.
- Booleans and comparisons: how Python decides things.
- f-strings: sentences with numbers inside — the analyst's reporting line.
- Errors, read properly — the red wall is a map, not a punishment.

## 31.1 Variables

A **variable** is a labelled box holding one thing:

```python
shop_name = "Tariro's Grocery"
average_basket = 8.42
n_sales = 6420
```

The `=` is not mathematics' equality; it is an instruction: *put the right side in the box named by the left*. Read it right-to-left and it never confuses. Use a variable by name (`average_basket * 2`), change it (`n_sales = n_sales + 150` — take the box, add, put it back), and — the professional habits — **name it as what it means** (`average_basket`, not `x`, not `ab`); **snake_case** (lowercase, underscores — Python's universal convention); and let the name carry the unit when money is involved (`revenue_usd`, `price_per_bottle`) — the unlabelled-number rule of Chapter 27, applied to your own code.

## 31.2 Numbers

Two number types, and the difference is one you have met before:

```python
n_sales = 6420            # int -- a count; no decimal point
average_basket = 8.42     # float -- a measurement; decimal point present
```

Python's arithmetic is the spreadsheet's: `+ - * /`, parentheses for grouping, `**` for powers (`2**10`), and `//` with `%` for whole-division and remainder (`17 // 5` → 3; `17 % 5` → 2 — the "how many full boxes, how many left over" pair, quietly useful for weekday math: `day_number % 7`). Floats carry the Chapter 7 warning: `0.1 + 0.2` is `0.30000000000000004` — binary's small print, identical in every tool that uses binary floats, and the reason money is rounded for *display* and reconciled for *truth*. Integers never drift; when a number is a count, keep it an int.

## 31.3 Text

A **string** is text in quotes (single or double — pick one and stay consistent; this book uses double):

```python
item = "Cooking Oil 2L"
len(item)                      # 14 -- characters, spaces included
item.upper()                   # "COOKING OIL 2L"
item.lower()                   # "cooking oil 2l" -- the TRIM-family's cousins
item.strip()                   # trims edge whitespace (the ghost-blank slayer)
item[:11]                      # "Cooking Oil" -- slice: first 11 characters
"Oil" in item                  # True -- membership test
```

Strings are Chapter 8's cleaning tools in code form: `.strip()` kills ghost blanks, `.upper()`/`.lower()` unify case (three EcoCash spellings meet their final solution), and slicing takes substrings by position. Strings join with `+` (`"Daily " + "report"`), but the join you will actually use is next — because analysts do not concatenate; analysts *report*.

## 31.4 f-strings: The Reporting Line

The **f-string** is the single most-used line in the working analyst's Python — text with live values dropped in, formatted on the spot:

```python
month = "2025-06"
revenue = 3401.55
n = 389

print(f"{month}: revenue ${revenue:,.2f} from {n} sales")
# 2025-06: revenue $3,401.55 from 389 sales
```

The recipe: an `f` before the opening quote; `{name}` drops a variable in; and after a colon, *format specifiers* — `,` for thousands separators, `.2f` for two decimals, `.0f` for none, `.1%` for percentages (`0.31` prints as `31.0%`). Every sentence of every report you generate in Part VII is an f-string at heart: the chart carries the shape, the f-string carries the number, in the format the reader needs. Practise until `f"{x:,.2f}"` is muscle.

## 31.5 Booleans and Decisions

A **boolean** is a fact: `True` or `False` (capitalised — Python is fussy). Comparisons produce them (`revenue > 3000`, `item == "Cooking Oil 2L"` — double `==` compares, single `=` assigns; mixing them up is everyone's first bug), and they combine with `and`/`or`/`not` — the WHERE clause's combiners, spelled out in English:

```python
is_weekend = day == "Sat" or day == "Sun"
big_sale = amount >= 50 and payment_type == "EcoCash"
is_member = customer_id != "none"
```

Booleans are the seeds of decisions (`if` statements, Chapter 32) and of *filters* — and here is the preview that makes Python click for an analyst: in pandas, `sales[sales["amount"] >= 50]` is a filter, and the inner part is exactly the boolean line above. The whole query language of this book — WHERE, filters, if — reduces to booleans. Learn them here, spend them forever.

## 31.6 Errors as Friends

Sooner than you plan, a red wall appears:

```text
TypeError: can only concatenate str (not "float") to str
```

The instinctive response is dread. The professional response is a checklist, because Python's errors are *specifically, lovingly instructive*:

1. **Read the last line first** — the error *type* and its message. This one says: you used `+` between text and a number. (Fix: an f-string — the error was telling you what to do.)
2. **Read the arrow** — the traceback points at the exact line. Unlike a spreadsheet's silent wrong answer, Python's wrong answer *announces itself with a location* — a luxury, not an insult.
3. **Learn the four regulars**: `NameError` (typo — the box was never made or is misspelled), `TypeError` (mixing types — text plus number), `SyntaxError` (missing quote/colon/parenthesis — the sentence is not English), `KeyError`/`IndexError` (asking for a column or position that is not there — a data question, usually).

Copy the error's last line, search it verbatim, and the internet answers — errors are so standardised that the fix for yours is documented a million times. The reframe that makes you a programmer: *you are not a person who avoids errors; you are a person who reads them fast.*

> **From Your Toolkit — the atoms:** every tool ahead is these atoms assembled: a pandas DataFrame is boxes of columns (variables), filters are booleans, report lines are f-strings, and cleaning is `.strip()`/`.upper()` at scale. SQL people: variable = alias, boolean = WHERE, f-string = CONCAT with manners. Nothing new arrives after this chapter that is not *combinations* — which is why the Practice Lab matters more than the reading.

## Key Takeaways

- Variables are labelled boxes; `=` assigns, names mean things, snake_case, units in money names.
- int vs float: counts vs measurements; floats round for display only; `//` and `%` for boxes and remainders.
- Strings carry the cleaning kit (`.strip()`, `.upper()`, slicing, `in`) — Chapter 8 as code.
- f-strings are the reporting line: `f"{revenue:,.2f}"` is muscle to build; every generated sentence uses one.
- Booleans (==, and/or/not) are WHERE's atoms and pandas filters' seeds; errors are maps — last line first, arrow second, four regulars memorised.

## Practice Lab

1. The shop in variables: create `shop_name`, `revenue_usd`, `n_sales`, `best_day`; print a four-line summary with one f-string per line, all numbers formatted; then change `revenue_usd` and re-print — the boxes update, the format holds.
2. The float wall: compute `0.1 + 0.2`, see the binary truth; then `round(0.1 + 0.2, 2)` and print both with an f-string explaining the difference to a colleague; reconcile a real money sum against the spreadsheet to two decimals.
3. The cleaning atoms: take the three EcoCash spellings ("EcoCash", "ecocash ", "ECOCASH") and, with `.strip().upper()` (or `.title()` if you prefer sentence-case), map all three to one; write the one-line before/after table in a Markdown cell.
4. The boolean bench: for six real sales rows (type them as variables), write booleans for "weekend", "big basket", "member", "EcoCash weekend sale"; print each with an f-string that states it in words.
5. The error museum: deliberately raise all four regulars (misspell a name, add text to a number, drop a quote, index a list at 99); for each, paste the last error line into a Markdown cell and write the fix underneath. Your museum is your future debugging speed.

## Further Reading

- Chapter 32 (control flow and functions — the atoms start combining)
- *Automate the Boring Stuff with Python* (Sweigart), chapters 1–2 — free online, the friendliest first-sixty-pages in the field
