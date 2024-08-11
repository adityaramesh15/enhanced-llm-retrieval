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
        index_name = 'enhanced-llm-retrieval'
        if index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=index_name, dimensions=768, metric='cosine',
                spec=ServerlessSpec(cloud="aws", region="us-east-1"))
        self.index = self.pc.Index(index_name)

    
    def upsert_page(self, id, text, time):
        index = self.pc.Index(self.index_name)
        upsert_response = index.upsert (
            vectors=[ {
                "id": id,
                "values": text,
                "metadata": {
                    'time': time
                }
            }]
        )

    def search():
        ...
