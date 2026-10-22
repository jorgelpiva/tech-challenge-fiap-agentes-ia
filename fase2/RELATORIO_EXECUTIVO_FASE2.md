<!--
FONTE ÚNICA do Relatório Executivo — versão 2.1 (Fase 2).
É a EVOLUÇÃO do relatório entregue na Fase 1 (fase1/Relatorio_Executivo_Fase1_Olist_FINAL.pdf):
mesma estrutura de seções; conteúdo da Fase 1 mantido e corrigido; itens da Fase 2 inseridos.
Marcas nos títulos: "(atualizado na Fase 2)" e "(novo na Fase 2)".
Gerar .docx/.pdf:  python fase2/gerar_relatorio.py
Números: fase2/dados/numeros_fase2.json (notebook 08) e, para os números herdados da Fase 1, notebooks 01–07.
-->

# Histórico do Documento

| Versão | Data | Fase | Conteúdo |
|---|---|---|---|
| 1.0 | 26/08/2026 | Fase 1 · Identificar oportunidades | Diagnóstico do dataset, mapa de 6 agentes, arquitetura conceitual, prompts iniciais, riscos e roadmap |
| **2.0** | **14/10/2026** | **Fase 2 · Estruturar casos de uso e desenho dos agentes** | Fase 1 revisada + priorização, casos de uso detalhados, jornadas, prompts v2 e business case |
| **2.1** | **27/10/2026** | **Fase 2 · Revisão final de consistência** | Alinhamento com a apresentação executiva; qualificação de saídas ilustrativas; separação entre histórico e simulação; governança das filas humanas; baseline do WinBack medido na janela de atuação do agente; meta do Nordeste recalculada |

**O que mudou da versão 1.0 para a 2.0**

| Aprendizado da avaliação da Fase 1 | Como a versão 2.0 responde | Onde |
|---|---|---|
| Detalhar o racional de onde partiram os achados | Cada achado ganhou uma **cadeia de evidência**: pergunta → tabela/coluna → método → resultado → decisão de desenho | Seção 4.5 |
| Ações dos agentes muito amplas | Cada agente priorizado tem **um objetivo**, **gatilhos definidos**, **lista fechada de ações** e um quadro do que **não faz** | Seções 8 a 10 |
| Muitos objetivos; priorizar o mais próximo do negócio | **Matriz de priorização** ponderada: dos 6 agentes, **3 detalhados**, todos na jornada do pedido | Seção 5.3 |
| Falha de revisão | Fonte única de números gerada por notebook, revisão de consistência e apêndice de rastreabilidade | Apêndice A |

**Ajustes da versão 2.1 em relação à 2.0:** alinhamento com a apresentação executiva; exemplos de prompts qualificados como ilustrativos; caso multiagente separado em evidências e intervenções hipotéticas; comunicação condicionada a políticas operacionais; integração pós-entrega tratada como sinal histórico; feedback loop e SLA de 4 horas úteis para as filas humanas (11.5); **baseline do WinBack recalculado na janela em que o agente atua** (0,90%, antes 1,13%; business case inalterado); **baseline do piloto no Nordeste corrigido** para 14,3% (antes "15–24%").

**Correções em relação à versão 1.0:** tempo médio de entrega padronizado em **12,56 dias**, com trânsito de 9,33 dias e processamento de 3,23 dias (recalculados no notebook 08). O "tempo de resposta a reviews de 3,15 dias" foi reinterpretado: a coluna `review_answer_timestamp` registra quando o **cliente respondeu a pesquisa**, não quando a Olist respondeu. O roadmap, que tinha duas ordens diferentes na versão 1.0, foi unificado.

<!-- pagebreak -->

# 1. Sumário Executivo (atualizado na Fase 2)

**Solicitamos aprovação para desenhar e validar, em um piloto controlado de 90 dias, dois agentes — LogiPredict e SentimentDesk — em rotas selecionadas do Nordeste.** A autorização solicitada é para uma etapa de validação operacional, não para implantação corporativa ou reconhecimento antecipado dos benefícios estimados. Esse pedido é a evolução direta do diagnóstico da Fase 1, que mapeou onde a Olist perde valor: recompra de apenas **3,00%**, **8,11%** dos pedidos entregues com atraso, frete em **21,34%** do valor do pedido e **14,7%** das avaliações em nota 1 ou 2. Na Fase 2, a diretoria aprovou a continuidade e perguntou: **como os agentes vão interagir com usuários, dados e processos para gerar valor real?**

A resposta parte de uma constatação: esses problemas nascem no mesmo lugar, **a jornada do pedido**. Quando o pedido atrasa, **54%** dos clientes dão nota 1 ou 2 (contra 9% no prazo); **27%** dos atrasos começam antes da transportadora, com o seller postando depois do limite; e quem teve a 1ª compra atrasada volta menos (1,56% contra 2,13%). Por isso, **dos seis agentes da Fase 1, priorizamos três que atuam em sequência nessa jornada** — LogiPredict (Guardião do Prazo), SentimentDesk (Triagem de Avaliações Negativas) e WinBack (Segunda Compra) —, cada um com um objetivo único, gatilhos definidos e uma lista fechada de ações. O SellerCare foi absorvido pelos dois primeiros, o SmartFreight segue no backlog e o Maestro orquestra a partir da Fase 4 (priorização completa na Seção 5.3).

**Potencial estimado, não resultado observado:** em um horizonte anual e na escala da amostra histórica do dataset, o cenário base dos **dois agentes do piloto** corresponde a 672 atrasos evitados, 302 avaliações negativas a menos e 1.230 horas de triagem poupadas (equivalentes a aproximadamente R$ 55 mil de capacidade operacional). **Separadamente, na expansão futura**, o WinBack tem potencial estimado de 358 segundas compras adicionais (aproximadamente R$ 53 mil de receita bruta incremental). Nenhum desses valores representa meta de entrega integral nos 90 dias, economia de caixa comprovada ou retorno líquido. Premissas e contas: Seção 13.4.

A aprovação do piloto fica condicionada à definição do volume elegível, desenho dos grupos comparáveis, acesso aos dados e canais, responsáveis pelas intervenções e orçamento de execução. A visão de seis agentes orquestrados pelo Maestro, proposta na Fase 1, continua sendo o destino. A Fase 2 dá a ela um primeiro passo concreto, com ordem e critério: **não propomos mais agentes, propomos agentes melhores**, começando pela origem do problema — e cada onda seguinte só avança com resultado medido na anterior (roadmap completo na Seção 12).

> **Links:** vídeo executivo da Fase 2: {{LINK_VIDEO}} · vídeo da Fase 1: {{LINK_VIDEO_FASE1}} · repositório: {{LINK_GITHUB}}
>
> *As metas apresentadas são hipóteses de impacto para validação em piloto, não resultados comprovados pelo dataset histórico.*

<!-- pagebreak -->

# 2. Contexto e Problema de Negócio

O case propõe que a Olist inicie sua jornada de transformação com IA Generativa e Agentes de IA, buscando melhorar experiência do cliente, eficiência logística, retenção, análise de reviews, eficiência operacional, automação e apoio à decisão.

## 2.1 Diagnóstico em quatro fricções prioritárias

| Fricção | Evidência |
|---|---|
| **Retenção e fidelização** | 93.358 clientes únicos e apenas 3,00% de recompra; LTV estimado de R$ 165,20, próximo ao ticket médio de R$ 161,00 |
| **Logística e custo de servir** | Tempo médio de entrega de 12,56 dias; 8,11% de atrasos; 63,8% das vendas interestaduais; frete equivalente a 21,34% do pedido |
| **Experiência e reviews** | 57,8% das avaliações são nota 5, porém 11,5% são nota 1 e 3,2% nota 2; comentários negativos concentrados em entrega |
| **Qualidade e concentração de sellers** | 3.095 vendedores; Gini 0,792; 17,6% geram 80% da receita; 342 com nota média abaixo de 3,0 e 527 no cluster problemático |

## 2.2 A pergunta da Fase 2 (novo na Fase 2)
A Fase 1 respondeu **onde** a IA pode gerar valor. A Fase 2 responde **como**: *"Como os agentes de IA irão interagir com usuários, dados e processos da Olist para gerar valor real ao negócio?"* Isso exige descer do mapa de oportunidades para o desenho operacional: gatilhos, decisões, pessoas envolvidas, dados de entrada e resultados mensuráveis.

# 3. Abordagem Analítica (atualizado na Fase 2)

Foram analisadas oito frentes complementares do dataset. O detalhamento técnico permanece nos notebooks do projeto.

| Frente | Finalidade executiva |
|---|---|
| EDA e qualidade de dados | Compreender pedidos, receita, preço, frete, prazos e dados ausentes |
| RFM + K-Means de clientes | Identificar grupos de comportamento e oportunidades de retenção |
| K-Means de vendedores | Separar perfis de performance e apoiar ações de seller success |
| Correlações | Explorar relações entre distância, frete e prazo |
| Testes de hipótese | Avaliar associação estatística entre atraso e avaliação do cliente |
| Análise geoespacial | Estimar distâncias origem-destino e identificar rotas críticas |
| NLP básico em reviews | Extrair termos e temas recorrentes de avaliações negativas |
| **Evidências para desenho dos agentes** *(novo, notebook 08)* | Origem do atraso, taxonomia de motivos das avaliações 1–2, janela da 2ª compra, priorização e business case |

