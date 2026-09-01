# Tableau Dashboard — Build Spec

**Data source:** `messi_tableau_extract.csv` (one row per club season / international
tournament, unified with `scope`, `period`, `competition`, `appearances`, `goals`,
`assists`, `trophies_won`, `result`).

I can't run Tableau Desktop directly in this environment, so the data is fully
prepped — connect this CSV in Tableau Public/Desktop and build the four sheets
below, then combine into one dashboard. This should take ~20–30 minutes.

## Sheet 1 — "Career Arc" (line/area chart)
- Columns: `period` (sort by chronological order — add a calculated field
  `sort_order` if needed, or sort manually since seasons/years are already in order)
- Rows: `SUM(goals)`
- Color: `scope` (Club vs International)
- Mark type: Area or Line
- Filter: none (show full career)

## Sheet 2 — "Club Comparison" (bar chart)
- Filter: `scope = Club`
- Columns: `competition` (i.e., club name)
- Rows: `SUM(goals)`, `SUM(assists)` (dual axis or side-by-side bars)
- Color: `competition`
- Sort: descending by goals

## Sheet 3 — "Trophy Timeline" (Gantt/symbol map)
- Filter: `trophies_won = 1`
- Columns: `period`
- Rows: `competition`
- Color: `scope`
- Mark type: Circle, sized by 1 (constant) — a simple trophy timeline

## Sheet 4 — "Goal Involvement Efficiency" (scatter or bar)
- Calculated field: `GA per Appearance = (SUM([goals]) + SUM([assists])) / SUM([appearances])`
- Columns: `period`
- Rows: `GA per Appearance`
- Color: `scope`

## Dashboard layout
- Top: Sheet 1 (Career Arc) full width — the hero visual
- Bottom-left: Sheet 2 (Club Comparison)
- Bottom-right: Sheet 4 (Goal Involvement Efficiency)
- Floating element: Sheet 3 (Trophy Timeline) as a strip along the bottom
- Title: "Lionel Messi — A Data-Driven Retrospective (2004–2026)"
- Add a filter action: clicking a club/tournament in Sheet 2 or 3 highlights
  the corresponding points in Sheet 1

## Publishing
Once built, publish to **Tableau Public** and grab the embed/share link — that
link is what goes in the GitHub README and the LinkedIn post.

## Extra sheets — creative narrative findings

The extract now includes `approx_age` and `assist_share` columns to support
these additional sheets:

### Sheet 5 — "The Age-Defying Curve" (dual-axis line + reference band)
- Columns: `approx_age`
- Rows: `SUM(goals)`
- Color/Shape: highlight ages 35+ in a different color (calculated field:
  `IF [approx_age] >= 35 THEN "35+" ELSE "Under 35" END`)
- Callout: annotate that ~14% of his career club goals came at age 35+

### Sheet 6 — "World Cup Arc" (the standout visual)
- Filter: `competition = FIFA World Cup`
- Columns: `period` (World Cup year)
- Rows: `SUM(goals)`
- Mark type: Line with circle markers, labeled with `result`
- This is the U-shaped/non-linear chart — his two highest-scoring World Cups
  were his last two (2022 and 2026). Make this the dashboard's focal chart.

### Sheet 7 — "Scorer to Creator" (playmaker evolution)
- Columns: `period` (club seasons only)
- Rows: `AVG(assist_share)` formatted as a percentage
- Trend line: enable Tableau's built-in trend line to show the upward slope
- Reference line: overall career average `assist_share`

### Sheet 8 — "Trophy Efficiency" (goals required per trophy)
- Calculated field: `Goals per Trophy = SUM([goals]) / SUM([trophies_won])`
- Columns: `competition` grouped as Barcelona / PSG / Inter Miami / Argentina
  (use a calculated "team" field, since club vs. international rows are
  structured slightly differently — group by `league` or a custom grouping)
- Rows: `Goals per Trophy`
- Sort ascending — Argentina should surface as the most efficient, undercutting
  the "couldn't win for country" narrative

### Suggested dashboard additions
- Add Sheet 6 (World Cup Arc) as a second hero visual alongside Sheet 1
- Add Sheet 8 (Trophy Efficiency) as a callout tile with a bold headline number
  ("11.3 goals per international trophy — his most efficient trophy conversion
  of any team")
