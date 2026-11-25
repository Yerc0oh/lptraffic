import networkx as nx
from src.traffic_graph import load_network,build_graph

def test_graph():
    n,e=load_network(); g=build_graph(n,e); assert g.is_directed() and len(g)==24 and g.number_of_edges()==64 and nx.is_strongly_connected(g)

def test_blocked():
    n,e=load_network(); e['bloqueo']=0; e.loc[0,'bloqueo']=1; g=build_graph(n,e); assert not g.has_edge(e.iloc[0].origen,e.iloc[0].destino)
