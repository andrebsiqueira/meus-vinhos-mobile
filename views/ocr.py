import streamlit as st
import pandas as pd

from google import genai

from banco import conectar

def show_ocr():

    st.markdown(
        '<div class="secao" style="font-size: 28px;">🍷 OCR</div>',
        unsafe_allow_html=True
    )

    try: 
        google_key = ( st.secrets["G_KEY1"] + st.secrets["G_KEY2"] + st.secrets["G_KEY3"] ) 
    except Exception as e: 
        st.error(f"Error reading API Key: {e}") st.stop()

    st.write(st.secrets["G_KEY1"])

    
