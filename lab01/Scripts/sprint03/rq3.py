import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('lab01/sprint02/top_repositories_java.csv')


media = df['total_releases'].mean()
mediana = df['total_releases'].median()

print(media)
print(mediana)

plt.figure(figsize=(10, 6))
plt.bar(range(len(df)), df['total_releases'], label='Releases')
plt.axhline(media, color='red', linestyle='--', label='Média')
plt.axhline(mediana, color='green', linestyle='-.', label='Mediana')
plt.xlabel('Repositórios')
plt.ylabel('Número total de Releases')
plt.title('Número total de Releases por Repositório')
plt.legend()
plt.xticks([], [])  
plt.ylim(0, 14816)  
plt.tight_layout()  
plt.show()
