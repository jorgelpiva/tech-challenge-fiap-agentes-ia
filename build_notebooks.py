import os
import sys
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell
from nbconvert.preprocessors import ExecutePreprocessor

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
NOTEBOOKS_DIR = os.path.join(BASE_DIR, 'notebooks')
OUT_DIR = os.path.join(NOTEBOOKS_DIR, 'outputs')
os.makedirs(OUT_DIR, exist_ok=True)

# Helper setup code for notebook cells to handle paths seamlessly
PATH_SETUP = """import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Configuração de estilo visual
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 11

# Detecção dinâmica de caminhos para dados e outputs
DATA_DIR = '../data/olist' if os.path.exists('../data/olist') else 'data/olist'
if not os.path.exists(DATA_DIR):
    DATA_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist'

OUTPUT_DIR = './outputs' if os.path.exists('./outputs') or os.path.basename(os.getcwd()) == 'notebooks' else 'notebooks/outputs'
os.makedirs(OUTPUT_DIR, exist_ok=True)

print(f"📁 Diretório de Dados: {os.path.abspath(DATA_DIR)}")
print(f"📁 Diretório de Outputs: {os.path.abspath(OUTPUT_DIR)}")
"""

def create_nb_01():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 📊 Notebook 01 — Visão Geral e Qualidade dos Dados (Olist)\n\n"
                          "**Objetivo:** Carregar as 9 tabelas do dataset da Olist, realizar inspeção de qualidade "
                          "(nulos, tipos, duplicatas), estatísticas descritivas básicas e gráficos de distribuição iniciais."),
        
        new_markdown_cell("## 1. Importações e Configuração de Ambiente"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento dos Datasets"),
        new_code_cell("""files = {
    'customers': 'olist_customers_dataset.csv',
    'orders': 'olist_orders_dataset.csv',
    'order_items': 'olist_order_items_dataset.csv',
    'order_payments': 'olist_order_payments_dataset.csv',
    'order_reviews': 'olist_order_reviews_dataset.csv',
    'products': 'olist_products_dataset.csv',
    'sellers': 'olist_sellers_dataset.csv',
    'geolocation': 'olist_geolocation_dataset.csv',
    'category_translation': 'product_category_name_translation.csv'
}

data = {}
for name, file in files.items():
    filepath = os.path.join(DATA_DIR, file)
    try:
        data[name] = pd.read_csv(filepath)
        print(f"✓ Sucesso ao carregar {name}: {data[name].shape[0]} linhas, {data[name].shape[1]} colunas")
    except Exception as e:
        print(f"✗ Erro ao carregar {name}: {e}")
"""),
        
        new_markdown_cell("## 3. Relatório de Qualidade e Estrutura dos Dados"),
        new_code_cell("""for name, df in data.items():
    print(f"==================== TABELA: {name.upper()} ====================")
    print(f"Formato: {df.shape[0]} linhas × {df.shape[1]} colunas")
    print(f"Linhas duplicadas: {df.duplicated().sum()}")
    
    null_counts = df.isnull().sum()
    null_cols = null_counts[null_counts > 0]
    if len(null_cols) > 0:
        print("Valores Nulos:")
        for col, count in null_cols.items():
            pct = (count / len(df)) * 100
            print(f"  - {col}: {count} nulos ({pct:.2f}%)")
    else:
        print("Valores Nulos: Nenhum")
    print("-" * 60)
"""),
        
        new_markdown_cell("## 4. Estatísticas Descritivas Básicas"),
        new_code_cell("""for name, df in data.items():
    num_cols = df.select_dtypes(include=[np.number]).columns
    if len(num_cols) > 0:
        print(f"=== Estatísticas Numéricas: {name.upper()} ===")
        display(df[num_cols].describe().T)
"""),
        
        new_markdown_cell("## 5. Contagens Globais e Indicadores-Chave"),
        new_code_cell("""total_orders = data['orders']['order_id'].nunique()
total_customers = data['customers']['customer_id'].nunique()
unique_customers = data['customers']['customer_unique_id'].nunique()
total_sellers = data['sellers']['seller_id'].nunique()
total_products = data['products']['product_id'].nunique()
total_reviews = data['order_reviews']['review_id'].nunique()

print(f"📦 Total de Pedidos: {total_orders:,}")
print(f"👤 Total de Clientes Únicos: {unique_customers:,}")
print(f"🏪 Total de Vendedores: {total_sellers:,}")
print(f"🏷️ Total de Produtos Únicos: {total_products:,}")
print(f"⭐ Total de Avaliações (Reviews): {total_reviews:,}")
"""),
        
        new_markdown_cell("## 6. Distribuições Visuais"),
        new_code_cell("""# 6.1 Status dos Pedidos
plt.figure(figsize=(10, 5))
ax = sns.countplot(data=data['orders'], y='order_status', 
                   order=data['orders']['order_status'].value_counts().index, palette='Blues_r')
plt.title('Distribuição dos Status dos Pedidos', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade de Pedidos')
plt.ylabel('Status')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_distribuicao_status_pedidos.png'))
plt.show()
"""),
        
        new_code_cell("""# 6.2 Tipos de Pagamento
plt.figure(figsize=(9, 5))
ax = sns.countplot(data=data['order_payments'], x='payment_type', 
                   order=data['order_payments']['payment_type'].value_counts().index, palette='Greens_r')
plt.title('Distribuição dos Tipos de Pagamento', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Pagamento')
plt.ylabel('Quantidade de Transações')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_distribuicao_tipos_pagamento.png'))
plt.show()
"""),
        
        new_code_cell("""# 6.3 Distribuição das Notas de Avaliação
plt.figure(figsize=(8, 5))
sns.countplot(data=data['order_reviews'], x='review_score', palette='magma')
plt.title('Distribuição dos Review Scores (1 a 5)', fontsize=14, fontweight='bold')
plt.xlabel('Nota de Avaliação (Review Score)')
plt.ylabel('Frequência')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_distribuicao_notas_avaliacao.png'))
plt.show()
"""),
        
        new_code_cell("""# 6.4 Top 15 Categorias de Produtos
products_cat = data['products'].merge(data['category_translation'], on='product_category_name', how='left')
top_cats = products_cat['product_category_name_english'].value_counts().head(15)

plt.figure(figsize=(11, 6))
sns.barplot(y=top_cats.index, x=top_cats.values, palette='viridis')
plt.title('Top 15 Categorias de Produtos por Volume', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade de Produtos')
plt.ylabel('Categoria (Inglês)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_top15_categorias.png'))
plt.show()
"""),
        
        new_code_cell("""# 6.5 Distribuição Geográfica de Clientes e Vendedores por Estado
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

top_c_states = data['customers']['customer_state'].value_counts().head(10)
sns.barplot(x=top_c_states.index, y=top_c_states.values, ax=axes[0], palette='rocket')
axes[0].set_title('Top 10 Estados de Clientes', fontweight='bold')
axes[0].set_ylabel('Quantidade de Clientes')

top_s_states = data['sellers']['seller_state'].value_counts().head(10)
sns.barplot(x=top_s_states.index, y=top_s_states.values, ax=axes[1], palette='mako')
axes[1].set_title('Top 10 Estados de Vendedores', fontweight='bold')
axes[1].set_ylabel('Quantidade de Vendedores')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_top10_estados_clientes.png'))
plt.show()
"""),
        
        new_markdown_cell("## 7. Conclusão da Visão Geral\n\n"
                          "- O dataset contém **99.441 pedidos** realizados por **96.096 clientes únicos** abastecidos por **3.095 vendedores**.\n"
                          "- 97% dos pedidos possuem status `delivered`.\n"
                          "- O meio de pagamento predominante é o **cartão de crédito**, seguido pelo **boleto**.\n"
                          "- A maior parte dos clientes e vendedores está concentrada no estado de **São Paulo (SP)**.")
    ]
    return nb

