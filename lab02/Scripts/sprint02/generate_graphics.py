import os.path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

current_dir = os.path.dirname(os.path.abspath(__file__))
# Carregar os dados do arquivo CSV
df = pd.read_csv(os.path.join(current_dir, 'top_repositories_with_loc.csv'))
graphics_path = os.path.join(current_dir, 'graphics')
if not os.path.exists(graphics_path):
    os.makedirs(graphics_path)

# Definir estilo do seaborn para os gráficos
# sns.set(style="whitegrid")
# 
# # RQ 01: Relação entre a popularidade dos repositórios (estrelas) e suas características de qualidade
# sns.pairplot(df, vars=['stars', 'cbo', 'dit', 'lcom'])
# plt.suptitle('Relação entre Popularidade e Características de Qualidade', y=1.02)
# plt.savefig(os.path.join(graphics_path, 'popularidade_caracteristicas_qualidade.png'))
# plt.close()
# 
# # RQ 02: Relação entre a maturidade dos repositórios (tempo desde a criação) e suas características de qualidade
# df['years_since_creation'] = (pd.to_datetime('now') - pd.to_datetime(df['created_at'])).dt.days / 365
# sns.pairplot(df, vars=['years_since_creation', 'cbo', 'dit', 'lcom'])
# plt.suptitle('Relação entre Maturidade e Características de Qualidade', y=1.02)
# plt.savefig(os.path.join(graphics_path, 'maturidade_caracteristicas_qualidade.png'))
# plt.close()
# 
# # RQ 03: Relação entre a atividade dos repositórios (lançamentos) e suas características de qualidade
# sns.pairplot(df, vars=['releases', 'cbo', 'dit', 'lcom'])
# plt.suptitle('Relação entre Atividade e Características de Qualidade', y=1.02)
# plt.savefig(os.path.join(graphics_path, 'atividade_caracteristicas_qualidade.png'))
# plt.close()
# 
# # RQ 04: Relação entre o tamanho dos repositórios (linhas de código) e suas características de qualidade
# sns.pairplot(df, vars=['loc', 'cbo', 'dit', 'lcom'])
# plt.suptitle('Relação entre Tamanho e Características de Qualidade', y=1.02)
# plt.savefig(os.path.join(graphics_path, 'tamanho_caracteristicas_qualidade.png'))
# plt.close()


# RQ 01: Relação entre a popularidade (estrelas) e as características de qualidade
plt.figure(figsize=(10, 6))
plt.scatter(df['stars'], df['cbo'], alpha=0.5)
plt.title('Relação entre Popularidade e Coupling Between Objects')
plt.xlabel('Estrelas')
plt.ylabel('cbo')
plt.grid(True)
plt.savefig('popularidade_vs_cbo.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['stars'], df['dit'], alpha=0.5)
plt.title('Relação entre Popularidade e Depth Inheritance Tree')
plt.xlabel('Estrelas')
plt.ylabel('DIT')
plt.grid(True)
plt.savefig('popularidade_vs_dit.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['stars'], df['lcom'], alpha=0.5)
plt.title('Relação entre Popularidade e Lack of Cohesion of Methods')
plt.xlabel('Estrelas')
plt.ylabel('LCOM')
plt.grid(True)
plt.savefig('popularidade_vs_lcom.png')
plt.close()

# RQ 02: Relação entre a maturidade (anos desde a criação) e as características de qualidade
df['created_at'] = pd.to_datetime(df['created_at'])
df['years_since_creation'] = (pd.Timestamp.now() - df['created_at']).dt.days / 365
plt.figure(figsize=(10, 6))
plt.scatter(df['years_since_creation'], df['lcom'], alpha=0.5)
plt.title('Relação entre Maturidade e Lack of Cohesion of Methods')
plt.xlabel('Anos desde a criação')
plt.ylabel('lcom')
plt.grid(True)
plt.savefig('maturidade_vs_lcom.png')
plt.close()

df['created_at'] = pd.to_datetime(df['created_at'])
df['years_since_creation'] = (pd.Timestamp.now() - df['created_at']).dt.days / 365
plt.figure(figsize=(10, 6))
plt.scatter(df['years_since_creation'], df['dit'], alpha=0.5)
plt.title('Relação entre Maturidade e Depth Inheritance Tree')
plt.xlabel('Anos desde a criação')
plt.ylabel('DIT')
plt.grid(True)
plt.savefig('maturidade_vs_dit.png')
plt.close()

df['created_at'] = pd.to_datetime(df['created_at'])
df['years_since_creation'] = (pd.Timestamp.now() - df['created_at']).dt.days / 365
plt.figure(figsize=(10, 6))
plt.scatter(df['years_since_creation'], df['cbo'], alpha=0.5)
plt.title('Relação entre Maturidade e Coupling Between Objects')
plt.xlabel('Anos desde a criação')
plt.ylabel('CBO')
plt.grid(True)
plt.savefig('maturidade_vs_cbo.png')
plt.close()

# RQ 03: Relação entre a atividade (lançamentos) e as características de qualidade
plt.figure(figsize=(10, 6))
plt.scatter(df['releases'], df['dit'], alpha=0.5)
plt.title('Relação entre Atividade e Depth Inheritance Tree')
plt.xlabel('Lançamentos')
plt.ylabel('dit')
plt.grid(True)
plt.savefig('atividade_vs_dit.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['releases'], df['cbo'], alpha=0.5)
plt.title('Relação entre Atividade e Coupling Between Objects')
plt.xlabel('Lançamentos')
plt.ylabel('CBO')
plt.grid(True)
plt.savefig('atividade_vs_cbo.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['releases'], df['lcom'], alpha=0.5)
plt.title('Relação entre Atividade e Lack of Cohesion of Methods')
plt.xlabel('Lançamentos')
plt.ylabel('LCOM')
plt.grid(True)
plt.savefig('atividade_vs_lcom.png')
plt.close()

# RQ 04: Relação entre o tamanho (loc) e as características de qualidade
plt.figure(figsize=(10, 6))
plt.scatter(df['loc'], df['cbo'], alpha=0.5)
plt.title('Relação entre Tamanho e Coupling Between Objects')
plt.xlabel('Linhas de Código')
plt.ylabel('cbo')
plt.grid(True)
plt.savefig('tamanho_vs_cbo.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['loc'], df['lcom'], alpha=0.5)
plt.title('Relação entre Tamanho e Lack of Cohesion of Methods')
plt.xlabel('Linhas de Código')
plt.ylabel('LCOM')
plt.grid(True)
plt.savefig('tamanho_vs_lcom.png')
plt.close()

plt.figure(figsize=(10, 6))
plt.scatter(df['loc'], df['dit'], alpha=0.5)
plt.title('Relação entre Tamanho e Depth Inheritance Tree')
plt.xlabel('Linhas de Código')
plt.ylabel('DIT')
plt.grid(True)
plt.savefig('tamanho_vs_dit.png')
plt.close()