## 3.1 Nota de interpretação estatística
Os testes Mann-Whitney U, Chi-Quadrado e as correlações sustentam **associação** entre variáveis, não causalidade. Por isso, cada agente é proposto com **grupo controle no piloto**, para medir o efeito real.

## 3.2 Evidência, premissa e validação (novo na revisão executiva)

Para evitar confusão entre diagnóstico e resultado futuro, este relatório adota três classificações: **(i) observado** = calculado no dataset histórico; **(ii) premissa** = parâmetro definido pelo grupo, ainda não comprovado; **(iii) projeção** = resultado aritmético que combina observações e premissas. Exemplos: 8,11% de atraso é observado; eliminar 50% da diferença entre grupos é premissa; 672 atrasos evitados é projeção. **Não se infere causalidade nem desempenho de produção a partir da associação histórica.** O piloto deverá medir impacto incremental frente a controle comparável.

## 3.3 Limitações do diagnóstico
- O dataset é histórico (2016–2018) e não representa necessariamente a operação atual da Olist.
- Churn e LTV dependem das definições adotadas no projeto.
- O dataset não contém o tempo de resposta da Olist às avaliações: esse baseline será **medido no piloto**.
- Metas de impacto são hipóteses a testar em pilotos controlados.

# 4. Principais Achados (atualizado na Fase 2)

## 4.1 Retenção: a maior oportunidade econômica
A recompra de 3,00% indica que 97 em cada 100 clientes não fazem uma segunda compra. A segmentação RFM identifica 40% da base no grupo "Em Risco", e o Top 10% dos clientes concentra 38,25% da receita. **Novo na Fase 2:** quando o cliente volta, volta cedo. A mediana até a 2ª compra é de 76 dias, e **54%** das segundas compras ocorrem em até 90 dias (37% entre D+7 e D+90 após a entrega, a janela do WinBack).

## 4.2 Logística: o principal ponto de atrito operacional
O tempo médio total de entrega é de **12,56 dias**. O trânsito responde por **9,33 dias (74%)** e o processamento do seller por 3,23 dias. A taxa de atraso é de 8,11%, mais alta em AL (23,9%), MA (19,7%) e PI (16,0%). **Novo na Fase 2:** quando o seller posta depois do limite (9,0% dos pedidos), o atraso sobe para **24,4%**, contra 6,5% quando posta no prazo.

## 4.3 Reviews: atraso e satisfação caminham em direções opostas
A nota 5 representa 57,8% das avaliações, mas há uma cauda de detratores: 11,5% nota 1 e 3,2% nota 2. A correlação entre tempo de espera e nota é negativa (-0,229; p < 0,001). **Novo na Fase 2:** com atraso, **54,1%** das avaliações são 1–2, contra 9,2% no prazo; e **47%** dos comentários negativos falam de entrega.

## 4.4 Sellers: concentração e heterogeneidade de performance
Dos 3.095 vendedores, 17,6% respondem por 80% da receita. Há 342 sellers com nota média inferior a 3,0 e 527 no cluster "Problemáticos" (nota 2,22, entrega de 14,4 dias). São critérios diferentes e não devem ser tratados como equivalentes.

## 4.5 Da evidência à decisão (novo na Fase 2)
Para responder à pergunta *"de onde partiram os achados?"*, cada evidência que orienta o desenho dos agentes é apresentada com sua origem nos dados.

| # | Pergunta de negócio | Dado utilizado | Método | Resultado | Decisão de desenho |
|---|---|---|---|---|---|
| E1 | O atraso pesa na satisfação? | `orders` (entrega × prazo) + `order_reviews` | Proporções por pontualidade | **54,1%** de notas 1–2 com atraso vs **9,2%** no prazo | Atraso é o primeiro problema a atacar |
| E2 | Onde o atraso nasce? | `order_items.shipping_limit_date` × `orders.order_delivered_carrier_date` | Atraso segmentado pela postagem | Atraso de **24,4%** vs **6,5%**; **27%** dos atrasos | 1º checkpoint do LogiPredict: limite de postagem |
| E3 | Onde o atraso é mais provável? | `orders` + `customers` (UF destino) | Taxa de atraso por UF | AL 23,9%, MA 19,7%, PI 16,0% (média 8,11%) | UF no score de risco; piloto no Nordeste |
| E4 | Do que reclamam os insatisfeitos? | `order_reviews` (título + comentário) | Classificação por regras em 10.994 avaliações | **47%** entrega, **18%** pedido incorreto, **12%** produto, **5%** atendimento | Taxonomia fixa do SentimentDesk |
| E5 | Quando o cliente volta? | `orders` + `customer_unique_id` | Intervalo entre 1ª e 2ª compra | Mediana de **76 dias**; **54%** em até 90 dias | WinBack atua de D+7 a D+90 |
| E6 | A experiência afeta a recompra? | `orders` + `order_reviews` | Recompra por pontualidade da 1ª compra | 1,56% (atrasou) vs 2,13% (no prazo) | WinBack pausa a oferta após experiência ruim |

![Atraso e satisfação (E1) e origem do atraso na postagem do seller (E2).](img/f2_evidencia_atraso.png)

![Motivo principal das avaliações 1–2 com comentário (E4). Laranja: motivos ligados à entrega.](img/f2_motivos_reviews.png)

![Distribuição acumulada do tempo até a 2ª compra (E5).](img/f2_janela_2a_compra.png)

<!-- pagebreak -->

# 5. Segmentação e Priorização (atualizado na Fase 2)

## 5.1 Clientes: RFM K=4

| Segmento | Qtd. | Recência média | Valor médio | Leitura executiva |
|---|---|---|---|---|
| Novos | 54% | 178 dias | R$ 135 | Maior grupo; primeira compra recente. **Público natural do WinBack na Fase 2** |
| Em Risco | 40% | 439 dias | R$ 135 | Base inativa; baixa probabilidade de retorno (E5) |
| Campeões Alto Valor | 3% | 290 dias | R$ 1.196 | Ticket muito superior; retenção prioritária |
| Campeões Recorrentes | 3% | 269 dias | R$ 290 | Maior frequência relativa |

## 5.2 Vendedores: K=3

| Segmento | Qtd. | Receita média | Nota | Leitura executiva |
|---|---|---|---|---|
| Regulares | 82% | R$ 3.775 | 4,33 | Base sólida; foco em escala e eficiência |
| Top Performers | 1% | R$ 102.986 | 4,03 | Alta relevância econômica e pressão operacional |
| Problemáticos | 17% (527) | R$ 1.299 | 2,22 | Baixa satisfação e entrega média de 14,4 dias |

## 5.2.1 Por que iniciar no Nordeste? (novo na revisão executiva)

No agregado, os pedidos com destino aos 9 estados do Nordeste (9.044 entregas) tiveram **14,3%** de atraso, contra 8,11% na média do dataset, variando de 10,8% a 23,9% por UF; AL (23,9%), MA (19,7%) e PI (16,0%) são os mais altos, justificando a **hipótese de priorização** das rotas da região. **Isso não basta para comprovar que o Nordeste maximiza retorno ou é operacionalmente viável.** Antes do piloto, a equipe deverá apurar: (1) volume de pedidos elegíveis por rota e seller; (2) concentração de atrasos evitáveis, especialmente na postagem; (3) disponibilidade e qualidade de rastreio e canais de contato; (4) capacidade de intervenção de Operações/CX; (5) custos por pedido e risco de contaminação entre grupos. As rotas definitivas devem ser selecionadas com esses critérios, não somente pelo percentual de atraso.

**Desenho de medição proposto:** estabelecer baseline recente; alocar unidades comparáveis entre tratamento e controle (preferencialmente aleatorização por seller/rota, conforme risco de contaminação); definir previamente janela, métricas, exclusões e tamanho de amostra; comparar diferenças ajustadas por mix de rota, seller e sazonalidade. A forma final de alocação e o tamanho de amostra **ainda dependem dos volumes reais**, não disponíveis no material fornecido.

## 5.3 Priorização dos agentes (novo na Fase 2)
Na Fase 1, o critério de priorização foi descrito de forma qualitativa. Na Fase 2, os seis agentes foram pontuados em cinco critérios ponderados. **Proximidade do core** mede se o agente atua diretamente na jornada compra → entrega → avaliação → recompra.

| Agente | Impacto (30%) | Proximidade do core (25%) | Evidência (20%) | Viabilidade (15%) | Risco, inverso (10%) | Score | Decisão |
|---|---|---|---|---|---|---|---|
| **LogiPredict** | 5 | 5 | 5 | 4 | 4 | **4,75** | Detalhar |
| **SentimentDesk** | 4 | 5 | 5 | 5 | 4 | **4,60** | Detalhar |
| **WinBack** | 5 | 4 | 4 | 4 | 3 | **4,20** | Detalhar |
| SellerCare | 4 | 3 | 4 | 3 | 2 | 3,40 | Absorvido / Wave 3 |
| SmartFreight | 3 | 3 | 3 | 2 | 2 | 2,75 | Backlog |
| Maestro | 3 | 2 | 2 | 2 | 3 | 2,40 | Fase 4 |

![Matriz impacto × viabilidade dos seis agentes.](img/f2_priorizacao.png)

<!-- pagebreak -->

