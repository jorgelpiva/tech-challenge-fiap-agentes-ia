import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import matplotlib
matplotlib.use('Agg')

# Diretórios
DATA_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/'
OUT_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/'
os.makedirs(OUT_DIR, exist_ok=True)
SUMMARY_FILE = os.path.join(OUT_DIR, '03_summary.txt')

def main():
    print("Carregando datasets...")
    df_customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
    df_orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
    df_items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
    df_payments = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_payments_dataset.csv'))
    df_reviews = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_reviews_dataset.csv'))

    # Converter datas
    df_orders['order_purchase_timestamp'] = pd.to_datetime(df_orders['order_purchase_timestamp'])
    df_orders['order_delivered_customer_date'] = pd.to_datetime(df_orders['order_delivered_customer_date'])
    df_orders['order_estimated_delivery_date'] = pd.to_datetime(df_orders['order_estimated_delivery_date'])

    # Merge
    print("Mesclando dados...")
    # Considerar apenas pedidos entregues
    orders = df_orders[df_orders['order_status'] == 'delivered'].copy()
    
    # Pagamentos por pedido
    payments_agg = df_payments.groupby('order_id')['payment_value'].sum().reset_index()
    
    # Avaliações por pedido (média)
    reviews_agg = df_reviews.groupby('order_id')['review_score'].mean().reset_index()
    
    df = orders.merge(df_customers, on='customer_id', how='inner')
    df = df.merge(payments_agg, on='order_id', how='left')
    df = df.merge(reviews_agg, on='order_id', how='left')

    # Atraso na entrega (dias)
    df['delivery_delay'] = (df['order_delivered_customer_date'] - df['order_estimated_delivery_date']).dt.days

    # 1. Customer Base Analysis
    print("Análise de Base de Clientes...")
    total_unique_customers = df['customer_unique_id'].nunique()
    
    # Por estado
    state_counts = df_customers['customer_state'].value_counts()
    plt.figure(figsize=(12, 6))
    sns.barplot(x=state_counts.index, y=state_counts.values, palette='viridis')
    plt.title('Distribuição de Clientes por Estado', fontsize=14)
    plt.ylabel('Número de Clientes')
    plt.xlabel('Estado')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, '03_clientes_por_estado.png'))
    plt.close()

    # Novos clientes por mês
    df['order_month'] = df['order_purchase_timestamp'].dt.to_period('M')
    first_purchase = df.groupby('customer_unique_id')['order_purchase_timestamp'].min().reset_index()
    first_purchase['first_purchase_month'] = first_purchase['order_purchase_timestamp'].dt.to_period('M')
    new_customers_monthly = first_purchase['first_purchase_month'].value_counts().sort_index()
    
    plt.figure(figsize=(14, 6))
    new_customers_monthly.plot(kind='line', marker='o', color='teal')
    plt.title('Novos Clientes por Mês', fontsize=14)
    plt.ylabel('Quantidade de Novos Clientes')
    plt.xlabel('Mês')
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, '03_novos_clientes_mes.png'))
    plt.close()

    # 2. Purchase Behavior
    print("Análise de Comportamento de Compra...")
    orders_per_customer = df.groupby('customer_unique_id')['order_id'].nunique()
    multi_order_customers = (orders_per_customer > 1).sum()
    recompra_rate = multi_order_customers / total_unique_customers * 100

    plt.figure(figsize=(8, 6))
    sns.countplot(x=np.clip(orders_per_customer, 1, 5), palette='mako')
    plt.title('Distribuição de Pedidos por Cliente (Capped at 5)', fontsize=14)
    plt.xlabel('Número de Pedidos')
    plt.ylabel('Número de Clientes')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, '03_pedidos_por_cliente.png'))
    plt.close()

    # Tempo médio entre pedidos para clientes recorrentes
    recurring = df[df['customer_unique_id'].isin(orders_per_customer[orders_per_customer > 1].index)].copy()
    recurring = recurring.sort_values(['customer_unique_id', 'order_purchase_timestamp'])
    recurring['prev_order_date'] = recurring.groupby('customer_unique_id')['order_purchase_timestamp'].shift(1)
    recurring['days_between_orders'] = (recurring['order_purchase_timestamp'] - recurring['prev_order_date']).dt.days
    avg_days_between_orders = recurring['days_between_orders'].mean()

    # 3. Cohort Analysis
    print("Análise de Cohort...")
    df['cohort_month'] = df.groupby('customer_unique_id')['order_purchase_timestamp'].transform('min').dt.to_period('M')
    df['cohort_index'] = (df['order_month'].dt.year - df['cohort_month'].dt.year) * 12 + (df['order_month'].dt.month - df['cohort_month'].dt.month)
    
    cohort_data = df.groupby(['cohort_month', 'cohort_index'])['customer_unique_id'].nunique().reset_index()
    cohort_pivot = cohort_data.pivot(index='cohort_month', columns='cohort_index', values='customer_unique_id')
    cohort_sizes = cohort_pivot.iloc[:, 0]
    retention = cohort_pivot.divide(cohort_sizes, axis=0) * 100

    plt.figure(figsize=(16, 10))
    sns.heatmap(retention.iloc[:, 1:], annot=True, fmt='.1f', cmap='YlGnBu', vmin=0, vmax=5)
    plt.title('Matriz de Retenção de Cohorts (%)', fontsize=16)
    plt.ylabel('Mês de Aquisição (Cohort)')
    plt.xlabel('Meses Subsequentes')
    plt.tight_layout()
    plt.savefig(os.path.join(OUT_DIR, '03_cohort_retention.png'))
    plt.close()

    # 4. Churn Analysis
    print("Análise de Churn...")
    max_date = df['order_purchase_timestamp'].max()
    six_months_ago = max_date - pd.DateOffset(months=6)
    
    customer_stats = df.groupby('customer_unique_id').agg(
        last_purchase=('order_purchase_timestamp', 'max'),
        total_spent=('payment_value', 'sum'),
        total_orders=('order_id', 'nunique'),
        avg_review=('review_score', 'mean'),
        avg_delay=('delivery_delay', 'mean')
    ).reset_index()
    
    customer_stats['is_churn'] = customer_stats['last_purchase'] < six_months_ago
    churn_rate = customer_stats['is_churn'].mean() * 100

    churn_profile = customer_stats.groupby('is_churn').agg({
        'total_spent': 'mean',
        'avg_review': 'mean',
        'avg_delay': 'mean'
    })

    # 5. Customer Value
    print("Análise de Valor do Cliente...")
    total_revenue = customer_stats['total_spent'].sum()
    top_10_percent = int(0.1 * total_unique_customers)
    top_customers_revenue = customer_stats.nlargest(top_10_percent, 'total_spent')['total_spent'].sum()
    pareto_contribution = (top_customers_revenue / total_revenue) * 100

    # LTV simples = Valor Médio Gasto * Frequência Média
    aov = total_revenue / df['order_id'].nunique()
    freq = df['order_id'].nunique() / total_unique_customers
    ltv = aov * freq

    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write("=== RESUMO DA ANÁLISE DE CLIENTES E RETENÇÃO ===\n")
        f.write(f"Total de clientes únicos: {total_unique_customers}\n")
        f.write(f"Taxa de recompra: {recompra_rate:.2f}%\n")
        f.write(f"Tempo médio entre pedidos (recorrentes): {avg_days_between_orders:.1f} dias\n")
        f.write("\n=== CHURN ===\n")
        f.write(f"Taxa de Churn (inativos há > 6 meses): {churn_rate:.2f}%\n")
        f.write(f"Perfil Churn - Ticket Médio: R$ {churn_profile.loc[True, 'total_spent']:.2f}\n")
        f.write(f"Perfil Ativos - Ticket Médio: R$ {churn_profile.loc[False, 'total_spent']:.2f}\n")
        f.write(f"Perfil Churn - Avaliação Média: {churn_profile.loc[True, 'avg_review']:.2f}\n")
        f.write(f"Perfil Ativos - Avaliação Média: {churn_profile.loc[False, 'avg_review']:.2f}\n")
        f.write("\n=== VALOR DO CLIENTE ===\n")
        f.write(f"LTV Estimado Simples: R$ {ltv:.2f}\n")
        f.write(f"Pareto: Top 10% clientes contribuem com {pareto_contribution:.2f}% da receita.\n")
        
    print(f"Resumo salvo em {SUMMARY_FILE}")
    print("Gráficos gerados com sucesso.")

if __name__ == '__main__':
    main()
