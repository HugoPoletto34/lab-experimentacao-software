import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


df = pd.read_csv('lab01/sprint02/top_repositories.csv')



media = df['pull_requests'].mean()
mediana = df['pull_requests'].median()
print(media)
print(mediana)


plt.figure(figsize=(10, 6))
plt.bar(range(len(df)), df['pull_requests'], label='Pull Requests')
plt.axhline(media, color='red', linestyle='--', label='Média')
plt.axhline(mediana, color='green', linestyle='-.', label='Mediana')
plt.xlabel('Repositórios')
plt.ylabel('Número total de Pull Requests aceitas')
plt.title('Número total de Pull Requests aceitas por Repositório')
plt.legend()
plt.xticks([], [])  
plt.tight_layout()  
plt.show()