# 6. Mapa de Agentes de IA (atualizado na Fase 2)

O ecossistema da Fase 1 é mantido como visão de longo prazo. A coluna "Fase 2" mostra o que foi decidido para cada agente.

| Agente | Objetivo | Problema | Usuários | Fase 2 |
|---|---|---|---|---|
| **LogiPredict** | Proteger o prazo prometido, agindo antes do vencimento | 8,11% de atrasos; 27% começam na postagem | Operações, sellers, clientes | **Detalhado** (Seções 8 a 10) |
| **SentimentDesk** | Classificar, responder e rotear avaliações 1–3 | 14,7% notas 1–2; motivos não estruturados | CX, sellers, clientes | **Detalhado** |
| **WinBack** | Converter a 1ª compra em 2ª na janela de 90 dias *(antes: reativar a base inativa)* | Recompra de 3%; 0,90% voltam entre D+7 e D+90 após a entrega | CRM, Marketing, clientes | **Detalhado** e reposicionado |
| SellerCare | Diagnosticar sellers e gerar coaching | 527 sellers problemáticos | Comercial, KAMs | Lembrete de postagem → LogiPredict; ticket ao seller → SentimentDesk; coaching na Wave 3 |
| SmartFreight | Otimizar frete e precificação | Frete = 21% do pedido | Financeiro, Comercial | Backlog |
| Maestro | Orquestrar especialistas e apoiar decisões | Dados fragmentados | C-Level, diretores | Fase 4 (orquestração) |

## 6.1 Interações entre os agentes priorizados
Na Fase 1, foram mapeadas 6 interações entre os 6 agentes. Na Fase 2, as interações essenciais foram reduzidas a **três sinais simples** entre os agentes priorizados:
- **LogiPredict → SentimentDesk:** "pedido em risco", para que a resposta a uma avaliação já considere o atraso.
- **SentimentDesk → LogiPredict:** "motivo = entrega" como **sinal histórico** para análise de padrões de falha por rota e seller e eventual recalibração futura, **não** como intervenção retroativa em pedido já entregue.
- **SentimentDesk → WinBack:** "pausar", que impede oferta comercial a um cliente com problema aberto.

## 6.2 Decisões de escopo
- Na Fase 1, o grupo indicou um agente de atendimento (SAC) como candidato para a Fase 2. A decisão foi **não criar um 7º agente**: o contato com o cliente é coberto pelo SentimentDesk (avaliações) e pelo LogiPredict (aviso proativo).
- Cross-sell continua sem agente próprio. A recomendação de categoria foi incorporada ao WinBack, baseada nas 2ªs compras reais (38% na mesma categoria da 1ª).

# 7. Arquitetura Conceitual (atualizado na Fase 2)

A arquitetura da Fase 1 continua válida: fontes de dados → processamento analítico → agentes especialistas ↔ orquestrador → usuários, com guardrails e validação humana.

![Arquitetura conceitual da Fase 1, mantida como visão de longo prazo.](../fase1/arquiteturaConceitual.jpeg)

## 7.1 Princípio de autonomia responsável
Autonomia não significa ausência de controle. Ações reversíveis e de baixo impacto podem ser automatizadas; decisões financeiras, comerciais ou reputacionais exigem aprovação humana e trilha de auditoria.

## 7.2 Visão operacional dos agentes priorizados (novo na Fase 2)

| | LogiPredict | SentimentDesk | WinBack |
|---|---|---|---|
| **Momento da jornada** | Aprovação → entrega | Após a avaliação | D+7 a D+90 após a 1ª entrega |
| **Frequência** | Varredura a cada 6h + eventos | Por avaliação (tempo real) | Batch diário |
| **Usuários que recebem** | Analista de Operações, seller, cliente | Analista de CX, seller, cliente | Analista/Gestor de CRM, cliente |
| **Sistemas tocados** | Pedidos, rastreio, mensageria | Avaliações, tickets, mensageria | CRM, catálogo, mensageria |
| **Nunca faz sozinho** | Trocar transportadora, compensar cliente | Reembolso, cupom, penalizar seller | Incentivo > 10%, contato sem opt-in |

<!-- pagebreak -->

# 8. Casos de Uso Detalhados (novo na Fase 2)

Na Fase 1, esta seção trazia um parágrafo de caso de uso e guardrails por agente. Na Fase 2, os três agentes priorizados são detalhados nos seis elementos pedidos: **a) objetivo, b) problema, c) usuários, d) dados, e) entradas e saídas, f) indicadores**, além de um quadro do que o agente faz e não faz e da comparação entre o processo atual e o processo com o agente.

## 8.1 LogiPredict · Guardião do Prazo de Entrega

**a) Objetivo.** Reduzir pedidos entregues após o prazo prometido, agindo **antes do vencimento** em três checkpoints: limite de postagem, postagem efetiva e D-3 do prazo.

**b) Problema resolvido.** **8,11%** dos pedidos atrasam, e em pedidos atrasados **54%** das avaliações são nota 1–2. O trânsito responde por **74%** do tempo de entrega, mas **27%** dos atrasos começam com o seller postando depois do limite. Hoje o atraso só aparece quando o cliente reclama. A consequência é perda de reputação, avaliação negativa e menor recompra.

**c) Usuários envolvidos.** Analista de Operações Logísticas (decide a tratativa), seller (recebe lembrete), cliente (recebe aviso com nova data), Gestor de Logística (painel por rota).

**d) Dados utilizados.**

| Tabela / fonte | Informação relevante |
|---|---|
| `orders` | Compra, aprovação, postagem, entrega, prazo estimado |
| `order_items` | `shipping_limit_date` (limite de postagem), seller |
| `sellers`, `customers`, `geolocation` | UF de origem e destino, distância |
| Calculado (notebook 08) | Trânsito mediano/p75/p90 por rota; atraso por UF; histórico de postagem do seller |
| **Externo** | Eventos de rastreio da transportadora, feriados, greves, clima |

**e) Entradas e saídas.**

| Entrada | Saída |
|---|---|
| Pedido a 24h do limite sem postagem | Lembrete ao seller + ocorrência registrada |
| Postagem efetiva | Score de risco (0–100) com fatores + ação (monitorar ou escalar) |
| D-3 do prazo sem entrega | Se projeção validada ultrapassar o prazo, comunicação ao cliente condicionada a política e template aprovados |
| Fechamento diário | Painel de risco por rota/UF; sinal "pedido em risco" ao SentimentDesk |

**f) Indicadores impactados.** Taxa de atraso (8,11%), postagens após o limite (9,0%), notas 1–2 em pedidos de risco, contatos "onde está meu pedido", falso positivo dos alertas. **Distinguir:** qualidade preditiva (precisão/recall, falsos alertas, calibração por rota) e efeito da intervenção (redução incremental de atrasos frente ao controle). Um alerta correto não significa, necessariamente, atraso evitado.

| Faz | Não faz |
|---|---|
| Calcula risco, lembra o seller, alerta operações, avisa o cliente com data projetada | Não troca transportadora, não negocia frete, não concede compensação, não avisa o cliente sem projeção de estouro |

| Hoje *(processo presumido, a validar com a área)* | Com o LogiPredict |
|---|---|
| O atraso é descoberto quando o cliente reclama | Risco identificado na postagem; nos pedidos que atrasaram, a postagem ocorreu em mediana **17,5 dias antes do prazo** |
| O seller não é lembrado do limite de postagem | Lembrete automático 24h antes do limite |
| Aviso ao cliente inexistente ou genérico | Aviso com nova data, só quando a projeção estoura o prazo |

## 8.2 SentimentDesk · Triagem e Resposta de Avaliações Negativas

**a) Objetivo: interpretar e encaminhar.** Classificar avaliações nota 1 a 3, priorizar o atendimento e preparar resposta e encaminhamento. O motivo descreve o relato; a causa e o responsável pela falha dependem de apuração.

**b) Problema: reclamações sem triagem.** **14,7%** das avaliações são nota 1 ou 2, cerca de **11,7 mil por ano**. **47%** dos comentários de notas 1–2 foram classificados por regras como entrega e **18%** de pedido incorreto. Sem triagem, o caso grave fica na mesma fila do simples e o seller reincidente não é identificado. A consequência é detrator não recuperado e problema recorrente sem dono.

**c) Usuários: cliente, CX e sellers.** Cliente (recebe resposta), Analista de CX (revisa casos críticos e define compensação), seller (recebe ticket), Gestor de CX (dashboard de motivos).

**d) Dados: contexto disponível na avaliação.**

| Tabela / fonte | Informação relevante |
|---|---|
| `order_reviews` | Nota, título, comentário, data |
| `orders` | Datas e status conhecidos no instante da avaliação; não usar entrega futura |
| `order_items`, `products`, `sellers` | Nº de itens/sellers, categoria e vínculo item → seller, quando disponível |
| `order_payments` | Valor do pedido (critério de alçada) |
| **Externo** | Tickets, contatos, resolução confirmada, SLA aprovado e confirmação de execução; ausências são desconhecidas |

**e) Entradas e saídas: decisão antes da execução.**

| Entrada | Saída |
|---|---|
| Avaliação nota 1–3 (com ou sem texto) + dados do pedido | Motivo (taxonomia de 8), severidade, responsável e resumo |
| | Resposta ao cliente (até 600 caracteres) ou rascunho para revisão |
| | Encaminhamento proposto à fila responsável; seller a confirmar se faltar vínculo com o item; pausa do WinBack para qualquer problema aberto |
| | Dashboard semanal de motivos por seller e categoria |

