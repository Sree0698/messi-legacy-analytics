-- 1. Goal contribution (G+A) per club season, ranked descending
SELECT
    season,
    club,
    goals,
    assists,
    goals + assists AS goal_contributions
FROM messi_analytics.club_stats
ORDER BY goal_contributions DESC;

-- 2. Running (cumulative) career goals across club seasons, using a window function
SELECT
    season,
    club,
    goals,
    SUM(goals) OVER (ORDER BY season ROWS UNBOUNDED PRECEDING) AS cumulative_goals
FROM messi_analytics.club_stats
ORDER BY season;

-- 3. Best statistical season per club, using RANK() partitioned by club
SELECT *
FROM (
    SELECT
        season,
        club,
        goals,
        assists,
        RANK() OVER (PARTITION BY club ORDER BY goals DESC) AS goal_rank_in_club
    FROM messi_analytics.club_stats
)
WHERE goal_rank_in_club = 1;

-- 4. Career phase comparison via CTE: Barcelona vs PSG vs Inter Miami totals
WITH club_totals AS (
    SELECT
        club,
        COUNT(*) AS seasons_played,
        SUM(appearances) AS total_appearances,
        SUM(goals) AS total_goals,
        SUM(assists) AS total_assists,
        SUM(trophies_won) AS total_trophies
    FROM messi_analytics.club_stats
    GROUP BY club
)
SELECT
    club,
    seasons_played,
    total_appearances,
    total_goals,
    total_assists,
    ROUND(total_goals / NULLIF(total_appearances, 0), 2) AS goals_per_appearance,
    total_trophies
FROM club_totals
ORDER BY total_goals DESC;

-- 5. Goal involvement efficiency (goals+assists per appearance) year over year, with
--    a 3-row moving average using a window function
WITH per_season AS (
    SELECT
        season,
        club,
        appearances,
        goals,
        assists,
        ROUND((goals + assists) / NULLIF(appearances, 0), 2) AS ga_per_app
    FROM messi_analytics.club_stats
)
SELECT
    season,
    club,
    ga_per_app,
    ROUND(AVG(ga_per_app) OVER (
        ORDER BY season
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ), 2) AS three_season_moving_avg
FROM per_season
ORDER BY season;

-- 6. International tournaments: goals per tournament, best to worst
SELECT
    year,
    tournament,
    result,
    goals,
    assists,
    CASE WHEN result = 'Champion' THEN 1 ELSE 0 END AS trophy_won
FROM messi_analytics.international_stats
ORDER BY goals DESC;

-- 7. Career-long summary: club vs international goal totals
SELECT 'Club (all competitions)' AS scope, SUM(goals) AS total_goals, SUM(assists) AS total_assists
FROM messi_analytics.club_stats
UNION ALL
SELECT 'International (Argentina)' AS scope, SUM(goals) AS total_goals, SUM(assists) AS total_assists
FROM messi_analytics.international_stats;

-- 8. Trophy timeline — every major trophy year across club and international careers
SELECT year AS trophy_year, tournament AS competition, 'International' AS scope
FROM messi_analytics.international_stats WHERE result = 'Champion'
UNION ALL
SELECT
    CAST(SUBSTR(season, 1, 4) AS INT64) AS trophy_year,
    club AS competition,
    'Club' AS scope
FROM messi_analytics.club_stats
WHERE trophies_won > 0
ORDER BY trophy_year;

-- ============================================================
-- CREATIVE / NARRATIVE FINDINGS
-- ============================================================

-- 9. Age-defying output: share of career club goals scored at age 35+
WITH totals AS (
    SELECT
        SUM(goals) AS career_goals,
        SUM(CASE WHEN approx_age >= 35 THEN goals ELSE 0 END) AS goals_35_plus
    FROM messi_analytics.club_stats
)
SELECT
    career_goals,
    goals_35_plus,
    ROUND(100.0 * goals_35_plus / career_goals, 1) AS pct_goals_after_35
