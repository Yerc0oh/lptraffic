import random
import networkx as nx
import pytest
from src.genetic_algorithm import optimize,valid,crossover,mutate,cost
from src.traffic_graph import load_network,build_graph

def graph():
    n,e=load_network(); e['tiempo_recorrido_min']=e.distancia_km*3; return build_graph(n,e)

def test_optimization():
    g=graph(); r=optimize(g,'N01','N20',population=20,generations=25); assert all(valid(g,p,'N01','N20') for p in r['routes']); assert len({tuple(p) for p in r['routes']})==len(r['routes']); assert cost(g,r['routes'][0])>=cost(g,r['references']['Dijkstra tiempo'])-1e-9
    assert all(a['mejor_costo']>=b['mejor_costo']-1e-9 for a,b in zip(r['history'],r['history'][1:])); assert r['routes']==optimize(g,'N01','N20',population=20,generations=25)['routes']

def test_cross_mutation():
    g=nx.DiGraph(); g.add_edges_from([('A','B'),('B','C'),('C','D'),('B','E'),('E','D'),('A','E')]); p=['A','B','C','D']; q=['A','B','E','D']; rng=random.Random(42)
    assert crossover(g,p,q,rng)==q
    for _ in range(20): assert valid(g,mutate(g,p,rng),'A','D')

def test_unreachable():
    g=graph(); g.remove_edges_from(list(g.out_edges('N01')))
    with pytest.raises(ValueError,match='No existe'): optimize(g,'N01','N20')

def test_invalid_parameters():
    with pytest.raises(ValueError): optimize(graph(),'N01','N20',population=3,elite=3)

def test_real_models_end_to_end():
    from src.neural_network import load
    from src.prediction import inputs,predict
    n,e=load_network(); block=e.iloc[0].edge_id; pred=predict(inputs(e,'2026-02-02',8,11,3,'Lluvia',blocked=[block]),load('classifier'),load('regressor')).rename(columns={'tramo_id':'edge_id'}); g=build_graph(n,pred)
    r=optimize(g,'N01','N20',population=20,generations=25)
    assert all(valid(g,p,'N01','N20') for p in r['routes']) and not g.has_edge(e.iloc[0].origen,e.iloc[0].destino)
