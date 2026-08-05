import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import datetime

# Use Agg backend for non-interactive plotting
matplotlib.use('Agg')

# Configure paths
DATA_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/data/olist/'
OUTPUT_DIR = '/home/jorge/Documents/tech-challenge-agentes-ia/notebooks/outputs/'
os.makedirs(OUTPUT_DIR, exist_ok=True)
SUMMARY_FILE = os.path.join(OUTPUT_DIR, '05_summary.txt')

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # Convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])

    # Haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def main():
    print("Iniciando análise logística...")
    
    # 1. Load data
    print("Carregando datasets...")
    orders = pd.read_csv(os.path.join(DATA_DIR, 'olist_orders_dataset.csv'))
    order_items = pd.read_csv(os.path.join(DATA_DIR, 'olist_order_items_dataset.csv'))
    sellers = pd.read_csv(os.path.join(DATA_DIR, 'olist_sellers_dataset.csv'))
    customers = pd.read_csv(os.path.join(DATA_DIR, 'olist_customers_dataset.csv'))
    geo = pd.read_csv(os.path.join(DATA_DIR, 'olist_geolocation_dataset.csv'))
    products = pd.read_csv(os.path.join(DATA_DIR, 'olist_products_dataset.csv'))
    
    # Convert datetime columns
    date_cols = ['order_purchase_timestamp', 'order_approved_at', 
                 'order_delivered_carrier_date', 'order_delivered_customer_date', 
                 'order_estimated_delivery_date']
    for col in date_cols:
        orders[col] = pd.to_datetime(orders[col])
        
    # Filter delivered orders
    delivered_orders = orders[orders['order_status'] == 'delivered'].copy()
    
    # Calculate geolocation means per zip code
    geo_mean = geo.groupby('geolocation_zip_code_prefix').agg({
        'geolocation_lat': 'mean',
        'geolocation_lng': 'mean'
    }).reset_index()
    
    # Merge datasets
    print("Realizando merges...")
    # Customers with geo
    cust_geo = customers.merge(geo_mean, left_on='customer_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
    cust_geo = cust_geo.rename(columns={'geolocation_lat': 'cust_lat', 'geolocation_lng': 'cust_lng'})
    
    # Sellers with geo
    sell_geo = sellers.merge(geo_mean, left_on='seller_zip_code_prefix', right_on='geolocation_zip_code_prefix', how='left')
    sell_geo = sell_geo.rename(columns={'geolocation_lat': 'sell_lat', 'geolocation_lng': 'sell_lng'})
    
    # Merge orders with customers
    df = delivered_orders.merge(cust_geo, on='customer_id', how='left')
    
    # Merge order items with products and sellers
    items_prod_sell = order_items.merge(products, on='product_id', how='left')
    items_prod_sell = items_prod_sell.merge(sell_geo, on='seller_id', how='left')
    
    # Calculate product volume
    items_prod_sell['product_volume_cm3'] = items_prod_sell['product_length_cm'] * items_prod_sell['product_width_cm'] * items_prod_sell['product_height_cm']
    
    # Join orders with items (this can create multiple rows per order)
    df_full = df.merge(items_prod_sell, on='order_id', how='inner')
    
    # Calculate distances
    df_full['distance_km'] = haversine(
        df_full['cust_lat'], df_full['cust_lng'],
        df_full['sell_lat'], df_full['sell_lng']
    )
    
    # --- 2. Delivery Time Analysis ---
    print("Analisando tempo de entrega...")
    # Keep only order-level for delivery times to avoid duplicates
    orders_deliv = df.copy()
    orders_deliv = orders_deliv.dropna(subset=['order_purchase_timestamp', 'order_delivered_customer_date', 'order_estimated_delivery_date'])
    
    orders_deliv['actual_delivery_days'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
    orders_deliv['estimated_delivery_days'] = (orders_deliv['order_estimated_delivery_date'] - orders_deliv['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
    orders_deliv['delivery_accuracy'] = (orders_deliv['order_delivered_customer_date'] - orders_deliv['order_estimated_delivery_date']).dt.total_seconds() / (24*3600)
    
    orders_deliv['is_late'] = orders_deliv['delivery_accuracy'] > 0
    overall_late_pct = orders_deliv['is_late'].mean() * 100
    
    # Charts for delivery
    plt.figure(figsize=(10,6))
    sns.histplot(orders_deliv['actual_delivery_days'].clip(0, 60), bins=30, kde=True)
    plt.title('Distribuição do Tempo Real de Entrega (limitado a 60 dias)')
    plt.xlabel('Dias')
    plt.ylabel('Frequência')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_distribuicao_tempo_real_entrega.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(10,6))
    sns.histplot(orders_deliv['estimated_delivery_days'].clip(0, 60), bins=30, kde=True, color='orange')
    plt.title('Distribuição do Tempo Estimado de Entrega (limitado a 60 dias)')
    plt.xlabel('Dias')
    plt.ylabel('Frequência')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_distribuicao_tempo_estimado_entrega.png'), bbox_inches='tight')
    plt.close()
    
    plt.figure(figsize=(10,6))
    sns.histplot(orders_deliv['delivery_accuracy'].clip(-30, 30), bins=30, kde=True, color='green')
    plt.axvline(0, color='red', linestyle='--')
    plt.title('Precisão da Entrega: Real - Estimado (Dias)\n(Valores > 0 indicam atraso)')
    plt.xlabel('Diferença (Dias)')
    plt.ylabel('Frequência')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_distribuicao_precisao_entrega.png'), bbox_inches='tight')
    plt.close()
    
    # Late delivery by month
    orders_deliv['purchase_month'] = orders_deliv['order_purchase_timestamp'].dt.to_period('M')
    late_by_month = orders_deliv.groupby('purchase_month')['is_late'].mean() * 100
    
    plt.figure(figsize=(12,6))
    late_by_month.plot(kind='line', marker='o')
    plt.title('Taxa de Entregas Atrasadas por Mês de Compra')
    plt.xlabel('Mês')
    plt.ylabel('% de Atraso')
    plt.grid(True)
    plt.savefig(os.path.join(OUTPUT_DIR, '05_atraso_por_mes.png'), bbox_inches='tight')
    plt.close()
    
    # Late delivery by state (customer)
    late_by_state_c = orders_deliv.groupby('customer_state')['is_late'].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(12,6))
    sns.barplot(x=late_by_state_c.index, y=late_by_state_c.values, palette='viridis')
    plt.title('Taxa de Atraso por Estado do Cliente')
    plt.xlabel('Estado')
    plt.ylabel('% de Atraso')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_atraso_por_estado_cliente.png'), bbox_inches='tight')
    plt.close()
    
    # For seller, we need df_full
    df_full['delivery_accuracy'] = (df_full['order_delivered_customer_date'] - df_full['order_estimated_delivery_date']).dt.total_seconds() / (24*3600)
    df_full['is_late'] = df_full['delivery_accuracy'] > 0
    
    late_by_state_s = df_full.groupby('seller_state')['is_late'].mean().sort_values(ascending=False) * 100
    plt.figure(figsize=(12,6))
    sns.barplot(x=late_by_state_s.index, y=late_by_state_s.values, palette='magma')
    plt.title('Taxa de Atraso por Estado do Vendedor')
    plt.xlabel('Estado')
    plt.ylabel('% de Atraso')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_atraso_por_estado_vendedor.png'), bbox_inches='tight')
    plt.close()
    
    # --- 3. Seller Performance ---
    print("Analisando performance dos vendedores...")
    df_full['seller_processing_days'] = (df_full['order_delivered_carrier_date'] - df_full['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
    
    plt.figure(figsize=(10,6))
    sns.histplot(df_full['seller_processing_days'].clip(0, 15), bins=30, kde=True, color='purple')
    plt.title('Distribuição do Tempo de Processamento do Vendedor (limitado a 15 dias)')
    plt.xlabel('Dias (Compra até Coleta pela Transportadora)')
    plt.ylabel('Frequência')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_distribuicao_processamento_vendedor.png'), bbox_inches='tight')
    plt.close()
    
    # Top 20 sellers with most late deliveries
    seller_lates = df_full[df_full['is_late']].groupby('seller_id').size().sort_values(ascending=False).head(20)
    seller_total = df_full.groupby('seller_id').size()
    
    # Avg processing by seller state
    avg_proc_state = df_full.groupby('seller_state')['seller_processing_days'].mean().sort_values(ascending=False)
    
    # --- 4. Freight Analysis ---
    print("Analisando frete...")
    # Freight by state
    freight_by_state = df_full.groupby('customer_state')['freight_value'].mean().sort_values(ascending=False)
    plt.figure(figsize=(12,6))
    sns.barplot(x=freight_by_state.index, y=freight_by_state.values, palette='coolwarm')
    plt.title('Valor Médio de Frete por Estado do Cliente')
    plt.xlabel('Estado')
    plt.ylabel('Frete Médio (R$)')
    plt.savefig(os.path.join(OUTPUT_DIR, '05_frete_medio_por_estado.png'), bbox_inches='tight')
    plt.close()
    
    # Correlate freight with weight and volume
    corr_freight_weight = df_full['freight_value'].corr(df_full['product_weight_g'])
    corr_freight_volume = df_full['freight_value'].corr(df_full['product_volume_cm3'])
    
    # Freight % by category
    df_full['freight_pct'] = (df_full['freight_value'] / (df_full['price'] + df_full['freight_value'])) * 100
    freight_pct_cat = df_full.groupby('product_category_name')['freight_pct'].mean().sort_values(ascending=False).head(15)
    
    # --- 5. Geographic Analysis ---
    print("Analisando distâncias...")
    # Calculate actual_delivery_days on df_full for distance correlation
    df_full['actual_delivery_days'] = (df_full['order_delivered_customer_date'] - df_full['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
    df_full['seller_processing_days'] = (df_full['order_delivered_carrier_date'] - df_full['order_purchase_timestamp']).dt.total_seconds() / (24*3600)
    # Distance vs delivery time & freight
    df_valid_dist = df_full.dropna(subset=['distance_km', 'actual_delivery_days', 'freight_value'])
    corr_dist_time = df_valid_dist['distance_km'].corr(df_valid_dist['actual_delivery_days'])
    corr_dist_freight = df_valid_dist['distance_km'].corr(df_valid_dist['freight_value'])
    
    # --- 6. Bottleneck Identification ---
    print("Identificando gargalos...")
    df_full['carrier_transit_days'] = (df_full['order_delivered_customer_date'] - df_full['order_delivered_carrier_date']).dt.total_seconds() / (24*3600)
    avg_seller_proc = df_full['seller_processing_days'].mean()
    avg_carrier_transit = df_full['carrier_transit_days'].mean()
    avg_total_deliv = df_full['actual_delivery_days'].mean()
    
    # --- 7. Save Summary ---
    print("Salvando sumário...")
    with open(SUMMARY_FILE, 'w', encoding='utf-8') as f:
        f.write("=== RESUMO DA ANÁLISE LOGÍSTICA ===\n\n")
        
        f.write(f"1. Visão Geral de Entregas\n")
        f.write(f"Tempo médio de entrega: {avg_total_deliv:.2f} dias\n")
        f.write(f"Taxa global de atrasos: {overall_late_pct:.2f}%\n")
        f.write(f"Tempo médio de processamento do vendedor: {avg_seller_proc:.2f} dias\n")
        f.write(f"Tempo médio em trânsito (transportadora): {avg_carrier_transit:.2f} dias\n\n")
        
        f.write(f"2. Atrasos por Região\n")
        f.write(f"Top 3 Estados com maior % de atraso (Cliente):\n")
        for st, val in late_by_state_c.head(3).items():
            f.write(f"  {st}: {val:.2f}%\n")
        f.write(f"Top 3 Estados com maior % de atraso (Vendedor):\n")
        for st, val in late_by_state_s.head(3).items():
            f.write(f"  {st}: {val:.2f}%\n\n")
            
        f.write(f"3. Frete\n")
        f.write(f"Correlação Valor Frete x Peso do Produto: {corr_freight_weight:.4f}\n")
        f.write(f"Correlação Valor Frete x Volume do Produto: {corr_freight_volume:.4f}\n")
        f.write(f"Top 3 Categorias onde o Frete representa maior % do valor total:\n")
        for cat, val in freight_pct_cat.head(3).items():
            f.write(f"  {cat}: {val:.2f}%\n\n")
            
        f.write(f"4. Distância (Geolocalização)\n")
        f.write(f"Correlação Distância x Tempo de Entrega: {corr_dist_time:.4f}\n")
        f.write(f"Correlação Distância x Valor do Frete: {corr_dist_freight:.4f}\n\n")
        
        f.write(f"5. Gargalos Identificados\n")
        f.write("A maior parte do tempo de entrega é consumida pela transportadora (trânsito).\n")
        f.write(f"O processamento dos vendedores (preparação do pacote) leva em média {avg_seller_proc:.2f} dias.\n")
        f.write(f"O trânsito da transportadora leva em média {avg_carrier_transit:.2f} dias.\n")
        if avg_seller_proc > avg_carrier_transit:
            f.write("Atenção: o tempo de preparação do vendedor está mais alto que o tempo de trânsito!\n")
        else:
            f.write("Conclusão: o trânsito até o cliente é o gargalo principal na velocidade de entrega.\n")
            
        f.write("\nTop 5 Vendedores com MAIS atrasos absolutos (IDs):\n")
        for seller_id, count in seller_lates.head(5).items():
            f.write(f"  {seller_id} ({count} atrasos, total ordens: {seller_total[seller_id]})\n")

    print(f"Resumo salvo em {SUMMARY_FILE}")
    print("Processo concluído.")

if __name__ == '__main__':
    main()
