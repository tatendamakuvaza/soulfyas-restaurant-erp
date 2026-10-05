# Chapter 49: Your Portfolio

*Part VII — Real Projects and Your Portfolio*

> "Nobody hires you for what you know. They hire you for what you have *done* — and the portfolio is the proof you keep where they can see it."

### In this chapter you will learn

- GitHub from absolute zero: account, repository, commits — the analyst's minimum viable git.
- The three-project portfolio: what to include, what to cut, and how to order it.
- The README as shop window: writing the page that gets you the interview.
- The walkthrough: a guided tour a stranger can follow in ten minutes.
- Keeping it alive: the portfolio as a career habit, not a job-hunt artefact.

## 49.1 GitHub in One Hour

GitHub is where working analysts (and every hiring manager) look for evidence — a public shelf for your artefacts. The minimum-viable workflow, genuinely from zero:

1. **Account**: github.com → Sign up (free). Your username is professional-facing: a variant of your real name beats `dataninja420`.
2. **Repository**: New repository → name it `data-analytics-portfolio` → Public → Add a README → Create. A *repository* is a project folder that tracks every change.
3. **Files**: the **+ → Upload files** page handles your first uploads (the web interface is a fine start; the command line arrives when a job demands it). Upload a project folder's contents, **Commit changes** (the commit message: "Project 4: customer churn analysis" — a labelled save point; the habit Chapter 20 taught, now on the world's shelf).
4. **Edit in the browser**: the pencil icon on any file — the README you will rewrite in section 49.3 is edited exactly like a document.

That is the whole requirement: an account, a repository, files, commits. (Branches, pull requests, `git` itself — the professional's tools — arrive in your first job or in an evening of learning from GitHub's own tutorials; the *portfolio* needs none of them to start. If you already know git, use it properly — commit per project, meaningful messages; if you do not, the web path is honest and sufficient.)

Two house rules: **every project folder gets its own README** (what, why, how to run, the finding, the limits — the header-block habit of Chapter 20, grown to a page); and **data goes in with care** — small generated datasets in-repo (labelled synthetic), large files linked rather than committed, never anything you have no right to publish (Chapter 44's licences; Chapter 59's ethics).

## 49.2 The Three-Project Portfolio

Six projects exist in your ledger; the *portfolio* shows three to four. Selection is the craft — a portfolio is an argument, not an archive:

