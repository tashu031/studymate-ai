import streamlit as st
import google.generativeai as genai
import os

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Notes Generator",
    page_icon="📚",
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

st.title("📚 AI Notes Generator")

st.markdown("""
Generate exam-ready notes instantly.

✅ Short Notes

✅ Important Definitions

✅ Key Concepts

✅ Interview Questions

✅ Exam Tips
""")

st.divider()

topic = st.text_input(
    "Enter Topic",
    placeholder="Example: DBMS Normalization"
)

difficulty = st.selectbox(
    "Difficulty Level",
    [
        "Beginner",
        "Intermediate",
        "Advanced"
    ]
)

if st.button("Generate Notes"):

    if topic:

        with st.spinner("Generating Notes..."):

            prompt = f"""
            Create complete study notes for:

            Topic: {topic}

            Level: {difficulty}

            Include:

            1. Introduction
            2. Important Definitions
            3. Key Concepts
            4. Examples
            5. Interview Questions
            6. Exam Tips
            7. Quick Revision Summary

            Format properly using headings.
            """

            response = model.generate_content(prompt)

            st.success("Notes Generated Successfully")

            st.markdown(response.text)

    else:
        st.warning("Please enter a topic")
st.divider()

st.info(
    "💡 Pro Tip: Generate notes before exams and use Quick Revision Summary for last-minute preparation."
)