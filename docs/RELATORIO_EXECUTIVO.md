# RELATÓRIO EXECUTIVO E DIAGNÓSTICO DE DADOS 
## Fase 1 — Tech Challenge de IA Agêntica

**Autores:** Grupo X — Pós-Graduação IA para Devs | FIAP | 2025  
**Data:** 06 de Agosto de 2026  
**Base de Dados Analisada:** Brazilian E-Commerce Public Dataset by Olist (2016-2018)  
**Volume de Dados:** 99.441 pedidos processados  

---

## 1. Sumário Executivo

O presente relatório consolida os resultados da análise exploratória e modelagem de dados avançada conduzida sobre a base pública de e-commerce da Olist, referente aos anos de 2016 a 2018. Com um volume de mais de 99 mil pedidos e uma receita transacionada superior a R$ 16 milhões, o objetivo central desta fase de diagnóstico foi identificar os principais gargalos operacionais e oportunidades estratégicas que justifiquem a implementação de uma arquitetura baseada em Inteligência Artificial Agêntica.

Nossa análise revelou um cenário de e-commerce com alta capacidade de aquisição, mas com falhas críticas na retenção de clientes e na eficiência logística. O achado mais alarmante reside na taxa de recompra de apenas 3,00%, indicando que a esmagadora maioria dos consumidores não retorna para uma segunda compra. Esse sintoma está intrinsecamente ligado à experiência de entrega e à qualidade do serviço prestado pelos vendedores, onde 8,11% dos pedidos sofrem atrasos e as notas de satisfação apresentam forte correlação negativa (-0,229) com o tempo de espera.

Diante desse cenário, a modelagem de segmentação via K-Means e Análise RFM permitiu mapear clusters vitais, demonstrando que uma pequena fração da base (3%) representa os "Campeões de Alto Valor". A abordagem proposta neste documento não apenas diagnostica essas feridas abertas, mas estrutura o alicerce para a criação de um ecossistema de agentes autônomos de IA, desenhado especificamente para atuar de forma proativa na retenção, na predição de falhas logísticas e no suporte inteligente.

---

## 2. Contexto e Problema de Negócio

A Olist atua como um ecossistema de soluções para conectar pequenas e médias empresas ao mercado de e-commerce, funcionando como um grande *marketplace* de integração. A base de dados cedida para este estudo reflete a realidade do e-commerce brasileiro entre 2016 e 2018, um período de forte crescimento, mas com os clássicos gargalos de infraestrutura e logística continentais do Brasil.

O problema de negócio central foca na **sustentabilidade e lucratividade a longo prazo**. Um e-commerce não sobrevive apenas de aquisição de novos clientes (Customer Acquisition Cost - CAC); ele precisa maximizar o Valor do Ciclo de Vida do Cliente (Lifetime Value - LTV). Com um LTV estimado em apenas R$ 165,20, muito próximo ao ticket médio isolado (R$ 161,00), evidencia-se que o modelo atual opera de forma transacional, sem construir lealdade.

Os desafios enfrentados incluem:
- **Dependência de Malha Logística Fragmentada:** Com 63,8% das vendas ocorrendo de forma interestadual, o Brasil apresenta um desafio colossal.
- **Controle de Qualidade Descentralizado:** Com 3.095 vendedores na plataforma, garantir um padrão Olist de excelência é complexo. 
- **Insatisfação Relacional:** A métrica de 11,5% de avaliações com nota 1 evidencia detratores ativos, cujas queixas centrais envolvem os processos de entrega ("prazo", "entregue").

O desafio proposto para a FIAP, portanto, é audacioso: como podemos injetar inteligência autônoma e preditiva (IA Agêntica) nesse fluxo para antecipar problemas, personalizar o atendimento e automatizar o controle de qualidade dos lojistas parceiros?

---

## 3. Metodologia

A condução deste estudo diagnóstico seguiu as melhores práticas de Ciência de Dados, utilizando ferramentas estatísticas e de *Machine Learning* não supervisionado para extrair inteligência dos dados brutos. 

As 7 frentes de análise realizadas englobaram:

