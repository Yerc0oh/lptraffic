import streamlit as st

def render():
    st.header('Acerca de LPTraffic'); st.markdown('''**Materia:** Inteligencia Artificial · La Paz, Bolivia

**Problemática:** la congestión vehicular ocasiona retrasos y dificulta la planificación de desplazamientos.

**Objetivo general:** desarrollar un prototipo que estime la congestión y compare rutas urbanas mediante IA.

**Objetivos específicos:** generar y validar datos; entrenar dos redes MLP; ponderar un grafo; aplicar selección, cruce, mutación y elitismo; evaluar los resultados frente a referencias simples.

**Metodología:** simulación reproducible, separación cronológica, escalado y codificación, entrenamiento supervisado y optimización evolutiva.

**Tecnologías:** Python, Streamlit, Pandas, NumPy, Scikit-learn, NetworkX, Plotly, Folium, Joblib y Pytest.

**Limitaciones:** datos sintéticos, red de corredores aproximada y sentidos asumidos bidireccionales, condiciones constantes, sin observaciones ni tráfico en vivo. Las métricas no demuestran precisión en la ciudad real.''')
    for i in range(1,4): st.text_input(f'Integrante {i}',key=f'integrante{i}')
