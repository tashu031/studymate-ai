import streamlit as st
import pandas as pd

st.title("📊 Analytics Dashboard")

df = pd.read_csv(
    "data/assignments.csv"
)

st.subheader(
    "Assignments By Subject"
)

subject_count = (
    df["Subject"]
    .value_counts()
)

st.bar_chart(
    subject_count
)

st.subheader(
    "Assignment Distribution"
)

st.area_chart(
    subject_count
)

st.metric(
    "Total Assignments",
    len(df)
)
