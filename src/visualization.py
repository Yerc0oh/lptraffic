import folium
import plotly.graph_objects as go
from src.config import COLORS,MUTED,BORDER,INK

def schematic(nodes,edges,routes=()):
    pos=nodes.set_index('node_id'); fig=go.Figure()
    for r in edges.itertuples():
        a,b=pos.loc[r.origen],pos.loc[r.destino]; color=COLORS.get(getattr(r,'nivel_trafico',''),BORDER); blocked=getattr(r,'bloqueo',0)
        fig.add_trace(go.Scatter(x=[a.longitud,b.longitud],y=[a.latitud,b.latitud],mode='lines',line=dict(color=MUTED if blocked else color,width=2,dash='dot' if blocked else 'solid'),hovertext=r.avenida,showlegend=False))
    for path,label,color in routes:
        p=pos.loc[path]; fig.add_trace(go.Scatter(x=p.longitud,y=p.latitud,mode='lines+markers',name=label,line=dict(color=color,width=5)))
    fig.add_trace(go.Scatter(x=nodes.longitud,y=nodes.latitud,mode='markers',text=nodes.nombre,hoverinfo='text',marker=dict(size=8,color=INK),name='Nodos'))
    fig.update_layout(height=520,xaxis_title='Longitud aproximada',yaxis_title='Latitud aproximada',yaxis_scaleanchor='x',margin=dict(l=10,r=10,t=15,b=10)); return fig

def geographic(nodes,edges,routes=()):
    pos=nodes.set_index('node_id'); m=folium.Map(location=[nodes.latitud.mean(),nodes.longitud.mean()],zoom_start=13)
    for r in edges.itertuples():
        a,b=pos.loc[r.origen],pos.loc[r.destino]; blocked=getattr(r,'bloqueo',0)
        folium.PolyLine([(a.latitud,a.longitud),(b.latitud,b.longitud)],color=MUTED if blocked else COLORS.get(getattr(r,'nivel_trafico',''),BORDER),weight=3,dash_array='5 8' if blocked else None,tooltip=r.avenida+' (esquema)').add_to(m)
    for path,label,color in routes:
        p=pos.loc[path]; folium.PolyLine(p[['latitud','longitud']].values.tolist(),color=color,weight=6,tooltip=label).add_to(m)
    for r in nodes.itertuples(): folium.CircleMarker([r.latitud,r.longitud],radius=4,tooltip=r.nombre,color=INK).add_to(m)
    if routes:
        for key,label in [(routes[0][0][0],'Origen'),(routes[0][0][-1],'Destino')]:
            p=pos.loc[key]; folium.Marker([p.latitud,p.longitud],tooltip=label).add_to(m)
    return m
