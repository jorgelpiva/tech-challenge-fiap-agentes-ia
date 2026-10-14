<!--
FONTE ÚNICA do Relatório Executivo da Fase 2.
Gerar .docx/.pdf:  python fase2/gerar_relatorio.py
Números: fase2/dados/numeros_fase2.json (notebook 08). Não digitar número que não esteja lá.
A capa é montada pelo script (equipe, links); o link do vídeo fica em fase2/config_relatorio.json.
-->

# 1. Sumário Executivo

Na Fase 1, mostramos **onde** a Olist perde valor. A Fase 2 responde à pergunta da diretoria: **como os agentes de IA vão interagir com usuários, dados e processos para gerar valor real?**

A resposta parte de uma constatação dos dados. Os problemas de experiência, reputação e recorrência **nascem no mesmo lugar: a jornada do pedido**. Quando o pedido atrasa, **54%** dos clientes dão nota 1 ou 2, contra **9%** quando chega no prazo. **Um quarto** dos atrasos (27%) começa antes da transportadora, com o seller postando depois do limite. E quem teve a primeira compra atrasada volta menos (1,56% contra 2,13%).

Por isso, **concentramos a iniciativa em três agentes especializados** que atuam em sequência na jornada do pedido, em vez dos seis propostos na Fase 1:

| Agente | Papel único na operação | Gatilho | Humano decide quando… | KPI principal |
|---|---|---|---|---|
| **LogiPredict** · Guardião do Prazo | Detectar o risco de atraso e agir antes do vencimento | Limite de postagem, postagem, D-3 do prazo | Risco alto exige tratativa com a transportadora | Taxa de atraso (8,11%) |
| **SentimentDesk** · Triagem de Avaliações Negativas | Classificar o motivo, responder e rotear cada avaliação 1–3 | Avaliação publicada | O caso é crítico, a confiança é baixa ou há compensação | Tempo até a 1ª resposta |
| **WinBack** · Segunda Compra | Converter a 1ª compra em 2ª dentro da janela de 90 dias | D+7 após a 1ª entrega | O incentivo passa do teto de 10% | Conversão em 2ª compra (1,13% em 90 dias) |

**Valor esperado no cenário base (12 meses, na escala do dataset):** 670 atrasos evitados e cerca de 300 avaliações 1–2 a menos (LogiPredict); 1.229 horas de triagem poupadas, ou R$ 55 mil (SentimentDesk); 358 segundas compras adicionais, ou R$ 53 mil de receita (WinBack). As premissas são conservadoras e estão explícitas na Seção 9.

**Recomendação:** aprovar um **piloto de 90 dias da Wave 1 (LogiPredict + SentimentDesk)**. Os dois agentes usam dados que a Olist já possui, decidem dentro de casa e têm efeito mensurável em semanas. O WinBack entra na Wave 2, quando opt-in e grupo controle estiverem prontos.

> **Links:** vídeo executivo da Fase 2: {{LINK_VIDEO}} · repositório: {{LINK_GITHUB}} · vídeo da Fase 1: {{LINK_VIDEO_FASE1}}

<!-- pagebreak -->

# 2. Evolução do Projeto: da Fase 1 para a Fase 2

## 2.1 O que mantivemos
A base analítica da Fase 1 continua válida: 99.441 pedidos, sete frentes de análise (EDA, RFM, clusterização, correlações, testes de hipótese, análise geoespacial e NLP) e as quatro fricções do diagnóstico (retenção, logística, experiência e sellers). Os nomes dos agentes também foram mantidos, para preservar a rastreabilidade.

## 2.2 O que aprendemos com a avaliação da Fase 1 e como respondemos

| Ponto da avaliação | O que fizemos na Fase 2 | Onde ver |
|---|---|---|
| Detalhar o racional de onde partiram os achados | Cada achado agora segue uma **cadeia de evidência**: pergunta → tabela/coluna → método → resultado → decisão de desenho | Seção 3 |
| Ações dos agentes muito amplas, sem especialização | Cada agente tem **um objetivo**, **gatilhos definidos**, **lista fechada de ações** e uma seção explícita do que **não faz** | Seções 5 e 6 |
| Muitos objetivos; priorizar o mais próximo do negócio | **Matriz de priorização** com critérios ponderados: de 6 agentes para **3 detalhados**, todos na jornada do pedido | Seção 4 |
| Falha de revisão | **Fonte única de números** gerada por notebook, checklist de QA e apêndice de rastreabilidade | Apêndices A e B |

