import streamlit as st
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página y estilo
st.set_page_config(page_title="Sistema de Repuestos", layout="wide")

st.markdown("""
    <style>
    h1 { color: #ff0000; }
    .stTextInput>div>div>input { border-color: #ff0000; }
    </style>
    """, unsafe_allow_html=True)

# 2. Mostrar Logo
try:
    st.image("logo.png", width=200)
except:
    pass

st.title("🔴 Buscador de Repuestos")

# 3. Conexión a Google Sheets
conn = st.connection("gsheets", type=GSheetsConnection)

try:
    # Lee los datos (asegúrate que tu Excel tenga datos)
    df = conn.read()
    
    # 4. Buscador
    busqueda = st.text_input("Escribe el repuesto, marca o modelo que buscas:")

    if busqueda:
        # Filtra en todas las columnas
        mask = df.apply(lambda row: row.astype(str).str.contains(busqueda, case=False).any(), axis=1)
        resultados = df[mask]
        
        if not resultados.empty:
            st.success(f"Se encontraron {len(resultados)} resultados:")
            st.dataframe(resultados, use_container_width=True)
        else:
            st.warning("No se encontraron coincidencias.")
    else:
        st.write("Ingresa un término para ver los repuestos disponibles.")
        st.dataframe(df.head(10), use_container_width=True) # Muestra los primeros 10 por defecto

except Exception as e:
    st.error("Error al conectar con Google Sheets. Revisa que los 'Secrets' estén bien configurados.")
    
