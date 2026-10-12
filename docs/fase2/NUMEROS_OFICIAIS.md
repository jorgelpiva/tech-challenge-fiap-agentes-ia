# 🔢 Números Oficiais — Fase 2

> **Gerado automaticamente** por `notebooks/08_fase2_evidencias_business_case.ipynb`. Não edite à mão: rode o notebook.
> Todo número do relatório, dos slides e do vídeo deve estar nesta tabela.

| Chave | Valor | Definição | Fonte |
|---|---|---|---|
| `pedidos_total` | 99.441 | Pedidos no dataset (todas as situações) | orders |
| `pedidos_entregues` | 96.470 | Pedidos com status delivered e data de entrega | orders |
| `receita_total` | 16.008.872,12 | Soma de payment_value | order_payments |
| `ticket_medio` | 160,99 | Valor médio pago por pedido | order_payments |
| `dias_entrega_medio` | 12,56 | Média (dias corridos fracionados) entre compra e entrega, pedidos entregues. Substitui o 12,47 da Fase 1. | orders |
| `dias_transito_medio` | 9,33 | Média entre postagem (delivered_carrier) e entrega | orders |
| `dias_proc_medio` | 3,23 | Média entre compra e postagem (processamento do seller) | orders |
| `pct_transito` | 74,30 | % do tempo total gasto em trânsito | orders |
| `taxa_atraso` | 8,11 | % de pedidos entregues após order_estimated_delivery_date | orders |
| `nota_media_atrasado` | 2,57 | Nota média de pedidos entregues com atraso | orders+reviews |
| `nota_media_no_prazo` | 4,29 | Nota média de pedidos entregues no prazo | orders+reviews |
| `pct_neg_atrasado` | 54,10 | % de notas 1–2 em pedidos atrasados | orders+reviews |
| `pct_neg_no_prazo` | 9,20 | % de notas 1–2 em pedidos no prazo | orders+reviews |
| `pct_postagem_atrasada` | 9,00 | % de pedidos em que o seller postou após shipping_limit_date | orders+order_items |
| `atraso_se_postagem_atrasada` | 24,40 | Taxa de atraso quando a postagem foi após o limite | orders+order_items |
| `atraso_se_postagem_no_prazo` | 6,50 | Taxa de atraso quando a postagem foi no prazo | orders+order_items |
| `pct_atrasos_com_postagem_atrasada` | 27,20 | % dos pedidos atrasados que tiveram postagem atrasada pelo seller | orders+order_items |
| `mediana_dias_postagem_ate_prazo_atrasados` | 17,50 | Nos pedidos que atrasaram: mediana de dias entre a postagem e o prazo prometido (janela para agir) | orders |
| `atraso_top_uf` | AL: 23,90; MA: 19,70; PI: 16,00; CE: 15,30; SE: 15,20 | UFs de destino com maior taxa de atraso | orders+customers |
| `reviews_total` | 99.224 | Avaliações no dataset | order_reviews |
| `pct_nota_1` | 11,50 | % de avaliações nota 1 | order_reviews |
| `pct_nota_1_2` | 14,70 | % de avaliações nota 1 ou 2 | order_reviews |
| `reviews_negativas` | 14.575 | Avaliações nota 1–2 | order_reviews |
| `reviews_negativas_com_texto` | 10.994 | Avaliações nota 1–2 com título ou comentário | order_reviews |
| `motivos_reviews_negativas` | Não recebido: 39,50; Outros/genérico: 17,80; Item faltando: 10,40; Produto errado/diferente: 7,40; Qualidade/expectativa: 7,20; Atraso: 7,10; Atendimento/estorno: 5,40; Defeito/avaria: 5,10 | Motivo principal (regras) em reviews 1–2 com texto | order_reviews |
| `grupos_reviews_negativas` | Entrega: 46,70; Outros: 17,80; Pedido incorreto: 17,80; Produto: 12,30; Atendimento e financeiro: 5,40 | Grupo executivo do motivo principal | order_reviews |
| `pct_neg_em_pedido_atrasado` | 33,80 | % das notas 1–2 (pedidos entregues) cujo pedido atrasou | orders+reviews |
| `reviews_negativas_12m` | 11.711 | Avaliações 1–2 criadas entre set/2017 e ago/2018 | order_reviews |
| `clientes_unicos` | 93.358 | customer_unique_id com ao menos 1 pedido entregue | orders+customers |
| `taxa_recompra` | 3,00 | % de clientes únicos com 2+ pedidos entregues | orders+customers |
| `recompras_validas` | 1.948 | Clientes com 2ª compra em dia diferente da 1ª | orders |
| `mediana_dias_2a_compra` | 76 | Mediana de dias entre 1ª e 2ª compra (gap ≥ 1 dia) | orders |
| `pct_2a_compra_ate_30d` | 29,30 | % das 2ªs compras que ocorrem em até 30 dias | orders |
| `pct_2a_compra_ate_60d` | 44,40 | % das 2ªs compras que ocorrem em até 60 dias | orders |
| `pct_2a_compra_ate_90d` | 54,40 | % das 2ªs compras que ocorrem em até 90 dias | orders |
| `pct_2a_compra_ate_180d` | 75,40 | % das 2ªs compras que ocorrem em até 180 dias | orders |
| `ticket_2a_compra` | 148,35 | Valor médio da 2ª compra | orders+payments |
| `recompra_1a_atrasada` | 1,56 | Recompra quando a 1ª compra atrasou | orders+reviews |
| `recompra_1a_no_prazo` | 2,13 | Recompra quando a 1ª compra chegou no prazo | orders+reviews |
| `recompra_top_categorias` | fashion_bolsas_e_acessorios: 3,60; moveis_decoracao: 2,70; esporte_lazer: 2,70; cama_mesa_banho: 2,60; pet_shop: 2,50 | Categorias da 1ª compra com maior recompra (≥1.000 clientes) | orders+items+products |
| `priorizacao` | LogiPredict: 4,75; SentimentDesk: 4,60; WinBack: 4,20; SellerCare: 3,40; SmartFreight: 2,75; Maestro: 2,40 | Score ponderado (pesos 30/25/20/15/10) | avaliação do grupo |
| `bc_pedidos_12m` | 74.206 | Pedidos entregues set/2017–ago/2018 | orders |
| `bc_postagens_atrasadas_12m` | 6.689 | Pedidos com postagem atrasada no período | orders+items |
| `bc_novos_clientes_12m` | 71.693 | 1ª compra entregue no período | orders |
| `bc_conversao_2a_compra_90d` | 1,13 | % de clientes com 2ª compra em 1–90 dias | orders |
| `bc_premissas` | reducao_gap_atraso: Conservador: 0,25; Base: 0,50; Otimista: 0,75; min_manual: 12; min_agente: 3; custo_hora: 45,00; cobertura_sentiment: Conservador: 0,50; Base: 0,70; Otimista: 0,90; uplift_pp_2a_compra: Conservador: 0,00; Base: 0,01; Otimista: 0,01 | Premissas do business case | grupo |
| `bc_logipredict` | Conservador: atrasos_evitados: 335; notas_1_2_evitadas: 150; Base: atrasos_evitados: 670; notas_1_2_evitadas: 300; Otimista: atrasos_evitados: 1.006; notas_1_2_evitadas: 451 | Atrasos e notas 1–2 evitados por ano | cálculo |
| `bc_sentimentdesk` | Conservador: horas_poupadas: 878; reais_poupados: 39.525,00; Base: horas_poupadas: 1.229; reais_poupados: 55.334,00; Otimista: horas_poupadas: 1.580; reais_poupados: 71.144,00 | Horas e R$ de triagem poupados por ano | cálculo |
| `bc_winback` | Conservador: segundas_compras_extra: 179; receita_extra: 26.589,00; Base: segundas_compras_extra: 358; receita_extra: 53.178,00; Otimista: segundas_compras_extra: 716; receita_extra: 106.357,00 | 2ªs compras e receita incremental por ano | cálculo |
| `transito_rotas_exemplos` | MG->MA: pedidos: 61; mediana: 14,90; p75: 20,50; p90: 26,10; SP->BA: pedidos: 2.307; mediana: 14,10; p75: 20,50; p90: 28,00; SP->SP: pedidos: 30.735; mediana: 3,60; p75: 6,10; p90: 9,40 | Trânsito (dias) por rota UF seller → UF cliente, usado nos exemplos do LogiPredict | orders+sellers+customers |
| `pct_2a_compra_mesma_categoria` | 37,80 | % das 2ªs compras na mesma categoria da 1ª | orders+items+products |
| `categorias_2a_compra_exemplos` | cama_mesa_banho: cama_mesa_banho: 46,50; moveis_decoracao: 9,30; utilidades_domesticas: 6,20; beleza_saude: beleza_saude: 50,70; perfumaria: 4,60; esporte_lazer: 4,60 | Categorias mais comuns da 2ª compra por categoria da 1ª (exemplos do WinBack) | orders+items+products |
