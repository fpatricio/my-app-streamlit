# Distribuidor Inteligente de Mesas

## 1. Enlaces

- Repositorio GitHub: https://github.com/fpatricio/my-app-streamlit
- Aplicación desplegada: https://my-app-app-w24z75mdjdmprrdgiua9ju.streamlit.app/
- Archivo principal de la app: https://github.com/fpatricio/my-app-streamlit/blob/main/app.py
- Archivo de contexto del agente: https://github.com/fpatricio/my-app-streamlit/blob/main/AGENTS.md

## 2. Problema y usuario

El usuario objetivo de esta aplicación es un organizador de eventos, por ejemplo un responsable de bodas, reuniones empresariales, celebraciones familiares o actos institucionales, que necesita distribuir a los asistentes en mesas de forma ordenada, justa y eficiente.

Sin la aplicación, este proceso se hace de manera manual. El usuario suele utilizar una lista de grupos o familias, anotar cuántas personas tiene cada uno, probar combinaciones a ojo en una hoja de cálculo o un cuaderno, y volver a revisar si hay familias separadas o demasiados huecos vacíos. Este método consume mucho tiempo, requiere esfuerzo repetitivo y no garantiza que la distribución sea óptima ni consistente.

La app resuelve la parte más tediosa y repetitiva del problema: registrar familias, ordenar grupos por tamaño, distribuirlos en mesas de manera automática y visualizar la ocupación real de cada mesa. La inteligencia aplicada en esta solución no reemplaza la decisión final del usuario, sino que le ayuda a tomar una decisión más rápida y mejor informada.

Lo que queda fuera de la automatización es la validación humana final: por ejemplo, decidir si una mesa debe cambiar de ubicación, si un grupo necesita preferencia especial, o si el organizador quiere ajustar la capacidad o la disposición del salón de acuerdo con criterios no representados en los datos. En otras palabras, la app automatiza la planificación básica, pero la decisión final sigue estando bajo control del responsable del evento.

## 3. Especificación

La aplicación permite organizar grupos de personas en mesas de evento sin separar a las familias ni desperdiciar demasiado espacio.

### Funcionalidades principales

- Registro de familias o grupos con nombre y número de integrantes.
- Ajuste de la capacidad por mesa desde la barra lateral.
- Visualización de las familias registradas en una tabla.
- Distribución automática por mesas.
- Detección de grupos que exceden la capacidad de una mesa.
- Mapa visual de cada mesa con ocupación, huecos y alertas.
- Cálculo de métricas: número de mesas necesarias, asientos vacíos y eficiencia general del salón.

### Entradas de usuario

- Capacidad máxima de cada mesa.
- Nombre de la familia o grupo.
- Número de integrantes del grupo.

### Salidas generadas

- Lista de familias registradas.
- Distribución por mesas.
- Ocupación total y vacíos en cada mesa.
- Mensajes de advertencia cuando una familia supera la capacidad.
- Indicadores de eficiencia global.

### Criterios de aceptación

- Si la lista de familias está vacía, la aplicación muestra un mensaje informativo y no intenta distribuir nada.
- Si una familia tiene más integrantes que la capacidad de la mesa, la app la divide en fragmentos y avisa claramente al usuario.
- Si una familia no cabe en una mesa existente, la app abre una nueva mesa.
- Si la capacidad por mesa cambia, la distribución se recalcula automáticamente.
- Si el usuario limpia la lista, la app vuelve a un estado inicial sin datos.
- La aplicación debe mostrar siempre una distribución legible y comprensible para el usuario.

### Casos límite relevantes

- Una sala con familias pequeñas y una capacidad de mesa baja.
- Un grupo grande que requiere dividirse.
- Lista vacía.
- Modificación de la capacidad de mesa mientras el usuario ya ha introducido familias.
- Repetición de nombres o grupos con tamaños muy distintos.

## 4. La pieza de IA

En la versión actual de la app, la lógica no depende de una API de IA externa. La solución funciona mediante un algoritmo simple y determinista que ordena familias por tamaño y las asigna a mesas en función de la capacidad disponible. Esto permite que la app sea rápida, fiable y sin costes de tokens ni dependencia de servicios externos.

Aunque en esta versión no hay llamadas a Gemini ni a un modelo de Hugging Face, la aplicación está preparada para mantener una política de seguridad adecuada si se incorpora IA en una futura mejora. En ese caso, la clave de la API debería almacenarse en los Secretos de Streamlit Cloud, nunca dentro del código fuente ni en el repositorio público. Asimismo, la aplicación debería implementar bloques try/except para detectar errores como:

- 429 Too Many Requests (cuota agotada)
- fallos de red
- errores del modelo o del servicio
- respuestas vacías o incompletas