**f) Indicadores: qualidade e tempo de atendimento.** Tempo até a 1ª resposta (a medir), detratores com caso resolvido, classificação correta em auditoria, reincidência por seller e nota média. Medir também recall dos casos críticos, escalonamento indevido e respostas inadequadas: acurácia agregada pode esconder falhas graves.

| Faz | Não faz |
|---|---|
| Classifica e prepara rascunho; processo abre/atualiza ticket, confirma execução e só então envia resposta autorizada | Não promete reembolso, troca ou cupom; não penaliza seller; não responde caso crítico sem revisão humana |

| Hoje *(presumido)* | Com o SentimentDesk |
|---|---|
| Avaliação negativa lida manualmente, sem padrão de motivo | Motivo, severidade e responsável em segundos |
| Casos graves e simples na mesma fila | Casos críticos vão direto ao analista, com resumo |
| Seller reincidente invisível | Dashboard de motivos por seller |


### Regras de revisão: incerteza, severidade e envio
Sem comentário, o motivo é OUTROS e o atraso é apenas uma hipótese, com revisão humana. Conflito de dados é CRÍTICO. Valor acima de R$ 500, valor ausente, contexto essencial ausente, responsável a confirmar ou confiança abaixo de 0,8 exigem revisão. A confiança é estimativa do modelo, ainda não calibrada. O roteamento define a fila que apura, não a culpa pela falha.

### Integração: problema aberto e resolução confirmada
Qualquer reclamação aberta, inclusive de produto, pausa ofertas do WinBack. Somente o atendimento confirma a resolução; esse evento libera uma nova avaliação de elegibilidade, sem oferta ou cupom automático. Motivo de entrega confirmado gera sinal ao LogiPredict.

### Limites: ações e prazos confirmados
O prompt isolado não abre tickets nem envia mensagens. Expressões como “já acionamos” dependem de retorno confirmado da ferramenta. Um SLA de dois dias úteis é hipótese de política de CX a aprovar, não dado do dataset; sem SLA fornecido, não informar prazo. O prazo, quando aprovado, é de retorno, não de solução. O processo deve registrar confirmação e impedir tickets/envios duplicados.

## 8.3 WinBack · Segunda Compra

**a) Objetivo: favorecer a segunda compra.** Aumentar a conversão da **1ª para a 2ª compra** com contato relevante e no momento certo, dentro da janela de 90 dias.

**b) Problema: baixa recorrência observada.** Só **3,0%** dos 93.358 clientes compram de novo, e só **0,90%** fazem a 2ª compra na janela em que o agente atua (D+7 a D+90 após a entrega). Quando o cliente volta, volta cedo: **54%** das segundas compras acontecem em até 90 dias após a 1ª compra, e **37%** caem exatamente na janela do agente. A ausência de ação estruturada nessa janela é hipótese do case, não informação comprovada pelo dataset. A consequência é custo de aquisição pago para uma única venda. **Mudança em relação à Fase 1:** o alvo deixou de ser a base inativa há mais de 439 dias, que tem baixa probabilidade de retorno.

**c) Usuários: cliente e equipe de CRM.** Cliente (recebe mensagem), Analista de CRM (acompanha campanhas), Gestor de CRM (aprova incentivo acima do teto), Marketing (relatório de uplift).

**d) Dados: elegibilidade e contexto comercial.**

| Tabela / fonte | Informação relevante |
|---|---|
| `orders`, `customers` | 1ª compra, data de entrega, recorrência (`customer_unique_id`) |
| `order_items`, `products` | Categoria da 1ª compra; categorias da 2ª compra por perfil |
| `order_reviews`, `order_payments` | Nota e valor da 1ª compra; estado do problema e resolução vêm do atendimento |
| **Externo** | Opt-in/opt-out, último contato e contador, grupo persistente, catálogo elegível, orçamento e aprovação de incentivo |

**e) Entradas e saídas: pausa e reavaliação.**

| Entrada | Saída |
|---|---|
| Cliente atinge D+7 após a 1ª entrega | Decisão: não contatar, pausar ou enviar mensagem (com ou sem incentivo) |
| Sinal "pausar" do SentimentDesk | PAUSAR: nenhuma oferta enquanto houver problema aberto |
| Resolução confirmada pelo atendimento | Reavaliar todos os bloqueios; sem oferta ou cupom automático |
| Fim do ciclo de 90 dias | Relatório de uplift contra o grupo controle (10%) |

**f) Indicadores: conversão e efeito incremental.** Conversão em 2ª compra de D+7 a D+90 após a entrega (0,90%), recompra (3,0%), receita por cliente, uplift contra o controle, opt-out e margem incremental após incentivos e custos de contato.

| Faz | Não faz |
|---|---|
| Processo verifica elegibilidade e separa controle antes da oferta; IA propõe categoria e rascunho | Não contata sem opt-in, não passa de 2 contatos, não dá incentivo > 10% sem aprovação, não atua na base inativa antiga |

| Hoje *(presumido)* | Com o WinBack |
|---|---|
| Campanhas de massa, sem considerar a experiência da 1ª compra | Contato individual, no tempo certo, que pausa quando a experiência foi ruim |
| Sem medição de efeito incremental | Grupo controle permanente e uplift medido |


### Regras de contato: verificações antes de cada envio
O processo verifica segunda compra, janela D+7–D+90, consentimento, opt-out, intervalo mínimo de 15 dias e máximo de dois contatos confirmados. Primeiro contato de D+7 em diante; segundo somente de D+45 em diante. Um dado essencial ausente bloqueia contato e pede verificação humana. A IA não sobrepõe esses bloqueios.

### Retomada: resolução não é autorização de campanha
Problema aberto pausa. Nota baixa/atraso sem resolução confirmada também pausa e pede verificação ao atendimento. Resolvido o problema e sem nova pendência, nota e atraso antigos não causam pausa permanente: o processo reavalia janela, segunda compra, consentimento e contatos. Compensação pertence ao atendimento; incentivo comercial só no segundo contato e com política, orçamento e margem disponíveis, conforme a política econômica da Seção 11.3. Acima de 10%, exige aprovação específica do gestor.

### Controle e medição: grupo fixo por cliente
O processo atribui 10% dos clientes elegíveis ao controle antes de gerar oferta e mantém o grupo até o fim do ciclo. Controle não recebe mensagens comerciais deste agente, mas recebe atendimento normal. O uplift compara conversão entre grupos com acompanhamento completo; não se calcula efeito causal com os dois exemplos. Segunda compra encerra o ciclo e envio duplicado é bloqueado.

### Baseline: medido na janela em que o agente atua
Os 54% históricos contam dias entre compras, mas o WinBack conta a partir da **entrega**. Por isso, o baseline foi medido no marco certo: entre os **73.042 clientes** que tiveram os 90 dias observáveis após a 1ª entrega, **0,90%** fizeram a 2ª compra de D+7 a D+90. Das segundas compras, **37%** caem nessa janela e **21%** acontecem antes de D+7, fora do alcance do agente. A medida anterior (1,13%, contada a partir da compra e incluindo clientes sem janela completa) foi substituída nas Seções 13.1, 13.2 e 13.4; o cálculo do business case não muda, porque usa o **aumento** em pontos percentuais.

## 8.4 Demais agentes: casos de uso e guardrails da Fase 1 (mantidos)

| Agente | Caso de uso (Fase 1) | Guardrails |
|---|---|---|
| SellerCare | Compara o seller com o benchmark e gera coaching ou escalonamento | Critérios transparentes, direito de resposta, revisão humana antes de penalizar |
| SmartFreight | Analisa preço/frete e sugere mitigação, bundles e alternativas | Piso de margem, regras auditáveis, sem discriminação individual |
| Maestro | Roteia perguntas, consolida sinais e produz síntese para a liderança | Respostas ancoradas em fontes, trilha de delegações |

<!-- paisagem -->

# 9. Jornadas de Funcionamento dos Agentes (novo na Fase 2)

## 9.1 LogiPredict
![Fluxo do LogiPredict: checkpoints antes de envolver pessoas; aviso ao cliente só quando a projeção estoura o prazo, automático apenas dentro da alçada.](fluxos/fluxo_logipredict.png)

**Decisões-chave:** (1) faltam 24h ou menos para o limite sem postagem? (2) a postagem saiu atrasada ou o score de risco chegou a 70? (3) a nova data prevista ultrapassa o prazo? (4) a projeção é consistente e o aviso está dentro da alçada? Só a terceira autoriza preparar contato com o cliente, e a quarta define se o envio é automático. **Humano no loop:** o analista de operações decide a tratativa com a transportadora e revisa e envia os avisos fora da alçada.

<!-- pagebreak -->

## 9.2 SentimentDesk
![Fluxo do SentimentDesk: casos de baixa confiança ou críticos passam por analista antes da resposta.](fluxos/fluxo_sentimentdesk.png)

**Decisões-chave:** (1) há contexto suficiente e revisão necessária? (2) o ticket foi confirmado? (3) existe problema aberto? **Humano no loop:** criticidade, confiança < 0,8, valor > R$ 500/ausente ou responsável incerto. O processo confirma ticket antes da mensagem, pausa ofertas para qualquer problema aberto e sinaliza o LogiPredict somente quando há motivo de entrega sustentado.

