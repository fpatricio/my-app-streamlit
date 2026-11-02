# AGENTS.md

## Rol
Eres un asistente de programación que ayuda a construir una app Streamlit para optimizar la distribución de personas en mesas de eventos.

## Objetivo del proyecto
Crear una herramienta útil para organizadores de eventos que quieran:
- registrar familias o grupos,
- definir la capacidad por mesa,
- asignar espacios sin romper familias,
- visualizar la ocupación de cada mesa,
- mostrar métricas útiles de la distribución.

## Restricciones
- No guardar claves ni tokens en el código.
- Mantener la app simple, clara y fácil de probar.
- Priorizar funcionalidad útil antes que complejidad visual.
- Documentar cambios importantes en el README.
- No inventar funcionalidades no pedidas.

## Flujo recomendado
1. Analizar el problema y la estructura del proyecto.
2. Implementar la lógica de distribución y la interfaz en Streamlit.
3. Validar casos límite (lista vacía, familias grandes, capacidad ajustada).
4. Revisar manualmente la salida y mejorar la claridad.
5. Documentar la app y su uso.

## Recomendación de diseño
- Usar Streamlit para desplegar la aplicación rápidamente.
- Mantener el estado de familias en `st.session_state`.
- Ordenar grupos por tamaño para mejorar la distribución.
- Mostrar avisos claros cuando una familia excede la capacidad de una mesa.
- Evitar mensajes complejos y mantener la experiencia de usuario simple.

## Instrucciones para la IA
- No añadas dependencias innecesarias.
- No publiques secretos en el código ni en el repositorio.
- Si se usa una API externa en el futuro, guarda la clave en Streamlit Secrets.
- Revisa siempre la salida manualmente antes de cerrar un cambio.
- Si hay un caso límite, prueba antes de darlo por válido.

## Prompts sugeridos
- “Crea una app Streamlit para ordenar familias en mesas de eventos, evitando separar a las familias y mostrando ocupación.”
- “Implementa una interfaz con sidebar para registrar familias y ajustar la capacidad por mesa.”
- “Añade una lógica que divida grupos demasiado grandes y muestre alertas.”
- “Haz que la app calcule métricas de ocupación y eficiencia del salón.”
- “Revisa la interfaz para que sea clara y evite errores en casos límite.”
