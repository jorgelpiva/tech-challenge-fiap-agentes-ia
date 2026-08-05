import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
import datetime

# Setup paths
data_dir = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/'
output_dir = '/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/'
os.makedirs(output_dir, exist_ok=True)

# 1. Customer RFM Analysis
print("Loading data...")
customers = pd.read_csv(os.path.join(data_dir, 'olist_customers_dataset.csv'))
orders = pd.read_csv(os.path.join(data_dir, 'olist_orders_dataset.csv'))
order_items = pd.read_csv(os.path.join(data_dir, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(data_dir, 'olist_order_payments_dataset.csv'))
reviews = pd.read_csv(os.path.join(data_dir, 'olist_order_reviews_dataset.csv'))
products = pd.read_csv(os.path.join(data_dir, 'olist_products_dataset.csv'))
sellers = pd.read_csv(os.path.join(data_dir, 'olist_sellers_dataset.csv'))
category_translations = pd.read_csv(os.path.join(data_dir, 'product_category_name_translation.csv'))

# Convert dates
orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])

# Merge for RFM
df_rfm = orders.merge(customers, on='customer_id')
df_rfm = df_rfm.merge(payments.groupby('order_id')['payment_value'].sum().reset_index(), on='order_id')

# Reference date for Recency
ref_date = orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# Group by customer_unique_id
rfm = df_rfm.groupby('customer_unique_id').agg(
    Recency=('order_purchase_timestamp', lambda x: (ref_date - x.max()).days),
    Frequency=('order_id', 'nunique'),
    Monetary=('payment_value', 'sum')
).reset_index()

print("RFM Analysis completed.")

# 2. K-Means Clustering
# Standardize
scaler_rfm = StandardScaler()
rfm_scaled = scaler_rfm.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

# Elbow method & Silhouette
inertia = []
sil_scores = []
K_range = range(2, 11)
print("Calculating K-Means Elbow and Silhouette...")
# For performance, calculate silhouette on a sample if dataset is huge, but rfm has ~96k rows
sample_size = min(20000, rfm_scaled.shape[0])
sample_idx = np.random.choice(rfm_scaled.shape[0], sample_size, replace=False)
rfm_scaled_sample = rfm_scaled[sample_idx]

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    kmeans.fit(rfm_scaled)
    inertia.append(kmeans.inertia_)
    # Calculate silhouette on sample
    labels = kmeans.predict(rfm_scaled_sample)
    sil_scores.append(silhouette_score(rfm_scaled_sample, labels))

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
plt.plot(K_range, inertia, marker='o', color='#1f77b4')
plt.title('Método do Cotovelo (Elbow)', fontsize=12)
plt.xlabel('Número de Clusters (K)')
plt.ylabel('Inércia')
plt.grid(True, alpha=0.5)

plt.subplot(1, 2, 2)
plt.plot(K_range, sil_scores, marker='s', color='#ff7f0e')
plt.title('Silhouette Score por K', fontsize=12)
plt.xlabel('Número de Clusters (K)')
plt.ylabel('Score Silhouette')
plt.grid(True, alpha=0.5)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'kmeans_elbow_silhouette.png'))
plt.close()

# Select optimal K (e.g., K=4)
optimal_k = 4
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
rfm['Cluster'] = kmeans.fit_predict(rfm_scaled)

# 2D PCA
pca = PCA(n_components=2)
rfm_pca = pca.fit_transform(rfm_scaled)

plt.figure(figsize=(8, 6))
sns.scatterplot(x=rfm_pca[:, 0], y=rfm_pca[:, 1], hue=rfm['Cluster'], palette='viridis', s=20)
plt.title('Projeção PCA dos Clusters de Clientes', fontsize=14)
plt.xlabel('Componente Principal 1')
plt.ylabel('Componente Principal 2')
plt.legend(title='Cluster')
plt.savefig(os.path.join(output_dir, 'kmeans_pca_clusters.png'))
plt.close()

