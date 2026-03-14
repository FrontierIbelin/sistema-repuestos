import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de pantalla ancha
st.set_page_config(page_title="Sistema de Repuestos", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #ffffff; }
    h1 { color: #d32f2f; font-size: 28px; font-weight: bold; }
    .stSelectbox label { color: #d32f2f; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

try:
    st.image("logo.png", width=120)
except:
    pass

st.title("➕ Buscador de Repuestos")

# 2. Conexión
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read().dropna(how='all')

# 3. FILTROS EN LA PARTE SUPERIOR
col1, col2, col3, col4 = st.columns(4)

with col1:
    marcas = ["Seleccione..."] + sorted(df["Marca Prod"].dropna().unique().tolist()) if "Marca Prod" in df.columns else ["Seleccione..."]
    marca_sel = st.selectbox("Marca Prod", marcas)

with col2:
    cats = ["Seleccione..."] + sorted(df["Categoría"].dropna().unique().tolist()) if "Categoría" in df.columns else ["Seleccione..."]
    cat_sel = st.selectbox("Categoría", cats)

with col3:
    tiendas = ["Seleccione..."] + sorted(df["Tienda"].dropna().unique().tolist()) if "Tienda" in df.columns else ["Seleccione..."]
    tienda_sel = st.selectbox("Tienda", tiendas)

with col4:
    busqueda = st.text_input("🔍 Buscar Código o Descrip.")

# 4. LÓGICA DE FILTRADO
# Solo filtramos si hay alguna selección o texto
activado = (marca_sel != "Seleccione...") or (cat_sel != "Seleccione...") or (tienda_sel != "Seleccione...") or (busqueda != "")

if activado:
    df_final = df.copy()
    if marca_sel != "Seleccione...":
        df_final = df_final[df_final["Marca Prod"] == marca_sel]
    if cat_sel != "Seleccione...":
        df_final = df_final[df_final["Categoría"] == cat_sel]
    if tienda_sel != "Seleccione...":
        df_final = df_final[df_final["Tienda"] == tienda_sel]
    if busqueda:
        mask = df_final.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        df_final = df_final[mask]

    st.write(f"### 📋 Resultados encontrados: {len(df_final)}")
    st.dataframe(df_final, use_container_width=True, hide_index=True)
    
    if df_final.empty:
        st.warning("No se encontraron coincidencias para su búsqueda.")
else:
    # Mensaje inicial cuando no han buscado nada
    st.info("Para comenzar, seleccione un filtro arriba o escriba en el buscador.")
    