## 2.3 Correções de rigor em relação à Fase 1
- **Tempo médio de entrega:** padronizado em **12,56 dias** (compra → entrega, dias corridos fracionados, pedidos entregues). A Fase 1 registrava 12,47 e 12,56 em pontos diferentes.
- **"Tempo de resposta a reviews (3,15 dias)":** a coluna `review_answer_timestamp` registra quando o **cliente respondeu a pesquisa**, não quando a Olist respondeu o cliente. Retiramos esse número como baseline do SentimentDesk; o tempo real de resposta será **medido no piloto**.
- **Público do WinBack:** na Fase 1, o alvo eram 38.655 clientes inativos há mais de 439 dias. Os dados mostram que **54% das segundas compras acontecem em até 90 dias** e 75% em até 180. Reativar base antiga tem baixa probabilidade de retorno, então o agente foi **reposicionado para a janela pós-1ª compra**.
- **Roadmap:** a Fase 1 trazia ordens diferentes para as ondas em duas seções. Agora há um roadmap único (Seção 11).

## 2.4 O que é novo nesta fase
Casos de uso com os seis elementos pedidos (a–f), **fluxos operacionais** com gatilhos, decisões e humano no loop, uma **jornada multiagente** com um pedido real, **prompts v2 testados com casos reais** do dataset e **business case em três cenários**.

<!-- pagebreak -->

# 3. Da Evidência à Decisão: o racional dos achados

Todos os números desta seção vêm do notebook `08_fase2_evidencias_business_case.ipynb`, executado sobre as tabelas públicas da Olist. A tabela mostra o caminho de cada achado até a decisão de desenho do agente.

| # | Pergunta de negócio | Dado utilizado | Método | Resultado | Decisão de desenho |
|---|---|---|---|---|---|
| E1 | O atraso pesa na satisfação? | `orders` (entrega × prazo) + `order_reviews` (nota) | Comparação de proporções entre pedidos atrasados e no prazo | **54,1%** de notas 1–2 com atraso vs **9,2%** no prazo; nota média 2,57 vs 4,29 | Atraso é o primeiro problema a atacar (LogiPredict) |
| E2 | Onde o atraso nasce? | `order_items.shipping_limit_date` × `orders.order_delivered_carrier_date` | Taxa de atraso segmentada pela pontualidade da postagem | Postagem após o limite em **9,0%** dos pedidos: atraso de **24,4%** vs **6,5%**; **27%** de todos os atrasos | Primeiro checkpoint do LogiPredict é o **limite de postagem** |
| E3 | Onde o atraso é mais provável? | `orders` + `customers` (UF destino) | Taxa de atraso por UF | AL 23,9%, MA 19,7%, PI 16,0%, CE 15,3% (média 8,11%) | UF destino entra no score de risco; piloto começa no Nordeste |
| E4 | Do que reclamam os insatisfeitos? | `order_reviews` (título + comentário, notas 1–2) | Classificação por regras em 10.994 avaliações com texto | **47%** entrega (39,5% "não recebido"), **18%** pedido incorreto, **12%** produto, **5%** atendimento | Taxonomia fixa do SentimentDesk; o motivo define o roteamento |
| E5 | Quando o cliente volta? | `orders` + `customers.customer_unique_id` | Intervalo entre 1ª e 2ª compra (excluindo mesmo dia) | Mediana de **76 dias**; **54%** em até 90 dias | WinBack atua de D+7 a D+90, não na base antiga |
| E6 | A experiência afeta a recompra? | `orders` + `order_reviews` | Recompra por pontualidade da 1ª compra | 1,56% (atrasou) vs 2,13% (no prazo) | WinBack **pausa** a oferta quando a 1ª experiência foi ruim |

![Atraso e satisfação (E1) e origem do atraso na postagem do seller (E2).](img/f2_evidencia_atraso.png)

![Motivo principal das avaliações 1–2 com comentário (E4). Laranja: motivos ligados à entrega.](img/f2_motivos_reviews.png)

![Distribuição acumulada do tempo até a 2ª compra (E5).](img/f2_janela_2a_compra.png)

> **Nota de interpretação.** São associações observadas em dados históricos (2016–2018), não prova de causalidade. Por isso, cada agente é proposto com **grupo controle no piloto**, para medir o efeito real antes de escalar.

<!-- pagebreak -->

# 4. Priorização: por que três agentes

Avaliamos os seis agentes da Fase 1 em cinco critérios, com pesos definidos pelo grupo. **Proximidade do core** mede se o agente atua diretamente na jornada compra → entrega → avaliação → recompra, que é onde está a receita do marketplace.

| Agente | Impacto (30%) | Proximidade do core (25%) | Evidência nos dados (20%) | Viabilidade (15%) | Risco, inverso (10%) | Score | Decisão |
|---|---|---|---|---|---|---|---|
| **LogiPredict** | 5 | 5 | 5 | 4 | 4 | **4,75** | Detalhar |
| **SentimentDesk** | 4 | 5 | 5 | 5 | 4 | **4,60** | Detalhar |
| **WinBack** | 5 | 4 | 4 | 4 | 3 | **4,20** | Detalhar |
| SellerCare | 4 | 3 | 4 | 3 | 2 | 3,40 | Absorvido / Wave 3 |
| SmartFreight | 3 | 3 | 3 | 2 | 2 | 2,75 | Backlog |
| Maestro | 3 | 2 | 2 | 2 | 3 | 2,40 | Fase 4 (orquestração) |

