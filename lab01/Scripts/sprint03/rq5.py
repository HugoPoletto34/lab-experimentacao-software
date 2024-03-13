import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('lab01/sprint02/top_repositories.csv')


linguagem_count = df['primary_language'].value_counts()


plt.figure(figsize=(10, 6))
linguagem_count.plot(kind='barh')
plt.xlabel('Número de Repositórios')
plt.ylabel('Linguagem Primária')
plt.title('Distribuição das Linguagens Primárias dos Repositórios')
plt.tight_layout()
plt.show()
