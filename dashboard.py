import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("jobs_multi.csv")
st.title("Job Scraper Dashboard")
st.dataframe(df.head(50))

company = st.selectbox("Filter by company", ["All"] + df["company"].unique().tolist())
if company != "All":
    df = df[df['company'] == company]

st.write("Count:", len(df))
fig, ax = plt.subplots()
df['company'].value_counts().head(10).plot(kind='bar', ax=ax)
st.pyplot(fig)