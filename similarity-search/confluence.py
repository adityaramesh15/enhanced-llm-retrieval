import requests
from requests.auth import HTTPBasicAuth
import json
import os

url = "https://adityaramesh15.atlassian.net/wiki/api/v2/spaces/enhancedllmretrieval/pages"
api_key = os.environ.get("CONFLUENCE_API_KEY")

auth = HTTPBasicAuth("adityaramesh15@gmail.com", api_key)



