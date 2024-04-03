import git
import csv
import os
import subprocess
from functools import reduce

from lab02.Scripts.sprint01 import generate_data_set


def clone_repository(repo_url, destination_path):
    try:
        # Clonar o repositório
        git.Repo.clone_from(repo_url, destination_path)
        print("Repositório clonado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao clonar o repositório: {e}")


def delete_repository(destination_path):
    try:
        # deletar o clone do repositírio
        os.system(f"rmdir /s /q {destination_path}")
        print("Repositório deletado com sucesso!")
    except Exception as e:
        print(f"Ocorreu um erro ao deletar o repositório: {e}")


def ler_csv(nome_arquivo):
    dados = []
    with open(nome_arquivo, newline='') as csvfile:
        leitor_csv = csv.reader(csvfile, delimiter=',')
        for linha in leitor_csv:
            dados.append(linha)
    return dados


def ck_analysis(repo_path, results_dir, ck_dir, repo_name):
    try:
        print(f"Gerando Métricas CK de {repo_name}...")
        ck_results = os.path.join(results_dir, repo_name, "")
        ck_command = f'java -jar {ck_dir} {repo_path} true 0 false {ck_results}'
        if not os.path.exists(ck_results):
            os.makedirs(ck_results)
        subprocess.run(ck_command, shell=True)
        print(f"Métricas geradas com sucesso pára {repo_name}")
        return os.path.join(ck_results, "class.csv"), os.path.join(ck_results, "method.csv")
    except Exception as e:
        print(f"Erro ao gerar métricas para {repo_name}: {e}")


def soma(x, y):
    return str(int(x[35]) + int(y[35]))


if __name__ == "__main__":
    # Ler o arquivo CSV
    nome_arquivo = "top_repositories_java.csv"
    dados = ler_csv(nome_arquivo)
    # remover primeira linha
    dados.pop(0)

    repos_with_loc = []
    for linha in dados:
        name = linha[0]
        repo_url = f"https://github.com/{name}.git"
        name_with_owner = name.replace('/', '_')
        destination_path = f"repositorios_clonados\\{name_with_owner}"
        try:
            print(linha)
            stars = linha[1]
            created_at = linha[2]
            releases = linha[3]
            current_dir = os.path.dirname(os.path.abspath(__file__))
            result_dir = os.path.join(current_dir, "results")
            ck_class_result_path = os.path.join(result_dir, name_with_owner, "class.csv")

            if not os.path.exists(ck_class_result_path):
                clone_repository(repo_url, destination_path)
                ck_path = os.path.join(current_dir, "ck-0.7.1-SNAPSHOT-jar-with-dependencies.jar")
                ck_class_result_path, ck_method_result_path = ck_analysis(destination_path, result_dir, ck_path,
                                                                          name_with_owner)

            result_dados_class = ler_csv(ck_class_result_path)

            result_dados_class.pop(0)
            loc = 0
            cbo = 0
            dit = 0
            lcom = 0
            # Usando um loop for para iterar sobre cada elemento da lista e somá-lo ao total
            for elemento in result_dados_class:
                cbo += int(elemento[3])
                dit += int(elemento[8])
                lcom += int(elemento[11])
                loc += int(elemento[34])

            repo = {
                "name_with_owner": name,
                "stars": stars,
                "created_at": created_at,
                "releases": releases,
                "loc": loc,
                "cbo": cbo,
                "dit": dit,
                "lcom": lcom
            }
            print(repo)
            repos_with_loc.append(repo)

        except Exception as e:
            print(f"Ocorreu um erro na análise do repositório: {e}")

        delete_repository(os.path.abspath(destination_path))

    generate_data_set.save_to_csv('top_repositories_with_loc', repos_with_loc)

    # URL do repositório a ser clonado
    # name = "lab-experimentacao-software"
    # repo_url = f"https://github.com/HugoPoletto34/{name}.git"
    #
    # # Caminho de destino para clonar o repositório
    # destination_path = f"repositorios_clonados/{name}"
    #
    # # Clonar o repositório
    # clone_repository(repo_url, destination_path)
