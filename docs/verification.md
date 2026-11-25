# Verificación de la entrega

Entorno ejecutado: Python 3.13.5, scikit-learn 1.8.0. Pruebas: 21 aprobadas (pytest). Compilación sintáctica de app, módulos y scripts: correcta. Streamlit y Streamlit-Folium no estaban disponibles; pip no pudo conectarse al repositorio, por lo que no se ejecutó la interfaz. No se verificó Python 3.11 ni el mapa base web.

## Datos

- Principal: 100,000 filas, 2023-01-01 a 2025-12-31.
- Prueba: 5,000 filas, 2026-01-01 a 2026-03-31.
- Red: 24 nodos, 64 aristas dirigidas, aproximadas y no verificadas cartográficamente.
- Clases principales: {'Medio': 48459, 'Bajo': 40140, 'Alto': 11401}.
- Bloqueos de prueba: 65.

## Evaluación independiente

### classifier
- Épocas ejecutadas: 28 (máximo configurado: 35).
- Entrenamiento: 80000; validación: 20000.
- modelo: accuracy=0.86920, precision=0.86181, recall=0.82631, f1=0.84129
- base: accuracy=0.47660, precision=0.15887, recall=0.33333, f1=0.21518

### regressor
- Épocas ejecutadas: 35 (máximo configurado: 35).
- Entrenamiento: 79030; validación: 19738.
- modelo: mae=0.24013, mse=0.15399, rmse=0.39241, r2=0.94479
- base: mae=1.12779, mse=2.98446, rmse=1.72756, r2=-0.07007

Estas métricas son resultados reales de una simulación, no medidas del tráfico real.