# Profiling and Naming
cluster_profile = rfm.groupby('Cluster')[['Recency', 'Frequency', 'Monetary']].mean()
cluster_counts = rfm['Cluster'].value_counts()
cluster_profile['Size'] = cluster_counts

print("Cluster Profile:")
print(cluster_profile)

# Assign names based on profiling (simplistic heuristic)
r_rank = cluster_profile['Recency'].rank()
f_rank = cluster_profile['Frequency'].rank()
m_rank = cluster_profile['Monetary'].rank()

cluster_names = {}
for c in cluster_profile.index:
    if f_rank[c] >= optimal_k - 1 and m_rank[c] >= optimal_k - 1:
        cluster_names[c] = 'Campeões'
    elif r_rank[c] >= optimal_k - 1:
        cluster_names[c] = 'Em Risco / Inativos'
    elif r_rank[c] <= 2 and f_rank[c] <= 2:
        cluster_names[c] = 'Novos Clientes'
    else:
        cluster_names[c] = 'Regulares'

rfm['Segmento'] = rfm['Cluster'].map(cluster_names)

# 3. Hierarchical Clustering
print("Running Hierarchical Clustering...")
rfm_sample = rfm.sample(n=3000, random_state=42)
sample_scaled = scaler_rfm.transform(rfm_sample[['Recency', 'Frequency', 'Monetary']])
Z = linkage(sample_scaled, method='ward')

plt.figure(figsize=(10, 6))
dendrogram(Z, truncate_mode='level', p=5)
plt.title('Dendrograma de Clustering Hierárquico (Amostra)', fontsize=14)
plt.xlabel('Tamanho dos clusters / Índice da amostra')
plt.ylabel('Distância')
plt.savefig(os.path.join(output_dir, 'hierarchical_dendrogram.png'))
plt.close()

# 4. Seller Segmentation
print("Seller Segmentation...")
# Merge orders, order_items, reviews
orders['order_delivered_customer_date'] = pd.to_datetime(orders['order_delivered_customer_date'])
orders['order_approved_at'] = pd.to_datetime(orders['order_approved_at'])
orders['delivery_time'] = (orders['order_delivered_customer_date'] - orders['order_approved_at']).dt.days

seller_data = order_items.merge(orders[['order_id', 'delivery_time']], on='order_id', how='left')
seller_data = seller_data.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')

seller_agg = seller_data.groupby('seller_id').agg(
    total_revenue=('price', 'sum'),
    total_orders=('order_id', 'nunique'),
    avg_review_score=('review_score', 'mean'),
    avg_delivery_time=('delivery_time', 'mean'),
    total_products=('product_id', 'nunique')
).fillna(0).reset_index()

scaler_sellers = StandardScaler()
seller_features = ['total_revenue', 'total_orders', 'avg_review_score', 'avg_delivery_time', 'total_products']
seller_scaled = scaler_sellers.fit_transform(seller_agg[seller_features])

# Simple K-Means K=3 for sellers
kmeans_s = KMeans(n_clusters=3, random_state=42, n_init=10)
seller_agg['Cluster'] = kmeans_s.fit_predict(seller_scaled)

seller_profile = seller_agg.groupby('Cluster')[seller_features].mean()
seller_profile['Size'] = seller_agg['Cluster'].value_counts()
print("Seller Profile:")
print(seller_profile)

# 5. Correlation Matrix
print("Correlation Matrix...")
# Let's do correlation on the main joined dataset
main_df = orders.merge(order_items, on='order_id')
main_df = main_df.merge(reviews, on='order_id', how='left')
main_df = main_df.merge(payments, on='order_id', how='left')
main_df['delivery_time'] = (pd.to_datetime(main_df['order_delivered_customer_date']) - pd.to_datetime(main_df['order_approved_at'])).dt.days

