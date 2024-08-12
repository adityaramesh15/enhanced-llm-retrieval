import pinecone
from dotenv import load_dotenv
import os


class Database:   
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX")
        self.pc = pinecone.Pinecone(api_key=self.api_key)


    def startup(self):       
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name, dimensions=384, metric='cosine',
                spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"))
        self.index = self.pc.Index(self.index_name)
    

    def clear(self):
        self.pc.delete_index(self.index_name)

    
    def upsert_page(self, page_id, vector, time, name):
        index = self.pc.Index(self.index_name)
        index.upsert (
            vectors=[ {
                "id": page_id,
                "values": vector,
                "metadata": {
                    'time': time,
                    'name': name
                }
            }]
        )

    def db_search(self, query_vector):
        index = self.pc.Index(self.index_name)
        result = index.query(
            vector = query_vector,
            top_k=3
        )
        return result
    