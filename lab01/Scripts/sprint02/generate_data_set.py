import pandas as pd

from github_graph_ql import run_query


def get_repositories(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    repositories_list = []

    query = """
    {
      search(query: "%s", type: %s, first: %s, after: %s) {
        edges {
          node {
            ... on Repository {
                nameWithOwner
                stargazers {
                    totalCount
                }
                createdAt
                pullRequests(states: MERGED) {
                    totalCount
                }
                releases(first: 100, orderBy: {field: CREATED_AT, direction: DESC}) {
                  totalCount
                }
                updatedAt
                primaryLanguage {
                    name
                }
                issues(states: [OPEN] ) {
                  totalCount
                }
                closedIssues: issues(states: [CLOSED]) {
                  totalCount
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
        stars = repo_info['stargazers']['totalCount']
        created_at = repo_info['createdAt'].split('T')[0]
        updated_at = repo_info['updatedAt'].split('T')[0]
        pull_requests = repo_info['pullRequests']['totalCount']
        total_releases = repo_info['releases']['totalCount']
        primary_language = repo_info['primaryLanguage']['name'] if repo_info['primaryLanguage'] else None
        open_issues = repo_info['issues']['totalCount']
        closed_issues = repo_info['closedIssues']['totalCount']
        total_issues = (open_issues + closed_issues)
        if total_issues == 0:
            percentual = 0
        else:
            percentual = (closed_issues / total_issues) * 100
        repositories_list.append({
            "name_with_owner": name_with_owner,
            "stars": stars,
            "created_at": created_at,
            "updated_at": updated_at,
            "pull_requests": pull_requests,
            "total_releases": total_releases,
            "primary_language": primary_language,
            "open_issues": open_issues,
            "closed_issues": closed_issues,
            "percentual": percentual
        })

    if page_info['hasNextPage'] and pages > 1:
        end_cursor = page_info['endCursor']
        repositories_list.extend(get_repositories(end_cursor, num_repos, query_type, type, pages - 1))

    return repositories_list

def save_to_csv(repositories):
    df = pd.DataFrame(repositories)
    df.to_csv('top_repositories.csv', index=False)

if __name__ == "__main__":
    top_repositories = get_repositories(pages=10, num_repos=100)
    if top_repositories:
        save_to_csv(top_repositories)
        print("Data saved successfully to top_repositories.csv")