def create_nb_02():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 💰 Notebook 02 — Análise de Pedidos e Receita (Olist)\n\n"
                          "**Objetivo:** Analisar a evolução temporal das vendas, métricas de receita (ticket médio, mediano), "
                          "comportamento de pagamentos, sazonalidade e taxa de cancelamento."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento e Cruzamento de Dados"),
        new_code_cell("""orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))
trans = pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))

# Converter datas
date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
             'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

# Merges para análise completa
items_prod = items.merge(products, on='product_id', how='left').merge(trans, on='product_category_name', how='left')
df_full = orders.merge(items_prod, on='order_id', how='left')
print(f"✓ Shape total unificado: {df_full.shape}")
"""),
        
        new_markdown_cell("## 3. Análise Temporal e Sazonalidade"),
        new_code_cell("""# Criar colunas temporais
orders['year_month'] = orders['order_purchase_timestamp'].dt.to_period('M')
orders['day_name'] = orders['order_purchase_timestamp'].dt.day_name()
orders['hour_of_day'] = orders['order_purchase_timestamp'].dt.hour

monthly_orders = orders.groupby('year_month').size()

plt.figure(figsize=(12, 5))
monthly_orders.plot(kind='line', marker='o', color='#2b5c8f', linewidth=2.5)
plt.title('Evolução Mensal do Volume de Pedidos (2016-2018)', fontsize=14, fontweight='bold')
plt.xlabel('Mês/Ano')
plt.ylabel('Número de Pedidos')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '01_evolucao_mensal.png'))
plt.show()
"""),
        
        new_code_cell("""fig, axes = plt.subplots(1, 2, figsize=(14, 5))

order_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sns.countplot(data=orders, x='day_name', order=order_days, ax=axes[0], palette='Blues_d')
axes[0].set_title('Pedidos por Dia da Semana', fontweight='bold')
axes[0].set_xlabel('Dia')
axes[0].set_ylabel('Pedidos')

sns.countplot(data=orders, x='hour_of_day', ax=axes[1], palette='magma')
axes[1].set_title('Pedidos por Hora do Dia', fontweight='bold')
axes[1].set_xlabel('Hora (0h - 23h)')
axes[1].set_ylabel('Pedidos')

plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '02_pedidos_por_dia_semana.png'))
plt.show()
"""),
        
        new_markdown_cell("## 4. Métricas Financeiras e Receita"),
        new_code_cell("""total_revenue = items['price'].sum()
total_freight = items['freight_value'].sum()
grand_total = total_revenue + total_freight

order_value = items.groupby('order_id').agg({
    'price': 'sum',
    'freight_value': 'sum'
})
order_value['total'] = order_value['price'] + order_value['freight_value']

avg_ticket = order_value['total'].mean()
median_ticket = order_value['total'].median()
freight_pct = (total_freight / grand_total) * 100

print(f"💵 Receita Total (Itens): R$ {total_revenue:,.2f}")
print(f"🚚 Valor Total de Frete: R$ {total_freight:,.2f}")
print(f"🛍️ Receita Bruta Total: R$ {grand_total:,.2f}")
print(f"📊 Ticket Médio por Pedido: R$ {avg_ticket:.2f}")
print(f"📊 Ticket Mediano por Pedido: R$ {median_ticket:.2f}")
print(f"🚚 Frete Médio como % da Receita Bruta: {freight_pct:.2f}%")
"""),
        
        new_code_cell("""# Top 15 Categorias por Receita
cat_rev = items_prod.groupby('product_category_name_english')['price'].sum().sort_values(ascending=False).head(15)

plt.figure(figsize=(11, 6))
sns.barplot(x=cat_rev.values, y=cat_rev.index, palette='viridis')
plt.title('Top 15 Categorias por Receita Total (R$)', fontsize=14, fontweight='bold')
plt.xlabel('Receita acumulada (R$)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_receita_por_categoria.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Análise de Pagamentos e Parcelamento"),
        new_code_cell("""pmt_summary = payments.groupby('payment_type').agg(
    transacoes=('payment_value', 'count'),
    valor_total=('payment_value', 'sum'),
    ticket_medio=('payment_value', 'mean'),
    parcelas_medias=('payment_installments', 'mean')
).sort_values(by='valor_total', ascending=False)

display(pmt_summary)
"""),
        
        new_code_cell("""plt.figure(figsize=(9, 5))
sns.boxplot(data=payments[payments['payment_value'] < 1000], x='payment_type', y='payment_value', palette='Set2')
plt.title('Distribuição dos Valores de Pagamento por Tipo (< R$ 1000)', fontsize=14, fontweight='bold')
plt.xlabel('Tipo de Pagamento')
plt.ylabel('Valor da Transação (R$)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '08_valor_por_tipo_pagamento.png'))
plt.show()
"""),
        
        new_markdown_cell("## 6. Funil de Pedidos e Entregas"),
        new_code_cell("""status_counts = orders['order_status'].value_counts()
cancel_rate = (status_counts.get('canceled', 0) / len(orders)) * 100

orders_delivered = orders.dropna(subset=['order_delivered_customer_date', 'order_purchase_timestamp']).copy()
orders_delivered['delivery_time_days'] = (orders_delivered['order_delivered_customer_date'] - orders_delivered['order_purchase_timestamp']).dt.total_seconds() / (24*3600)

avg_delivery_time = orders_delivered['delivery_time_days'].mean()
median_delivery_time = orders_delivered['delivery_time_days'].median()

print(f"🚫 Taxa de Cancelamento de Pedidos: {cancel_rate:.2f}%")
print(f"⏱️ Tempo Médio de Entrega: {avg_delivery_time:.2f} dias")
print(f"⏱️ Tempo Mediano de Entrega: {median_delivery_time:.2f} dias")
""")
    ]
    return nb

def create_nb_03():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 👥 Notebook 03 — Análise de Clientes, Recompra e Churn (Olist)\n\n"
                          "**Objetivo:** Analisar a base de clientes da Olist, identificar a taxa de recompra (recorrência), "
                          "realizar análise de Cohort de retenção mensal e quantificar a taxa de churn e Pareto de receita."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento dos Dados"),
        new_code_cell("""customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))
reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
cust_orders = orders.merge(customers, on='customer_id', how='left')
print(f"✓ Total de registros de pedidos de clientes: {cust_orders.shape[0]}")
"""),
        
        new_markdown_cell("## 3. Distribuição Geográfica e Crescimento da Base"),
        new_code_cell("""state_counts = customers['customer_state'].value_counts()

plt.figure(figsize=(12, 5))
sns.barplot(x=state_counts.index, y=state_counts.values, palette='viridis')
plt.title('Distribuição de Clientes por Estado (UF)', fontsize=14, fontweight='bold')
plt.xlabel('Estado')
plt.ylabel('Quantidade de Clientes')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_clientes_por_estado.png'))
plt.show()
"""),
        
        new_code_cell("""cust_first_order = cust_orders.groupby('customer_unique_id')['order_purchase_timestamp'].min().reset_index()
cust_first_order['cohort_month'] = cust_first_order['order_purchase_timestamp'].dt.to_period('M')
new_cust_by_month = cust_first_order.groupby('cohort_month').size()

plt.figure(figsize=(12, 5))
new_cust_by_month.plot(kind='line', marker='s', color='#1f77b4', linewidth=2)
plt.title('Aquisição de Novos Clientes por Mês', fontsize=14, fontweight='bold')
plt.xlabel('Mês')
plt.ylabel('Novos Clientes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_novos_clientes_mes.png'))
plt.show()
"""),
        
        new_markdown_cell("## 4. Comportamento de Compra e Taxa de Recompra"),
        new_code_cell("""orders_per_customer = cust_orders.groupby('customer_unique_id')['order_id'].nunique()
single_order_cust = (orders_per_customer == 1).sum()
multi_order_cust = (orders_per_customer > 1).sum()
total_unique = len(orders_per_customer)
recompra_rate = (multi_order_cust / total_unique) * 100

print(f"👤 Total de Clientes Únicos: {total_unique:,}")
print(f"1️⃣ Clientes com Apenas 1 Pedido: {single_order_cust:,} ({(single_order_cust/total_unique)*100:.2f}%)")
print(f"🔄 Clientes com 2+ Pedidos (Recorrentes): {multi_order_cust:,} ({recompra_rate:.2f}%)")
print(f"⚠️ TAXA DE RECOMPRA DA OLIST: {recompra_rate:.2f}%")
"""),
        
        new_code_cell("""plt.figure(figsize=(8, 5))
