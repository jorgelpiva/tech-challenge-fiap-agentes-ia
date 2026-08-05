import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

# Set paths
DATA_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/'
OUTPUT_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("1. Loading datasets...")
orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))
translations = pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))
customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))

# Process datetimes
datetime_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
for col in datetime_cols:
    orders[col] = pd.to_datetime(orders[col])

# Merges
print("Merging data...")
products = pd.merge(products, translations, on='product_category_name', how='left')
df_main = orders.merge(customers, on='customer_id', how='left')

# order items full details
df_items = df_main.merge(items, on='order_id', how='inner').merge(products, on='product_id', how='left')

# order level payments
order_payments = payments.groupby('order_id').agg(
    total_payment=('payment_value', 'sum'),
    payment_installments=('payment_installments', 'max')
).reset_index()

df_orders_full = df_main.merge(order_payments, on='order_id', how='left')

# Setup style
sns.set_theme(style="whitegrid")
palette_name = "viridis"

summary = []
summary.append("=== ANÁLISE DE PEDIDOS E RECEITA ===")

# --- 2. Temporal Analysis ---
print("2. Running temporal analysis...")
df_orders_full['year_month'] = df_orders_full['order_purchase_timestamp'].dt.to_period('M').astype(str)
df_orders_full['day_of_week'] = df_orders_full['order_purchase_timestamp'].dt.dayofweek
df_orders_full['hour_of_day'] = df_orders_full['order_purchase_timestamp'].dt.hour

monthly_orders = df_orders_full.groupby('year_month').size()
monthly_revenue = df_orders_full.groupby('year_month')['total_payment'].sum()

fig, ax1 = plt.subplots(figsize=(14, 7))
sns.lineplot(x=monthly_orders.index, y=monthly_orders.values, marker='o', ax=ax1, color='#1f77b4', label='Nº Pedidos')
ax1.set_title('Evolução Mensal - Pedidos e Receita', fontsize=16)
ax1.set_xlabel('Mês/Ano', fontsize=12)
ax1.set_ylabel('Número de Pedidos', color='#1f77b4', fontsize=12)
ax1.tick_params(axis='y', labelcolor='#1f77b4')
plt.xticks(rotation=45)

ax2 = ax1.twinx()
sns.lineplot(x=monthly_revenue.index, y=monthly_revenue.values, marker='s', ax=ax2, color='#2ca02c', label='Receita')
ax2.set_ylabel('Receita (R$)', color='#2ca02c', fontsize=12)
ax2.tick_params(axis='y', labelcolor='#2ca02c')
fig.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_evolucao_mensal.png'))
plt.close()

# Day of week
plt.figure(figsize=(10, 6))
days_map = {0:'Seg', 1:'Ter', 2:'Qua', 3:'Qui', 4:'Sex', 5:'Sáb', 6:'Dom'}
df_orders_full['day_name'] = df_orders_full['day_of_week'].map(days_map)
order_days = ['Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sáb', 'Dom']
sns.countplot(data=df_orders_full, x='day_name', order=order_days, palette=palette_name)
plt.title('Compras por Dia da Semana', fontsize=14)
plt.xlabel('Dia da Semana')
plt.ylabel('Total de Pedidos')
plt.savefig(os.path.join(OUTPUT_DIR, '02_pedidos_por_dia_semana.png'))
plt.close()

# Hour of day
plt.figure(figsize=(12, 6))
sns.countplot(data=df_orders_full, x='hour_of_day', palette="magma")
plt.title('Compras por Hora do Dia', fontsize=14)
plt.xlabel('Hora do Dia')
plt.ylabel('Total de Pedidos')
plt.savefig(os.path.join(OUTPUT_DIR, '03_pedidos_por_hora.png'))
plt.close()

# --- 3. Revenue Analysis ---
print("3. Running revenue analysis...")
total_revenue = df_orders_full['total_payment'].sum()
valid_tickets = df_orders_full[(df_orders_full['total_payment'] > 0) & (df_orders_full['total_payment'].notnull())]['total_payment']
avg_ticket = valid_tickets.mean()
med_ticket = valid_tickets.median()

summary.append("\n--- RECEITA ---")
summary.append(f"Receita Total: R$ {total_revenue:,.2f}")
summary.append(f"Ticket Médio: R$ {avg_ticket:.2f}")
summary.append(f"Ticket Mediano: R$ {med_ticket:.2f}")

cat_rev = df_items.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(20)
plt.figure(figsize=(12, 8))
sns.barplot(x=cat_rev.values, y=cat_rev.index, palette=palette_name)
plt.title('Top 20 Categorias por Receita (R$)', fontsize=14)
plt.xlabel('Receita')
plt.ylabel('Categoria')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_receita_por_categoria.png'))
plt.close()

state_rev = df_orders_full.groupby('customer_state')['total_payment'].sum().sort_values(ascending=False).head(10)
plt.figure(figsize=(10, 6))
sns.barplot(x=state_rev.index, y=state_rev.values, palette=palette_name)
plt.title('Top 10 Estados por Receita', fontsize=14)
plt.xlabel('Estado')
plt.ylabel('Receita Total (R$)')
plt.savefig(os.path.join(OUTPUT_DIR, '05_receita_por_estado.png'))
plt.close()

