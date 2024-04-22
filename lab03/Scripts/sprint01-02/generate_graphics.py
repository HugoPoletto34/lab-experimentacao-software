import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Carregar o dataset
df = pd.read_csv('metrics.csv')

if __name__ == "__main__":
    # Calculando a matriz de correlação, ignorando a coluna 'name_with_owner'
    correlation_matrix = df.drop(columns='name_with_owner').corr()

    # Plotando a matriz de correlação
    plt.figure(figsize=(15, 13), dpi=100, facecolor='w', edgecolor='k', frameon=True, clear=True, linewidth=1.0,
               tight_layout=True)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', fmt=".2f", square=True)
    plt.title('Matriz de Correlação entre Métricas de Pull Requests')
    plt.savefig('graphics/correlation_matrix.png')
