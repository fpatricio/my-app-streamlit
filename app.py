import streamlit as st
import pandas as pd
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


def nombre_valido(nombre):
    if not nombre or not nombre.strip():
        return False
    nombre_limpio = nombre.strip()
    patron = r"^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s'\-]+$"
    return bool(re.fullmatch(patron, nombre_limpio))


def mejor_mesa_para(familias_en_mesa, capacidad_mesa, integrantes):
    """Devuelve la mejor mesa disponible para ubicar a un grupo, minimizando huecos."""
    mejor_idx = None
    mejor_hueco = None

    for idx, mesa in enumerate(familias_en_mesa):
        ocupados = sum(f['integrantes'] for f in mesa)
        hueco_disponible = capacidad_mesa - ocupados
        if hueco_disponible >= integrantes:
            hueco_restante = hueco_disponible - integrantes
            if mejor_hueco is None or hueco_restante < mejor_hueco:
                mejor_hueco = hueco_restante
                mejor_idx = idx

    return mejor_idx


def optimizar_distribucion(familias, capacidad_mesa):
    familias_ordenadas = sorted(familias, key=lambda x: x['integrantes'], reverse=True)
    mesas = []
    alertas_division = []

    for fam in familias_ordenadas:
        nombre = fam['nombre']
        integrantes = fam['integrantes']

        if integrantes > capacidad_mesa:
            alertas_division.append(
                f"⚠️ **{nombre}** ({integrantes} pers.) excede la capacidad de una mesa ({capacidad_mesa} asientos) y tuvo que ser dividida."
            )

            restante = integrantes
            while restante > 0:
                tamano_fragmento = min(restante, capacidad_mesa)
                idx_mesa = mejor_mesa_para(mesas, capacidad_mesa, tamano_fragmento)

                if idx_mesa is not None:
                    mesas[idx_mesa].append({"nombre": f"{nombre} (Grupo)", "integrantes": tamano_fragmento})
                else:
                    mesas.append([{"nombre": f"{nombre} (Grupo)", "integrantes": tamano_fragmento}])

                restante -= tamano_fragmento
        else:
            idx_mesa = mejor_mesa_para(mesas, capacidad_mesa, integrantes)

            if idx_mesa is not None:
                mesas[idx_mesa].append(fam)
            else:
                mesas.append([fam])

    return mesas, alertas_division


def recomendacion_mesa(familias_actuales, capacidad, integrantes_nuevos):
    if integrantes_nuevos > capacidad:
        fragmentos = math.ceil(integrantes_nuevos / capacidad)
        return {
            "tipo": "division",
            "mensaje": f"Se dividirá en {fragmentos} grupo(s) para ajustar la capacidad de la mesa.",
            "mesa": None,
        }

    familias_preview = familias_actuales + [{"nombre": "Previsualización", "integrantes": integrantes_nuevos}]
    mesas_preview, _ = optimizar_distribucion(familias_preview, capacidad)

    for idx, mesa in enumerate(mesas_preview):
        if any(f.get("nombre") == "Previsualización" for f in mesa):
            ocupados = sum(f['integrantes'] for f in mesa)
            huecos = capacidad - ocupados
            return {
                "tipo": "mesa",
                "mensaje": f"La mejor opción es la mesa {idx + 1}. Ocupación estimada: {ocupados}/{capacidad} asientos. Hueco restante: {huecos}.",
                "mesa": idx + 1,
            }

    return {
        "tipo": "nueva",
        "mensaje": "Se abrirá una nueva mesa porque no hay hueco suficiente en las actuales.",
        "mesa": len(mesas_preview) + 1,
    }


with st.sidebar.form("nueva_familia_form", clear_on_submit=True):
    nombre_fam = st.text_input("Nombre de la Familia / Grupo:", placeholder="Ej. Familia Pérez")
    integrantes_fam = st.number_input("Número de integrantes:", min_value=1, max_value=20, value=4, step=1)
    submit_button = st.form_submit_button(label="Agregar Familia")

    recomendacion = recomendacion_mesa(st.session_state.familias, capacidad_mesa, int(integrantes_fam))
    if recomendacion["tipo"] == "mesa":
        st.caption(f"📌 Recomendación: {recomendacion['mensaje']}")
    elif recomendacion["tipo"] == "division":
        st.caption(f"⚠️ Recomendación: {recomendacion['mensaje']}")
    else:
        st.caption(f"🆕 Recomendación: {recomendacion['mensaje']}")

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

# --- Ejecutar Distribución ---
if st.session_state.familias:
    st.markdown("---")
    st.header("🗺️ Mapa de Distribución Optimizado")

    mesas_asignadas, alertas = optimizar_distribucion(st.session_state.familias, capacidad_mesa)

    for alerta in alertas:
        st.warning(alerta)

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
            ratio = asientos_ocupados / capacidad_mesa if capacidad_mesa else 0

            if ratio < 0.5:
                color_fondo = "#fff3cd"
                color_borde = "#f4b942"
            elif ratio < 0.85:
                color_fondo = "#e7f3ff"
                color_borde = "#4da3ff"
            else:
                color_fondo = "#dff7e8"
                color_borde = "#32a852"

            lista_html = "".join(
                [f"<div>• {f['nombre']} ({f['integrantes']} pers.)</div>" for f in mesa]
            )

            st.markdown(
                f"""
                <div style="background:{color_fondo}; border: 2px solid {color_borde}; border-radius: 12px; padding: 16px; margin-bottom: 16px; color: #1f1f1f;">
                    <h3 style="margin-top:0;">🍽️ Mesa {idx + 1}</h3>
                    <div><strong>Ocupación:</strong> {asientos_ocupados} / {capacidad_mesa} asientos</div>
                    <div style="margin: 10px 0;"><strong>Estado:</strong> {max(0, min(100, round(ratio * 100)))}%</div>
                    <div>{lista_html}</div>
                    <div style="margin-top: 10px;">{('⚠️ Quedan ' + str(vacios) + ' asiento(s) vacío(s)') if vacios > 0 else '🎉 Mesa completamente llena'}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.subheader("📊 Análisis de Capacidad")
    col_metric1, col_metric2, col_metric3, col_metric4 = st.columns(4)
    eficiencia = ((total_invitados) / total_asientos_disponibles) * 100 if total_asientos_disponibles > 0 else 0
    ocupacion_media = (sum(sum(f['integrantes'] for f in mesa) for mesa in mesas_asignadas) / total_asientos_disponibles) * 100 if total_asientos_disponibles > 0 else 0
    mesa_mas_llena = max((sum(f['integrantes'] for f in mesa) / capacidad_mesa) * 100 for mesa in mesas_asignadas) if mesas_asignadas else 0

    col_metric1.metric("Total de Mesas Necesarias", len(mesas_asignadas))
    col_metric2.metric("Total Asientos Vacíos", total_asientos_vacios)
    col_metric3.metric("Eficiencia del Salón", f"{eficiencia:.1f}%")
    col_metric4.metric("Mesa más llena", f"{mesa_mas_llena:.1f}%")

    st.caption(f"📌 Ocupación media general: {ocupacion_media:.1f}%")
