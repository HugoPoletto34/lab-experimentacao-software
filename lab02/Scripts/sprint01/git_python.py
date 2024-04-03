import git
import csv
import os

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


def contar_linhas_codigo(diretorio):
    total_linhas_codigo = 0
    total_linhas_comentario = 0

    for root, dirs, files in os.walk(diretorio):
        try:

            for file in files:
                if file.endswith('.java'):
                    file_path = os.path.join(root, file)
                    # Tentar abrir o arquivo com diferentes encodings
                    for encoding in ['utf-8', 'latin1', 'cp1252']:
                        try:
                            with open(file_path, 'r', encoding=encoding) as f:
                                linhas = f.readlines()
                                in_comentario = False
                                for linha in linhas:
                                    linha = linha.strip()
                                    if linha.startswith('//') or linha == '':
                                        total_linhas_comentario += 1
                                    elif linha.startswith('/*'):
                                        total_linhas_comentario += 1
                                        in_comentario = True
                                    elif linha.endswith('*/') and in_comentario:
                                        total_linhas_comentario += 1
                                        in_comentario = False
                                    else:
                                        total_linhas_codigo += 1
                            # Se conseguirmos abrir o arquivo com sucesso, podemos parar de tentar outros encodings
                            break
                        except UnicodeDecodeError:
                            continue
        except Exception as e:
            continue
    return total_linhas_codigo, total_linhas_comentario


def ler_csv(nome_arquivo):
    dados = []
    with open(nome_arquivo, newline='') as csvfile:
        leitor_csv = csv.reader(csvfile, delimiter=',')
        for linha in leitor_csv:
            dados.append(linha)
    return dados


if __name__ == "__main__":
    # Ler o arquivo CSV
    nome_arquivo = "top_repositories_java.csv"
    dados = ler_csv(nome_arquivo)
    # remover primeira linha
    dados.pop(0)
    repo_with_error = os.listdir("repositorios_clonados");
    repos_with_loc = []
    for linha in dados:
        try:
            if linha[0].replace('/', '_') in repo_with_error:

                print(linha)
                name = linha[0]
                stars = linha[1]
                created_at = linha[2]
                releases = linha[3]

                repo_url = f"https://github.com/{name}.git"
                destination_path = f"repositorios_clonados\\{name.replace('/', '_')}"
                # clone_repository(repo_url, destination_path)

                total_linhas_codigo, total_linhas_comentario = contar_linhas_codigo(destination_path)

                print("Total de linhas de código Java:", total_linhas_codigo)
                print("Total de linhas de comentário:", total_linhas_comentario)

                repos_with_loc.append({
                    "name_with_owner": name,
                    "stars": stars,
                    "created_at": created_at,
                    "releases": releases,
                    "total_linhas_codigo": total_linhas_codigo,
                    "total_linhas_comentario": total_linhas_comentario
                })

                delete_repository(os.path.abspath(destination_path))
        except Exception as e:
            print(f"Ocorreu um erro ao clonar o repositório: {e}")

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