1. **Análise Exploratória de Dados (EDA):** Limpeza, tratamento de nulos e compreensão da distribuição de variáveis como preço, frete e tempo de entrega.
2. **Modelagem de Segmentação de Clientes (RFM + K-Means):** Utilização da matriz de Recência, Frequência e Valor Monetário (RFM) clusterizada via algoritmo K-Means para K=4, isolando grupos comportamentais de consumidores.
3. **Clusterização de Vendedores (K-Means):** Aplicação de K-Means (K=3) para categorizar lojistas baseado em receita, avaliações e tempo de entrega.
4. **Análise Estatística de Correlações:** Testes de Correlação de Pearson para variáveis contínuas (ex: Preço × Frete).
5. **Teste de Hipóteses (Mann-Whitney U e Chi-Square):** Para validar estatisticamente a relação não-linear entre a ocorrência de atrasos (variável categórica/binária) e as notas de review.
6. **Análise Geoespacial Logística:** Utilização da Fórmula de Haversine para cálculo de distâncias entre os CEPs de origem (vendedor) e destino (cliente) e avaliação de rotas críticas.
7. **Processamento de Linguagem Natural Básica (NLP):** Extração e contagem de frequência de palavras-chave nos comentários de avaliações negativas (notas 1 e 2).

> 💡 **Nota Técnica:** Todos os modelos foram validados buscando a minimização do erro e a coesão interna dos clusters (ex: Método do Cotovelo para o K-Means).

---

## 4. Principais Achados e Diagnóstico

Para facilitar a digestão executiva, dividimos nossos achados baseados em dados reais em 5 temas críticos.

### 4.1. Retenção de Clientes (A Falha Silenciosa)

O ecossistema atrai clientes, mas falha gravemente em retê-los. O modelo de negócios está refém de compras de oportunidade única.

- **Dado em Destaque:** 93.358 clientes únicos registraram uma **Taxa de Recompra de míseros 3,00%**. 
- **Interpretação Executiva:** Isso significa que 97 em cada 100 clientes não voltam a comprar na plataforma. Associado a isso, temos uma Taxa de Churn altíssima de 58,61% (clientes inativos por mais de 6 meses).
- **Implicação para o Negócio:** O Custo de Aquisição de Clientes (CAC) está sendo desperdiçado, pois o LTV está estagnado em R$ 165,20 (muito próximo ao Ticket Médio de R$ 161,00). Sem estratégias de fidelização, o modelo financeiro se torna insustentável caso o marketing de aquisição encareça.

> ⚠️ **Achado Crítico:** Apenas o Top 10% dos clientes são responsáveis por 38,25% de toda a receita. Perder um desses clientes custa desproporcionalmente caro.

### 4.2. Logística (O Calcanhar de Aquiles)

A entrega é o principal gerador de atrito na jornada do consumidor, amplificado pela vasta dimensão continental.

- **Dado em Destaque:** O tempo médio de entrega é de 12,47 dias. O gargalo real encontra-se na etapa de trânsito pela transportadora (9,19 dias — 74% do tempo total), enquanto o vendedor leva em média 3,28 dias (26%).
- **Interpretação Executiva:** Com 63,8% das vendas sendo transações interestaduais, a logística sofre. A taxa global de atrasos é de 8,11%. Estados do Nordeste são os mais penalizados: Alagoas (AL) apresenta 23,9% de taxa de atraso, seguido de Maranhão (19,7%) e Piauí (16,0%). 
- **Implicação para o Negócio:** O frete já pesa 21,34% sobre o valor total do pedido. A correlação de 0,39 entre distância e tempo mostra que a matriz logística não consegue otimizar as entregas longas. Isso destrói margens e frustra clientes.

### 4.3. Satisfação e Reviews (A Voz do Consumidor)

O consumidor brasileiro é vocal quando o serviço falha, e o impacto logístico dita a nota final.

- **Dado em Destaque:** Embora 57,8% das avaliações sejam Nota 5, existe uma fatia preocupante de detratores (11,5% de Nota 1 e 3,2% de Nota 2). 
- **Interpretação Executiva:** 41,3% dos reviews deixam comentários escritos. A análise de texto revelou as principais palavras-chave nas reclamações: *"prazo"*, *"entregue"*, *"pedido"*. Validamos a causalidade através de Mann-Whitney U e Chi-Quadrado, comprovando uma correlação negativa (-0,229, p<0,001) entre atraso logístico e a nota.
- **Implicação para o Negócio:** O tempo médio de resposta da plataforma a um review é de longos 3,15 dias. Respostas lentas para clientes frustrados garantem a total alienação e queima definitiva da ponte para uma recompra.

### 4.4. Vendedores (Desigualdade e Performance)

O ecossistema é suportado por uma base muito concentrada, expondo risco de dependência de parceiros.

- **Dado em Destaque:** O Índice de Gini de 0,792 revela uma desigualdade brutal: 17,6% dos 3.095 vendedores geram expressivos 80% da receita total.
- **Interpretação Executiva:** A maior parte dos lojistas vende pouco. Além disso, identificamos 342 vendedores (aprox. 11% da base) operando com notas médias de avaliação inferiores a 3,0.
- **Implicação para o Negócio:** Vendedores ruins estão queimando a marca do marketplace perante o consumidor final. Ao mesmo tempo, 56% dos vendedores são especialistas focados em apenas 1 categoria, o que pode limitar as ações de *cross-selling* interno.

