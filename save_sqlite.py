import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("jobs_multi.csv")
engine = create_engine("sqlite:///jobs.db")
df.to_sql("jobs", con=engine, if_exists="replace", index=False)
print("Saved to jobs.db (table: jobs) - rows:", len(df))