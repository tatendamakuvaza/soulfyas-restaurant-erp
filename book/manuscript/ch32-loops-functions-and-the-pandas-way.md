# Chapter 32: Loops, Functions, and the Pandas Way

*Part V — Python: From Zero to Dangerous*

> "A loop repeats. A function is a reusable sentence. And pandas does to both what the combine harvester did to the scythe."

### In this chapter you will learn

- Lists and dictionaries: boxes that hold many things.
- `for` loops and `if` decisions — flow, in two keywords.
- Functions: your own verbs, defined once and used forever.
- The pandas way: *vectorised* operations — why analysts loop rarely.
- A complete mini-program: the daily exceptions report, from scratch.

## 32.1 Collections

Single variables hold one thing; analysis holds *many*. Python's two everyday containers:

```python
# a list: ordered, numbered, editable -- the column's raw material
items = ["Maize meal 10kg", "Cooking Oil 2L", "Rice 2kg"]
items[0]              # "Maize meal 10kg" -- counting starts at ZERO
items[-1]             # "Rice 2kg" -- the last, from the end
items.append("Sugar 1kg")

# a dictionary: label -> value -- the row's raw material
sale = {"date": "2025-06-14", "amount": 11.50, "payment_type": "EcoCash"}
sale["amount"]        # 11.5 -- fetch by name, not position
sale["till"] = 2      # add a key
```

Zero-based counting is Python's first ambush: `items[1]` is the *second* item. It is not pedantry; it is how offsets work (position 1 means "one step from the start"), and every tool in this book secretly agrees (Excel's `INDEX`, SQL's `LIMIT ... OFFSET`). The dictionary is the more important analyst object: a table row *is* a dictionary (column names → values), and a DataFrame is a million of them — hold that mental image and pandas never feels arbitrary.

## 32.2 Flow: for and if

The **for loop** visits every item in a list; the **if statement** chooses:

```python
daily_takings = [2980, 1520, 3410, 890, 3120, 4270, 2650]

for takings in daily_takings:
    if takings < 2000:
        print(f"Quiet day: ${takings:,} -- check the log")
    elif takings > 4000:
        print(f"Great day: ${takings:,} -- what happened?")
    else:
        print(f"Ordinary day: ${takings:,}")
```

Read it aloud: *for each* takings in the list, *if* it is low say quiet, *else if* high say great, *else* ordinary. The colons and the indentation are not decoration — **indentation (four spaces) is how Python knows what belongs inside the loop and the if**. Get it wrong and `IndentationError` tells you; get it right and the structure of your code is visible in its shape, which is why Python reads like a recipe. (A `while` loop also exists — "repeat until a condition breaks"; rare in analyst code, recognised on sight in others'.)

## 32.3 Functions

A **function** is a sentence you define once and use forever — input in parentheses, answer from `return`:

```python
def day_verdict(takings, low=2000, high=4000):
    """Classify one day's takings as quiet/ordinary/great."""
    if takings < low:
        return "quiet"
    elif takings > high:
        return "great"
    return "ordinary"

day_verdict(890)          # "quiet"
day_verdict(4270)         # "great"
day_verdict(1520, low=1200)   # "ordinary" -- the threshold is an argument
```

The professional payoffs are exactly the query-pack's payoffs (Chapter 20's etiquette, now in code): **named once, tested once, reused everywhere**; **arguments make assumptions visible** (the thresholds are not buried, they are parameters); and the **docstring** (the triple-quoted sentence under the `def`) documents the *why*. Your Part II IQR fence, your z-score, your reconciliation check — all are functions in this book's `toolkit.py` by the end of this Part. Analysts who write functions stop repeating themselves; analysts who stop repeating themselves stop making copy-paste errors — the same argument as CTEs, the same argument as syntax files, the same argument as do-files. It is all one discipline.

## 32.4 The Pandas Way

Now the culture shock that defines working Python. You *could* loop over 6,420 sales and add up the EcoCash ones:

```python
total = 0
for amount, ptype in zip(amounts, payment_types):
    if ptype == "EcoCash":
        total = total + amount
```

It works — and it is how you would explain a sum to a child. Python's (and pandas') native idiom is to say it *to the whole column at once*:

```python
sales.loc[sales["payment_type"] == "EcoCash", "amount"].sum()
```

