import streamlit as st

from funcoes_acesso import (
    criar_usuario_acesso,
    atualizar_nome_acesso
)


# ============================================================
# TELA INITIAL
# ============================================================

def show_initial():

    # --------------------------------------------------------
    # Cria o registro do acesso
    # --------------------------------------------------------

    criar_usuario_acesso()


    # --------------------------------------------------------
    # Tela de apresentação
    # --------------------------------------------------------

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 20px 10px 10px 10px;
        ">
            <div style="font-size: 50px;">
                🍷
            </div>
            <h2>
                Welcome to Meus Vinhos
            </h2>
            <p>
                Tell us your name
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # Nome
    # --------------------------------------------------------

    nome = st.text_input(
        "Name",
        placeholder="Enter your name...",
        label_visibility="collapsed",
        key="initial_nome"
    )


    # --------------------------------------------------------
    # Botões
    # --------------------------------------------------------

    col1, col2 = st.columns(2)


    # ========================================================
    # CONTINUE
    # ========================================================

    with col1:

        if st.button(
            "Continue 🍷",
            width="stretch"
        ):

            nome = nome.strip()

            if nome:

                atualizar_nome_acesso(nome)

            st.session_state["initial_completed"] = True

            st.rerun()


    # ========================================================
    # SKIP
    # ========================================================

    with col2:

        if st.button(
            "Skip",
            width="stretch"
        ):

            st.session_state["initial_completed"] = True

            st.rerun()