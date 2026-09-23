import streamlit as st
import pandas as pd

from banco import conectar

def show_people():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 People</div>',
        unsafe_allow_html=True
    )

    st.info(
            "Who is always there when it’s time to open a bottle? 😄"
        )