import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import re
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

import matplotlib
matplotlib.use('Agg')

sns.set_theme(style="whitegrid")
sns.set_palette("muted")

DATA_DIR = "/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/"
OUT_DIR = "/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/"

os.makedirs(OUT_DIR, exist_ok=True)

print("Loading datasets...")
reviews = pd.read_csv(os.path.join(DATA_DIR, "olist_order_reviews_dataset.csv"))
orders = pd.read_csv(os.path.join(DATA_DIR, "olist_orders_dataset.csv"))
items = pd.read_csv(os.path.join(DATA_DIR, "olist_order_items_dataset.csv"))
products = pd.read_csv(os.path.join(DATA_DIR, "olist_products_dataset.csv"))
translations = pd.read_csv(os.path.join(DATA_DIR, "product_category_name_translation.csv"))
customers = pd.read_csv(os.path.join(DATA_DIR, "olist_customers_dataset.csv"))
sellers = pd.read_csv(os.path.join(DATA_DIR, "olist_sellers_dataset.csv"))

print("Merging datasets...")
date_cols_orders = ['order_purchase_timestamp', 'order_approved_at', 
                   'order_delivered_carrier_date', 'order_delivered_customer_date', 
                   'order_estimated_delivery_date']
for col in date_cols_orders:
    orders[col] = pd.to_datetime(orders[col])
    
date_cols_reviews = ['review_creation_date', 'review_answer_timestamp']
for col in date_cols_reviews:
    reviews[col] = pd.to_datetime(reviews[col])

df = reviews.merge(orders, on="order_id", how="left")
df = df.merge(items, on="order_id", how="left")
df = df.merge(products, on="product_id", how="left")
df = df.merge(translations, on="product_category_name", how="left")
df = df.merge(customers, on="customer_id", how="left")
df = df.merge(sellers, on="seller_id", how="left")

df['order_purchase_month'] = df['order_purchase_timestamp'].dt.to_period('M')

with open(os.path.join(OUT_DIR, "04_summary.txt"), "w", encoding='utf-8') as f:
    f.write("=== ANÁLISE DE AVALIAÇÕES E SATISFAÇÃO ===\n\n")

print("Analyzing review scores...")
score_dist = reviews['review_score'].value_counts(normalize=True).sort_index() * 100

