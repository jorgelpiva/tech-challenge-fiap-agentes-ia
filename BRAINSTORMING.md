# 💡 Brainstorming — Achados e Oportunidades de IA para a Olist

> Documento vivo com insights extraídos das análises exploratórias e ideias para aplicação de IA Agêntica.  
> Última atualização: 2026-08-05

---

## 🔍 Achados das Análises Exploratórias

### 📦 Pedidos e Receita (Script 02)

| Métrica | Valor |
|---------|-------|
| **Receita Total** | R$ 16.008.872,12 |
| **Ticket Médio** | R$ 161,00 |
| **Ticket Mediano** | R$ 105,29 |
| **Total de Pedidos** | 99.441 |
| **Taxa de Cancelamento** | 0,63% |
| **Frete Médio como % do Valor Total** | 21,34% |
| **Tempo Médio de Entrega** | 12,56 dias |
| **Média de Parcelas (Cartão)** | 3,51 |

**Insights-chave:**
- 🔴 **Frete representa 21% do valor total** — barreira significativa de compra
- 📊 Correlação preço × frete: 0,41 (moderada) — produtos mais caros pagam mais frete
- ⚠️ Correlação preço × review: -0,004 (inexistente) — preço não afeta satisfação diretamente
- 📉 Correlação frete × review: -0,036 (muito fraca) — frete alto tem leve impacto negativo

---

### 👥 Clientes e Retenção (Script 03)

| Métrica | Valor |
|---------|-------|
| **Clientes Únicos** | 93.358 |
| **Taxa de Recompra** | **3,00%** ⚠️ |
| **Tempo Médio entre Pedidos** (recorrentes) | 78,8 dias |
| **Taxa de Churn** (inativos >6 meses) | **58,61%** 🔴 |
| **LTV Estimado** | R$ 165,20 |
| **Top 10% clientes** | Contribuem com **38,25%** da receita |

**Insights-chave:**
- 🔴 **Taxa de recompra de apenas 3%** — PROBLEMA CRÍTICO. 97% dos clientes não voltam!
- 🔴 **Churn de 58,6%** — mais da metade dos clientes está inativa
- 💡 Top 10% dos clientes geram 38% da receita — oportunidade de programa de fidelidade
- Perfil churned vs ativo é muito similar (ticket e review) — churn NÃO é motivado por insatisfação explícita, mas sim por falta de engajamento

---

### ⭐ Reviews e Satisfação (Script 04)

| Métrica | Valor |
|---------|-------|
| **Nota 5** | 57,8% |
| **Nota 4** | 19,3% |
| **Nota 3** | 8,2% |
| **Nota 2** | 3,2% |
| **Nota 1** | **11,5%** ⚠️ |
| **Correlação Atraso × Nota** | **-0,229** |
| **Reviews com comentário** | 41,3% (40.668) |
| **Tempo médio de resposta** | 3,15 dias |

**Insights-chave:**
- ✅ Distribuição polarizada: 77% dão nota 4-5, mas **11,5% dão nota 1** (bimodal)
- 🔴 **Atraso na entrega é o principal ofensor da satisfação** (correlação -0,23, p<0,001)
- 📊 Teste Chi-quadrado e Mann-Whitney U confirmam: **atraso × nota é estatisticamente significativo**
- 💡 Palavras mais frequentes em reviews **negativas**: "entregue", "prazo", "pedido" — confirmam foco em logística
- 💡 Palavras em reviews **positivas**: "prazo", "bom", "recomendo", "qualidade", "ótimo" — entrega no prazo gera satisfação
- ⚠️ Frete em si tem impacto marginal na nota (-0,036), mas o **atraso** é decisivo

---

### 🚚 Logística (Script 05)

| Métrica | Valor |
|---------|-------|
| **Tempo médio de entrega** | 12,47 dias |
| **Taxa global de atrasos** | **8,11%** |
| **Tempo médio processamento vendedor** | 3,28 dias |
| **Tempo médio trânsito transportadora** | **9,19 dias** 🔴 |

**Atrasos por Região (Cliente):**
| Estado | % Atraso |
|--------|----------|
| AL | 23,93% |
| MA | 19,67% |
| PI | 15,97% |

