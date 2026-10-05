# Chapter 60: Media and Sport Analytics — The Nhaka FC and Kumba Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Sport measures everything and wins nothing by measuring; media measures nothing and calls it reach. Both are wrong the same way."

### In this chapter you will learn

- The two-headed canvas: performance analytics (sport) and attention analytics (media).
- Sport: expected goals in miniature, recruitment value, and injury risk as a survival problem.
- Media: the metrics that pay — attention, churn, and content decay.
- Kumba's frontier: analytics and language technology for low-resource markets.
- The storytelling bridge: how analytics becomes broadcast.
- Failure modes: Goodhart ruins the game, and reach is not revenue.

## 60.1 The Two-Headed Question

This playbook pairs two industries that share one underlying commodity — **attention** — and one shared failure: measuring what is easy instead of what matters. **Nhaka FC** is a fictional Premier Soccer League club: 28 professional players, an academy, modest revenue, and a technical director who wants to stop signing players "because the chairman saw them once". **Kumba** is a fictional media and language-technology company: streaming radio and news in Shona and Ndebele, a small advertising business, and a language-services division whose frontier work — Chapter 65's low-resource NLP — is watched from well beyond Harare. The canvas, twice:

| Slot | Nhaka FC's answer | Kumba's answer |
|---|---|---|
| Core question | Which players, which style, which risks — at what wage? | Which content, for whom, at what attention value? |
| Unit of analysis | The match event; the player-season; the session | The listener-session; the content item; the campaign impression |
| Key metrics | Expected goals for/against, points per wage, availability rate | Listening hours, subscriber churn, attention per content dollar |
| Data reality | Event-coded matches, GPS training loads, sparse injury records | Streaming logs, app telemetry, no panel ratings, Shona/Ndebele content untitled |
| First project | The recruitment value ledger | The content decay curve |
| Failure mode | Metrics that ruin the playing style | Reach that never becomes revenue |

## 60.2 Sport: Expected Goals in Miniature

The idea that changed football analytics: shots are not equal, so count the *quality* of chances. A minimal expected-goals (xG) model — the shot's outcome probability given location, body part, and assist type — is a logistic regression you can fit in an afternoon and defend in a pub:

```python
import statsmodels.formula.api as smf
model = smf.logit("goal ~ distance + angle_rad + header + fast_break",
                  data=shots).fit()
shots["xg"] = model.predict(shots)
# A season's story: goals minus xG = finishing (or luck) above chance creation.
```

The honest uses: xG over a season separates *chance creation* from *finishing luck* (a striker 6 goals above xG is due a regression the wage negotiation should know about); xG against exposes a defence that has been bailed out by its goalkeeper; and the rolling xG difference is the earliest signal that the team's style has changed. The honest caveats: sample sizes are small (a season is ~350 shots), the model is only as good as the event coding, and — the classic — xG is a *scouting* tool, not a tactic: a team that optimises shot-taking to maximise xG becomes predictable (Section 60.6's Goodhart, in boots).

## 60.3 Recruitment and Injury

**Recruitment value** is the club's moneyball ledger: contribution (xG+xA per 90, availability-weighted) per wage dollar, compared honestly against the *replacement* — the academy player who costs a stipend. The craft is the comparison set: a winger scouted against the whole league looks average; against age-mates in the same tactical role, he is a bargain or a fraud. **Injury analytics** is Chapter 63's survival discipline in tracksuit: hazard of injury as a function of training load (GPS distance, high-intensity efforts), congestion (matches per 14 days), and history — used to *manage exposure* (rotate before the hazard spikes), never to promise that a player will stay fit. Availability is the quiet metric: the squad's expected available minutes is worth as many points as any signing.

## 60.4 Media: Attention That Pays

Kumba's analytics stand on one honest distinction: **reach is not attention, and attention is not revenue**. Reach counts devices; attention measures minutes; revenue needs *minutes that advertisers or subscribers will pay for*. The core artefacts:

