import pinecone
from hybrid_search.utils import load_env_variable, singleton

@singleton
class Database:
    def __init__(self):
        self.api_key = load_env_variable("PINECONE_API_KEY")
        self.index_name = load_env_variable("PINECONE_INDEX")
        self.pc = pinecone.Pinecone(api_key=self.api_key)
        self.startup()

    def startup(self):
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name, dimension=768, metric='dotproduct',
                spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"))
        self.index = self.pc.Index(self.index_name)

    def clear_all(self):
       index = self.pc.Index(self.index_name)
       index.delete(delete_all=True)

    def upsert_page(self, page_id, dense_vector, sparse_vector, text):
        index = self.pc.Index(self.index_name)
        index.upsert(vectors=[{
            "id": page_id,
            "values": dense_vector,
            "metadata": {'content': text},
            'sparse_values': sparse_vector
        }])

    def db_search(self, dense_vector, sparse_vector):
        index = self.pc.Index(self.index_name)
        return index.query(vector=dense_vector, 
                           sparse_vector = sparse_vector,
                           top_k=3)

    def get_text(self, id):
        index = self.pc.Index(self.index_name)
        result = index.fetch(ids = [id])
        return result['vectors'][id]['metadata']['content']

# if __name__ == "__main__":
#     test = Database()
#     print(test.get_text('65575-2'))