FROM totals;

-- 10. Consistency index: mean, stdev, and coefficient of variation of Barcelona
--     season goal tallies (BigQuery has native STDDEV_POP, used here directly)
WITH barca AS (
    SELECT goals FROM messi_analytics.club_stats WHERE club = 'FC Barcelona'
)
SELECT
    ROUND(AVG(goals), 1) AS mean_goals_per_season,
    ROUND(STDDEV_POP(goals), 1) AS stdev_goals_per_season,
    ROUND(STDDEV_POP(goals) / AVG(goals), 2) AS coefficient_of_variation
FROM barca;

-- 11. Trophy efficiency: goals required per trophy won, club vs. international
SELECT 'FC Barcelona' AS scope, SUM(goals) AS goals, SUM(trophies_won) AS trophies,
       ROUND(SUM(goals) / NULLIF(SUM(trophies_won), 0), 1) AS goals_per_trophy
FROM messi_analytics.club_stats WHERE club = 'FC Barcelona'
UNION ALL
SELECT 'Paris Saint-Germain', SUM(goals), SUM(trophies_won),
       ROUND(SUM(goals) / NULLIF(SUM(trophies_won), 0), 1)
FROM messi_analytics.club_stats WHERE club = 'Paris Saint-Germain'
UNION ALL
SELECT 'Inter Miami CF', SUM(goals), SUM(trophies_won),
       ROUND(SUM(goals) / NULLIF(SUM(trophies_won), 0), 1)
FROM messi_analytics.club_stats WHERE club = 'Inter Miami CF'
UNION ALL
SELECT 'Argentina (International)', SUM(goals), SUM(CASE WHEN result = 'Champion' THEN 1 ELSE 0 END),
       ROUND(SUM(goals) / NULLIF(SUM(CASE WHEN result = 'Champion' THEN 1 ELSE 0 END), 0), 1)
FROM messi_analytics.international_stats
ORDER BY goals_per_trophy;

-- 12. Resilience: "dip-then-bounce-back" seasons, using LAG/LEAD window functions
WITH ordered AS (
    SELECT
        season, club, goals,
        LAG(goals) OVER (ORDER BY season) AS prev_goals,
        LEAD(goals) OVER (ORDER BY season) AS next_goals
    FROM messi_analytics.club_stats
)
SELECT
    season, club, goals, prev_goals, next_goals,
    CASE
        WHEN goals < prev_goals AND next_goals > goals THEN 'Bounced back'
        WHEN goals < prev_goals AND next_goals IS NULL THEN 'Career ended on a dip'
        WHEN goals < prev_goals THEN 'Did not bounce back'
        ELSE NULL
    END AS dip_outcome
FROM ordered
WHERE goals < prev_goals
ORDER BY season;

-- 13. World Cup arc: goals per World Cup across all six tournaments
SELECT
    year,
    result,
    goals,
    RANK() OVER (ORDER BY goals DESC) AS goal_rank_among_world_cups
FROM messi_analytics.international_stats
WHERE tournament = 'FIFA World Cup'
ORDER BY year;

-- 14. Playmaker evolution: assist share of total goal contributions,
--     early career (2004-05 to 2007-08) vs. final seasons (2024-2026)
SELECT
    CASE
        WHEN season IN ('2004-05','2005-06','2006-07','2007-08') THEN 'Early career (age 18-21)'
        WHEN season IN ('2024','2025','2026') THEN 'Final seasons (age 37-39)'
    END AS career_phase,
    ROUND(AVG(assists / NULLIF(goals + assists, 0)), 3) AS avg_assist_share
FROM messi_analytics.club_stats
WHERE season IN ('2004-05','2005-06','2006-07','2007-08','2024','2025','2026')
GROUP BY career_phase;

-- 15. Best tournament performance in a losing campaign
SELECT year, tournament, result, goals
FROM messi_analytics.international_stats
WHERE result != 'Champion'
ORDER BY goals DESC
LIMIT 3;
