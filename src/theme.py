import plotly.graph_objects as go
import plotly.io as pio
from src.config import SAND,SURFACE,BORDER,INK,MUTED,TERRACOTTA,TERRACOTTA_DARK,CLAY

def apply_plotly_theme():
    pio.templates['lptraffic']=go.layout.Template(layout=go.Layout(
        font=dict(family='Segoe UI, Inter, sans-serif',color=INK,size=13),
        paper_bgcolor='rgba(0,0,0,0)',plot_bgcolor='rgba(0,0,0,0)',
        colorway=[TERRACOTTA,TERRACOTTA_DARK,CLAY,'#7E8F71','#D9A183'],
        title=dict(font=dict(color=INK,size=18)),
        xaxis=dict(gridcolor=BORDER,zerolinecolor=BORDER,linecolor=BORDER,tickcolor=BORDER),
        yaxis=dict(gridcolor=BORDER,zerolinecolor=BORDER,linecolor=BORDER,tickcolor=BORDER),
        legend=dict(bgcolor=SURFACE,bordercolor=BORDER,borderwidth=1,font=dict(color=INK)),
        hoverlabel=dict(bgcolor=INK,bordercolor=TERRACOTTA_DARK,font=dict(color=SURFACE)),
        margin=dict(l=50,r=25,t=55,b=45),
    ))
    pio.templates.default='lptraffic'