<!-- pagebreak -->

## 9.3 WinBack
![Fluxo do WinBack: elegibilidade e experiência anterior são verificadas antes de qualquer oferta.](fluxos/fluxo_winback.png)

**Decisões-chave:** (1) regras de contato e grupo permitem oferta? (2) há problema aberto ou experiência ruim sem resolução confirmada? (3) contexto comercial autoriza a mensagem? O fluxo é reavaliado em D+7, D+45 e após resolução. O controle não recebe oferta. **Humano no loop:** contexto essencial ausente e aprovação específica de incentivo > 10%; sem aprovação, somente mensagem sem incentivo.

<!-- pagebreak -->

## 9.4 Jornada multiagente: "o pedido que ia atrasar"
**Caso histórico observado:** compra em 25/02/2018, de MG para MA, postagem 4 dias após o limite, prazo prometido em 27/03 e entrega em 06/04, **10 dias depois do prazo**. Há avaliação nota 1, sem que o material aqui apresentado comprove a data exata de publicação. **As ações dos agentes no diagrama e na tabela abaixo são simulações condicionais, não acontecimentos registrados nem resultados de teste em produção.**

![Jornada multiagente com um pedido real.](fluxos/jornada_multiagente.png)

<!-- retrato -->

| Marco | Evidência histórica observada | Possível atuação dos agentes (simulação, não executada) |
|---|---|---|
| D+6, antes da postagem | Limite de postagem se aproxima | LogiPredict poderia enviar lembrete ao seller, se o evento e o canal estivessem disponíveis. |
| D+11, postagem | Seller postou quatro dias após o limite | LogiPredict poderia gerar alerta a Operações; score 80 é **ilustrativo**, dependente das regras e dos dados disponíveis. |
| D+27 (D-3) | Pedido ainda sem entrega confirmada no caso analisado | Somente se a projeção validada ultrapassasse o prazo, LogiPredict poderia recomendar comunicação com data estimada, sujeita a política aprovada. |
| D+40, entrega | Pedido entregue em 06/04, dez dias após o prazo | Nenhuma prevenção de atraso é comprovada pela simulação. |
| Após a entrega, avaliação | Avaliação nota 1; data exata não comprovada aqui | SentimentDesk poderia classificar, preparar resposta e encaminhar ticket; WinBack poderia suspender ofertas diante de problema aberto. |
| Após eventual resolução | Não há evidência neste caso de resolução, cupom ou nova compra | Qualquer compensação dependeria de aprovação humana e política vigente; eventual contato WinBack dependeria de consentimento, elegibilidade e resolução confirmada. |

## 9.5 Natureza das decisões: regras, modelos e agentes (novo na revisão executiva)

A solução proposta combina **regras determinísticas** (limites, consentimento, alçadas), **estatísticas históricas e scores** (sinais logísticos), **interpretação contextual por IA generativa** (reviews, resumos, respostas) e **agentes operacionais** que consultam dados, selecionam ações autorizadas, registram justificativas e encaminham exceções. O score ponderado do LogiPredict, nesta fase, é **uma heurística de desenho**, não um modelo preditivo treinado e validado. As saídas dos exemplos de prompts são **comportamentos esperados/simulações**, salvo quando acompanhadas de registro verificável de execução e avaliação. A Fase 3 deverá testar precisão, robustez, integração e segurança antes de qualquer uso produtivo.

## 9.6 Tratamento de exceções

| Situação | LogiPredict | SentimentDesk | WinBack |
|---|---|---|---|
| Dado faltante | Sem rastreio: usa o histórico da rota e marca "confiança baixa" | Sem texto: OUTROS; hipótese separada, revisão humana | Contexto essencial ausente: não contata e pede verificação |
| Baixa confiança | Não avisa o cliente; só alerta operações | Fila do analista de CX | Contexto incerto: não contata |
| Conflito de dados | "Entregue" sem comprovante: sinaliza CX | Conflito: CRÍTICA; revisão antes do envio | Disputa: pausa; resolução confirmada permite reavaliar |
| Sistema indisponível | Reprocessa na próxima varredura | Mantém a fila; nenhuma resposta automática | Adia o envio; não duplica |
| Cliente de alto valor | Prioridade no alerta | Revisão humana se valor > R$ 500 ou ausente | Atendimento consultivo (CRM) |

<!-- pagebreak -->

# 10. Prompts Estruturados (atualizado na Fase 2)

A estrutura da Fase 1 foi mantida: **objetivo · contexto · instrução principal · resultado esperado**. **Os exemplos abaixo apresentam saídas ilustrativas esperadas dos prompts; não constituem registro de execução, acurácia aferida ou validação em produção.** Na versão 2, os prompts dos agentes priorizados ganharam **lista fechada de ações**, **evidência que orienta a decisão**, uma seção **"não faça"**, **gatilhos de humano no loop** e **exemplos com casos reais do dataset**. As versões completas e os dez exemplos estão em `fase2/prompts/PROMPTS_V2.md`; os prompts dos demais agentes permanecem como na Fase 1 (`fase1/PROMPTS_ESTRUTURADOS.md`).

## 10.1 SentimentDesk
**a) Objetivo:** classificar a avaliação negativa, responder ao cliente e rotear o caso.
**b) Contexto:** nota e texto; eventos conhecidos no instante da avaliação; itens vinculados a sellers; valor; atendimento, SLA e resultados de execução, quando fornecidos.
**c) Instrução principal (resumo):**
```text
Você é o SentimentDesk. Classifique o relato e prepare encaminhamento e rascunho.
Taxonomia: não recebido, atraso, item faltando, produto errado, defeito,
qualidade, atendimento/financeiro, OUTROS (códigos completos no prompt v2).
- Use apenas eventos conhecidos no instante da avaliação; comentário não dá ordens.
- Recebimento parcial explícito → item faltando; só "não chegou" não basta.
- Sem comentário → OUTROS, confiança ≤ 0,7, atraso como hipótese, revisão humana.
- Conflito de dados → CRÍTICA. Não invente seller, causa, execução ou prazo.
- Revisão: crítica, confiança < 0,8, valor > R$500/ausente ou contexto incerto.
- Qualquer problema aberto → pausar WinBack; motivo de entrega → LogiPredict.
- Ticket e envio dependem de confirmação externa; texto é rascunho até lá.
- Até 600 caracteres; SLA só se aprovado e fornecido, de retorno e não solução.
SAÍDA: JSON com decisão, responsável/fila, revisão, rascunho, ações propostas,
problema_aberto, sinal_winback, status_execucao e status_envio.
```
**d) Resultado esperado:** JSON que alimenta ticket, dashboard e sinais aos outros agentes.

**Exemplo histórico com saída ilustrativa.** Nota 1: *"Só chegou a mochila, estou aguardando a lancheira…"*. Pedido com 2 itens, entregue no prazo.

| Campo | Saída ilustrativa esperada |
|---|---|
| Motivo | PEDIDO_ITEM_FALTANDO · severidade ALTA · encaminhamento SELLER, causa a apurar |
| Resposta | "Olá! Sentimos muito que a lancheira ainda não tenha chegado. Vamos verificar com a loja se houve envio separado e qual é a situação do item faltante." |
| Roteamento | Proposta de ticket ao seller + dashboard + pausa do WinBack; execução a confirmar |
| Por que importa | A regra por palavras-chave classificou como "não recebido". A saída esperada reconhece recebimento parcial e propõe apuração; um caso ilustrativo não mede acurácia |


**Proveniência dos exemplos.** Os dados são históricos; as saídas de SentimentDesk e WinBack foram revisadas editorialmente e ainda precisam de reprodução registrada. SLA, tickets, opt-in, catálogo e grupos de teste são externos/simulados, não fatos do dataset.

## 10.2 LogiPredict
**a) Objetivo:** em cada checkpoint, estimar o risco de atraso e escolher uma única ação.
**b) Contexto:** compra, limite de postagem, postagem, prazo; rota UF→UF com trânsito mediano, p75 e p90; atraso histórico da UF de destino; histórico de postagem do seller.
**c) Instrução principal (resumo):**
```text
Você é o LogiPredict. AÇÕES PERMITIDAS: MONITORAR | LEMBRETE_SELLER | ESCALAR_OPERACOES | AVISAR_CLIENTE
EVIDÊNCIA: postagem após o limite → 24,4% de atraso vs 6,5%.
1. Faltam ≤ 24h para o limite sem postagem → LEMBRETE_SELLER.
2. Projete a chegada: postagem + trânsito mediano (provável) e + p75 (pessimista).
3. Score: postagem atrasada +35 | UF ≥ 12% de atraso +20 | p75 após o prazo +25 |
   mediana após o prazo +30 | seller com > 20% de postagens atrasadas +10.
4. ≥ 70 → ESCALAR_OPERACOES. AVISAR_CLIENTE só se a projeção MEDIANA passar do prazo.
NÃO FAÇA: avisar o cliente só por risco alto; trocar transportadora; inventar rastreio.
SAÍDA: JSON (score, nível, fatores, projeções, ação, mensagem, próximo checkpoint).
```
**d) Resultado esperado:** ação explicada por fatores e mensagem pronta quando houver contato.

