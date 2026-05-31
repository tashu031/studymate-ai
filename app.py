import streamlit as st
import pandas as pd
from datetime import date
import google.generativeai as genai
import os
import random


# =====================================
# PAGE CONFIG
# =====================================

st.set_page_config(
    page_title="StudyMate AI Pro",
    page_icon="🎓",
    layout="wide"
)

dark_mode = st.checkbox("🌙 Dark Mode")


# =====================================
# GEMINI CONFIG
# =====================================

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
gemini_enabled = bool(GEMINI_API_KEY)

if not gemini_enabled:
    st.warning("❌ GEMINI_API_KEY not found — AI features disabled")
else:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel("gemini-2.5-flash")

# =====================================
# LOAD DATA
# =====================================

df = pd.read_csv("data/assignments.csv")
exam_df = pd.read_csv("data/exams.csv")

# Compute due dates and priority early so sidebar metrics can use them
today = pd.to_datetime(date.today())

df["DueDate"] = pd.to_datetime(df["DueDate"])

df["Days Left"] = (
    df["DueDate"] - today
).dt.days

def get_priority(days):

    if days <= 2:
        return "🔴 High"

    elif days <= 5:
        return "🟡 Medium"

    else:
        return "🟢 Low"

df["Priority"] = df["Days Left"].apply(
    get_priority
)

# Precompute KPI metrics so sidebar can reference them
total_assignments = len(df)
upcoming_exams = len(exam_df)
urgent_tasks = len(
    df[df["Days Left"] <= 3]
)

productivity_score = max(
    0,
    100 - urgent_tasks * 10
)

# =====================================
# HEADER
# =====================================

with st.sidebar:

    st.image(
        "https://cdn-icons-png.flaticon.com/512/3135/3135755.png",
        width=120
    )

    st.title("StudyMate AI")

    st.success(
        "🎓 Student Productivity Platform"
    )

    st.markdown("---")

    st.info(
        "Manage Assignments\n\nTrack Exams\n\nGet AI Guidance"
    )
    st.markdown("---")

    st.success("🟢 Student Mode Active")

    st.metric(
        "🔥 Study Streak",
        st.session_state.get("streak", 0)
    )

    st.metric(
        "⚡ Productivity",
        f"{productivity_score}%"
    )
  
st.markdown("""
<div style="
padding:30px;
border-radius:20px;
background:linear-gradient(90deg,#2563eb,#7c3aed);
color:white;
margin-bottom:20px;
">

<h1>🎓 StudyMate AI Pro</h1>

<h3>
Your Personal AI Academic Assistant
</h3>

<p>
📚 Assignment Tracking &nbsp;&nbsp;|
📝 Exam Management &nbsp;&nbsp;|
🤖 AI Mentor &nbsp;&nbsp;|
📈 Analytics &nbsp;&nbsp;|
🎯 Goal Planning
</p>

</div>
""", unsafe_allow_html=True)
st.divider()

# (Assignment priority computed earlier after loading data)

# =====================================
# KPI CARDS
# =====================================

# =====================================
# KPI CARDS + PRODUCTIVITY
# =====================================

# total_assignments = len(df)

# upcoming_exams = len(exam_df)

# urgent_tasks = len(
#     df[df["Days Left"] <= 3]
# )

# productivity_score = max(
#     0,
#     100 - urgent_tasks * 10
# )

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "📚 Assignments",
        total_assignments
    )

with col2:
    st.metric(
        "📝 Exams",
        upcoming_exams
    )

with col3:
    st.metric(
        "⚠️ Urgent",
        urgent_tasks
    )

with col4:
    st.metric(
        "⚡ Productivity",
        f"{productivity_score}%"
    )

# =====================================
# WELCOME CARD
# =====================================

st.info(
    f"""
    👋 Welcome Back!

    📚 Assignments: {total_assignments}

    📝 Upcoming Exams: {upcoming_exams}

    ⚠️ Urgent Tasks: {urgent_tasks}

    ⚡ Productivity Score: {productivity_score}%

    Keep pushing forward. Every study session counts!
    """
)

# =====================================
# QUICK OVERVIEW
# =====================================

st.subheader("📊 Quick Overview")

col1, col2 = st.columns(2)

with col1:

    st.markdown("### 📚 Recent Assignments")

    st.dataframe(
        df[
            ["Subject", "Task", "Priority"]
        ].head(5),
        use_container_width=True
    )

with col2:

    st.markdown("### 📝 Upcoming Exams")

    st.dataframe(
        exam_df.head(5),
        use_container_width=True
    )

st.divider()

# =====================================
# PRODUCTIVITY SCORE
# =====================================

st.subheader("⚡ Productivity Score")

st.progress(productivity_score)

st.success(
    f"Current Productivity Score: {productivity_score}/100"
)
# =====================================
# STUDY STREAK
# =====================================

st.subheader("🔥 Study Streak")

if "streak" not in st.session_state:
    st.session_state.streak = 0

if st.button("✅ Mark Study Session Complete"):
    st.session_state.streak += 1

st.success(
    f"Current Study Streak: {st.session_state.streak} Days"
)


# =====================================
# CHARTS
# =====================================

st.subheader("📈 Analytics")

