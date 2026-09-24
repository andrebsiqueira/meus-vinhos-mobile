import streamlit as st
from google import genai

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )

    st.markdown("<br>", unsafe_allow_html=True)
    
    # ============================================================
    # API KEY
    # ============================================================

    if "google_api_key" not in st.session_state:
        st.session_state.google_api_key = ""

    if "gemini_connected" not in st.session_state:
        st.session_state.gemini_connected = False

    # ============================================================ 
    # CONEXÃO COM GEMINI 
    # ============================================================ 
    
    try: 
        # Junta as 3 partes da API Key 
        google_key = ( st.secrets["G_KEY1"] + st.secrets["G_KEY2"] + st.secrets["G_KEY3"] ) 
    except Exception as e: 
        st.error(f"Unable to load Gemini API Key: {e}") 
        return 
        
    # ============================================================ 
    # CRIA CLIENTE GEMINI 
    # ============================================================ 
    
    try: 
        client = genai.Client( api_key=google_key ) 
        st.session_state.google_api_key = google_key 
        st.session_state.gemini_connected = True 
    except Exception as e: 
        st.error( f"Unable to connect to Gemini: {e}" ) 
        st.session_state.gemini_connected = False 
        
        return

    # ============================================================
    # CLIENT GEMINI
    # ============================================================

    try:

        client = genai.Client(
            api_key=st.session_state.google_api_key
        )

    except Exception as e:

        st.error(f"Unable to connect to Gemini: {e}")

        st.session_state.gemini_connected = False

        return

    # ============================================================
    # CHAT
    # ============================================================

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ============================================================
    # INPUT DO CHAT
    # ============================================================

    pergunta = st.chat_input(
        "Ask me anything about wine..."
    )

    if pergunta:

        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        with st.chat_message("user"):
            st.markdown(pergunta)

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=pergunta
            )

            resposta = response.text

        except Exception as e:

            resposta = f"Unable to generate a response: {e}"

        with st.chat_message("assistant"):
            st.markdown(resposta)

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": resposta
            }
        )
