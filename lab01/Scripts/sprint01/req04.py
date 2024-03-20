from github_graph_ql import run_query

def get_repositories_req4(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = '{ search(query: "%s", type: %s, first: %s)' % (query_type, type, num_repos)
    query += '{ nodes { ... on Repository { name updatedAt } } } }'  # Corregido aquí, name updatedAt en lugar de name {updatedAt }
    result = run_query(query)
    return result


if __name__ == '__main__':
   repositories =  get_repositories_req4(num_repos=100, pages=1)
   print(repositories)