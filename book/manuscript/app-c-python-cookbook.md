# Appendix C: Python Cookbook

*Appendices — The Cookbook*

> "Twenty-five pandas snippets — Part V compressed to a reference — plus two bonus sections this book promised: the full monthly-report pipeline, and the recipe that generated Tariro's data."

Conventions: `import pandas as pd` assumed; `sales` is a DataFrame with columns `date` (datetime), `item`, `category`, `payment_type`, `amount`, `customer_id`, `till`; `customers` has `customer_id`, `name`, `suburb`, `joined`, `loyalty_tier`.

## Loading and Inspecting

**1. The load, with the things you always forget**

```python
sales = pd.read_csv("sales.csv",
                    parse_dates=["date"],     # dates parsed at load
                    dtype={"customer_id": "string"})   # ids stay text
```

**2. The four instruments**

```python
sales.head()                              # eyeball
sales.info()                              # dtypes + nulls (the schema, free)
sales["amount"].describe()                # the five numbers plus mean/std
sales["payment_type"].value_counts()      # categorical frequencies
```

**3. The loading liturgy (the checks, as code)**

```python
assert sales["amount"].isna().sum() == 0, "null amounts -- stop"
assert customers["customer_id"].duplicated().sum() == 0, "dup keys -- stop"
orphans = (sales.loc[sales["customer_id"].notna()
    & ~sales["customer_id"].isin(customers["customer_id"])])
print(f"{len(sales):,} rows | total {sales['amount'].sum():,.2f} | "
      f"{len(orphans)} orphans")
```

## Selecting and Cleaning

**4. Boolean selection (WHERE)**

```python
big_ecocash = sales[(sales["amount"] >= 50)
                    & (sales["payment_type"] == "EcoCash")]   # parentheses + & |
june = sales[sales["date"].between("2025-06-01", "2025-06-30")]
```

**5. The string cleaners (Ch. 8 as methods)**

```python
sales["payment_type"] = (sales["payment_type"]
                         .str.strip().str.title())   # ghost blanks + case
sales["suburb"] = sales["suburb"].fillna("Unknown")
```

**6. New columns, vectorised**

```python
sales["month"] = sales["date"].dt.to_period("M")
sales["weekday"] = sales["date"].dt.day_name()
sales["is_weekend"] = sales["weekday"].isin(["Saturday", "Sunday"])
sales["is_whale"] = sales["amount"] > 21.50        # name the constant in real code
```

**7. Conditional labelling (the IF chain, ordered)**

```python
sales["basket_class"] = pd.cut(sales["amount"],
                               bins=[0, 5, 10, 21.5, np.inf],
                               labels=["tiny", "small", "big", "whale"])
```

**8. Deduplicate, keep latest**

```python
clean = (sales.sort_values("date")
              .drop_duplicates(subset=["sale_id"], keep="last"))
```

