import streamlit as st
import pandas as pd

from banco import conectar

from google import genai

# Acessa a chave guardada nos segredos
google_key = st.secrets["GOOGLE_API_KEY"]

#client = genai.Client(api_key=st.secrets["GOOGLE_API_KEY"])

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )
