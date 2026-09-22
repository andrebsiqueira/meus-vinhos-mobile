import streamlit as st
import pandas as pd

from banco import conectar

def show_home():

    st.markdown(
        '<div class="secao">🍷 Home</div>',
        unsafe_allow_html=True
    )