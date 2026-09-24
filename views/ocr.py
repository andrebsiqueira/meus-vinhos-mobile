import streamlit as st
import pandas as pd

from google import genai

from banco import conectar

def show_ocr():

    google_key = st.secrets["G_KEY1"] + st.secrets["G_KEY2"] + st.secrets["G_KEY3"]

    st.write(google_key)

    
