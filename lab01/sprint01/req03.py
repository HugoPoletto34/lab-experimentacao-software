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
                releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                  totalCount
                  pageInfo {
                    endCursor
                    hasNextPage
                  }
                }
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
        total_releases = repo_info['releases']['totalCount']
        stars = repo_info['stargazers']['totalCount']
        print(f"Repositório: {name_with_owner} - Total de releases: {total_releases} - Estrelas: {stars} - URL: {url}")

    if page_info['hasNextPage'] and pages > 1:
        end_cursor = page_info['endCursor']
        get_repositories(end_cursor, num_repos, query_type, type, pages-1)

def get_releases(owner, name, cursor=None, num_releases=100, pages=1):
    query = """
    {
      repository(owner: "%s", name: "%s") {
        releases(first: %s, after: %s, orderBy: {field: CREATED_AT, direction: DESC}) {
          edges {
            node {
              name
              publishedAt
              url
            }
          }
          pageInfo {
            endCursor
            hasNextPage
          }
        }
      }
    }
    """ % (owner, name, num_releases, f'"{cursor}"' if cursor else "null")

    result = run_query(query)
    releases = result['data']['repository']['releases']['edges']
    page_info = result['data']['repository']['releases']['pageInfo']

    for release in releases:
        release_info = release['node']
        name = release_info['name']
        published_at = release_info['publishedAt'].split('T')[0]
        url = release_info['url']
        print(f"Release: {name} - Publicação: {published_at} - URL: {url}")

    if page_info['hasNextPage'] and pages > 1:
        end_cursor = page_info['endCursor']
        get_releases(owner, name, end_cursor, num_releases, pages-1)




if __name__ == '__main__':
    get_repositories(num_repos=100, pages=1)