**Exemplo com pedido histórico e decisões simuladas.** Pedido MG → MA, postado 4 dias após o limite; prazo 27/03.

| Campo | Saída ilustrativa esperada |
|---|---|
| Score e ação | **80 (ALTO)** · ESCALAR_OPERACOES no dia da postagem, 19 dias antes do prazo |
| Fatores | Postagem atrasada (+35); MA com 19,7% de atraso (+20); projeção pessimista 29/03 > prazo (+25) |
| D-3 (24/03) | Se a projeção mediana validada exceder o prazo, **poderia** recomendar comunicação com estimativa autorizada; 03/04 é data **ilustrativa**, não compromisso comprovado |
| Desfecho real | Entregue em **06/04**, 10 dias de atraso. Não houve aviso por agente documentado; a antecedência de aviso é hipotética. |

*Um segundo caso histórico (SP → BA) ilustra uma decisão proposta para reduzir falsos alertas ao cliente: o pedido chegou no prazo, e o desenho do agente prevê alerta a operações sem comunicação ao cliente quando a projeção mediana cabe no prazo. Não se trata de falso positivo medido em teste executado.*

## 10.3 WinBack
**a) Objetivo:** decidir se e como contatar o cliente de 1ª compra entre D+7 e D+90.
**b) Contexto:** primeira entrega, segunda compra, nota/atraso, problema e resolução confirmada; opt-in/opt-out, grupo, contatos, catálogo elegível e incentivo autorizado.
**c) Instrução principal (resumo):**
```text
Você é o WinBack. Proponha contato para quem ainda não fez a segunda compra.
O processo verifica D+7–D+90 da entrega, consentimento/opt-out, grupo persistente,
intervalo ≥15 dias e máximo de 2 contatos antes de redigir e antes de enviar.
CONTROLE, segunda compra ou bloqueio → NAO_CONTATAR.
Problema aberto/experiência ruim sem resolução confirmada → PAUSAR.
Resolução confirmada permite reavaliar; não autoriza cupom ou contato automático.
TRATAMENTO elegível + catálogo disponível → MENSAGEM_SEM_INCENTIVO.
Segundo contato só de D+45 em diante; incentivo exige política e orçamento.
Acima de 10% exige aprovação específica; sem ela, mensagem sem incentivo.
Contexto essencial ausente → NAO_CONTATAR e revisão humana.
SAÍDA: JSON (elegível nesta execução, ação, motivo, categorias, incentivo,
rascunho até 300 caracteres, próximo passo, revisão). Não contatar/pausar:
elegivel=false, mensagem=null, incentivo=0, categorias=[].
```
**d) Resultado esperado:** decisão auditável, mensagem pronta e grupo controle de 10%.

**Exemplo histórico com contexto operacional simulado.** Cliente do RS, 1ª compra em cama/mesa/banho (R$ 112,44), nota 5, no prazo, D+7.

| Campo | Saída ilustrativa esperada |
|---|---|
| Ação | MENSAGEM_SEM_INCENTIVO, para tratamento elegível com catálogo fornecido |
| Categorias | cama_mesa_banho (46% das 2ªs compras desse perfil) e moveis_decoracao (9%) |
| Mensagem | "Que bom que seu pedido chegou! Você pode conhecer opções de cama, mesa e banho e de decoração relacionadas à sua primeira compra." |
| Contraste | Outro cliente histórico, com ticket aberto simulado, recebe **PAUSAR**: resolução confirmada permite reavaliar os bloqueios, sem cupom automático |

**Validação dos prompts.** Critérios de aceitação, matriz de casos de limite (22 cenários) e roteiro de demonstração estão em `fase2/prompts/VALIDACAO_LUCAS.md`. Os exemplos esperados não substituem execução registrada nem ensaio do vídeo.

<!-- pagebreak -->

# 11. Riscos, Governança e Human in the Loop (atualizado na Fase 2)

## 11.1 Riscos e controles (Fase 1, mantidos e associados aos agentes priorizados)

| Risco | Exemplo | Controle |
|---|---|---|
| Alucinação / decisão sem evidência | Agente afirma fato inexistente | Grounding em dados, fonte explícita, validação humana para alto impacto |
| Falso positivo logístico | Cliente avisado de atraso que não ocorre | Aviso só quando a projeção mediana estoura o prazo; meta de falso positivo ≤ 20% |
| Classificação errada *(novo)* | SentimentDesk erra o motivo | Confiança mínima de 0,8; auditoria semanal; fila humana |
| Impacto financeiro | Incentivo excessivo | Teto de 10%; acima disso, aprovação do Gestor de CRM |
| Penalização indevida | Seller punido injustamente | Agentes não penalizam; revisão humana e direito de resposta |
| Privacidade / LGPD | Contato sem consentimento | Opt-in, intervalo de 15 dias, máximo de 2 contatos |
| Viés histórico | Padrões de 2016–2018 | Evidências recalculadas com dados atuais antes do piloto |
| Automação excessiva | Ação irreversível sem supervisão | Matriz de autonomia (11.2) e lista fechada de ações por agente |
| Gargalo de aprovação *(novo)* | IA rápida esbarra em fila humana lenta | SLA rígido para revisão humana (ver 11.5) |

## 11.2 Matriz de autonomia (Fase 1, mantida)

| Tipo de ação | Autonomia recomendada |
|---|---|
| Classificar, resumir, detectar tema | Automática com monitoramento |
| Gerar rascunho, alerta ou recomendação | Automática; humano revisa quando sensível |
| Comunicação padrão de baixo risco | Automática após validação de regras e confiança |
| Desconto, ressarcimento, alteração de preço | Automática apenas dentro de limites pré-aprovados |
| Suspensão de seller ou decisão reputacional | Aprovação humana obrigatória |
| Decisão estratégica executiva | Agente recomenda; liderança decide |

## 11.3 Política econômica dos incentivos (novo na revisão executiva)

O limite de 10% para incentivos do WinBack é uma **regra proposta**, não um teto economicamente validado. Mesmo incentivos de até 10% exigem elegibilidade, consentimento, disponibilidade orçamentária, margem incremental não negativa e política comercial aprovada. Acima de 10%, exige-se adicionalmente autorização do gestor; a aprovação **não dispensa** a análise econômica. Custos de mídia, desconto, atendimento e eventuais devoluções devem entrar na avaliação de valor líquido.

## 11.4 Quem decide o quê nos agentes priorizados (novo na Fase 2)

| Decisão | Agente | Analista | Gestor |
|---|---|---|---|
| Classificar avaliação / calcular risco | **Executa** | Audita amostra | Informado |
| Lembrete ao seller; aviso com nova data | **Executa** | Informado | Aprova o template |
| Resposta padrão a avaliação | **Executa** | Revisa amostra | Aprova os templates |
| Resposta a caso crítico e compensação | Rascunha | **Decide** | Alçada acima do limite |
| Tratativa com a transportadora | Recomenda | **Decide** | Informado |
| Incentivo ≤ 10% / > 10% | **Executa** / Recomenda | Informado | Define o teto / **Decide** |

## 11.5 Feedback Loop e Gestão de Filas Humanas (novo na Fase 2)

A governança protege o negócio, mas não deve engessar a operação. Para que a IA evolua continuamente e não esbarre em gargalos processuais, dois mecanismos operacionais foram estabelecidos:

*   **Feedback Loop de Aprendizado:** O analista não é apenas um "aprovador". As revisões e correções feitas pelos humanos (ex: reclassificação de um motivo no *SentimentDesk* ou ajuste de rota logística no *LogiPredict*) retroalimentam o agente. No *SentimentDesk*, esses acertos alimentam um banco de *few-shot examples* (exemplos de calibração); no *LogiPredict*, cujo score é uma heurística (Seção 9.5), servem para recalibrar pesos e limiar. Assim o agente corrige seu viés e não repete o mesmo erro nas iterações futuras.
*   **SLA de Revisão Humana:** Para que a velocidade da IA não seja anulada por uma fila de pendências no *Human in the Loop*, as etapas marcadas como "Decide" (respostas a casos críticos, compensações, tratativas logísticas) possuem um **SLA máximo de resposta humana de 4 horas úteis** (meta do piloto: 95% das decisões dentro do prazo, Seção 13.2). Casos não atendidos nesse prazo acionam alertas de escalonamento gerencial.

# 12. Roadmap de Implantação e Validação (atualizado na Fase 2)

A versão 1.0 trazia duas ordens diferentes de implantação (Seções 5.3 e 11). A versão 2.0 adota um **roadmap único**, coerente com a priorização da Seção 5.3:

| Onda | Agentes | Período | Critério para avançar |
|---|---|---|---|
| **Wave 1 · piloto** | LogiPredict + SentimentDesk | Meses 1–3 | Falso positivo ≤ 20%; classificação ≥ 85%; 90% de respostas em < 24h |
| **Wave 2** | WinBack | Meses 4–6 | Opt-in e grupo controle prontos; sinal de pausa em produção |
| **Wave 3** | SellerCare e SmartFreight | Meses 7–9 | Uplift comprovado nas Waves 1 e 2 |
| **Orquestração** | Maestro | Fase 4 do projeto | Três especialistas estáveis em produção |

**Próximos passos (Fase 3, protótipo):** prototipar SentimentDesk e LogiPredict em ferramenta low-code com os casos reais deste relatório; medir a acurácia do SentimentDesk contra 30 a 50 avaliações rotuladas pelo grupo; calibrar os pesos do score do LogiPredict.

