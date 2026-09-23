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
    # CARREGA OS VINHOS DO BANCO
    # ============================================================

    conexao = conectar()

    query = """
        SELECT
            vin.id,
            vin.nome AS vinho,
            vi.nome AS vinicola,
            vi.pais,
            vi.regiao,
            vin.uva,
            vin.safra,
            vin.tipo,
            vin.nota,
            vin.data_vinho,
            vin.ano_vinho,
            vin.pessoas
        FROM vinhos vin
        LEFT JOIN vinicolas vi
            ON vi.id = vin.vinicola_id
        ORDER BY vin.nome
    """

    df = pd.read_sql_query(query, conexao)

    conexao.close()

    # ============================================================
    # CONVERSA
    # ============================================================

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    # Mostra mensagens anteriores
    for message in st.session_state.chat_messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # ============================================================
    # PERGUNTA DO USUÁRIO
    # ============================================================

    pergunta = st.chat_input(
        "Ask me anything about your wine collection..."
    )

    if pergunta:

        # Mostra pergunta
        st.session_state.chat_messages.append(
            {
                "role": "user",
                "content": pergunta
            }
        )

        with st.chat_message("user"):
            st.markdown(pergunta)

        # ========================================================
        # PREPARA OS DADOS PARA A IA
        # ========================================================

        dados_vinhos = df.to_string(
            index=False
        )

        prompt = f"""
You are the AI assistant for a personal wine collection.

Answer the user's question using the wine collection data
provided below.

IMPORTANT RULES:

1. Use the database information whenever the question is
   about the user's wine collection.

2. Do not invent wines, wineries, grapes, countries, dates,
   ratings or other information.

3. If the requested information is not available in the
   database, clearly say that it is not available.

4. Answer in English.

5. Be concise but useful.

6. When appropriate, organize results using bullet points
   or simple tables.

WINE COLLECTION:

{dados_vinhos}

USER QUESTION:

{pergunta}
"""

        # ========================================================
        # CHAMADA AO GEMINI
        # ========================================================

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash",
                contents=prompt
            )

            resposta = response.text

        except Exception as e:

            resposta = f"Unable to generate a response: {e}"

        # ========================================================
        # MOSTRA RESPOSTA
        # ========================================================

        with st.chat_message("assistant"):
            st.markdown(resposta)

        st.session_state.chat_messages.append(
            {
                "role": "assistant",
                "content": resposta
            }
        )
