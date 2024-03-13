import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime

df = pd.read_csv('lab01/sprint02/top_repositories.csv')

df['created_at'] = pd.to_datetime(df['created_at'])

hoje = datetime.now()
df['idade'] = (hoje - df['created_at']).dt.days // 365

# Calcular média e mediana
media = df['idade'].mean()
mediana = df['idade'].median()

sns.histplot(data=df, x='idade')
plt.axvline(media, color='r', linestyle='--', label=f'Média: {media:.2f} anos')
plt.axvline(mediana, color='g', linestyle='--', label=f'Mediana: {mediana:.2f} anos')
plt.legend()

plt.show()