# 🚀 Tech Challenge — Agentic AI

> **Pós-graduação em IA Agêntica (FIAP)**  
> **Case: Olist Intelligent Marketplace**  
> **Equipe de Consultoria Estratégica em IA**

---

## ▶️ Fase 2 (em andamento, entrega em 27/10/2026)

**"Como os agentes de IA irão interagir com usuários, dados e processos da Olist para gerar valor real ao negócio?"**

A Fase 2 detalha três agentes priorizados na jornada do pedido: **LogiPredict** (guardião do prazo), **SentimentDesk** (triagem de avaliações negativas) e **WinBack** (segunda compra), com casos de uso, fluxos operacionais, prompts testados com casos reais e business case.

| Documento | Descrição |
|---|---|
| [fase2/EVOLUCAO_FASE2.md](fase2/EVOLUCAO_FASE2.md) | **Comece aqui:** evolução Fase 1 → 2, entregáveis e decisões |
| [fase2/RELATORIO_EXECUTIVO_FASE2.md](fase2/RELATORIO_EXECUTIVO_FASE2.md) | Relatório Executivo v2 (fonte; o PDF é gerado a partir dele) |
| [fase2/prompts/PROMPTS_V2.md](fase2/prompts/PROMPTS_V2.md) | Prompts estruturados v2 com 10 casos reais |
| [fase2/NUMEROS_OFICIAIS.md](fase2/NUMEROS_OFICIAIS.md) | Fonte única de números (notebook 08) |
| [notebooks/08_fase2_evidencias_business_case.ipynb](notebooks/08_fase2_evidencias_business_case.ipynb) | Cadeia de evidência, priorização e business case |

> O conteúdo abaixo documenta a **Fase 1** (preservado).

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

Uma pasta por fase na raiz; dados e notebooks são compartilhados entre as fases.

