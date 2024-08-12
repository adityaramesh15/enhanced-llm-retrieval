import os
import pytz
from datetime import datetime
from dotenv import load_dotenv
import requests
from requests.auth import HTTPBasicAuth

load_dotenv()

def load_env_variable(var_name):
    value = os.getenv(var_name)
    if not value:
        raise EnvironmentError(f"Missing environment variable: {var_name}")
    return value

def convert_utc_to_local(utc_time_str, timezone='America/Chicago'):
    utc_time = datetime.strptime(utc_time_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    local_timezone = pytz.timezone(timezone)
    local_time = utc_time.replace(tzinfo=pytz.utc).astimezone(local_timezone)
    return local_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')

def make_request(url, auth, params=None, timeout=10):
    response = requests.get(url, auth=auth, params=params, timeout=timeout)
    return response.json()

def initialize_auth():
    username = load_env_variable("CONFLUENCE_USERNAME")
    api_key = load_env_variable("CONFLUENCE_API_KEY")
    return HTTPBasicAuth(username, api_key)
