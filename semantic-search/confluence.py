import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

class ConfluenceAPI:
    def __init__(self):
        load_dotenv()
        self.confluence_api_key = os.getenv("CONFLUENCE_API_KEY")
        self.confluence_space_name = os.getenv("CONFLUENCE_SPACE_NAME")
        self.username = os.getenv("CONFLUENCE_USERNAME")
        self.api_url = os.getenv("CONFLUENCE_URL")
        
        self.auth = HTTPBasicAuth(self.username, self.confluence_api_key)

        if not all([self.confluence_api_key, self.confluence_space_name, self.username, self.api_url]):
            raise EnvironmentError("Missing required environment variables for Confluence API.")


    def get_space_id(self):
        url = f"{self.api_url}/spaces"
        while url:
            response = requests.get(url, auth=self.auth, timeout=10)
            data = response.json()  
            for space in data['results']:
                if space['name'] == self.confluence_space_name:
                    return space['id']
            url = data['_links'].get('next')  
        return None


    def get_page_ids(self, space_id):
        url = f"{self.api_url}/spaces/{space_id}/pages"
        page_ids = {}
        while url:
            response = requests.get(url, auth=self.auth)
            data = response.json()  
            for page in data['results']:
                title = page['title']
                page_ids[title] = page['id']
            url = data['_links'].get('next')  
        return page_ids


    def get_content(self, page_id):
        url = f"{self.api_url}/pages/{page_id}"
        params = {'body-format': 'view', 'include-version': 'True'}
        response = requests.get(url, auth=self.auth, params=params)
        data = response.json()

        return data['body']['view']['value']
    
    
if __name__ == "__main__":
    confluence_api = ConfluenceAPI()
    # confluence_api.upsert_pages(space_name = 'enhanced-llm-retrieval')


