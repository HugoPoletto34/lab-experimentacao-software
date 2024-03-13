import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


df = pd.read_csv('lab01/sprint02/top_repositories.csv')


df['percent_closed'] = df['closed_issues'] / (df['open_issues'] + df['closed_issues']) * 100

print(df['percent_closed'].mean())
print(df['percent_closed'].median())


plt.figure(figsize=(10, 6))
plt.bar(range(len(df)), df['percent_closed'])
plt.xlabel('Repositórios')
plt.ylabel('Percentual de Issues Fechadas (%)')
plt.title('Percentual de Issues Fechadas por Repositório')
plt.xticks([], [])  

plt.axhline(df['percent_closed'].mean(), color='red', linestyle='--', label='Média')
plt.axhline(df['percent_closed'].median(), color='green', linestyle='-.', label='Mediana')
plt.legend()
plt.tight_layout()  

plt.show()
