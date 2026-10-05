# Chapter 2: The Analyst's Mindset

*Part I — Beginning: You, the Data Analyst*

> "Three habits separate trusted analysts from fast ones: be curious, be suspicious, be clear."

### In this chapter you will learn

- The three habits that make an analyst — curiosity, skepticism, clarity.
- Why the question always comes before the data.
- The three honesty rules you will be held to for the rest of the book.
- How to read a number like an analyst (the five questions to ask any figure).
- The patience loop: how beginners actually learn this craft.

## 2.1 Curiosity: The Fuel

Every good analysis begins with a small itch: *why did that happen?* The analyst's version of curiosity is specific — it is aimed at **differences and changes**. Sales fell — from what, to what, since when, where, for whom? The untrained eye reads "sales fell 5%" as a fact; the curious analyst immediately asks five smaller questions, because inside every big number there are ten smaller ones, and the interesting one is always hiding in there.

You already have this habit if you have ever wondered why one bus route is always full and the next is empty. This chapter's work is to aim the wondering at tables — and to write it down. The analyst's notebook habit: every question you ask of the data gets a line, even (especially) the ones you answer along the way to something else.

## 2.2 Skepticism: The Shield

Curiosity without skepticism is how rumours get spreadsheets. The skeptic's discipline is that **every number is an answer to a question someone chose, on data someone collected, with rules someone decided** — and any of those someones may have been tired, rushed, or hopeful. The five questions to ask any figure you meet (this book uses them constantly):

1. **Compared to what?** — "Sales are up 12%" means nothing without last month, last year, or the plan.
2. **Says who?** — where did this number come from: a till, a survey, an estimate, a guess with formatting?
3. **What is missing?** — which rows, stores, days, or people are not in the data? (The missing ones are rarely missing at random.)
4. **What was counted exactly?** — "customers" — people, or transactions? "Active" — this month, or ever?
5. **Could it be luck?** — is the difference real, or the ordinary wobble of any variable thing? (Part IV gives you the tools for this one.)

None of this is cynicism. The skeptic's posture is not "numbers are lies" but "numbers are claims" — and claims deserve polite verification. Analysts who ask these five questions pleasantly, every time, become the people whose sign-off everyone wants.

## 2.3 Clarity: The Point

Analysis that cannot be explained has not happened. The clarity habit has two halves:

- **Explain it simply.** If you cannot describe your finding to a smart twelve-year-old in three sentences, you do not yet understand it — the sentence is not a simplification of the analysis, it is the analysis, compressed. (Einstein probably never said the famous version, but the rule holds anyway.)
- **Show the uncertainty.** Numbers wobble; samples miss; next month differs. Saying "sales rose about 5% — between 3% and 7% — and we are fairly confident it is the price change, though the supply gap muddies it" is not weakness. It is the reason the listener can build on your number without being ambushed later.

Clarity is a service ethic. Your reader has thirty seconds and other meetings. The whole of Part VI (charts, dashboards, the one-page story) is this habit, given tools.

## 2.4 The Three Honesty Rules

For the rest of this book — and the rest of your career — you are held to three rules. They will be repeated until they are reflexes:

1. **The average is not the answer.** Averages hide the very differences that decisions need. The average customer does not exist; the average of 10 and 1000 is 505, which describes neither. Whenever you meet an average, you will ask (Chapter 22) what it is hiding.
2. **Correlation is not causation.** Ice cream sales and drownings rise together every summer — because of the sun, not the ice cream. Two things moving together is a clue for investigation, never a conclusion. Chapter 28 teaches you to catch your own mind making this mistake.
3. **The sample is not the population.** The 200 people who answered your survey are not "the customers"; they are the customers who answer surveys. Chapter 25 shows what that costs and how to adjust for it.

None of these rules require mathematics. They require the willingness to say "not yet proven" in a meeting where everyone wants "proven" — which is, again, exactly why the people who say it are trusted.

> **From Your Toolkit — your notebook:** paper or a notes app is the analyst's zeroth tool. From today, every piece of work in this book starts with three lines in your notebook: *the question, the decision it serves, what I expect to find.* You will be amazed (in about six weeks) how much of your own learning lives in those notebooks.

## 2.5 Reading a Number Like an Analyst

A quick drill to make the habits concrete. A colleague says: "Our new loyalty programme is working — members spend 40% more than non-members."

- **Curiosity:** 40% more — per visit, or per month? All members, or the ones who joined? Since when?
- **Skepticism:** compared to what — non-members who chose not to join, or people who were never asked? What if the people who join a loyalty programme were always the frequent shoppers? (They usually are. This exact trap — and its cure — is Chapter 28's centerpiece.)
- **Clarity:** the honest version: "Members spend 40% more than non-members; some of that difference existed before they joined. To measure the programme properly we would need..." — and now you sound like the most valuable person in the room, because you are.

That paragraph is the whole mindset in ninety seconds: itch, doubt, translate. Everything else in this book is giving those three habits tools.

## 2.6 The Patience Loop

Beginners learn this craft in a loop, and knowing the loop prevents the week-three dropout that claims most self-learners:

1. **Confusion** ("what even is a dataframe?") — normal, required, temporary.
2. **A small win** (the query runs; the chart appears) — worth more than it looks.
3. **A small failure** (the query runs *wrong*) — where the actual learning happens.
4. **The explanation that clicks** ("it is just a table — a spreadsheet I can program").

One loop is maybe twenty minutes. A chapter of this book is a few loops. The tools change the loop's content, never its shape — the confusion you feel meeting SQL in Chapter 15 is the same confusion you will feel meeting Python in Chapter 31, and the same feeling you will professionalise on the job forever. Analysts are not people who stopped being confused; they are people who learned that confusion is the working state of anyone learning anything worth learning.

## Key Takeaways

- Three habits: be curious (differences and changes), be skeptical (numbers are claims), be clear (three sentences and the uncertainty).
- Ask any number five questions: compared to what, says who, what is missing, what was counted, could it be luck.
- Three honesty rules, forever: the average is not the answer; correlation is not causation; the sample is not the population.
- The notebook habit: question, decision, expectation — three lines before any tool.
- The patience loop (confuse, win, fail, click) is the shape of learning every tool in this book.

## Practice Lab

1. Take today's headline number from any news site and run the five questions at it. Write the answers you *wish* you could get — those wishes are real analytical questions someone is paid to answer.
2. The average trap: find a real "average" in an advert or article (average salary, average customer, average rating). Write two sentences on who or what it might be hiding.
3. Correlation hunt: list three pairs of things that rise together (ice cream and drownings style). For each, write the hidden third factor.
4. Start the notebook: three lines for a question in your own life with numbers in it (spending, time, marks, fitness). Keep the notebook by Chapter 5 — the running case will move into it.
5. Reframe the loyalty claim: rewrite "members spend 40% more" in the honest version from Section 2.5, in your own words, as if to your manager.

## Further Reading

- *How to Lie with Statistics* — Darrell Huff (sixty years old, one hour to read, permanently useful)
- Chapter 22 (why averages lie, with pictures), Chapter 25 (samples), Chapter 28 (the causation trap)
