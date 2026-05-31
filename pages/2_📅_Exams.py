import streamlit as st
import pandas as pd

st.title("📝 Exams")

exam_df = pd.read_csv(
    "data/exams.csv"
)

st.dataframe(
    exam_df,
    use_container_width=True
)