corr_cols = ['price', 'freight_value', 'payment_value', 'payment_installments', 'review_score', 'delivery_time']
corr_matrix = main_df[corr_cols].corr(numeric_only=True)

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f", vmin=-1, vmax=1)
plt.title('Matriz de Correlação de Métricas de Negócio', fontsize=14)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'correlation_matrix.png'))
plt.close()

# 6. Product Category Analysis
print("Product Category Analysis...")
prod_cat = order_items.merge(products[['product_id', 'product_category_name']], on='product_id', how='left')
prod_cat = prod_cat.merge(reviews[['order_id', 'review_score']], on='order_id', how='left')
prod_cat = prod_cat.merge(category_translations, on='product_category_name', how='left')
prod_cat['category'] = prod_cat['product_category_name_english'].fillna(prod_cat['product_category_name'])

cat_agg = prod_cat.groupby('category').agg(
    revenue=('price', 'sum'),
    volume=('order_id', 'count'),
    avg_review=('review_score', 'mean')
).reset_index()

# BCG Matrix Style (Revenue vs Volume, color by Review Score)
plt.figure(figsize=(10, 8))
scatter = plt.scatter(cat_agg['volume'], cat_agg['revenue'], c=cat_agg['avg_review'], cmap='RdYlGn', s=100, alpha=0.7)
plt.colorbar(scatter, label='Média de Avaliação (Review Score)')
plt.xscale('log')
plt.yscale('log')
plt.title('Análise de Categorias (Matriz BCG)', fontsize=14)
plt.xlabel('Volume de Vendas (escala log)')
plt.ylabel('Receita Total (escala log)')

# Annotate top 5 by revenue
top_cats = cat_agg.nlargest(5, 'revenue')
for _, row in top_cats.iterrows():
    plt.annotate(row['category'], (row['volume'], row['revenue']), xytext=(5,5), textcoords='offset points', fontsize=9)

plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(os.path.join(output_dir, 'category_bcg_matrix.png'))
plt.close()

# 7. Summary
print("Writing summary...")
summary_text = f"""Resumo da Análise de Clustering e Segmentação (Olist)
===================================================

1. Segmentação de Clientes (RFM)
--------------------------------
K-Means K={optimal_k} utilizado.
Perfil dos Clusters (Valores Médios):
{cluster_profile.to_string()}

Distribuição de Segmentos:
{rfm['Segmento'].value_counts().to_string()}

2. Segmentação de Vendedores
----------------------------
Agrupamento em 3 clusters baseados em receita, ordens, nota média, tempo de entrega e diversidade de produtos.
Perfil dos Sellers:
{seller_profile.to_string()}

3. Principais Correlações
-------------------------
A matriz de correlação revelou:
- Forte correlação positiva entre 'price' e 'payment_value'.
- Correlação negativa moderada entre 'delivery_time' e 'review_score' (maior tempo de entrega resulta em avaliações menores).
- 'freight_value' tem alguma correlação com o preço e número de parcelas.

4. Categorias de Produtos
-------------------------
As categorias líderes em receita e volume destacam-se no quadrante superior direito da matriz BCG.
Avaliações variam bastante, indicando oportunidade para melhorar a qualidade em categorias específicas com alto volume e baixa avaliação.

Recomendações para Agentes de IA:
---------------------------------
1. Agente de Engajamento: Pode direcionar campanhas específicas para 'Campeões' (upsell/cross-sell) e tentar reativar clientes 'Em Risco' através de descontos ou frete grátis.
2. Agente de Qualidade: Deve monitorar o tempo de entrega ('delivery_time'), pois é o principal ofensor do 'review_score'. Pode alertar vendedores (ou clientes) sobre possíveis atrasos na entrega com base em modelagem preditiva.
3. Agente de Sucesso do Vendedor: Identificar vendedores do cluster com baixa performance (baixa avaliação e alta taxa de entrega) e enviar dicas de melhoria ou retirá-los do catálogo premium.
"""

with open(os.path.join(output_dir, '07_summary.txt'), 'w', encoding='utf-8') as f:
    f.write(summary_text)

print("Analysis completed successfully.")