![Matriz impacto × viabilidade dos agentes propostos na Fase 1.](img/f2_priorizacao.png)

**O que acontece com os demais agentes:**
- **SellerCare:** as duas ações de maior evidência foram **absorvidas**. O lembrete de postagem ficou no LogiPredict, e o ticket ao seller por pedido incorreto, no SentimentDesk. O coaching estruturado de sellers fica para a Wave 3, alimentado pelos dados desses dois agentes.
- **SmartFreight:** depende de dados de concorrência e de regras de margem que o dataset não contém. Fica no backlog.
- **Maestro:** a orquestração só faz sentido quando houver especialistas em produção. Será desenhada na **Fase 4**, conforme o roadmap do curso. Nesta fase, a interação entre os três agentes acontece por **sinais simples** (Seção 7.4).

<!-- pagebreak -->

# 5. Como os Agentes Operam na Olist

## 5.1 Visão operacional
Os três agentes atuam em momentos diferentes da mesma jornada e conversam por sinais. Nenhum deles executa decisões financeiras ou reputacionais sozinho.

| | LogiPredict | SentimentDesk | WinBack |
|---|---|---|---|
| **Momento da jornada** | Aprovação → entrega | Após a avaliação | D+7 a D+90 após a 1ª entrega |
| **Frequência** | Varredura a cada 6h + eventos | Por avaliação (tempo real) | Batch diário |
| **Usuários que recebem** | Analista de Operações, seller, cliente | Analista de CX, seller, cliente | Analista/Gestor de CRM, cliente |
| **Sistemas tocados** | Pedidos, rastreio, mensageria | Avaliações, atendimento (tickets), mensageria | CRM, catálogo, mensageria |
| **Envia sinal para** | SentimentDesk (pedido em risco) | LogiPredict (motivo entrega), WinBack (pausar) | n/a (consome sinais) |
| **Nunca faz sozinho** | Trocar transportadora, compensar cliente | Reembolso, cupom, penalizar seller | Incentivo > 10%, contato sem opt-in |

## 5.2 Padrão visual dos fluxos
Todos os fluxos da Seção 7 usam a mesma legenda: **gatilho** (caixa escura), **ação do agente** (cor do agente), **decisão** (losango amarelo), **humano no loop** (borda laranja) e **saída** (verde). As raias separam o que dispara o fluxo, o que o agente faz, o que exige pessoa e o que é entregue.

<!-- pagebreak -->

# 6. Casos de Uso Detalhados

## 6.1 LogiPredict · Guardião do Prazo de Entrega

**a) Objetivo.** Reduzir pedidos entregues após o prazo prometido, agindo **antes do vencimento** em três checkpoints: limite de postagem, postagem efetiva e D-3 do prazo.

**b) Problema resolvido.** **8,11%** dos pedidos entregues atrasam. Em pedidos atrasados, **54%** das avaliações são nota 1–2. O trânsito responde por **74%** do tempo de entrega, mas **27%** dos atrasos começam com o seller postando depois do limite. Hoje, o atraso só aparece quando o cliente reclama. A consequência é perda de reputação, avaliação negativa e menor recompra.

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
| D-3 do prazo sem entrega | Aviso ao cliente com nova data (template aprovado) |
| Fechamento diário | Painel de risco por rota/UF; sinal "pedido em risco" ao SentimentDesk |

**f) Indicadores impactados.** Taxa de atraso (baseline 8,11%), % de postagens após o limite (9,0%), % de notas 1–2 em pedidos de risco, contatos "onde está meu pedido", taxa de falso positivo dos alertas.

**Faz / não faz.**

| Faz | Não faz |
|---|---|
| Calcula risco, lembra o seller, alerta operações, avisa o cliente com data projetada | Não troca transportadora, não negocia frete, não concede compensação, não avisa o cliente sem projeção de estouro |

**AS-IS → TO-BE** *(processo atual presumido, a validar com a área)*

| Hoje | Com o LogiPredict |
|---|---|
| O atraso é descoberto quando o cliente reclama ou avalia | Risco identificado na postagem; nos pedidos que atrasaram, a postagem ocorreu em mediana **17,5 dias antes do prazo**, tempo suficiente para agir |
| O seller não é lembrado do limite de postagem | Lembrete automático 24h antes do limite |
| Aviso ao cliente inexistente ou genérico | Aviso com nova data, só quando a projeção estoura o prazo |

## 6.2 SentimentDesk · Triagem e Resposta de Avaliações Negativas

