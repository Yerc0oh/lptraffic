import pandas as pd
import streamlit as st
from src.config import DATA,MODELS,NOTICE
from src.data_loader import validate,fingerprint
from src.neural_network import load,FILES
from src.traffic_graph import load_network
from src.visualization import schematic,geographic

@st.cache_data
def read_csv(path,modified):
    return validate(pd.read_csv(path))

def dataset():
    if 'dataset' not in st.session_state:
        p=DATA/'traffic_dataset.csv'; st.session_state.dataset=read_csv(str(p),p.stat().st_mtime_ns)
        st.session_state.dataset_hash=fingerprint(st.session_state.dataset)
    return st.session_state.dataset

def set_dataset(df):
    st.session_state.dataset=df; st.session_state.dataset_hash=fingerprint(df)
    for k in ['predictions','route_result','eval_classifier','eval_regressor','trained_classifier','trained_regressor']: st.session_state.pop(k,None)

def test_data():
    p=DATA/'traffic_test.csv'; return read_csv(str(p),p.stat().st_mtime_ns)

def independent_test(df):
    test=test_data()
    if df.fecha.max()>=test.fecha.min(): raise ValueError('El dataset activo no precede al periodo de prueba independiente. Use otro conjunto de prueba en código.')
    return test

@st.cache_resource
def cached_model(kind,modified): return load(kind)

def model(kind):
    path=MODELS/FILES[kind]
    if not path.exists(): return None
    return cached_model(kind,path.stat().st_mtime_ns)

def compatible_models():
    dataset(); a,b=model('classifier'),model('regressor')
    if not a or not b: raise ValueError('Entrene y guarde ambos modelos primero.')
    if any(m['dataset_hash']!=st.session_state.dataset_hash for m in [a,b]): raise ValueError('Los modelos no corresponden al dataset activo. Restáurelo o vuelva a entrenar.')
    return a,b

def download(df,label,name): st.download_button(label,df.to_csv(index=False).encode('utf-8-sig'),name,'text/csv')

def show_map(nodes,edges,routes=(),key='map'):
    st.caption('Conexiones y coordenadas aproximadas; las líneas no representan geometrías de calles.')
    if st.checkbox('Usar mapa base en línea',key=key):
        try:
            from streamlit_folium import st_folium
            st_folium(geographic(nodes,edges,routes),height=500,use_container_width=True,returned_objects=[])
        except Exception: st.warning('Mapa base no disponible. Se muestra el esquema local.')
    st.plotly_chart(schematic(nodes,edges,routes),use_container_width=True)

def conditions(prefix):
    from datetime import datetime
    from zoneinfo import ZoneInfo
    now=datetime.now(ZoneInfo('America/La_Paz'))
    a,b=st.columns(2)
    date=a.date_input('Fecha',now.date(),key=prefix+'date'); hour=b.slider('Hora',0,23,now.hour,key=prefix+'hour')
    temp=a.number_input('Temperatura (°C)',-40.,50.,15.,key=prefix+'temp'); precip=b.number_input('Precipitación (mm)',0.,300.,0.,key=prefix+'precip')
    weather=a.selectbox('Clima',['Soleado','Nublado','Lluvia','Granizo'],key=prefix+'weather'); holiday=b.checkbox('Feriado',key=prefix+'holiday'); event=a.checkbox('Evento especial',key=prefix+'event')
    return date,hour,temp,precip,weather,holiday,event
