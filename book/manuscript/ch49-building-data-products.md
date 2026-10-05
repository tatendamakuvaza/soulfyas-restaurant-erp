# Chapter 49: Building Data Products — Dashboards, Apps, and APIs

*Part IX — The Extended Curriculum: Special Topics and the Craft of Teaching*

> "The last mile of analytics is a product, not a PDF."

### In this chapter you will learn

- The product ladder: report → dashboard → app → API → automated decision service — and when to climb each rung.
- A working Streamlit app in one file: the churn explorer.
- A production-shape scoring API with FastAPI.
- The product crafts: versioning, logging, documentation, authentication.
- Deployment realities: containers, CI, and what to run where.
- When *not* to build a product — the discipline of the last rung.

## 49.1 The Product Ladder

Analysis creates understanding; a product *delivers* it, repeatedly, to someone who was not in the room. Each rung of the ladder adds interactivity, engineering, and maintenance — climb only as far as the decision demands:

| Rung | Form | Interaction | Maintenance | Soulfya's example |
|---|---|---|---|---|
| 1 | Report / memo | None | None | Monthly performance write-up |
| 2 | Dashboard (Chapter 18–19) | Filter and drill | Refresh, model upkeep | "Are we healthy?" page |
| 3 | Notebook-as-app | Parameter play | Low | Scenario planner for the founder |
| 4 | Web app | Full interaction | Real | Churn campaign workbench |
| 5 | API | Machine-to-machine | Real + latency SLAs | Live delivery-ETA scoring |
| 6 | Automated decision service | Acts on its own | Everything in Part VIII's MLOps | Dynamic prep recommendations |

The professional error is skipping rungs: teams build a web app (rung 4) for an audience that needed a well-written memo (rung 1), or an API (rung 5) for a question asked quarterly. The other professional error is *camping* at rung 1 forever while a weekly, repeated, human-heavy ritual begs for rung 2.

## 49.2 Rung 3–4 in One File: Streamlit

Streamlit turns a Python script into a web app: the script reruns top-to-bottom on every interaction, widgets become function calls, and the whole framework fits in a morning. The churn campaign workbench:

```python
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(page_title="Churn Explorer", layout="wide")
st.title("Soul Circle Churn Explorer")

@st.cache_data
def load_scores():
    scores = pd.read_csv("member_scores.csv", parse_dates=["score_date"])
    scores["segment"] = scores["segment"].fillna("unknown")
    return scores

@st.cache_resource
def load_model():
    return joblib.load("churn_pipeline.joblib")

scores = load_scores()
model  = load_model()

with st.sidebar:
    outlets = st.multiselect("Outlets", sorted(scores["outlet_id"].unique()))
    min_risk = st.slider("Minimum risk score", 0.0, 1.0, 0.5)
    top_n = st.number_input("Campaign size", 50, 2000, 200)
    run = st.button("Build campaign")

view = scores[scores["risk"] >= min_risk]
if outlets:
    view = view[view["outlet_id"].isin(outlets)]

col1, col2, col3 = st.columns(3)
col1.metric("Members above threshold", f"{len(view):,}")
col2.metric("Churners in view (last 60d)", f"{view['churned'].sum():,}")
col3.metric("Est. value of campaign", f"${view.nlargest(top_n, 'risk')['expected_value'].sum():,.0f}")

st.scatter_chart(view, x="days_since_visit", y="risk", color="segment", height=380)

if run:
    campaign = view.nlargest(top_n, "risk")
    campaign.to_csv("this_weeks_campaign.csv", index=False)
    st.success(f"Campaign built: {len(campaign)} members, "
               f"{campaign['member_id'].nunique()} unique, CSV ready for download.")
    st.data_editor(campaign[["member_id", "risk", "days_since_visit", "segment"]])
```

Fifteen minutes of work produces what a month of email round-trips never did: the retention team explores risk thresholds themselves, sees the expected value move, and pulls the campaign list when they are satisfied. The `@st.cache_data` / `@st.cache_resource` decorators are the entire performance strategy — data loads once, the model loads once.

The honest limits: Streamlit apps are internal tools. Authentication is basic, multi-user state is awkward, and anything customer-facing eventually wants a real frontend — by which point the app has already paid for itself as the prototype that proved the need.

## 49.3 Rung 5: A Scoring API with FastAPI

When another system needs your model — the delivery app's backend, the POS, a partner — you serve it as an API. FastAPI is the modern standard: type hints become validation, and documentation is generated automatically.