**a) Objetivo.** Responder rapidamente toda avaliação nota 1 a 3 e **levar o problema a quem pode resolvê-lo**: transporte, seller ou atendimento.

**b) Problema resolvido.** **14,7%** das avaliações são nota 1 ou 2, cerca de **11,7 mil por ano**. Quase metade (**47%**) fala de entrega e **18%** de pedido incorreto (item faltando ou produto errado). Hoje não há visão estruturada desses motivos. Sem triagem, o caso grave fica na mesma fila do simples e o seller reincidente não é identificado. A consequência é detrator não recuperado e problema recorrente sem dono.

**c) Usuários envolvidos.** Cliente (recebe resposta), Analista de CX (revisa casos críticos e define compensação), seller (recebe ticket), Gestor de CX (dashboard de motivos).

**d) Dados utilizados.**

| Tabela / fonte | Informação relevante |
|---|---|
| `order_reviews` | Nota, título, comentário, data |
| `orders` | Datas e status do pedido; atraso |
| `order_items`, `products`, `sellers` | Nº de itens e sellers no pedido, categoria |
| `order_payments` | Valor do pedido (critério de alçada) |
| **Externo** | Sistema de tickets, histórico de contatos do cliente, reclamações em canais públicos |

**e) Entradas e saídas.**

| Entrada | Saída |
|---|---|
| Avaliação nota 1–3 (com ou sem texto) + dados do pedido | Motivo (taxonomia fixa de 8), severidade, responsável e resumo |
| | Resposta ao cliente (até 600 caracteres) ou rascunho para revisão |
| | Ticket ao seller; sinal ao LogiPredict (entrega) e ao WinBack (pausar) |
| | Dashboard semanal de motivos por seller e categoria |

**f) Indicadores impactados.** Tempo até a 1ª resposta (baseline a medir), % de detratores com caso resolvido, % de classificação correta em auditoria amostral, reincidência por seller, nota média.

**Faz / não faz.**

| Faz | Não faz |
|---|---|
| Classifica, resume, responde com template seguro, abre ticket, sinaliza outros agentes | Não promete reembolso, troca ou cupom; não penaliza seller; não responde caso crítico sem revisão humana |

**AS-IS → TO-BE** *(presumido)*

| Hoje | Com o SentimentDesk |
|---|---|
| Avaliação negativa lida manualmente, sem padrão de motivo | Motivo, severidade e responsável em segundos |
| Casos graves e simples na mesma fila | Casos críticos vão direto ao analista, com resumo |
| Seller reincidente invisível | Dashboard de motivos por seller alimenta a gestão de sellers |

## 6.3 WinBack · Segunda Compra

**a) Objetivo.** Aumentar a conversão da **1ª para a 2ª compra** com contato relevante e no momento certo, dentro da janela de 90 dias.

**b) Problema resolvido.** Só **3,0%** dos 93.358 clientes compram de novo, e só **1,13%** voltam em até 90 dias. Mas quando o cliente volta, volta cedo: **54%** das segundas compras acontecem em até 90 dias. Hoje não há ação estruturada nessa janela. A consequência é custo de aquisição pago para uma única venda.

**c) Usuários envolvidos.** Cliente (recebe mensagem), Analista de CRM (acompanha campanhas), Gestor de CRM (aprova incentivo acima do teto), Marketing (relatório de uplift).

**d) Dados utilizados.**

| Tabela / fonte | Informação relevante |
|---|---|
| `orders`, `customers` | 1ª compra, data de entrega, recorrência (`customer_unique_id`) |
| `order_items`, `products` | Categoria da 1ª compra; categorias da 2ª compra por perfil |
| `order_reviews` | Nota da 1ª compra |
| `order_payments` | Valor da 1ª compra |
| **Externo** | Opt-in (LGPD), histórico de contatos, catálogo e estoque atuais, teto de incentivo |

**e) Entradas e saídas.**

| Entrada | Saída |
|---|---|
| Cliente atinge D+7 após a 1ª entrega | Decisão: não contatar, pausar ou enviar mensagem (com ou sem incentivo) |
| Sinal "pausar" do SentimentDesk | Mensagem personalizada com até 2 categorias recomendadas |
| Ticket resolvido | Mensagem de desculpas com incentivo dentro do teto |
| Fim do ciclo de 90 dias | Relatório de uplift contra o grupo controle (10%) |

**f) Indicadores impactados.** Conversão em 2ª compra em 90 dias (baseline 1,13%), taxa de recompra (3,0%), receita por cliente, uplift contra o controle, taxa de opt-out.

**Faz / não faz.**

| Faz | Não faz |
|---|---|
| Decide elegibilidade, momento, categoria e mensagem; separa o grupo controle | Não contata sem opt-in, não passa de 2 contatos, não dá incentivo > 10% sem aprovação, não atua na base inativa antiga |

**AS-IS → TO-BE** *(presumido)*

