# Chapter 66: Simulation I — Queueing and the Utilisation Cliff

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "Busy feels like a staffing problem; it is almost always a mathematics problem."

### In this chapter you will learn

- The three numbers of every queue: arrival rate, service rate, utilisation.
- The utilisation cliff: why waits explode as you approach 100% busy.
- Little's Law and the queue arithmetic you can do on a napkin.
- Variability's surcharge: Kingman's formula, and why averages lie at the counter.
- Pools versus separate queues, and the staffing memo that settles it.
- Failure modes: the utilisation target that kills, and the average wait nobody lives.

## 66.1 The Queue You Already Own

Soulfya's Avondale outlet on a Saturday: one till, a steady stream of customers, and a manager who believes the answer is "more staff, obviously". The analytics answer is a piece of arithmetic that says *when* more staff matter, *how much*, and what the current wait is costing — before anyone is hired. Queueing theory is the mathematics of waiting lines, and it is the highest-return-per-formula chapter in this book for anyone who touches operations: restaurants, clinics (Chapter 54), licensing offices (Chapter 57), delivery dispatch, support desks.

## 66.2 Three Numbers

- **λ (lambda)** — the arrival rate: customers per minute, orders per hour. Estimated from timestamps, and *as a distribution* — Saturday arrivals are not a smooth river; they clump.
- **μ (mu)** — the service rate: customers served per minute per server, from the service-time distribution (and its variance, which matters as much as its mean).
- **ρ (rho)** — the utilisation: λ / (number of servers × μ). The share of capacity that is busy. ρ must stay below 1; the interesting question is how far below.

Every queue conversation is three numbers, and the discipline of the chapter is extracting them from the timestamps you already log.

## 66.3 The Cliff

The single most valuable table in operational analytics — expected waiting time in queue (Wq) for a single-server queue at increasing utilisation, in units of mean service time (M/M/1, Wq = ρ/(μ−λ)):

| Utilisation ρ | Wq in service times | At Soulfya's (mean service 3.0 min) |
|---|---|---|
| 0.60 | 1.5 | 4.5 min (a calm counter) |
| 0.80 | 4.0 | 12 min (the line you photograph) |
| 0.90 | 9.0 | 27 min (walk-outs begin) |
| 0.95 | 19.0 | 57 min (the counter is a rumour) |

Read the shape, not the numbers: from 60% to 80% busy, waits double; from 80% to 90%, they double again; the last five points of utilisation cost more than the first fifty. The Saturday problem at Avondale is not "busy"; it is **ρ = 0.9 on one till** — and the fix is a second till at peak, which drops ρ to 0.45 for the queue that matters, at a fraction of a full-time hire.

```python
def mm1_wq(lam, mu):
    rho = lam / mu
    return rho / (mu - lam) if rho < 1 else float("inf")
# Two tills, pooled (M/M/2): waits fall faster than the naive halving
# because idle minutes on either till cover the other's clumps.
```

## 66.4 Little's Law and Kingman's Surcharge

**Little's Law** — L = λW — ties the queue in the room to the wait per customer: see 9 people waiting and you know the wait without a stopwatch. It is the napkin arithmetic of operations (Chapter 54's ward manager, Chapter 57's licensing office), and it is exactly true for any stable queue, however messy.

**Kingman's formula** is the honest upgrade to the table above: waits grow with *variability* as well as utilisation —

```text
Wq ≈ (ca^2 + cs^2)/2 × ρ/(1−ρ) × service_time
```

— where ca is arrival variability and cs is service-time variability. The management implications write themselves: **cut variability, not just add capacity**. A limited menu at peak (smaller cs), batch preparation before the rush, and smoothing arrival clumps (pre-orders, timed pickup slots) all shorten the line without a single new hire — and Chapter 67's simulation exists to test exactly these moves before the Saturday they land.

## 66.5 Pools versus Separate Queues

