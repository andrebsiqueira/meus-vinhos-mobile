import streamlit as st
import pandas as pd

from google import genai

from banco import conectar

def show_ocr():

    st.write(st.secrets["G_KEY1"])

    
