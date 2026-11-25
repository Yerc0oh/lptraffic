import numpy as np
import pandas as pd
from src.config import FEATURES

def inputs(edges,date,hour,temp,precip,weather,holiday=False,event=False,blocked=(),accidents=()):
    d=pd.Timestamp(date); df=edges.copy().rename(columns={'edge_id':'tramo_id'}); df=df.assign(hora=hour,dia_semana=d.dayofweek,mes=d.month,es_fin_semana=int(d.dayofweek>=5),es_feriado=int(holiday),es_hora_pico=int(7<=hour<=9 or 17<=hour<=20),temperatura_c=temp,precipitacion_mm=precip,condicion_climatica=weather,evento_especial=int(event),bloqueo=df.tramo_id.isin(blocked).astype(int),accidente=df.tramo_id.isin(accidents).astype(int)); return df

def predict(df,classifier,regressor):
    result=df.copy(); x=df[FEATURES]; pipe=classifier['pipeline']; probs=pipe.predict_proba(x)
    result['nivel_trafico']=pipe.predict(x)
    for i,c in enumerate(pipe.named_steps['mlp'].classes_): result['prob_'+c.lower()]=probs[:,i]
    result['tiempo_recorrido_min']=np.nan
    open_=df.bloqueo==0
    if open_.any():
        p=regressor['pipeline'].predict(x.loc[open_]);
        if not np.isfinite(p).all(): raise ValueError('Predicción de tiempo no finita.')
        result.loc[open_,'tiempo_recorrido_min']=np.maximum(p,.05)
    result['velocidad_estimada_kmh']=60*result.distancia_km/result.tiempo_recorrido_min
    return result
