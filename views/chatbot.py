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
    
    # Configura a API do Google
    client = genai.Client(api_key=google_key)
    
    if st.button("Test Gemini", width="stretch"):
    
        try:
            resposta = client.models.generate_content(
                model="gemini-3.5-flash",
                contents="Responda apenas: Gemini funcionando!"
            )
            st.success("Gemini connection successful!")
            st.write(resposta.text)
    
        except Exception as e:
            st.error("Gemini connection failed.")
            st.exception(e)

