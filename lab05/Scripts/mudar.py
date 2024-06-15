import requests
import time
import json
import pandas as pd

# Token de autenticação do GitHub
TOKEN = 'seu_token_github'
HEADERS = {'Authorization': f'Bearer {TOKEN}'}

# Função para medir o tempo de resposta e tamanho da resposta para GraphQL
def measure_graphql(query):
    url = 'https://api.github.com/graphql'
    headers = {'Content-Type': 'application/json', **HEADERS}
    data = json.dumps({"query": query})

    start_time = time.time()
    response = requests.post(url, headers=headers, data=data)
    end_time = time.time()

    response_time = (end_time - start_time) * 1000  # Convertendo para milissegundos
    response_size = len(response.content)

    return response_time, response_size

# Função para medir o tempo de resposta e tamanho da resposta para REST
def measure_rest(endpoint):
    url = f'https://api.github.com/{endpoint}'
    headers = HEADERS

    start_time = time.time()
    response = requests.get(url, headers=headers)
    end_time = time.time()

    response_time = (end_time - start_time) * 1000  # Convertendo para milissegundos
    response_size = len(response.content)

    return response_time, response_size

# Consultas GraphQL
simple_query = '''
{
  user(login: "ezhulenev") {
    id
    name
    email
    location
  }
}
'''

complex_query = '''
{
  repository(owner: "tensorflow", name: "tensorflow") {
    id
    name
    stargazers {
      totalCount
    }
    forks {
      totalCount
    }
    issues {
        totalCount
    }
    pullRequests {
        totalCount
    }
    
    
  }
}
'''

# Endpoints REST
simple_endpoint = 'users/ezhulenev'
complex_endpoint = 'repos/tensorflow/tensorflow'

# Executando as medições
results = []
for _ in range(100):  # Número de repetições para obter uma média significativa
    gql_simple_time, gql_simple_size = measure_graphql(simple_query)
    gql_complex_time, gql_complex_size = measure_graphql(complex_query)
    rest_simple_time, rest_simple_size = measure_rest(simple_endpoint)
    rest_complex_time, rest_complex_size = measure_rest(complex_endpoint)

    results.append({
        'type': 'GraphQL', 'query': 'Simple', 'time': gql_simple_time, 'size': gql_simple_size
    })
    results.append({
        'type': 'GraphQL', 'query': 'Complex', 'time': gql_complex_time, 'size': gql_complex_size
    })
    results.append({
        'type': 'REST', 'query': 'Simple', 'time': rest_simple_time, 'size': rest_simple_size
    })
    results.append({
        'type': 'REST', 'query': 'Complex', 'time': rest_complex_time, 'size': rest_complex_size
    })

df = pd.DataFrame(results)
df.to_csv('experiment_results.csv', index=False)