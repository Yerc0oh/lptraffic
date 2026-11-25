import pandas as pd
import pytest
from src.config import DATA,COLUMNS
from src.data_generator import generate
from src.data_loader import validate,split

def test_reproducible():
    pd.testing.assert_frame_equal(generate(300,42),generate(300,42))

def test_packaged_data():
    a=validate(pd.read_csv(DATA/'traffic_dataset.csv')); b=validate(pd.read_csv(DATA/'traffic_test.csv'))
    assert len(a)==100000 and len(b)==5000
    assert list(a.columns)==COLUMNS and a.fecha.max()<b.fecha.min()
    assert not set(a.id)&set(b.id)
    assert set(a.nivel_trafico)=={'Bajo','Medio','Alto'} and set(b.nivel_trafico)==set(a.nivel_trafico)
    assert not a.duplicated().any() and a.indice_congestion.between(0,100).all()
    assert a.loc[a.bloqueo==1,'tiempo_recorrido_min'].isna().all()

def test_split():
    a,b=split(generate(3000)); assert .78<len(a)/(len(a)+len(b))<.82
    assert (a.fecha+' '+a.hora.astype(str).str.zfill(2)).max() < (b.fecha+' '+b.hora.astype(str).str.zfill(2)).min()

@pytest.mark.parametrize('column,value',[('hora',24),('tramo_id','X'),('condicion_climatica','Nieve'),('distancia_km',-1),('nivel_trafico','Otro')])
def test_invalid(column,value):
    df=generate(50); df.loc[0,column]=value
    with pytest.raises(ValueError): validate(df)

def test_duplicate():
    a=generate(20)
    with pytest.raises(ValueError): validate(pd.concat([a,a]))
