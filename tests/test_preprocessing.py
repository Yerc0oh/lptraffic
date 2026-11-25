import numpy as np
from src.config import FEATURES
from src.preprocessing import transformer
from src.data_generator import generate

def test_no_leakage():
    assert not set(FEATURES)&{'indice_congestion','nivel_trafico','velocidad_promedio_kmh','vehiculos_hora','tiempo_recorrido_min','id','fecha','fuente'}

def test_transformer():
    d=generate(500); x=transformer().fit(d.iloc[:300][FEATURES]); a=x.transform(d.iloc[300:][FEATURES]); assert a.shape[0]==200 and np.isfinite(a).all()
