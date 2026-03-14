import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Configuración de pantalla ancha y estilo
st.set_page_config(page_title="Sistema de Inventario Pro", layout="wide")

st.markdown("""
    <style>
    h1 { color: #d32f2f; font-family: 'Arial Black'; margin-bottom: 20px; }
    .stSelectbox label { color: #333333; font-weight: bold; }
    .stDataFrame { border: 1px solid #d32f2f; }
    </style>
    """, unsafe_allow_html=True)

# Intento de cargar logo si existe
try:
    st.image("logo.png", width=120)
except:
    pass

st.title("🔴 Buscador de Inventario de Repuestos")

# 2. Conexión a Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read().dropna(how='all')
    
    # Limpieza de nombres de columnas (quita espacios accidentales)
    df.columns = df.columns.str.strip()

    # 3. BARRA DE FILTROS HORIZONTALES (5 Columnas)
    f1, f2, f3, f4, f5 = st.columns(5)

    with f1:
        marcas = ["Seleccione..."] + sorted(df["Marca Vehículo"].dropna().unique().tolist()) if "Marca Vehículo" in df.columns else ["Seleccione..."]
        marca_sel = st.selectbox("Marca", marcas)

    with f2:
        # Filtro dinámico para el modelo
        df_mod = df[df["Marca Vehículo"] == marca_sel] if marca_sel != "Seleccione..." else df
        modelos = ["Seleccione..."] + sorted(df_mod["Modelo"].astype(str).dropna().unique().tolist()) if "Modelo" in df.columns else ["Seleccione..."]
        mod_sel = st.selectbox("Modelo", modelos)

    with f3:
        años = ["Seleccione..."] + sorted(df["Año"].astype(str).dropna().unique().tolist()) if "Año" in df.columns else ["Seleccione..."]
        año_sel = st.selectbox("Año", años)

    with f4:
        cilindros = ["Seleccione..."] + sorted(df["Cilindraje"].astype(str).dropna().unique().tolist()) if "Cilindraje" in df.columns else ["Seleccione..."]
        cil_sel = st.selectbox("Cilindraje", cilindros)

    with f5:
        tipos = ["Seleccione..."] + sorted(df["Tipo de Repuesto"].dropna().unique().tolist()) if "Tipo de Repuesto" in df.columns else ["Seleccione..."]
        tipo_sel = st.selectbox("Tipo de Repuesto", tipos)

    # Buscador de texto (Códigos y Descripción)
    busqueda = st.text_input("🔍 Buscar por Código (OEM o Alterno) o descripción específica:")

    # 4. LÓGICA DE FILTRADO ACTIVO
    # Solo mostramos la tabla si el usuario interactúa con algún filtro
    activado = (marca_sel != "Seleccione...") or (mod_sel != "Seleccione...") or (año_sel != "Seleccione...") or (cil_sel != "Seleccione...") or (tipo_sel != "Seleccione...") or (busqueda != "")

    if activado:
        df_final = df.copy()
        
        if marca_sel != "Seleccione...":
            df_final = df_final[df_final["Marca Vehículo"] == marca_sel]
        if mod_sel != "Seleccione...":
            df_final = df_final[df_final["Modelo"].astype(str) == mod_sel]
        if año_sel != "Seleccione...":
            df_final = df_final[df_final["Año"].astype(str) == año_sel]
        if cil_sel != "Seleccione...":
            df_final = df_final[df_final["Cilindraje"].astype(str) == cil_sel]
        if tipo_sel != "Seleccione...":
            df_final = df_final[df_final["Tipo de Repuesto"] == tipo_sel]
        
        if busqueda:
            mask = df_final.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
            df_final = df_final[mask]

        # 5. MOSTRAR RESULTADOS
        # Definimos el orden de las columnas final
        cols_orden = [
            "Marca Vehículo", "Modelo", "Año", "Cilindraje", 
            "Tipo de Repuesto", "Descripción", "LISTA OEM", 
            "Códigos Alternos", "Cantidad", "Ubicación", "Precio"
        ]
        
        # Filtramos solo las columnas que realmente existan en el Sheets
        columnas_finales = [c for c in cols_orden if c in df_final.columns]
        
        st.write(f"### 📋 Repuestos encontrados: {len(df_final)}")
        
        # Mostramos la tabla con el ancho de la pantalla
        st.dataframe(df_final[columnas_finales], use_container_width=True, hide_index=True)
        
        # Alerta visual de Stock Agotado
        if "Cantidad" in df_final.columns:
            agotados = df_final[df_final["Cantidad"].astype(float) <= 0]
            if not agotados.empty:
                st.error(f"⚠️ Nota: Tienes {len(agotados)} producto(s) con stock en 0.")

    else:
        # Mensaje de bienvenida cuando no hay filtros activos
        st.info("👋 Bienvenido. Por favor, selecciona los datos del vehículo o escribe un código para buscar.")

except Exception as e:
    st.error("No se pudo conectar con el inventario.")
    st.info("Revisa que los nombres de las columnas en tu Google Sheets sean idénticos a los del código.")
    # st.write(e) # Descomentar para ver el error técnico si persiste
    
