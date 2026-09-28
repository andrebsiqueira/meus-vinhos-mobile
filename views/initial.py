import streamlit as st

from funcoes_acesso import (
    criar_usuario_acesso,
    atualizar_nome_acesso
)


def show_initial():

    criar_usuario_acesso()

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 20px 10px 10px 10px;
        ">
            <h2>
                Welcome to Meus Vinhos Mobile APP 🍷
            </h2>
            <p>
                Tell us your name
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    nome = st.text_input(
        "Name",
        placeholder="Enter your name...",
        label_visibility="collapsed",
        key="initial_nome"
    )

    if st.button(
        "Continue 🍷",
        width="stretch"
    ):

        nome = nome.strip()

        if not nome:
            st.warning("Please enter your name.")
            st.stop()

        atualizar_nome_acesso(nome)

        st.session_state["nome_usuario"] = nome
        st.session_state["initial_completed"] = True

        st.rerun()