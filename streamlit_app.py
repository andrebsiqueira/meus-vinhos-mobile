import streamlit as st
from streamlit_option_menu import option_menu

from views.home import show_home
from views.my_wines import show_my_wines
from views.wineries import show_wineries
from views.regions import show_regions
from views.ocr import show_ocr
from views.people import show_people
from views.settings import show_settings

with st.sidebar:

    selected = option_menu(
        "Main Menu",
        [
            "Home",
            "My Wines",
            "Wineries",
            "Regions",
            "OCR",
            "People",
            "Settings"
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

#st.write("You selected:", selected)

if selected == "Home":
    show_home()

elif selected == "My Wines":
    show_my_wines()

elif selected == "Wineries":
    show_wineries()

elif selected == "Regions":
    show_regions()

elif selected == "OCR":
    show_ocr()

elif selected == "People":
    show_people()

elif selected == "Settings":
    show_settings()
    
