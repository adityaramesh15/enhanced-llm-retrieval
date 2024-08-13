import pinecone
from hybrid_search.utils import load_env_variable

class Database:
    def __init__(self):
        self.api_key = load_env_variable("PINECONE_API_KEY")
        self.index_name = load_env_variable("PINECONE_INDEX")
        self.pc = pinecone.Pinecone(api_key=self.api_key)

    def startup(self):
        if self.index_name not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=self.index_name, dimensions=384, metric='dotproduct',
                spec=pinecone.ServerlessSpec(cloud="aws", region="us-east-1"))
        self.index = self.pc.Index(self.index_name)

    def clear_all(self):
       index = self.pc.Index(self.index_name)
       index.delete(delete_all=True)

    def get_time(self, page_id):
        index = self.pc.Index(self.index_name)
        result = index.fetch([page_id])
        return result['vectors'][page_id]['metadata']['time']

    def upsert_page(self, page_id, dense_vector, sparse_vector, time, name):
        index = self.pc.Index(self.index_name)
        index.upsert(vectors=[{
            "id": page_id,
            "values": dense_vector,
            "metadata": {'time': time, 'name': name},
            'sparse_values': sparse_vector
        }])

    def db_search(self, dense_vector, sparse_vector):
        index = self.pc.Index(self.index_name)
        return index.query(vector=dense_vector, 
                           sparse_vector = sparse_vector,
                           top_k=3)


if __name__ == "__main__":
    test = Database()
    # print(test.get_time('33409'))