# Chapter 51: Retail and E-Commerce — The Ndineka Fashion House Playbook

*Part X — Analytics Across Industries: Domain Playbooks*

> "Retail analytics is one question in four costumes: what to stock, at what price, for whom, and how much is already dead."

### In this chapter you will learn

- The retail playbook canvas: six slots that organise every retail analytics problem.
- Market-basket analysis: affinity, lift, and the difference between "bought together" and "buys more because".
- Markdown optimisation and price elasticity, honestly bounded.
- Customer lifetime value with the RFM bridge from your toolkit.
- The failure modes: the average customer, the dead-stock spiral, promo dependence.

## 51.1 The Retail Question

**Ndineka Fashion House** is a fictional Harare retailer: four stores, a growing online channel, 30,000 SKUs of seasonal clothing, and a founder — Ndineka herself — who describes her business in one sentence: "I buy six months before I sell, and I am wrong on purpose because being exactly right is impossible." That sentence is the entire retail problem. Inventory is frozen cash; the buy decision is made under uncertainty about weather, taste, and the economy; and the analyst's job is to shrink the wrongness, not to pretend it away.

Every retail analytics question reduces to one of four: **what to stock** (assortment), **at what price** (pricing and markdown), **for whom** (customers), and **how much is already dead** (inventory health). The playbook canvas organises them:

| Slot | Ndineka's answer |
|---|---|
| Core question | Which lines, at what price, for which customers, bought how deep? |
| Unit of analysis | The SKU × store × week (and the customer, for the CLV layer) |
| Key metrics | Sell-through, gross margin, weeks of cover, dead-stock value, CLV |
| Data reality | POS transactions, seasonal buys, returns, a loyalty app, no true cost of returns |
| First project | The dead-stock ledger: name it, age it, price it |
| Failure mode | Promo dependence — margin spent to buy revenue |

## 51.2 The Dead-Stock Ledger First

The highest-return first project in retail is almost always an inventory health report, because it requires no modelling and funds everything that follows. The discipline is aging: every SKU-store row gets weeks-on-shelf, sell-through rate, and a classification.

```sql
SELECT sku, store,
       weeks_on_shelf,
       units_sold / NULLIF(units_received, 0) AS sell_through,
       CASE
         WHEN weeks_on_shelf >= 26 AND sell_through < 0.30 THEN 'dead'
         WHEN weeks_on_shelf >= 12 AND sell_through < 0.50 THEN 'slow'
         ELSE 'healthy'
       END AS stock_class,
       retail_price * units_on_hand AS frozen_value
FROM inventory_snapshot
ORDER BY frozen_value DESC;
```

The `frozen_value` column is the meeting: when the leadership team sees that 22% of working capital is wearing a "dead" tag, markdown optimisation stops being a data science conversation and becomes a Tuesday agenda item.

## 51.3 Market-Basket Analysis

Baskets are the atom of retail behaviour. The classic measures, on the Soulfya's data you already know from Part II:

- **Support** — the share of baskets containing the pair. Rare pairs are noise.
- **Confidence** — given the anchor, how often the companion appears.
- **Lift** — confidence divided by the companion's base rate. Lift above 1 means the anchor *changes* the companion's probability.

```python
pairs = (baskets.groupby(["anchor", "companion"])["basket_id"].nunique()
         .rename("both").reset_index())
pairs = pairs.merge(anchor_totals, on="anchor").merge(comp_totals, on="companion")
pairs["confidence"] = pairs["both"] / pairs["anchor_total"]
pairs["lift"] = pairs["confidence"] / (pairs["companion_total"] / n_baskets)
strong = pairs[(pairs["support"] >= 0.005) & (pairs["lift"] >= 1.5)]
```

