import streamlit as st
import pandas as pd

from banco import conectar

import google.generativeai as genai

# Acessa a chave guardada nos segredos
google_key = st.secrets["GOOGLE_API_KEY"]

# Configura a API do Google
genai.configure(api_key=google_key)

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )
