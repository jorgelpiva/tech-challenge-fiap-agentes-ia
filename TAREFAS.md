# 📝 Tarefas — Tech Challenge Fase 1

> Wiki de acompanhamento do progresso do projeto.  
> Última atualização: 2026-08-05 (após execução de todas as análises)

---

## 🏗️ Estrutura do Projeto

- [x] Leitura e interpretação do PDF do Tech Challenge
- [x] Criação da estrutura de pastas (data, notebooks, docs, reports)
- [x] Cópia do dataset Olist para a pasta `data/olist/`
- [x] Criação do `CONTEXTO.md`
- [x] Criação do `TAREFAS.md` (este arquivo)
- [x] Criação do `BRAINSTORMING.md`
- [x] Criação do `README.md` detalhado
- [x] Criação do `.gitignore`

---

## 📊 Análise Exploratória de Dados (EDA)

- [x] **Notebook 01 — Visão Geral dos Dados** ✅
  - [x] Carregamento e inspeção de todas as 9 tabelas
  - [x] Tipos de dados, valores nulos, dimensões
  - [x] Estatísticas descritivas básicas
  - [x] 8 gráficos de distribuição (status, pagamento, reviews, categorias, estados)
  - [x] Summary exportado para `outputs/01_summary.txt`

- [x] **Notebook 02 — Análise de Pedidos e Receita** ✅
  - [x] Evolução temporal mensal (pedidos e receita)
  - [x] Sazonalidade (dia da semana, hora do dia)
  - [x] Ticket médio R$161 / mediano R$105,29
  - [x] Frete = 21,34% do valor total
  - [x] Análise de pagamentos e parcelamento
  - [x] Correlações: preço×frete (0,41), preço×review (-0,004), frete×review (-0,036)

- [x] **Notebook 03 — Análise de Clientes e Retenção** ✅
  - [x] 93.358 clientes únicos
  - [x] **Taxa de recompra: 3%** (achado crítico!)
  - [x] **Churn: 58,61%**
  - [x] Cohort analysis com heatmap de retenção
  - [x] Pareto: Top 10% = 38,25% da receita

- [x] **Notebook 04 — Análise de Reviews e Satisfação** ✅
  - [x] Distribuição de notas (57,8% nota 5, 11,5% nota 1)
  - [x] **Correlação atraso × nota: -0,229** (principal ofensor!)
  - [x] Testes estatísticos: Chi-quadrado e Mann-Whitney U (p<0,001)
  - [x] Análise textual de comentários positivos e negativos
  - [x] Tempo médio de resposta: 3,15 dias

- [x] **Notebook 05 — Análise Logística** ✅
  - [x] Tempo médio de entrega: 12,47 dias
  - [x] **Trânsito transportadora = 9,19 dias (74% do total)** — gargalo
  - [x] Atrasos: AL 24%, MA 20%, PI 16%
  - [x] Correlação frete×peso (0,61), distância×tempo (0,39)
  - [x] Identificação de gargalos: trânsito > processamento vendedor

- [x] **Notebook 06 — Análise de Vendedores** ✅
  - [x] Pareto: 17,6% geram 80% da receita (Gini 0,79)
  - [x] **342 vendedores com nota < 3,0**
  - [x] 56% são especialistas (1 categoria)
  - [x] 63,8% vendas inter-estado
  - [x] Tempo médio processamento: 3,7 dias

- [x] **Notebook 07 — Clustering e Segmentação** ✅
  - [x] K-Means de clientes (RFM, K=4): Novos, Em Risco, Campeões (valor), Campeões (recorrentes)
  - [x] Hierarchical clustering (dendrograma)
  - [x] Segmentação de vendedores (K=3): Regulares, Top, Problemáticos
  - [x] Matriz de correlação completa
  - [x] BCG matrix de categorias
  - [x] Silhouette score e Elbow method

---

## 📊 Outputs Gerados

- [x] **45 gráficos PNG** em `notebooks/outputs/`
- [x] **7 summaries .txt** em `notebooks/outputs/`
- [x] `BRAINSTORMING.md` atualizado com todos os achados reais

---

## 📄 Relatório Executivo

- [x] Diagnóstico do negócio baseado nos dados (BRAINSTORMING.md)
- [x] Oportunidades identificadas para IA (6 agentes propostos)
- [x] Mapa de Agentes de IA (≥3 agentes) — 6 agentes detalhados
- [x] Arquitetura conceitual inicial (diagrama em BRAINSTORMING.md)
- [ ] Formatação final do relatório (Word/Google Docs/Notion)
- [ ] Prompts estruturados para cada agente (objetivo, contexto, instrução, resultado)
- [ ] Impacto esperado quantificado para cada agente

---

## 🎥 Vídeo Executivo

- [ ] Roteiro do vídeo (até 5 min)
- [ ] Apresentação de apoio (slides)
- [ ] Gravação

---

## 📌 Notas e Decisões

| Data | Decisão/Nota |
|---|---|
| 2026-08-05 | Projeto iniciado. EDA como base para identificar oportunidades de IA. |
| 2026-08-05 | Foco em análises acionáveis: logística, reviews, retenção, segmentação. |
| 2026-08-05 | **Todos os 7 Jupyter Notebooks (.ipynb) foram gerados e executados via kernel Python** |
| 2026-08-05 | **Saídas, tabelas e gráficos embutidos diretamente nos arquivos .ipynb** |
| 2026-08-05 | **Achado principal: taxa de recompra de 3% e atraso como principal ofensor de satisfação** |
| 2026-08-05 | **6 agentes de IA propostos, todos baseados em evidências dos dados** |
| 2026-08-05 | Próximo passo: formatar relatório executivo e estruturar prompts |

---

## 📈 Métricas de Progresso

| Fase | Completo |
|------|----------|
| Estrutura do projeto | ██████████ 100% |
| EDA e análises | ██████████ 100% |
| Documentação de achados | ██████████ 100% |
| Relatório executivo | ████░░░░░░ 40% |
| Prompts estruturados | ░░░░░░░░░░ 0% |
| Vídeo | ░░░░░░░░░░ 0% |
