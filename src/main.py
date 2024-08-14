from hybrid_search.search import SemanticSearch
from hybrid_search.update import UpdateDatabase
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

    query = "What is the policy for leave of absence do to personal reasons?"
    print()
    print(s.search(query))
    
    # complete the processes
    for proc in procs:
        proc.join()