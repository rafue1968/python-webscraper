import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("jobs_multi.csv")

df["title"] = df["title"].str.strip()
df["company"] = df["company"].str.strip()
df["location"] = df["location"].str.strip()


print("Total rows:", len(df))
print("Top 10 companies:\n", df["company"].value_counts().head(10))

top5 = df["company"].value_counts().head(5)
fig = top5.plot(kind="bar", rot=45).get_figure()
fig.tight_layout()
fig.savefig("top_companies.png")
print("Saved top_companies.png")
plt.show()