import streamlit as st
import pandas as pd
from google import genai

from banco import conectar

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )

    # Acessa a chave guardada nos segredos
    google_key = st.secrets.get("GOOGLE_API_KEY")
