import streamlit as st
import pandas as pd
from datetime import date
import google.generativeai as genai
import os


GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.5-flash")


st.title("📚 StudyMate AI Dashboard")

# -----------------------
# ASSIGNMENTS
# -----------------------

df = pd.read_csv("assignments.csv")

st.subheader("➕ Add New Assignment")

subject = st.text_input("Subject")
task = st.text_input("Task")
due_date = st.date_input("Due Date")

if st.button("Add Assignment"):

    new_row = pd.DataFrame({
        "Subject":[subject],
        "Task":[task],
        "DueDate":[due_date]
    })

    df = pd.concat([df,new_row], ignore_index=True)

    df.to_csv("assignments.csv", index=False)

    st.success("Assignment Added!")

# -----------------------
# PRIORITY SYSTEM
# -----------------------

df = pd.read_csv("assignments.csv")

today = pd.to_datetime(date.today())
df["DueDate"] = pd.to_datetime(df["DueDate"])

df["Days Left"] = (df["DueDate"] - today).dt.days

def get_priority(days):

    if days <= 2:
        return "🔴 High"

    elif days <= 5:
        return "🟡 Medium"

    else:
        return "🟢 Low"

df["Priority"] = df["Days Left"].apply(get_priority)

st.subheader("📋 Assignments")

st.dataframe(df)

# -----------------------
# MOST URGENT TASK
# -----------------------

urgent_task = df.sort_values("Days Left").iloc[0]

st.warning(
    f"⚠️ Most Urgent Task: {urgent_task['Task']} "
    f"({urgent_task['Days Left']} days left)"
)

st.subheader("🤖 AI Study Recommendation")

if st.button("What Should I Study Today?"):

    prompt = f"""
    You are a study planning assistant.

    Here are my assignments:

    {df.to_string(index=False)}

    Based on priority and due dates:

    1. Tell me what I should study first.
    2. Tell me what can wait.
    3. Give me a study plan for today.
    """

    if urgent_task["Priority"] == "🔴 High":
        recommendation = f"""
        Focus on {urgent_task['Task']} first.
        
        It has the highest priority and only
        {urgent_task['Days Left']} day(s) left.

        After completing it, move to the next
        medium-priority assignments.
        """
else:
    recommendation = """
    No urgent assignments today.

    Focus on medium-priority tasks and start
    preparing for upcoming exams.
    """

st.success(recommendation)
# -----------------------
# EXAMS
# -----------------------

exam_df = pd.read_csv("exams.csv")

st.subheader("📝 Upcoming Exams")

st.dataframe(exam_df)