**Correlações Logísticas:**
| Relação | Correlação |
|---------|-----------|
| Frete × Peso | **0,61** (forte) |
| Frete × Volume | **0,58** (forte) |
| Distância × Tempo Entrega | **0,39** (moderada) |
| Distância × Frete | **0,39** (moderada) |

**Insights-chave:**
- 🔴 **Trânsito da transportadora é o gargalo principal** (9,19 dias de 12,47 totais = 74% do tempo)
- ⚠️ Processamento do vendedor leva 3,28 dias — também há espaço de melhoria
- 🔴 Estados do Norte/Nordeste têm taxa de atraso 2-3x acima da média
- 💡 63,8% das vendas são **inter-estado** — logística cross-state é regra, não exceção
- 📊 Frete correlaciona fortemente com peso (0,61) e volume (0,58) — previsível, mas automatizável
- ⚠️ Categorias com frete proporcionalmente alto: "casa_conforto_2" (46%), "dvds_blu_ray" (41%), "eletronicos" (36%)

---

### 🏪 Vendedores (Script 06)

| Métrica | Valor |
|---------|-------|
| **Total de vendedores ativos** | 3.095 |
| **Top 3 estados** | SP, PR, MG |
| **% vendedores que geram 80% da receita** | **17,6%** |
| **Gini de concentração** | **0,792** 🔴 |
| **Receita Média** | R$ 4.391,48 |
| **Receita Mediana** | R$ 821,48 |
| **Avaliação média** | 3,97 |
| **Vendedores com nota < 3,0** | **342** |
| **Tempo médio de processamento** | 3,7 dias |
| **Vendedores especialistas (1 cat.)** | 1.728 (56%) |
| **Vendas inter-estado** | 63,8% |

**Insights-chave:**
- 🔴 **Concentração altíssima (Gini 0,79)**: 17,6% dos vendedores geram 80% da receita
- ⚠️ Receita mediana (R$ 821) é 5x menor que a média (R$ 4.391) — cauda longa de sellers pequenos
- 🔴 **342 vendedores com nota média < 3,0** — afetam reputação da plataforma
- 💡 Maioria é especialista (56% vendem em 1 categoria) — segmentação clara
- 💡 63,8% das vendas são inter-estado — dependência forte de logística de longa distância

---

### 🎯 Clustering e Segmentação (Script 07)

#### Segmentação de Clientes (RFM — K=4)

| Segmento | Recência (dias) | Frequência | Valor Médio | Tamanho |
|----------|----------------|------------|-------------|---------|
| **Novos Clientes** | 178 | 1,0 | R$ 135 | 52.056 (54%) |
| **Em Risco / Inativos** | 439 | 1,0 | R$ 135 | 38.655 (40%) |
| **Campeões (Alto Valor)** | 290 | 1,0 | R$ 1.196 | 2.422 (3%) |
| **Campeões (Recorrentes)** | 269 | 2,1 | R$ 290 | 2.962 (3%) |

#### Segmentação de Vendedores (K=3)

| Cluster | Receita | Pedidos | Nota Média | Tempo Entrega | Produtos | Tamanho |
|---------|---------|---------|------------|---------------|----------|---------|
| **Regulares** | R$ 3.775 | 28 | 4,33 | 10,0 dias | 11 | 2.535 (82%) |
| **Top Performers** | R$ 102.986 | 808 | 4,03 | 12,2 dias | 162 | 33 (1%) |
| **Problemáticos** | R$ 1.299 | 6 | **2,22** | **14,4 dias** | 3 | 527 (17%) |

**Insights-chave:**
- 🔴 **40% dos clientes são "Em Risco / Inativos"** — grupo enorme para agente de retenção
- 💡 Apenas **6% são "Campeões"** — alto valor ou recorrentes, devem ser tratados como VIP
- 🔴 **17% dos vendedores são "Problemáticos"** — nota 2,2, entrega em 14,4 dias
- ⚠️ Top Performers (1% dos sellers) têm nota ligeiramente menor (4,03) — possível efeito de volume
- 📊 Correlação negativa confirmada: tempo de entrega × review score

---

## 🤖 Mapa de Agentes de IA Propostos (Baseado nos Achados)

### Agente 1: 🎯 Agente de Retenção e Engajamento (Anti-Churn)

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | 97% dos clientes não voltam. Taxa de recompra de 3%. Churn de 58,6% |
| **Objetivo** | Identificar clientes em risco e engajar proativamente |
| **Dados** | customers, orders, order_items, payments, reviews |
| **Usuários** | Equipe de Marketing, CRM, Gestão Comercial |
| **Ações** | Campanhas personalizadas, cupons, recomendações de produtos |
| **Benefício** | ↑ Retenção, ↑ LTV, ↑ Frequência de compra |
| **Impacto Estimado** | Se recompra subir de 3% para 6%: ~R$ 480K receita adicional/ano |
| **Segmentos Alvo** | 38.655 clientes "Em Risco" + 52.056 "Novos Clientes" |

### Agente 2: 🚚 Agente de Logística Preditiva

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | 8,11% de atrasos. Trânsito é 74% do tempo de entrega. Norte/NE tem 2-3x mais atrasos |
| **Objetivo** | Prever atrasos antes que ocorram e alertar proativamente |
| **Dados** | orders, order_items, sellers, geolocation, products |
| **Usuários** | Equipe de Operações, Vendedores, Atendimento |
| **Ações** | Alertas de risco de atraso, sugestão de transportadoras, comunicação proativa ao cliente |
| **Benefício** | ↓ Atrasos, ↑ Satisfação (atraso é principal ofensor: correlação -0,23 com nota) |
| **Impacto Estimado** | Reduzir atraso de 8,11% para 4%: ~4.000 pedidos/ano sem atraso → melhoria significativa em NPS |

### Agente 3: ⭐ Agente de Análise de Reviews

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | 11,5% das avaliações são nota 1. 41% dos reviews têm comentários não analisados estruturalmente |
| **Objetivo** | Classificar sentimento, extrair temas, gerar alertas automáticos |
| **Dados** | reviews, orders, products, sellers |
| **Usuários** | Equipe de Produto, Gestão de Sellers, Atendimento |
| **Ações** | Dashboard de sentimento em tempo real, alertas de problemas recorrentes, resposta automática |
| **Benefício** | Identificação rápida de problemas, redução de reviews negativos |
| **Impacto Estimado** | Detecção antecipada de 342 vendedores com nota < 3,0 |

### Agente 4: 🏪 Agente de Sucesso do Vendedor

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | 17% dos sellers são "Problemáticos" (nota 2,2, entrega 14,4 dias). Gini 0,79 de concentração |
| **Objetivo** | Monitorar KPIs, gerar recomendações, coaching automatizado |
| **Dados** | sellers, order_items, reviews, orders, products |
| **Usuários** | Equipe de Gestão de Sellers |
| **Ações** | Onboarding inteligente, alertas de performance, recomendações de melhoria |
| **Benefício** | ↑ Nível de serviço da plataforma, ↓ sellers problemáticos |
| **Impacto Estimado** | Reduzir 527 sellers problemáticos melhorando nota média de 3,97 para 4,2+ |

### Agente 5: 💰 Agente de Precificação e Frete Inteligente

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | Frete = 21% do valor total. Categorias com frete >40% do valor. Correlação frete×peso 0,61 |
| **Objetivo** | Otimizar custos de frete e sugerir estratégias de precificação |
| **Dados** | order_items, products, geolocation, payments |
| **Usuários** | Vendedores, Equipe Comercial |
| **Ações** | Sugestões de preço, otimização de embalagem, cálculo de frete inteligente |
| **Benefício** | ↓ Abandono de carrinho, ↑ Conversão |

### Agente 6: 📊 Agente Executivo de BI

| Aspecto | Descrição |
|---------|-----------|
| **Problema** | Dados dispersos, difícil cruzar insights entre áreas |
| **Objetivo** | Gerar relatórios executivos sob demanda e responder perguntas de negócio |
| **Dados** | Todas as tabelas do dataset |
| **Usuários** | Diretoria, Gerentes de Área |
| **Ações** | Dashboards conversacionais, alertas de anomalias, resumos periódicos |
| **Benefício** | Democratização do acesso a dados, agilidade na tomada de decisão |

---

## 📊 Matriz de Correlações Estratégicas

