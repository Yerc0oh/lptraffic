# Metodología experimental

## Simulación

Se seleccionan combinaciones únicas de fecha, hora y arista mediante un generador NumPy con semilla 42 para los datos históricos y 43 para prueba. La demanda depende de horas pico, mediodía, fines de semana, feriados simplificados y eventos, con ruido normal. La precipitación se simula con mayor probabilidad en noviembre–marzo. Accidentes, eventos y lluvia aumentan el índice de congestión. Se limita el índice al intervalo 0–100 y se divide en tres clases (35 y 70 como umbrales). La velocidad se reduce al aumentar el índice, con variación aleatoria; el tiempo es 60 × distancia / velocidad. Un bloqueo asigna índice 100, velocidad cero y tiempo ausente. Todos son supuestos, no estadísticas de La Paz.

## Aprendizaje supervisado

Se ordena el conjunto principal por fecha y hora y se separa aproximadamente 80/20 sin dividir observaciones del mismo instante. Se codifican categorías por OneHotEncoder y se escalan numéricas por StandardScaler. Hora, día y mes se convierten en pares seno/coseno con períodos 24, 7 y 12. Los transformadores se ajustan solo con entrenamiento. Las entradas excluyen flujo, velocidad, índice, tiempo y clase observados. La regresión excluye bloqueos. La clasificación recibe el indicador de bloqueo como condición conocida, no la etiqueta.

La red por defecto tiene 32 y 16 neuronas ocultas y activación ReLU. Adam ajusta pesos con tasa 0,001 y lotes de 128. Cada llamada a `partial_fit` ejecuta una época sin reiniciar los pesos. La validación selecciona los mejores pesos por F1 macro o MAE y detiene tras diez épocas sin mejora significativa. El CSV de enero–marzo de 2026 se reserva para evaluación independiente. Se comparan redes con clase mayoritaria y mediana de entrenamiento; se calculan exactitud, precisión, recall, F1 macro, MAE, MSE, RMSE y R². La validación mide desempeño simulado; la prueba no demuestra validez externa.

## Optimización evolutiva

Cada cromosoma es una ruta simple dirigida desde origen a destino. Se retiran bloqueos antes de buscar; los tiempos predichos positivos ponderan las aristas. La población inicial se obtiene por DFS aleatorizada con número acotado de intentos. Si no hay suficientes rutas distintas se permiten repeticiones. La aptitud es `1/(suma de tiempos + 1e-9)`. Por torneo se selecciona el individuo con menor costo. El cruce une segmentos de rutas que comparten un nodo; la mutación sustituye un segmento por una búsqueda aleatorizada que excluye el resto de la ruta. Se validan los descendientes y el elitismo preserva las mejores soluciones. Se archivan rutas distintas para presentar hasta tres alternativas. Los parámetros iniciales son 50 individuos, 100 generaciones, cruce 0,80, mutación 0,15, élite 2 y torneo 3.

Dijkstra de menor distancia y de menor tiempo predicho se calculan únicamente como referencias. En este problema, con costos fijos y positivos, la referencia por tiempo es óptima. La solución genética puede igualarla o quedar por encima. La optimización usa condiciones constantes y un objetivo temporal único; no incorpora penalizaciones opcionales por distancia o congestión. No utiliza los tiempos observados del CSV de prueba.