plt.figure(figsize=(8, 5))
ax = sns.barplot(x=score_dist.index, y=score_dist.values, palette="Blues_d")
plt.title("Distribuição das Notas de Avaliação (%)", fontsize=14)
plt.xlabel("Nota (Review Score)", fontsize=12)
plt.ylabel("Porcentagem (%)", fontsize=12)
for i, v in enumerate(score_dist.values):
    ax.text(i, v + 0.5, f"{v:.1f}%", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_review_score_distribution.png"))
plt.close()

monthly_score = df.groupby('order_purchase_month')['review_score'].mean().reset_index()
monthly_score['order_purchase_month'] = monthly_score['order_purchase_month'].dt.to_timestamp()

plt.figure(figsize=(12, 6))
sns.lineplot(data=monthly_score, x='order_purchase_month', y='review_score', marker='o')
plt.title("Evolução da Nota Média ao Longo do Tempo", fontsize=14)
plt.xlabel("Mês da Compra", fontsize=12)
plt.ylabel("Nota Média", fontsize=12)
plt.grid(True)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_review_score_evolution.png"))
plt.close()

cat_scores = df.groupby('product_category_name_english')['review_score'].agg(['mean', 'count'])
cat_scores = cat_scores[cat_scores['count'] > 50].sort_values('mean', ascending=False)

top_15 = cat_scores.head(15)
bottom_15 = cat_scores.tail(15)

plt.figure(figsize=(10, 8))
sns.barplot(x=top_15['mean'], y=top_15.index, palette="Greens_d")
plt.title("Top 15 Categorias por Nota Média (Min 50 avaliações)", fontsize=14)
plt.xlabel("Nota Média", fontsize=12)
plt.ylabel("Categoria (Inglês)", fontsize=12)
plt.xlim(3.5, 5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_top15_categories.png"))
plt.close()

plt.figure(figsize=(10, 8))
sns.barplot(x=bottom_15['mean'], y=bottom_15.index, palette="Reds_d")
plt.title("Bottom 15 Categorias por Nota Média (Min 50 avaliações)", fontsize=14)
plt.xlabel("Nota Média", fontsize=12)
plt.ylabel("Categoria (Inglês)", fontsize=12)
plt.xlim(1, 5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_bottom15_categories.png"))
plt.close()

cust_state = df.groupby('customer_state')['review_score'].mean().sort_values(ascending=False)
sell_state = df.groupby('seller_state')['review_score'].mean().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
sns.barplot(x=cust_state.index, y=cust_state.values, ax=axes[0], palette="Purples_d")
axes[0].set_title("Nota Média por Estado do Cliente", fontsize=14)
axes[0].set_ylim(3.5, 4.5)
sns.barplot(x=sell_state.index, y=sell_state.values, ax=axes[1], palette="Oranges_d")
axes[1].set_title("Nota Média por Estado do Vendedor", fontsize=14)
axes[1].set_ylim(3.5, 4.5)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_scores_by_state.png"))
plt.close()

print("Analyzing delivery impact...")
df_del = df.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date', 'review_score'])
df_del['delivery_delay_days'] = (df_del['order_delivered_customer_date'] - df_del['order_estimated_delivery_date']).dt.total_seconds() / (24*3600)

def categorize_delay(days):
    if days < 0: return 'Adiantado'
    elif days == 0: return 'No Prazo'
    elif days <= 7: return 'Atraso 1-7d'
    elif days <= 30: return 'Atraso 7-30d'
    else: return 'Atraso >30d'

df_del['delay_category'] = df_del['delivery_delay_days'].apply(categorize_delay)
delay_order = ['Adiantado', 'No Prazo', 'Atraso 1-7d', 'Atraso 7-30d', 'Atraso >30d']
delay_stats = df_del.groupby('delay_category')['review_score'].mean().reindex(delay_order)

plt.figure(figsize=(10, 6))
sns.barplot(x=delay_stats.index, y=delay_stats.values, palette="rocket")
plt.title("Nota Média de Avaliação por Status de Entrega", fontsize=14)
plt.ylabel("Nota Média", fontsize=12)
plt.ylim(1, 5)
for i, v in enumerate(delay_stats.values):
    if not np.isnan(v):
        plt.text(i, v + 0.1, f"{v:.2f}", ha='center')
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_delivery_delay_vs_score.png"))
plt.close()

df_sample = df_del.sample(min(10000, len(df_del)), random_state=42)
plt.figure(figsize=(10, 6))
sns.scatterplot(data=df_sample, x='delivery_delay_days', y='review_score', alpha=0.1)
plt.title("Atraso de Entrega (Dias) vs Nota de Avaliação", fontsize=14)
plt.xlabel("Dias de Atraso (>0 indica atraso, <0 adiantado)", fontsize=12)
plt.ylabel("Nota (Review Score)", fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(OUT_DIR, "04_delay_scatter.png"))
plt.close()

corr_delay_score = df_del['delivery_delay_days'].corr(df_del['review_score'])

print("Analyzing freight impact...")
df_freight = df.dropna(subset=['price', 'freight_value', 'review_score'])
df_freight['freight_ratio'] = df_freight['freight_value'] / (df_freight['price'] + df_freight['freight_value'])
corr_freight_score = df_freight['freight_value'].corr(df_freight['review_score'])
corr_ratio_score = df_freight['freight_ratio'].corr(df_freight['review_score'])

print("Analyzing text...")
reviews_df = df[['review_id', 'review_score', 'review_comment_message']].drop_duplicates()
reviews_df['has_comment'] = reviews_df['review_comment_message'].notna()
comment_counts = reviews_df['has_comment'].value_counts()

def clean_text(text):
    if pd.isna(text): return ""
    text = str(text).lower()
    text = re.sub(r'[^a-záéíóúçãõâêîôû\s]', '', text)
    return text

negative_reviews = reviews_df[reviews_df['review_score'].isin([1, 2])]['review_comment_message']
positive_reviews = reviews_df[reviews_df['review_score'].isin([4, 5])]['review_comment_message']

stop_words = set(['o', 'a', 'e', 'do', 'da', 'de', 'que', 'em', 'um', 'uma', 'para', 'com', 'não', 'na', 'no', 'os', 'as', 'é', 'mas', 'se', 'por', 'mais', 'como', 'muito', 'meu', 'foi', 'produto', 'veio', 'chegou', 'pra', 'eu', 'comprei', 'estou', 'tudo', 'bem', 'antes', 'dia', 'recebi', 'ainda', 'só', 'até', 'já', 'nao', 'pois', 'entregou', 'entrega', 'compra', 'loja'])

def get_top_words(series, top_n=50):
    words = []
    for text in series:
        if pd.notna(text):
            words.extend([w for w in clean_text(text).split() if len(w) > 2 and w not in stop_words])
    return pd.Series(words).value_counts().head(top_n)

top_neg = get_top_words(negative_reviews, 50) if not negative_reviews.empty else pd.Series()
top_pos = get_top_words(positive_reviews, 50) if not positive_reviews.empty else pd.Series()

df['response_time_days'] = (df['review_answer_timestamp'] - df['review_creation_date']).dt.total_seconds() / (24*3600)
avg_resp_time = df['response_time_days'].mean()

print("Running statistical tests...")
df_del['is_late'] = df_del['delivery_delay_days'] > 0
contingency = pd.crosstab(df_del['is_late'], df_del['review_score'])
chi2, p_chi2, dof, expected = stats.chi2_contingency(contingency)

late_scores = df_del[df_del['is_late']]['review_score']
ontime_scores = df_del[~df_del['is_late']]['review_score']
mwu_stat, p_mwu = stats.mannwhitneyu(ontime_scores, late_scores, alternative='greater')

with open(os.path.join(OUT_DIR, "04_summary.txt"), "a", encoding='utf-8') as f:
    f.write(f"1. Distribuição de Notas:\n")
    for idx, val in score_dist.items():
        f.write(f"   Nota {idx}: {val:.1f}%\n")
    
    f.write(f"\n2. Impacto do Atraso:\n")
    f.write(f"   Correlação Atraso vs Nota: {corr_delay_score:.3f}\n")
    f.write(f"   Teste Chi-quadrado (Atraso vs Nota) p-value: {p_chi2:.3e}\n")
    f.write(f"   Teste Mann-Whitney U (No prazo vs Atrasado) p-value: {p_mwu:.3e}\n")
    
    f.write(f"\n3. Impacto do Frete:\n")
    f.write(f"   Correlação Valor Frete vs Nota: {corr_freight_score:.3f}\n")
    f.write(f"   Correlação Proporção Frete/Total vs Nota: {corr_ratio_score:.3f}\n")
    
    f.write(f"\n4. Análise de Comentários:\n")
    f.write(f"   Avaliações com comentário: {comment_counts.get(True, 0)} ({(comment_counts.get(True, 0)/len(reviews_df))*100:.1f}%)\n")
    f.write(f"   Avaliações sem comentário: {comment_counts.get(False, 0)} ({(comment_counts.get(False, 0)/len(reviews_df))*100:.1f}%)\n")
    f.write(f"   Top 10 palavras negativas: {list(top_neg.index[:10])}\n")
    f.write(f"   Top 10 palavras positivas: {list(top_pos.index[:10])}\n")
    
    f.write(f"\n5. Tempo de Resposta (Review):\n")
    f.write(f"   Média de resposta: {avg_resp_time:.2f} dias\n")

print("Analysis complete. Outputs saved in", OUT_DIR)
