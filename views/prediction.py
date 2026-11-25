import pandas as pd
import streamlit as st
from src.utils import compatible_models,conditions,download
from src.traffic_graph import load_network
from src.prediction import inputs,predict

def render():
    st.header('Predicción individual'); _,edges=load_network(); nodes,_=load_network(); names=nodes.set_index('node_id').nombre; labels={r.edge_id:f'{r.avenida} · {names[r.origen]} → {names[r.destino]} ({r.edge_id})' for r in edges.itertuples()}
    with st.form('prediction'):
        edge=st.selectbox('Tramo vial',list(labels),format_func=labels.get); cond=conditions('p'); blocked=st.checkbox('Bloqueo total'); accident=st.checkbox('Accidente'); submit=st.form_submit_button('Predecir tráfico',type='primary')
    if submit:
        try:
            a,b=compatible_models(); row=predict(inputs(edges[edges.edge_id==edge],*cond,blocked=[edge] if blocked else [],accidents=[edge] if accident else []),a,b); row['fecha']=str(cond[0]); st.session_state.predictions=pd.concat([st.session_state.get('predictions',pd.DataFrame()),row],ignore_index=True)
        except Exception as e: st.error(str(e))
    if 'predictions' not in st.session_state: return
    df=st.session_state.predictions; r=df.iloc[-1]; st.subheader(f"{r.avenida} · {r.nivel_trafico}")
    for col,level in zip(st.columns(3),['bajo','medio','alto']): col.metric('Prob. '+level,f'{r["prob_"+level]:.1%}')
    if r.bloqueo: st.error('Tramo no disponible para circular.')
    else:
        a,b=st.columns(2); a.metric('Tiempo estimado',f'{r.tiempo_recorrido_min:.2f} min'); b.metric('Velocidad estimada',f'{r.velocidad_estimada_kmh:.1f} km/h'); st.info({'Bajo':'Condición simulada favorable.','Medio':'Considere margen adicional de tiempo.','Alto':'Considere una ruta alternativa.'}[r.nivel_trafico])
    st.dataframe(df[['fecha','hora','tramo_id','avenida','nivel_trafico','tiempo_recorrido_min','bloqueo']]); download(df,'Exportar predicciones','predicciones.csv')
    if st.button('Limpiar historial'): st.session_state.pop('predictions'); st.rerun()
