import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler, FunctionTransformer
from src.config import FEATURES,CAT,NUM

def cyclical(x):
    a=np.asarray(x,dtype=float); theta=a*2*np.pi/np.array([24,7,12]); return np.concatenate([np.sin(theta),np.cos(theta)],axis=1)

def transformer():
    return ColumnTransformer([('num',StandardScaler(),[c for c in NUM if c not in ['hora','dia_semana','mes']]),('cyclic',FunctionTransformer(cyclical),['hora','dia_semana','mes']),('cat',OneHotEncoder(handle_unknown='ignore',sparse_output=False),CAT)])
