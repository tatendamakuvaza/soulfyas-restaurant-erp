# Chapter 59: Ethics and Privacy, Essentials

*Part IX — Beyond the Basics*

> "The ethics chapter is not at the end because it is a conclusion. It is at the end because by now you can understand every example."

### In this chapter you will learn

- The five principles that govern working analysts — short enough to memorise.
- Privacy law's common core: consent, purpose, minimisation — across borders.
- Bias: where it actually enters (data, measurement, modelling) and what you owe.
- The honest-presentation duties: cherry-picking, dark patterns, the numbers that harm.
- The refusal list — the work you decline, and how to decline it.

## 59.1 The Five Principles

Data ethics as practiced — not as a philosophy seminar, but as the working rules that keep people safe and analysts employable:

1. **Consent and legitimate use** — people's data is used with permission or another lawful, honest basis; "we have it, so we may" is not a basis.
2. **Purpose limitation** — data collected for X is used for X (Chapter 47's rule, generalised: the survey about Sundays is not a marketing list).
3. **Minimisation** — collect and keep the least data that answers the question; every column is a liability as well as an asset.
4. **Honesty in representation** — the analysis says what the data says, with its limits attached (Parts I–VIII's discipline, now a *duty* and not just a craft).
5. **Do no predictable harm** — before shipping, ask who could be hurt by this number being wrong *or right*: the segment it profiles, the worker it schedules to zero hours, the neighbourhood it redlines.

These five are the common core of every serious framework — from the ACM's code to corporate policies to law (next section). Memorise them; they compress to: *used with permission, for the stated purpose, the least of it, told honestly, harming no one.*

## 59.2 Privacy Law's Common Core

You will meet data-protection law by name: **GDPR** (Europe — and the world's de facto template), **POPIA** (South Africa), Zimbabwe's **Cyber and Data Protection Act**, and their siblings. The names differ; the skeleton is the same five principles, in legal costume, plus operational rights you must be able to recognise when a stakeholder asks: **access** ("show me the data you hold on me"), **rectification** ("correct it"), **erasure** ("delete it" — the right to be forgotten, with its exceptions), **portability**, and **objection**. The analyst-relevant realities, in practice: personal data has a *lawful basis* or it does not get processed; there are **special categories** (health, religion, ethnicity, sexuality, biometrics) where the bar is higher and the purposes narrower; **anonymisation** that actually works is harder than it looks (a "anonymised" dataset of postcode + birthdate + purchases re-identifies embarrassingly often — aggregation and k-anonymity thinking exist because naive masking fails); and *someone in the room is responsible* — increasingly, by name, with training and sign-off. The career-craft version: the analyst who can say "this needs a lawful basis check before we build it" is not the blocker in the room; they are the one saving the team from the conversation nobody wants with the regulator.

## 59.3 Where Bias Enters

Bias, in the analyst's terms, is Chapter 25 wearing consequences. It enters at three doors, and the duties differ at each:

- **Data bias** — the sample is not the population: the survey that only saw in-shoppers (Ch. 47, stated), the hiring data of a biased past, the fraud data that only caught the fraudsters your current rules found. Duty: *know your sampling frame, declare its limits, and never let the quiet omission (who is missing?) pass unexamined* — the missing are rarely missing at random.
- **Measurement bias** — the instrument distorts: the churn definition that reads poverty as disloyalty (customers with less money buy less often — a 60-day silence rule flags the budget before the loyalty), the satisfaction survey only the satisfied answer, the crime statistics that measure policing, not crime. Duty: *interrogate what the number actually measures* — the "says who?" question, asked of the metric itself.
- **Modelling bias** — the model amplifies the past into the future: trained on biased history, it recommends the bias (the classic: résumé screens that learned to discount women because history did). Duty at analyst scale: *test the model's errors by group* (the error analysis of Ch. 57, disaggregated — if it fails more for one segment, say so loudly), and never let a proxy (postcode for income, purchases for health) launder a sensitive attribute through an innocuous column. The statistical vocabulary you own — base rates, false positives, selection — is precisely the vocabulary in which bias is visible; that is no coincidence.

## 59.4 Honest Presentation

The communication duties, beyond the craft you already practise: **no cherry-picking** — the window, the segment, the metric chosen because it flatters (Chapter 11's truncated axis and Chapter 26's twentieth test were rehearsals; at work, the choice of *which* finding to show is the same crime, committed with a spotlight); **no dark analytics** — the dashboard engineered to hide the declining line, the "average" chosen because the median was worse, the chart that resets its axis per quarter; and the **harms of accuracy** — the number that is *right* and shouldn't be shown: the individual-level productivity ranking (statistically fragile, humanly corrosive), the neighbourhood risk score, the list of "likely pregnant shoppers" (a real, notorious case — correct prediction, indefensible use). The analyst's question before shipping anything about people: *would I be comfortable explaining this chart, to the people in it?* — the Chapter 2 questions, finally pointed at yourself.

## 59.5 The Refusal List

The work you decline, stated now — while it is abstract — so you can recognise it when it arrives wearing a deadline and a job title: findings pre-decided ("we need the numbers to show X" — you can find what the data says; you cannot decide what it says first); deception by omission (the report that leaves out the disconfirming segment); surveillance beyond consent (the tracking whose subjects don't know); profiling of the vulnerable (predicting pregnancy, sexuality, illness — or pricing against desperation); and the re-identification of data you were told was anonymised ("just join it with this public list"). The refusal craft — because careers are built on *how*: offer the honest alternative ("I can't build a case for a pre-decided finding, but I can test whether the data supports it — and if it doesn't, you'll want to know before the board does"), escalate once, in writing, and document your dissent politely. The one-sentence spine, worth its weight in decades: **the analyst's signature is the reason anyone believes the number — guard what it is worth.**

> **From Your Toolkit — the conscience is the career:** every principle here is a chapter you already lived, generalised: consent (47), minimisation (44's licensing and 47's minimum-data), honesty (all of it), the missing-data question (8, 25, 60), the error analysis (57). The tools will change employers; the ethics travel with the signature — and in a decade of practice, they are what the reputation is made of (Ch. 56's compounding, at its longest horizon).

## Key Takeaways

- Five principles: permission, purpose, minimisation, honesty, no predictable harm — the common core of codes and law alike.
- Privacy law's skeleton is those principles plus the data-subject rights; special categories are a higher bar; naive anonymisation fails — someone is responsible by name.
- Bias enters three doors (sample, measurement, model); duties: declare the frame, interrogate the metric, disaggregate the errors — and watch the proxies.
- Presentation duties: no cherry-picking, no dark analytics, and the question "could I explain this to the people in it?"
- The refusal list and craft: offer the honest alternative, escalate once in writing, document — the signature is why anyone believes the number.

## Practice Lab

1. The principles audit, on your own shelf: run Projects 1–6 against the five principles; write the two-paragraph ethics section your portfolio README deserves (Ch. 49 promised one; here is its content).
2. The re-identification experiment: take your customers file; "anonymise" it by dropping names; then show that suburb + join-date + rough spend identifies specific individuals (join against a hypothetical public list — reason it through); write the k-anonymity note: how many people share each combination?
3. The measurement-bias gallery: find three metrics in your own work (or public life) that measure the instrument rather than the thing (school league tables, response-time metrics, engagement); for each, one sentence on what it really measures.
4. The disaggregation drill: on the churn project's error analysis, split the model's misses (or the rule's flags) by suburb and tier; report honestly whether the rule fails unevenly; write the one-line caveat the report needs.
5. The refusal rehearsal: script your response to the two requests most likely in your first year ("can you make the dashboard show growth?" and "just pull the numbers that support the proposal"); role-play both; keep the scripts — the wording, rehearsed, is what holds under deadline pressure.

## Further Reading

- Chapter 60 (messy reality — where ethics meets deadlines), *Weapons of Math Destruction* (O'Neil) — the essential book on this chapter, no prerequisites
- Your jurisdiction's data-protection act — read the principles section once; you will recognise every line
