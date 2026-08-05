# 🚀 Tech Challenge — Agentic AI | Fase 1

> **Pós-graduação em IA Agêntica (FIAP)**  
> **Case: Olist Intelligent Marketplace**  
> **Equipe de Consultoria Estratégica em IA**

---

## 📌 Sobre o Projeto

Este projeto faz parte do **Tech Challenge** da pós-graduação em IA Agêntica, correspondendo à **Fase 1 — Fundamentos de IA e Agentic AI**. O objetivo é analisar o contexto de negócio da **Olist** e identificar oportunidades iniciais de aplicação de **IA Generativa** e **Agentes de IA**.

### Pergunta Central

> *"Como a Olist poderia utilizar IA Generativa e Agentes de IA para melhorar sua operação e seus indicadores de negócio?"*

### Contexto

A Olist é um marketplace brasileiro que conecta pequenos lojistas a grandes canais de venda. A empresa busca iniciar sua jornada de transformação digital com IA, enfrentando desafios em:

- 🎯 Experiência do cliente
- 🚚 Eficiência logística
- 🔄 Retenção e fidelização
- ⭐ Análise de reviews
- ⚙️ Eficiência operacional
- 🤖 Automação de processos
- 📊 Apoio à tomada de decisão

---

## 📂 Estrutura do Projeto

```
tech-challenge-agentes-ia/
│
├── 📄 README.md                    # Este arquivo
├── 📄 CONTEXTO.md                  # Contexto do projeto e referência rápida
├── 📄 TAREFAS.md                   # Wiki de acompanhamento de tarefas
├── 📄 BRAINSTORMING.md             # Achados, insights e ideias de agentes IA
├── 🔧 setup_data.sh                # Script para baixar o dataset automaticamente
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
├── 📄 TECH_CHALLENGE_AGENTIC_AI-FASE_1.pdf  # Enunciado do desafio
│
├── 📁 data/
│   └── 📁 olist/                   # Dataset Olist (Brazilian E-Commerce)
│       ├── olist_customers_dataset.csv
│       ├── olist_orders_dataset.csv
│       ├── olist_order_items_dataset.csv
│       ├── olist_order_payments_dataset.csv
│       ├── olist_order_reviews_dataset.csv
│       ├── olist_products_dataset.csv
│       ├── olist_sellers_dataset.csv
│       ├── olist_geolocation_dataset.csv
│       └── product_category_name_translation.csv
│
├── 📁 notebooks/                   # Scripts de análise exploratória
│   ├── 01_visao_geral_dados.py     # Visão geral e qualidade dos dados
│   ├── 02_pedidos_e_receita.py     # Análise de pedidos, receita e pagamentos
│   ├── 03_clientes_e_retencao.py   # Análise de clientes, recompra e churn
│   ├── 04_reviews_e_satisfacao.py  # Análise de reviews e satisfação do cliente
│   ├── 05_analise_logistica.py     # Análise logística e performance de entrega
│   ├── 06_analise_vendedores.py    # Análise e segmentação de vendedores
│   ├── 07_clustering_segmentacao.py # K-Means, clustering hierárquico, RFM
│   └── 📁 outputs/                 # Gráficos e resumos gerados
│       ├── *.png                   # Visualizações
│       └── *_summary.txt           # Resumos de cada análise
│
├── 📁 docs/                        # Documentação adicional
│
└── 📁 reports/                     # Relatório executivo final
```

---

## 📊 Dataset — Brazilian E-Commerce (Olist)

O dataset público contém **~100 mil pedidos** realizados entre **2016 e 2018** em marketplaces brasileiros. Dados anonimizados que permitem análises orientadas a negócio.

### Tabelas Disponíveis

| # | Tabela | Descrição | Registros |
|---|--------|-----------|-----------|
| 1 | `customers` | Dados de clientes e localização | ~99k |
| 2 | `orders` | Pedidos e status operacionais | ~100k |
| 3 | `order_items` | Itens comprados, preços e fretes | ~113k |
| 4 | `payments` | Informações de pagamento | ~104k |
| 5 | `order_reviews` | Avaliações e comentários | ~100k |
| 6 | `products` | Informações de produtos | ~33k |
| 7 | `sellers` | Dados dos vendedores | ~3k |
| 8 | `geolocation` | Dados geográficos (lat/lng) | ~1M |
| 9 | `category_translation` | Tradução de categorias PT→EN | 71 |

### Diagrama de Relacionamento

```
customers ──┐
            ├── orders ──┬── order_items ──┬── products
            │            │                 └── sellers
            │            ├── payments
            │            └── reviews
            │
geolocation ─── (zip_code_prefix) ─── customers / sellers
```

---

## 🔬 Análises Realizadas

### 1. Visão Geral dos Dados (`01_visao_geral_dados.py`)
- Inspeção inicial de todas as tabelas
- Qualidade dos dados (nulos, duplicatas, tipos)
- Estatísticas descritivas básicas
- Distribuições iniciais (status, pagamento, reviews, categorias)

### 2. Pedidos e Receita (`02_pedidos_e_receita.py`)
- Evolução temporal de pedidos e receita
- Análise de sazonalidade (dia da semana, hora do dia)
- Ticket médio, distribuição de receita
- Análise de pagamentos (tipos, parcelamento)
- Correlações: preço × frete × review score