| Hoje | Com o WinBack |
|---|---|
| Campanhas de massa, sem considerar a experiência da 1ª compra | Contato individual, no tempo certo, que pausa quando a experiência foi ruim |
| Sem medição de efeito incremental | Grupo controle permanente e uplift medido |

<!-- paisagem -->

# 7. Jornadas de Funcionamento dos Agentes

## 7.1 LogiPredict
![Fluxo do LogiPredict: dois checkpoints de decisão antes de envolver pessoas e aviso ao cliente apenas quando a projeção estoura o prazo.](fluxos/fluxo_logipredict.png)

**Decisões-chave:** (1) o seller vai estourar o limite de postagem? (2) o risco passou do limiar? (3) a nova data prevista passa do prazo? Só a terceira resposta autoriza contato com o cliente. **Humano no loop:** o analista de operações decide a tratativa com a transportadora.

<!-- pagebreak -->

## 7.2 SentimentDesk
![Fluxo do SentimentDesk: o agente classifica, mas casos de baixa confiança ou críticos passam por analista antes da resposta.](fluxos/fluxo_sentimentdesk.png)

**Decisões-chave:** (1) a classificação é confiável? (2) o caso é crítico? (3) o motivo é entrega? **Humano no loop:** classificação manual quando a confiança é baixa; revisão da resposta e definição de compensação nos casos críticos.

<!-- pagebreak -->

## 7.3 WinBack
![Fluxo do WinBack: elegibilidade e experiência anterior são verificadas antes de qualquer oferta.](fluxos/fluxo_winback.png)

**Decisões-chave:** (1) há consentimento e intervalo mínimo? (2) a 1ª experiência foi ruim? (3) o incentivo passa do teto? **Humano no loop:** o Gestor de CRM aprova incentivos acima de 10%.

<!-- pagebreak -->

## 7.4 Jornada multiagente: "o pedido que ia atrasar"
A jornada abaixo usa um **pedido real do dataset**: compra em 25/02/2018, de MG para MA, postada 4 dias após o limite e entregue em 06/04, **10 dias depois do prazo**. O cliente deu nota 1. Mostramos o que teria acontecido com os três agentes em operação.

![Jornada multiagente com um pedido real.](fluxos/jornada_multiagente.png)

<!-- retrato -->

| Dia | O que acontece | Agente / pessoa |
|---|---|---|
| D+6 | O limite de postagem se aproxima e o seller recebe lembrete | LogiPredict |
| D+11 | A postagem sai atrasada para uma rota com 19,7% de atraso; score 80 e alerta a operações | LogiPredict → Analista de Ops |
| D+27 (D-3 do prazo) | Sem confirmação de entrega, cliente avisado com nova data (03/04) | LogiPredict |
| D+40 | Entrega atrasada e nota 1 sem comentário; motivo inferido "atraso", resposta e ticket | SentimentDesk |
| D+40 | Oferta de 2ª compra pausada | WinBack |
| D+41 | Analista de CX aprova cupom de desculpas dentro da alçada | Humano |
| D+55 | Caso resolvido; oferta de 2ª compra na categoria afim | WinBack |

## 7.5 Tratamento de exceções

| Situação | LogiPredict | SentimentDesk | WinBack |
|---|---|---|---|
| Dado faltante | Sem rastreio: usa só o histórico da rota e marca "confiança baixa" | Sem texto: infere pelo pedido, confiança ≤ 0,7, revisão humana | Sem opt-in conhecido: não contata |
| Baixa confiança | Não avisa o cliente; só alerta operações | Fila do analista de CX | Mensagem sem incentivo |
| Conflito de dados | Status "entregue" sem comprovante: sinaliza CX | "Entregue" mas cliente diz que não recebeu: severidade CRÍTICA | Pedido em disputa: pausa |
| Sistema indisponível | Reprocessa na próxima varredura | Mantém a fila; nenhuma resposta automática | Adia o envio; não duplica |
| Cliente de alto valor | Prioridade no alerta | Revisão humana se valor > R$ 500 | Atendimento consultivo (CRM) |

<!-- pagebreak -->

# 8. Prompts Estruturados v2

Os prompts seguem a estrutura **objetivo · contexto · instrução principal · resultado esperado**. Na Fase 2, cada um ganhou **lista fechada de ações**, **evidência que orienta a decisão**, seção **"não faça"** e **gatilhos de humano no loop**. As versões completas e os dez exemplos com casos reais estão em `fase2/prompts/PROMPTS_V2.md`.

