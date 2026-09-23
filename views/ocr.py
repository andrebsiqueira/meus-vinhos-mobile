import streamlit as st
from google import genai

def show_ocr():

    st.markdown(
        "<div class='secao'>🤖 AI Assistant</div>",
        unsafe_allow_html=True
    )

    try:
        client = genai.Client()

    except Exception as e:
        st.error(f"Unable to connect to Gemini: {e}")
        return
