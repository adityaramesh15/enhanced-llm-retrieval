import requests
from requests.auth import HTTPBasicAuth
import json
import os
from dotenv import load_dotenv


load_dotenv()
api_url = os.getenv("CONFLUENCE_URL")
api_key = os.getenv("CONFLUENCE_API_KEY")
username = os.getenv("CONFLUENCE_USERNAME")
auth = HTTPBasicAuth(username, api_key)


def get_space_id():
    url = f"{api_url}/spaces"
    space_ids = {}
    while url:
        response = requests.get(url, auth=auth)
        data = response.json()  
       
        for space in data['results']:
            name = space['name']
            space_ids[name] = space['id']
        
        url = data['_links'].get('next')  
    return space_ids


def get_page_ids(space_id):
    url = f"{api_url}/spaces/{space_id}/pages"
    page_ids = {}
    while url:
        response = requests.get(url, auth=auth)
        data = response.json()  

        for page in data['results']:
            title = page['title']
            page_ids[title] = page['id']

        url = data['_links'].get('next')  
    return page_ids


def get_content(page_id):
    ...


def upsert_pages():
    ...