The trap is reading lift as causation. Sadza-and-soft-drink has lift 1.4 because dinner is dinner — the pair reflects a meal occasion, not a promotion opportunity. The honest reading of basket analysis is *hypothesis generation*: every strong pair is a candidate for an experiment (Chapter 61's toolkit), never a layout change on its own.

## 51.4 Markdown and Price Elasticity

Markdown is not discounting; it is *managing the decay curve of a perishable asset* — fashion is perishable milk with better lighting. The analyst's contribution is elasticity bounded honestly. Fit demand (units sold) against price across comparable lines and weeks, but never as raw regression: confounders (season, stock depth, weather) ride along with every price cut. The defensible version is difference-based: compare similar items marked down at different times, or the same item across stores with staggered markdowns, and bound the elasticity estimate — "between -1.2 and -2.0" is an honest answer; "-1.61" is a costume.

Markdown optimisation, one paragraph: for each dead SKU, choose the smallest discount that clears stock before its terminal date (season end), given the elasticity bound and the salvage value. A -30% markdown that clears 80% of units beats a -50% markdown that clears 95% — the remaining 15% is worth more in the bargain bin than the margin given away on the first 80.

## 51.5 The Customer Layer: RFM to CLV

**From Your Toolkit — Excel and SQL:** you have built an RFM table before, even if you called it "sorting customers". Recency, frequency, monetary value is a pivot table in Excel (`GROUP BY` in SQL): every customer scored 1–5 on each axis, segments read off the grid — champions, at-risk, hibernating, gone. The bridge to CLV is Chapter 52's subject in full, but the retail version in one line: **CLV = margin per period × expected periods remaining**, with expected periods estimated from the retention curve of the customer's segment. Ndineka's champions (top RFM decile) generate 41% of margin — the number that justifies the loyalty programme's entire budget, and the number to check monthly.

## 51.6 Returns and the Long Tail

Two quiet killers. **Returns**: the online channel's return rate (Ndineka's is 28%, driven by sizing) is a data problem — fit notes, size charts, and the returns ledger joined back to product metadata turns "free shipping both ways" from a cost into a feedback loop that fixes the catalogue. **The long tail**: 30,000 SKUs means most SKUs sell rarely; models fit on averages will misprice the tail. Segment the assortment (core / seasonal / tail) and model each with its own honesty — the tail gets rules and monitoring, not deep learning.

## 51.7 Failure Modes

- **The average customer** — no one is average; averages misprice the tail and mis-target promotions. Segment first (Chapter 30), always.
- **The dead-stock spiral** — refusing to mark down because "the margin loss is visible and the cash release isn't". Show the ledger in cash terms.
- **Promo dependence** — every promotion trains customers to wait (Chapter 32's sleeping dogs, in retail form). Track full-price sell-through as a health metric, not just revenue.
- **Basket-lift layouts** — rearranging stores on untested affinities; Chapter 61's discipline applies.

> **Teaching Tip — The frozen-cash walk:** take the class to any clothing store (or its website) and have each student pick three items, guess weeks-on-shelf and the coming markdown, and write the retailer's likely reason for the buy. Back in the lab, the dead-stock ledger feels like a familiar object, not a SQL exercise. The best retail exam question is one sentence: "Why is retail inventory perishable?"

## Key Takeaways

- Retail is four questions: assortment, price, customers, inventory health — and the canvas keeps them straight.
- The dead-stock ledger is the highest-ROI first project: no models, immediate cash conversation.
- Basket analysis (support, confidence, lift) is hypothesis generation; lift is not causation, and layouts deserve experiments.
- Elasticity is a bound, not a number; markdown is perishable-asset decay management.
- RFM is the bridge from transactions to customers, and full-price sell-through guards against promo dependence.

## Practice Lab

1. Build the dead-stock ledger on Soulfya's inventory snapshot (Appendix F generator): classify SKUs, sum frozen value, and write the one-page memo that makes the cash visible.
2. Compute support, confidence, and lift for all item pairs in a month of baskets; list the top ten by lift and annotate each with "occasion, substitution, or cause?" — then design the experiment that would settle one of them.
3. Estimate the elasticity bound for a markdown family using staggered-store prices; write the confidence interval and one paragraph on what confounds remain.
4. Build the RFM grid for Soulfya's Soul Circle members; identify the at-risk segment and size the win-back budget with an expected-value calculation.
5. Audit the long tail: what share of SKUs sold fewer than three units last quarter, and what rule (not model) would you apply to them?
6. The Ndineka memo: three recommendations — one assortment, one pricing, one customer — each with its metric, its baseline, and its reversal condition.

## Further Reading

- *The New Science of Retailing* — Fisher and Raman
- *Why We Buy* — Paco Underhill (the physical analogue of basket analysis)
- Chapter 32 (uplift), Chapter 61 (causal discipline for experiments), Chapter 62 (pricing under uncertainty)
