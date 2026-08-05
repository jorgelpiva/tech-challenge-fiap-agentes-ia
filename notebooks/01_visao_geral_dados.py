import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    DATA_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/'
    OUT_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/'
    
    # Criar diretório se não existir
    os.makedirs(OUT_DIR, exist_ok=True)
    
    sns.set_theme(style="whitegrid")
    
    # 1. Carregar todos os 9 arquivos CSV
    files = {
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
            print(f"Sucesso ao carregar: {file}")
        except Exception as e:
            print(f"Erro ao carregar {file}: {e}")
            
    summary_lines = []
    summary_lines.append("="*50)
    summary_lines.append("RELATÓRIO DE QUALIDADE E VISÃO GERAL DOS DADOS")
    summary_lines.append("="*50 + "\n")
    
    # 2 e 4. Relatório por tabela (shape, dtypes, nulls, unique values, head) e qualidade
    for name, df in data.items():
        summary_lines.append(f"--- Tabela: {name.upper()} ---")
        summary_lines.append(f"Formato (Linhas, Colunas): {df.shape}")
        
        # dtypes
        summary_lines.append("Tipos de dados:\n" + df.dtypes.to_string())
        
        # Nulos
        nulls = df.isnull().sum()
        null_pct = (nulls / len(df)) * 100
        null_info = pd.DataFrame({'Nulos': nulls, '% Nulos': null_pct})
        if nulls.sum() > 0:
            summary_lines.append("\nValores Nulos:\n" + null_info[null_info['Nulos'] > 0].to_string())
        else:
            summary_lines.append("\nNenhum valor nulo encontrado.")
            
        # Valores Únicos
        summary_lines.append("\nValores Únicos por Coluna:\n" + df.nunique().to_string())
        
        # Duplicatas (Data quality)
        dupes = df.duplicated().sum()
        summary_lines.append(f"\nLinhas duplicadas totais: {dupes}")
        
        # Primeiras 5 linhas
        summary_lines.append("\nPrimeiras 5 linhas:\n" + df.head().to_string())
        summary_lines.append("\n" + "-"*50 + "\n")
        
    # 3. Estatísticas básicas
    summary_lines.append("="*50)
    summary_lines.append("ESTATÍSTICAS BÁSICAS (Variáveis Numéricas)")
    summary_lines.append("="*50 + "\n")
    for name, df in data.items():
        num_cols = df.select_dtypes(include=[np.number]).columns
        if len(num_cols) > 0:
            summary_lines.append(f"--- {name.upper()} ---")
            summary_lines.append(df.describe().to_string())
            summary_lines.append("\n" + "-"*30 + "\n")
            
    # 5. Contagens chave
    orders_df = data.get('orders', pd.DataFrame())
    customers_df = data.get('customers', pd.DataFrame())
    products_df = data.get('products', pd.DataFrame())
    sellers_df = data.get('sellers', pd.DataFrame())
    reviews_df = data.get('order_reviews', pd.DataFrame())
    
    tot_orders = len(orders_df)
    tot_customers = len(customers_df)
    uniq_customers = customers_df['customer_unique_id'].nunique() if 'customer_unique_id' in customers_df.columns else 0
    tot_products = len(products_df)
    tot_sellers = len(sellers_df)
    tot_reviews = len(reviews_df)
    
    summary_lines.append("="*50)
    summary_lines.append("MÉTRICAS CHAVE")
    summary_lines.append("="*50)
    summary_lines.append(f"Total de Pedidos: {tot_orders}")
    summary_lines.append(f"Total de Clientes (registros): {tot_customers}")
    summary_lines.append(f"Total de Clientes Únicos: {uniq_customers}")
    summary_lines.append(f"Total de Produtos: {tot_products}")
    summary_lines.append(f"Total de Vendedores: {tot_sellers}")
    summary_lines.append(f"Total de Avaliações: {tot_reviews}")
    summary_lines.append("\n")
    
    # Salvar relatório de texto
    with open(os.path.join(OUT_DIR, '01_summary.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(summary_lines))
        
    # 6. Gráficos
    def save_plot(filename):
        plt.tight_layout()
        plt.savefig(os.path.join(OUT_DIR, filename), dpi=300, bbox_inches='tight')
        plt.close()
        
    # - Order status distribution
    if 'order_status' in orders_df.columns:
        plt.figure(figsize=(10,6))
        sns.countplot(data=orders_df, y='order_status', order=orders_df['order_status'].value_counts().index, palette='Blues_r')
        plt.title('Distribuição de Status dos Pedidos', fontsize=14, pad=15)
        plt.xlabel('Quantidade', fontsize=12)
        plt.ylabel('Status do Pedido', fontsize=12)
        save_plot('01_distribuicao_status_pedidos.png')
        
    # - Payment type distribution
    payments_df = data.get('order_payments', pd.DataFrame())
    if 'payment_type' in payments_df.columns:
        plt.figure(figsize=(10,6))
        sns.countplot(data=payments_df, x='payment_type', order=payments_df['payment_type'].value_counts().index, palette='Greens_r')
        plt.title('Distribuição dos Tipos de Pagamento', fontsize=14, pad=15)
        plt.xlabel('Tipo de Pagamento', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        save_plot('02_distribuicao_tipos_pagamento.png')
        
    # - Review score distribution
    if 'review_score' in reviews_df.columns:
        plt.figure(figsize=(8,5))
        sns.countplot(data=reviews_df, x='review_score', palette='magma')
        plt.title('Distribuição das Notas de Avaliação', fontsize=14, pad=15)
        plt.xlabel('Nota (Review Score)', fontsize=12)
        plt.ylabel('Quantidade', fontsize=12)
        save_plot('03_distribuicao_notas_avaliacao.png')
        
    # - Top 15 product categories
    if 'product_category_name' in products_df.columns:
        plt.figure(figsize=(12,8))
        top_cats = products_df['product_category_name'].value_counts().head(15)
        sns.barplot(y=top_cats.index, x=top_cats.values, palette='viridis')
        plt.title('Top 15 Categorias de Produtos (por quantidade vendida)', fontsize=14, pad=15)
        plt.xlabel('Quantidade de Produtos', fontsize=12)
        plt.ylabel('Categoria', fontsize=12)
        save_plot('04_top15_categorias.png')
        
    # - Top 10 customer states
    if 'customer_state' in customers_df.columns:
        plt.figure(figsize=(10,6))
        top_c_states = customers_df['customer_state'].value_counts().head(10)
        sns.barplot(x=top_c_states.index, y=top_c_states.values, palette='rocket')
        plt.title('Top 10 Estados com Mais Clientes', fontsize=14, pad=15)
        plt.xlabel('Estado do Cliente', fontsize=12)
        plt.ylabel('Quantidade de Clientes', fontsize=12)
        save_plot('05_top10_estados_clientes.png')
        
    # - Top 10 seller states
    if 'seller_state' in sellers_df.columns:
        plt.figure(figsize=(10,6))
        top_s_states = sellers_df['seller_state'].value_counts().head(10)
        sns.barplot(x=top_s_states.index, y=top_s_states.values, palette='mako')
        plt.title('Top 10 Estados com Mais Vendedores', fontsize=14, pad=15)
        plt.xlabel('Estado do Vendedor', fontsize=12)
        plt.ylabel('Quantidade de Vendedores', fontsize=12)
        save_plot('06_top10_estados_vendedores.png')
        
    # - Price & Freight distributions
    order_items_df = data.get('order_items', pd.DataFrame())
    if 'price' in order_items_df.columns:
        plt.figure(figsize=(10,6))
        # Filtering outliers up to 95th percentile for better visualization
        price_data = order_items_df['price']
        sns.histplot(price_data[price_data <= price_data.quantile(0.95)], bins=50, kde=True, color='purple')
        plt.title('Distribuição de Preços dos Produtos (até o percentil 95)', fontsize=14, pad=15)
        plt.xlabel('Preço (R$)', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        save_plot('07_distribuicao_precos.png')
        
    if 'freight_value' in order_items_df.columns:
        plt.figure(figsize=(10,6))
        freight_data = order_items_df['freight_value']
        sns.histplot(freight_data[freight_data <= freight_data.quantile(0.95)], bins=50, kde=True, color='orange')
        plt.title('Distribuição do Valor de Frete (até o percentil 95)', fontsize=14, pad=15)
        plt.xlabel('Frete (R$)', fontsize=12)
        plt.ylabel('Frequência', fontsize=12)
        save_plot('08_distribuicao_frete.png')
        
    print("Análise concluída com sucesso!")
    print("Métricas chave:")
    print(f"  Total de Pedidos: {tot_orders}")
    print(f"  Total de Clientes Únicos: {uniq_customers}")
    print(f"  Total de Vendedores: {tot_sellers}")

if __name__ == "__main__":
    main()