## 8.1 SentimentDesk
**a) Objetivo:** classificar a avaliação negativa, responder ao cliente e rotear o caso.
**b) Contexto:** nota, título e comentário; datas de compra, prazo e entrega; nº de itens e de sellers; categoria; valor; UFs; reclamações do seller em 30 dias.
**c) Instrução principal (resumo):**
```text
Você é o SentimentDesk, agente de triagem de avaliações negativas da Olist.
TAXONOMIA (1 principal + até 2 secundários): ENTREGA_NAO_RECEBIDO | ENTREGA_ATRASO |
PEDIDO_ITEM_FALTANDO | PEDIDO_PRODUTO_ERRADO | PRODUTO_DEFEITO | PRODUTO_QUALIDADE |
ATENDIMENTO_FINANCEIRO | OUTROS
- Use os dados do pedido para desempatar (ex.: "não chegou" + 2 itens + entregue → item faltando).
- "Entregue" no sistema, mas o cliente diz que não recebeu → conflito de dados, severidade CRÍTICA.
- Resposta de até 600 caracteres, empática, com próximo passo e prazo padrão de 2 dias úteis.
NÃO FAÇA: prometer reembolso/troca/cupom/data; culpar seller ou transportadora; inventar fatos.
HUMANO NO LOOP: severidade CRÍTICA, confiança < 0,8 ou valor > R$ 500.
SAÍDA: JSON (motivo, confiança, severidade, responsável, resumo, resposta, roteamento, revisão).
```
**d) Resultado esperado:** JSON que alimenta ticket, dashboard e sinais aos outros agentes.

**Exemplo real.** Avaliação nota 1: *"Só chegou a mochila, estou aguardando a lancheira…"*. Pedido com 2 itens, entregue no prazo.

| Campo | Saída do agente |
|---|---|
| Motivo | PEDIDO_ITEM_FALTANDO (confiança 0,90) · severidade ALTA · responsável SELLER |
| Resposta | "Olá! Sentimos muito: seu pedido deveria ter chegado completo. Já abrimos uma solicitação para localizar a lancheira e confirmar se ela foi enviada separadamente. Em até 2 dias úteis você recebe nosso retorno com a solução." |
| Roteamento | Ticket ao seller (confirmar envio do 2º item) + dashboard |
| Por que importa | A regra por palavras-chave classificou como "não recebido". O agente cruzou o texto com os dados do pedido e acertou o responsável. |

## 8.2 LogiPredict
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

**Exemplo real.** Pedido MG → MA, postado 4 dias após o limite; prazo 27/03.

| Campo | Saída do agente |
|---|---|
| Score e ação | **80 (ALTO)** · ESCALAR_OPERACOES no dia da postagem, 19 dias antes do prazo |
| Fatores | Postagem atrasada (+35); MA com 19,7% de atraso (+20); projeção pessimista 29/03 > prazo (+25) |
| D-3 (24/03) | Sem entrega confirmada → AVISAR_CLIENTE com nova data 03/04 |
| Desfecho real | Entregue em **06/04**, 10 dias de atraso. O cliente teria sido avisado 10 dias antes |

*Um segundo caso real (SP → BA) mostra o **falso positivo controlado**: o agente alertou operações, mas não avisou o cliente porque a projeção mediana cabia no prazo. O pedido chegou no prazo.*

## 8.3 WinBack
**a) Objetivo:** decidir se e como contatar o cliente de 1ª compra entre D+7 e D+90.
**b) Contexto:** datas da 1ª compra e da entrega; categoria e valor; nota; atraso; opt-in; último contato; tickets abertos; categorias da 2ª compra por perfil.
**c) Instrução principal (resumo):**
```text
Você é o WinBack. Só clientes de 1ª compra, de 7 a 90 dias após a entrega.
AÇÕES: NAO_CONTATAR | PAUSAR | MENSAGEM_SEM_INCENTIVO | MENSAGEM_COM_INCENTIVO
1. Sem opt-in, contato < 15 dias ou 2 contatos já feitos → NAO_CONTATAR.
2. Nota ≤ 2, atraso ou ticket aberto → PAUSAR até o SentimentDesk resolver.
3. Boa experiência → mensagem sem incentivo, na mesma categoria ou em uma afim.
   Incentivo só no 2º contato (D+45). Incentivo > 10% exige aprovação humana.
NÃO FAÇA: urgência falsa; contato fora da janela; dados pessoais além do primeiro nome.
SAÍDA: JSON (elegível, ação, motivo, categorias, incentivo, mensagem, próximo passo).
```
**d) Resultado esperado:** decisão auditável, mensagem pronta e grupo controle de 10%.

**Exemplo real.** Cliente do RS, 1ª compra em cama/mesa/banho (R$ 112,44), nota 5, entregue no prazo, D+7.

| Campo | Saída do agente |
|---|---|
| Ação | MENSAGEM_SEM_INCENTIVO (incentivo reservado para o 2º contato) |
| Categorias | cama_mesa_banho (46% das 2ªs compras desse perfil) e moveis_decoracao (9%) |
| Mensagem | "Que bom que seu pedido chegou certinho! Separamos novidades em cama, mesa e banho e itens de decoração que combinam com a sua compra." |
| Contraste | Outro cliente real (1ª compra atrasada, nota 2, ticket aberto) recebe **PAUSAR**: nenhuma oferta até o caso ser resolvido |

<!-- pagebreak -->

# 9. Indicadores e Business Case

## 9.1 Indicadores por agente

| Agente | Indicador | Baseline (dataset) | Meta do piloto (90 dias) | Como medir |
|---|---|---|---|---|
| LogiPredict | Taxa de atraso nas rotas do piloto | 8,11% (Brasil); 15–24% no Nordeste | −1 p.p. nas rotas piloto | Comparação com rotas controle |
| LogiPredict | Postagens após o limite | 9,0% | ≤ 6% | `shipping_limit_date` × postagem |
| LogiPredict | Falso positivo do aviso ao cliente | n/a | ≤ 20% | Avisos × entregas no prazo |
| SentimentDesk | Tempo até a 1ª resposta | A medir (não existe no dataset) | 90% em < 24h | Log do agente |
| SentimentDesk | Classificação correta | n/a | ≥ 85% | Auditoria amostral semanal (50 casos) |
| SentimentDesk | Casos críticos com analista em < 4h | n/a | 95% | Fila de CX |
| WinBack | Conversão em 2ª compra (90 dias) | 1,13% | 1,63% (+0,5 p.p.) | Uplift contra grupo controle de 10% |
| WinBack | Opt-out por contato | n/a | < 1% | CRM |

## 9.2 Business case: três cenários
Janela: set/2017 a ago/2018 (12 meses), **na escala do dataset público**. Como o dataset é uma amostra da operação, os valores servem para **dimensionar a lógica**; o cálculo escala linearmente com o volume real.

| Agente | Lógica do cálculo | Conservador | Base | Otimista |
|---|---|---|---|---|
| LogiPredict | 6.689 postagens atrasadas × diferença de atraso (24,4% → 6,5%) × % da diferença eliminada (25/50/75%) | 335 atrasos evitados · 150 notas 1–2 a menos | **670 atrasos · 300 notas 1–2 a menos** | 1.006 atrasos · 451 notas 1–2 a menos |
| SentimentDesk | 11.711 avaliações 1–2 × % tratada com o agente (50/70/90%) × 9 min poupados × R$ 45/h | 878 h · R$ 39,5 mil | **1.229 h · R$ 55,3 mil** | 1.580 h · R$ 71,1 mil |
| WinBack | 71.693 novos clientes × aumento da conversão em 90 dias (+0,25/+0,5/+1,0 p.p.) × ticket da 2ª compra (R$ 148,35) | 179 compras · R$ 26,6 mil | **358 compras · R$ 53,2 mil** | 716 compras · R$ 106,4 mil |

**Premissas explícitas:** 12 minutos de triagem manual contra 3 minutos com o agente; custo do analista de R$ 45/hora; incrementos de conversão em pontos percentuais absolutos sobre a base de 1,13%. O efeito indireto (cliente com entrega no prazo recompra mais) **não foi somado**, para manter o cálculo conservador.

> **Leitura executiva.** O maior retorno não está nos valores isolados. Está na combinação: menos atrasos geram menos avaliações negativas, o que reduz a fila do CX e preserva a chance de segunda compra. Os três agentes atacam elos da mesma corrente.

<!-- pagebreak -->

# 10. Governança, Riscos e Humano no Loop

## 10.1 Quem decide o quê (RACI simplificado)

| Decisão | Agente | Analista | Gestor | Observação |
|---|---|---|---|---|
| Classificar avaliação / calcular risco | **Executa** | Audita amostra | Informado | Automático com monitoramento |
| Lembrete ao seller | **Executa** | Informado | n/a | Template aprovado |
| Aviso ao cliente com nova data | **Executa** | Informado | Aprova o template | Só com projeção de estouro |
| Resposta padrão a avaliação | **Executa** | Revisa amostra | Aprova os templates | Casos críticos nunca automáticos |
| Resposta a caso crítico e compensação | Rascunha | **Decide** | Alçada acima do limite | Trilha de auditoria |
| Tratativa com a transportadora | Recomenda | **Decide** | Informado | n/a |
| Incentivo ≤ 10% | **Executa** | Informado | Define o teto | n/a |
| Incentivo > 10% | Recomenda | n/a | **Decide** | n/a |

## 10.2 Riscos e controles

| Risco | Onde aparece | Controle |
|---|---|---|
| Alarme falso ao cliente | LogiPredict | Aviso só quando a projeção mediana estoura o prazo; meta de falso positivo ≤ 20% |
| Classificação errada | SentimentDesk | Confiança mínima de 0,8; auditoria semanal; fila humana |
| Promessa indevida | SentimentDesk, WinBack | Seção "não faça" nos prompts; templates aprovados por CX e Jurídico |
| Excesso de contato / LGPD | WinBack | Opt-in, intervalo de 15 dias, máximo de 2 contatos, opt-out monitorado |
| Viés histórico | Todos | Evidências recalculadas com dados atuais antes do piloto |
| Dependência de dados externos | LogiPredict | Funciona só com o histórico; rastreio é melhoria, não pré-requisito |