### 3. Clientes e Retenção (`03_clientes_e_retencao.py`)
- Distribuição geográfica de clientes
- Taxa de recompra e análise de recorrência
- Análise de cohort (retenção mensal)
- Análise de churn e perfil de clientes em risco
- Análise de Pareto (contribuição dos top clientes)

### 4. Reviews e Satisfação (`04_reviews_e_satisfacao.py`)
- Distribuição e evolução de notas
- Impacto de atrasos na satisfação (com testes estatísticos)
- Impacto do frete na satisfação
- Análise textual de comentários (palavras frequentes)
- Testes: Chi-quadrado, Mann-Whitney U

### 5. Análise Logística (`05_analise_logistica.py`)
- Tempo de entrega vs. estimativa
- Taxa de atraso por estado e por mês
- Performance dos vendedores (tempo de processamento)
- Correlações: peso × frete, distância × tempo, distância × frete
- Identificação de gargalos

### 6. Análise de Vendedores (`06_analise_vendedores.py`)
- Distribuição geográfica e evolução da base
- Performance (receita, reviews, entregas)
- Análise de Pareto (concentração de vendas)
- Especialização por categoria
- Comércio intra-estado vs. inter-estado

### 7. Clustering e Segmentação (`07_clustering_segmentacao.py`)
- **RFM Analysis** (Recency, Frequency, Monetary)
- **K-Means Clustering** com método Elbow e Silhouette
- **Clustering Hierárquico** (dendrograma)
- **Segmentação de vendedores** por performance
- **Matriz de correlação** de métricas-chave
- **Análise BCG** de categorias de produtos

---

## 🤖 Agentes de IA Propostos

Com base nas análises, foram identificadas oportunidades para os seguintes agentes:

| Agente | Problema Resolvido | Impacto Esperado |
|--------|-------------------|-----------------|
| **Agente de Atendimento** | Respostas lentas a clientes | ↓ Tempo de resposta, ↑ Satisfação |
| **Agente de Reviews** | Reviews sem análise estruturada | Identificação rápida de problemas |
| **Agente de Logística** | Atrasos impactam satisfação | ↓ Atrasos, ↑ NPS |
| **Agente de Retenção** | Baixa taxa de recompra | ↑ Retenção e LTV |
| **Agente de Sellers** | Vendedores com baixa performance | ↑ Nível de serviço |
| **Agente de Precificação** | Frete alto como barreira | ↑ Conversão |

> Detalhes completos no arquivo [BRAINSTORMING.md](BRAINSTORMING.md).

---

## ⚙️ Como Executar

### 1. Clonar o repositório

```bash
git clone <URL_DO_REPOSITORIO>
cd tech-challenge-agentes-ia
```

### 2. Baixar o dataset

O dataset da Olist **não está incluído no repositório** (está no `.gitignore` por ser grande ~120MB). Use o script de setup para baixá-lo automaticamente:

```bash
# Download automático via Kaggle CLI (recomendado)
./setup_data.sh
```

O script tenta, nesta ordem:
1. **Kaggle CLI** (`kaggle datasets download`) — requer `pip install kaggle` + credenciais
2. **Kaggle Python API** — mesma dependência, via código Python
3. **Instruções manuais** — se nenhum método automático estiver disponível, exibe instruções passo a passo

> **Configurar Kaggle CLI (primeira vez):**
> 1. `pip install kaggle`
> 2. Acesse [kaggle.com/settings](https://www.kaggle.com/settings) → API → **Create New Token**
> 3. Salve o `kaggle.json` em `~/.kaggle/` e rode `chmod 600 ~/.kaggle/kaggle.json`

Se preferir o download manual:
1. Acesse: [Brazilian E-Commerce Dataset (Kaggle)](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)
2. Clique em **Download** (conta Kaggle gratuita necessária)
3. Extraia os CSVs na pasta `data/olist/`

### 3. Instalar dependências Python

```bash
# Python 3.10+
pip install pandas numpy matplotlib seaborn scipy scikit-learn plotly
```

### 4. Executar as análises

```bash
# Executar análise individual
python3 notebooks/01_visao_geral_dados.py

# Executar todas as análises de uma vez
for script in notebooks/0*.py; do
    echo "=== Executando $script ==="
    python3 "$script"
done
```

Os gráficos serão salvos em `notebooks/outputs/` e os resumos em `notebooks/outputs/*_summary.txt`.

---

## 📁 Documentos de Apoio

| Documento | Descrição |
|-----------|-----------|
| [CONTEXTO.md](CONTEXTO.md) | Referência rápida do projeto, entregáveis, critérios |
| [TAREFAS.md](TAREFAS.md) | Wiki de acompanhamento do progresso |
| [BRAINSTORMING.md](BRAINSTORMING.md) | Achados, insights e propostas de agentes |

---

## 📅 Evolução do Projeto

| Fase | Status | Foco |
|------|--------|------|
| **Fase 1** | 🔄 Em andamento | Fundamentos, EDA, visão estratégica |
| Fase 2 | ⏳ Futuro | Casos de uso e desenho de agentes |
| Fase 3 | ⏳ Futuro | Protótipos e validação |
| Fase 4 | ⏳ Futuro | Orquestração multiagentes |
| Fase 5 | ⏳ Futuro | Governança e escala corporativa |

---

## 👥 Equipe

*(Adicionar nomes dos integrantes do grupo)*

---

> **Nota:** Este projeto simula uma consultoria estratégica em IA para a Olist. O foco é na **visão de negócio**, **identificação de oportunidades** e **raciocínio executivo**, não em desenvolvimento técnico avançado.
