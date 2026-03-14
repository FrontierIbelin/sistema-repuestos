import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración básica
st.set_page_config(page_title="Sistema de Repuestos", layout="wide")

st.markdown("""
    <style>
    h1, .stSelectbox label { color: #ff0000 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    st.image("logo.png", width=150)
except:
    pass

st.title("🔴 Gestión de Inventario")

# 2. Conexión a los datos
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read()
    
    # Limpiar espacios en blanco en los nombres de las columnas
    df.columns = df.columns.str.strip()
    df = df.dropna(how='all')

    # 3. INTERFAZ DE FILTROS (Solo se muestran si la columna existe)
    st.sidebar.header("🔍 Filtros")
    
    df_final = df.copy()

    # Filtro Dinámico de Marca
    if "Marca" in df.columns:
        marcas = ["Todas"] + sorted(df["Marca"].dropna().unique().tolist())
        marca_sel = st.sidebar.selectbox("Selecciona Marca", marcas)
        if marca_sel != "Todas":
            df_final = df_final[df_final["Marca"] == marca_sel]

    # Filtro Dinámico de Categoría
    if "Categoría" in df.columns:
        cats = ["Todas"] + sorted(df["Categoría"].dropna().unique().tolist())
        cat_sel = st.sidebar.selectbox("Selecciona Categoría", cats)
        if cat_sel != "Todas":
            df_final = df_final[df_final["Categoría"] == cat_sel]

    # 4. Buscador General
    busqueda = st.text_input("Busca por Código, Nombre o Ubicación:")
    if busqueda:
        mask = df_final.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_final = df_final[mask]

    # 5. Mostrar la Tabla
    st.write(f"Mostrando **{len(df_final)}** resultados")
    st.dataframe(df_final, use_container_width=True)

except Exception as e:
    st.error(f"Error de conexión o formato: {e}")
    st.info("Revisa que tu Google Sheets tenga datos y que los 'Secrets' sean correctos.")
    
