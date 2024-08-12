import confluence
import database
import embed
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from datetime import datetime


class SemanticSearch:
    def __init__(self):
        self.db = database.Database()
        self.confluence_api = confluence.ConfluenceAPI()
        self.tokenizer, self.model = embed.initialize()
    
    def load_pages(self):
        # Eventually I will incorporate page-change checking before uploading page to reduce resource usage. 
        space_id = self.confluence_api.get_space_id()
        pages = self.confluence_api.get_page_ids(space_id)

        for page in pages.items():

            name = page[0]
            page_id = page[1]

            if name == 'enhanced-llm-retrieval home':
                continue

            html_data = self.confluence_api.get_content(page_id)

            soup = BeautifulSoup(html_data, 'html.parser')
            text = soup.get_text(separator=" ")

            vector = embed.embed_text(self.tokenizer, self.model, text)

            now = datetime.now()
            current_time = now.strftime('%Y-%m-%dT%H:%M:%S.%f')[:-3] + 'Z'

            self.db.upsert_page(page_id, vector, current_time, name)


    def search(self, query):
        vector = embed.embed_text(self.tokenizer, self.model, query)
        result = self.db.db_search(vector)
        return result