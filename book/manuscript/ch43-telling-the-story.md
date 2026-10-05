# Chapter 43: Telling the Story

*Part VI — Dashboards and Storytelling with Power BI*

> "The dashboard shows everything. The story says what matters. The craft is delivering both in one meeting."

### In this chapter you will learn

- The BI publishing path: Desktop file → service → shared, with scheduled refresh.
- The narrative layer: annotations, the summary page, and the guided path.
- Presenting to non-analysts: the five-minute walkthrough that works.
- The dashboard-vs-report decision, made consciously.
- Part VI's close: the full toolkit, assembled around one shop.

## 43.1 Publishing, the Honest Path

The last technical mile: getting the dashboard to its readers. In Power BI's world: **Publish** (Home → Publish, from Desktop) sends the `.pbix` to the **Power BI service** — Microsoft's cloud — where the report lives at a URL, viewable in a browser and (with the mobile app) on a phone; readers need licences (free viewers, in the common organisational setup). **Scheduled refresh** connects the service to the data source and refreshes on a timer — the Chapter 37 cron, managed by clicks; a **gateway** (a small local agent) is needed when the source is on-premises (Tariro's laptop CSVs, a company database behind the firewall).

For this book's scope — and many small-team real cases — the honest publishing ladder is simpler: (1) the `.pbix` file itself, shared (readers open it in Desktop, free — the *file* is the deliverable, version-controlled like any artefact); (2) export: Power BI can export pages/visuals to PDF or PowerPoint for the meeting pack — the dashboard's findings, frozen for the record; (3) the service, when an organisation is already licensed — which is your first job's likely path, and a day-one skill after this Part. (Chapter 61's free stack covers the no-licence alternatives: publishing the same star-schema to Metabase, or a scheduled HTML report from Part V's pipeline — the *architecture* of this Part transfers entire.)

## 43.2 The Narrative Layer

A dashboard shows everything; a reader needs to be *told* what matters. Three narrative devices, all built into the file, all turning the page from data into communication:

- **The summary page** — the *first* page of the report: three finding-phrased text boxes ("Revenue grew 31% over 18 months"; "Sundays are 28% below weekdays — a traffic problem (p < 0.001)"; "EcoCash share rising: 31% → 44%"), each beside its supporting visual in miniature, each with a page-navigation button to the full story. Chapter 13's one-page report, reborn as the dashboard's front door — and it satisfies the five-second rule at the *file* level, not just the page level.
- **Annotations on the chart** — the month-9 oil cliff, labelled on the line chart itself ("cooking-oil price rise +0.80"); the payday sawtooth, noted. Power BI: text boxes positioned precisely, or the "Smart narrative" visual (generated text you then *edit* — the machine drafts, you verify; always verify). The annotation is the finding-title rule from Chapter 11, placed at the exact coordinate where the reader will wonder.
- **The guided path** — buttons that navigate ("See the oil story →", "Drill to items →") so a first-time reader is walked through the argument you would walk them through in person. Bookmarks (Chapter 41) plus buttons equal a *tour* of the data: the storytelling of a presentation, encoded in the artefact.

## 43.3 The Five-Minute Walkthrough

The meeting — bank manager, boss, client — where you present the dashboard. The format that works (it is Chapter 13's report structure, spoken):

1. **The headline, first** (30 seconds): "Trade is up 31% over eighteen months, with one real problem — cooking oil since the price rise — and one opportunity, Sundays. I'll show you all three in five minutes." The audience now has the story's shape; everything after is evidence they have been promised.
2. **The movement** (60s): the revenue line with LY comparison; point at the dip *when you reach it*, name its cause, move on. Never narrate every point — you are the analyst, not the chart's tour guide; you pre-read the chart (Chapter 11) and deliver its three findings.
3. **The stories** (2 minutes): Sunday (the verdict tile — and the *caveat in the sentence*: "…which is a traffic problem, not basket size — that's a tested finding, not a hunch"), oil (the cliff, the quantity story, the pending shelf trial from Chapter 28), loyalty (the share trend, with the self-selection caveat attached as naturally as the number).
4. **The interaction, once** (60s): hand over the mouse or click the slicer yourself — "here's March, here's EcoCash only" — showing the audience the dashboard answers *their* follow-ups without you. That moment converts the dashboard from your presentation into their tool.
5. **The ask** (30s): what should happen next — the recommendations, measurable, with owners and dates (the shelf trial; the four-Sunday promotion test; the top-5 order increase). End on a decision, not on "any questions?" (there will be questions; the ask survives them).

Two presenting rules that carry the whole craft: **never show a number without its comparison or cause** (the naked number is the amateur's tell), and **say the caveat before the listener finds it** (Chapter 2's "says who?", delivered proactively — the trust dividend compounds across every future meeting).

## 43.4 Dashboard or Report?

The conscious decision, made on every deliverable for the rest of your career:

| Reach for a **dashboard** when... | Reach for a **report** (PDF/notebook/deck) when... |
|---|---|
| The question recurs ("how are we doing?") | The question is deep ("why did this happen?") |
| Readers need different slices | Readers need one argument, end to end |
| Data refreshes on a schedule | The analysis is a snapshot in time |
| The audience is many and varied | The audience is specific and known |
| Speed of answer matters most | Rigor and narrative matter most |

Tariro's shop needs both, and has both: the Trade Overview dashboard for the recurring pulse, Project 3's automated monthly report for the argued findings. The professional failure mode is format fundamentalism — the analyst who dashboards everything (deep findings crushed into tiles) or reports everything (recurring questions re-answered monthly by hand). The brief decides; the toolkit serves.

## 43.5 Part VI Closes: the Toolkit Assembled

Stand back from the shop. One data story now flows through five tools, each doing its natural job: the **spreadsheet** (Part II) for first contact and one-off questions; the **database** (Part III) as the governed source of truth; **statistics** (Part IV) as the meaning machinery; **Python** (Part V) as the automated engine; and the **dashboard** (Part VI) as the always-on window for readers. The same shop, the same numbers, the same honesty rules — reconciled at every hand-off, caveated at every claim, tested where testing was owed. That is the working stack of a data analyst, complete, and *you built all five layers on one real dataset* — which is precisely the portfolio story Part VII now turns into a career asset.

> **From Your Toolkit — communication is the last mile:** every artefact of Parts II–VI exists to be *read*: the report page, the chart's title, the dashboard's summary screen, the five-minute walkthrough. The pattern is one pattern — headline, evidence, caveat, ask — from Chapter 13's one-pager to this chapter's meeting. Master the pattern and the tools become interchangeable instruments behind it.

## Key Takeaways

- Publishing ladder: share the .pbix (free, version-controlled) → export PDF/PPT for the record → the service with scheduled refresh and gateway when licensed; the architecture transfers to free alternatives.
- The narrative layer ships in the file: summary page (findings as front door), chart annotations at the wondering-point, guided navigation.
- The five-minute walkthrough: headline → movement → stories (with caveats spoken first) → one interaction → the ask; never a naked number.
- Dashboard vs report is a conscious decision by question type, audience, refresh, and depth — both live in the professional stack.
- Part VI completes the five-tool stack around one dataset — the portfolio story Part VII monetises.

## Practice Lab

1. Build the summary page: three finding-phrased text boxes with mini-visuals and navigation buttons; reorder pages so it is first; run the five-second test at the *file* level (open, glance, close: what did you learn?).
2. The annotation pass: label the oil cliff, the payday rhythm, and the best week on the charts where they occur; add one Smart-narrative visual and *edit its text* until every sentence would survive your own skepticism audit.
3. The walkthrough, rehearsed: script your five minutes (headline, movement, stories, interaction, ask — timing pencilled in the margin); deliver it to a friend or your phone's camera; watch it back once; note the two fixes.
4. The export pack: export the dashboard pages to PDF and the summary findings to one slide; compare what survives the export (interactivity does not — does the static version still tell the story? fix what does not); file both in the portfolio folder.
5. The reflection page (portfolio feedstock): 200 words — "one dataset, five tools, what each was best at" — with the Trade Overview screenshot at the top. Chapter 49 will publish this page almost verbatim.

## Further Reading

- Chapters 44–49 (projects and the portfolio — the story becomes a career), *Storytelling with Data* (Knaflic) ch. 7–8
- Microsoft Learn: "Manage workspaces" — the service-side skills of this chapter, official form
