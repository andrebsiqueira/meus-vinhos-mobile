import streamlit as st
import pandas as pd

from banco import conectar

def show_wineries():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Wineries & Producers</div>',
        unsafe_allow_html=True
    )