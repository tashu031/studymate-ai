import streamlit as st
import google.generativeai as genai
import os

st.title("🤖 AI Mentor")

api_key = os.getenv("GEMINI_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-2.5-flash")
else:
    model = None

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):
        st.markdown(
            msg["content"]
        )

prompt = st.chat_input(
    "Ask your study question..."
)

if prompt:

    st.session_state.messages.append(
        {
            "role":"user",
            "content":prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    if model is None:
        st.error("AI is not configured (missing GEMINI_API_KEY).")
    else:
        response = model.generate_content(
            prompt
        )

        answer = response.text

        with st.chat_message(
            "assistant"
        ):
            st.markdown(answer)

        st.session_state.messages.append(
            {
                "role":"assistant",
                "content":answer
            }
        )


# =====================================
# AI QUIZ GENERATOR
# =====================================

st.divider()

st.subheader("🧠 AI Quiz Generator")

topic = st.text_input(
    "Enter Topic for Quiz"
)

if st.button(
    "Generate Quiz"
):

    try:

        quiz_prompt = f"""
        Create a quiz on:

        {topic}

        Requirements:

        1. Generate 5 MCQs
        2. Each question should have 4 options
        3. Show the correct answer
        4. Make it suitable for college students
        """

        if model is None:
            st.error("AI is not configured (missing GEMINI_API_KEY).")
        else:
            quiz_response = model.generate_content(
                quiz_prompt
            )

            st.markdown(
                quiz_response.text
            )

    except Exception as e:

        st.error(
            f"Quiz Generator Error: {e}"
        )