- **Include**: (1) the **wild-card public-data project** (Chapter 44's queue — real data, real mess, no planted answers: your proof you work outside the book); (2) **one deep analysis project** with statistics (Project 4 churn, or the wild-card if it runs tests) — proof you conclude, not just describe; (3) **one automation or BI project** (Project 3's pipeline or Project 6's dashboard) — proof you *ship tools*, the rarest skill at junior level. A fourth slot (the survey, if you fielded it for real — human data + ethics discipline) if it is genuinely yours.
- **Cut**: near-duplicates (Projects 1–2 are chapters of the same story as 3 — fold their findings into 3's README); unfinished work (a dead notebook reads as unfinished work, because it is); anything you cannot defend line-by-line in an interview — the portfolio is an *invitation to be questioned*, and you will be (Chapter 52).
- **Order**: lead with the wild card (real data) or the project with the strongest *finding* — the first project a recruiter opens gets the only unmixed attention you will receive.

The book's projects 3, 4, 6 + your wild card is the recommended four — tools covered (Python ×3, statistics, BI), every finding real-or-labelled, each with the full artefact trail (code, exhibit, report, note).

## 49.3 The README as Shop Window

The repository's front page is written for a stranger with 90 seconds: a hiring manager, skimming, phone in hand. The structure that earns the second minute:

```markdown
# Your Name — Data Analytics Portfolio

One paragraph: who you are, what you do (Excel, SQL, Python,
statistics, Power BI), and the one-line story of the portfolio.
*(Links: LinkedIn, email, CV.)*

## Projects

### 1. [Wild-card title] — one sentence, the finding with its number
Real data from [source]. Question, method, finding, the
recommendation it produced. **Stack: Python, pandas, scipy.**
→ notebook · report · dashboard (links)

### 2. Customer churn — founding cohort drifting, 60 at-risk named
... (same shape, each 3-4 lines)

## What I practise
The working stack, one line each: the reconciliation habit,
testing over vibes, caveats attached to claims. (Yes — say the
*habits*. Everyone lists tools; habits are what you actually sell.)

## Data & honesty
All synthetic datasets are labelled as generated (generator
included). Public data cited to source. No data I have no right
to publish.
```

The craft rules, all of them this book's rules in miniature: **findings with numbers in the project blurbs** ("founding cohort churning 2× fast", not "explored churn"); **links that work** (dead links are the most common portfolio failure — click every one, monthly); **the honesty section present** (it reads as senior; most candidates have none); and *spell your own name right* — the portfolio, CV, and LinkedIn must match exactly (this book's author has seen a CV misspelling its own candidate's name; so has every hiring manager).

## 49.4 The Walkthrough

Some interviews (and most serious recruiters) will open the portfolio *with you watching*. Prepare the ten-minute guided tour, three projects, three minutes each — the Chapter 43 five-minute walkthrough's sibling, applied to your own shelf:

1. **The map** (1 min): the README, top to bottom — who, the four projects, the honesty section. "Everything here is reproducible from the repo."
2. **One deep project** (3–4 min): the wild card or churn — question first (the anatomy's law, spoken), the one exhibit that carries the finding, the statistical verdict with its caveat, the recommendation. Close on the *limits* — voluntarily, before asked; it is your strongest move.
3. **One tool project** (2–3 min): the pipeline or the dashboard — what it automates (the before/after timing), the checks that guard it, a live click or re-run if the room allows.
4. **The invitation** (1 min): "Happy to go deeper on any of these — the code, the decisions, or what I'd do differently." Then *stop talking*. The interview takes the invitation.

Rehearse it once aloud with a timer (the Chapter 43 lab method); ten minutes is the ceiling, and stopping on time is itself evidence of the communication craft Part VI built.

## 49.5 Keeping It Alive

The portfolio's final rule: it is a *living shelf*, not a job-hunt artefact — the Chapter 44 dataset habit feeds it (one dataset a month; the best become projects), each new project gets its note-and-README on shipping day, and the "What I practise" section evolves as you do (in your first job, it grows employer-relevant lines: their warehouse, their domain). A repository with a commit last month is read as *an analyst at work*; one with a burst of activity two years ago is read as *a course certificate with extra steps*. You are the first — the compounding career of Chapter 62 begins on this shelf.

> **From Your Toolkit — the shelf is the career:** Part VIII is about to send you into the market, and every move there — the CV (Ch. 51), the interviews (52–53), the freelancing (55) — links back here: the CV's projects section is three lines pointing at this repository; the technical tests are passed with the skills these projects evidence; the case interviews are *your walkthrough, retold*. The portfolio is not the last chapter of learning; it is the first chapter of working.

## Key Takeaways

- GitHub minimum: account, public repository, files, commits, per-project READMEs — web interface is an honest start; git proper can wait for the job.
- Show three or four projects, chosen as an argument: real data (wild card), deep statistics, a shipped tool (automation/BI); cut duplicates, dead work, and anything you cannot defend.
- The README is written for a 90-second stranger: findings with numbers, working links, the habits section, the honesty section.
- The ten-minute walkthrough: map → one deep project (limits stated first-hand) → one tool project → the invitation; rehearse with a timer, stop on time.
- Keep it alive monthly — a living shelf reads as an analyst at work; the dataset habit feeds it forever.

## Practice Lab

1. The hour: create the GitHub account and `data-analytics-portfolio`; upload Projects 3, 4, and 6 with their folders; write per-project READMEs (what/why/how-to-run/finding/limits) — commit messages meaningful.
2. The front page: write the main README in section 49.3's shape; make your four project links; verify every link by clicking; align name spelling across CV, LinkedIn, and GitHub.
3. The wild card, begun (if not yet built): take Chapter 44's top-ranked local question; run the full anatomy (Ch. 45) at portfolio depth — question log, first hour, liturgy, analysis, one-page report; ship it as project #1 with its note.
4. The walkthrough, rehearsed: ten minutes, timer, camera (phone); watch it back; note the two worst moments (usually: mumbling the finding, or over-running); re-rehearse once; book it done.
5. The liveness system: set a monthly reminder (first Friday); the agenda is already written — one dataset (Ch. 44), link-check the shelf, update the notes; write the agenda into the reminder so the habit survives enthusiasm's departure.

## Further Reading

- Part VIII (the hunt: CV, interviews, offers), Chapter 61 (the free stack that keeps the shelf fed)
- GitHub's "Hello World" guide — 10 minutes, the git concepts in miniature
