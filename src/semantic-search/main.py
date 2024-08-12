from search import SemanticSearch
from update import UpdateDatabase
from multiprocessing import Process
import os

tst = UpdateDatabase();
s = SemanticSearch()

def run_update():
    tst.periodic_update()

if __name__ == "__main__": 
    tst.load_all()
    os.environ['TOKENIZERS_PARALLELISM'] = 'true' 

    procs = []
    proc = Process(target=run_update)  
    procs.append(proc)
    proc.start()

    query = "Can you drink alcohol on campus?"

    print(s.search(query))
    
    # complete the processes
    for proc in procs:
        proc.join()