### 4.5. Segmentação Analítica (A Visão Estratégica)

Ao invés de tratar a base de forma homogênea, revelamos *personas* baseadas em dados através do K-Means.

#### Clientes (RFM K=4)
| Segmento | Qtd (%) | Recência Média | Valor Médio | Perfil Executivo |
| :--- | :--- | :--- | :--- | :--- |
| **Novos** | 54% | 178 dias | R$ 135 | O grande bolo de consumidores de "primeira e única vez". |
| **Em Risco** | 40% | 439 dias | R$ 135 | Base massiva já adormecida. |
| **Campeões Alto Valor** | 3% | 290 dias | R$ 1.196 | Compram itens caros, ticket médio fortíssimo. |
| **Campeões Recorr.** | 3% | 269 dias | R$ 290 | Frequência levemente maior, mas ainda inativos recentemente. |

#### Vendedores (K=3)
| Segmento | Qtd (%) | Receita Média | Nota | Perfil Executivo |
| :--- | :--- | :--- | :--- | :--- |
| **Regulares** | 82% | R$ 3.775 | 4,33 | Base sólida, precisa de escala e incentivos. |
| **Top Performers** | 1% | R$ 102.986 | 4,03 | A elite do faturamento. Curiosamente, a nota é inferior à dos regulares, por volume de pressão operacional. |
| **Problemáticos** | 17% | R$ 1.299 | 2,22 | Destruidores de valor. Entregas muito lentas (14,4 dias). |

---

## 5. Oportunidades Identificadas para IA Agêntica

A partir do diagnóstico doloroso de baixa recompra e atrito logístico, propomos uma arquitetura com **6 Agentes de IA Autônomos** focados na virada desses KPIs.

1. 🤖 **Agente de Logística Preditiva (LogiPredict)**
   - **Gatilho:** Assim que um pedido é despachado para AL, MA, PI, ou rotas críticas identificadas.
   - **Ação:** Monitora o status no trânsito (que representa 74% do tempo). Se houver anomalia ou risco da entrega passar dos 12 dias previstos, alerta o cliente preventivamente e re-calcula o prazo, gerenciando a ansiedade antes da reclamação formal.
   - **Impacto Esperado:** Redução de 30% nas avaliações negativas ligadas a prazo e logística.

2. 🤖 **Agente de Retenção — Anti-Churn (WinBack)**
   - **Gatilho:** Quando um cliente entra no 6º mês de inatividade (caminhando para compor os 58,61% de Churn).
   - **Ação:** Gera ofertas hiper-personalizadas utilizando o histórico de compras e produtos similares. Para os "Campeões de Alto Valor", autoriza a emissão de cupons agressivos de desconto no frete.
   - **Impacto Esperado:** Elevação da taxa de recompra de 3,00% para um benchmark mais saudável (estimado 7% em 12 meses).

3. 🤖 **Agente de Sucesso do Vendedor (SellerCare)**
   - **Gatilho:** Queda contínua de avaliações de um vendedor ou entrada no cluster "Problemáticos" (atualmente com 527 lojistas).
   - **Ação:** O agente bloqueia a exposição (BuyBox) deste vendedor automaticamente e envia um plano de ação gerado por IA apontando falhas de *SLA* de processamento interno (que hoje é de 3,28 dias).
   - **Impacto Esperado:** Limpeza automática do marketplace e aumento da nota média global.

4. 🤖 **Agente de Reviews & Sentimento (SentimentDesk)**
   - **Gatilho:** Inserção de uma avaliação com notas 1 ou 2 acompanhada de comentários de texto.
   - **Ação:** Reduz o tempo de resposta atual (3,15 dias) para menos de 5 minutos. O agente interpreta o motivo (ex: atraso), emite um pedido formal de desculpas, abre protocolo e, se aplicável, oferece ressarcimento parcial do frete de forma autônoma.
   - **Impacto Esperado:** Retenção imediata de detratores em momento de fúria e reversão potencial da nota.

5. 🤖 **Agente de Precificação & Frete (SmartFreight)**
   - **Gatilho:** Checkout de vendas inter-estado (63,8% das operações) ou cadastro de novo produto.
   - **Ação:** Como o frete impacta 21% do valor do pedido, o Agente busca e negocia em tempo real as APIs de diferentes parceiros logísticos analisando peso e volume, oferecendo o melhor balanço preço/prazo. Também propõe **kits/bundles** (cross-sell) para diluir o custo logístico e elevar o ticket médio (R$ 161,00).
   - **Impacto Esperado:** Aumento de conversão no carrinho e crescimento da receita vinculada.