— a filter (a boolean, Chapter 31!) selecting rows, then `.sum()` over the selected column: **vectorisation** — one instruction applied to every row internally, at C speed. On 6,420 rows the difference is comfort; on a million it is the difference between a second and a coffee. The loop is not wrong — it is *for explanation*; the vectorised line is *for work*. The rule you will hear from every professional: **if you are writing a for loop over a DataFrame's rows, there is almost always a pandas one-liner you are missing** — and this book's job in Chapter 34 is to hand you the one-liners.

## 32.5 A Complete Mini-Program

Everything in this chapter, assembled into something real — the daily exceptions report (Chapter 24's flagging instrument, now as code). Type it into one cell; it is your first program, not your first exercise:

```python
def exceptions_report(takings_by_day, mean=None, sd=None):
    """Flag days whose takings are more than 2 SDs from typical."""
    if mean is None:                       # compute if not supplied
        mean = sum(takings_by_day) / len(takings_by_day)
    if sd is None:
        sq = [(t - mean) ** 2 for t in takings_by_day]
        sd = (sum(sq) / (len(sq) - 1)) ** 0.5

    flags = []
    for day, t in takings_by_day:
        z = (t - mean) / sd
        if abs(z) > 2:
            flags.append((day, t, round(z, 1)))
    return flags

week = [("Mon", 2980), ("Tue", 1520), ("Wed", 3410),
        ("Thu", 890), ("Fri", 3120), ("Sat", 4270), ("Sun", 2150)]

for day, t, z in exceptions_report(week):
    print(f"{day}: ${t:,} (z = {z:+.1f}) -- investigate")
```

Find what is inside it: a list of tuples, a function with defaults and a docstring, a loop, an if, a z-score computed from scratch (with the n−1 divisor — you know why), an f-string with a signed format, a filter list. Eleven meaningful lines; and when Chapter 34 rewrites it in three lines of pandas, you will know *exactly* what those three lines are doing — because you built the machine they replace. That is the honest way to learn a high-level tool: build the wheel once, then accept the car.

> **From Your Toolkit — flow is forever:** for/if/functions are the atoms of *all* code you will ever read — the do-files of Chapter 29, the SQL of Part III (a CTE *is* a function's cousin; WHERE *is* an if; GROUP BY *is* a loop with manners), and the automation scripts of Chapter 37 and Project 5. And the vectorised instinct returns as SQL's set-thinking: describe the *what*, let the engine do the *how*.

## Key Takeaways

- Lists are numbered columns (counting from zero); dictionaries are labelled rows; a DataFrame is a million dictionaries.
- for visits, if chooses, indentation *is* the structure — Python reads like a recipe because it is shaped like one.
- Functions: define once, use forever; arguments make assumptions visible; docstrings carry the why.
- The pandas way: vectorise — filters and methods over columns, not loops over rows; loops explain, one-liners work.
- The mini-program is the chapter: collections + flow + function + f-strings = the exceptions report, your first real artefact.

## Practice Lab

1. The tour of containers: build a five-sale list of dictionaries; print the third sale's amount, the last sale's payment type; add a sale; loop over all five and print an f-string line each ("sale 3: $11.50 by EcoCash").
2. The weekday classifier: write `day_verdict(takings, low, high)` with a docstring; classify a full week; then classify with different thresholds and note in a Markdown cell *which business question* each threshold answers.
3. The fence, as a function: implement `iqr_fences(values)` returning the pair (lower, upper) — reuse it on `amount` data and reconcile against your Part II fence values exactly.
4. Loop vs pandas: compute EcoCash revenue both ways (the loop, then the one-liner) and time both with `%%time` as the cell's first line; record the two numbers; write the sentence about what vectorisation buys.
5. Extend the mini-program: add a `summary` function that takes the flags and returns an f-string paragraph ("3 exceptional days this week: Tue (z = −2.1), Thu (z = −3.4), Sat (z = +2.0)"); wire it into `exceptions_report`; Restart & Run All; save as `exceptions-report-v1.ipynb` — version one of a tool you will rebuild in Chapter 34 and automate in Chapter 37.

## Further Reading

- Chapter 33 (pandas properly — the DataFrame grammar), Chapter 34 (the analysis one-liners)
- *Automate the Boring Stuff* (Sweigart) chapters 3–6 (functions, lists, dictionaries) for extra reps