- **The content decay curve**: listening by content item against minutes-since-publication, by format — news decays in hours, drama serials in days, and the shape (not the peak) tells the schedule what to commission next.
- **The churn layer**: Chapter 27's retention curves on subscriber data — which programmes appear in the listening histories of those who stay? (Correlation, honestly labelled; the causal test is Chapter 61's — stagger a schedule change across regions and watch.)
- **The attention ledger**: listening hours per content dollar, by format and language — the commissioning meeting's one table.

**From Your Toolkit — Power BI:** the attention dashboard is a genre you know: cohort retention curves, a decay chart per format, and the commissioning table on the front page. The bridge: this is the same retention analytics as Zuva Mobile (Chapter 52) with listening minutes in the ARPU seat.

## 60.5 Kumba's Frontier: Language Technology

Kumba's deepest analytics problem is Chapter 65's subject and this part's bridge to Part XI: content in Shona and Ndebele is poorly served by tools trained on the internet's English — transcription, search, and recommendation underperform exactly where Kumba's audience lives. The practical frontier: speech and text models adapted to low-resource languages (transfer learning from related languages, SentencePiece tokenisation on Shona corpora), metadata generated in-language (the untitled archive is unsearchable in any language), and — the quiet craft — *evaluation sets built by hand* because no benchmark exists. The strategic lesson for every analyst: where the tooling is thin, the data you can build becomes the moat.

## 60.6 The Storytelling Bridge and the Shared Failure

Analytics in both industries becomes valuable when it becomes *story*: the broadcast graphic (xG rolling difference at minute 70), the commentary line, the schedule insight a producer can pitch. Chapter 74's structures apply verbatim: one message, evidence, the decision. And both industries share the terminal failure mode — **Goodhart**: the player who stops shooting from anywhere because low-xG shots dent the dashboard; the newsroom that chases clicks into trivia. The practitioner's guard is the paired metric (Chapter 45): every performance metric travels with its health companion — xG with unpredictability, clicks with subscriber retention — and the pair is reviewed together, or the metric eventually ruins the thing it measured.

> **Teaching Tip — Code your own match:** give students a raw match event file (20 minutes of an amateur match, coded from video) and have them compute xG, then explain it to a panel playing a sceptical coach, a chairman, and a journalist. The three explanations must differ — the coach wants tactics, the chairman wants money, the journalist wants a sentence — and the exercise teaches the last mile of this whole part: the same analysis, told three ways, or it was never done.

## Key Takeaways

- Sport and media both measure attention; both fail by measuring the easy proxy.
- xG is a small, defensible model with big honest uses — chance creation versus finishing luck — and it is a scouting tool, not a tactic.
- Recruitment value is contribution per wage against the honest replacement; availability is the quiet signing.
- Reach is not attention, attention is not revenue: decay curves, churn curves, and the attention per content dollar ledger are the media desk.
- Where tooling is thin — low-resource languages — the data you build is the moat.
- Pair every metric with its health companion, or Goodhart ruins the game and the newsroom alike.

## Practice Lab

1. Fit the minimal xG model on the shot data (Appendix F generator); report each striker's goals minus xG and write the wage-negotiation paragraph that regression-to-the-mean deserves.
2. Build the recruitment ledger: contribution per 90, availability-weighted, per wage dollar — against the whole league and against age-mates; note where the two comparisons disagree and which you trust.
3. Fit the injury hazard model on training loads and congestion; produce next month's rotation plan and its expected available minutes.
4. Build the content decay curves by format and language; write the commissioning memo — what to renew, what to retire, what to schedule at 18:30.
5. The churn layer: retention curves for subscribers with and without each flagship programme in their history; label the correlation honestly and design the staggered test that would settle it.
6. Code 20 minutes of a match (any match, your own events file) and produce the three explanations: coach, chairman, journalist.

## Further Reading

- *The Numbers Game* — Anderson and Sally (football analytics' best entry point)
- *Soccernomics* — Kuper and Szymanski (recruitment economics)
- Chapter 63 (survival for injuries), Chapter 65 (low-resource NLP — Kumba's deep end), Chapter 74 (the three-way storytelling)
