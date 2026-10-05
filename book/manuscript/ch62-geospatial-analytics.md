# Chapter 62: Geospatial Analytics — Where the Data Lives

*Part XI — The Frontier: Advanced Methods and Emerging Practice*

> "Every row has an address; most analysis pretends it doesn't."

### In this chapter you will learn

- Spatial data's two geometries (points and polygons) and the spatial join.
- Distance-based features: buffers, drive times, and nearest-neighbour logic.
- Moran's I: measuring clustering honestly, with a permutation test.
- The Soulfya's fourth-outlet siting study: demand surfaces, cannibalisation, and the gravity model.
- The modifiable areal unit problem and the ecological fallacy.
- Failure modes: the heat map that lies, and choropleths of population.

## 62.1 Space Is a Column You Forgot

Soulfya's delivery data has a latitude and longitude on every order — two columns the dashboards ignore. Turn them on and the questions multiply: where do orders come from, how far is too far, which neighbourhoods churn on delivery times, and where should the fourth outlet go? Geospatial analytics is not a new discipline so much as a missing feature: **place**, with its own joins, its own statistics, and its own ways to lie.

The two geometries that cover 90% of practice: **points** (customers, orders, outlets, towers) and **polygons** (suburbs, wards, districts, trade areas). The core operation is the **spatial join**: which polygon contains each point, or which point is nearest each point — and once you can do that, place flows into every model you already know.

```python
import geopandas as gpd
orders = gpd.GeoDataFrame(orders,
    geometry=gpd.points_from_xy(orders["lon"], orders["lat"]), crs="EPSG:4326")
wards = gpd.read_file("wards.geojson")
orders_by_ward = gpd.sjoin(orders, wards, how="left", predicate="within")
```

**From Your Toolkit — Power BI:** every map visual you have built was a spatial join the tool did silently — points coloured by a measure, with the polygon boundaries implied. The bridge: when the map is not enough (drive times, buffers, clustering tests), the same data goes to `geopandas`, and the result comes back as a column the dashboard can show.

## 62.2 Distance Features: Buffers and Drive Times

Straight-line distance is where spatial features begin and where they mislead. The craft: **buffers** (everything within 2 km of an outlet — but a river is not 2 km of road), **drive times** (the honest measure, from a routing service or a road network graph), and **nearest-X** (distance to the nearest competitor, computed once, reused everywhere). Soulfya's delivery data shows the classic result: orders fall off sharply past 15 minutes of drive time, not past any straight-line threshold — the river and the highway decide the trade area, not the compass.

## 62.3 Moran's I: Is It Clustered, or Does It Just Look Clustered?

Humans see clusters in noise; Moran's I is the test that keeps you honest. The statistic measures whether near things are more alike than far things — spatial autocorrelation — and it is one ratio:

```text
I = (n / S0) * sum(i,j: wij * (xi - xbar)(xj - xbar)) / sum(i: (xi - xbar)^2)
```

Values near +1 mean clustered (similar values adjacent), near 0 mean scattered, negative means dissimilar values adjacent. The interpretation rule that makes it honest: **never read the raw I without its permutation test** — shuffle the values across the map a thousand times, and see how often chance produces an I this large. In the Soulfya's outlet-siting lab, delivery-frequency by suburb yields I = 0.31 with a permutation p of 0.004: the clustering is real, and the hot spots in the north and east are where the analysis should look.

## 62.4 Siting the Fourth Outlet

The part's running study: Azu wants a fourth outlet, and the analytics earn their fee by turning a hunch ("Borrowdale feels busy") into a siting shortlist. The method, in layers:

1. **The demand surface**: kernel density of delivery orders and loyalty visits, weighted by basket value — where does money live on the map?
2. **The competition and cannibalisation layer**: a simple gravity model — expected patronage falls with drive time and rises with outlet attractiveness — to estimate how much of the new outlet's revenue comes from the existing three. A site that "wins" mostly by stealing Avondale's customers is a smaller decision than it looks.
3. **The constraint layer**: rent per square metre, parking, power reliability, staff transport — the Chapter 59 lesson that constraints are the model.
4. **The shortlist memo**: three sites, expected incremental revenue (net of cannibalisation) with intervals, and the pre-committed measurement plan (a control geography for the post-opening evaluation, Chapter 61's ghost).

## 62.5 Two Classic Traps

- **The modifiable areal unit problem (MAUP)** — aggregate the same points by suburb and the pattern says one thing; by ward and it says another; by 1-km grid and a third. There is no "true" aggregation — so report the one that matches the decision (trade areas for siting; administrative units for compliance) and check that the finding survives the alternatives.
- **The ecological fallacy** — a suburb whose average income is high is not a suburb of rich households; averages over areas describe areas, never the people in them. The analyst's rule: **aggregate for planning, individual data for people-level claims**, and never slide between them silently.

## 62.6 Failure Modes

- **The heat map that lies** — kernel density of *orders* shows where your current customers are, not where demand is (the whole city orders less from a badly-placed outlet); normalise by population or households before calling anything a demand map.
- **Choropleths of population** — more people means more everything; map *rates*, not counts, or the map is a population map wearing a costume.
- **Precision navels** — coordinates to six decimal places from a phone's GPS are accurate to a city block on a good day; match the precision of the geography to the precision of the decision.
- **The missing base map moment** — analysis that never checks whether the "empty" area is empty because of data gaps (no delivery coverage = no orders recorded), not absence of demand.

> **Teaching Tip — Two maps, one truth:** hand students the same point data and ask for the trade-area map twice — once as straight-line buffers, once as drive-time polygons. The two maps disagree about every border suburb, and the disagreement is the lecture: geography is a model too, and the road network is part of your data whether you loaded it or not.

## Key Takeaways

- Space is a feature: spatial joins and distance features bring place into every model you already know.
- Straight-line distance misleads; drive time is the honest currency of trade areas and delivery.
- Moran's I plus its permutation test separates real clustering from pattern-hungry eyes.
- Siting is layered: demand surface, cannibalisation (gravity), constraints, and a pre-committed evaluation plan.
- Aggregate for planning, individual data for people; and always check which aggregation is doing the talking (MAUP).

## Practice Lab

1. Build the demand surface for Soulfya's delivery orders; map it per 1,000 households, and mark where the raw-count map and the normalised map disagree most.
2. Compute nearest-competitor and drive-time-to-outlet features for every member; add them to the churn model from Part V and report whether they earn their place.
3. Compute Moran's I for delivery frequency by suburb; run the permutation test and write the two-sentence interpretation a manager can repeat. (The worked numbers — with the sum of cross-products 502.5 — are in Appendix G.)
4. The siting study: build the gravity model, score three candidate sites on incremental revenue net of cannibalisation, and write the shortlist memo with intervals.
5. The MAUP audit: aggregate the same orders by suburb, ward, and 1-km grid; find one finding that changes sign across aggregations and explain what the decision-maker should be told.
6. The missing-base-map check: identify suburbs with zero orders, and determine — from coverage polygons and population — whether they are low demand or no coverage.

## Further Reading

- *Geographic Data Science with Python* — Rey, Arribas-Bel and Wolf (free online)
- `geopandas` and `libpysal` documentation and galleries
- Chapter 61 (the evaluation plan every siting deserves), Chapter 59 (constraints as data), Chapter 57 (wards and the public-sector map)
