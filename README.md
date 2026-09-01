# Messi Legacy Analytics

A full-stack data analytics retrospective on Lionel Messi's professional career —
built across **Excel, SQL, Python, and Tableau** — timed to his retirement from
international football with Argentina (August 31, 2026).

> Note: Messi retired from the **Argentina national team**, not from club football.
> He continues playing for Inter Miami CF (MLS) through 2028. This project covers
> his full club tenure (Barcelona → PSG → Inter Miami) and his complete major-
> tournament international record.

## Project Structure

```
messi-legacy-analytics/
├── data/
│   ├── messi_club_stats.csv           # Season-by-season club stats, 2004–2026
│   ├── messi_international_stats.csv  # Major tournament stats, 2005–2026
│   └── DATA_NOTES.md                  # Sourcing & methodology
├── sql/
│   ├── build_db.py                    # Loads CSVs into SQLite
│   ├── analysis_queries.sql           # CTEs, window functions, ranking queries
│   └── messi_analytics.db
├── python/
│   └── analysis.py                    # EDA + matplotlib visualizations
├── excel/
│   ├── build_workbook.py              # Generates the workbook programmatically
│   └── Messi_Legacy_Analytics.xlsx    # Formula-driven workbook w/ charts + Creative Insights sheet
├── tableau/
│   ├── messi_tableau_extract.csv      # Unified extract for Tableau
│   └── TABLEAU_DASHBOARD_SPEC.md      # Dashboard build spec
└── visuals/                           # Exported PNG charts from the Python script
```

## Tech Stack & What Each Layer Does

| Layer | Tool | What it shows |
|---|---|---|
| Data prep | Python / pandas | Cleaning, unifying club + international records |
| Analysis | SQL (SQLite) | CTEs, window functions (`RANK`, `SUM() OVER`, moving averages), trophy timeline |
| Analysis & viz | Python / matplotlib | Career arc, cumulative goals, club comparison, tournament goals |
| Reporting | Excel / openpyxl | Formula-driven summary workbook (SUMIF, ROUND) with native charts |
| BI Dashboard | Tableau | Interactive career-arc dashboard with cross-filtering |

## Key Findings

**The basics:**
- **672 goals in 778 appearances for Barcelona** (0.86 G/app) across 17 seasons — the peak was **2011-12: 73 goals, 29 assists**.
- Of 8 major international tournaments analyzed, Messi's Argentina reached **6 finals**, converting **3 into trophies** (2021 & 2024 Copa América, 2022 World Cup).

**The creative findings:**
1. **Age-defying output** — 13.8% of his career club goals (108 of 780) came at age 35+, across 169 appearances. Elite athletes are supposed to decline after 32-33; Messi didn't.
2. **Remarkable consistency** — Barcelona goals-per-season had a coefficient of variation of just 0.48 across 17 seasons (mean 39.5, stdev 19.0) — sustained excellence, not a short peak.
3. **The trophy-efficiency paradox** — goals required per trophy won: Barcelona 26.9, Inter Miami 19.0, PSG 16.0, but **Argentina just 11.3**. Despite a decade of "can't win for country" criticism, his individual output converted to team silverware *more* efficiently at international level than at any club.
4. **Near-total resilience** — of 9 statistical "dip" seasons across his career, **8 were immediately followed by a rebound**. The only one that wasn't was his final season (2026) — because there was no next season left to bounce back in.
5. **The World Cup arc is a U-curve, not a decline** — goals per World Cup: 1, 0, 4, 1, 7, **8**. His two highest-scoring World Cups were his *last* two, at ages 35 and 39.
6. **Scorer to creator** — assist share of goal contributions rose from 21.3% (age 18-21) to 37.8% (age 37-39), a clear tactical evolution as he aged.
7. **The 2016 preview** — his best tournament tally in a losing campaign (5 goals, 2016 Copa América Centenario) came five years before his first international trophy.

## How to Reproduce
```bash
pip install pandas matplotlib openpyxl
python sql/build_db.py
python python/analysis.py
python excel/build_workbook.py
```

## Author
Sreelakshmi (E S) — Data Quality Analyst
[GitHub](https://github.com/Sree0698) · [LinkedIn](https://www.linkedin.com/in/e-s-sreelakshmi-95504b241)
