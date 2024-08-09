from pinecone.grpc import PineconeGRPC as Pinecone
from pinecone import ServerlessSpec
import os


def startup(): 
    pc = Pinecone(api_key = os.environ.get("PINECONE_API_KEY"))
    index_name = pc.Index("enhanced-llm-retrieval")

    if index_name not in pc.list_indexes.names():
        pc.create_index(name = 'enhanced-llm-retrieval', dimensions = 768, metric = 'cosine', 
                        spec = ServerlessSpec(cloud="aws", region="us-east-1"))


