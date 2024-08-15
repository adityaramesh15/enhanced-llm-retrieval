import time
from hybrid_search import database
from hybrid_search import confluence
from hybrid_search import embed
from datetime import datetime, timezone
from hybrid_search.utils import html_to_text

class UpdateDatabase:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.embed = embed.Embed()

    def update_page(self, page_id, name):
        html_data = self.confluence_api.get_content(page_id)
        text = html_to_text(html_data)
        dense, sparse = self.embed.embed_text(text)
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.db.upsert_page(page_id, dense, sparse, current_time, name)

    def load_all(self):
        space_id = self.confluence_api.get_space_id()
        pages = self.confluence_api.get_page_ids(space_id)
        for name, page_id in pages.items():
            self.update_page(page_id, name)

    def periodic_update(self):
        while True:
            space_id = self.confluence_api.get_space_id()
            pages = self.confluence_api.get_page_ids(space_id)

            for name, page_id in pages.items():
                confluence_time = datetime.strptime(self.confluence_api.get_time(page_id), "%Y-%m-%dT%H:%M:%S.%f%z")
                vector_db_time = datetime.strptime(self.db.get_time(page_id), "%Y-%m-%dT%H:%M:%S.%f%z")

                if confluence_time > vector_db_time:
                    print(f"Updated this ID {page_id} in Pinecone Database")
                    self.update_page(page_id, name)
            
            time.sleep(30)


if __name__ == "__main__":
    test = UpdateDatabase()
    # test.update_all()
    # test.periodic_update()