**9. Missingness triage (Ch. 60's liturgy)**

```python
sales.isna().mean()                              # share missing, per column
sales[sales["amount"].isna()]["weekday"].value_counts()  # does missingness correlate?
```

**10. Impute with a flag**

```python
sales["was_imputed"] = sales["amount"].isna()
sales["amount"] = sales["amount"].fillna(
    sales.groupby("category")["amount"].transform("median"))
```

## Grouping and Reshaping

**11. The pivot (totals of X by Y)**

```python
by_payment = sales.groupby("payment_type")["amount"].agg(["count", "sum", "mean"])
```

**12. Named aggregations (the AS aliases)**

```python
by_cat = sales.groupby("category").agg(
    revenue=("amount", "sum"),
    n_sales=("amount", "count"),
    avg_basket=("amount", "mean"))
```

**13. Two-way pivot (pivot_table)**

```python
mix = sales.pivot_table(index="month", columns="payment_type",
                        values="amount", aggfunc="sum", fill_value=0)
```

**14. Share of total (with the decimal point)**

```python
by_cat["pct_share"] = 100 * by_cat["revenue"] / by_cat["revenue"].sum()
```

**15. Top-N, overall and per group**

```python
top10 = sales.groupby("item")["amount"].sum().nlargest(10)
top3_per_cat = (sales.groupby(["category", "item"])["amount"].sum()
                     .reset_index()
                     .sort_values(["category", "amount"],
                                  ascending=[True, False])
                     .groupby("category").head(3))
```

**16. Percentiles and the fence**

```python
q1, q3 = sales["amount"].quantile([0.25, 0.75])
fence = q3 + 1.5 * (q3 - q1)
whales = sales[sales["amount"] > fence]
```

## Joining (with the defence)

**17. The merge (LEFT JOIN)**

```python
enriched = sales.merge(customers, on="customer_id", how="left")
```

**18. The fan-out defence (two lines, every merge)**

```python
print(len(sales), "->", len(enriched))                    # counts must match
assert sales["amount"].sum() == enriched["amount"].sum()  # totals reconcile
```

**19. The anti-join**

```python
left_only = sales.merge(customers, on="customer_id",
                        how="left", indicator=True)
orphans = left_only[left_only["_merge"] == "left_only"]
```

**20. Aggregate, then join (fan-out-proof enrichment)**

```python
member_value = (sales.dropna(subset=["customer_id"])
                .groupby("customer_id")
                .agg(lifetime=("amount", "sum"),
                     n_purchases=("amount", "count")))
customers = customers.merge(member_value, on="customer_id", how="left")
```

## Time Series

**21. Resample (the calendar groupby)**

```python
daily = sales.groupby("date")["amount"].sum().sort_index()
monthly = daily.resample("ME").sum()
```

**22. Rolling and cumulative (the frames of Ch. 19)**

```python
daily_7day = daily.rolling(7).mean()
running_total = sales.sort_values("date")["amount"].cumsum()
```

**23. LAG and month-over-month**

```python
monthly = monthly.to_frame("revenue")
monthly["mom_pct"] = monthly["revenue"].pct_change() * 100
monthly["yoy"] = monthly["revenue"] - monthly["revenue"].shift(12)
```

## Statistics and Charts

**24. The six instruments (Ch. 36, one block)**

```python
from scipy import stats

sun = daily[daily.index.day_name() == "Sunday"]
week = daily[daily.index.day_name() != "Sunday"]
t, p = stats.ttest_ind(sun, week, equal_var=False)      # Welch
r, p_r = stats.pearsonr(oil["price"], oil["bottles"])
chi2, p_c, dof, exp = stats.chi2_contingency(pd.crosstab(x, y))
assert exp.min() >= 5                                    # the cell-count rule
s_lo, s_hi = np.percentile(
    [daily.sample(frac=1.0, replace=True).mean() for _ in range(2000)],
    [2.5, 97.5])                                        # the bootstrap CI
```

**25. The chart pair (fast + craft)**

```python
ax = monthly.plot(figsize=(9, 4), color="#0F766E")       # fast
ax.set_title("Monthly revenue: growth, and the month-9 dip")
ax.set_ylabel("Revenue (USD)"); ax.spines[["top","right"]].set_visible(False)
fig = ax.get_figure(); fig.savefig("exhibit.png", dpi=150)   # craft: the file
```

## Bonus 1: The Monthly Pipeline (full listing)

Chapter 37's `build_report.py`, complete — the report that builds itself:

```python
"""Tariro's monthly report -- builds itself. Run: python build_report.py"""
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt

RAW, OUT = Path("data/raw"), Path("output")
TEAL, FENCE = "#0F766E", 21.50

def loading_checks(sales, customers):
    orphans = sales.loc[sales["customer_id"].notna()
        & ~sales["customer_id"].isin(customers["customer_id"])]
    lines = [f"sales rows: {len(sales):,}",
             f"null amounts: {sales['amount'].isna().sum()}",
             f"orphan sales: {len(orphans)}",
             f"total revenue: {sales['amount'].sum():,.2f}"]
    return "\n".join(lines), len(orphans), sales["amount"].isna().sum()

def main():
    sales = pd.read_csv(RAW / "sales.csv", parse_dates=["date"])
    customers = pd.read_csv(RAW / "customers.csv")
    sales["month"] = sales["date"].dt.to_period("M")

    log, n_orphan, n_null = loading_checks(sales, customers)
    if n_null > 0:
        raise SystemExit("ABORT: null amounts -- investigate first")
    if n_orphan > 20:
        raise SystemExit(f"ABORT: {n_orphan} orphans (tolerance 20)")

    monthly = sales.groupby("month")["amount"].sum()
    by_day = sales.groupby(sales["date"].dt.day_name())["amount"] \
                 .agg(["count", "sum", "mean"])
    member_share = (sales.assign(m=sales["customer_id"].notna())
                         .groupby("month")["m"].mean() * 100)
    latest, prev = monthly.index[-1], monthly.iloc[-2]

    out = OUT / str(latest); (out / "exhibits").mkdir(parents=True, exist_ok=True)

    fig, ax = plt.subplots(figsize=(9, 4))
    ax.plot(monthly.index.astype(str), monthly.values, color=TEAL)
    ax.set_title(f"Monthly revenue: {monthly.iloc[-1]:,.0f} "
                 f"({(monthly.iloc[-1]/prev-1)*100:+.1f}% MoM)")
    ax.set_ylabel("Revenue (USD)"); fig.autofmt_xdate()
    fig.savefig(out / "exhibits" / "revenue.png", dpi=150,
                bbox_inches="tight"); plt.close(fig)

    report = f"""# Tariro's Grocery -- Monthly Report {latest}

Revenue: ${monthly.iloc[-1]:,.2f}
({(monthly.iloc[-1]/prev-1)*100:+.1f}% vs {monthly.index[-2]}).
Member share of sales: {member_share.iloc[-1]:.1f}%.
Sunday takings averaged ${by_day.loc['Sunday','mean']:,.0f} vs weekday
${by_day.drop('Sunday')['mean'].mean():,.0f}.

_Caveats: member share is association, not causation;
one shop's 18 months is a sample, not a population._

## Run log
```
{log}
```
"""
    (out / "report.md").write_text(report)
    print(f"Built: {out/'report.md'}")

if __name__ == "__main__":
    main()
```

## Bonus 2: Generating Tariro's Data

The recipe behind the running case — noise, then planted effects, then the truth file (Ch. 44's method; adapt freely, label always):

```python
"""Generate Tariro's dataset: honest noise + planted effects + truth file."""
import numpy as np, pandas as pd

rng = np.random.default_rng(42)          # seeded: reproducible truth
days = pd.date_range("2024-01-01", periods=548, freq="D")   # 18 months

# ---- noise: weekdays vary, lognormal basket amounts (right-skew, Ch. 23)
base_traffic = {"Monday": 30, "Tuesday": 32, "Wednesday": 34,
                "Thursday": 33, "Friday": 42, "Saturday": 46, "Sunday": 26}
rows = []
for d in days:
    n = rng.poisson(base_traffic[d.day_name()])
    payday = 1.35 if d.day >= 25 else 1.0          # PLANT: payday spike
    fri_sat = 1.33 if d.day_name() in ("Friday", "Saturday") else 1.0
    n = int(n * payday * fri_sat)
    for _ in range(n):
        amount = round(float(rng.lognormal(1.6, 0.55)), 2)   # median ~5
        rows.append({"date": d, "amount": min(amount, 420.0)})

sales = pd.DataFrame(rows)
sales["payment_type"] = rng.choice(               # PLANT: EcoCash rising
    ["Cash", "EcoCash", "Card"], p=[.45, .40, .15],
    size=len(sales))
# ... payment probs drift by month toward EcoCash; items/categories assigned;
#     oil price rises +0.80 in month 9, quantities fall ~35% (PLANT);
#     member ids attached for ~25% of sales; founding cohort's frequency
#     declines 8%/month after month 12 (PLANT: the churn);
#     3 stock weeks dropped, ~1% amounts zeroed, a duplicate row inserted.

# ---- the truth file: score every method against known reality
truth = """# Truth (planted patterns)
- payday (25th+): traffic x1.35
- Friday/Saturday: x1.33
- Sunday: base 26 vs weekday ~32 (the shortfall is TRAFFIC)
- oil: price +0.80 at month 9; quantity -35% (quantity-led collapse)
- EcoCash share: 31% -> 44% across 18 months
- founding cohort: -8%/month frequency after month 12
- flaws: 3 missing stock weeks; 1 duplicated sale; 1 amount lost a zero
"""
Path("truth.md").write_text(truth)
```

*(The full generator, with every planted pattern implemented, ships with the book's repository — the listing above is the skeleton; the `truth.md` is the point: analyses scored against known reality.)*

*The cookbook's one law, inherited from Part V: the notebook that cannot be Restart-and-Run-All'd is a rumour — every snippet above assumes clean, top-to-bottom reproducibility.*
