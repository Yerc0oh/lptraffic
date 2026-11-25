# LPTraffic

Sistema inteligente de predicción y optimización del tráfico vehicular en La Paz, Bolivia. Proyecto académico para la materia de Inteligencia Artificial, diseñado para tres integrantes.

**Aviso:** los datos son sintéticos, las coordenadas y conexiones son aproximadas y los sentidos se asumieron bidireccionales. No es un servicio de tráfico en vivo ni un navegador GPS. Las métricas solamente evalúan la simulación.

## Problemática y objetivos

La congestión vehicular ocasiona demoras en los desplazamientos urbanos. El objetivo general es implementar un prototipo experimental para anticipar la congestión y estimar rutas. Los objetivos específicos son preparar datos reproducibles, entrenar dos redes neuronales supervisadas, construir un grafo dirigido y evaluar un algoritmo genético de optimización frente a referencias convencionales.

## Instalación

Recomendado: Python 3.11 de 64 bits, 8 GB de RAM, navegador moderno, sin GPU. Para instalar dependencias se necesita acceso a internet o un repositorio local de paquetes. Después, los cálculos y el esquema Plotly funcionan sin internet. El mapa base opcional Folium necesita conexión.

Descomprima el ZIP, entre a `LPTraffic` y ejecute `iniciar_windows.bat` en Windows o `bash iniciar_linux.sh` en Linux. Alternativamente:

```bash
python -m venv venv
```

Active el entorno con `venv\Scripts\activate` (CMD Windows) o `source venv/bin/activate` (Linux/macOS). Luego:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Abra http://localhost:8501. No se requieren cuentas, claves ni servicios de pago.

## Uso

1. **Inicio:** explore indicadores históricos, distribución de clases, estado de modelos y esquema de la red.
2. **Gestión del dataset:** filtre, pagine, exporte, cargue CSV o genere datos sintéticos. Los datos activos se conservan durante la sesión; descárguelos para persistirlos. La plantilla contiene las 26 columnas requeridas. Los tiempos vacíos son exclusivos de tramos bloqueados.
3. **Entrenamiento:** seleccione MLP de clasificación o regresión, configure sus capas y parámetros, inicie el entrenamiento, revise pérdidas y métricas. Evalúe el CSV independiente y guarde el modelo. Repita para el otro tipo. No utilice las métricas de prueba para elegir hiperparámetros.
4. **Predicción:** seleccione tramo, fecha, hora, clima y condiciones especiales. Consulte probabilidades, tiempo y velocidad estimados. Exporte el historial.
5. **Rutas:** seleccione origen y destino, condiciones, bloqueos y parámetros genéticos. Revise las tres mejores rutas distintas disponibles, comparación con Dijkstra, evolución y exportación. Las líneas rectas son esquemáticas, no trazados de calles.
6. **Acerca del proyecto:** consulte los objetivos, las limitaciones y edite los nombres de los tres integrantes durante la sesión.

Los modelos incluidos fueron entrenados efectivamente. Si se cambia el dataset, se deben volver a entrenar ambos modelos o restaurar el original. No cargue archivos Joblib de terceros: la deserialización no es segura con archivos no confiables.

## Comandos adicionales

```bash
python -m scripts.generate_dataset
python -m scripts.train_models
python -m pytest -q
```

El script de generación reemplaza los cuatro CSV originales con la misma semilla. El entrenamiento de línea de comandos permite `--epochs 35`; por defecto utiliza hasta 100 épocas y aplica detención temprana sobre la validación cronológica. Los modelos incluidos se entrenaron con un máximo de 35 épocas. Los valores de feriados corresponden a un conjunto simplificado de fechas fijas de simulación, no a un calendario oficial completo.

## Estructura

- `app.py`, `.streamlit`, `assets`: interfaz, configuración y estilo.
- `src`: generación, validación, preprocesamiento, redes MLP, predicciones, grafo, algoritmo genético y visualización.
- `views`: seis módulos Streamlit.
- `data`: 100.000 observaciones de 2023–2025, 5.000 de 2026 y dos tablas viales.
- `models`: modelos reales serializados y metadatos de entrenamiento.
- `scripts`: generación y entrenamiento por consola.
- `tests`: pruebas automatizadas del núcleo.
- `docs`: arquitectura, diccionario, metodología y verificación.

## Tecnologías y defensa académica

Python, Pandas y NumPy procesan los datos; Scikit-learn implementa MLPClassifier y MLPRegressor con ReLU, Adam y normalización/codificación. NetworkX mantiene la conectividad. El algoritmo genético propio representa cada ruta mediante una lista de nodos, calcula aptitud inversamente proporcional al tiempo, selecciona por torneo, cruza nodos compartidos, muta segmentos y conserva los mejores individuos. Plotly, Folium y Streamlit presentan los resultados; Joblib guarda los modelos y Pytest verifica el núcleo.

Para pesos positivos y aditivos, Dijkstra obtiene la solución óptima; el algoritmo genético constituye una exploración experimental, no una garantía de superioridad. Véase `docs/methodology.md` para fórmulas.

## Limitaciones y mejoras

No se han validado coordenadas, sentidos, longitudes ni capacidades frente a cartografía oficial. Los enlaces representan corredores y posibles conexiones simplificadas. Se supone tráfico constante durante el viaje y no se modelan semáforos, pendientes ni horarios de giro. El rendimiento con datos reales es desconocido. Mejoras: incorporar observaciones reales, validar cartografía y restricciones, considerar incertidumbre y tráfico dependiente del tiempo.

La generación, entrenamiento, evaluación y pruebas del núcleo se ejecutaron en Python 3.13.5; Python 3.11 es el objetivo de instalación, pero no estaba disponible para verificarlo. Streamlit y Streamlit-Folium no estaban instalados y el entorno no permitió descargarlos, por lo que la ejecución interactiva de los seis módulos y los mapas web queda pendiente de verificación local. Véase `docs/verification.md`.
