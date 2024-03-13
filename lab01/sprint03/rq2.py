import pandas as pd
import matplotlib.pyplot as plt

# Passo 1: Carregar os dados do arquivo CSV
df = pd.read_csv('lab01/sprint02/top_repositories.csv')

# Passo 2: Calcular o total de pull requests aceitas para cada número de estrelas
total_pull_requests_by_stars = df.groupby('stars')['pull_requests'].sum()

# Passo 3: Criar um gráfico para visualizar a métrica
plt.figure(figsize=(10, 6))
total_pull_requests_by_stars.plot(kind='bar', color='skyblue')
plt.xlabel('Número de Estrelas')
plt.ylabel('Total de Pull Requests Aceitas')
plt.title('Total de Pull Requests Aceitas por Número de Estrelas')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
