import networkx as nx
import pandas as pd
from src.config import DATA

# Nodos de referencia aproximados; enlaces son corredores esquemáticos, no geometrías reales.
NODES = [
('N01','Plaza San Francisco','Centro',-16.4961,-68.1374),('N02','Montes / Pando','Centro',-16.4912,-68.1392),('N03','Montes / Pérez Velasco','Centro',-16.4955,-68.1369),('N04','Mariscal Santa Cruz / Obelisco','Centro',-16.4990,-68.1350),('N05','El Prado / Camacho','Centro',-16.5010,-68.1337),('N06','Plaza del Estudiante','Centro',-16.5045,-68.1309),('N07','6 de Agosto / 20 de Octubre','Sopocachi',-16.5064,-68.1329),('N08','Plaza Abaroa','Sopocachi',-16.5114,-68.1285),('N09','Plaza Isabel la Católica','San Jorge',-16.5119,-68.1234),('N10','Arce / San Jorge','San Jorge',-16.5170,-68.1216),('N11','6 de Agosto / Belisario Salinas','Sopocachi',-16.5090,-68.1304),('N12','20 de Octubre / Aspiazu','Sopocachi',-16.5101,-68.1341),('N13','20 de Octubre / Landaeta','Sopocachi',-16.5070,-68.1353),('N14','Kantutani / final 20 de Octubre','Sopocachi',-16.5164,-68.1300),('N15','Puente Kantutani','Sopocachi',-16.5200,-68.1265),('N16','Puentes Trillizos / San Jorge','San Jorge',-16.5210,-68.1197),('N17','Avenida del Poeta / Arce','San Jorge',-16.5141,-68.1226),('N18','Avenida del Poeta / Cancha Zapata','Centro',-16.5067,-68.1251),('N19','Plaza Triangular','Miraflores',-16.5012,-68.1221),('N20','Plaza Villarroel','Miraflores',-16.4917,-68.1194),('N21','Busch / monumento Busch','Miraflores',-16.4963,-68.1207),('N22','Saavedra / Hospital de Clínicas','Miraflores',-16.5051,-68.1198),('N23','Saavedra / estadio','Miraflores',-16.4996,-68.1239),('N24','Miraflores / Puente de las Américas','Miraflores',-16.5095,-68.1189)]
LINKS = [(2,3,'Montes'),(3,1,'Montes'),(3,4,'Mariscal Santa Cruz'),(1,4,'Mariscal Santa Cruz'),(4,5,'16 de Julio (El Prado)'),(5,6,'16 de Julio (El Prado)'),(6,7,'6 de Agosto'),(7,11,'6 de Agosto'),(11,8,'6 de Agosto'),(6,9,'Arce'),(9,10,'Arce'),(7,13,'20 de Octubre'),(13,12,'20 de Octubre'),(12,14,'20 de Octubre'),(8,12,'Belisario Salinas'),(8,9,'Sánchez Lima / conexión'),(14,15,'Kantutani'),(15,16,'Puentes Trillizos'),(10,16,'Arce / conexión'),(9,17,'Arce'),(17,18,'Avenida del Poeta'),(18,5,'Camacho / conexión'),(18,19,'Avenida del Poeta / conexión'),(19,21,'Busch'),(21,20,'Busch'),(19,23,'Saavedra'),(23,22,'Saavedra'),(22,24,'Saavedra'),(24,16,'Puentes Trillizos / conexión'),(22,19,'Saavedra / conexión'),(21,23,'Vías de Miraflores'),(13,4,'Landaeta / conexión')]

def write_network():
    import math
    nodes = pd.DataFrame(NODES, columns=['node_id','nombre','zona','latitud','longitud'])
    edges=[]
    for i,j,road in LINKS:
        a,b=NODES[i-1],NODES[j-1]
        km=round(math.hypot((a[3]-b[3])*111,(a[4]-b[4])*107)*1.28,3)
        lanes=1 if 'conexión' in road or road=='Belisario Salinas' else 2
        for x,y in [(a,b),(b,a)]:
            edges.append([f'E{len(edges)+1:03}',x[0],y[0],road,x[2],km,lanes,lanes*650,35 if lanes==2 else 25])
    nodes.to_csv(DATA/'road_nodes.csv',index=False)
    pd.DataFrame(edges,columns=['edge_id','origen','destino','avenida','zona','distancia_km','numero_carriles','capacidad_vehicular','velocidad_referencia_kmh']).to_csv(DATA/'road_edges.csv',index=False)

def load_network():
    return pd.read_csv(DATA/'road_nodes.csv'),pd.read_csv(DATA/'road_edges.csv')

def build_graph(nodes=None,edges=None):
    if nodes is None or edges is None: nodes,edges=load_network()
    graph=nx.DiGraph()
    for row in nodes.to_dict('records'): graph.add_node(row['node_id'],**row)
    for row in edges.to_dict('records'):
        if row.get('bloqueo',0): continue
        graph.add_edge(row['origen'],row['destino'],**row)
    return graph
