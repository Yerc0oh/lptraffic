import streamlit as st
import plotly.express as px
from src.utils import dataset,model,show_map
from src.traffic_graph import load_network
from src.config import COLORS

def render():
    st.header('Inicio · Panorama histórico'); df=dataset(); nodes,edges=load_network()
    cols=st.columns(4); cols[0].metric('Registros',f'{len(df):,}'); cols[1].metric('Tramos',len(edges)); cols[2].metric('Nodos',len(nodes)); cols[3].metric('Datos sintéticos',f'{df.fuente.eq("sintetico").mean():.0%}')
    for kind,label,metric in [('classifier','Clasificación','accuracy'),('regressor','Regresión','mae')]:
        try: b=model(kind)
        except Exception as e: st.warning(str(e)); continue
        if b:
            compatible=b['dataset_hash']==st.session_state.dataset_hash
            st.write(f'**{label}:** {"compatible" if compatible else "dataset diferente"} · {b["trained_at"][:16]} · {metric.upper()} validación: {b["metrics"]["validacion"]["modelo"][metric]:.3f}')
        else: st.info(f'{label}: pendiente de entrenamiento.')
    a,b=st.columns(2); counts=df.nivel_trafico.value_counts().rename_axis('nivel').reset_index(name='registros'); a.plotly_chart(px.bar(counts,x='nivel',y='registros',color='nivel',color_discrete_map=COLORS,title='Distribución de tráfico'),use_container_width=True)
    b.plotly_chart(px.line(df.groupby('hora',as_index=False).indice_congestion.mean(),x='hora',y='indice_congestion',title='Congestión por hora'),use_container_width=True)
    a.plotly_chart(px.bar(df.groupby('avenida',as_index=False).indice_congestion.mean().sort_values('indice_congestion'),x='indice_congestion',y='avenida',orientation='h',title='Congestión por avenida'),use_container_width=True)
    b.plotly_chart(px.bar(df.groupby('dia_semana',as_index=False).indice_congestion.mean().assign(dia=['Lun','Mar','Mié','Jue','Vie','Sáb','Dom']) if df.dia_semana.nunique()==7 else df.groupby('dia_semana',as_index=False).indice_congestion.mean(),x='dia_semana',y='indice_congestion',title='Congestión por día (0 = lunes)'),use_container_width=True)
    show_map(nodes,edges,key='dashboard_map')
