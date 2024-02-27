# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import requests
from dotenvy import load_env, read_file
from os import environ

load_env(read_file('../../.env'))

token = environ.get("USER_TOKEN")
headers = {"Authorization": f"Bearer {token}"}

def run_query(query):

    request = requests.post('https://api.github.com/graphql', json={'query': query}, headers=headers)
    if request.status_code == 200:
        return request.json()
    else:
        raise Exception("Query failed to run by returning code of {}. {}".format(request.status_code, query))