col1, col2 = st.columns(2)

with col1:

    priority_counts = (
        df["Priority"]
        .value_counts()
    )

    st.bar_chart(priority_counts)

with col2:

    st.line_chart(
        df["Days Left"]
    )

# =====================================
# ADD NEW ASSIGNMENT
# =====================================

st.subheader("➕ Add New Assignment")

subject = st.text_input("Subject")

task = st.text_input("Task")

due_date = st.date_input("Due Date")

if st.button("Add Assignment"):

    new_row = pd.DataFrame({
        "Subject": [subject],
        "Task": [task],
        "DueDate": [due_date]
    })

    updated_df = pd.concat(
        [df, new_row],
        ignore_index=True
    )

    updated_df.to_csv(
        "data/assignments.csv",
        index=False
    )

    st.success(
        "✅ Assignment Added Successfully!"
    )

    st.rerun()

st.divider()

# =====================================
# ASSIGNMENT TABLE
# =====================================

st.subheader("📋 Assignment Dashboard")

st.dataframe(
    df,
    use_container_width=True
)


st.subheader("🏆 Achievements")

if total_assignments >= 5:

    st.success(
        "🏅 Assignment Master"
    )

if total_assignments >= 10:

    st.success(
        "🥇 Productivity Hero"
    )

if urgent_tasks == 0:

    st.success(
        "🚀 All Tasks Under Control"
    )


quotes = [
    "Success is built daily.",
    "Small progress is still progress.",
    "Consistency beats motivation.",
    "Study hard today for a better tomorrow.",
    "Every chapter completed is a victory."
]

st.info(random.choice(quotes))

csv = df.to_csv(index=False)

st.download_button(
    "📥 Download Assignment Report",
    csv,
    file_name="study_report.csv",
    mime="text/csv"
)
st.subheader("📈 Semester Progress")

progress = min(
    total_assignments * 10,
    100
)

st.progress(progress)

st.write(
    f"{progress}% Complete"
)

# =====================================
# MOST URGENT TASK
# =====================================

if len(df) > 0:

    urgent_task = (
        df.sort_values("Days Left")
        .iloc[0]
    )

    st.warning(
        f"⚠️ Most Urgent Task: "
        f"{urgent_task['Task']} "
        f"({urgent_task['Days Left']} day(s) left)"
    )

# =====================================
# AI RECOMMENDATION
# =====================================

st.subheader(
    "🤖 AI Study Recommendation"
)

if st.button(
    "What Should I Study Today?"
):

    try:

        prompt = f"""
        You are an expert academic mentor.

        Assignments:

        {df.to_string(index=False)}

        Exams:

        {exam_df.to_string(index=False)}

        Provide:

        1. Priority ranking
        2. Today's study plan
        3. Weekly study plan
        4. Productivity tips
        5. Exam preparation strategy
        6. Motivation message
        """

        if not gemini_enabled:
            st.error("AI features are disabled (GEMINI_API_KEY missing).")
        else:
            response = model.generate_content(
                prompt
            )

            st.success(
                response.text
            )

    except Exception as e:

        st.error(
            f"Gemini Error: {e}"
        )

st.divider()
# =====================================
# AI TIMETABLE GENERATOR
# =====================================

st.subheader("📅 AI Study Timetable Generator")

study_hours = st.slider(
    "Available Study Hours Today",
    min_value=1,
    max_value=12,
    value=4
)

if st.button("Generate Timetable"):

    try:

        timetable_prompt = f"""
        You are an expert study planner.

        Available study hours:
        {study_hours}

        Assignments:

        {df.to_string(index=False)}

        Exams:

        {exam_df.to_string(index=False)}

        Create:

        1. Hour-by-hour study timetable
        2. Prioritize urgent assignments
        3. Prioritize upcoming exams
        4. Include short breaks
        5. Give study tips for the day
        """

        if not gemini_enabled:
            st.error("AI features are disabled (GEMINI_API_KEY missing).")
        else:
            timetable_response = model.generate_content(
                timetable_prompt
            )

            st.success(
                timetable_response.text
            )

    except Exception as e:

        st.error(
            f"Timetable Generator Error: {e}"
        )

# =====================================
# EXAM COUNTDOWN
# =====================================

st.subheader("⏳ Exam Countdown")

for _, row in exam_df.iterrows():

    exam_date = pd.to_datetime(
        row["ExamDate"]
    )

    days_left = (
        exam_date - pd.Timestamp.today()
    ).days

    st.info(
        f"📖 {row['Subject']} : "
        f"{days_left} days left"
    )


st.subheader(
    "🎯 Exam Readiness"
)

readiness = max(
    0,
    100 - urgent_tasks * 10
)

st.progress(readiness)

st.write(
    f"Readiness Score: {readiness}%"
)
# =====================================
# UPCOMING EXAMS
# =====================================

st.subheader("📝 Upcoming Exams")

st.dataframe(
    exam_df,
    use_container_width=True
)

# =====================================
# FOOTER
# =====================================

st.markdown("---")

st.markdown(
"""
### 🚀 StudyMate AI Pro

Built with:
- Streamlit
- Gemini AI
- Data Analytics
- Productivity Tracking

Designed for students.
"""
)