import math

import pandas as pd

if __name__ == "__main__":
    df = pd.read_csv('pull_requests.csv')
    metrics = []
    for value in df.values:
        repository_name = f'{value[0]}/{value[1]}'
        reviews = value[3]
        date_created = value[4]
        date_merged = value[5]
        date_closed = value[6]
        num_arquivos = value[7]
        num_linhas_adicionadas = value[8]
        num_linhas_deletadas = value[9]
        tempo_analise = ''
        was_merged = len(date_merged) > 0 if type(date_merged) is str else math.isnan(date_merged) is not True
        was_closed = len(date_closed) > 0 if type(date_closed) is str else math.isnan(date_closed) is not True
        if was_merged:
            tempo_analise = (pd.to_datetime(date_merged) - pd.to_datetime(date_created)).seconds
        elif was_closed:
            tempo_analise = (pd.to_datetime(date_closed) - pd.to_datetime(date_created)).seconds

        num_caracteres_descricao = value[10]
        num_participantes = value[11]
        num_comentarios = value[12]

        metrics.append({
            'reviews': reviews,
            'num_arquivos': num_arquivos,
            'num_linhas_adicionadas': num_linhas_adicionadas,
            'num_linhas_deletadas': num_linhas_deletadas,
            'tempo_analise': tempo_analise,
            'num_caracteres_descricao': num_caracteres_descricao,
            'num_participantes': num_participantes,
            'num_comentarios': num_comentarios,
            'was_merged': was_merged,
        })

    df_metrics = pd.DataFrame(metrics)
    df_metrics.to_csv('metrics.csv', index=False)