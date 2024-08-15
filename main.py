from hybrid_search.search import SemanticSearch
from hybrid_search.update import UpdateDatabase
from rag_llm.response import Response
from rag_llm.model import Model
from multiprocessing import Process
import os

db = UpdateDatabase()
semantic = SemanticSearch()
response = Response()
# test = Model()

def run_update():
    db.periodic_update()

if __name__ == "__main__": 
    db.load_all()
    os.environ['TOKENIZERS_PARALLELISM'] = 'true' 

    procs = []
    proc = Process(target=run_update)  
    procs.append(proc)
    proc.start()

    query = "Any policies on Pregnancy I should know about?"
    matches = semantic.search(query)
    print(response.query_model(query, matches))

    
    
    # complete the processes
    for proc in procs:
        proc.join()