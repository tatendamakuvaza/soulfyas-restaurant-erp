# Appendix E: Datasets and Resources

*Practice data, public datasets, and the reading list behind the course*

> "Data is the course's tuition: every dataset below is chosen because it teaches something specific."

## How to Use This Appendix

Every chapter's Practice Lab assumes data. Three sources cover the whole course: **Appendix F's Soulfya's generator** (fabricates the running case's entire universe with planted patterns), the public datasets listed here, and your own organisation's extracts (used under Chapter 42's governance and Chapter 68's privacy floor). Work the labs in that order: generated data first (you know what should be found), public data second (you practise finding it), real data last (nothing teaches governance like real data).

When you download a public dataset, practise the Part II discipline from the first minute: write the data card (source, licence, grain, known gaps), load it through your validation gates, and only then begin analysis. The habit is the point — a dataset you have not profiled is a stranger you are about to marry.

## Core Public Datasets, by Part

| Dataset | Where | Use it for | Part |
|---|---|---|---|
| Soulfya's generated suite | Appendix F script | Every running case lab | I–XII |
| Titanic passenger list | Public (Kaggle, many mirrors) | First classification, missing data, leakage-safe practice | V |
| Ames / Boston housing | Public (scikit-learn, Kaggle) | Regression, feature engineering, honest evaluation | III, V |
| NYC taxi trips | NYC Open Data | Big-ish data, DuckDB/Spark practice, fares and geography | VII |
| Bikeshare trips (Capital Bikeshare or local) | Open data portals | Time series, seasonality, forecasting leagues | III, V |
| Online Retail II (UCI) | UCI ML Repository | Market basket, RFM, CLV — the Part X retail labs | IV, X |
| Telco customer churn | Public (IBM sample, Kaggle mirrors) | Churn baselines, calibration, uplift practice | V, X |
| Bank marketing (UCI) | UCI ML Repository | Uplift and campaign response, imbalanced targets | V, X |
| Olist Brazilian e-commerce | Kaggle | Multi-table joins, star schema, delivery ETAs | II, VII, X |
| Superstore sample | Tableau Public | Dashboard drills, metric trees | IV |
| Gapminder / World Bank indicators | gapminder.org, data.worldbank.org | Trend craft, small multiples, development analytics | III, IV, X |
| DHS / MICS survey data (aggregated) | dhsprogram.com, unicef.org/mics | Survey weights, stratified estimation | III, X |
| CRAN / UCI time series | UCI, Monash TS archive | Forecasting league tables | V |
| Medical cost / diabetes readmission (UCI) | UCI ML Repository | Clinical risk, calibration | X |
| Palmer penguins | Public (allisonhorst) | First EDA, tidy graphics | I, IV |
| Open FIFA / football events | Public (Kaggle) | Expected goals, sport analytics | X |

Licence note: check each source's licence before publishing derived work; academic-teaching use is broadly permitted for most of the above, but "public" is not "yours to redistribute" — the data card records the licence with everything else.

## Tools (Free), by Purpose

