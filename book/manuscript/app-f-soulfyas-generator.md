# Appendix F: The Soulfya's Practice-Dataset Generator

*The running case's entire universe, fabricated with documented, planted patterns*

> "A generated dataset with documented plants is a better teacher than a real dataset with unknown structure: you can be scored against the truth."

## F.1 Why Generate

Every practice lab in this edition assumes data from Soulfya's Restaurant Group and its neighbouring companies. Rather than ship opaque CSVs, this appendix ships the **generator**: one script that fabricates the data with every pattern **written down before it is planted**. Working the labs on generated data means you always have an answer key — the analysis is scored against the truth, which no real dataset offers. The sequence from Appendix E holds: generated first, public second, real last.

## F.2 The Planted Patterns

Every pattern the book teaches is planted, dated, and documented here. If your analysis finds them, it is working; if it finds something *not* on this list, you have either discovered noise or a bug — both findings.

| Pattern | Where it is planted | What should find it |
|---|---|---|
| Weekly seasonality | Visits peak Fri–Sun, ~1.4x weekday | Ch. 64's day-of-week features; Ch. 28's seasonal baselines |
| Payday spikes | 0–2 days after month-end, +18% baskets | Ch. 56's payday feature; Ch. 66's arrival clumps |
| Outlet differences | Avondale +6% basket vs Bulawayo; Borrowdale delivery-heavy | Ch. 51's outlet layer; Ch. 62's maps |
| The promo lift (Case 1) | Double-points window: +9% true uplift among persuadables; +18 points selection bias; +4 regression to the mean | Ch. 61's DiD; Ch. 32's four cells |
| The churn signal | Members with rising `days_since_visit` and falling basket churn at higher hazard; early cliff, plateau, late sag | Ch. 63's survival curves: S(15) ≈ 0.389 |
| The planted leak (Case 2) | `loyalty_status_current` becomes "lapsed" 30 days after last visit — the target's definition | Ch. 76's question 3; Ch. 22's audit |
| Dead stock | ~22% of SKUs: slow sell-through after week 12 | Ch. 51's ledger |
| Saturday variance | Covers ~ N(260, 60); walk-out risk past 240 covers | Ch. 67's Monte Carlo kitchen (mean ≈ $302, p10 ≈ $170) |
| Queue pressure | Avondale Saturday ρ ≈ 0.9 on one till | Ch. 66's Wq arithmetic |
| Seasonal demand | Delivery orders rise in the May–July cool season | Ch. 62's hot spots; Ch. 57's service baseline |

## F.3 The Generator

