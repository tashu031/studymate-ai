import streamlit as st
import google.generativeai as genai
import os

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="Exam Roadmap Generator",
    page_icon="🗺️",
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

st.title("🗺️ AI Exam Roadmap Generator")

st.markdown("""
Generate a personalized exam preparation roadmap.

✅ Day-wise Plan

✅ Important Topics

✅ Revision Schedule

✅ Smart Time Allocation

✅ Final Revision Strategy
""")

st.divider()

subject = st.text_input(
    "Subject",
    placeholder="Example: DBMS"
)

days_left = st.slider(
    "Days Remaining Until Exam",
    1,
    60,
    15
)

level = st.selectbox(
    "Current Preparation Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

if st.button("Generate Exam Roadmap"):

    if subject:

        with st.spinner("Preparing Your Roadmap..."):

            prompt = f"""
            Create a detailed exam roadmap.

            Subject:
            {subject}

            Days Left:
            {days_left}

            Current Level:
            {level}

            Include:

            1. Day-by-day study plan
            2. Important topics
            3. Revision schedule
            4. Mock test strategy
            5. Final 2-day revision plan
            6. Exam day tips

            Format with headings and day numbers.
            """

            response = model.generate_content(prompt)

            st.success(
                "Roadmap Generated Successfully"
            )

            st.markdown(response.text)

    else:
        st.warning(
            "Please enter a subject."
        )

st.divider()

st.info(
    "💡 Example: DBMS, Python, Operating Systems, Computer Networks, Java."
)