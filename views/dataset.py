import pandas as pd
import streamlit as st
from src.config import DATA,COLUMNS
from src.utils import dataset,set_dataset,test_data,download,read_csv
from src.data_loader import validate
from src.data_generator import generate

def render():
    st.header('Gestión del dataset'); df=dataset(); st.caption(f'{len(df):,} filas × {len(df.columns)} columnas. Fuentes: {", ".join(df.fuente.unique())}')
    with st.expander('Cargar, restaurar o generar datos'):
        file=st.file_uploader('CSV externo',type='csv')
        if st.button('Validar y cargar CSV',disabled=file is None):
            try: set_dataset(validate(pd.read_csv(file))); st.success('CSV cargado. Se requiere modelo compatible.'); st.rerun()
            except (ValueError,TypeError,pd.errors.ParserError) as e: st.error(str(e))
        if st.button('Restaurar dataset original'):
            p=DATA/'traffic_dataset.csv'; set_dataset(read_csv(str(p),p.stat().st_mtime_ns)); st.rerun()
        n=st.selectbox('Cantidad de registros',[10000,25000,50000,100000]); seed=st.number_input('Semilla',0,2**31-1,42)
        if st.button('Generar dataset sintético'):
            set_dataset(validate(generate(n,seed))); st.rerun()
    a,b,c=st.columns(3); start=a.date_input('Desde',pd.Timestamp(df.fecha.min()).date()); end=b.date_input('Hasta',pd.Timestamp(df.fecha.max()).date()); roads=c.multiselect('Avenida',sorted(df.avenida.unique())); levels=st.multiselect('Nivel',['Bajo','Medio','Alto']); search=st.text_input('Buscar texto en avenida, tramo o zona')
    view=df[df.fecha.between(str(start),str(end))]
    if roads: view=view[view.avenida.isin(roads)]
    if levels: view=view[view.nivel_trafico.isin(levels)]
    if search: view=view[view[['avenida','tramo_id','zona']].apply(lambda x:x.str.contains(search,case=False,regex=False)).any(axis=1)]
    st.caption(f'{len(view):,} coincidencias'); page=st.number_input('Página (100 filas)',1,max(1,(len(view)+99)//100),1); st.dataframe(view.iloc[(page-1)*100:page*100],use_container_width=True)
    with st.expander('Estadísticas y calidad'):
        st.dataframe(df.describe().T); st.write('Duplicados exactos:',int(df.duplicated().sum())); st.dataframe(df.isna().sum().rename('nulos')); st.bar_chart(df.nivel_trafico.value_counts()); st.caption('Tiempo nulo indica tramo bloqueado.')
    download(df,'Descargar dataset activo','traffic_dataset.csv'); download(test_data(),'Descargar prueba independiente','traffic_test.csv'); download(pd.DataFrame(columns=COLUMNS),'Descargar plantilla CSV','plantilla.csv')
