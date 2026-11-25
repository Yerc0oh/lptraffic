# Diccionario de datos

Los CSV emplean UTF-8 y coma como separador. Las fechas son ISO (`AAAA-MM-DD`), zona horaria conceptual America/La_Paz. Los registros son sintéticos; una fila representa una combinación única de fecha, hora y tramo.

| Columna | Tipo / dominio | Significado |
|---|---|---|
| id | entero positivo único | Identificador de observación |
| fecha | fecha ISO | Fecha de simulación |
| hora | entero 0–23 | Hora local |
| dia_semana | entero 0–6 | Lunes = 0 |
| mes | entero 1–12 | Mes |
| es_fin_semana | 0/1 | Sábado o domingo |
| es_feriado | 0/1 | Feriado supuesto o indicado |
| es_hora_pico | 0/1 | 7–9 y 17–20 inclusive |
| tramo_id | texto E001–E064 | Identificador de arista |
| avenida | texto | Corredor de la arista |
| zona | texto | Zona del nodo de origen |
| distancia_km | decimal positivo | Longitud aproximada |
| numero_carriles | entero positivo | Carriles supuestos |
| capacidad_vehicular | entero positivo | Capacidad horaria estimada |
| temperatura_c | decimal -40 a 50 | Temperatura en °C |
| precipitacion_mm | decimal 0–300 | Precipitación en mm |
| condicion_climatica | Soleado/Nublado/Lluvia/Granizo | Condición simulada |
| evento_especial | 0/1 | Evento que afecta el tráfico |
| bloqueo | 0/1 | Tramo totalmente cerrado |
| accidente | 0/1 | Accidente en el tramo |
| vehiculos_hora | entero no negativo | Flujo simulado |
| velocidad_promedio_kmh | decimal 0–150 | Velocidad; cero si bloqueado |
| tiempo_recorrido_min | decimal positivo o vacío | Tiempo; vacío si bloqueado |
| indice_congestion | decimal 0–100 | Índice simulado |
| nivel_trafico | Bajo/Medio/Alto | Bajo <35; medio 35–<70; alto ≥70 |
| fuente | texto no vacío | Origen, `sintetico` en archivos incluidos |

## Red vial

`road_nodes.csv`: `node_id` (clave), `nombre`, `zona`, `latitud`, `longitud` (grados decimales aproximados).

`road_edges.csv`: `edge_id` (clave), `origen` y `destino` (claves de nodo), `avenida`, `zona`, `distancia_km`, `numero_carriles`, `capacidad_vehicular`, `velocidad_referencia_kmh`. Cada arista tiene sentido propio; la red de ejemplo incluye ambas direcciones por supuesto académico. Las longitudes resultan de distancia aproximada entre coordenadas multiplicada por 1,28, no mediciones de calle.

Para incorporar datos externos, mantenga las características físicas coherentes con el CSV vial. No se imputan valores obligatorios faltantes: deben corregirse en origen. Se conserva el vacío legítimo de tiempo para bloqueos. No deben utilizarse observaciones de prueba para entrenar ni seleccionar hiperparámetros.
