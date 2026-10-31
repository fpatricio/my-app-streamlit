import streamlit as st

st.title("Convertidor a Mayúsculas")

# Caja de texto para ingresar el texto
texto_usuario = st.text_input("Escribe tu texto aquí:", "")

# Procesamiento del texto
texto_mayusculas = texto_usuario.upper()

# Caja de texto donde se muestra el resultado procesado
st.text_area("Texto procesado (en mayúsculas):", value=texto_mayusculas, height=100)
