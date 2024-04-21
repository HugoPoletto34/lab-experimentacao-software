import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('metrics.csv')  # Substitua 'seu_dataset.csv' pelo nome do seu arquivo CSV

# Definição de Métricas
metrics = {
    'Tamanho': ['num_arquivos', 'num_linhas_adicionadas', 'num_linhas_deletadas'],
    'Tempo de Análise': ['tempo_analise'],
    'Descrição': ['num_caracteres_descricao'],
    'Interações': ['num_participantes', 'num_comentarios']
}

# Calculando a matriz de correlação
correlation_matrix = df.corr()

# Plotando a matriz de correlação
plt.figure(figsize=(15, 13), dpi=100, facecolor='w', edgecolor='k', frameon=True, clear=True, linewidth=1.0, tight_layout=True)
sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
plt.title('Matriz de Correlação entre Métricas e Feedback Final das Revisões')
plt.savefig('graphics/correlation_matrix.png')
plt.show()