- **Python stack**: pandas, scikit-learn, statsmodels, matplotlib, seaborn, statsforecast or sktime for leagues; DuckDB for analytical SQL on files.
- **Big data practice**: DuckDB first (single-node is the honest default, Chapter 37); Spark locally via `pyspark` when the decision test says so; Dask rarely and deliberately.
- **Dashboards**: Power BI Desktop (free), or Plotly Dash / Streamlit (Chapter 49) for products.
- **Causal inference**: `statsmodels`, `causalimpact`, `dowhy`, `econml` (Part XI's frontier reading).
- **Survey analysis**: Stata or R with `survey`; Python's `statsmodels` with weights for the same discipline.
- **Geospatial**: `geopandas`, `libpysal` (Moran's I and friends, Chapter 62).
- **Survival**: `lifelines` (Chapter 63).
- **Experimentation**: `scipy.stats`, `statsmodels` sequential tests, and Chapter 67's simulation notebooks.
- **Text**: `sentence-transformers`, `sentencepiece` (Chapter 65's low-resource work).

## Domain Playbook Addendum (Part X)

Each playbook chapter pairs with the datasets above and one domain-specific practice source. The pattern: run the chapter's Practice Lab twice — once on the Soulfya's-generated analogue (where Appendix F plants the answers), once on the public source (where the world decides).

- **Retail (Ch. 51)** — Online Retail II for basket and RFM; Olist for the multi-table version; the dead-stock ledger lab runs on Appendix F's inventory snapshot.
- **Marketing (Ch. 52)** — Telco churn and Bank marketing for the uplift and cohort labs; any app-store or SaaS sample for payback-week practice.
- **Financial services (Ch. 53)** — The UCI credit-approval style samples and Give Me Some Credit (Kaggle) for scorecard practice; generate fraud with Appendix F's planted-adversary mode.
- **Healthcare (Ch. 54)** — Diabetes 130-US readmission (UCI) is the canonical readmission lab; any DHS/MICS extract for the survey-weight discipline.
- **Agriculture (Ch. 55)** — FAOSTAT for production series; CHIRPS rainfall (public) and MODIS NDVI for the layered forecast; Sable Fields comes from Appendix F.
- **Energy (Ch. 56)** — UMass/ISO-NE or ENTSO-E public load data for the day-ahead forecast league; smart-meter samples (UK-DALE, Pecan Street) for interval analytics.
- **Government (Ch. 57)** — Your own city's open-data portal (Harare's and most capitals publish something); World Bank indicators for the evaluation labs; Case 4's tariff data is generated.
- **Manufacturing (Ch. 58)** — The SECOM dataset (UCI) for SPC-style quality; Appendix F's line counters for OEE and the maintenance hazard.
- **Transport (Ch. 59)** — NYC taxi for routing-adjacent ETA practice; any GTFS feed for schedule reality; Kunaka's telematics is generated (Case 3's numbers).
- **Media and sport (Ch. 60)** — Public football event data (Kaggle's European matches) for xG; any podcast/streaming sample for decay curves; Kumba's corpora are built, not downloaded (Chapter 65).

## Frontier and Practitioner Resources (Parts XI–XII)

- **Causal inference (Ch. 61)** — Scott Cunningham's *Causal Inference: The Mixtape* (free online); the World Bank's DiD resources; `causalimpact` documentation.
- **Geospatial (Ch. 62)** — `geopandas` gallery; the Geographic Data Science textbook (free); libpysal's spatial-statistics tutorials.
- **Survival and forecasting depth (Ch. 63–64)** — `lifelines` documentation (an excellent tutorial in itself); FPP3 (*Forecasting: Principles and Practice*, free online) for hierarchical methods; `sktime` for the leagues.
- **Low-resource NLP (Ch. 65)** — Masakhane's published work (the reference for African-language NLP); `sentencepiece` papers; Hugging Face's course.
- **Simulation (Ch. 66–67)** — Julia/Python queueing tutorials; the Monte Carlo kitchen notebooks from Chapter 67; any discrete-event library's manual (SimPy) is a course in itself.
- **Experimentation (Ch. 67)** — Kohavi, Tang and Xu, *Trustworthy Online Controlled Experiments* — the practitioner's bible; CUPED references from Microsoft's published papers.
- **Privacy (Ch. 68)** — The Differential Privacy textbook (Dwork and Roth, free online); OpenDP's documentation.
- **Analytics engineering (Ch. 69)** — dbt's documentation and blog; Kimball's dimensional toolkit.
- **Staying current (Ch. 70)** — The newsletters and reading discipline of Chapter 70; Papers With Code for method tracking.
- **Delivery craft (Ch. 71–80)** — Appendix J's five cases as the role-play corpus; *The Flaw of Averages* (Savage) for the constraint of the week; the options-paper and value-ledger templates from Part XII, used on your own engagements.

## Building Your Own Practice Data

When no public dataset fits (often, for Parts VII–XII), generate it: the discipline is Appendix F's — write down every planted pattern before generating, so the analysis can be *scored against truth*, which no real dataset offers. A generated dataset with documented plants is a better teacher than a real dataset with unknown structure; the sequence is always generated → public → real, in that order, for every new skill.