6. 🤖 **Agente Orquestrador Executivo — BI (Maestro)**
   - **Gatilho:** Consulta do C-Level em linguagem natural ou sinais consolidados dos 5 agentes especialistas.
   - **Ação:** Roteia cada pergunta de negócio ao agente competente, consolida as respostas, resolve conflitos (ex.: Retenção quer desconto agressivo × Finanças acusa prejuízo) e gera relatórios executivos sob demanda (Text-to-SQL sobre o data warehouse).
   - **Impacto Esperado:** Decisão mais rápida e cerca de 40 horas/semana economizadas em consolidação manual de relatórios gerenciais.

---

## 6. Recomendações Estratégicas (Roadmap de Implantação)

Para o *board* diretivo, recomendamos as seguintes ações táticas priorizadas pelo modelo Custo x Benefício:

**Curto Prazo (Q1 - Q2):**
1. **Implantação Imediata do Agente de Reviews & Sentimento (SentimentDesk):** Não podemos tolerar 3 dias para responder um detrator. A automação desta camada tem ROI instantâneo.
2. **"Quarentena" Algorítmica de Vendedores Problemáticos:** Executar uma suspensão temporária dos 342 vendedores com nota abaixo de 3,0 para frear a degradação da marca.

**Médio Prazo (Q3):**
3. **Campanha "Primeira Recompra" orquestrada por IA:** Focar todos os esforços em resgatar a base inativa de 40%. A meta é provar a viabilidade de forçar o LTV para o patamar de R$ 300,00 na amostra impactada.
4. **Reengenharia Logística para o Nordeste:** Utilizar o *LogiPredict* atrelado a Centros de Distribuição Avançados (Cross-docking) para mitigar os gargalos em AL, MA e PI.

**Longo Prazo (Q4):**
5. **Transição para um Modelo de IA Agêntica Completo:** Implementar uma malha de agentes operando colaborativamente — o agente de reviews (SentimentDesk) informando o agente de qualidade de vendedores (SellerCare) em tempo real, sob a coordenação do orquestrador (Maestro), retroalimentando o sistema sem intervenção humana de analistas de nível 1.

---

## 7. Conclusão

A base da Olist comprova que o e-commerce no Brasil possui um tráfego fenomenal, validado por quase 100 mil pedidos faturados neste recorte de tempo. Contudo, os dados contam uma história de operações reativas, onde o cliente experimenta um serviço transacional sem brilho logístico e o parceiro vende sem o devido monitoramento de qualidade.

Com um custo de frete pesado (21,34%), atrasos focais (Nordeste) e um silêncio angustiante de mais de 3 dias no pós-venda, a plataforma pavimenta o caminho para a altíssima rejeição e inatividade (97% não efetuam segunda compra).

**A Inteligência Artificial não deve atuar apenas como um gerador de *dashboards*.** Nossa proposta provê um arsenal **Agêntico**, dando autonomia a sistemas que tomam micro-decisões críticas 24 horas por dia. Desde bloquear lojistas tóxicos a salvar uma venda com respostas em milissegundos. É através dessa transição de reativo para preditivo autônomo que este e-commerce deixará de focar apenas na receita primária e passará a construir fidelização e um LTV lucrativo e dominante.

---

## 8. Apêndice: Tabela Mestra de KPIs

| Categoria | Indicador | Valor / Resultado |
| :--- | :--- | :--- |
| **Financeiro** | Receita Total | R$ 16.008.872,12 |
| **Financeiro** | Ticket Médio | R$ 161,00 |
| **Financeiro** | LTV Estimado | R$ 165,20 |
| **Clientes** | Taxa de Recompra | 3,00% (Crítico) |
| **Clientes** | Taxa de Churn (> 6 meses) | 58,61% |
| **Clientes** | Concentração Receita | 10% dos clientes = 38,25% da receita |
| **Logística** | Tempo Médio Total | 12,56 dias |
| **Logística** | Taxa de Atrasos | 8,11% |
| **Logística** | Fator Frete | 21,34% do pedido total |
| **Satisfação** | NPS Proxy (Notas 1 e 2) | 14,7% de detratores severos |
| **Satisfação** | Tempo Resp. a Reviews | 3,15 dias |
| **Vendedores** | Concentração de Vendas | Gini 0,792 (17,6% geram 80% rec.) |
| **Vendedores** | Vendedores Notas Críticas | 342 com Nota < 3,0 |
| **Vendedores** | Tempo Proc. Vendedor | 3,28 dias (Gargalo interno) |

---
*Fim do Relatório. Versão gerada para aprovação do Conselho Deliberativo.*