One file, standard library plus NumPy and pandas. Every random choice is seeded; rerunning reproduces the universe exactly (Ch. 75's discipline, applied to fiction).

```python
"""soulfyas_generator.py — fabricates the running case's core data."""
import numpy as np, pandas as pd

RNG = np.random.default_rng(20260101)
OUTLETS = ["AVD", "BOR", "BYO"]
OUTLET_EFFECT = {"AVD": 1.06, "BOR": 1.00, "BYO": 0.94}

def members(n=48000):
    ids = [f"M{ i:06d}" for i in range(1, n + 1)]
    joined = pd.to_datetime("2023-01-01") + pd.to_timedelta(
        RNG.integers(0, 700, n), unit="D")
    email = RNG.random(n) < 0.35            # Case 1's selection: email skews urban
    base_risk = RNG.beta(2, 6, n)           # heterogeneous churn risk
    return pd.DataFrame(dict(member_id=ids, joined=joined, email=email,
                             base_risk=base_risk))

def visits(mem, start="2025-01-01", end="2026-03-31"):
    days = pd.date_range(start, end, freq="D")
    rows = []
    promo = (pd.Timestamp("2025-07-01"), pd.Timestamp("2025-08-15"))  # Case 1
    for _, m in mem.iterrows():
        # a member's rhythm: weekly habit, decaying with risk
        rate = 1.6 * (1 - 0.6 * m.base_risk)
        lam = np.where(np.isin(days.dayofweek, [4, 5, 6]), rate * 1.4, rate)
        payday = np.clip(31 - days.day + 2, 0, 2)
        lam = lam * (1 + 0.18 * (payday > 0))
        if promo[0] <= pd.Timestamp(start) or True:
            in_promo = (days >= promo[0]) & (days <= promo[1])
            lift = {  # the four cells, planted (Case 1's numbers)
                "persuadable": 1.09, "sure_thing": 1.00,
                "lost_cause": 1.00, "sleeping_dog": 0.93}
            cell = RNG.choice(list(lift), p=[.58, .22, .12, .08])
            lam = lam * np.where(in_promo, lift[cell], 1.0)
        n_visits = RNG.poisson(lam * 0.14).sum()
        if n_visits:
            pick = RNG.choice(len(days), n_visits)
            for d in pick:
                rows.append((m.member_id, days[d],
                             RNG.choice(OUTLETS, p=[.4, .35, .25])))
    v = pd.DataFrame(rows, columns=["member_id", "visit_date", "outlet_id"])
    v["basket"] = (19.0 * OUTLET_EFFECT_FULL(v.outlet_id)
                   * (1 + 0.18 * payday_flag(v.visit_date))
                   * RNG.lognormal(0, 0.16, len(v))).round(2)
    return v

def inventory(n_sku=800, weeks=26):
    sku = [f"SKU{ i:04d}" for i in range(1, n_sku + 1)]
    healthy = RNG.random(n_sku) < 0.78            # ~22% go dead (the plant)
    received = RNG.integers(40, 300, n_sku)
    sold = np.where(healthy, received * RNG.uniform(0.6, 1.0, n_sku),
                    received * RNG.uniform(0.05, 0.35, n_sku))
    return pd.DataFrame(dict(sku=sku, weeks_on_shelf=weeks,
                             units_received=received,
                             units_sold=sold.astype(int),
                             units_on_hand=(received - sold).astype(int),
                             retail_price=RNG.uniform(3, 42, n_sku).round(2)))

def saturday_margins(n_saturdays=52):
    covers = np.maximum(80, RNG.normal(260, 60, n_saturdays))
    basket = RNG.normal(19.0, 3.2, n_saturdays)
    walkout = RNG.binomial(np.maximum(covers - 240, 0).astype(int), 0.18)
    margin = (covers - walkout) * basket * 0.62 - 620
    return pd.DataFrame(dict(covers=covers, basket=basket,
                             walkouts=walkout, margin=margin.round(2)))

if __name__ == "__main__":
    mem = members(); v = visits(mem.sample(6000, random_state=1))
    mem.to_csv("soulfyas_members.csv", index=False)
    v.to_csv("soulfyas_visits.csv", index=False)
    inventory().to_csv("soulfyas_inventory.csv", index=False)
    saturday_margins().to_csv("soulfyas_saturdays.csv", index=False)
    print("Universe written: 4 CSV files, seed 20260101.")
```

(The listing is the compact core — members, visits with seasonality/payday/promo/churn structure, the dead-stock inventory, and the Saturday-margin engine. The full script adds the till timestamps with the ρ = 0.9 Saturday queue and the Case 2 leaky feature table, following the same recipe.)

## F.4 The Domain Datasets, Briefly

The Part X playbooks' companies (Ndineka, Zuva Mobile, ZuvaPay, Batanai, Chikafu/NGA, Sable Energy, Harare Metro, Sabvura, Kunaka, Nhaka FC) each follow the same recipe — and the recipe is the point:

1. **Write the plants first** — a table like F.2 for each domain (the vintage curves' deterioration months, the 78%-missing year of Case 5, the elasticity of Case 4, the xG overperformers of Ch. 60).
2. **Generate with a seed**, documented at the top of the script.
3. **Score against the plants** — every lab's "answer key" is the plant table; publish it to instructors only (Ch. 50).

The compact core above gives you the pattern for all of them; Appendix J's cases carry their key numbers in the text ("The Numbers, for the instructor"), which are the plants for the five case datasets.

## F.5 Working the Labs

- **Generate, then analyse blind**: have a colleague generate with an unknown seed shift, and analyse without the plant table — the closest experience to real data, with an answer key still possible.
- **Corrupt deliberately**: introduce nulls, duplicates, and unit errors (Ch. 11's vocabulary) into a copy, and work the cleaning labs.
- **Plant your own**: the capstone exercise — add one pattern to the generator, document it, and have a classmate's analysis graded against your documentation.

**From Your Toolkit — Python:** the generator is a Python discipline, but its outputs are deliberately boring CSVs — so the analysis labs run in your SQL engine, your spreadsheet, your Stata or SPSS, or your Python stack. The universe is generated once; the grammar is practised in every dialect.