```python
from fastapi import FastAPI
from pydantic import BaseModel, Field
import joblib, pandas as pd

app = FastAPI(title="Soulfyas Scoring API", version="1.2.0")
model = joblib.load("churn_pipeline.joblib")

class MemberFeatures(BaseModel):
    days_since_visit: float = Field(..., ge=0, le=730)
    visits_90d: int = Field(..., ge=0)
    avg_basket: float = Field(..., ge=0)
    delivery_share: float = Field(..., ge=0, le=1)
    complaint_filed: int = Field(..., ge=0, le=1)

class ChurnScore(BaseModel):
    risk: float
    model_version: str

@app.post("/v1/churn", response_model=ChurnScore)
def score(m: MemberFeatures):
    X = pd.DataFrame([m.model_dump()])
    risk = float(model.predict_proba(X)[0, 1])
    return ChurnScore(risk=risk, model_version="1.2.0")

# run:  uvicorn scoring_api:app --host 0.0.0.0 --port 8000
```

Read what the fifteen lines include: input *validation* (impossible values rejected with a 422 before they reach the model), a *versioned route* (`/v1/` — so v2 can ship beside v1), and the model version in every response — Chapter 43's traceability requirements, implemented as a side effect of good design. Swagger documentation appears at `/docs` for free. In production, add authentication (an API key header at minimum), structured logging of inputs and scores (the drift dataset of Chapter 43), and latency monitoring.

## 49.4 Product Craft: The Four Habits

1. **Version everything together** — code (git), model artefact (registry), API route (`/v1/`), and the version echoed in responses. "Which model produced this score?" must be answerable from the score itself.
2. **Log like you will be debugged** — every request (timestamp, features, score, latency, caller), because your monitoring data *is* your log, and Chapter 43's drift detection will read exactly this table.
3. **Document the contract** — the API's generated docs plus one human page: what the score means, its calibration, its known weaknesses (Chapter 29's model card, linked from the product).
4. **Degrade gracefully** — a model failure should not take down the caller: fall back to a default score, a cached result, or an explicit "unavailable" that the caller is designed to handle. Products fail; *systems* degrade.

## 49.5 Deployment, Minimally

The container that runs the same everywhere (Chapter 43's one-sentence Docker):

```text
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY scoring_api.py churn_pipeline.joblib .
CMD ["uvicorn", "scoring_api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Where it runs is a Chapter 41 decision: a small VM, a container service, or a platform's managed endpoint — the artefact does not change. The CI habit from Chapter 43 applies verbatim: every push runs the model smoke test (fit on a fixed toy sample, score a fixed row, assert the score within tolerance) before anything deploys.

## 49.6 The Discipline of the Last Rung

The rung you choose is a maintenance contract. A memo costs nothing after Thursday; a dashboard costs a refresh schedule and a model; an API costs latency, uptime, and a rotation of on-call analysts. Before climbing, ask Chapter 2's question in product form: *how many people, how often, making which decision?* Soulfya's churn workbench served three people weekly — a Streamlit app, aggressively unglamorous, was the correct ceiling. The delivery-ETA scorer served thousands of app sessions daily — a containerised API earned itself. Both answers are right; the sin is not knowing which you are building.

> **Teaching Tip — Ship week:** make the course capstone literally a shipped artefact — a live URL (Streamlit sharing or any free host) or a running container — graded with a rubric of product habits: does it state its model version? Does it degrade gracefully? Would a stranger understand the front page in thirty seconds? Students who have *deployed something* interview differently: they have war stories about CORS, caching, and cold starts, and war stories are what "experience" means.

## Key Takeaways

- Products are rungs, not a summit: report → dashboard → app → API → decision service; climb to match the decision's frequency and audience, no further.
- Streamlit turns analysis into an interactive workbench in an afternoon — the highest value-per-line tool in this book for internal audiences.
- FastAPI gives validation, versioned routes, and generated documentation for free — and those defaults implement Chapter 43's traceability requirements.
- The four product habits: versioned-together artefacts, request logging (your drift dataset), documented contracts, graceful degradation.
- Deployment is a six-line container plus a CI smoke test; where it runs is a cloud economics decision.
- The last rung is a maintenance contract — size it to the audience, and let the boring tool win when the boring tool suffices.

## Practice Lab

1. Build the churn explorer on your Part V scores; add a segment filter and a "download campaign CSV" button; deploy it (Streamlit sharing or a container) and send the link to a non-analyst for a critique.
2. Wrap your trained pipeline in the FastAPI scorer; call it with curl; then send an invalid feature value and read the 422 — write two sentences on why this protected your model.
3. Add `/v2/churn` with a second model; route 10% of traffic to it via a simple flag; log which version scored each request; you have built a minimal champion–challenger.
4. Break it on purpose: corrupt the model file and restart; implement the graceful fallback (default score + warning header); document the behaviour in the API's human page.
5. Write the rung justification memo for three artefacts your organisation needs — one per rung 2, 3, and 5 — with audience, frequency, and maintenance cost for each.
6. The ship-week rubric: score your own capstone artefact against Section 49.4's four habits; fix the lowest score before calling any project done.

## Further Reading

- Streamlit and FastAPI official documentation (both free, both excellent)
- *Designing Machine Learning Systems* — Huyen, chapters 7–8 (serving and products)
- Chapter 43 for the monitoring this chapter's logs feed.
