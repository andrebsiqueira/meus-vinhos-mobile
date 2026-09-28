import streamlit as st
from streamlit_option_menu import option_menu

from views.initial import show_initial
from views.home import show_home
from views.my_wines import show_my_wines
from views.wineries import show_wineries
from views.regions import show_regions
from views.people import show_people
from views.ocr import show_ocr
from views.chatbot import show_chatbot
from views.settings import show_settings

from funcoes_acesso import (
    registrar_pagina,
    buscar_nome_acesso
)

# ============================================================
# INITIAL
# ============================================================

# Cria o registro do acesso somente uma vez por sessão.
# O próprio initial.py cria o acesso e guarda o ID
# em st.session_state["acesso_id"].

if "acesso_id" not in st.session_state:
    show_initial()
    st.stop()

if not st.session_state.get("initial_completed", False):
    show_initial()
    st.stop()

# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Meus Vinhos Mobile APP",
    page_icon="🍷",
    layout="wide"
)

# ============================================================
# CSS GLOBAL
# ============================================================


# ============================================================
# RECUPERA O NOME DO USUÁRIO
# ============================================================

if "nome_usuario" not in st.session_state:

    nome = buscar_nome_acesso()

    if nome:
        st.session_state["nome_usuario"] = nome

with st.sidebar:

    selected = option_menu(
        "App Main Menu",
        [
            "Home",
            "My Wines",
            "Wineries",
            "Regions",
            "People",
            "OCR",
            "AI Chatbot",
            "Settings"
        ],
        icons=[
            "house",
            "journal-richtext",
            "building",
            "globe",
            "people",
            "search",
            "robot",
            "gear"
        ],
        menu_icon="wine",
        default_index=0
    )

# ============================================================
# PÁGINAS
# ============================================================

if selected == "Home":

    registrar_pagina("Home")
    show_home()


elif selected == "My Wines":

    registrar_pagina("My Wines")
    show_my_wines()


elif selected == "Wineries":

    registrar_pagina("Wineries")
    show_wineries()


elif selected == "Regions":

    registrar_pagina("Regions")
    show_regions()


elif selected == "People":

    registrar_pagina("People")
    show_people()


elif selected == "OCR":

    registrar_pagina("OCR")
    show_ocr()


elif selected == "AI Chatbot":

    registrar_pagina("AI Chatbot")
    show_chatbot()


elif selected == "Settings":

    registrar_pagina("Settings")
    show_settings()
