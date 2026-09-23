import streamlit as st
import pandas as pd

from banco import conectar

from google import genai

# Acessa a chave guardada nos segredos
google_key = st.secrets["GOOGLE_API_KEY"]

# Configura a API do Google
client = genai.Client(api_key=google_key)

resposta = client.models.generate_content(
    model="gemini-3.3-flash",
    contents="Qual é a principal uva utilizada no vinho Malbec argentino?"
)

st.write(resposta.text)

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )
