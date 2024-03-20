import requests
import os
import subprocess

token = "token"

query = '''
query search($queryString: String!, $perPage: Int!, $cursor: String) {
  search(query: $queryString, type: REPOSITORY, first: $perPage, after: $cursor) {
    edges {
      node {
        ... on Repository {
          name
          nameWithOwner
          url
        }
      }
    }
    pageInfo {
      endCursor
      hasNextPage
    }
  }
}
'''

variables = {
    "queryString": "language:java", 
    "perPage": 1000
}

url = "https://api.github.com/graphql"

response = requests.post(url, json={"query": query, "variables": variables}, headers={"Authorization": f"Bearer {token}"})

if response.status_code == 200:
    data = response.json()
    for repo in data["data"]["search"]["edges"]:
        repo_name = repo["node"]["nameWithOwner"]
        repo_url = repo["node"]["url"]
        print(f"Clonando repositório {repo_name} ({repo_url})")
        os.system(f"git clone {repo_url}")
        
        repo_dir = repo_name.split('/')[1]
        
        os.chdir(repo_dir)
        
        subprocess.run(["mvn com.github.jazzmuesli:ck-mvn-plugin:metrics"], shell=True)
        
        os.chdir("..")
else:
    print(f"Erro na solicitação: {response.status_code} - {response.text}")
