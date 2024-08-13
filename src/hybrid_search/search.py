from hybrid_search import confluence
from hybrid_search import database
from hybrid_search import embed

class SemanticSearch:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.tokenizer, self.dense_model, self.sparse_model = embed.initialize()
        
    def search(self, query):
        dense, sparse = embed.embed_text(self.tokenizer, self.dense_model, self.sparse_model, query)
        result = self.db.db_search(dense, sparse)
        return result