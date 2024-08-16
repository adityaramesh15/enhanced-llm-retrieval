from rag_llm import model
from rag_llm import rag
from rag_llm import context
from hybrid_search.utils import singleton

@singleton
class Response:
    def __init__(self):
        self.model = model.Model()
        self.rag = rag.RAG()
        self.redis = context.Redis()

    def query_model(self, session_id, query, matches):
        documents = self.rag.get_documents(matches)
        prompt = self.rag.create_prompt(query, documents)

        self.redis.store_conversation(session_id, 'user', prompt)
        messages = self.redis.get_conversation(session_id)

        response = self.model.get_response(messages)

        self.redis.store_conversation(session_id, 'assistant', response['message']['content'])

        return response['message']['content']
    
    def terminate(self, session_id):
        self.redis.clear_conversation(session_id)


