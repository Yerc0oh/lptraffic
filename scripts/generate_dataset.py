from src.config import DATA
from src.traffic_graph import write_network
from src.data_generator import generate

def main():
    write_network()
    generate().to_csv(DATA/'traffic_dataset.csv',index=False)
    generate(5000,43,'2026-01-01','2026-03-31',100001).to_csv(DATA/'traffic_test.csv',index=False)
if __name__=='__main__': main()
