import streamlit as st

from pathlib import Path
import base64
import time

import random

from funcoes_acesso import (
    criar_usuario_acesso,
    atualizar_nome_acesso
)

def show_initial():

    # CSS para cultar o header
    st.markdown(
        """
        <style>
        /* 1. Ocultar cabeçalho do Streamlit (Share, GitHub, etc.) */
        header[data-testid="stHeader"] {
            display: none !important;
        }
        .block-container {
            padding-top: 1.5rem !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    VERSAO_APP = st.session_state.get("versao_app", "Not available")

    criar_usuario_acesso()

    caminho_imagem = (
        Path(__file__).resolve().parent.parent
        / "images"
        / "logo_initial.jpg"
    )

    def get_base64_image(image_path):
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()

    try:
        img_b64 = get_base64_image(caminho_imagem)

        st.markdown(
            f"""
            <style>
                .stApp {{
                    background-image: url("data:image/jpeg;base64,{img_b64}");
                    background-size: cover;
                    background-position: center;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                }}
            </style>
            """,
            unsafe_allow_html=True,
        )
    except FileNotFoundError:
        st.error(f"Imagem não encontrada no caminho: {caminho_imagem}")

    # Executa somente uma vez por sessão
    if "initial_sleep_done" not in st.session_state:
        time.sleep(3)
        st.session_state["initial_sleep_done"] = True

    wine_quotes = [ 
        "Gemini is AI and can make mistakes.",
        "Every bottle tells a story.",
        "Good wine, good company, good memories.",
        "Wine is the poetry of the table.",
        "A great wine is an experience, not just a drink.",
        "Wine brings people together.",
        "Life is too short for ordinary wine.",
        "There is always a story behind a bottle.",
        "Good wine deserves good company.",
        "Discover. Taste. Remember.",
        "One bottle, many memories.",
        "Wine turns moments into memories.",
        "Every vintage has a story to tell.",
        "The best wines are the ones we remember.",
        "A bottle shared is a memory made.",
        "Wine is about place, time and people.",
        "Explore the world one bottle at a time.",
        "Sometimes the best plans begin <br>with a bottle of wine.",
        "Open a bottle, open a story.",
        "Wine makes ordinary moments memorable.",
        "Collect bottles. Create memories.",
        "Good wine is meant to be enjoyed.",
        "Behind every bottle, there is a journey."
    ]

    # CSS para transformar o st.container(border=True) no card estilizado
    st.markdown(
        """
        <style>
            div[data-testid="stVerticalBlockBorderWrapper"] {
                background: rgba(25, 12, 15, 0.82) !important;
                backdrop-filter: blur(10px) !important;
                -webkit-backdrop-filter: blur(10px) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                border-radius: 18px !important;
                padding: 10px !important;
                box-shadow: 0 8px 30px rgba(0,0,0,0.4) !important;
            }
            
            /* Cor dos textos e labels dentro do card */
            div[data-testid="stVerticalBlockBorderWrapper"] label p {
                color: #ffffff !important;
                font-weight: 500 !important;
            }
        </style>
    """,
        unsafe_allow_html=True,
    )

    if "frase_inicial" not in st.session_state:
        st.session_state["frase_inicial"] = random.choice(wine_quotes)

    frase = st.session_state["frase_inicial"]

    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.80);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 20px;
            padding: 12px 16px;
            margin: 20px auto 15px auto;
            max-width: 380px;
            text-align: center;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.12);
        ">
            <p style="
                color: #555555;
                font-size: 0.95rem;
                margin: 0;
                font-weight: 500;
            ">
                Olá! Seja Bem-vindo ao<br><br>
            </p>
            <h2 style="
                color: #1a1a1a;
                font-size: 2.25rem;
                font-weight: 700;
                margin: 0 0 8px 0;
                line-height: 0.3;
            ">
                Meus Vinhos App<br>
            </h2>
            <p style="
                color: #555555;
                font-size: 0.95rem;
                margin: 0;
                opacity: 0.80;
                font-weight: 500;
                font-style: italic;       
            ">
                "{frase}"<br><br>
            </p>
            <p style="
                color: #555555;
                font-size: 0.95rem;
                margin: 0;
                font-weight: 500;
            ">
                Versão Mobile {VERSAO_APP}<br>Desenvolvido por André Siqueira
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # CSS para criar o card de validação
    st.markdown(
        """
        <style>
        /* 2. Fundo e moldura para o bloco de validação */
        .auth-card {
            background: rgba(255, 255, 255, 0.90);
            backdrop-filter: blur(8px);
            -webkit-backdrop-filter: blur(8px);
            padding: 1.2rem 1.2rem 0.8rem 1.2rem;
            border-radius: 16px;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.12);
            margin-top: 1rem;
            margin-bottom: 1rem;
        }

        /* Input com fundo branco sólido e borda definida */
        div[data-testid="stTextInput"] input {
            background-color: #ffffff !important;
            color: #222222 !important;
            border-radius: 10px !important;
            border: 1px solid #d0d0d0 !important;
            padding: 10px 14px !important;
            font-size: 0.95rem !important;
        }

        /* 3. Destaque para o botão Continue (vinho/bordô combinando com o tema) */
        div[data-testid="stButton"] button {
            background-color: #722F37 !important; /* Tom vinho bordô */
            color: #ffffff !important;
            font-weight: 600 !important;
            border-radius: 10px !important;
            border: none !important;
            padding: 0.55rem 1rem !important;
            box-shadow: 0 2px 6px rgba(114, 47, 55, 0.35) !important;
            transition: 0.2s all ease-in-out;
        }
        div[data-testid="stButton"] button:hover {
            background-color: #581d24 !important;
            color: #ffffff !important;
        }    
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Bloco do seu código dentro do container estilizado:
    #st.markdown('<div class="auth-card">', unsafe_allow_html=True)

    nome = st.text_input(
        "Nome",
        placeholder="Digite seu nome..",
        label_visibility="collapsed",
        key="initial_nome"
    )

    if st.button("Continuar 🍷", use_container_width=True):
        nome = nome.strip()

        if not nome:
            #st.warning("Por favor digite seu nome.")
            st.stop()

        atualizar_nome_acesso(nome)

        st.session_state["nome_usuario"] = nome
        st.session_state["initial_completed"] = True

        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)