One queue feeding several servers beats one line per server — the pooled queue never idles a server while another line grows, and the customer experience (one fair line) is the one people rage about less. The exceptions are real: servers with different speeds (the fast lane behind the slow till), setup differences (the delivery-only counter), and the political economy of priority (clinical triage, Chapter 54). The analytics answer is a simulation run, not a principle — but the prior is pooled until proven otherwise.

## 66.6 The Staffing Memo

The chapter's deliverable, the one that earns the fee: current λ and μ by hour (from timestamps), current ρ and Wq, two staffing scenarios, and the cost line — expected walk-outs × basket value against wage minutes, at the p90 Saturday, not the average one. At Avondale: the second till at peak hours costs $38 per Saturday in wage minutes and removes an estimated 6 walk-outs at a $19 average basket — $114 recovered, a 3:1 return before counting the goodwill, which is the part the review scores (Chapter 60's attention logic) eventually bill.

**From Your Toolkit — Excel:** the entire chapter runs in a spreadsheet — Wq and Little's Law are one cell each, the scenario table is a data table, and the Saturday simulation of Chapter 67 can live beside it. Queueing arithmetic was born for the napkin and the spreadsheet; the manager you are advising already trusts both.

## 66.7 Failure Modes

- **The utilisation target that kills** — "keep staff 85% utilised" sounds efficient and, at the counter, is a queue policy: 85% on one till is a 20-minute line. Set targets on waits, not utilisation — capacity is the cost, the wait is the harm.
- **The average wait nobody lives** — mean Wq across the day hides the 12:30 spike that drives every review; report by hour, and defend the worst hour.
- **Arrivals as a rate** — the clumps are the message; a Poisson assumption you never check against the clumpy reality (church crowds, payday, the bus arrival) under-states the peak every time.
- **Serving the queue, not the customer** — optimising till throughput while the actual wait is at the kitchen (the system has two queues in series; the long one is the constraint).

> **Teaching Tip — Live the cliff:** run the class as a queue. One "server" rolling dice (mean service 30 seconds), "customers" arriving per a clumpy schedule — first at ρ = 0.5, then ρ = 0.9. Students time their own waits, plot them, and *feel* the non-linearity before you show the table. No one who has stood in the 0.9 round argues for the 85% utilisation target again.

## Key Takeaways

- Every queue is three numbers: λ, μ, ρ — extractable from timestamps you already log.
- Waits explode non-linearly as utilisation approaches 1: the last 5% of busy costs more than the first 50%.
- Little's Law (L = λW) is napkin arithmetic; Kingman adds the variability surcharge — cut variation, not just add capacity.
- Pooled queues beat separate lines until proven otherwise; simulation settles the exceptions.
- Staff against the p90 hour, target waits not utilisation, and always find the *longer* queue in the system.

## Practice Lab

1. Estimate λ and μ by hour from Soulfya's till timestamps (Appendix F); compute ρ and Wq per hour; find the cliff hours and the utilisation target hiding in the current roster.
2. The staffing memo: two scenarios, wage cost versus walk-out cost, at the p90 hour; write the one-page version the owner signs.
3. Variability audit: measure arrival clumping (variance/mean of counts) and service-time variance; use Kingman to rank three interventions — second till, limited menu, pre-order slots.
4. Pool test: simulate one shared queue versus two tills with separate lines under the measured Saturday pattern; report the wait distribution, not the mean.
5. The series trap: measure the kitchen queue and the till queue separately; identify which one binds at peak and recompute the staffing memo against the true constraint.
6. Little's Law check: count the queue at random moments (L) and the average wait from timestamps (W); verify L = λW and explain any gap as measurement error or non-stationarity.

## Further Reading

- *Queueing Methods for Services and Manufacturing* — Hall (the practitioner's reference)
- Little's original paper (1961) — one page, permanent value
- Chapter 67 (simulation that tests these moves), Chapter 54 and 57 (the clinic and the licensing office)
