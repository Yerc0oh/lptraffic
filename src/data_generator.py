import numpy as np
import pandas as pd
from src.config import COLUMNS
from src.traffic_graph import load_network

def generate(n=100000,seed=42,start='2023-01-01',end='2025-12-31',id_start=1):
    rng=np.random.default_rng(seed)
    _,edges=load_network()
    dates=pd.date_range(start,end)
    # Una observación por tramo, fecha y hora.
    total=len(dates)*24*len(edges)
    if n>total: raise ValueError('Demasiados registros para el periodo.')
    ix=rng.choice(total,n,replace=False)
    d=dates[ix//(24*len(edges))]; h=(ix//len(edges))%24
    e=edges.iloc[ix%len(edges)].reset_index(drop=True)
    day=d.dayofweek.to_numpy(); month=d.month.to_numpy(); weekend=day>=5
    holidays=np.isin(d.strftime('%m-%d'),['01-01','01-22','05-01','07-16','08-06','11-02','12-25'])
    peak=((h>=7)&(h<=9))|((h>=17)&(h<=20))
    wet=np.isin(month,[11,12,1,2,3]); rain=rng.random(n)<np.where(wet,.32,.09)
    hail=rain&(rng.random(n)<.06); precipitation=np.where(rain,rng.gamma(1.8,2,n),0).round(2)
    weather=np.where(hail,'Granizo',np.where(rain,'Lluvia',np.where(rng.random(n)<.4,'Nublado','Soleado')))
    temp=(10+3*np.cos((month-1)*np.pi/6)+5*np.cos((h-14)*np.pi/12)+rng.normal(0,2,n)).round(1)
    event=rng.random(n)<.07; accident=rng.random(n)<.035; blocked=rng.random(n)<.012
    demand=.23+.49*peak+.20*((h>=12)&(h<=14))+.17*((h>=10)&(h<=16))+.12*((h>=6)&(h<=22))-.19*((h<=5)|(h>=23))-.20*weekend-.13*holidays+.16*event
    demand=np.clip(demand+rng.normal(0,.09,n),.015,1.4)
    cap=e.capacidad_vehicular.to_numpy(); flow=np.maximum(0,np.round(cap*demand)).astype(int)
    idx=np.clip(8+65*demand+13*rain+10*hail+23*accident+10*event+rng.normal(0,5,n),0,100)
    idx=np.where(blocked,100,idx).round(2)
    speed=np.maximum(3,e.velocidad_referencia_kmh.to_numpy()*(1-.77*idx/100)*rng.uniform(.9,1.1,n))
    speed=np.where(blocked,0,speed).round(2)
    time=np.divide(60*e.distancia_km.to_numpy(),speed,out=np.full(n,np.nan),where=~blocked).round(3)
    df=pd.DataFrame(dict(id=np.arange(id_start,id_start+n),fecha=d.strftime('%Y-%m-%d'),hora=h,dia_semana=day,mes=month,es_fin_semana=weekend.astype(int),es_feriado=holidays.astype(int),es_hora_pico=peak.astype(int),tramo_id=e.edge_id,avenida=e.avenida,zona=e.zona,distancia_km=e.distancia_km,numero_carriles=e.numero_carriles,capacidad_vehicular=cap,temperatura_c=temp,precipitacion_mm=precipitation,condicion_climatica=weather,evento_especial=event.astype(int),bloqueo=blocked.astype(int),accidente=accident.astype(int),vehiculos_hora=np.where(blocked,0,flow),velocidad_promedio_kmh=speed,tiempo_recorrido_min=time,indice_congestion=idx,nivel_trafico=np.where(idx<35,'Bajo',np.where(idx<70,'Medio','Alto')),fuente='sintetico'))
    return df[COLUMNS].sort_values(['fecha','hora','tramo_id']).reset_index(drop=True)
