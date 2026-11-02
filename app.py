import streamlit as st
import pandas as pd
import math
import re

st.set_page_config(
    page_title="Distribuidor Inteligente de Mesas",
    page_icon="🪑",
    layout="wide"
)

st.title("🪑 Distribuidor Inteligente de Asientos para Eventos")
st.write("**Problema:** Evita la separación de familias y minimiza el desperdicio de asientos en tus eventos.")

# --- Configuración del Salón (Sidebar) ---
st.sidebar.header("1. Configuración del Salón")
capacidad_mesa = st.sidebar.number_input("Capacidad por mesa (asientos):", min_value=2, max_value=20, value=8, step=1)

# --- Registro de Familias ---
st.sidebar.header("2. Registro de Familias")
if 'familias' not in st.session_state:
    st.session_state.familias = [
        {"nombre": "Familia Pérez", "integrantes": 6},
        {"nombre": "Familia Gómez", "integrantes": 4},
        {"nombre": "Familia Rodríguez", "integrantes": 3},
        {"nombre": "Familia Martínez", "integrantes": 7},
        {"nombre": "Familia López", "integrantes": 2}
    ]

# Validación del nombre de la familia: solo letras, espacios y caracteres básicos

def nombre_valido(nombre):
    if not nombre or not nombre.strip():
        return False
    nombre_limpio = nombre.strip()
    patron = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s'\-]+$"
    return bool(re.fullmatch(patron, nombre_limpio))

with st.sidebar.form("nueva_familia_form", clear_on_submit=True):
    nombre_fam = st.text_input("Nombre de la Familia / Grupo:", placeholder="Ej. Familia Pérez")
    integrantes_fam = st.number_input("Número de integrantes:", min_value=1, max_value=20, value=4, step=1)
    submit_button = st.form_submit_button(label="Agregar Familia")
    
    if submit_button:
        nombre_limpio = " ".join(nombre_fam.split())
        if not nombre_limpio:
            st.warning("Escribe un nombre para la familia o grupo.")
        elif not nombre_valido(nombre_limpio):
            st.warning("El nombre solo puede contener letras, espacios, acentos, guion y apóstrofo.")
        else:
            st.session_state.familias.append({"nombre": nombre_limpio, "integrantes": int(integrantes_fam)})
            st.success(f"¡{nombre_limpio} agregada!")

# --- Visualización y Limpieza de Lista ---
st.subheader("👥 Grupos y Familias Registradas")
if st.session_state.familias:
    df_familias = pd.DataFrame(st.session_state.familias)
    st.dataframe(df_familias, use_container_width=True)
    if st.button("🗑️ Limpiar lista de familias"):
        st.session_state.familias = []
        st.rerun()
else:
    st.info("No hay familias registradas aún. Utiliza el panel izquierdo para añadir grupos.")

# --- Algoritmo de Distribución ---
def optimizar_distribucion(familias, capacidad_mesa):
    # Ordenar familias de mayor a menor para priorizar grupos grandes (First-Fit Decreasing adaptado)
    familias_ordenadas = sorted(familias, key=lambda x: x['integrantes'], reverse=True)
    
    mesas = [] # Lista de listas, cada sublista contiene diccionarios de familias asignadas
    alertas_division = []
    
    for fam in familias_ordenadas:
        nombre = fam['nombre']
        integrantes = fam['integrantes']
        
        # Alerta para grupos más grandes que una mesa
        if integrantes > capacidad_mesa:
            alertas_division.append(f"⚠️ **{nombre}** ({integrantes} pers.) excede la capacidad de una mesa ({capacidad_mesa} asientos) y tuvo que ser dividida.")
            
            # Dividir la familia en fragmentos
            restante = integrantes
            while restante > 0:
                tamano_fragmento = min(restante, capacidad_mesa)
                asignado = False
                # Intentar meter el fragmento en mesas existentes
                for mesa in mesas:
                    asientos_ocupados = sum(f['integrantes'] for f in mesa)
                    if capacidad_mesa - asientos_ocupados >= tamano_fragmento:
                        mesa.append({"nombre": f"{nombre} (Grupo)", "integrantes": tamano_fragmento})
                        asignado = True
                        break
                if not asignado:
                    mesas.append([{"nombre": f"{nombre} (Grupo)", "integrantes": tamano_fragmento}])
                restante -= tamano_fragmento
        else:
            # Intentar acomodar la familia entera en una mesa existente sin dividir
            asignado = False
            for mesa in mesas:
                asientos_ocupados = sum(f['integrantes'] for f in mesa)
                if capacidad_mesa - asientos_ocupados >= integrantes:
                    mesa.append(fam)
                    asignado = True
                    break
            # Si no cabe en ninguna, abrir nueva mesa
            if not asignado:
                mesas.append([fam])
                
    return mesas, alertas_division

# --- Ejecutar Distribución ---
if st.session_state.familias:
    st.markdown("---")
    st.header("🗺️ Mapa de Distribución Optimizado")
    
    mesas_asignadas, alertas = optimizar_distribucion(st.session_state.familias, capacidad_mesa)
    
    # Mostrar Alertas Especiales
    for alerta in alertas:
        st.warning(alerta)
        
    # Mostrar Mesas
    cols = st.columns(3)
    total_asientos_vacios = 0
    total_asientos_disponibles = len(mesas_asignadas) * capacidad_mesa
    total_invitados = sum(f['integrantes'] for f in st.session_state.familias)
    
    for idx, mesa in enumerate(mesas_asignadas):
        col = cols[idx % 3]
        with col:
            asientos_ocupados = sum(f['integrantes'] for f in mesa)
            vacios = capacidad_mesa - asientos_ocupados
            total_asientos_vacios += vacios
            
            st.markdown(f"### 🍽️ Mesa {idx + 1}")
            st.progress(asientos_ocupados / capacidad_mesa)
            st.write(f"**Ocupación:** {asientos_ocupados} / {capacidad_mesa} asientos")
            
            # Lista de integrantes
            for f in mesa:
                st.write(f"• {f['nombre']} ({f['integrantes']} pers.)")
                
            if vacios > 0:
                st.warning(f"⚠️ Quedan {vacios} asiento(s) vacío(s) en esta mesa.")
            else:
                st.success("🎉 ¡Mesa completamente llena!")
            st.markdown("---")
            
    # --- Estadísticas de Eficiencia ---
    st.subheader("📊 Análisis de Capacidad")
    col_metric1, col_metric2, col_metric3 = st.columns(3)
    eficiencia = ((total_invitados) / total_asientos_disponibles) * 100 if total_asientos_disponibles > 0 else 0
    
    col_metric1.metric("Total de Mesas Necesarias", len(mesas_asignadas))
    col_metric2.metric("Total Asientos Vacíos", total_asientos_vacios, delta=f"{-total_asientos_vacios} asientos", delta_color="inverse")
    col_metric3.metric("Eficiencia del Salón", f"{eficiencia:.1f}%")
