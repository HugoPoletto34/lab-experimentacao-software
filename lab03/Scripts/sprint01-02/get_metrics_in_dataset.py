import math

import pandas as pd

if __name__ == "__main__":
    df_pull_requests = pd.read_csv('pull_requests.csv')
    df_repositories = pd.read_csv('top_repositories_with_PRs.csv')
    metrics = []
    for value in df_repositories.values:
        owner, name = value[0].split('/')
        df_repository = df_pull_requests.loc[(df_pull_requests['owner'] == owner) & (df_pull_requests['name'] == name)]
        avarage_reviews = df_repository['reviews'].mean()
        avarage_num_arquivos = df_repository['files'].mean()
        avarage_num_linhas_adicionadas = df_repository['additions'].mean()
        avarage_num_linhas_deletadas = df_repository['deletions'].mean()
        df_tempo_analise = df_repository.apply(lambda x: (pd.to_datetime(x['merged_at']) - pd.to_datetime(x['created_at'])).seconds if x['merged_at'] else (pd.to_datetime(x['closed_at']) - pd.to_datetime(x['created_at'])).seconds, axis=1)
        avarage_tempo_analise = df_tempo_analise.mean()
        avarage_num_caracteres_descricao = df_repository['num_characters'].mean()
        avarage_num_participantes = df_repository['participants'].mean()
        avarage_num_comentarios = df_repository['comments'].mean()
        avarage_num_pr_merged = df_repository['merged_at'].count()

        metrics.append({
            'name_with_owner': value[0],
            'avarage_reviews': avarage_reviews,
            'avarage_num_arquivos': avarage_num_arquivos,
            'avarage_num_linhas_adicionadas': avarage_num_linhas_adicionadas,
            'avarage_num_linhas_deletadas': avarage_num_linhas_deletadas,
            'avarage_tempo_analise': avarage_tempo_analise,
            'avarage_num_caracteres_descricao': avarage_num_caracteres_descricao,
            'avarage_num_participantes': avarage_num_participantes,
            'avarage_num_comentarios': avarage_num_comentarios,
            'avarage_num_pr_merged': avarage_num_pr_merged,
        })

    df_metrics = pd.DataFrame(metrics)
    df_metrics.to_csv('metrics.csv', index=False)


    #
    #
    #
    #
    # for value in df_pull_requests.values:
    #     repository_name = f'{value[0]}/{value[1]}'
    #     reviews = value[3]
    #     date_created = value[4]
    #     date_merged = value[5]
    #     date_closed = value[6]
    #     num_arquivos = value[7]
    #     num_linhas_adicionadas = value[8]
    #     num_linhas_deletadas = value[9]
    #     tempo_analise = ''
    #     was_merged = len(date_merged) > 0 if type(date_merged) is str else math.isnan(date_merged) is not True
    #     was_closed = len(date_closed) > 0 if type(date_closed) is str else math.isnan(date_closed) is not True
    #     if was_merged:
    #         tempo_analise = (pd.to_datetime(date_merged) - pd.to_datetime(date_created)).seconds
    #     elif was_closed:
    #         tempo_analise = (pd.to_datetime(date_closed) - pd.to_datetime(date_created)).seconds
    #
    #     num_caracteres_descricao = value[10]
    #     num_participantes = value[11]
    #     num_comentarios = value[12]
    #
    #     metrics.append({
    #         'reviews': reviews,
    #         'num_arquivos': num_arquivos,
    #         'num_linhas_adicionadas': num_linhas_adicionadas,
    #         'num_linhas_deletadas': num_linhas_deletadas,
    #         'tempo_analise': tempo_analise,
    #         'num_caracteres_descricao': num_caracteres_descricao,
    #         'num_participantes': num_participantes,
    #         'num_comentarios': num_comentarios,
    #         'was_merged': was_merged,
    #     })
    #
    # df_metrics = pd.DataFrame(metrics)
    # df_metrics.to_csv('metrics.csv', index=False)