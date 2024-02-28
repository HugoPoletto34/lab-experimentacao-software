from github_graph_ql import run_query


def get_issues_closed(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = """
    {
    search(query: "%s", type: %s, first: %s, after: %s) {
        nodes {
            ... on Repository {
               nameWithOwner
               issues(states: [CLOSED]) {
                    totalCount
                }
            }
        }
      }
    }
    """ % (query_type, type, num_repos, f'"{cursor}"' if cursor else "null")

    result = run_query(query)
    repositories = result['data']['search']['nodes']

    for repo_info in repositories:
        name_with_owner = repo_info['nameWithOwner']
        closed_issues = repo_info['issues']['totalCount']
        print(f"Repositório: {name_with_owner} - Total de issues fechadas: {closed_issues}")

def get_issues_totais(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = """
    search(query: "%s", type: %s, first: %s, after: %s) {
        nodes {
            ... on Repository {
               name
               issues {
                    totalCount
                }
            }
        }
      }
    }
    """ % (query_type, type, num_repos, f'"{cursor}"' if cursor else "null")

    result = run_query(query)
    repositories = result['data']['search']['edges']

    for repo in repositories:
        repo_info = repo['node']
        name_with_owner = repo_info['nameWithOwner']
        total_issues = repo_info['issues']['totalCount']
        print(f"Repositório: {name_with_owner} - Issues totais: {total_issues}")


if __name__ == '__main__':
    get_issues_closed(num_repos=100, pages=1)
