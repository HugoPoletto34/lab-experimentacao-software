import pandas as pd
import os

from github_graph_ql import run_query

def validate_pr_by_time(pr):
    created_at = pr['createdAt']
    merged_at = pr['mergedAt']
    closed_at = pr['closedAt']
    if merged_at:
        diff = (pd.to_datetime(merged_at) - pd.to_datetime(created_at)).seconds
        return diff >= 3600
    elif closed_at:
        diff = (pd.to_datetime(closed_at) - pd.to_datetime(created_at)).seconds
        return diff >= 3600
    return False


def get_pr_infos(owner, name, first=100, after=None, pages=1):
    pull_requests = []
    try:
        query = """
        {
          repository(owner: "%s", name: "%s") {
            pullRequests(states: [CLOSED, MERGED], first: %s, after: %s) {
              nodes {
                reviews {
                    totalCount
                }
                number
                createdAt
                mergedAt
                closedAt
                files {
                  totalCount
                }
                additions
                deletions
                bodyText
                participants {
                  totalCount
                }
                comments {
                  totalCount
                }
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
        prs = result['data']['repository']['pullRequests']['nodes']
        prs = [pr for pr in prs if pr['reviews']['totalCount'] > 0]
        prs = [pr for pr in prs if validate_pr_by_time(pr)]

        for pr in prs:
            number = pr['number']
            reviews = pr['reviews']['totalCount']
            created_at = pr['createdAt']
            merged_at = pr['mergedAt']
            closed_at = pr['closedAt']
            files = pr['files']['totalCount']
            additions = pr['additions']
            deletions = pr['deletions']
            body_text = pr['bodyText']
            num_characters = len(body_text)
            participants = pr['participants']['totalCount']
            comments = pr['comments']['totalCount']
            print(f"Repository: {owner}_{name} PR: {number} - Criação: {created_at} - Total Reviews: {reviews} - Merged: {merged_at} - Fechado: {closed_at} - Arquivos: {files} - Adições: {additions} - Deleções: {deletions} - Participantes: {participants} - Comentários: {comments}")

            pull_requests.append({"owner": owner, "name": name, "number": number, "reviews": reviews, "created_at": created_at, "merged_at": merged_at, "closed_at": closed_at, "files": files, "additions": additions, "deletions": deletions, "num_characters": num_characters, "participants": participants, "comments": comments})

        page_info = result['data']['repository']['pullRequests']['pageInfo']

        if page_info['hasNextPage'] and pages > 1:
            end_cursor = page_info['endCursor']
            pull_requests.extend(get_pr_infos(owner, name, first, end_cursor, pages - 1))

        return pull_requests

    except Exception as e:
        print(f"Error: {e}")
        return pull_requests


def save_to_csv(list, filename):
    df = pd.DataFrame(list)
    df.to_csv(filename, index=False)


if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Carregar os dados do arquivo CSV
    df = pd.read_csv(os.path.join(current_dir, 'top_repositories_with_PRs.csv'))
    repositories = df['name_with_owner']
    pull_requests = []
    for repo in repositories:
        owner, name = repo.split("/")
        print(f"Getting PRs for repository {owner}/{name}")
        pull_requests.extend(get_pr_infos(owner, name, 25, pages=40))

    save_to_csv(pull_requests, 'pull_requests.csv')
