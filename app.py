import streamlit as st
from src.config import ROOT,NOTICE
from src.theme import apply_plotly_theme
from views import dashboard,dataset,training,prediction,routes,about

st.set_page_config(page_title='LPTraffic',layout='wide',initial_sidebar_state='expanded')
apply_plotly_theme()
st.markdown('<style>'+ (ROOT/'assets/styles.css').read_text(encoding='utf-8')+'</style>',unsafe_allow_html=True)
st.title('LPTraffic'); st.caption('Sistema inteligente de predicción y optimización del tráfico vehicular en La Paz')
st.info(NOTICE)
modules={'Inicio':dashboard,'Gestión del dataset':dataset,'Entrenamiento':training,'Predicción de tráfico':prediction,'Optimización de rutas':routes,'Acerca del proyecto':about}
st.sidebar.title('LPTraffic'); st.sidebar.caption('Navegación')
if 'page' not in st.session_state: st.session_state.page='Inicio'
for name in modules:
    if st.sidebar.button(name,key=f'nav_{name}',use_container_width=True,type='primary' if st.session_state.page==name else 'secondary'):
        st.session_state.page=name
st.sidebar.divider(); st.sidebar.caption('Proyecto desarrollado para la materia de Inteligencia Artificial - Universidad Mayor de San Andrés (UMSA) - La Paz, Bolivia   Carrera de Informática - 2026')
try: modules[st.session_state.page].render()
except (OSError,ValueError,KeyError,TypeError) as e: st.error(f'No se pudo completar la operación: {e}')
