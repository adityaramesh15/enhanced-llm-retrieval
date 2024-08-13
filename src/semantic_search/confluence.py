from semantic_search.utils import load_env_variable, make_request, initialize_auth

class ConfluenceAPI:
    def __init__(self):
        self.api_url = load_env_variable("CONFLUENCE_URL")
        self.space_name = load_env_variable("CONFLUENCE_SPACE_NAME")
        self.auth = initialize_auth()

    def get_space_id(self):
        url = f"{self.api_url}/spaces"
        while url:
            data = make_request(url, self.auth)
            for space in data['results']:
                if space['name'] == self.space_name:
                    return space['id']
            url = data['_links'].get('next')
        return None

    def get_page_ids(self, space_id):
        url = f"{self.api_url}/spaces/{space_id}/pages"
        page_ids = {}
        while url:
            data = make_request(url, self.auth)
            for page in data['results']:
                page_ids[page['title']] = page['id']
            url = data['_links'].get('next')
        return page_ids

    def get_content(self, page_id):
        url = f"{self.api_url}/pages/{page_id}"
        data = make_request(url, self.auth, params={'body-format': 'view'})
        return data['body']['view']['value']

    def get_time(self, page_id):
        url = f"{self.api_url}/pages/{page_id}"
        data = make_request(url, self.auth, params={'include-version': 'True'})
        return data['version']['createdAt']

if __name__ == "__main__":
    test = ConfluenceAPI()
    print(test.get_time('33409'))