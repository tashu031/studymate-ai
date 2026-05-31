import streamlit as st
import pandas as pd
from datetime import date

st.title("📚 Assignments")

df = pd.read_csv("data/assignments.csv")

today = pd.to_datetime(date.today())

if "DueDate" in df.columns:
    df["DueDate"] = pd.to_datetime(df["DueDate"])
else:
    df["DueDate"] = pd.NaT

if not df.empty:
    df["Days Left"] = (df["DueDate"] - today).dt.days
else:
    df["Days Left"] = pd.Series(dtype="int64")


def get_priority(days):
    if days < 0:
        return "🔴 Overdue"
    if days <= 2:
        return "🔴 High"
    elif days <= 5:
        return "🟡 Medium"
    else:
        return "🟢 Low"

if not df.empty:
    df["Priority"] = df["Days Left"].apply(get_priority)
    df["Status"] = df["Days Left"].apply(
        lambda days: "Overdue" if days < 0 else ("Due Today" if days == 0 else "Upcoming")
    )
else:
    df["Priority"] = pd.Series(dtype="string")
    df["Status"] = pd.Series(dtype="string")

active_df = df[df["Status"] != "Overdue"].copy()
overdue_df = df[df["Status"] == "Overdue"].copy()

st.subheader("Active Assignments")
if not active_df.empty:
    st.dataframe(active_df, use_container_width=True)
else:
    st.info("No active assignments. Add one below!")

if not overdue_df.empty:
    st.subheader("⚠️ Overdue Assignments")
    st.warning("These assignments are past their due date.")
    st.dataframe(overdue_df, use_container_width=True)

st.subheader("➕ Add Assignment")

subject = st.text_input("Subject")
task = st.text_input("Task")
due_date = st.date_input("Due Date")

if st.button("Add Assignment"):
    if subject.strip() == "" or task.strip() == "":
        st.error("Please enter both Subject and Task.")
    else:
        if due_date < date.today():
            st.warning("This assignment is already overdue. It will appear in the overdue section.")

        new_row = pd.DataFrame({
            "Subject": [subject],
            "Task": [task],
            "DueDate": [due_date]
        })

        df = pd.concat([df, new_row], ignore_index=True)
        df.to_csv("data/assignments.csv", index=False)
        st.success("✅ Assignment added successfully.")
        st.experimental_rerun()

st.subheader("🗑 Delete Assignment")
if not df.empty:
    delete_options = df.apply(
        lambda row: f"{row.name}|{row['Subject']} - {row['Task']} ({row['DueDate'].date()})",
        axis=1
    ).tolist()
    delete_selection = st.selectbox("Select Assignment to delete", delete_options)

    if st.button("Delete Assignment"):
        delete_index = int(delete_selection.split("|", 1)[0])
        df = df[df.index != delete_index]
        df.to_csv("data/assignments.csv", index=False)
        st.success("✅ Assignment deleted.")
        st.experimental_rerun()
else:
    st.info("No assignments to delete.")
