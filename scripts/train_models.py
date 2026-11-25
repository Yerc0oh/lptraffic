import argparse
import pandas as pd
from src.config import DATA
from src.data_loader import validate
from src.neural_network import train,evaluate,save

def main():
    p=argparse.ArgumentParser(); p.add_argument('--epochs',type=int,default=100); args=p.parse_args()
    df=validate(pd.read_csv(DATA/'traffic_dataset.csv')); test=validate(pd.read_csv(DATA/'traffic_test.csv'))
    for kind in ['classifier','regressor']:
        b=train(df,kind,{'epochs':args.epochs},lambda row,n: print(kind,row,flush=True) if row['epoca']%10==0 else None); m,base=evaluate(b,test); b['metrics']['prueba']={'modelo':m,'base':base}; save(b); print(kind,m,flush=True)
if __name__=='__main__': main()