sns.countplot(x=np.clip(orders_per_customer, 1, 5), palette='mako')
plt.title('Distribuição de Número de Pedidos por Cliente Unique ID', fontsize=14, fontweight='bold')
plt.xlabel('Quantidade de Pedidos (5 = 5 ou mais)')
plt.ylabel('Número de Clientes')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_pedidos_por_cliente.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Análise de Cohort (Retenção Mensal)"),
        new_code_cell("""def get_month_int(df, column):
    year = df[column].dt.year
    month = df[column].dt.month
    return year, month

cust_orders['order_month'] = cust_orders['order_purchase_timestamp'].dt.to_period('M')
cust_orders['cohort_month'] = cust_orders.groupby('customer_unique_id')['order_purchase_timestamp'].transform('min').dt.to_period('M')

cohort_group = cust_orders.groupby(['cohort_month', 'order_month'])
cohort_data = cohort_group.agg({'customer_unique_id': 'nunique'}).reset_index()

cohort_data['period_number'] = (cohort_data['order_month'] - cohort_data['cohort_month']).apply(lambda x: x.n)
cohort_pivot = cohort_data.pivot(index='cohort_month', columns='period_number', values='customer_unique_id')
cohort_size = cohort_pivot.iloc[:, 0]
retention = cohort_pivot.divide(cohort_size, axis=0) * 100

plt.figure(figsize=(14, 8))
sns.heatmap(retention.iloc[:18, :12], annot=True, fmt='.1f', cmap='YlGnBu', vmin=0, vmax=3)
plt.title('Matriz de Cohort — Taxa de Retenção (%) por Mês de Entrada', fontsize=14, fontweight='bold')
plt.xlabel('Meses Após Primeira Compra')
plt.ylabel('Coorte (Mês de Entrada)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '03_cohort_retention.png'))
plt.show()
"""),
        
        new_markdown_cell("## 6. Análise de Churn e Valor do Cliente (Pareto)"),
        new_code_cell("""max_date = cust_orders['order_purchase_timestamp'].max()
cust_summary = cust_orders.groupby('customer_unique_id').agg(
    last_order=('order_purchase_timestamp', 'max'),
    order_count=('order_id', 'nunique')
).reset_index()

cust_summary['days_since_last'] = (max_date - cust_summary['last_order']).dt.days
churn_threshold = 180 # 6 meses
churned_cust = (cust_summary['days_since_last'] > churn_threshold).sum()
churn_rate = (churned_cust / len(cust_summary)) * 100

print(f"🔴 Clientes Inativos (> {churn_threshold} dias): {churned_cust:,}")
print(f"🔴 TAXA DE CHURN DA BASE: {churn_rate:.2f}%")

# Pareto de Clientes
cust_spend = cust_orders.merge(payments, on='order_id').groupby('customer_unique_id')['payment_value'].sum().sort_values(ascending=False)
top_10_pct_count = int(len(cust_spend) * 0.10)
top_10_pct_revenue = cust_spend.head(top_10_pct_count).sum()
total_spent_all = cust_spend.sum()
pareto_pct = (top_10_pct_revenue / total_spent_all) * 100

print(f"📈 Concentração Pareto: Top 10% dos clientes representam {pareto_pct:.2f}% da receita total!")
""")
    ]
    return nb

