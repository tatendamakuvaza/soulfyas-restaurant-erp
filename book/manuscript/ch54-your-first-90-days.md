# Chapter 54: Your First 90 Days

*Part VIII — Getting the Job*

> "You spent a book learning to analyse. The first ninety days are the analysis of you — run them like a project."

### In this chapter you will learn

- Days 1–30: learning the terrain — the data, the people, the questions that already exist.
- Days 31–60: the first owned deliverable, and the quick win that buys trust.
- Days 61–90: the systematisation that makes you indispensable.
- The stakeholders: whom to meet, what to ask, how to say no while new.
- The traps of the new analyst — the five ways beginners quietly fail.

## 54.1 Days 1–30: Learn the Terrain

The beginner's error is proving yourself with immediate cleverness; the professional's opening move is a *listening tour* with a notebook. Your first month is three maps:

- **The data map**: where does data live, really? (Warehouse, vendor exports, the finance director's personal spreadsheet that is somehow the source of truth.) What are the tables, the refresh schedules, the *known* flaws — and who knows them? Ask every person the same question: *"if a number looks wrong, who would you ask?"* — the answers draw the org chart of trust. Then run Chapter 44's first hour on the main datasets, for real: types, nulls, the reconciliation sweep. You are not fixing anything yet; you are building the map every future fix will use.
- **The people map**: your manager (what does *their* boss ask *them* monthly? — that question is the job), the senior analyst (your mentor-in-place; bring specific questions, not general neediness), the stakeholders (who consumes numbers; who blocks; who is quietly right), and the engineers (the relationship that pays for years: they know why the data is the way it is). One coffee, one genuine question, each — the *notes* are the deliverable.
- **The questions map**: what reports already exist (get them all — the weekly pack, the dashboard nobody opens, the ad-hoc slide decks)? What questions do people repeat? Every repeated question is either an automatable answer or an unresolved argument — and both are your 90-day material.

## 54.2 Days 31–60: First Deliverable and the Quick Win

Choose the first owned deliverable with Chapter 45's anatomy and one new criterion — *visibility*: a recurring deliverable somebody already wants, ideally one the previous analyst delivered slowly. Take the monthly sales pack (every company has one): rebuild it with the full craft — loading checks, reconciliation to the known totals, tested findings with caveats, the one-page front, the log. Ship it *early* (before the deadline, once), and the message lands: this one is safe to hand bigger things.

Then the **quick win**: a fix so obviously valuable it cannot be argued with, sized to a week. The classic shapes, all from this book: the reconciliation report that catches the double-counted source before month-end (Ch. 17's law, productised); the 90-minute report that becomes 10 automated minutes (Ch. 37, the story you already own); the dashboard whose broken filter nobody had time to fix; the top-ten query pack for the stakeholder who emails "can you pull..." weekly. The quick win's mechanics matter: *state the before* ("this takes Sue 3 hours monthly"), *deliver the after with the number* ("it now takes 10 minutes"), and *credit the people who helped* — the win buys trust for the system, not the ego.

## 54.3 Days 61–90: Systematise

The month that converts "promising new hire" into "load-bearing analyst": you stop *doing* the work and start *building the way the work is done*. The moves: **document** — the READMEs, runbooks, and query-pack headers of Chapters 20 and 37, applied to everything you touched; a successor should run your monthly pack from your runbook alone (test that claim — hand it over for one cycle). **Automate the second time** — anything done twice gets scheduled; the pipeline habit, applied to your own calendar. **Take the recurring question** — the one from your questions map with the most askers — and answer it *permanently*: a dashboard tile, a saved query, a weekly mail. And **measure yourself**: at day 90, write your own review — what ships faster because of you, what breaks less, what does the team know now that it didn't — the Chapter 51 bullet craft, applied to the job itself. (That document, kept quarterly, is the raw material of every future promotion case — Chapter 56's ladder is climbed on these.)

## 54.4 Saying No While New

The trap nobody warns juniors about: the requests. "Can you just pull this quickly?" (a day's work, undefined), "can you make the dashboard show the numbers we want?" (a request to break the data), "can you take on this side project?" (someone else's abandoned headache). The polite-refusal toolkit, learnt early: **clarify before committing** ("happy to look — what decision is this for? deadline? who else has asked?" — half of all requests dissolve at this question, because they were exploratory); **negotiate sequence, never just say yes** ("I can take this on after the month-end pack on the 5th, or sooner if we bump X — which would you prefer?"); and **the two words that protect your integrity forever**: "let me check the data first" — the sentence that makes you *slow once* and trusted always. New analysts who say yes to everything build the reputation of a vending machine; the ones who clarify and sequence build the reputation of an analyst. Ninety days decides which.

## 54.5 The Five Traps

The quiet failure modes, named so you can check yourself against them monthly:

1. **Tool peacocking** — leading with clever code on problems a pivot solves. The tools serve the question; nobody credits a scissor lift used to change a lightbulb.
2. **Skipping the reconciliation** — inheriting data, assuming it is clean; the previous analyst's numbers wrong *becomes* your numbers wrong the moment you touch them. Bridge-check everything you inherit, on day one.
3. **Going dark** — working two weeks on the perfect thing nobody asked for. Ship small, show early, course-correct in daylight (the small-cells habit, applied to careers).
4. **Caveat-free confidence** — presenting findings without the limits; the first time a stakeholder finds your hole, the trust debt is enormous. The Part IV discipline is a career-long one.
5. **Becoming the report machine** — letting the job collapse into producing the weekly pack. The pack is the floor, not the ceiling; the questions map keeps pointing at the ceiling, and 61–90 is when you claim it.

> **From Your Toolkit — the first project is you:** notice what the ninety days actually are: the five moves of Chapter 45, run on yourself — *question* (what does this team need?), *data* (the terrain maps), *analysis* (the deliverables), *communication* (the coffees, the numbers-with-names), *checking* (the self-review, the traps audit). The book's final reframe: you are the dataset now — profile yourself honestly, clean your habits, ship your improvements, and reconcile your promises against your delivery.

## Key Takeaways

- Month 1: three maps (data, people, questions) and the first-hour liturgy on the main datasets; listen before fixing; ask "who would you ask if a number looked wrong?"
- Month 2: a visible recurring deliverable rebuilt with full craft and shipped early; then a one-week quick win with a stated before/after and shared credit.
- Month 3: systematise — runbooks a successor could run, automate-the-second-time, permanently answer one recurring question, and write your own 90-day review.
- Requests: clarify (half dissolve), negotiate sequence, and "let me check the data first" — the vending-machine reputation is the one to avoid.
- The five traps: tool peacocking, skipping reconciliation, going dark, caveat-free confidence, becoming the report machine — audit yourself monthly.

## Practice Lab

1. The 90-day plan, written: adapt this chapter's arc to the role you are hunting (Chapter 50's postings tell you the deliverables); one page, the three months, the measurable self-review dated.
2. The question kit: write your ten terrain questions (two per map — data, people, questions, requests, traps); memorise the three you will ask on day one; they are now yours in any job, forever.
3. The refusal rehearsal: script polite responses to the four classic trap requests; role-play with a friend playing an urgent stakeholder; note where you caved and rebuild the sentence.
4. The traps audit, on yourself: score yourself 1–5 on the five traps *today* (from your projects, study, or work history); write the one-line antidote for your two worst; schedule the monthly self-audit.
5. The self-review template: create the quarterly document now (what ships faster, what breaks less, what do they know now) and fill it once for your job-hunt itself — you have been running a 90-day project since Part I, and it deserves its review.

## Further Reading

- Chapter 55 (the freelance lane — the same 90-day logic, compressed into small paid engagements)
- *The First 90 Days* (Watkins) — the leadership classic; this chapter is its analyst translation
