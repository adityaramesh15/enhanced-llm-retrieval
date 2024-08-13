import time
import database
import confluence
import embed
from bs4 import BeautifulSoup
from datetime import datetime, timezone

class UpdateDatabase:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.tokenizer, self.model = embed.initialize()

    def get_page_data(self, page_id):
        html_data = self.confluence_api.get_content(page_id)
        soup = BeautifulSoup(html_data, 'html.parser')
        text = soup.get_text(separator=" ")
        return text 

    def update_page(self, page_id, name):
        text = self.get_page_data(page_id)
        vector = embed.embed_text(self.tokenizer, self.model, text)
        current_time = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        self.db.upsert_page(page_id, vector, current_time, name)

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
