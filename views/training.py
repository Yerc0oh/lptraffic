import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from src.utils import dataset,model,independent_test
from src.neural_network import train,save,evaluate,target
from src.config import CLASSES,TERRACOTTA

def architecture(layers,kind):
    labels=['Entrada\n18 variables + codificación']+[f'Oculta {i+1}\n{n} neuronas' for i,n in enumerate(layers)]+['Salida\n'+('3 clases' if kind=='classifier' else '1 tiempo')]; fig=go.Figure(go.Scatter(x=list(range(len(labels))),y=[0]*len(labels),mode='lines+markers+text',text=labels,textposition='top center',marker=dict(size=25,color=TERRACOTTA))); fig.update_layout(height=170,xaxis=dict(visible=False,range=[-.6,len(labels)-.4]),yaxis=dict(visible=False,range=[-.5,.6]),margin=dict(l=5,r=5,t=5,b=5)); return fig

def display_metrics(kind,b):
    rows=[]
    for split,values in b['metrics'].items():
        for name,metrics in values.items(): rows.append({'Conjunto':split,'Método':name,**{k:v for k,v in metrics.items() if isinstance(v,(int,float))}})
    st.dataframe(pd.DataFrame(rows),use_container_width=True); hist=pd.DataFrame(b['history']); st.plotly_chart(px.line(hist,x='epoca',y='perdida',title='Pérdida de entrenamiento'),use_container_width=True); st.plotly_chart(px.line(hist,x='epoca',y='validacion',title='Validación: F1 macro o MAE'),use_container_width=True)
    if kind=='classifier':
        for split in ['validacion','prueba']:
            if split in b['metrics']:
                m=b['metrics'][split]['modelo']; st.plotly_chart(px.imshow(m['matrix'],x=CLASSES,y=CLASSES,text_auto=True,labels={'x':'Predicción','y':'Real'},title='Matriz · '+split),use_container_width=True); st.dataframe(pd.DataFrame(m['report']).T)

def render():
    st.header('Entrenamiento de redes neuronales'); df=dataset(); kind=st.radio('Modelo',['classifier','regressor'],format_func=lambda x:'Clasificación MLP' if x=='classifier' else 'Regresión MLP',horizontal=True)
    a,b,c=st.columns(3); count=a.number_input('Capas ocultas',1,4,2); layers=tuple(a.number_input(f'Neuronas capa {i+1}',4,128,32 if i==0 else 16,key=f'layer{i}') for i in range(count)); activation=b.selectbox('Activación',['relu','tanh','logistic']); rate=b.number_input('Tasa de aprendizaje',.0001,.05,.001,format='%.4f'); epochs=c.number_input('Épocas máximas',1,200,100); batch=c.selectbox('Lote',[32,64,128,256,512],index=2); seed=c.number_input('Semilla',0,2**31-1,42); patience=c.number_input('Paciencia',2,30,10)
    st.plotly_chart(architecture(layers,kind),use_container_width=True)
    key='trained_'+kind
    if st.button('Iniciar entrenamiento',type='primary'):
        bar=st.progress(0); status=st.empty()
        def progress(row,total):
            bar.progress(row['epoca']/total); status.write(f"Época {row['epoca']}/{total} · pérdida {row['perdida']:.4f} · validación {row['validacion']:.4f} · {row['segundos']:.1f} s")
        try:
            st.session_state[key]=train(df,kind,dict(layers=layers,activation=activation,learning_rate=rate,epochs=epochs,batch=batch,seed=seed,patience=patience),progress); st.success('Entrenamiento terminado; mejores pesos restaurados.')
        except Exception as e: st.error(f'Entrenamiento fallido: {e}')
    if st.button('Cargar modelo guardado'):
        try:
            loaded=model(kind)
            if loaded: st.session_state[key]=loaded
            else: st.warning('No existe modelo guardado.')
        except Exception as e: st.error(str(e))
    if key not in st.session_state:
        try:
            loaded=model(kind)
            if loaded: st.session_state[key]=loaded
        except Exception as e: st.warning(str(e))
    if key not in st.session_state: return
    bundle=st.session_state[key]
    if bundle['dataset_hash']!=st.session_state.dataset_hash: st.warning('Este modelo pertenece a otro dataset.'); return
    a,b=st.columns(2)
    if a.button('Evaluar CSV de prueba'):
        try:
            test=independent_test(df); m,base=evaluate(bundle,test); bundle['metrics']['prueba']={'modelo':m,'base':base}; st.session_state[key]=bundle
        except Exception as e: st.error(str(e))
    if b.button('Guardar modelo'):
        try:
            save(bundle)
            for result_key in ['predictions','route_result']: st.session_state.pop(result_key,None)
            st.success('Modelo guardado.')
        except Exception as e: st.error(str(e))
    display_metrics(kind,bundle)
    if kind=='regressor':
        try:
            from src.data_loader import split
            part=independent_test(df) if 'prueba' in bundle['metrics'] else split(df)[1]; x,y=target(part,kind); x=x.iloc[:2000]; y=y.iloc[:2000]; p=np.maximum(.05,bundle['pipeline'].predict(x)); plot=pd.DataFrame({'Real':y.to_numpy(),'Predicho':p,'Error':p-y.to_numpy()}); st.plotly_chart(px.scatter(plot,x='Real',y='Predicho',title='Esperado vs. predicho (min)'),use_container_width=True); st.plotly_chart(px.histogram(plot,x='Error',title='Distribución de errores (min)'),use_container_width=True)
        except ValueError as e: st.warning(str(e))