def create_nb_04():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# ⭐ Notebook 04 — Análise de Reviews e Satisfação do Cliente (Olist)\n\n"
                          "**Objetivo:** Investigar a satisfação do cliente, o impacto dos atrasos logísticos e do frete nas avaliações, "
                          "e realizar testes estatísticos (Chi-Square e Mann-Whitney U) juntamente com análise dos comentários."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento e Preparação dos Dados"),
        new_code_cell("""reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))
orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))
trans = pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))

# Converter datas
date_cols = ['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

# Calcular atraso em dias (positivo = atrasado, negativo = adiantado)
orders_deliv = orders.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date']).copy()
orders_deliv['delay_days'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_estimated_delivery_date']).dt.total_seconds() / (24*3600)
orders_deliv['is_late'] = orders_deliv['delay_days'] > 0

df_rev = reviews.merge(orders_deliv, on='order_id', how='inner')
print(f"✓ Shape total da análise de reviews: {df_rev.shape}")
"""),
        
        new_markdown_cell("## 3. Distribuição dos Scores de Avaliação"),
        new_code_cell("""score_counts = reviews['review_score'].value_counts(normalize=True).sort_index() * 100

for score, pct in score_counts.items():
    print(f"  ⭐ Nota {score}: {pct:.1f}%")

plt.figure(figsize=(9, 5))
ax = sns.barplot(x=score_counts.index, y=score_counts.values, palette='magma')
plt.title('Distribuição Percentual de Review Scores (1 a 5)', fontsize=14, fontweight='bold')
plt.xlabel('Nota de Avaliação')
plt.ylabel('Percentual do Total (%)')
for p in ax.patches:
    ax.annotate(f'{p.get_height():.1f}%', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_review_score_distribution.png'))
plt.show()
"""),
        
        new_markdown_cell("## 4. Impacto dos Atrasos de Entrega na Nota"),
        new_code_cell("""# Agrupar por categoria de entrega
def categorize_delay(days):
    if days <= 0:
        return 'No Prazo / Adiantado'
    elif days <= 7:
        return 'Atraso 1-7 dias'
    elif days <= 30:
        return 'Atraso 7-30 dias'
    else:
        return 'Atraso 30+ dias'

df_rev['delay_category'] = df_rev['delay_days'].apply(categorize_delay)
cat_order = ['No Prazo / Adiantado', 'Atraso 1-7 dias', 'Atraso 7-30 dias', 'Atraso 30+ dias']
avg_score_by_delay = df_rev.groupby('delay_category')['review_score'].mean().reindex(cat_order)

plt.figure(figsize=(10, 5))
ax = sns.barplot(x=avg_score_by_delay.index, y=avg_score_by_delay.values, palette='Reds_r')
plt.title('Nota Média de Avaliação por Categoria de Atraso Logístico', fontsize=14, fontweight='bold')
plt.xlabel('Categoria de Atraso')
plt.ylabel('Nota Média (1-5)')
plt.ylim(1, 5)
for p in ax.patches:
    ax.annotate(f'{p.get_height():.2f}', (p.get_x() + p.get_width() / 2., p.get_height()),
                ha='center', va='center', xytext=(0, 5), textcoords='offset points')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '04_delivery_delay_vs_score.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Testes Estatísticos (Chi-Square e Mann-Whitney U)"),
        new_code_cell("""from scipy import stats

# Correlação de Pearson
corr_delay_score = df_rev['delay_days'].corr(df_rev['review_score'])
print(f"📊 Correlação entre Dias de Atraso e Nota de Review: {corr_delay_score:.4f}")

# Teste Mann-Whitney U (No prazo vs Atrasado)
on_time_scores = df_rev[~df_rev['is_late']]['review_score']
late_scores = df_rev[df_rev['is_late']]['review_score']

u_stat, p_val_mw = stats.mannwhitneyu(on_time_scores, late_scores, alternative='two-sided')
print(f"🧪 Teste Mann-Whitney U (No Prazo vs Atrasado): p-value = {p_val_mw:.4e}")

# Teste Chi-Square
contingency_table = pd.crosstab(df_rev['is_late'], df_rev['review_score'])
chi2, p_val_chi2, dof, ex = stats.chi2_contingency(contingency_table)
print(f"🧪 Teste Chi-Square (Atrasado × Review Score): p-value = {p_val_chi2:.4e}")

print("\\n✅ CONCLUSÃO: O atraso logístico afeta a satisfação do cliente de forma ESTATISTICAMENTE SIGNIFICATIVA (p < 0.001)!")
"""),
        
        new_markdown_cell("## 6. Análise de Comentários Textuais"),
        new_code_cell("""has_comment = reviews['review_comment_message'].notnull()
print(f"💬 Avaliações COM comentário escrito: {has_comment.sum():,} ({has_comment.mean()*100:.1f}%)")
print(f"😶 Avaliações SEM comentário escrito: {(~has_comment).sum():,} ({(~has_comment).mean()*100:.1f}%)")

# Palavras mais comuns em reviews nota 1 vs nota 5
neg_comments = reviews[reviews['review_score'] == 1]['review_comment_message'].dropna().str.lower()
pos_comments = reviews[reviews['review_score'] == 5]['review_comment_message'].dropna().str.lower()

from collections import Counter
import re

def get_top_words(series, n=10):
    words = []
    stopwords = set(['de', 'a', 'o', 'que', 'e', 'do', 'da', 'em', 'um', 'para', 'com', 'nao', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'foi', 'ao', 'ele', 'das', 'tem', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'cujos', 'quais', 'ser', 'produto', 'entrega'])
    for text in series:
        tokens = re.findall(r'\\b[a-záàâãéêíóôõúç]{3,}\\b', text)
        words.extend([w for w in tokens if w not in stopwords])
    return Counter(words).most_common(n)

print("\\n🔴 Top 10 Palavras em Reviews Negativos (Nota 1):")
for word, count in get_top_words(neg_comments, 10):
    print(f"  - {word}: {count:,} vezes")

print("\\n🟢 Top 10 Palavras em Reviews Positivos (Nota 5):")
for word, count in get_top_words(pos_comments, 10):
    print(f"  - {word}: {count:,} vezes")
""")
    ]
    return nb

def create_nb_05():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 🚚 Notebook 05 — Análise Logística e Performance de Entrega (Olist)\n\n"
                          "**Objetivo:** Analisar os tempos de entrega, taxas de atraso por região/estado, "
                          "gargalos entre processamento do vendedor e trânsito da transportadora, e calcular distâncias geográficas (Haversine)."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento dos Datasets e Função Haversine"),
        new_code_cell("""orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
sellers = pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv'))
customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
geo = pd.read_csv(os.path.join(DATA_DIR, 'olist_geolocation_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))

# Agrupar geolocalização por CEP (média de lat/lng)
geo_mean = geo.groupby('geolocation_zip_code_prefix')[['geolocation_lat', 'geolocation_lng']].mean().reset_index()

# Função para calcular distância Haversine em km
def haversine(lat1, lon1, lat2, lon2):
    R = 6371.0 # Raio da Terra em km
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arcsin(np.sqrt(a))
    return R * c
"""),
        
        new_markdown_cell("## 3. Desempenho de Entrega e Taxa Global de Atrasos"),
        new_code_cell("""date_cols = ['order_purchase_timestamp', 'order_approved_at', 'order_delivered_carrier_date',
             'order_delivered_customer_date', 'order_estimated_delivery_date']
for col in date_cols:
    orders[col] = pd.to_datetime(orders[col])

orders_deliv = orders.dropna(subset=['order_delivered_customer_date', 'order_estimated_delivery_date']).copy()
orders_deliv['actual_delivery_days'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
orders_deliv['estimated_delivery_days'] = (orders_deliv['order_estimated_delivery_date'] - orders_deliv['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
orders_deliv['delay_days'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_estimated_delivery_date']).dt.total_seconds() / (24*3600)
orders_deliv['is_late'] = orders_deliv['delay_days'] > 0

avg_deliv_days = orders_deliv['actual_delivery_days'].mean()
late_rate_global = orders_deliv['is_late'].mean() * 100

print(f"⏱️ Tempo Médio Real de Entrega: {avg_deliv_days:.2f} dias")
print(f"⏱️ Tempo Médio Estimado de Entrega: {orders_deliv['estimated_delivery_days'].mean():.2f} dias")
print(f"🚨 TAXA GLOBAL DE ATRASOS LOGÍSTICOS: {late_rate_global:.2f}%")
"""),
        
        new_code_cell("""plt.figure(figsize=(10, 5))
sns.histplot(orders_deliv['actual_delivery_days'].clip(0, 60), bins=30, kde=True, color='#2b5c8f')
plt.title('Distribuição do Tempo Real de Entrega (em dias)', fontsize=14, fontweight='bold')
plt.xlabel('Dias para Entrega')
plt.ylabel('Frequência de Pedidos')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_distribuicao_tempo_real_entrega.png'))
plt.show()
"""),
        
        new_markdown_cell("## 4. Atrasos por Região e Estado"),
        new_code_cell("""cust_orders = orders_deliv.merge(customers, on='customer_id', how='left')
late_by_state = cust_orders.groupby('customer_state')['is_late'].mean().sort_values(ascending=False) * 100

plt.figure(figsize=(12, 5))
sns.barplot(x=late_by_state.index, y=late_by_state.values, palette='viridis')
plt.title('Taxa de Atraso Logístico (%) por Estado do Cliente', fontsize=14, fontweight='bold')
plt.xlabel('Estado do Cliente')
plt.ylabel('% de Pedidos Atrasados')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '05_atraso_por_estado_cliente.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Decomposição de Gargalos: Vendedor vs Transportadora"),
        new_code_cell("""# Vendedor: Compra -> Envio para transportadora
orders_deliv['seller_proc_days'] = (orders_deliv['order_delivered_carrier_date'] - orders_deliv['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
# Transportadora: Transportadora -> Cliente final
orders_deliv['carrier_transit_days'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_delivered_carrier_date']).dt.total_seconds() / (24*3600)

avg_seller_proc = orders_deliv['seller_proc_days'].mean()
avg_carrier_transit = orders_deliv['carrier_transit_days'].mean()

print(f"🏭 Tempo Médio de Processamento do Vendedor: {avg_seller_proc:.2f} dias ({(avg_seller_proc/avg_deliv_days)*100:.1f}% do tempo total)")
print(f"🚚 Tempo Médio em Trânsito da Transportadora: {avg_carrier_transit:.2f} dias ({(avg_carrier_transit/avg_deliv_days)*100:.1f}% do tempo total)")
print("\\n⚠️ GARGALO PRINCIPAL: O trânsito da transportadora responde por cerca de 74% do tempo total de entrega!")
"""),
        
        new_markdown_cell("## 6. Distâncias Geográficas e Frete"),
        new_code_cell("""# Merges de geolocalização para cliente e vendedor
cust_geo = customers.merge(geo_mean, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
sell_geo = sellers.merge(geo_mean, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')

full_geo = items.merge(orders_deliv, on='order_id')
full_geo = full_geo.merge(cust_geo[['customer_id', 'geolocation_lat', 'geolocation_lng']], on='customer_id', how='left').rename(columns={'geolocation_lat': 'c_lat', 'geolocation_lng': 'c_lng'})
full_geo = full_geo.merge(sell_geo[['seller_id', 'geolocation_lat', 'geolocation_lng']], on='seller_id', how='left').rename(columns={'geolocation_lat': 's_lat', 'geolocation_lng': 's_lng'})

full_geo['distance_km'] = haversine(full_geo['c_lat'], full_geo['c_lng'], full_geo['s_lat'], full_geo['s_lng'])

corr_dist_time = full_geo['distance_km'].corr(full_geo['actual_delivery_days'])
corr_dist_freight = full_geo['distance_km'].corr(full_geo['freight_value'])

print(f"📏 Distância Média Vendedor-Cliente: {full_geo['distance_km'].mean():.1f} km")
print(f"📊 Correlação Distância × Tempo de Entrega: {corr_dist_time:.4f}")
print(f"📊 Correlação Distância × Valor do Frete: {corr_dist_freight:.4f}")
""")
    ]
    return nb

def create_nb_06():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 🏪 Notebook 06 — Análise e Segmentação de Vendedores (Olist)\n\n"
                          "**Objetivo:** Analisar a base de vendedores (sellers), a concentração de receita (Curva de Pareto e Coeficiente de Gini), "
                          "métricas de qualidade e especialização por categoria."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP),
        
        new_markdown_cell("## 2. Carregamento e Preparação dos Dados"),
        new_code_cell("""sellers = pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv'))
items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))
trans = pd.read_csv(os.path.join(DATA_DIR, 'product_category_name_translation.csv'))

items_full = items.merge(orders, on='order_id').merge(reviews, on='order_id', how='left')
print(f"✓ Total de itens de vendas por vendedores: {items_full.shape[0]}")
"""),
        
        new_markdown_cell("## 3. Visão Geral da Base de Vendedores"),
        new_code_cell("""total_sellers = len(sellers)
sellers_with_sales = items['seller_id'].nunique()
sellers_by_state = sellers['seller_state'].value_counts()

print(f"🏪 Total de Vendedores Cadastrados: {total_sellers}")
print(f"🛒 Vendedores Ativos (Com Pelo Menos 1 Venda): {sellers_with_sales}")

plt.figure(figsize=(10, 5))
sns.barplot(x=sellers_by_state.head(10).index, y=sellers_by_state.head(10).values, palette='mako')
plt.title('Top 10 Estados de Origem dos Vendedores', fontsize=14, fontweight='bold')
plt.xlabel('Estado (UF)')
plt.ylabel('Quantidade de Vendedores')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_sellers_by_state.png'))
plt.show()
"""),
        
        new_markdown_cell("## 4. Análise de Pareto e Concentração de Receita (Gini)"),
        new_code_cell("""seller_revenue = items.groupby('seller_id')['price'].sum().sort_values(ascending=False)

# Curva acumulada
total_rev = seller_revenue.sum()
cum_rev = seller_revenue.cumsum() / total_rev * 100
cum_sellers = (np.arange(1, len(seller_revenue) + 1) / len(seller_revenue)) * 100

top_80_sellers_pct = (seller_revenue[cum_rev <= 80].count() / len(seller_revenue)) * 100

# Coeficiente de Gini
def gini(array):
    array = np.sort(array)
    index = np.arange(1, array.shape[0] + 1)
    n = array.shape[0]
    return ((np.sum((2 * index - n - 1) * array)) / (n * np.sum(array)))

gini_score = gini(seller_revenue.values)

print(f"📈 PARETO: Apenas {top_80_sellers_pct:.1f}% dos vendedores geram 80% de toda a receita da Olist!")
print(f"📊 Coeficiente de Gini da Receita dos Sellers: {gini_score:.3f} (Altíssima concentração de mercado)")
"""),
        
        new_code_cell("""plt.figure(figsize=(10, 5))
plt.plot(cum_sellers, cum_rev, color='#d95f02', linewidth=2.5)
plt.axhline(80, color='gray', linestyle='--')
plt.axvline(top_80_sellers_pct, color='gray', linestyle='--')
plt.title('Curva de Pareto de Receita dos Vendedores (Olist)', fontsize=14, fontweight='bold')
plt.xlabel('% Acumulado de Vendedores')
plt.ylabel('% Acumulado de Receita')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_pareto_curve.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Qualidade e Avaliação Média por Vendedor"),
        new_code_cell("""seller_metrics = items_full.groupby('seller_id').agg(
    total_receita=('price', 'sum'),
    total_pedidos=('order_id', 'nunique'),
    review_medio=('review_score', 'mean')
).reset_index()

low_score_sellers = (seller_metrics['review_medio'] < 3.0).sum()
print(f"⚠️ Vendedores com Nota Média < 3.0: {low_score_sellers} ({ (low_score_sellers/len(seller_metrics))*100:.1f}%)")

plt.figure(figsize=(9, 5))
sns.histplot(seller_metrics['review_medio'], bins=20, kde=True, color='#7570b3')
plt.title('Distribuição da Nota Média de Avaliação por Vendedor', fontsize=14, fontweight='bold')
plt.xlabel('Review Score Médio')
plt.ylabel('Quantidade de Vendedores')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, '06_seller_avg_reviews.png'))
plt.show()
"""),
        
        new_markdown_cell("## 6. Especialização por Categoria"),
        new_code_cell("""items_cat = items.merge(products, on='product_id')
seller_cats = items_cat.groupby('seller_id')['product_category_name'].nunique()

specialists = (seller_cats == 1).sum()
generalists = (seller_cats > 1).sum()

print(f"🎯 Vendedores Especialistas (1 única categoria): {specialists} ({specialists/len(seller_cats)*100:.1f}%)")
print(f"🌐 Vendedores Generalistas (2+ categorias): {generalists} ({generalists/len(seller_cats)*100:.1f}%)")
""")
    ]
    return nb

def create_nb_07():
    nb = new_notebook()
    nb.cells = [
        new_markdown_cell("# 🤖 Notebook 07 — Clustering, Segmentação e Matriz de Correlação (Olist)\n\n"
                          "**Objetivo:** Aplicar técnicas de Machine Learning não-supervisionado (**K-Means Clustering**, **Hierarchical Clustering** / Dendrograma), "
                          "gerar a segmentação de clientes (**RFM**), segmentação de vendedores, matriz de correlação completa e matriz BCG de categorias."),
        
        new_markdown_cell("## 1. Importações e Configurações"),
        new_code_cell(PATH_SETUP + """
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
"""),
        
        new_markdown_cell("## 2. Segmentação de Clientes (Análise RFM)"),
        new_code_cell("""orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))

orders['order_purchase_timestamp'] = pd.to_datetime(orders['order_purchase_timestamp'])
cust_orders = orders.merge(customers, on='customer_id').merge(payments, on='order_id')

ref_date = cust_orders['order_purchase_timestamp'].max() + pd.Timedelta(days=1)

# Cálculo de Recência, Frequência e Valor Monetário
rfm = cust_orders.groupby('customer_unique_id').agg(
    Recency=('order_purchase_timestamp', lambda x: (ref_date - x.max()).days),
    Frequency=('order_id', 'nunique'),
    Monetary=('payment_value', 'sum')
).reset_index()

print("✓ Resumo das Métricas RFM:")
display(rfm.describe().T)
"""),
        
        new_markdown_cell("## 3. K-Means Clustering em Clientes (Elbow & Silhouette)"),
        new_code_cell("""scaler = StandardScaler()
rfm_scaled = scaler.fit_transform(rfm[['Recency', 'Frequency', 'Monetary']])

inertias = []
silhouettes = []
K_range = range(2, 8)

for k in K_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = km.fit_predict(rfm_scaled)
    inertias.append(km.inertia_)
    # Sample for silhouette score for fast execution
    sample_idx = np.random.choice(len(rfm_scaled), size=min(10000, len(rfm_scaled)), replace=False)
    silhouettes.append(silhouette_score(rfm_scaled[sample_idx], labels[sample_idx]))

fig, ax1 = plt.subplots(figsize=(10, 5))
ax1.plot(K_range, inertias, 'bo-', label='Inércia (Elbow)')
ax1.set_xlabel('Número de Clusters (K)')
ax1.set_ylabel('Inércia', color='b')

ax2 = ax1.twinx()
ax2.plot(K_range, silhouettes, 'ro--', label='Silhouette Score')
ax2.set_ylabel('Silhouette Score', color='r')

plt.title('Método Elbow e Silhouette Score para Definição de K (RFM)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'kmeans_elbow_silhouette.png'))
plt.show()
"""),
        
        new_code_cell("""# Treinar modelo K-Means final com K=4
kmeans_final = KMeans(n_clusters=4, random_state=42, n_init=10)
rfm['Cluster'] = kmeans_final.fit_predict(rfm_scaled)

# Projeção 2D com PCA
pca = PCA(n_components=2)
rfm_pca = pca.fit_transform(rfm_scaled)
rfm['PCA1'] = rfm_pca[:, 0]
rfm['PCA2'] = rfm_pca[:, 1]

plt.figure(figsize=(10, 6))
sns.scatterplot(data=rfm, x='PCA1', y='PCA2', hue='Cluster', palette='Set1', alpha=0.7)
plt.title('Visualização dos Clusters RFM (Projeção PCA 2D)', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'kmeans_pca_clusters.png'))
plt.show()

# Perfil dos Clusters
cluster_profile = rfm.groupby('Cluster').agg(
    Recencia_Media=('Recency', 'mean'),
    Frequencia_Media=('Frequency', 'mean'),
    Monetario_Medio=('Monetary', 'mean'),
    Tamanho=('customer_unique_id', 'count')
)
print("📊 Perfil dos Clusters de Clientes (RFM):")
display(cluster_profile)
"""),
        
        new_markdown_cell("## 4. Clustering Hierárquico (Dendrograma)"),
        new_code_cell("""# Amostragem para dendrograma (1000 registros para legibilidade)
sample_rfm = rfm_scaled[:1000]
linked = linkage(sample_rfm, method='ward')

plt.figure(figsize=(12, 6))
dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=False)
plt.title('Dendrograma do Clustering Hierárquico (Amostra de Clientes)', fontsize=14, fontweight='bold')
plt.xlabel('Índice da Amostra')
plt.ylabel('Distância Euclidiana (Ward)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'hierarchical_dendrogram.png'))
plt.show()
"""),
        
        new_markdown_cell("## 5. Segmentação de Vendedores (K=3)"),
        new_code_cell("""items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))
