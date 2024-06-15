import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Carregar resultados do experimento (type,query,time,size)
df = pd.read_csv('experiment_results.csv')

# Renomear as colunas para o português
column_names = {
    'type': 'Tipo', 'query': 'Consulta', 'time': 'Tempo (ms)', 'size': 'Tamanho (bytes)'
}
df.rename(columns=column_names, inplace=True)

# renomear os valores da coluna 'Consulta' para português
df['Consulta'] = df['Consulta'].replace({'Simple': 'Simples', 'Complex': 'Complexa'})

# Visualização dos resultados
plt.figure(figsize=(12, 6))
sns.boxplot(x='Consulta', y='Tempo (ms)', hue='Tipo', data=df)
plt.title('Tempo de Resposta das Consultas (ms)')
plt.savefig('response_time_comparison.png')

plt.show()

# Visualização do tamanho das respostas sem usar boxplot
plt.figure(figsize=(12, 6))
sns.barplot(x='Consulta', y='Tamanho (bytes)', hue='Tipo', data=df)
plt.title('Tamanho das Respostas (bytes)')
plt.savefig('response_size_comparison.png')
plt.show()

