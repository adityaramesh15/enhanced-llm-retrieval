from rag_llm import model
from rag_llm import rag

class Response:
    def __init__(self):
        self.model = model.Model()
        self.rag = rag.RAG()

    def query_model(self, query, matches):
        documents = self.rag.get_documents(matches)
        prompt = self.rag.create_prompt(query, documents)
        response = self.model.get_response(prompt)

        return response['response']


