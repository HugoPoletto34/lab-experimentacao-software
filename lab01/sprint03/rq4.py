import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('lab01/sprint02/top_repositories.csv')


df['updated_at'] = pd.to_datetime(df['updated_at'])

df['days_since_update'] = (datetime.now() - df['updated_at']).dt.days


media = df['days_since_update'].mean()
mediana = df['days_since_update'].median()
moda = df['days_since_update'].mode()[0]
print(media)
print(mediana)
print(moda)

plt.figure(figsize=(10, 6))
plt.scatter(df.index, df['days_since_update'])
plt.axhline(media, color='red', linestyle='--', label='Média')
plt.axhline(mediana, color='green', linestyle='-.', label='Mediana')
plt.axhline(moda, color='blue', linestyle=':', label='Moda')
plt.xlabel('Repositórios')
plt.ylabel('Dias desde a última atualização')
plt.title('Tempo até a última atualização por Repositório')
plt.legend()
plt.xticks([], [])  
plt.tight_layout()  
plt.show()
