import streamlit as st
from google import genai

def show_chatbot():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 AI Chatbot</div>',
        unsafe_allow_html=True
    )

    # ============================================================
    # API KEY
    # ============================================================

    if "google_api_key" not in st.session_state:
        st.session_state.google_api_key = ""

    if "gemini_connected" not in st.session_state:
        st.session_state.gemini_connected = False

    # ============================================================
    # FORMULÁRIO DA API KEY
    # ============================================================

    if not st.session_state.gemini_connected:

        st.markdown("### 🔑 Connect to Gemini")

        st.write(
            "Enter your Google Gemini API Key to start the AI Chatbot."
        )

        st.markdown("<br>", unsafe_allow_html=True)
        
        with st.form("api_key_form"):

            api_key = st.text_input(
                "Google Gemini API Key",
                type="password",
                placeholder="Enter your API Key..."
            )

            conectar = st.form_submit_button(
                "🔗 Connect to Gemini",
                width="stretch"
            )

            if conectar:

                if not api_key.strip():

                    st.error("Please enter your API Key.")

                else:

                    try:

                        client = genai.Client(
                            api_key=api_key.strip()
                        )

                        # Guarda a chave somente na sessão atual
                        st.session_state.google_api_key = api_key.strip()

                        st.session_state.gemini_connected = True

                        st.rerun()

                    except Exception as e:

                        st.error(
                            f"Unable to connect to Gemini: {e}"
                        )

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
