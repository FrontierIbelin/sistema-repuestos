import streamlit as st
import pandas as pd

# 1. Configuración visual
st.set_page_config(page_title="Sistema de Repuestos", layout="wide")

# 2. Aplicar color rojo y estilos (CORREGIDO)
st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #ff0000; }
    .stButton>button { background-color: #ff0000; color: white; }
    </style>
    """, unsafe_allow_html=True)

# 3. Cargar el logo
try:
    st.image("logo.png", width=250)
except:
    st.error("No se encontró el archivo logo.png")

st.title("🔴 Buscador de Repuestos")

# 4. Buscador
query = st.text_input("Busca por nombre, marca o modelo de auto:")

if query:
    st.write(f"Buscando: {query}...")
    st.info("Conexión con Google Sheets pendiente.")
else:
    st.write("Ingresa un repuesto para comenzar.")
    
