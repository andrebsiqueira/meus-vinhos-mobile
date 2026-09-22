import streamlit as st
from streamlit_option_menu import option_menu

#with st.sidebar:
#    selected = option_menu("Main Menu", ["Home", 'Settings'], 
#        icons=['house', 'gear'], menu_icon="cast", default_index=1)
#    selected

with st.sidebar:

    selected = option_menu(
        "Main Menu",
        [
            "Home",
            "My Wines",
            "Vinícolas",
            "Regiões",
            "OCR",
            "Pessoas",
            "Administração"
        ],
        icons=[
            "house",
            "journal-richtext",
            "building",
            "globe",
            "search",
            "people",
            "gear"
        ],
        menu_icon="wine",
        default_index=0
    )

st.write("Você selecionou:", selected)

if selected == "Início":
    mostrar_inicio()

elif selected == "Meus Vinhos":
    mostrar_meus_vinhos()

elif selected == "Vinícolas":
    mostrar_vinicolas()

elif selected == "Regiões":
    mostrar_regioes()

elif selected == "OCR":
    mostrar_ocr()

elif selected == "Pessoas":
    mostrar_pessoas()

elif selected == "Administração":
    mostrar_administracao()