Esto garantizaría que, si la IA no funciona temporalmente, la app no se rompa y el usuario reciba un mensaje amigable como “La recomendación no está disponible en este momento. La distribución se ha calculado con la lógica local”. Además, el almacenamiento seguro de secretos y el control de errores son requisitos esenciales para evitar fugas de información y mejorar la robustez de la aplicación.

## 5. Proceso con IA

Para guiar el desarrollo con el agente, se creó el archivo AGENTS.md en la raíz del repositorio. Este archivo actúa como contexto de trabajo y establece la intención del proyecto, las restricciones y el flujo recomendado para la implementación.

### Contenido del archivo AGENTS.md

```md
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
```

### Prompts clave utilizados

- “Crea una app Streamlit para ordenar familias en mesas de eventos, evitando separar a las familias y mostrando ocupación.”
- “Implementa una interfaz con sidebar para registrar familias y ajustar la capacidad por mesa.”
- “Añade una lógica que divida grupos demasiado grandes y muestre alertas.”
- “Haz que la app calcule métricas de ocupación y eficiencia del salón.”
- “Revisa la interfaz para que sea clara y evite errores en casos límite.”

### Qué se delegó a la IA

- Estructura inicial de la app.
- Diseño base de la interfaz en Streamlit.
- Lógica de clasificación y distribución por mesas.
- Redacción inicial de mensajes y textos visibles.
- Validación rápida de casos límite básicos.

### Qué se revisó y corrigió a mano

- La claridad de la interfaz para usuarios no técnicos.
- La organización del flujo de uso.
- El comportamiento de familias grandes y listas vacías.
- La coherencia del algoritmo con el problema real.
- La calidad de los mensajes para asegurar una experiencia útil y entendible.

## 6. Prueba y mejora

La prueba de la aplicación se realizó asumiendo el rol de organizador de un evento. Se comprobaron varios escenarios reales: familias pequeñas, una familia grande que excedía la capacidad de la mesa, una lista vacía y cambios en la capacidad disponible.

Durante la ejecución, se detectó que la interfaz necesitaba mensajes más claros para explicar cuándo una familia había sido dividida y cómo se interpretaba la ocupación de cada mesa. Además, se comprobó que la visualización debía ser más legible para que el usuario comprendiera rápidamente el estado global del salón.

Como mejora directa derivada de la prueba, se reforzó la presentación de la ocupación por mesa, se añadieron avisos específicos para casos límite y se simplificó el texto de la interfaz para que el usuario entendiera mejor qué estaba ocurriendo. El resultado fue una app más clara, útil y robusta frente a situaciones difíciles.

## 7. Pitch escrito (5 frases exactas)

- Problema: El problema de los organizadores de eventos es que asignar familias a mesas a mano suele romper grupos y dejar asientos vacíos innecesarios.
- Solución: Nuestra app soluciona esto permitiendo registrar familias, ajustar la capacidad por mesa y distribuir automáticamente los grupos.
- Valor de la IA: Gracias a la automatización logramos una distribución más ordenada, rápida y consistente que sería costosa de hacer manualmente.
- Aprendizaje: Al probar la app con usuarios reales aprendimos que la claridad en la ocupación y las alertas es esencial, y por ello mejoramos la interfaz y los mensajes de aviso.
- Futuro: En el futuro, planeamos añadir recomendaciones más avanzadas para eventos complejos, además de una mejor gestión de salones y capacidades variables.

## 8. Capturas de pantalla

Para este apartado debes añadir 4 capturas en el documento final. Cada una debe ir acompañada por una línea descriptiva debajo:

- Captura 1: App funcionando en el flujo principal con familias registradas y distribución visual por mesas.
- Captura 2: App respondiendo correctamente ante un caso límite, como una familia que supera la capacidad de una mesa o una lista vacía.
- Captura 3: Trabajo con el agente o con el archivo AGENTS.md durante el desarrollo del proyecto.
- Captura 4: Evidencia de la prueba, como una captura del proceso de validación o feedback del usuario.

Nota importante: En el documento final, cada captura debe ir acompañada por una línea explicativa breve, sin mostrar claves ni secretos del proyecto.

## Conclusión

La aplicación “Distribuidor Inteligente de Mesas” resuelve una necesidad real de organización de eventos, reduciendo el trabajo manual y mejorando la lógica de asignación. Su valor principal radica en hacer más sencillo y eficiente el reparto de personas a mesas, evitando la separación de familias y minimizando el desperdicio de espacio. La propuesta combina un enfoque útil, una interfaz sencilla y una lógica clara, con una base suficientemente robusta para ser probada y mejorada en iteraciones futuras.
