TÍTULO: Distribuidor Inteligente de Mesas

Enlaces
Repositorio GitHub: https://github.com/fpatricio/my-app-streamlit
Aplicación desplegada: https://my-app-app-w24z75mdjdmprrdgiua9ju.streamlit.app/
Archivo principal de la app: https://github.com/fpatricio/my-app-streamlit/blob/main/app.py
Archivo de contexto del agente: https://github.com/fpatricio/my-app-streamlit/blob/main/AGENTS.md

Problema y usuario El usuario objetivo de esta aplicación es un organizador de eventos, por ejemplo un responsable de bodas, reuniones empresariales, celebraciones familiares o actos institucionales, que necesita distribuir a los asistentes en mesas de forma ordenada, justa y eficiente.
Sin la aplicación, este proceso se hace de manera manual. El usuario suele utilizar una lista de grupos o familias, anotar cuántas personas tiene cada uno, probar combinaciones a ojo en una hoja de cálculo o un cuaderno, y volver a revisar si hay familias separadas o demasiados huecos vacíos. Este método consume mucho tiempo, requiere esfuerzo repetitivo y no garantiza que la distribución sea óptima ni consistente.

La app resuelve la parte más tediosa y repetitiva del problema: registrar familias, ordenar grupos por tamaño, distribuirlos en mesas de manera automática y visualizar la ocupación real de cada mesa. La inteligencia aplicada en esta solución no reemplaza la decisión final del usuario, sino que le ayuda a tomar una decisión más rápida y mejor informada.

Lo que queda fuera de la automatización es la validación humana final: por ejemplo, decidir si una mesa debe cambiar de ubicación, si un grupo necesita preferencia especial, o si el organizador quiere ajustar la capacidad o la disposición del salón de acuerdo con criterios no representados en los datos. En otras palabras, la app automatiza la planificación básica, pero la decisión final sigue estando bajo control del responsable del evento.

Especificación La aplicación permite organizar grupos de personas en mesas de evento sin separar a las familias ni desperdiciar demasiado espacio.
Funcionalidades principales:

Registro de familias o grupos con nombre y número de integrantes.
Ajuste de la capacidad por mesa desde la barra lateral.
Visualización de las familias registradas en una tabla.
Distribución automática por mesas.
Detección de grupos que exceden la capacidad de una mesa.
Mapa visual de cada mesa con ocupación, huecos y alertas.
Cálculo de métricas: número de mesas necesarias, asientos vacíos y eficiencia general del salón.
Entradas de usuario:

Capacidad máxima de cada mesa.
Nombre de la familia o grupo.
Número de integrantes del grupo.
Salidas generadas:

Lista de familias registradas.
Distribución por mesas.
Ocupación total y vacíos en cada mesa.
Mensajes de advertencia cuando una familia supera la capacidad.
Indicadores de eficiencia global.
Criterios de aceptación:

Si la lista de familias está vacía, la aplicación muestra un mensaje informativo y no intenta distribuir nada.
Si una familia tiene más integrantes que la capacidad de la mesa, la app la divide en fragmentos y avisa claramente al usuario.
Si una familia no cabe en una mesa existente, la app abre una nueva mesa.
Si la capacidad por mesa cambia, la distribución se recalcula automáticamente.
Si el usuario limpia la lista, la app vuelve a un estado inicial sin datos.
La aplicación debe mostrar siempre una distribución legible y comprensible para el usuario.
Casos límite relevantes:

Una sala con familias pequeñas y una capacidad de mesa baja.
Un grupo grande que requiere dividirse.
Lista vacía.
Modificación de la capacidad de mesa mientras el usuario ya ha introducido familias.
Repetición de nombres o grupos con tamaños muy distintos.
La pieza de IA En la versión actual de la app, la lógica no depende de una API de IA externa. La solución funciona mediante un algoritmo simple y determinista que ordena familias por tamaño y las asigna a mesas en función de la capacidad disponible. Esto permite que la app sea rápida, fiable y sin costes de tokens ni dependencia de servicios externos.
Aunque en esta versión no hay llamadas a Gemini ni a un modelo de Hugging Face, la aplicación está preparada para mantener una política de seguridad adecuada si se incorpora IA en una futura mejora. En ese caso, la clave de la API debería almacenarse en los Secretos de Streamlit Cloud, nunca dentro del código fuente ni en el repositorio público. Asimismo, la aplicación debería implementar bloques try/except para detectar errores como:

429 Too Many Requests (cuota agotada)
fallos de red
errores del modelo o del servicio
respuestas vacías o incompletas
Esto garantizaría que, si la IA no funciona temporalmente, la app no se rompa y el usuario reciba un mensaje amigable como “La recomendación no está disponible en este momento. La distribución se ha calculado con la lógica local”. Además, el almacenamiento seguro de secretos y el control de errores son requisitos esenciales para evitar fugas de información y mejorar la robustez de la aplicación.

Proceso con IA Para guiar el desarrollo con el agente, se creó el archivo AGENTS.md en la raíz del repositorio. Este archivo actúa como contexto de trabajo y establece la intención del proyecto, las restricciones y el flujo recomendado para la implementación.