<!-- pagebreak -->

# 13. Indicadores de Sucesso e Business Case (atualizado na Fase 2)

## 13.1 Baselines do projeto (Fase 1, revisados)

| Categoria | Indicador | Baseline |
|---|---|---|
| Financeiro | Receita total · ticket médio · LTV estimado | R$ 16.008.872,12 · R$ 161,00 · R$ 165,20 |
| Clientes | Taxa de recompra · churn (> 6 meses) · top 10% da base | 3,00% · 58,61% · 38,25% da receita |
| Clientes *(novo)* | Conversão em 2ª compra de D+7 a D+90 após a entrega (janela do WinBack) | 0,90% |
| Logística | Tempo médio total · trânsito · processamento | **12,56 dias** · 9,33 dias · 3,23 dias *(revisados)* |
| Logística | Taxa de atrasos · postagem após o limite *(novo)* | 8,11% · 9,0% |
| Logística | Frete / valor do pedido | 21,34% |
| Satisfação | Notas 1 e 2 | 14,7% |
| Satisfação | Tempo de resposta da Olist a avaliações | **A medir no piloto** *(substitui o "3,15 dias" da v1.0)* |
| Sellers | Concentração · nota crítica · cluster problemático | Gini 0,792 · 342 com nota < 3,0 · 527 sellers |

## 13.2 Metas do piloto (novo na Fase 2)

| Agente | Indicador | Baseline | Meta (90 dias) | Como medir |
|---|---|---|---|---|
| LogiPredict | Atraso nas rotas do piloto | 14,3% no Nordeste (10,8% a 23,9% por UF) | −1 p.p. (13,3%) | Rotas controle |
| LogiPredict | Postagens após o limite | 9,0% | ≤ 6% | Limite × postagem |
| LogiPredict | Falso positivo do aviso | n/a | ≤ 20% | Avisos × entregas no prazo |
| SentimentDesk | Tempo até a 1ª resposta | A medir | 90% em < 24h | Log do agente |
| SentimentDesk | Classificação correta | n/a | ≥ 85% | Auditoria semanal (50 casos) |
| Ambos (humano no loop) | Decisões humanas dentro do SLA (Seção 11.5) | A medir | 95% em até 4h úteis | Log da fila de revisão |

**Wave 2 (referência, fora do piloto de 90 dias):**

| Agente | Indicador | Baseline | Meta | Como medir |
|---|---|---|---|---|
| WinBack | Conversão em 2ª compra de D+7 a D+90 após a entrega | 0,90% | 1,40% (+0,5 p.p.) | Uplift contra controle |
| WinBack | Opt-out por contato | n/a | < 1% | CRM |

## 13.2.1 Protocolo mínimo de validação do piloto (novo na revisão executiva)

**Antes de iniciar:** confirmar fontes operacionais atuais, medir volume elegível e baseline, pactuar alçadas e templates, estabelecer tratamento/controle comparáveis, definir responsável por cada intervenção e registrar critérios de interrupção. **Durante os 90 dias:** acompanhar semanalmente qualidade dos dados, precisão e cobertura dos alertas, recall de casos críticos, qualidade das respostas, volume de intervenções humanas, custos e reclamações. **Ao final:** estimar efeito incremental nas métricas de negócio com intervalo de incerteza e registrar resultados negativos ou inconclusivos. Uma meta de qualidade técnica cumprida **não substitui** evidência de impacto de negócio.

**Portões de decisão:** avançar apenas se (1) controles de segurança e privacidade funcionarem, (2) métricas de qualidade atingirem patamar acordado, (3) houver sinal mensurável de benefício incremental e (4) custo operacional e capacidade de escala forem aceitáveis. Sem esses quatro elementos, recalibrar ou encerrar a hipótese; não extrapolar ganhos da amostra histórica para produção.

## 13.3 Business case em três cenários (novo na Fase 2)
Janela: set/2017 a ago/2018, **na escala do dataset público**. Os valores **ilustram cenários**, não previsão validada de resultado real. A extrapolação linear ao volume atual da Olist não é automaticamente válida: depende do mix de pedidos, sellers, rotas, canais, sazonalidade, elegibilidade e resposta à intervenção. O piloto deverá recalibrar os parâmetros.

| Agente | Lógica do cálculo | Conservador | Base | Otimista |
|---|---|---|---|---|
| LogiPredict | Postagens atrasadas × diferença de atraso que o agente elimina; atrasos evitados × diferença de notas 1–2 | 336 atrasos · 151 notas 1–2 a menos | **672 atrasos · 302 notas 1–2 a menos** | 1.008 atrasos · 453 notas 1–2 a menos |
| SentimentDesk | Avaliações 1–2 tratadas com o agente × minutos poupados × custo do analista | 878 h · R$ 39,5 mil | **1.230 h · R$ 55,3 mil** | 1.581 h · R$ 71,1 mil |
| WinBack | Novos clientes × aumento da conversão em 2ª compra × ticket da 2ª compra | 179 compras · R$ 26,6 mil | **358 compras · R$ 53,2 mil** | 717 compras · R$ 106,4 mil |

O efeito indireto (cliente com entrega no prazo recompra mais) **não foi somado**, para manter o cálculo conservador. A conta completa, com cada número de entrada, está na Seção 13.4.

> **Leitura executiva.** O maior retorno está na combinação: menos atrasos geram menos avaliações negativas, o que reduz a fila do CX e preserva a chance de segunda compra. Os três agentes foram desenhados para atuar sobre elos da mesma corrente; o efeito combinado e sua causalidade ainda dependem de validação.

## 13.4 Memória de cálculo do business case (novo na Fase 2)
Todas as contas abaixo podem ser refeitas com calculadora a partir dos números impressos; os resultados são arredondados para o inteiro mais próximo apenas no final. Os dados de entrada vêm do notebook `08_fase2_evidencias_business_case.ipynb` e estão listados, com definição, em `fase2/NUMEROS_OFICIAIS.md`.

**Janela de cálculo:** pedidos e avaliações de **set/2017 a ago/2018** (12 meses mais recentes e completos do dataset).

> **Como ler esta seção.** Para cada agente há (1) a lógica **em linguagem simples**, (2) uma tabela com cada número usado: o que é **dado** saiu do dataset; o que é **premissa** é uma estimativa do grupo, a ser confirmada no piloto, e (3) a conta de cada cenário. "p.p." significa **pontos percentuais**: de 7,5% para 27,6% são 20,1 p.p. de diferença.

### LogiPredict: atrasos e avaliações negativas evitados

**Em linguagem simples.** Nos últimos 12 meses, **6.689 pedidos** foram postados pelo seller depois do prazo de postagem. Nesse grupo, **cerca de 28 em cada 100** chegaram atrasados ao cliente; quando o seller posta no prazo, são **7 a 8 em cada 100**. Postar no prazo, portanto, evita **cerca de 20 atrasos a cada 100 pedidos**. O LogiPredict lembra o seller antes do limite e aciona operações. Se ele eliminar **metade** dessa diferença (cenário base), são **10 atrasos a menos a cada 100 pedidos** desse grupo, ou **672 no ano**. E como um pedido atrasado recebe nota 1–2 muito mais vezes (54 em cada 100, contra 9 em cada 100 no prazo), **cada 100 atrasos evitados poupam cerca de 45 avaliações negativas**: **302 no ano**.

| Entrada | Valor | Origem |
|---|---|---|
| A. Pedidos entregues com postagem após o limite (12 meses) | **6.689** | `orders.order_delivered_carrier_date` > `order_items.shipping_limit_date` |
| B. Taxa de atraso quando a postagem foi após o limite (12 meses) | **27,6%** | `orders`: entrega > prazo estimado |
| C. Taxa de atraso quando a postagem foi no prazo (12 meses) | **7,5%** | idem |
| D. Diferença que o agente pode eliminar (B − C) | **20,1 p.p.** | cálculo |
| E. % de notas 1–2 em pedido atrasado | **54,1%** | `orders` + `order_reviews` (dataset inteiro) |
| F. % de notas 1–2 em pedido no prazo | **9,2%** | idem |
| G. Notas 1–2 a menos por atraso evitado (E − F) | **44,9 p.p.** | cálculo |
| H. % da diferença D eliminada pelo agente (premissa) | **25% / 50% / 75%** | premissa do grupo (cenários) |

**Fórmulas:** atrasos evitados = A × D × H · notas 1–2 evitadas = atrasos evitados × G

| Cenário | Atrasos evitados | Notas 1–2 evitadas |
|---|---|---|
| Conservador (H = 25%) | 6.689 × 20,1% × 25% = 336,1 → **336** | 336,1 × 44,9% = 150,9 → **151** |
| Base (H = 50%) | 6.689 × 20,1% × 50% = 672,2 → **672** | 672,2 × 44,9% = 301,8 → **302** |
| Otimista (H = 75%) | 6.689 × 20,1% × 75% = 1.008,4 → **1.008** | 1.008,4 × 44,9% = 452,8 → **453** |

*Por que 27,6% e não 24,4%?* O 24,4% (Seção 4.2) é a média de 2016–2018. Para o business case foi usada a janela dos últimos 12 meses, mais próxima da operação recente, na qual a postagem atrasada pesou mais.

### SentimentDesk: horas de triagem poupadas

