import streamlit as st
import google.generativeai as genai
import os

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Goal Planner",
    page_icon="🎯",
    layout="wide"
)

# ==========================
# GEMINI SETUP
# ==========================

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    st.error("Gemini API Key Missing")
    st.stop()

# ==========================
# UI
# ==========================

st.title("🎯 AI Goal Planner")

st.markdown("""
Turn big goals into actionable study plans.

✅ Weekly Roadmap

✅ Daily Targets

✅ Learning Milestones

✅ Progress Strategy

✅ Study Tips
""")

st.divider()

goal = st.text_input(
    "Enter Your Goal",
    placeholder="Example: Learn Python in 30 Days"
)

duration = st.slider(
    "Duration (Days)",
    7,
    180,
    30
)

study_hours = st.slider(
    "Study Hours Per Day",
    1,
    12,
    3
)

if st.button("Generate Goal Plan"):

    if goal:

        with st.spinner("Creating Your Roadmap..."):

            prompt = f"""
            Create a detailed learning roadmap.

            Goal:
            {goal}

            Duration:
            {duration} days

            Study Hours Per Day:
            {study_hours}

            Include:

            1. Weekly roadmap
            2. Daily tasks
            3. Important milestones
            4. Recommended study strategy
            5. Common mistakes to avoid
            6. Motivation tips

            Format neatly with headings.
            """

            response = model.generate_content(
                prompt
            )

            st.success(
                "Goal Plan Generated Successfully"
            )

            st.markdown(
                response.text
            )

    else:
        st.warning(
            "Please enter a goal."
        )

st.divider()

st.info(
    "💡 Example Goals: Learn Python, Master DBMS, Crack Placement Interviews, Learn Data Structures."
)