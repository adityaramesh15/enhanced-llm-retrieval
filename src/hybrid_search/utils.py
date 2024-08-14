import os
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def load_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Missing environment variable: {var_name}")
    return value

def make_request(url, auth, params=None, timeout=10):
    response = requests.get(url, auth=auth, params=params, timeout=timeout)
    return response.json()

def initialize_auth():
    username = load_env_variable("CONFLUENCE_USERNAME")
    api_key = load_env_variable("CONFLUENCE_API_KEY")
    return HTTPBasicAuth(username, api_key)

def singleton(cls):
    instances = {}

    def get_instances(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]
    
    return get_instances
