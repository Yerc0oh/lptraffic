import hashlib
import numpy as np
import pandas as pd
from src.config import COLUMNS,CAT,NUM,CLASSES
from src.traffic_graph import load_network

def validate(df):
    if df.empty: raise ValueError('El CSV está vacío.')
    missing=set(COLUMNS)-set(df.columns)
    if missing: raise ValueError('Columnas faltantes: '+', '.join(sorted(missing)))
    df=df[COLUMNS].copy()
    if df.drop(columns='tiempo_recorrido_min').isna().any().any(): raise ValueError('Existen valores nulos obligatorios.')
    for c in set(NUM+['id','vehiculos_hora','velocidad_promedio_kmh','tiempo_recorrido_min','indice_congestion']):
        df[c]=pd.to_numeric(df[c],errors='raise')
        if np.isinf(df[c]).any(): raise ValueError(f'Valores infinitos: {c}')
    dates=pd.to_datetime(df.fecha,format='%Y-%m-%d',errors='raise')
    if df.duplicated(['fecha','hora','tramo_id']).any() or df.id.duplicated().any(): raise ValueError('Registros duplicados.')
    bounds={'hora':(0,23),'dia_semana':(0,6),'mes':(1,12),'distancia_km':(.001,50),'numero_carriles':(1,10),'capacidad_vehicular':(1,20000),'temperatura_c':(-40,50),'precipitacion_mm':(0,300),'vehiculos_hora':(0,30000),'velocidad_promedio_kmh':(0,150),'indice_congestion':(0,100),'id':(1,1e12)}
    for c in ['es_fin_semana','es_feriado','es_hora_pico','evento_especial','bloqueo','accidente']: bounds[c]=(0,1)
    for c,(a,b) in bounds.items():
        if not df[c].between(a,b).all(): raise ValueError(f'Fuera de rango: {c}')
    for c in ['id','hora','dia_semana','mes','numero_carriles','capacidad_vehicular','vehiculos_hora','es_fin_semana','es_feriado','es_hora_pico','evento_especial','bloqueo','accidente']:
        if (df[c]%1!=0).any(): raise ValueError(f'Se requiere entero: {c}')
    if not (df.dia_semana==dates.dt.dayofweek).all() or not (df.mes==dates.dt.month).all() or not (df.es_fin_semana==(df.dia_semana>=5)).all() or not (df.es_hora_pico== (df.hora.between(7,9)|df.hora.between(17,20))).all(): raise ValueError('Variables temporales inconsistentes.')
    _,edges=load_network()
    if not df.tramo_id.isin(edges.edge_id).all(): raise ValueError('Tramos desconocidos.')
    for c in ['avenida','zona','distancia_km','numero_carriles','capacidad_vehicular']:
        expected=df.tramo_id.map(edges.set_index('edge_id')[c]); ok=np.isclose(df[c],expected) if c not in ['avenida','zona'] else df[c]==expected
        if not np.all(ok): raise ValueError(f'Característica del tramo inconsistente: {c}')
    if not df.condicion_climatica.isin(['Soleado','Nublado','Lluvia','Granizo']).all(): raise ValueError('Clima inválido.')
    expected=np.where(df.indice_congestion<35,'Bajo',np.where(df.indice_congestion<70,'Medio','Alto'))
    if not (df.nivel_trafico==expected).all(): raise ValueError('Nivel de tráfico inconsistente.')
    open_=df.bloqueo==0
    if not df.loc[open_,'tiempo_recorrido_min'].gt(0).all() or not df.loc[open_,'velocidad_promedio_kmh'].gt(0).all() or not df.loc[~open_,'tiempo_recorrido_min'].isna().all() or not df.loc[~open_,'velocidad_promedio_kmh'].eq(0).all(): raise ValueError('Tiempo/velocidad incompatibles con bloqueo.')
    return df.assign(fecha=dates.dt.strftime('%Y-%m-%d')).sort_values(['fecha','hora','tramo_id']).reset_index(drop=True)

def fingerprint(df):
    return hashlib.sha256(pd.util.hash_pandas_object(df,index=False).values.tobytes()).hexdigest()

def split(df):
    df=df.sort_values(['fecha','hora']); stamps=df.fecha+' '+df.hora.astype(str).str.zfill(2); cutoff=stamps.iloc[int(len(df)*.8)]; a,b=df[stamps<cutoff],df[stamps>=cutoff]
    if a.empty or b.empty: raise ValueError('Se necesitan distintos momentos para la división cronológica.')
    return a,b
