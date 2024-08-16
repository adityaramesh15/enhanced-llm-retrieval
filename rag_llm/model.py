import ollama
from hybrid_search.utils import load_env_variable, singleton

@singleton
class Model:
    def __init__(self):
        self.model =load_env_variable('OLLAMA_MODEL')
        self.client = ollama.Client()
    
    def get_response(self, messages):
        response = self.client.chat(model = self.model, messages = messages)
        return response