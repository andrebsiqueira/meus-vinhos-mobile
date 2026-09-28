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

st.markdown("""
<style>
    .block-container {
        padding-top: 1rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .titulo {
        font-size: 35px;
        font-weight: 600;
        letter-spacing: -1px;
        margin-bottom: 0;
    }

    .subtitulo {
        font-size: 18px;
        margin-bottom: 5px;
        opacity: 0.65;
    }

    .secao {
        font-size: 28px;
        font-weight: 600;
        margin-top: 35px;
        margin-bottom: 20px;
    }

    .card {
        border: 1px solid rgba(128,128,128,0.25);
        border-radius: 16px;
        padding: 22px;
        margin-bottom: 20px;
        overflow: hidden;
        overflow-wrap: break-word;
        word-break: break-word;
        height: 500px;
        background-color: #F5E6E8;
    }

    .card-texto {
        font-size: 15px;
    }

    .card-texto-obs {
        font-size: 14px;
        background-color: #F5F5F5;
    }

    .card-texto-bold {
        font-size: 18px;
        font-weight: 600;
        text-shadow: 1px 1px 1px rgba(0, 0, 0, 0.12);
    }

    .card-titulo {
        font-size: 21px;
        font-weight: 600;
        margin-bottom: 8px;
    }

    .card-info {
        font-size: 15px;
        opacity: 0.7;
        margin-bottom: 5px;
    }

    .nota {
        font-size: 18px;
        margin-top: 15px;
    }

    .hero {
        border-radius: 20px;
        padding: 25px;
        margin-bottom: 40px;
        background: linear-gradient(
            135deg,
            rgba(120,80,50,0.18),
            rgba(180,150,100,0.08)
        );
    }

    .hero-titulo {
        font-size: 36px;
        font-weight: 600;
    }

    .hero-texto {
        font-size: 18px;
        opacity: 0.7;
    }

    div[data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.2);
        padding: 20px;
        border-radius: 14px;
    }
</style>
""", unsafe_allow_html=True)

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
