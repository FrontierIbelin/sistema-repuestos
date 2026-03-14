import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración y Estilo
st.set_page_config(page_title="Catálogo de Repuestos", layout="wide")

st.markdown("""
    <style>
    .stSelectbox label { color: #ff0000; font-weight: bold; }
    h1 { color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

try:
    st.image("logo.png", width=150)
except:
    pass

st.title("🔴 Filtros de Inventario")

# 2. Conexión
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

# Limpiar datos vacíos para que no den error
df = df.dropna(how='all')

# 3. INTERFAZ DE FILTROS (En la barra lateral o arriba)
st.sidebar.header("🔍 Filtrar por:")

# Filtro de Marca
lista_marcas = ["Todas"] + sorted(df["Marca"].unique().tolist())
marca_sel = st.sidebar.selectbox("Selecciona Marca", lista_marcas)

# Filtro de Modelo
modelos_filtrados = df[df["Marca"] == marca_sel] if marca_sel != "Todas" else df
lista_modelos = ["Todos"] + sorted(modelos_filtrados["Modelo"].unique().tolist())
modelo_sel = st.sidebar.selectbox("Selecciona Modelo", lista_modelos)

# 4. Lógica de Filtrado
df_final = df.copy()

if marca_sel != "Todas":
    df_final = df_final[df_final["Marca"] == marca_sel]

if modelo_sel != "Todos":
    df_final = df_final[df_final["Modelo"] == modelo_sel]

# Buscador manual extra
busqueda = st.text_input("O busca algo específico (nombre, código...):")
if busqueda:
    df_final = df_final[df_final.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)]

# 5. Mostrar Resultados
st.write(f"Mostrando **{len(df_final)}** repuestos encontrados:")
st.dataframe(df_final, use_container_width=True)
