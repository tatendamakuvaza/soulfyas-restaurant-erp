# Chapter 69: Analytics Engineering — The Warehouse as a Product

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "Your warehouse has users, a roadmap, and bugs; only one of those is on the roadmap."

### In this chapter you will learn

- The analytics engineer: the role between the data engineer and the analyst.
- The layer cake: staging, intermediate, marts — and why the order is load-bearing.
- Tests as gates: schema tests, data tests, and the contract with downstream users.
- The workflow: git, pull requests, environments, and CI for queries.
- Naming, grain, and documentation as product decisions.
- Failure modes: the tribal-knowledge warehouse and the notebook that became production.

## 69.1 The Missing Role

Somewhere between the data engineer (pipes, platforms, uptime) and the analyst (questions, models, decisions) a gap opened, and into it fell everything neither owned: the metric that differs by outlet, the table nobody remembers building, the column named `final_v2_REAL`. The **analytics engineer** is the role that closes the gap: the person who treats the transformation layer — raw data to analysis-ready tables — as a **software product with users**, where the users are analysts, dashboards, and every executive who quotes a number.

Soulfya's data platform by Part VIII had three dashboards quoting three different "revenues" — the fan-out bug of Chapter 6, fossilised into architecture. The analytics engineering discipline is the permanent fix: one definition, versioned, tested, documented, owned.

## 69.2 The Layer Cake

The discipline's shape, in layers, each with one job:

- **Staging** (raw → cleaned): rename, type, deduplicate, apply the data card. One staging model per source table; no business logic; never bypassed.
- **Intermediate** (cleaned → shaped): joins, business logic, the fiddly middle where fan-out lives and dies. Consumed by marts, never by dashboards.
- **Marts** (shaped → consumed): the star schemas and wide tables of Chapter 8, named for their users — `finance_*`, `marketing_*`, `ops_*` — each with a stated grain and an owner.

The order is load-bearing: every layer consumes only the layer beneath, and every exception (the "quick" dashboard reading raw tables) is the technical debt that Chapter 43's incidents are made of.

```sql
-- models/marts/ops/outlet_daily.sql  (a mart model, dbt-style)
select o.outlet_id, d.date_day,
       sum(f.net_amount)          as revenue,
       count(distinct f.order_id) as orders,
       sum(f.net_amount) / nullif(count(distinct f.order_id), 0) as avg_basket
from {{ ref('stg_orders') }} f
join {{ ref('stg_outlets') }} o using (outlet_id)
join {{ ref('stg_dates') }}  d using (date_day)
group by 1, 2
```

**From Your Toolkit — SQL:** this chapter is SQL's homecoming. The language you learned first becomes the *product language*: versioned in git, reviewed in pull requests, tested in CI, and documented in the warehouse itself. Everything Part II taught as craft becomes, here, infrastructure.

## 69.3 Tests as Gates

Two families, both code:

- **Schema tests** — the shape of the data: not null, unique, accepted values, referential integrity (every order's outlet exists). Cheap, universal, and they catch the source system's 3 a.m. schema change before the dashboards do.
- **Data tests** — the meaning of the data: revenue non-negative, order counts within 3x of the 28-day median, no outlet-day rows for closed outlets. These encode institutional knowledge that used to live in one analyst's head, and fail loudly when the world changes.

```yaml
models:
  - name: outlet_daily
    columns:
      - name: outlet_id
        tests: [not_null, relationships: {to: ref('stg_outlets'), field: outlet_id}]
      - name: date_day
        tests: [not_null]
    tests:
      - unique_combination: {columns: [outlet_id, date_day]}
      - expression_is_true: {expression: "revenue >= 0"}
```

The discipline that makes tests real: **failures page someone** (Chapter 43's monitoring, applied to tables), and the failure's fix is a pull request, not a silent patch.

## 69.4 Contracts and Docs

The mart's contract with its users, stated in the model file: grain (one row per outlet-day), freshness (by 06:00), owner (a name, not a team email), and the metric definitions (revenue = net of refunds, including delivery, in USD). The docs generate the catalogue: the page an analyst reads *before* the query, and the page Chapter 76's audit starts from. A metric without a definition page is a rumour with a column name.

## 69.5 The Workflow

- **Git for everything** — branches, pull requests, and review for transformation code; the query that feeds the board is production software and lives like it.
- **Environments** — dev (your sandbox), staging (the copy), prod (the one the dashboards read); the pipeline promotes, people do not hotfix.
- **CI on every PR** — build the changed models, run the tests, check the docs; a broken definition dies in review, not on a Monday dashboard.
- **Modularity over cleverness** — small models, `ref()`-linked, each testable; the 400-line CTE-monolith is the notebook that became production, wearing a nicer shirt.

## 69.6 The Craft Decisions

Two conventions carry most of the value. **Naming is documentation**: `fct_`/`dim_` prefixes (facts and dimensions, Chapter 8's star schema made visible), past-tense staging (`stg_orders`, cleaned), no `_v2`, no `_final` — version control means never renaming to `final_REAL`. **Grain is stated, not discovered**: every model's file begins with its grain, one sentence, and the reviewer enforces it — because the fan-out bug of Chapter 6 was always a grain statement somebody skipped.

## 69.7 Failure Modes

- **The tribal-knowledge warehouse** — 4,000 tables, 12 documented, the map in three analysts' heads; the audit question "why does this number differ?" takes a week and a séance.
- **The notebook that became production** — the analysis script someone scheduled in cron, untested, undocumented, now load-bearing; the migration path is the layer cake, one notebook at a time.
- **Test theatre** — hundreds of not-nulls, zero meaning-tests; coverage counted, confidence unearned.
- **The undocumented metric** — `revenue` in two marts, one gross, one net, both believed; the contract and the catalogue are the cure.

> **Teaching Tip — The broken pipeline drill:** hand students a deliberately broken warehouse (a source column renamed, a fan-out reintroduced, a silent null flood) and a user complaint ("the board number is wrong"). The hunt — tests failing, lineage graph, the PR that fixes it — teaches the entire chapter as a lived incident, and the retrospective writes the runbook for them.

## Key Takeaways

- The analytics engineer treats transformation as a product: layers, tests, contracts, docs, and users who are analysts.
- The layer cake — staging, intermediate, marts — with each layer consuming only the one beneath; exceptions are debt.
- Tests are code that pages: schema for shape, data for meaning, and the fix is a pull request.
- Naming is documentation, grain is stated in the file, and a metric without a definition page is a rumour.
- Git, PRs, environments, CI — the query behind the board deck is production software and lives like it.

## Practice Lab

1. Draw Soulfya's current warehouse as the layer cake; find the three violations (dashboards reading raw, marts reading marts) and write the migration plan, one model at a time.
2. Convert the outlet-daily query into a tested model: five schema tests, three data tests, and the grain statement at the top of the file.
3. Write the contract page for the two "revenue" metrics that caused the three-dashboards problem; define each, name the owner, and mark the deprecated one.
4. Set up CI for the transformation repo: on every PR, build changed models, run tests, and fail on any error; document the workflow for a new analyst.
5. The naming audit: list every `_final`, `_v2`, and `tmp_` table in a warehouse you can access; write the renaming PR and its communication plan.
6. The broken pipeline drill: run it on a classmate's build; write the runbook you wish you had when the board number was wrong.

## Further Reading

- dbt's documentation and blog (the discipline's home turf)
- *The Data Warehouse Toolkit* — Kimball and Ross (the dimensional foundations)
- Chapter 8 (star schemas — this chapter is its infrastructure), Chapter 11 (validation — here made permanent), Chapter 43 (the monitoring that pages on test failure)
