import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import warnings
warnings.filterwarnings('ignore')

# Define directories
DATA_DIR = "/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/"
OUTPUT_DIR = "/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Set matplotlib backend to Agg
import matplotlib
matplotlib.use('Agg')

# Set professional style
sns.set_theme(style="whitegrid")
palette = sns.color_palette("muted")

def safe_savefig(fig, filename):
    fig.tight_layout()
    fig.savefig(os.path.join(OUTPUT_DIR, filename), dpi=300, bbox_inches='tight')
    plt.close(fig)

print("Loading datasets...")
sellers = pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv"))
order_items = pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))
orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
reviews = pd.read_csv(os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"))
products = pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv"))
translation = pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv"))
customers = pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))

print("Merging data...")
df = orders.merge(order_items, on="order_id", how="inner")
df = df.merge(sellers, on="seller_id", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(reviews[['order_id', 'review_score']].drop_duplicates(subset=['order_id']), on="order_id", how="left")
products_translated = products.merge(translation, on="product_category_name", how="left")
df = df.merge(products_translated[['product_id', 'product_category_name_english']], on="product_id", how="left")

df['order_purchase_timestamp'] = pd.to_datetime(df['order_purchase_timestamp'])
df['order_delivered_carrier_date'] = pd.to_datetime(df['order_delivered_carrier_date'])
df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')

print("Analyzing seller base...")
total_sellers = sellers['seller_id'].nunique()
active_sellers = df['seller_id'].nunique()

fig, ax = plt.subplots(figsize=(12, 6))
sellers['seller_state'].value_counts().plot(kind='bar', color=palette[0], ax=ax)
ax.set_title('Distribuição de Vendedores por Estado', fontsize=16)
ax.set_ylabel('Número de Vendedores')
ax.set_xlabel('Estado')
safe_savefig(fig, '06_sellers_by_state.png')

top_cities = sellers['seller_city'].value_counts().head(20)
fig, ax = plt.subplots(figsize=(12, 6))
top_cities.plot(kind='bar', color=palette[1], ax=ax)
ax.set_title('Top 20 Cidades por Número de Vendedores', fontsize=16)
ax.set_ylabel('Número de Vendedores')
ax.set_xlabel('Cidade')
plt.xticks(rotation=45, ha='right')
safe_savefig(fig, '06_sellers_top_cities.png')

first_sale = df.groupby('seller_id')['order_purchase_timestamp'].min().dt.to_period('M').value_counts().sort_index()
fig, ax = plt.subplots(figsize=(12, 6))
first_sale.plot(kind='line', marker='o', color=palette[2], ax=ax)
ax.set_title('Novos Vendedores por Mês (Primeira Venda)', fontsize=16)
ax.set_ylabel('Número de Novos Vendedores')
ax.set_xlabel('Mês')
plt.xticks(rotation=45)
safe_savefig(fig, '06_new_sellers_per_month.png')

print("Analyzing sales performance...")
seller_metrics = df.groupby('seller_id').agg(
    revenue=('price', 'sum'),
    orders_count=('order_id', 'nunique'),
    items_count=('order_item_id', 'count'),
    products_count=('product_id', 'nunique'),
    avg_price=('price', 'mean'),
    avg_review=('review_score', 'mean')
).reset_index()

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
sns.histplot(seller_metrics[seller_metrics['revenue'] < seller_metrics['revenue'].quantile(0.95)]['revenue'], bins=50, ax=axes[0], color=palette[3])
axes[0].set_title('Distribuição de Receita por Vendedor (Até 95º percentil)', fontsize=14)
axes[0].set_xlabel('Receita (R$)')

sns.boxplot(y=seller_metrics['revenue'], ax=axes[1], color=palette[3])
axes[1].set_yscale('log')
axes[1].set_title('Boxplot da Receita por Vendedor (Escala Log)', fontsize=14)
axes[1].set_ylabel('Receita (R$)')
safe_savefig(fig, '06_seller_revenue_dist.png')

print("Performing Pareto analysis...")
seller_metrics_sorted = seller_metrics.sort_values('revenue', ascending=False)
seller_metrics_sorted['cum_revenue'] = seller_metrics_sorted['revenue'].cumsum()
seller_metrics_sorted['cum_revenue_pct'] = seller_metrics_sorted['cum_revenue'] / seller_metrics_sorted['revenue'].sum()
seller_metrics_sorted['cum_sellers_pct'] = np.arange(1, len(seller_metrics_sorted) + 1) / len(seller_metrics_sorted)

pareto_80_idx = seller_metrics_sorted[seller_metrics_sorted['cum_revenue_pct'] >= 0.8].index[0]
pareto_80_sellers_pct = seller_metrics_sorted.loc[pareto_80_idx, 'cum_sellers_pct']

fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(seller_metrics_sorted['cum_sellers_pct'], seller_metrics_sorted['cum_revenue_pct'], color=palette[4], linewidth=2)
ax.axhline(0.8, color='red', linestyle='--', label='80% da Receita')
ax.axvline(pareto_80_sellers_pct, color='red', linestyle='--', label=f'{pareto_80_sellers_pct:.1%} dos Vendedores')
ax.set_title('Curva de Pareto de Receita por Vendedor', fontsize=16)
ax.set_xlabel('% Acumulada de Vendedores')
ax.set_ylabel('% Acumulada de Receita')
ax.legend()
safe_savefig(fig, '06_pareto_curve.png')

def gini(array):
    array = np.array(array).flatten()
    if np.amin(array) < 0:
        array -= np.amin(array)
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

gini_revenue = gini(seller_metrics['revenue'].values)

print("Analyzing quality metrics...")
fig, ax = plt.subplots(figsize=(10, 6))
sns.histplot(seller_metrics['avg_review'].dropna(), bins=20, color=palette[5], ax=ax)
ax.set_title('Distribuição da Nota Média de Avaliação por Vendedor', fontsize=16)
ax.set_xlabel('Nota Média')
safe_savefig(fig, '06_seller_avg_reviews.png')

df['processing_time_days'] = (df['order_delivered_carrier_date'] - df['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
seller_processing = df.groupby('seller_id')['processing_time_days'].mean().reset_index()

print("Analyzing category specialization...")
cat_per_seller = df.groupby('seller_id')['product_category_name_english'].nunique().reset_index()
cat_per_seller.columns = ['seller_id', 'num_categories']
cat_per_seller['type'] = np.where(cat_per_seller['num_categories'] == 1, 'Especialista', 'Generalista')
seller_metrics = seller_metrics.merge(cat_per_seller, on='seller_id', how='left')

fig, axes = plt.subplots(1, 2, figsize=(15, 6))
type_counts = cat_per_seller['type'].value_counts()
axes[0].pie(type_counts, labels=type_counts.index, autopct='%1.1f%%', colors=[palette[0], palette[1]])
axes[0].set_title('Proporção Especialistas vs Generalistas', fontsize=14)

sns.boxplot(x='type', y='revenue', data=seller_metrics, ax=axes[1], palette=[palette[0], palette[1]])
axes[1].set_yscale('log')
axes[1].set_title('Receita: Especialistas vs Generalistas (Log)', fontsize=14)
safe_savefig(fig, '06_specialist_vs_generalist.png')

print("Analyzing cross-state commerce...")
df['same_state'] = (df['customer_state'] == df['seller_state'])
cross_state_pct = (~df['same_state']).mean()

fig, ax = plt.subplots(figsize=(8, 6))
df['same_state'].value_counts(normalize=True).plot(kind='bar', color=[palette[2], palette[3]], ax=ax)
ax.set_xticklabels(['Estados Diferentes', 'Mesmo Estado'], rotation=0)
ax.set_title('Vendas: Mesmo Estado vs Estados Diferentes', fontsize=16)
ax.set_ylabel('Proporção de Pedidos')
safe_savefig(fig, '06_cross_state.png')

summary = f'''=========================================
RESUMO: ANÁLISE DE VENDEDORES (SELLERS)
=========================================

1. VISÃO GERAL
- Total de vendedores cadastrados: {total_sellers}
- Total de vendedores ativos (com vendas): {active_sellers}
- Top 3 estados com mais vendedores: {', '.join(sellers['seller_state'].value_counts().head(3).index.tolist())}

2. PERFORMANCE DE VENDAS & PARETO
- % de vendedores que geram 80% da receita: {pareto_80_sellers_pct:.1%}
- Coeficiente de Gini de concentração de receita: {gini_revenue:.3f} (muita concentração)
- Receita Média por vendedor ativo: R$ {seller_metrics['revenue'].mean():.2f}
- Mediana da Receita por vendedor: R$ {seller_metrics['revenue'].median():.2f}

3. QUALIDADE E AVALIAÇÃO
- Avaliação média dos vendedores: {seller_metrics['avg_review'].mean():.2f}
- Vendedores com nota média < 3.0: {len(seller_metrics[seller_metrics['avg_review'] < 3.0])}
- Tempo médio de processamento (compra até transportadora): {seller_processing['processing_time_days'].mean():.1f} dias

4. ESPECIALIZAÇÃO
- Vendedores especialistas (1 categoria): {len(cat_per_seller[cat_per_seller['type'] == 'Especialista'])}
- Vendedores generalistas (>1 categoria): {len(cat_per_seller[cat_per_seller['type'] == 'Generalista'])}

5. LOGÍSTICA E ESTADOS
- Vendas para clientes em estados diferentes do vendedor: {cross_state_pct:.1%}
'''

with open(os.path.join(OUTPUT_DIR, '06_summary.txt'), 'w', encoding='utf-8') as f:
    f.write(summary)

print("Analysis complete! Summary generated.")