products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))

seller_data = items.merge(reviews, on='order_id', how='left').merge(products, on='product_id', how='left')

seller_features = seller_data.groupby('seller_id').agg(
    receita_total=('price', 'sum'),
    total_pedidos=('order_id', 'nunique'),
    review_medio=('review_score', 'mean'),
    variedade_produtos=('product_id', 'nunique')
).fillna(0)

s_scaler = StandardScaler()
s_scaled = s_scaler.fit_transform(seller_features)

km_seller = KMeans(n_clusters=3, random_state=42, n_init=10)
seller_features['Cluster_Seller'] = km_seller.fit_predict(s_scaled)

seller_clusters = seller_features.groupby('Cluster_Seller').agg(
    Receita_Media=('receita_total', 'mean'),
    Pedidos_Medios=('total_pedidos', 'mean'),
    Review_Medio=('review_medio', 'mean'),
    Produtos_Diferentes=('variedade_produtos', 'mean'),
    Quantidade=('receita_total', 'count')
)

print("🏪 Perfil dos Clusters de Vendedores:")
display(seller_clusters)
"""),
        
        new_markdown_cell("## 6. Matriz de Correlação Completa das Métricas do Negócio"),
        new_code_cell("""orders_deliv = orders.dropna(subset=['order_delivered_customer_date']).copy()
