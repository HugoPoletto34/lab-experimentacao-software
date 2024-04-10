import json
import pandas as pd
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

# Defina a consulta GraphQL
query = gql("""
query ($cursor: String) {
  search(query: "stars:>1", type: REPOSITORY, first: 100, after: $cursor) {
    pageInfo {
      endCursor
      hasNextPage
    }
    edges {
      node {
        ... on Repository {
          name
          url
          pullRequests(states: [MERGED, CLOSED], first: 100) {
            totalCount
            nodes {
              reviews(first: 1) {
                totalCount
              }
            }
          }
        }
      }
    }
  }
}
""")

transport = RequestsHTTPTransport(url='https://api.github.com/graphql', headers={'Authorization': 'Bearer your_token'}, use_json=True)
client = Client(transport=transport, fetch_schema_from_transport=True)


cursor = None
data = []

while True:
    result = client.execute(query, variable_values={'cursor': cursor})
    for edge in result['search']['edges']:
        repo = edge['node']
        data.append({
            'name': repo['name'],
            'url': repo['url'],
            'pr_count': repo['pullRequests']['totalCount'],
            'first_pr_review_count': repo['pullRequests']['nodes'][0]['reviews']['totalCount'] if repo['pullRequests']['nodes'] else None
        })
    if not result['search']['pageInfo']['hasNextPage']:
        break
    cursor = result['search']['pageInfo']['endCursor']


df = pd.DataFrame(data)
df.to_csv('github_data.csv', index=False)
