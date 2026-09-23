import streamlit as st
import pandas as pd

import os

from banco import conectar

from google import genai

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )

    # Acessa a chave guardada nos segredos
    # google_key = st.secrets["GOOGLE_API_KEY"]
    google_key = os.getenv("GOOGLE_API_KEY")
    
    st.write(google_key)
