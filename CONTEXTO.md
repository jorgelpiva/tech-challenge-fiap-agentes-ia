# 📋 Contexto do Projeto — Tech Challenge Agentic AI (Fase 1)

> Arquivo de referência para manter contexto entre conversas e sessões de trabalho.

## Informações Gerais

| Campo | Valor |
|---|---|
| **Curso** | Pós-graduação em IA Agêntica (FIAP) |
| **Projeto** | Tech Challenge — Case Olist Intelligent Marketplace |
| **Fase Atual** | Fase 1 — Fundamentos de IA e Agentic AI |
| **Peso na Nota** | 90% da nota de todas as disciplinas da fase |
| **Tipo de Atividade** | Atividade em grupo, obrigatória |
| **Workspace** | `/home/jorge/Documents/tech-challenge-agentes-ia` |
| **Data de Início** | 2026-08-05 |

---

## Sobre a Olist (Case)

A Olist é um marketplace brasileiro que deseja iniciar sua jornada de transformação com IA Generativa e Agentes de IA. Desafios atuais:
- Experiência do cliente
- Eficiência logística
- Retenção e fidelização
- Análise de reviews
- Eficiência operacional
- Automação de processos
- Apoio à tomada de decisão
- Escalabilidade operacional

**Pergunta-chave da Fase 1:** "Como a Olist poderia utilizar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?"

---

## Dataset — Brazilian E-Commerce Public Dataset by Olist

~100 mil pedidos entre 2016 e 2018.

### Tabelas Disponíveis

| Tabela | Arquivo | Colunas Principais |
|---|---|---|
| **Customers** | `olist_customers_dataset.csv` | customer_id, customer_unique_id, zip_code, city, state |
| **Orders** | `olist_orders_dataset.csv` | order_id, customer_id, status, purchase_timestamp, approved_at, delivered_carrier_date, delivered_customer_date, estimated_delivery_date |
| **Order Items** | `olist_order_items_dataset.csv` | order_id, order_item_id, product_id, seller_id, shipping_limit_date, price, freight_value |
| **Payments** | `olist_order_payments_dataset.csv` | order_id, payment_sequential, payment_type, payment_installments, payment_value |
| **Reviews** | `olist_order_reviews_dataset.csv` | review_id, order_id, review_score, comment_title, comment_message, creation_date, answer_timestamp |
| **Products** | `olist_products_dataset.csv` | product_id, category_name, name_length, description_length, photos_qty, weight_g, length_cm, height_cm, width_cm |
| **Sellers** | `olist_sellers_dataset.csv` | seller_id, zip_code, city, state |
| **Geolocation** | `olist_geolocation_dataset.csv` | zip_code_prefix, lat, lng, city, state |
| **Tradução** | `product_category_name_translation.csv` | product_category_name, product_category_name_english |

---

## Entregáveis da Fase 1

### 1. Relatório Executivo (10-20 páginas)
- [x] Análise exploratória dos dados (EDA)
- [ ] Principais problemas/oportunidades identificados
- [ ] Análises realizadas no dataset
- [ ] Sugestões iniciais de uso de IA
- [ ] Impacto esperado para o negócio

### 2. Mapa de Agentes de IA (mínimo 3 agentes)
Para cada agente: Nome, Objetivo, Problema resolvido, Usuários envolvidos, Benefício esperado.

### 3. Arquitetura Conceitual Inicial
- Fontes de dados, agentes, usuários, entradas/saídas, interações entre agentes.

### 4. Estruturação de Prompts para Agentes de IA
Para cada agente: objetivo do prompt, contexto fornecido, instrução principal, resultado esperado.

### 5. Vídeo Executivo (até 5 min)
- Linguagem executiva, explicar problemas e oportunidades.

---

## Critérios de Avaliação

1. Visão Estratégica
2. Capacidade de conectar IA aos objetivos do negócio
3. Capacidade Analítica (profundidade das análises e qualidade dos insights)
4. Estruturação Executiva (clareza para executivos e stakeholders)
5. Qualidade Visual (organização, padronização, profissionalismo)
6. Criatividade e Inovação
7. Evolução do Projeto

---

## Evolução ao Longo da Pós-graduação

| Fase | Foco |
|---|---|
| **Fase 1** | Identificar oportunidades e desenhar visão estratégica |
| Fase 2 | Estruturar casos de uso e desenho dos agentes |
| Fase 3 | Construir protótipos e validar soluções |
| Fase 4 | Orquestrar múltiplos agentes e automações |
| Fase 5 | Estruturar governança, liderança e escala corporativa |

---

## Orientações Importantes

- Pensar como **consultoria executiva de IA**
- Evitar foco excessivamente técnico
- Priorizar: clareza, impacto de negócio, racional estratégico, tomada de decisão
- Sempre explicar: problema, benefício, impacto esperado, usuários envolvidos, riscos
- **NÃO é esperado desenvolvimento técnico avançado ou programação complexa**
- O projeto será reutilizado e expandido nas fases seguintes

---

## Notas de Sessão

### 2026-08-05 — Sessão Inicial
- Leitura do PDF do Tech Challenge
- Criação da estrutura do projeto
- Início da Análise Exploratória de Dados (EDA)
- Análises: correlação, estatísticas descritivas, clustering hierárquico, K-Means
- Criação dos documentos de brainstorming e acompanhamento de tarefas
