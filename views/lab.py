import streamlit as st
import pandas as pd

from banco import conectar

import base64
import os
from pathlib import Path


@st.cache_data
def get_flag_png(country_code, width=20):
    """
    Busca o arquivo .png na pasta flag_images, converte para Base64 
    e retorna a tag HTML <img> pronta.
    Exemplo de country_code: 'br', 'pt', 'ar', 'cl'
    """
    base_dir = Path(__file__).resolve().parent.parent
    file_path = base_dir / "flag_images" / f"{country_code.lower()}.png"
    
    if not file_path.exists():
        return ""
    
    with open(file_path, "rb") as f:
        data = f.read()
    
    encoded = base64.b64encode(data).decode("utf-8")
    return f'<img src="data:image/png;base64,{encoded}" width="{width}" style="vertical-align: middle; border-radius: 2px; margin-right: 6px;">'

def render_winery_card(nome, pais, sigla_pais, total_vinhos):
    # Puxa a tag HTML da bandeira local (.png)
    bandeira_html = get_flag_png(sigla_pais, width=18)
    
    card_html = f"""
    <div style="
        background: #ffffff;
        border: 1px solid #eee;
        border-radius: 12px;
        padding: 12px 16px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 6px rgba(0,0,0,0.04);
    ">
        <div style="flex-grow: 1;">
            <div style="font-weight: 600; font-size: 15px; color: #1a1a1a; margin-bottom: 3px;">
                {nome}
            </div>
            <div style="font-size: 13px; color: #666; display: flex; align-items: center;">
                {bandeira_html}<span>{pais}</span> &nbsp;•&nbsp; <span>Serra Gaúcha</span>
            </div>
        </div>
        <div style="
            background-color: #6A1B29;
            color: white;
            font-size: 11px;
            font-weight: 600;
            padding: 4px 8px;
            border-radius: 20px;
        ">
            {total_vinhos} wines
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def show_lab():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">💡 LAB</div>',
        unsafe_allow_html=True
    )

    st.info(
            "A space to experiment, test and explore new features."
        )

    caminho = Path(__file__).resolve().parent / "flag_images" / "br.png"

    # Testando:
    render_winery_card("Adega Cartuxa", "Portugal", "pt", 2)
    render_winery_card("Adolfo Lona", "Brasil", "br", 2)
    render_winery_card("Catena Zapata", "Argentina", "ar", 5)


    # -----------------------------------------------------
    # CARD CLICÁVEL DA VINÍCOLA
    # -----------------------------------------------------

    # Puxa a tag da bandeira em PNG (usando a função de base64 criada)
    bandeira_html = get_flag_png("BR", width=18)

    # Cria o card com borda nativa arredondada
    with st.container(border=True):
        # Renderiza o visual do card com nome, bandeira e informações
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <div>
                    <div style="font-weight: 600; font-size: 20px; color: #1a1a1a;">
                        Miolo
                    </div>
                    <div style="font-size: 15px; color: #666; display: flex; align-items: center; margin-top: 2px;">
                        {bandeira_html} <span>Brasil</span> &nbsp;•&nbsp; <span>Serra Gaúcha</span>
                    </div>
                </div>
                <div style="
                    background-color: #6A1B29;
                    color: white;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 4px 8px;
                    border-radius: 20px;
                    white-space: nowrap;
                ">
                    15 wines
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # CSS customizado para o botão "Ver vinícola"
        st.markdown("""
        <style>
            /* Estiliza o botão dentro do card */
            div[data-testid="stVerticalBlock"] div.stButton > button {
                background-color: #6A1B29 !important; /* Cor de fundo (ex: bordô) */
                color: #ffffff !important;           /* Cor do texto (branco) */
                border: none !important;             /* Remove a borda padrão */
                border-radius: 8px !important;       /* Cantos arredondados */
                font-weight: 500 !important;
                font-size: 14px !important;
                padding: 6px 12px !important;
                transition: opacity 0.2s ease, transform 0.1s ease;
            }

            /* Efeito ao passar o mouse ou tocar */
            div[data-testid="stVerticalBlock"] div.stButton > button:hover,
            div[data-testid="stVerticalBlock"] div.stButton > button:active {
                opacity: 0.9 !important;
                transform: scale(0.99);
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Botão de ação direta dentro do card
        if st.button("Ver vinícola ›", key=f"btn_vinicola_32", use_container_width=True):
            st.session_state["vinicola_selecionada"] = 32
            st.rerun()

    # -----------------------------------------------------
    # CARD CLICÁVEL DA VINÍCOLA
    # -----------------------------------------------------

    # Puxa a tag da bandeira em PNG (usando a função de base64 criada)
    bandeira_html = get_flag_png("CA", width=18)

    # Cria o card com borda nativa arredondada
    with st.container(border=True):
        # Renderiza o visual do card com nome, bandeira e informações
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px;">
                <div>
                    <div style="font-weight: 600; font-size: 20px; color: #1a1a1a;">
                        Henry of Pelham Family Estate Winery
                    </div>
                    <div style="font-size: 15px; color: #666; display: flex; align-items: center; margin-top: 2px;">
                        {bandeira_html} <span>Canada</span> &nbsp;•&nbsp; <span>Ontario</span>
                    </div>
                </div>
                <div style="
                    background-color: #6A1B29;
                    color: white;
                    font-size: 15px;
                    font-weight: 600;
                    padding: 4px 8px;
                    border-radius: 20px;
                    white-space: nowrap;
                ">
                    2 wines
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

        # CSS customizado para o botão "Ver vinícola"
        st.markdown("""
        <style>
            /* Estiliza o botão dentro do card */
            div[data-testid="stVerticalBlock"] div.stButton > button {
                background-color: #6A1B29 !important; /* Cor de fundo (ex: bordô) */
                color: #ffffff !important;           /* Cor do texto (branco) */
                border: none !important;             /* Remove a borda padrão */
                border-radius: 8px !important;       /* Cantos arredondados */
                font-weight: 500 !important;
                font-size: 14px !important;
                padding: 6px 12px !important;
                transition: opacity 0.2s ease, transform 0.1s ease;
            }

            /* Efeito ao passar o mouse ou tocar */
            div[data-testid="stVerticalBlock"] div.stButton > button:hover,
            div[data-testid="stVerticalBlock"] div.stButton > button:active {
                opacity: 0.9 !important;
                transform: scale(0.99);
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Botão de ação direta dentro do card
        if st.button("Ver vinícola ›", key=f"btn_vinicola_33", use_container_width=True):
            st.session_state["vinicola_selecionada"] = 33
            st.rerun()