<!-- pagebreak -->

# 11. Roadmap e Próximos Passos

| Onda | Agentes | Período | Critério para avançar |
|---|---|---|---|
| **Wave 1 · piloto** | LogiPredict + SentimentDesk | Meses 1–3 | Falso positivo ≤ 20%; classificação ≥ 85%; 90% de respostas em < 24h |
| **Wave 2** | WinBack | Meses 4–6 | Opt-in e grupo controle prontos; sinal de pausa do SentimentDesk em produção |
| **Wave 3** | SellerCare (coaching com dados dos agentes) e SmartFreight | Meses 7–9 | Uplift comprovado nas Waves 1 e 2 |
| **Orquestração** | Maestro | Fase 4 do projeto | Três especialistas estáveis em produção |

**Próximos passos (Fase 3, protótipo):**
1. Prototipar o SentimentDesk e o LogiPredict em ferramenta **low-code**, com os casos reais deste relatório como base de teste.
2. Medir a acurácia do SentimentDesk contra 30 a 50 avaliações rotuladas pelo grupo.
3. Calibrar os pesos do score do LogiPredict com o histórico completo (falso positivo × falso negativo).

# 12. Recomendação Executiva

A Fase 1 mostrou que a Olist tem um problema conectado: atraso gera avaliação negativa, e avaliação negativa coincide com menor recompra. A Fase 2 transforma esse diagnóstico em operação. São **três agentes especializados**, cada um com **um papel**, **gatilhos claros**, **lista fechada de ações** e **pessoas decidindo o que tem impacto financeiro ou reputacional**.

**Pedimos a aprovação do piloto da Wave 1 (LogiPredict + SentimentDesk) por 90 dias**, com rotas do Nordeste como foco logístico, grupo controle e as metas da Seção 9.1 como critério de continuidade. Os dois agentes usam dados que a Olist já possui, não executam ações irreversíveis e produzem resultado mensurável dentro do próprio piloto.

> **Mensagem para a diretoria.** Não propomos mais agentes; propomos agentes melhores. Começar pelo prazo de entrega é atacar a origem do problema, e cada passo seguinte só avança com resultado medido.

<!-- pagebreak -->

# Apêndice A: Rastreabilidade dos Requisitos da Fase 2

| Requisito do enunciado | Onde está |
|---|---|
| 1. Evolução do relatório da Fase 1 (sem recomeçar do zero) | Seção 2 + estrutura herdada da Fase 1 |
| 2. Pelo menos 3 agentes detalhados | Seção 6 (LogiPredict, SentimentDesk, WinBack) |
| 2a. Objetivo do agente | 6.1a, 6.2a, 6.3a |
| 2b. Problema resolvido (dor, impacto atual, consequências) | 6.1b, 6.2b, 6.3b + Seção 3 |
| 2c. Usuários envolvidos | 6.1c, 6.2c, 6.3c + 5.1 |
| 2d. Dados utilizados (tabelas, informações, dados externos) | 6.1d, 6.2d, 6.3d |
| 2e. Entradas e saídas | 6.1e, 6.2e, 6.3e |
| 2f. Indicadores impactados | 6.1f, 6.2f, 6.3f + 9.1 |
| 3. Fluxos com gatilhos, entradas, decisões, ações, interação humana e saída | Seção 7 (3 fluxos + jornada multiagente + exceções) |
| 4. Prompts com objetivo, contexto, instrução e resultado esperado | Seção 8 + `prompts/PROMPTS_V2.md` |
| 5. Vídeo executivo (link no relatório) | Sumário Executivo (Seção 1) e capa |
| Sempre explicar problema, benefício, impacto, usuários e riscos | Seções 6, 9 e 10 |

# Apêndice B: Fontes e Artefatos

| Artefato | Conteúdo |
|---|---|
| `notebooks/08_fase2_evidencias_business_case.ipynb` | Cadeia de evidência, priorização, business case, casos reais |
| `fase2/dados/numeros_fase2.json` | Fonte única de números (valor, definição, tabela de origem) |
| `fase2/prompts/PROMPTS_V2.md` | Prompts completos e 10 exemplos com casos reais |
| `fase2/fluxos/` | Fluxos em PNG e o script que os gera |
| Notebooks 01–07 e Relatório da Fase 1 | Diagnóstico original (preservado em `fase1/Relatorio_Executivo_Fase1_Olist_FINAL.pdf`) |
| Dataset | Brazilian E-Commerce Public Dataset by Olist (Kaggle), 2016–2018 |
