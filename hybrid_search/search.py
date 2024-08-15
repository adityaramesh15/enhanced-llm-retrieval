from hybrid_search import database
from hybrid_search import confluence
from hybrid_search import embed

class SemanticSearch:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.embed = embed.Embed()
        
    def search(self, query):
        dense, sparse = self.embed.embed_text(query)
        result = self.db.db_search(dense, sparse)
        return result