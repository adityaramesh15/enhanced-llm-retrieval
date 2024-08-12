from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
from dotenv import load_dotenv
import os


class Database:   
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("PINECONE_API_KEY")
        self.index_name = os.getenv("PINECONE_INDEX")
        self.pc = Pinecone(api_key=self.api_key)


    def startup(self):       
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name, dimensions=768, metric='cosine',
                spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        self.index = self.pc.Index(self.index_name)
    

    def clear(self):
        self.pc.delete_index(self.index_name)

    
    def upsert_page(self, page_id, text, time):
        index = self.pc.Index(self.index_name)
        index.upsert (
            vectors=[ {
                "id": page_id,
                "values": text,
                "metadata": {
                    'time': time
                }
            }]
        )

    def search(self, query_vector):
        index = self.pc.Index(self.index_name)
        result = index.query(
            vector = query_vector,
            top_k=3
        )
        return result
    