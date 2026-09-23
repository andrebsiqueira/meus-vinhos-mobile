import streamlit as st
import pandas as pd

from banco import conectar

def show_my_wines():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 My Wines</div>',
        unsafe_allow_html=True
    )