plt.figure(figsize=(14, 6))
plt.subplot(1, 2, 1)
sns.histplot(valid_tickets[valid_tickets < 1000], bins=50, kde=True, color='purple')
plt.title('Distribuição de Ticket (Até R$ 1000)')
plt.xlabel('Valor (R$)')
plt.subplot(1, 2, 2)
sns.boxplot(y=valid_tickets[valid_tickets < 1000], color='purple')
plt.title('Boxplot de Ticket')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_distribuicao_receita.png'))
plt.close()

df_items['freight_pct'] = (df_items['freight_value'] / (df_items['price'] + df_items['freight_value'])) * 100
avg_freight_pct = df_items.replace([np.inf, -np.inf], np.nan)['freight_pct'].dropna().mean()
summary.append(f"Frete Médio como % do Valor Total (Item): {avg_freight_pct:.2f}%")

# --- 4. Payment Analysis ---
print("4. Running payment analysis...")
pay_count = payments['payment_type'].value_counts()
pay_value = payments.groupby('payment_type')['payment_value'].sum().sort_values(ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))
axes[0].pie(pay_count.values, labels=pay_count.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set2"))
axes[0].set_title('Tipos de Pagamento por Volume (Qtd)')
axes[1].pie(pay_value.values, labels=pay_value.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette("Set3"))
axes[1].set_title('Tipos de Pagamento por Receita (R$)')
plt.savefig(os.path.join(OUTPUT_DIR, '07_tipos_pagamento.png'))
plt.close()

avg_inst_cc = payments[payments['payment_type'] == 'credit_card']['payment_installments'].mean()
summary.append("\n--- PAGAMENTOS ---")
summary.append(f"Média de Parcelas (Cartão de Crédito): {avg_inst_cc:.2f}")

plt.figure(figsize=(12, 6))
sns.boxplot(data=payments[payments['payment_value'] < 1000], x='payment_type', y='payment_value', palette='Set2')
plt.title('Valor de Pagamento por Tipo (Até R$ 1000)', fontsize=14)
plt.xlabel('Tipo de Pagamento')
plt.ylabel('Valor (R$)')
plt.savefig(os.path.join(OUTPUT_DIR, '08_valor_por_tipo_pagamento.png'))
plt.close()

# --- 5. Order Funnel ---
print("5. Running funnel analysis...")
status_counts = orders['order_status'].value_counts()
cancel_rate = (status_counts.get('canceled', 0) / len(orders)) * 100

summary.append("\n--- FUNIL E ENTREGAS ---")
summary.append(f"Total de Pedidos: {len(orders):,}")
summary.append(f"Taxa de Cancelamento: {cancel_rate:.2f}%")

plt.figure(figsize=(10, 5))
sns.barplot(x=status_counts.values, y=status_counts.index, palette='rocket')
plt.title('Distribuição de Status dos Pedidos')
plt.xlabel('Quantidade')
plt.ylabel('Status')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '09_status_pedidos.png'))
plt.close()

delivered = orders[orders['order_status'] == 'delivered'].copy()
delivered['delivery_time_days'] = (delivered['order_delivered_customer_date'] - delivered['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
valid_delivery = delivered['delivery_time_days'].dropna()

plt.figure(figsize=(10, 5))
sns.histplot(valid_delivery[valid_delivery < 60], bins=60, kde=True, color='teal')
plt.title('Tempo de Entrega em Dias (até 60 dias)', fontsize=14)
plt.xlabel('Dias')
plt.ylabel('Quantidade')
plt.savefig(os.path.join(OUTPUT_DIR, '10_tempo_entrega.png'))
plt.close()

summary.append(f"Tempo Médio de Entrega: {valid_delivery.mean():.2f} dias")
summary.append(f"Tempo Mediano de Entrega: {valid_delivery.median():.2f} dias")

# --- 6. Correlations ---
print("6. Running correlation analysis...")
items_reviews = df_items.merge(reviews[['order_id', 'review_score']], on='order_id', how='left').dropna(subset=['review_score', 'price', 'freight_value'])
corr_price_freight = items_reviews['price'].corr(items_reviews['freight_value'])
corr_price_review = items_reviews['price'].corr(items_reviews['review_score'])
corr_freight_review = items_reviews['freight_value'].corr(items_reviews['review_score'])

summary.append("\n--- CORRELAÇÕES ---")
summary.append(f"Preço vs Frete: {corr_price_freight:.4f}")
summary.append(f"Preço vs Nota de Avaliação: {corr_price_review:.4f}")
summary.append(f"Frete vs Nota de Avaliação: {corr_freight_review:.4f}")

# --- 7. Save Summary ---
print("7. Saving summary...")
with open(os.path.join(OUTPUT_DIR, '02_summary.txt'), 'w', encoding='utf-8') as f:
    f.write("\n".join(summary))

print("Script execution complete! All results saved.")
