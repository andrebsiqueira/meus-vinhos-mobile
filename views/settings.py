import streamlit as st
import pandas as pd

from banco import conectar

def show_settings():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Settings</div>',
        unsafe_allow_html=True
    )