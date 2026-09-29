import streamlit as st
import pandas as pd

from pathlib import Path

from banco import conectar

def show_tasting_notes():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 Tasting Notes</div>',
        unsafe_allow_html=True
    )

    st.info(
            "So, what are we waiting for? Let’s learn how to do it right!"
        )

    IMAGEM = (
        Path(__file__).resolve().parent.parent
        / "images"
        / "tasting_notes.jpg"
    )

    st.image(IMAGEM)