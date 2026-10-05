# Chapter 14: What a Database Is

*Part III — SQL: The Language of Data*

> "A spreadsheet is a whiteboard; a database is a filing system with a guard at the door."

### In this chapter you will learn

- Why Tariro's data outgrew the spreadsheet — the honest limits, in her story and in general.
- Tables, rows, columns, keys — the database vocabulary, mapped to what you already know.
- What a relational database is, and why "relational" is the point.
- SQLite and DB Browser for SQLite: a complete database engine, free, in fifteen minutes.
- How to load one of Tariro's CSVs and see it as a database table.

## 14.1 The Day the Spreadsheet Broke

Month 19: Tariro's grocery adds a second till, a part-time cashier, and — the real change — a **supplier database** her wholesaler emails monthly. Her workbook now has sales from two tills that must not be double-counted, stock counts from a Sunday ritual, customer sign-ups on a tablet, and supplier prices in a fourth file. The workbook becomes five files, then eight, then "final_v7_REALLY.xlsx". One afternoon the part-time cashier sorts one column of one sheet without selecting the row labels: three months of amounts detach from their dates. Nobody notices for a week.

That afternoon is why databases exist. The spreadsheet's strengths — see everything, touch everything — become its failures at scale: it stores *data* and *layout* and *analysis* in one fragile object; it lets any cell hold anything; and it has no memory of who changed what. A **database** separates storage from presentation, enforces rules at the door (this column holds dates; this key is never empty), and is built for many tables that stay consistent. Analysts do not abandon spreadsheets — reporting still lives there — but the *source of truth* for anything that grows moves to a database, and the analyst's job is to query it.

## 14.2 The Vocabulary

A **table** is a grid you already understand, with rules attached. Map it across:

| Spreadsheet | Database | The difference that matters |
|---|---|---|
| Sheet | Table | One kind of thing per table: `sales`, `customers`, `stock`, `suppliers` |
| Row 1 headers | Column names | Defined once, enforced; no merged cells, ever |
| Data row | Row (record) | One sale, one customer — no totals rows mixed in |
| The whole file | Database (schema) | Many related tables, named and governed |
| "that ID column" | Key (primary/foreign) | The join idea from Chapter 9, formalised |

Two kinds of key, and they are the whole of "relational": a **primary key** uniquely identifies each row in its own table (`customer_id` in `customers` — one row per customer, the column never repeats, never empty); a **foreign key** is a column in another table that *points* at it (`customer_id` inside `sales`, repeating freely — one customer, many sales). The relationship lives in the pair: customers-to-sales is **one-to-many**, the most common shape in all of business data. This is exactly the VLOOKUP key from Chapter 9 — the database just gives it a name, a rule, and a guard.

## 14.3 Relational: The Point

The **relational model** — one table per kind of thing, keys connecting them — is the design principle behind nearly every database you will meet at work. Its power is that each fact is stored **once, in its rightful place**: the customer's suburb lives only in `customers`; a sale records only `customer_id`. Update the suburb once, and every query that joins sees the change — no eight-file hunt, no copy drifting out of date. Its discipline is that you must *ask* rather than *browse*: the database does not show you everything; it answers questions. The asking language is SQL, next chapter.

Tariro's shop, designed relationally, is four small tables:

```text
customers(customer_id, name, suburb, joined, loyalty_tier)
sales(sale_id, date, till, customer_id, payment_type, amount)
stock(week, item, quantity_on_hand)
suppliers(item, supplier, unit_cost, last_price_change)
```

Read the parentheses and you can see the whole business: who shops (customers), what they bought (sales), what is on the shelves (stock), what it costs (suppliers). The keys in the middle — `customer_id` in sales — are the threads that tie them. Four modest tables will carry every question in Part III and most of the rest of the book.

## 14.4 SQLite and DB Browser

Databases you will hear named at work — MySQL, PostgreSQL, SQL Server — are *servers*: engines installed somewhere, connected to over a network. They matter (Chapter 57's world), but learning is better served by **SQLite**: a complete, industrial-grade relational engine that keeps each whole database in a single file and powers most of the world's phones. There is nothing to install as a service, nothing to configure, and the SQL you learn on it is 95% identical everywhere.

The companion tool is **DB Browser for SQLite** (sqlitebrowser.org; free, Windows/Mac/Linux): a friendly window onto database files — browse tables, edit values, and above all run SQL queries and see results. Install both habits now:

1. Download and install DB Browser for SQLite (five minutes, no account).
2. Open it → New Database → save as `tariros.db` in your `tariro-data` folder.
3. **File → Import → Table from CSV file** → your cleaned `sales.csv`. Tick "Column names in first line". DB Browser guesses types — check the guess (Chapter 4's lesson again: dates as dates, amounts as numbers) and let it create the table.

Double-click the `sales` table in the list: there it is — eighteen months and two tills of trading, now a governed table with typed columns and no detached-sort accidents possible. That feeling — the data now *holds still* — is what a database sells.

> **From Your Toolkit — one engine, many accents:** SQLite is your learning engine here, and Python ships it inside (`sqlite3`, no install — Chapter 33 reads this same `tariros.db` with code), Power BI connects to it directly (Part VI), and its file format is how this book's appendix datasets ship. At work the engine will be named PostgreSQL or SQL Server — the chapter SQL transfers almost line for line (Appendix A notes the dialect differences). The model — tables, keys, relations — never changes at all.

## Key Takeaways

- Spreadsheets mix storage, layout, and analysis; databases separate them and enforce rules at the door.
- One table per kind of thing; primary keys identify rows, foreign keys point across tables; one-to-many is the default shape.
- The relational model stores each fact once — updates propagate, copies cannot drift.
- SQLite + DB Browser: a real relational engine and a friendly workbench, free, in minutes; your `tariros.db` is born.
- Servers (PostgreSQL, MySQL, SQL Server) are the work version of the same idea — the SQL and the model transfer.

## Practice Lab

1. Sketch on paper the four tables of Tariro's shop; mark each primary key and each foreign key with an arrow; write under each arrow the relationship in words ("one customer → many sales").
2. Install DB Browser for SQLite, create `tariros.db`, and import your cleaned `sales.csv` as a table; open the table and confirm row count matches your workbook (reconciliation habit — always).
3. Import `customers.csv` the same way; check that DB Browser's type guesses are right (member ids stay text, `joined` is a date, suburb text); fix any column it mistyped and re-import.
4. Design on paper (do not build yet): where would a `tills` table or `staff` table plug in? Which existing tables would grow a foreign key? Two sentences each.
5. The guard, demonstrated: in DB Browser, try typing text into the `amount` column of a row and saving; record what the engine says. Write one sentence on why the spreadsheet never argued with you — and who paid for that silence.

## Further Reading

- Chapter 15 (SELECT, WHERE — the asking begins), Chapter 20 (the work databases by name)
- sqlitebrowser.org — the tool's own quick tour
