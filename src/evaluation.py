import numpy as np
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, classification_report, mean_absolute_error, mean_squared_error, r2_score
from src.config import CLASSES

def metrics(kind,y,p):
    if kind=='classifier':
        return dict(accuracy=accuracy_score(y,p),precision=precision_score(y,p,average='macro',zero_division=0),recall=recall_score(y,p,average='macro',zero_division=0),f1=f1_score(y,p,average='macro',zero_division=0),matrix=confusion_matrix(y,p,labels=CLASSES).tolist(),report=classification_report(y,p,labels=CLASSES,output_dict=True,zero_division=0))
    mse=mean_squared_error(y,p)
    return dict(mae=mean_absolute_error(y,p),mse=mse,rmse=float(np.sqrt(mse)),r2=r2_score(y,p) if len(y)>1 else 0.)
