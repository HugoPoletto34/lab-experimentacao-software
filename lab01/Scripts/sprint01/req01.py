from github_graph_ql import run_query


def get_repositories(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = """
    {
      search(query: "%s", type: %s, first: %s, after: %s) {
        edges {
          node {
            ... on Repository {
                nameWithOwner
                url
                stargazers {
                    totalCount
                }
                createdAt
            }
          }
        }
        pageInfo {
          endCursor
          hasNextPage
        }
      }
    }
    """ % (query_type, type, num_repos, f'"{cursor}"' if cursor else "null")

    result = run_query(query)
    repositories = result['data']['search']['edges']
    page_info = result['data']['search']['pageInfo']

    for repo in repositories:
        repo_info = repo['node']
        name_with_owner = repo_info['nameWithOwner']
        url = repo_info['url']
        created_at = repo_info['createdAt'].split('T')[0]
        stars = repo_info['stargazers']['totalCount']
        print(f"Repositório: {name_with_owner} - Criação: {created_at} - Estrelas: {stars} - URL: {url}")

    if page_info['hasNextPage'] and pages > 1:
        end_cursor = page_info['endCursor']
        get_repositories(end_cursor, num_repos, query_type, type, pages-1)


if __name__ == '__main__':
    get_repositories(num_repos=100, pages=20)