```
                    Impacto na Satisfação
                    ┌──────────────────────────────────┐
                    │                                  │
    Alto Impacto    │  ★ ATRASO NA ENTREGA (-0.229)    │
                    │    (Confirmado estatisticamente)  │
                    │                                  │
                    │  ⬤ TRÂNSITO TRANSPORTADORA       │
                    │    (9.19 dias = 74% do total)    │
                    │                                  │
    Médio Impacto   │  ⬤ VALOR DO FRETE (-0.036)       │
                    │  ⬤ FRETE COMO % DO TOTAL         │
                    │                                  │
    Baixo Impacto   │  ⬤ PREÇO DO PRODUTO (-0.004)     │
                    │                                  │
                    └──────────────────────────────────┘
```

---

## 🏗️ Arquitetura Conceitual (Refinada com Dados)

```
┌─────────────────────────────────────────────────────────────────┐
│                    OLIST INTELLIGENT MARKETPLACE                 │
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              FONTES DE DADOS (Dataset Olist)              │   │
│  │  customers │ orders │ items │ payments │ reviews │ geo   │   │
│  └──────────────────────┬───────────────────────────────────┘   │
│                          │                                       │
│  ┌──────────────────────▼───────────────────────────────────┐   │
│  │                 CAMADA DE PROCESSAMENTO                   │   │
│  │  ETL │ Feature Engineering │ RFM │ Clustering │ NLP      │   │
│  └──────┬──────────┬──────────┬──────────┬──────────┬───────┘   │
│         │          │          │          │          │            │
│  ┌──────▼───┐┌─────▼────┐┌───▼────┐┌────▼───┐┌────▼─────┐     │
│  │ Agente   ││ Agente   ││Agente  ││Agente  ││ Agente   │     │
│  │ Retenção ││ Logíst.  ││Reviews ││Sellers ││ Frete    │     │
│  │ (40K at  ││ (atraso  ││(11.5%  ││(17%    ││ (21% do  │     │
│  │  risk)   ││  8.11%)  ││ nota 1)││ probl.)││  total)  │     │
│  └──────┬───┘└─────┬────┘└───┬────┘└────┬───┘└────┬─────┘     │
│         │          │          │          │          │            │
│  ┌──────▼──────────▼──────────▼──────────▼──────────▼───────┐   │
│  │              ORQUESTRADOR DE AGENTES                      │   │
│  │  Coordena ações, resolve conflitos, prioriza alertas      │   │
│  └──────┬──────────┬──────────┬──────────┬──────────┬───────┘   │
│         │          │          │          │          │            │
│  ┌──────▼───┐┌─────▼────┐┌───▼────┐┌────▼───┐┌────▼─────┐     │
│  │Marketing ││Operações ││Produto ││Gestão  ││Comercial │     │
│  │ / CRM    ││          ││        ││Sellers ││          │     │
│  └──────────┘└──────────┘└────────┘└────────┘└──────────┘     │
│                        USUÁRIOS FINAIS                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Principais Conclusões para o Relatório Executivo

### Top 5 Problemas Identificados (ordenados por impacto)

1. **Retenção crítica**: Taxa de recompra de apenas 3% — a Olist funciona basicamente como marketplace de "compra única"
2. **Logística como gargalo**: 74% do tempo de entrega é trânsito da transportadora; Norte/NE com até 24% de atraso
3. **Vendedores problemáticos**: 17% dos sellers têm nota < 2,2 e entrega em 14,4 dias, afetando toda a plataforma
4. **Reviews negativos concentrados em logística**: Palavras-chave de reviews negativos são "prazo", "entregue", "pedido"
5. **Frete como barreira**: 21% do valor total, com categorias chegando a 46% de frete sobre o preço

### Top 5 Oportunidades de IA Agêntica

1. **Agente de Retenção**: Potencial de recuperar parte dos 38.655 clientes "Em Risco" com comunicação personalizada
2. **Agente de Logística Preditiva**: Antecipação de atrasos pode melhorar satisfação em toda a base
3. **Agente de Reviews**: Análise de sentimento em tempo real para resposta rápida a problemas
4. **Agente de Sucesso do Vendedor**: Coaching automatizado para os 527 sellers problemáticos
5. **Agente Executivo de BI**: Decisões mais rápidas e baseadas em dados para a diretoria
