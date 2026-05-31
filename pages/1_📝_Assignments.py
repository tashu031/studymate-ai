import streamlit as st
import pandas as pd

st.title("📚 Assignments")

df = pd.read_csv("data/assignments.csv")

st.dataframe(
    df,
    use_container_width=True
)

st.subheader("➕ Add Assignment")

subject = st.text_input("Subject")
task = st.text_input("Task")
due_date = st.date_input("Due Date")

if st.button("Add Assignment"):

    new_row = pd.DataFrame({
        "Subject":[subject],
        "Task":[task],
        "DueDate":[due_date]
    })

    df = pd.concat(
        [df,new_row],
        ignore_index=True
    )

    df.to_csv(
        "data/assignments.csv",
        index=False
    )

    st.success("Assignment Added")
