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
    
    if not google_key:
        st.error("GOOGLE_API_KEY not configured.")
        return

    try:
        client = genai.Client(api_key=google_key)
    except Exception as e:
        st.error(f"Unable to connect to AI Gemini: {e}")
        return
        
    # ============================================================
    # HISTÓRICO DO CHAT
    # ============================================================

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Exibe mensagens anteriores
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ============================================================
    # CAMPO DE PERGUNTA
    # ============================================================

    pergunta = st.chat_input(
        "Ask me anything about wine..."
    )

    if pergunta:

        # Mostra pergunta do usuário
        with st.chat_message("user"):
            st.markdown(pergunta)

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        # ========================================================
        # GEMINI
        # ========================================================

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=pergunta
            )

            resposta = response.text

        except Exception as e:

            resposta = f"Unable to generate a response: {e}"

        # ========================================================
        # RESPOSTA
        # ========================================================

        with st.chat_message("assistant"):
            st.markdown(resposta)

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": resposta
            }
        )
