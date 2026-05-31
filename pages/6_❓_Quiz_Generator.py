import streamlit as st
import google.generativeai as genai
import os

# ==========================
# PAGE CONFIG
# ==========================

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="❓",
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

st.title("❓ AI Quiz Generator")

st.markdown("""
Test your knowledge instantly.

✅ MCQs

✅ Correct Answers

✅ Difficulty Selection

✅ Exam Preparation
""")

st.divider()

topic = st.text_input(
    "Enter Topic",
    placeholder="Example: Python OOP"
)

difficulty = st.selectbox(
    "Difficulty",
    [
        "Easy",
        "Medium",
        "Hard"
    ]
)

num_questions = st.slider(
    "Number of Questions",
    5,
    20,
    10
)

if st.button("Generate Quiz"):

    if topic:

        with st.spinner("Creating Quiz..."):

            prompt = f"""
            Create a quiz on:

            Topic: {topic}

            Difficulty: {difficulty}

            Number of Questions:
            {num_questions}

            Requirements:

            1. Multiple Choice Questions
            2. Four options for each question
            3. Show correct answer below each question
            4. Format clearly
            """

            response = model.generate_content(
                prompt
            )

            st.success(
                "Quiz Generated Successfully"
            )

            st.markdown(
                response.text
            )

    else:
        st.warning(
            "Please enter a topic"
        )

st.divider()

st.info(
    "💡 Tip: Generate notes first, then test yourself with a quiz."
)