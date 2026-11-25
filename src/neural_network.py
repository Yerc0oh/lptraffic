import copy, json, time, platform
from datetime import datetime
from zoneinfo import ZoneInfo
import joblib
import numpy as np
import pandas as pd
import sklearn
from sklearn.neural_network import MLPClassifier,MLPRegressor
from sklearn.pipeline import Pipeline
from threadpoolctl import threadpool_limits
from src.config import FEATURES,CLASSES,MODELS
from src.data_loader import fingerprint,split
from src.preprocessing import transformer
from src.evaluation import metrics

DEFAULT=dict(layers=(32,16),activation='relu',learning_rate=.001,epochs=100,batch=128,seed=42,patience=10)
FILES={'classifier':'traffic_classifier.joblib','regressor':'travel_time_regressor.joblib'}

def target(df,kind):
    if kind=='regressor': df=df[df.bloqueo==0]
    return df[FEATURES],df['nivel_trafico' if kind=='classifier' else 'tiempo_recorrido_min']

def evaluate(bundle,df):
    kind=bundle['kind']; x,y=target(df,kind)
    if len(y)==0: raise ValueError('No hay registros evaluables.')
    p=bundle['pipeline'].predict(x)
    if kind=='regressor': p=np.maximum(.05,p)
    return metrics(kind,y,p),metrics(kind,y,np.repeat(bundle['baseline'],len(y)))

def train(df,kind,options=None,callback=None):
    cfg={**DEFAULT,**(options or {})}
    a,b=split(df); xa,ya=target(a,kind); xb,yb=target(b,kind)
    if len(ya)<2 or len(yb)<2: raise ValueError('Datos insuficientes para entrenar y validar.')
    prep=transformer(); x=prep.fit_transform(xa); v=prep.transform(xb)
    cls=MLPClassifier if kind=='classifier' else MLPRegressor
    model=cls(hidden_layer_sizes=tuple(cfg['layers']),activation=cfg['activation'],solver='adam',learning_rate_init=cfg['learning_rate'],batch_size=cfg['batch'],random_state=cfg['seed'],max_iter=1,early_stopping=False)
    best=None; score=-np.inf; idle=0; history=[]; start=time.perf_counter()
    with threadpool_limits(limits=1):
        for epoch in range(1,cfg['epochs']+1):
            if kind=='classifier': model.partial_fit(x,ya,classes=np.array(CLASSES))
            else: model.partial_fit(x,ya)
            p=model.predict(v)
            if kind=='regressor': p=np.maximum(.05,p)
            m=metrics(kind,yb,p); value=m['f1'] if kind=='classifier' else -m['mae']
            history.append(dict(epoca=epoch,perdida=float(model.loss_),validacion=float(value if kind=='classifier' else -value),segundos=time.perf_counter()-start))
            if value>score+1e-5: best=copy.deepcopy(model); score=value; idle=0
            else: idle+=1
            if callback: callback(history[-1],cfg['epochs'])
            if idle>=cfg['patience']: break
        bundle=dict(kind=kind,pipeline=Pipeline([('preprocess',prep),('mlp',best)]),baseline=ya.mode().iloc[0] if kind=='classifier' else float(ya.median()),config=cfg,history=history,dataset_hash=fingerprint(df),trained_at=datetime.now(ZoneInfo('America/La_Paz')).isoformat(),versions=dict(python=platform.python_version(),sklearn=sklearn.__version__,numpy=np.__version__,pandas=pd.__version__),n_train=len(ya),n_validation=len(yb))
        bundle['metrics']={}
        for name,part in [('entrenamiento',a),('validacion',b)]:
            m,base=evaluate(bundle,part); bundle['metrics'][name]={'modelo':m,'base':base}
    return bundle

def save(bundle,directory=MODELS):
    directory.mkdir(exist_ok=True,parents=True); kind=bundle['kind']; path=directory/FILES[kind]; tmp=path.with_suffix('.tmp'); joblib.dump(bundle,tmp); tmp.replace(path)
    meta={}
    mp=directory/'training_metadata.json'
    if mp.exists(): meta=json.loads(mp.read_text(encoding='utf-8'))
    meta[kind]={k:v for k,v in bundle.items() if k!='pipeline'}
    mp.write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding='utf-8')

def load(kind,directory=MODELS):
    path=directory/FILES[kind]
    if not path.exists(): return None
    b=joblib.load(path)
    if b['versions']['sklearn']!=sklearn.__version__: raise ValueError('Versión de scikit-learn diferente. Vuelva a entrenar.')
    return b
