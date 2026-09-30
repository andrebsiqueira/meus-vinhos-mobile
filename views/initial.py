import streamlit as st

from pathlib import Path
import base64

from funcoes_acesso import (
    criar_usuario_acesso,
    atualizar_nome_acesso
)

def show_initial():

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

    st.markdown(
        f"""
        <div style="
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(12px);
            -webkit-backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.6);
            border-radius: 20px;
            padding: 24px 20px;
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
                Olá, seja Bem-vindo ao<br>
            </p>
            <h2 style="
                color: #1a1a1a;
                font-size: 2.25rem;
                font-weight: 700;
                margin: 0 0 8px 0;
                line-height: 1.3;
            ">
                Meus Vinhos App<br>
            </h2>
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

    nome = st.text_input(
        "Name",
        placeholder="Digite seu nome para validar o acesso..",
        label_visibility="collapsed",
        key="initial_nome"
    )

    if st.button(
        "Continue 🍷",
        width="stretch"
    ):

        nome = nome.strip()

        if not nome:
            st.warning("Por favor digite seu nome.")
            st.stop()

        atualizar_nome_acesso(nome)

        st.session_state["nome_usuario"] = nome
        st.session_state["initial_completed"] = True

        st.rerun()