```
tech-challenge-agentes-ia/
│
├── 📄 README.md                    # Este arquivo
├── 📄 CONTEXTO.md                  # Contexto e referência rápida do projeto (todas as fases)
├── 🔧 setup_data.sh                # Script para baixar o dataset automaticamente
├── 🔧 build_notebooks.py           # Script auxiliar de geração dos notebooks 01–07
├── 📄 .gitignore                   # Arquivos ignorados pelo Git
│
├── 📁 fase1/                       # Fase 1 — entregue (80/90)
│   ├── TECH_CHALLENGE_AGENTIC_AI-FASE_1.pdf   # Enunciado
│   ├── Relatorio_Executivo_Fase1_Olist_FINAL.pdf (+ .docx)  # Relatório entregue
│   ├── RELATORIO_EXECUTIVO.md      # Relatório executivo (versão markdown)
│   ├── MAPA_AGENTES.md / .html     # Mapa de agentes
│   ├── ARQUITETURA.html            # Arquitetura conceitual
│   ├── PROMPTS_ESTRUTURADOS.md     # Prompts dos agentes
│   ├── ROTEIRO_VIDEO.md · APRESENTACAO.html
│   ├── BRAINSTORMING.md            # Achados e ideias de agentes
│   └── 📁 apresentacao/            # PPT e roteiro do vídeo da Fase 1
│
├── 📁 fase2/                       # Fase 2 — em andamento (ver EVOLUCAO_FASE2.md)
│   ├── POSTECH - Tech Challenge - Fase 2.pdf  # Enunciado
│   ├── EVOLUCAO_FASE2.md · PLANO_FASE2.md
│   ├── RELATORIO_EXECUTIVO_FASE2.md + gerar_relatorio.py
│   ├── NUMEROS_OFICIAIS.md · 📁 dados/ · 📁 img/
│   ├── 📁 fluxos/ · 📁 prompts/ · 📁 video/
│
├── 📁 data/olist/                  # Dataset Olist (baixado via setup_data.sh, fora do Git)
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
├── 📁 notebooks/                   # Jupyter Notebooks de análise exploratória
│   ├── 01_visao_geral_dados.ipynb  # Visão geral e qualidade dos dados
│   ├── 02_pedidos_e_receita.ipynb  # Análise de pedidos, receita e pagamentos
│   ├── 03_clientes_e_retencao.ipynb# Análise de clientes, recompra e churn
│   ├── 04_reviews_e_satisfacao.ipynb# Análise de reviews e satisfação do cliente
│   ├── 05_analise_logistica.ipynb  # Análise logística e performance de entrega
│   ├── 06_analise_vendedores.ipynb # Análise e segmentação de vendedores
│   ├── 07_clustering_segmentacao.ipynb # K-Means, clustering hierárquico, RFM
│   ├── 08_fase2_evidencias_business_case.ipynb # Fase 2: evidências, priorização, business case
│   ├── build_notebook_08.py        # Gera/executa o notebook 08
│   └── 📁 outputs/                 # Gráficos (*.png) e resumos (*_summary.txt)
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

### 1. Visão Geral dos Dados (`01_visao_geral_dados.ipynb`)
- Inspeção inicial de todas as tabelas
- Qualidade dos dados (nulos, duplicatas, tipos)
- Estatísticas descritivas básicas
- Distribuições iniciais (status, pagamento, reviews, categorias)

### 2. Pedidos e Receita (`02_pedidos_e_receita.ipynb`)
- Evolução temporal de pedidos e receita
- Análise de sazonalidade (dia da semana, hora do dia)
- Ticket médio, distribuição de receita
- Análise de pagamentos (tipos, parcelamento)
- Correlações: preço × frete × review score

### 3. Clientes e Retenção (`03_clientes_e_retencao.ipynb`)
- Distribuição geográfica de clientes
- Taxa de recompra e análise de recorrência
- Análise de cohort (retenção mensal)
- Análise de churn e perfil de clientes em risco
- Análise de Pareto (contribuição dos top clientes)

### 4. Reviews e Satisfação (`04_reviews_e_satisfacao.ipynb`)
- Distribuição e evolução de notas
- Impacto de atrasos na satisfação (com testes estatísticos)
- Impacto do frete na satisfação
- Análise textual de comentários (palavras frequentes)
- Testes: Chi-quadrado, Mann-Whitney U

### 5. Análise Logística (`05_analise_logistica.ipynb`)
- Tempo de entrega vs. estimativa
- Taxa de atraso por estado e por mês
- Performance dos vendedores (tempo de processamento)
- Correlações: peso × frete, distância × tempo, distância × frete
- Identificação de gargalos

### 6. Análise de Vendedores (`06_analise_vendedores.ipynb`)
- Distribuição geográfica e evolução da base
- Performance (receita, reviews, entregas)
- Análise de Pareto (concentração de vendas)
- Especialização por categoria
- Comércio intra-estado vs. inter-estado

### 7. Clustering e Segmentação (`07_clustering_segmentacao.ipynb`)
- **RFM Analysis** (Recency, Frequency, Monetary)
- **K-Means Clustering** com método Elbow e Silhouette
- **Clustering Hierárquico** (dendrograma)
- **Segmentação de vendedores** por performance
- **Matriz de correlação** de métricas-chave
- **Análise BCG** de categorias de produtos

---

## 🤖 Agentes de IA Propostos

Com base nas análises, foram identificadas oportunidades para os seguintes agentes:

| Agente (codinome) | Problema Resolvido | Impacto Esperado |
|--------|-------------------|-----------------|
| **Retenção — Anti-Churn (WinBack)** | Recompra de apenas 3% | Recompra 3% → 7% |
| **Logística Preditiva (LogiPredict)** | 8,11% de atrasos; 74% do tempo em trânsito | Atrasos → <4% |
| **Reviews & Sentimento (SentimentDesk)** | 11,5% de notas 1; resposta em ~3 dias | Resposta em minutos |
| **Sucesso do Vendedor (SellerCare)** | 527 sellers problemáticos (nota média 2,22) | −50% do cluster em 6 meses |
| **Precificação & Frete (SmartFreight)** | Frete = 21% do valor do pedido | Conversão +12% |
| **Orquestrador Executivo — BI (Maestro)** | Dados fragmentados atrasam a decisão | −40h/semana em relatórios |

> Detalhes completos no [Mapa de Agentes](fase1/MAPA_AGENTES.md) e nos [Prompts Estruturados](fase1/PROMPTS_ESTRUTURADOS.md).

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

### 4. Executar os Jupyter Notebooks (.ipynb)

Você pode abrir e acompanhar a execução passo a passo dos notebooks via Jupyter Lab ou VS Code:

```bash
# Abrir via Jupyter Lab / Notebook
jupyter lab notebooks/
# ou
jupyter notebook notebooks/
```

Ou re-executar todos os notebooks via linha de comando:

```bash
# Executar todos os notebooks via kernel headless
for nb in notebooks/*.ipynb; do
    echo "=== Executando $nb ==="
    jupyter nbconvert --to notebook --execute "$nb" --inplace
done
```

Todos os notebooks já possuem suas **saídas, tabelas e gráficos pré-renderizados e salvos**, prontos para leitura direta! Os gráficos também ficam armazenados em `notebooks/outputs/`.

---

## 📁 Documentos de Apoio

| Documento | Descrição |
|-----------|-----------|
| [fase1/RELATORIO_EXECUTIVO.md](fase1/RELATORIO_EXECUTIVO.md) | Relatório executivo — documento principal da Fase 1 |
| [fase1/MAPA_AGENTES.md](fase1/MAPA_AGENTES.md) · [.html](fase1/MAPA_AGENTES.html) | Mapa de agentes (texto + diagrama visual) |
| [fase1/ARQUITETURA.html](fase1/ARQUITETURA.html) | Arquitetura conceitual (diagrama visual) |
| [fase1/PROMPTS_ESTRUTURADOS.md](fase1/PROMPTS_ESTRUTURADOS.md) | Estruturação de prompts dos agentes |
| [fase1/ROTEIRO_VIDEO.md](fase1/ROTEIRO_VIDEO.md) · [APRESENTACAO.html](fase1/APRESENTACAO.html) | Roteiro e slides do vídeo executivo |
| [CONTEXTO.md](CONTEXTO.md) · [BRAINSTORMING.md](fase1/BRAINSTORMING.md) | Referência rápida e achados/insights de apoio |

---

## 📅 Evolução do Projeto

| Fase | Status | Foco |
|------|--------|------|
| **Fase 1** | ✅ Entregue (80/90) | Fundamentos, EDA, visão estratégica |
| **Fase 2** | 🔄 Em andamento ([plano](fase2/PLANO_FASE2.md)) | Casos de uso e desenho de agentes |
| Fase 3 | ⏳ Futuro | Protótipos e validação |
| Fase 4 | ⏳ Futuro | Orquestração multiagentes |
| Fase 5 | ⏳ Futuro | Governança e escala corporativa |

---

## 👥 Equipe

- Leonardo Granjeiro
- Jorge Leandro Piva
- Caio Sousa
- Lucas Vinicius Oliveira Mendes

> Pós-Graduação em IA para Devs — FIAP | Turma 2025

---

> **Nota:** Este projeto simula uma consultoria estratégica em IA para a Olist. O foco é na **visão de negócio**, **identificação de oportunidades** e **raciocínio executivo**, não em desenvolvimento técnico avançado.
