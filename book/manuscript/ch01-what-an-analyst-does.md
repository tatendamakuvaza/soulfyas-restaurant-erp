# Chapter 1: What a Data Analyst Actually Does

*Part I — Beginning: You, the Data Analyst*

> "The job is turning numbers into decisions — everything else is detail."

### In this chapter you will learn

- What a data analyst's day actually looks like, hour by hour.
- The five myths about the job — and the truth behind each.
- The one sentence that defines the whole profession.
- Where analysts work, what they earn, and who they answer to.
- A first taste of the running case you will work with for the whole book.

## 1.1 The Job in One Sentence

Strip away the job adverts, the buzzwords, and the software logos, and a data analyst does one thing:

> **A data analyst collects information, cleans it up, studies it, and explains what should be done about it — in language the decision-maker understands.**

Every chapter of this book is one of those four verbs. Collecting (Parts II, III, V), cleaning (everywhere, and more than anyone expects), studying (Part IV), and explaining (Part VI). If you remember nothing else today, remember the sentence: it is your compass whenever a tool or a technique feels confusing. Ask *which verb is this?* and the confusion usually shrinks.

## 1.2 A Day in the Life

A realistic Tuesday for a junior analyst at a retail company (the same world as the grocery store you will meet in Chapter 5, just bigger):

| Time | What is happening |
|---|---|
| 08:00 | Coffee, inbox: a manager asks why last week's sales dipped. The question of the day is born. |
| 08:30 | Pull the data — a SQL query against the sales database (Part III of this book). |
| 09:00 | Clean and check it: missing rows from one store's till, a duplicate upload, prices in the wrong column. Half the morning goes here. This is normal and never stops being normal. |
| 10:30 | Explore: totals by store and by day in a pivot table; a chart or two. The dip is real, mostly in one product line. |
| 11:30 | Dig deeper: was it the price change two weeks ago? A competitor's promotion? A supply gap? The analyst becomes a detective. |
| 13:00 | Write the summary: half a page, three numbers, one chart, a recommendation ("hold prices another two weeks; the dip is mostly the supply gap"). |
| 14:00 | Walk the manager through it. Answer "what about the Bulawayo store?" three times, pleasantly, with the numbers ready. |
| 15:00 | Update the weekly dashboard so everyone can watch the number recover. |
| 16:00 | A recurring report needs refreshing — the analyst spends thirty minutes on what will become a five-minute Python script by Chapter 37. |
| 17:00 | Note tomorrow's follow-up: the supply-gap theory needs one more dataset. |

Notice what is *not* there: no mathematics beyond arithmetic, no dramatic model-building, no solitary genius work. The real job is roughly **half communication and cleaning, a third exploration, and the rest tools** — which is good news, because those are all learnable, and this book teaches them in exactly that order.

## 1.3 Five Myths, Five Truths

1. **Myth: "You must be great at mathematics."** Truth: analysts need arithmetic, percentages, and clear thinking. The statistics in Part IV is taught here by counting and plain English — that is how working analysts actually reason.
2. **Myth: "You must have a computer science degree."** Truth: analysts arrive from every field — commerce, health, agriculture, admin. Employers test what you can *do*; by Part VII you will have three projects to show.
3. **Myth: "It is all about the latest AI."** Truth: the daily bread is tables, joins, and charts. AI is a map we draw in Chapter 57 — useful, later, optional.
4. **Myth: "It is a lonely job with a computer."** Truth: it is a service job. Your numbers only matter when a person trusts them enough to act — which makes Chapter 43's presentation skills as career-critical as any query.
5. **Myth: "The tools change too fast to learn."** Truth: the grammar is stable. The same table-join you will meet in Excel (Chapter 9), SQL (Chapter 17), and Python (Chapter 34) has not changed in decades. Learn the grammar once and tools become interchangeable accents.

## 1.4 Where Analysts Work and What They Earn

Every industry that records anything employs analysts: banks and insurers, retailers and manufacturers, hospitals and ministries, telecoms, farms, football clubs, and every consultancy that serves them. In most markets, junior analysts earn a solid professional salary from day one, with a clear ladder (Chapter 56) — senior analyst, lead, and specialist routes into data engineering, data science, or analytics management. The skill also travels: the same SQL that analyses a bank's loans in Harare analyses a hospital's queues in Nairobi or a retailer's stock in London, unaltered. Few careers are this portable.

And the freelance route is real: small businesses everywhere need exactly what this book teaches — a monthly report, a dashboard, a survey analysed — and Chapter 55 shows how to price and deliver that work from a laptop.

## 1.5 The Decision Is the Destination

Here is the habit that separates analysts from people who merely make spreadsheets: **before any work begins, they ask what decision the answer will change.** A manager's "can you pull the sales numbers?" is an invitation to a trap — a week of work answering a question nobody was asking. The professional reply is a gentle question: *"When you have the numbers, what will you do with them?"* If the answer is "decide whether to keep the Sunday opening", you now know exactly which numbers matter (Sundays versus other days, costs, footfall), which do not, and — by the end of Part IV — whether the difference is real or just noise.

> **From Your Toolkit — everything:** this habit costs nothing and works in every tool you will ever learn, because it happens before any tool is opened. Keep a one-line note at the top of every piece of work you do in this book: *the decision this serves.* By the projects of Part VII it will be automatic — and interviewers can smell the difference in candidates immediately.

## 1.6 What You Will Not Need

Reassurance, in writing:

- **No degree** is required to follow this book or to build its portfolio.
- **No mathematics beyond arithmetic** — every statistical idea is introduced by counting real cases first.
- **No paid software** — one afternoon in Chapter 4 and your toolkit is complete, free.
- **No prior experience** — the running case assumes you are starting exactly where you are.

## Key Takeaways

- The job in one sentence: collect, clean, study, explain — numbers into decisions.
- A real day is half cleaning and communication, a third exploration, the rest tools. All learnable, in that order.
- The five myths are false: no advanced maths, no CS degree, no AI prerequisite, not lonely, not a tools race.
- The defining habit: ask what decision the analysis will change, before touching any tool.
- The skill is portable, the ladder is real, and the freelance route exists from day one.

## Practice Lab

1. Find one real job advert for a "data analyst" near you (any job site). Circle every skill it mentions, and sort them into the four verbs: collect, clean, study, explain. Notice how the list stops looking scary once sorted.
2. Interview one person you know who uses spreadsheets at work (five minutes): what decision do they make with them? What do they wish they knew about their numbers? Write three lines.
3. Write your own one-line answer to "why do you want to be a data analyst?" — you will refine it in Chapter 51, and it is never too early to start.
4. Myth audit: which of the five myths had you believed? Write one sentence about where you think it came from.
5. The compass test: for each of these requests, write the decision question behind it — "how many visitors did our website get?", "which product sells best?", "are our customers happy?".

## Further Reading

- Chapter 2 (the mindset behind the job), Chapter 50 (the job landscape in detail)
- Any "day in the life of a data analyst" video, 15 minutes, any platform — see how many of this chapter's hours you can spot.
