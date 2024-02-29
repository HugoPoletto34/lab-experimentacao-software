from github_graph_ql import run_query


def get_repositories_req_6(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = """
    {
    search(query: "%s", type: %s, first: %s, after: %s) {
        nodes {
            ... on Repository {
               nameWithOwner
               issues(states: [OPEN] ) {
                  totalCount
                }
                closedIssues: issues(states: [CLOSED]) {
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
        open_issues = repo_info['issues']['totalCount']
        closed_issues = repo_info['closedIssues']['totalCount']
        total_issues = (open_issues + closed_issues)
        if total_issues == 0:
            percentual = 0
        else:
            percentual = (closed_issues / total_issues) * 100
        print(f"Repositório: {name_with_owner} - Percentual: {percentual}")


if __name__ == '__main__':
    get_repositories_req_6(num_repos=100, pages=1)
