from hybrid_search.search import SemanticSearch
from hybrid_search.update import UpdateDatabase
from rag_llm.response import Response
from multiprocessing import Process
import os

db = UpdateDatabase()
semantic = SemanticSearch()
response = Response()

def run_update():
    db.periodic_update()

if __name__ == "__main__": 
    session_id = 'test_session'
    db.load_all()
    os.environ['TOKENIZERS_PARALLELISM'] = 'true' 

    procs = []
    proc = Process(target=run_update)  
    procs.append(proc)
    proc.start()

    try:
        while True:
            query = input("Enter your query: ")
            matches = semantic.search(query)
            print("\nResponse:")
            print(response.query_model(session_id, query, matches))
    
    except KeyboardInterrupt:
        print("\nExiting...")
    
    finally:
        for proc in procs:
            response.terminate(session_id)
            proc.terminate() 
            proc.join()
        

        print("Processes terminated. Exiting program.")
