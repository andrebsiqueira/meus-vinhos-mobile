import streamlit as st
import pandas as pd

from banco import conectar

def show_ocr():

    st.markdown(
        '<div class="secao">🍷 OCR</div>',
        unsafe_allow_html=True
    )