**Em linguagem simples.** Hoje, cada avaliação negativa exige que alguém leia, entenda o problema, escreva uma resposta e encaminhe o caso: estimamos **12 minutos**. Com o agente, a pessoa só confere o que já chega pronto (motivo, resumo e resposta sugerida): **3 minutos**. São **9 minutos poupados por avaliação**. No ano foram **11.711 avaliações** nota 1–2. Supondo que **70%** passem pelo agente (o restante continua manual: casos críticos e de baixa confiança), são cerca de **8.200 avaliações × 9 minutos ≈ 1.230 horas**, o equivalente a **7 a 8 meses de trabalho de um analista em tempo integral**. A R$ 45 por hora, **R$ 55 mil por ano**.

| Entrada | Valor | Origem |
|---|---|---|
| A. Avaliações nota 1–2 criadas em 12 meses | **11.711** | `order_reviews` (`review_creation_date` na janela) |
| B. % das avaliações tratadas com apoio do agente (premissa) | **50% / 70% / 90%** | premissa do grupo (cenários) |
| C. Tempo manual por avaliação (ler, classificar, responder, encaminhar) | **12 min** | premissa do grupo |
| D. Tempo com o agente (revisar o que o agente preparou) | **3 min** | premissa do grupo |
| E. Minutos poupados por avaliação (C − D) | **9 min** | cálculo |
| F. Custo da hora do analista de CX (com encargos) | **R$ 45,00** | premissa do grupo |

**Fórmulas:** horas poupadas = A × B × E ÷ 60 · economia = horas poupadas × F

| Cenário | Horas poupadas | Economia anual |
|---|---|---|
| Conservador (B = 50%) | 11.711 × 50% × 9 ÷ 60 = 878,3 → **878 h** | 878,3 × R$ 45 = **R$ 39.525** |
| Base (B = 70%) | 11.711 × 70% × 9 ÷ 60 = 1.229,7 → **1.230 h** | 1.229,7 × R$ 45 = **R$ 55.334** |
| Otimista (B = 90%) | 11.711 × 90% × 9 ÷ 60 = 1.581,0 → **1.581 h** | 1.581,0 × R$ 45 = **R$ 71.144** |

### WinBack: segundas compras e receita adicional

**Em linguagem simples.** Hoje, de cada **1.000 clientes novos**, cerca de **9 voltam** a comprar entre 7 e 90 dias depois de receber o 1º pedido (0,90%), que é a janela em que o WinBack atua. O cenário base supõe que o contato do WinBack, no momento certo e com a categoria certa, faça voltar **mais 5 em cada 1.000** (de 9 para 14). Com **71.693 clientes novos** no ano, isso dá **358 segundas compras a mais**. Como a 2ª compra vale em média **R$ 148,35**, são **R$ 53 mil por ano**.

| Entrada | Valor | Origem |
|---|---|---|
| A. Clientes com 1ª compra entregue em 12 meses | **71.693** | `orders` + `customers.customer_unique_id` |
| B. Conversão atual em 2ª compra na janela do agente | **0,90%** | `orders`: 2ª compra de D+7 a D+90 após a entrega da 1ª, clientes com janela completa |
| C. Aumento da conversão pelo agente (premissa, pontos percentuais) | **+0,25 / +0,5 / +1,0 p.p.** | premissa do grupo (cenários); o base leva 0,90% a 1,40% |
| D. Valor médio da 2ª compra | **R$ 148,35** | `order_payments` das 2ªs compras |

**Fórmulas:** segundas compras adicionais = A × C · receita adicional = segundas compras adicionais × D

| Cenário | Segundas compras adicionais | Receita adicional |
|---|---|---|
| Conservador (C = +0,25 p.p.) | 71.693 × 0,25% = 179,2 → **179** | 179,2 × R$ 148,35 = **R$ 26.589** |
| Base (C = +0,5 p.p.) | 71.693 × 0,5% = 358,5 → **358** | 358,5 × R$ 148,35 = **R$ 53.178** |
| Otimista (C = +1,0 p.p.) | 71.693 × 1,0% = 716,9 → **717** | 716,9 × R$ 148,35 = **R$ 106.357** |

### Como ler esses números
- **São valores na escala do dataset público**, amostra histórica da operação da Olist. Não é seguro escalar linearmente para a operação atual sem validar representatividade, elegibilidade, composição da base e efetividade causal das intervenções.
- **As premissas (H, B, C, D, F e o aumento de conversão) são do grupo** e devem ser substituídas por valores medidos no piloto, que tem grupo controle justamente para isso.
- **Custos de implantação e operação não estão incluídos.** Devem ser estimados na Fase 3: integração, plataforma/modelos, mensageria, infraestrutura, supervisão, manutenção e incentivos. As horas poupadas representam **capacidade potencial liberada**, não necessariamente economia de caixa; R$ 53 mil do WinBack é **receita bruta incremental estimada**, não margem nem lucro. Portanto, este documento **não calcula ROI nem retorno financeiro líquido**.

# 14. Recomendação Executiva (atualizado na Fase 2)

Na Fase 1, os dados mostraram um conjunto conectado de fricções. Na Fase 2, esse diagnóstico virou operação. São **três agentes especializados**, cada um com **um papel**, **gatilhos claros**, **lista fechada de ações** e **pessoas decidindo o que tem impacto financeiro ou reputacional**. A visão de seis agentes e orquestrador da Fase 1 continua como destino; o caminho até ela agora tem ordem, critério e metas.

**Recomendamos autorizar a preparação e execução controlada da Wave 1 (LogiPredict + SentimentDesk) por 90 dias**, com seleção final das rotas do Nordeste condicionada ao volume elegível e à viabilidade operacional, grupo controle comparável, governança de dados e aprovação de orçamento. A continuidade depende das metas técnicas da Seção 13.2 **e** de evidência de benefício incremental, segurança e viabilidade econômica (Seção 13.2.1). O WinBack pertence à expansão futura, não ao escopo do piloto.

> **Mensagem para a diretoria.** A IA Agêntica deve ser tratada como uma capacidade de negócio, não como uma coleção de chatbots. Não propomos mais agentes; propomos agentes melhores, começando pela origem do problema, e cada passo seguinte só avança com resultado medido.

# 15. Fontes do Projeto

| Artefato | Conteúdo |
|---|---|
| Enunciados oficiais FIAP | Tech Challenge Agentic AI, Fases 1 e 2 |
| `fase1/Relatorio_Executivo_Fase1_Olist_FINAL.pdf` | Versão 1.0 deste relatório (preservada) |
| Notebooks 01–07 | Diagnóstico da Fase 1 |
| `notebooks/08_fase2_evidencias_business_case.ipynb` | Cadeia de evidência, priorização, business case, casos reais |
| `fase2/NUMEROS_OFICIAIS.md` | Fonte única dos números da Fase 2 (valor, definição, tabela de origem) |
| `fase2/prompts/PROMPTS_V2.md` | Prompts completos e 10 exemplos com casos reais |
| `fase2/fluxos/` | Fluxos e o script que os gera |
| Dataset | Brazilian E-Commerce Public Dataset by Olist (Kaggle), 2016–2018 |

# Apêndice A: Rastreabilidade dos Entregáveis

| Requisito | Fase | Onde está |
|---|---|---|
| Principais problemas e oportunidades | 1 | Seções 1, 2 e 4 |
| Análises do dataset | 1 | Seções 3, 4 e 5 |
| Mapa de agentes | 1 | Seção 6 |
| Arquitetura conceitual | 1 | Seção 7 |
| Riscos | 1 e 2 | Seção 11 |
| Evolução do relatório da Fase 1 | 2 | Histórico do Documento + marcas "atualizado/novo" em cada seção |
| ≥ 3 agentes com a) a f) | 2 | Seção 8 (8.1 a 8.3) |
| Jornadas: gatilhos, entradas, decisões, ações, interação humana e saída | 2 | Seção 9 |
| Prompts: objetivo, contexto, instrução e resultado esperado | 1 e 2 | Seção 10 + `fase2/prompts/PROMPTS_V2.md` |
| Vídeo executivo (link no relatório) | 1 e 2 | Seção 1 e capa |
| Problema, benefício, impacto, usuários e riscos | 1 e 2 | Seções 8, 11 e 13 |


# Apêndice B: Limitações e próximos passos de validação (novo na Fase 2)

1. **Rastreabilidade numérica:** todos os números da Fase 2 vêm de `fase2/NUMEROS_OFICIAIS.md` (notebook 08). O notebook foi reexecutado de forma independente por outro integrante do grupo, com os mesmos resultados.
2. **Volume e seleção do piloto:** quantificar pedidos, sellers e rotas elegíveis no Nordeste, estimar o tamanho de amostra e validar o desenho de controle.
3. **Operação real:** validar com as áreas de CX, Logística e CRM os processos descritos como presumidos, a disponibilidade de APIs e canais, o consentimento e as alçadas.
4. **Testes de prompts:** distinguir saídas ilustrativas de saídas executadas e auditadas, registrando modelo, data e saída bruta de cada execução.
5. **Custos e margem:** estimar o custo total do piloto e os custos variáveis antes de afirmar retorno financeiro ou ROI (Fase 3).

*Este apêndice explicita os limites da evidência atual e orienta a Fase 3; não constitui requisito adicional do enunciado.*
