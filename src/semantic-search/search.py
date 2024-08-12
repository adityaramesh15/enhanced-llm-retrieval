import confluence
import database
import embed

class SemanticSearch:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.tokenizer, self.model = embed.initialize()
        
    def search(self, query):
        vector = embed.embed_text(self.tokenizer, self.model, query)
        result = self.db.db_search(vector)
        return result