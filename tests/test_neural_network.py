import numpy as np
import pytest
from src.data_generator import generate
from src.neural_network import train,save,load,evaluate
from src.traffic_graph import load_network
from src.prediction import inputs,predict

@pytest.fixture(scope='module')
def bundles():
    df=generate(2500); return [train(df,k,{'epochs':3}) for k in ['classifier','regressor']]

def test_train_predict(bundles):
    _,edges=load_network(); x=inputs(edges,'2026-01-02',8,12,2,'Lluvia',blocked=[edges.iloc[0].edge_id]); p=predict(x,*bundles)
    assert np.allclose(p[['prob_bajo','prob_medio','prob_alto']].sum(axis=1),1)
    assert p.loc[p.bloqueo==0,'tiempo_recorrido_min'].gt(0).all() and np.isnan(p.iloc[0].tiempo_recorrido_min)

@pytest.mark.parametrize('idx',[0,1])
def test_persist(bundles,tmp_path,idx):
    b=bundles[idx]; save(b,tmp_path); restored=load(b['kind'],tmp_path); df=generate(300,43,'2026-01-01','2026-03-31'); assert evaluate(restored,df)==evaluate(b,df)
