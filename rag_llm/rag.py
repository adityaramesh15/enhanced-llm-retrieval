from hybrid_search.confluence import ConfluenceAPI
from hybrid_search.utils import html_to_text, singleton

@singleton
class RAG:
    def __init__(self):
        self.confluence = ConfluenceAPI()
        
    def get_documents(self, results):
        documents = []
        matches = results['matches']
        for match in matches:
            id = match['id']
            html_data = self.confluence.get_content(id)
            documents.append(html_to_text(html_data))
        
        return documents

    def create_prompt(self, query, documents):
        context = "".join(documents)
        prompt = f"Context:\n{context}\n\nQuery:{query}"
        return prompt