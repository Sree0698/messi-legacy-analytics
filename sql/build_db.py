import sqlite3
import pandas as pd
import os

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE, "sql", "messi_analytics.db")

club_df = pd.read_csv(os.path.join(BASE, "data", "messi_club_stats.csv"))
intl_df = pd.read_csv(os.path.join(BASE, "data", "messi_international_stats.csv"))

if os.path.exists(DB_PATH):
    os.remove(DB_PATH)

conn = sqlite3.connect(DB_PATH)
club_df.to_csv  # no-op to keep pandas import used explicitly
club_df.to_sql("club_stats", conn, index=False)
intl_df.to_sql("international_stats", conn, index=False)
conn.commit()
conn.close()
print("Database built:", DB_PATH)