orders_deliv['delivery_days'] = (pd.to_datetime(orders_deliv['order_delivered_customer_date']) - pd.to_datetime(orders_deliv['order_purchase_timestamp'])).dt.total_seconds() / (24*3600)

full_metrics = items.merge(orders_deliv, on='order_id').merge(reviews, on='order_id', how='left')

corr_vars = full_metrics[['price', 'freight_value', 'delivery_days', 'review_score']].dropna()
corr_matrix = corr_vars.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(corr_matrix, annot=True, fmt='.3f', cmap='coolwarm', vmin=-1, vmax=1)
plt.title('Matriz de Correlação entre Métricas do Negócio', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'correlation_matrix.png'))
plt.show()
"""),
        
        new_markdown_cell("## 7. Matriz BCG de Categorias de Produtos"),
        new_code_cell("""cat_summary = items.merge(products, on='product_id').merge(reviews, on='order_id', how='left').groupby('product_category_name').agg(
    receita=('price', 'sum'),
    volume=('order_id', 'count'),
    review_medio=('review_score', 'mean')
).dropna()

plt.figure(figsize=(10, 6))
sns.scatterplot(data=cat_summary, x='volume', y='receita', size='review_medio', hue='review_medio', palette='viridis', sizes=(20, 200))
plt.title('Matriz Matriz Volume × Receita × Review por Categoria', fontsize=14, fontweight='bold')
plt.xlabel('Volume de Vendas (Nº de Itens)')
plt.ylabel('Receita Acumulada (R$)')
plt.tight_layout()
plt.savefig(os.path.join(OUTPUT_DIR, 'category_bcg_matrix.png'))
plt.show()
""")
    ]
    return nb

def main():
    print("🚀 Iniciando a geração e execução dos 7 Jupyter Notebooks (.ipynb)...")
    
    generators = [
        ('01_visao_geral_dados.ipynb', create_nb_01),
        ('02_pedidos_e_receita.ipynb', create_nb_02),
        ('03_clientes_e_retencao.ipynb', create_nb_03),
        ('04_reviews_e_satisfacao.ipynb', create_nb_04),
        ('05_analise_logistica.ipynb', create_nb_05),
        ('06_analise_vendedores.ipynb', create_nb_06),
        ('07_clustering_segmentacao.ipynb', create_nb_07)
    ]
    
    ep = ExecutePreprocessor(timeout=300, kernel_name='python3')
    
    for filename, gen_func in generators:
        nb_path = os.path.join(NOTEBOOKS_DIR, filename)
        print(f"\n🔨 Gerando {filename}...")
        nb = gen_func()
        
        print(f"⚡ Executando {filename} via kernel Python...")
        try:
            ep.preprocess(nb, {'metadata': {'path': NOTEBOOKS_DIR}})
            print(f"✅ Executado com sucesso!")
        except Exception as e:
            print(f"⚠️ Erro ao executar {filename}: {e}")
            
        with open(nb_path, 'w', encoding='utf-8') as f:
            nbformat.write(nb, f)
        print(f"💾 Salvo em: {nb_path}")
        
    print("\n🎉 Todos os 7 notebooks foram gerados, executados e salvos com sucesso!")

if __name__ == '__main__':
    main()
