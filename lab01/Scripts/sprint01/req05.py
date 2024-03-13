from github_graph_ql import run_query

def get_repositories_languages(cursor=None, num_repos=100, query_type="stars:>0", type="REPOSITORY", pages=1):
    query = """
    {
        search(query: "stars:>1", type: REPOSITORY, first: 100) {
            nodes {
                ... on Repository {
                        name
                        primaryLanguage {
                            name
                        }
                }
            }
        }
    }"""
    result = run_query(query)
    return result

if __name__ == '__main__':
   repositories =  get_repositories_languages()
   print(repositories)
