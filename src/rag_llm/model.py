import ollama
import os
from dotenv import load_dotenv


class Model:
    def __init__(self):
        load_dotenv()
        self.model = os.getenv('OLLAMA_MODEL')
        self.client = ollama.Client(base_url="http://localhost:11414")

    def initialize_model(self):
        self.client.load_model(self.model)
    
    def get_response(self, input, model):
        response = self.client.complete(prompt=input, model=model)
        return response
