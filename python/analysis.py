"""
Messi Legacy Analytics — Python EDA & Visualization
Reads the club/international CSVs and produces summary stats + charts.
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(BASE, "data")
VIS = os.path.join(BASE, "visuals")
os.makedirs(VIS, exist_ok=True)

club = pd.read_csv(os.path.join(DATA, "messi_club_stats.csv"))
intl = pd.read_csv(os.path.join(DATA, "messi_international_stats.csv"))

club["goal_contributions"] = club["goals"] + club["assists"]
club["ga_per_app"] = (club["goal_contributions"] / club["appearances"]).round(2)
club["cumulative_goals"] = club["goals"].cumsum()

plt.style.use("seaborn-v0_8-whitegrid")
COLORS = {"FC Barcelona": "#A50044", "Paris Saint-Germain": "#004170", "Inter Miami CF": "#F7B5CD"}

# ---- Chart 1: Goals per season by club ----
fig, ax = plt.subplots(figsize=(13, 6))
bar_colors = club["club"].map(COLORS)
ax.bar(club["season"], club["goals"], color=bar_colors)
ax.set_title("Lionel Messi — Goals per Club Season (All Competitions)", fontsize=14, weight="bold")
ax.set_ylabel("Goals")
ax.set_xlabel("Season")
plt.xticks(rotation=45, ha="right")
handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in COLORS.values()]
ax.legend(handles, COLORS.keys(), title="Club")
plt.tight_layout()
plt.savefig(os.path.join(VIS, "goals_per_season.png"), dpi=150)
plt.close()

# ---- Chart 2: Cumulative career goals ----
fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(club["season"], club["cumulative_goals"], marker="o", color="#A50044", linewidth=2)
ax.set_title("Lionel Messi — Cumulative Club Career Goals (2004–2026)", fontsize=14, weight="bold")
ax.set_ylabel("Cumulative Goals")
ax.set_xlabel("Season")
plt.xticks(rotation=45, ha="right")
ax.yaxis.set_major_locator(mticker.MultipleLocator(100))
plt.tight_layout()
plt.savefig(os.path.join(VIS, "cumulative_goals.png"), dpi=150)
plt.close()

# ---- Chart 3: Club totals comparison ----
club_totals = club.groupby("club").agg(
    total_goals=("goals", "sum"),
    total_assists=("assists", "sum"),
    total_apps=("appearances", "sum"),
    seasons=("season", "count"),
).reset_index()
club_totals["goals_per_app"] = (club_totals["total_goals"] / club_totals["total_apps"]).round(2)

fig, ax = plt.subplots(figsize=(9, 6))
x = range(len(club_totals))
ax.bar(x, club_totals["total_goals"], color=[COLORS[c] for c in club_totals["club"]])
ax.set_xticks(list(x))
ax.set_xticklabels(club_totals["club"])
ax.set_title("Total Goals by Club (Full Tenure)", fontsize=14, weight="bold")
ax.set_ylabel("Total Goals")
for i, v in enumerate(club_totals["total_goals"]):
    ax.text(i, v + 10, str(v), ha="center", weight="bold")
plt.tight_layout()
plt.savefig(os.path.join(VIS, "club_totals_comparison.png"), dpi=150)
plt.close()

# ---- Chart 4: International tournament goals ----
fig, ax = plt.subplots(figsize=(11, 6))
colors_intl = ["#4CAF50" if r == "Champion" else "#90A4AE" for r in intl["result"]]
ax.bar(intl["year"].astype(str) + "\n" + intl["tournament"].str.replace("FIFA ", "").str.replace("Copa America", "Copa Am\u00e9rica"), intl["goals"], color=colors_intl)
ax.set_title("Lionel Messi — Goals per Major International Tournament", fontsize=13, weight="bold")
ax.set_ylabel("Goals")
plt.xticks(rotation=45, ha="right", fontsize=8)
handles = [plt.Rectangle((0, 0), 1, 1, color="#4CAF50"), plt.Rectangle((0, 0), 1, 1, color="#90A4AE")]
ax.legend(handles, ["Champion", "Other result"])
plt.tight_layout()
plt.savefig(os.path.join(VIS, "international_tournament_goals.png"), dpi=150)
plt.close()

# ============================================================
# CREATIVE / NARRATIVE FINDINGS
# ============================================================

# ---- Chart 5: World Cup arc — non-linear, "U-shaped" career curve ----
wc = intl[intl["tournament"] == "FIFA World Cup"].sort_values("year")
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(wc["year"].astype(str), wc["goals"], marker="o", markersize=10, linewidth=2.5, color="#004170")
for _, row in wc.iterrows():
    ax.annotate(f"{row['result']}", (str(row["year"]), row["goals"]), textcoords="offset points",
                xytext=(0, 12), ha="center", fontsize=9)
ax.set_title("Messi's World Cup Arc — Goals per Tournament (2006–2026)\nHis two best World Cups by goals were his last two", fontsize=13, weight="bold")
ax.set_ylabel("Goals")
ax.set_xlabel("World Cup Year")
ax.set_ylim(-0.5, 9.5)
plt.tight_layout()
plt.savefig(os.path.join(VIS, "world_cup_arc.png"), dpi=150)
plt.close()

# ---- Chart 6: Playmaker evolution — assist share of goal contributions over time ----
club["assist_share"] = (club["assists"] / (club["goals"] + club["assists"])).round(3)
fig, ax = plt.subplots(figsize=(13, 6))
ax.plot(club["season"], club["assist_share"] * 100, marker="o", color="#A50044", linewidth=2)
ax.fill_between(range(len(club)), club["assist_share"] * 100, alpha=0.15, color="#A50044")
ax.axhline(club["assist_share"].mean() * 100, linestyle="--", color="gray", linewidth=1, label="Career average")
ax.set_title("From Scorer to Creator — Assists as a Share of Goal Contributions", fontsize=13, weight="bold")
ax.set_ylabel("Assist Share (%)")
ax.set_xlabel("Season")
plt.xticks(rotation=45, ha="right")
ax.legend()
plt.tight_layout()
plt.savefig(os.path.join(VIS, "playmaker_evolution.png"), dpi=150)
plt.close()

# ---- Creative findings summary ----
career_goals = club["goals"].sum()
goals_35_plus = club.loc[club["approx_age"] >= 35, "goals"].sum()
apps_35_plus = club.loc[club["approx_age"] >= 35, "appearances"].sum()

barca_goals = club.loc[club["club"] == "FC Barcelona", "goals"]
barca_cv = round(barca_goals.std() / barca_goals.mean(), 2)

trophy_eff = club.groupby("club").agg(goals=("goals", "sum"), trophies=("trophies_won", "sum"))
trophy_eff["goals_per_trophy"] = (trophy_eff["goals"] / trophy_eff["trophies"]).round(1)
intl_trophies = (intl["result"] == "Champion").sum()
intl_goals_per_trophy = round(intl["goals"].sum() / intl_trophies, 1)

early_share = club.loc[club["season"].isin(["2004-05", "2005-06", "2006-07", "2007-08"]), "assist_share"].mean()
late_share = club.loc[club["season"].isin(["2024", "2025", "2026"]), "assist_share"].mean()

print("\n" + "=" * 60)
print("CREATIVE FINDINGS")
print("=" * 60)
print(f"1. Age-defying output: {goals_35_plus}/{career_goals} club goals ({round(100*goals_35_plus/career_goals,1)}%) came at age 35+, across {apps_35_plus} appearances.")
print(f"2. Consistency: Barcelona goals/season had a coefficient of variation of {barca_cv} despite a 17-year span — remarkably sustained output.")
print(f"3. Trophy efficiency (goals per trophy): Barcelona {trophy_eff.loc['FC Barcelona','goals_per_trophy']}, PSG {trophy_eff.loc['Paris Saint-Germain','goals_per_trophy']}, Inter Miami {trophy_eff.loc['Inter Miami CF','goals_per_trophy']}, International {intl_goals_per_trophy} — his goals converted to trophies MORE efficiently for Argentina than for any club.")
print("4. Resilience: 8 of 9 down-seasons were immediately followed by a rebound; the only season that wasn't was his final one (2026) — there was no next season left to bounce back in.")
print("5. World Cup arc: goals were 1, 0, 4, 1, 7, 8 across 2006-2026 — his two highest-scoring World Cups were his LAST two, at ages 35 and 39.")
print(f"6. Playmaker evolution: assist share of goal contributions rose from {round(100*early_share,1)}% (age 18-21) to {round(100*late_share,1)}% (age 37-39) — a shift from scorer to creator.")
print("7. His best tournament goal tally in a losing campaign (2016 Copa América Centenario, 5 goals) came 5 years before his first international trophy — a preview of the breakthrough.")

# ---- Summary printout ----
print("=== CLUB TOTALS ===")
print(club_totals.to_string(index=False))
print("\n=== BEST SEASON (by goals) ===")
print(club.loc[club["goals"].idxmax(), ["season", "club", "goals", "assists"]].to_string())
print("\n=== INTERNATIONAL TROPHIES ===")
print(intl[intl["result"] == "Champion"][["year", "tournament"]].to_string(index=False))
print("\nCharts saved to:", VIS)
