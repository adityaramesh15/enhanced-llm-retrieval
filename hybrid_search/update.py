import time
from hybrid_search import database
from hybrid_search import confluence
from hybrid_search import embed
from hybrid_search import chunk
from hybrid_search.utils import html_to_text
from datetime import datetime, timezone
import redis

class UpdateDatabase:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.chunk = chunk.SemanticChunk()
        self.embed = embed.Embed()
        self.redis = redis.Redis(host = 'localhost', port=6379, decode_responses=True)

    def update_page(self, page_id):
        html_data = self.confluence_api.get_content(page_id)
        text = html_to_text(html_data)
        chunks = self.chunk.split(text)

        for num, chunk in enumerate(chunks):
            dense, sparse = self.embed.embed_text(chunk)

            current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
            self.redis.set('update_time', current_time)

            id = f"{page_id}-{num}"
            self.db.upsert_page(id, dense, sparse, chunk)

    def load_all(self):
        space_id = self.confluence_api.get_space_id()
        pages = self.confluence_api.get_page_ids(space_id)
        for page_id in pages.values():
            self.update_page(page_id)

    def periodic_update(self):
        while True:
            space_id = self.confluence_api.get_space_id()
            pages = self.confluence_api.get_page_ids(space_id)

            for page_id in pages.values():
                confluence_time = datetime.strptime(self.confluence_api.get_time(page_id), "%Y-%m-%dT%H:%M:%S.%f%z")
                vector_db_time = datetime.strptime(self.redis.get('update_time'), "%Y-%m-%dT%H:%M:%S.%f%z")

                if confluence_time > vector_db_time:
                    print(f"Updated this ID {page_id} in Pinecone Database")
                    self.update_page(page_id)
            
            time.sleep(30)


if __name__ == "__main__":
    test = UpdateDatabase()
    # test.update_all()
    # test.periodic_update()
