from hybrid_search.database import Database
from hybrid_search.utils import singleton

@singleton
class RAG:
    def __init__(self):
        self.db = Database()

    #TODO change to grab text metadata from Pinecone Chunks    
    def get_documents(self, results):
        documents = []
        matches = results['matches']
        for match in matches:
            id = match['id']
            documents.append(self.db.get_text(id))
        return documents

    def create_prompt(self, query, documents):
        context = "".join(documents)
        prompt = f"Context:\n{context}\n\nQuery:{query}"
        return prompt