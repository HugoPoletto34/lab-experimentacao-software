import pandas as pd
import math
from github_graph_ql import run_query
import os


def get_total_pr_and_reviews(owner, name, first=100, after=None, pages=1):
    try:
        query = """
        {
          repository(owner: "%s", name: "%s") {
            pullRequests(states: [CLOSED, MERGED], first: %s, after: %s) {
              totalCount
              nodes {
                reviews {
                  totalCount
                }
                createdAt
                mergedAt
                closedAt
                
              }
              pageInfo {
                endCursor
                hasNextPage
              }
            }
    
          }
          
        }
        """ % (owner, name, first, f'"{after}"' if after else "null")

        result = run_query(query)
        total_pr = result['data']['repository']['pullRequests']['totalCount']
        if total_pr >= 100:
            total_valid_pr = 0
            total_reviews = 0
            for pr in result['data']['repository']['pullRequests']['nodes']:
                pr_reviews = pr['reviews']['totalCount']
                if pr_reviews > 0:
                    date_created = pr['createdAt']
                    date_merged = pr['mergedAt']
                    date_closed = pr['closedAt']

                    if date_merged:
                        diff = (pd.to_datetime(date_merged) - pd.to_datetime(date_created)).seconds
                        if diff >= 3600:
                            total_reviews += pr['reviews']['totalCount']
                            total_valid_pr += 1
                    elif date_closed:
                        diff = (pd.to_datetime(date_closed) - pd.to_datetime(date_created)).seconds
                        if diff >= 3600:
                            total_reviews += pr['reviews']['totalCount']
                            total_valid_pr += 1

            page_info = result['data']['repository']['pullRequests']['pageInfo']

            if page_info['hasNextPage'] and pages > 1:
                end_cursor = page_info['endCursor']
                new_total_pr, new_total_reviews = get_total_pr_and_reviews(owner, name, first, end_cursor, pages - 1)
                total_valid_pr += new_total_pr
                total_reviews += new_total_reviews

            if total_reviews >= 1:
                return total_valid_pr, total_reviews
            else:
                return -1, -1
        else:
            return -1, -1
    except Exception as e:
        print(f"Error getting data for repository {owner}/{name}: {e}")
        return -1, -1


def save_to_csv(df):
    df.to_csv('top_repositories_with_PRs.csv', index=False)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Carregar os dados do arquivo CSV
    df = pd.read_csv(os.path.join(current_dir, 'top_repositories.csv'))
    repositories = df['name_with_owner']
    total_valid_repositories = 0
    for repo in repositories:
        owner, name = repo.split("/")
        print(f"Getting data for repository {repo}")
        total_pr, total_reviews = get_total_pr_and_reviews(owner, name, pages=10)
        if total_pr == -1 and total_reviews == -1:
            print(f"Repository {repo} has no PRs with reviews or less than 100 PRs")
            continue
        else:
            total_valid_repositories += 1

            df.loc[df['name_with_owner'] == repo, 'total_pr'] = total_pr
            df.loc[df['name_with_owner'] == repo, 'total_reviews'] = total_reviews
            print(f"{total_valid_repositories} - Total PRs: {total_pr} - Total Reviews: {total_reviews}")
            if [x for x in df['total_reviews'] if not math.isnan(x)].__len__() >= 200:
                break

    # remover todas as linhas que possuem NaN
    df = df.dropna()
    save_to_csv(df)
    # if top_repositories:
    #
    #     print("Data saved successfully to top_repositories_java.csv")
