# 🎬 Roteiro — Vídeo Executivo | Tech Challenge Fase 1
## IA Agêntica para o E-Commerce Brasileiro (Olist)

> **Duração alvo:** 4 min 30 s — 5 min  
> **Formato:** Apresentação em vídeo com slides de apoio  
> **Integrantes do Grupo:**
> - 🎤 **Leonardo Granjeiro**
> - 🎤 **Jorge Leandro Piva**
> - 🎤 **Caio Sousa**
> - 🎤 **Lucas Vinicius Oliveira Mendes**
>
> **Pós-Graduação em IA para Devs — FIAP | Turma 2025**

---

## 📋 Estrutura Geral

| Segmento | Apresentador | Conteúdo | Duração |
|----------|-------------|----------|---------|
| Abertura e Contexto | **Leonardo** | Apresentação do grupo e do desafio | ~40 s |
| Diagnóstico de Dados | **Jorge** | Principais achados das análises | ~90 s |
| Proposta de IA Agêntica | **Caio** | Os 6 agentes e arquitetura | ~90 s |
| Impacto e Conclusão | **Lucas** | Métricas de impacto e encerramento | ~40 s |

---

## 🎬 CENA 1 — ABERTURA E CONTEXTO
**Apresentador: Leonardo Granjeiro** | ⏱️ ~40 segundos

> 🖥️ **SLIDE:** Logo FIAP + título "Tech Challenge — IA Agêntica Fase 1" + nomes do grupo

---

**[LEONARDO — câmera ligada ou voz sobre slide]**

> *"Olá! Somos o grupo formado por Leonardo, Jorge, Caio e Lucas, alunos da pós-graduação em IA para Devs da FIAP.*
>
> *O nosso Tech Challenge nos pediu para pensar como uma consultoria de IA: analisar um dataset real de e-commerce, identificar os principais problemas do negócio e propor agentes de IA que resolvam esses problemas de forma autônoma e mensurável.*
>
> *Escolhemos o Brazilian E-Commerce Dataset da Olist — mais de 99 mil pedidos reais feitos entre 2016 e 2018. E o diagnóstico que encontramos... foi revelador."*

> 🖥️ **SLIDE:** Mapa do Brasil com volume de pedidos por estado + logotipo da Olist

---

## 🎬 CENA 2 — DIAGNÓSTICO DE DADOS
**Apresentador: Jorge Leandro Piva** | ⏱️ ~90 segundos

> 🖥️ **SLIDE:** Título "O Diagnóstico — O que os Dados Revelaram"

---

**[JORGE — câmera ligada ou voz sobre slides]**

> *"Realizamos 7 análises exploratórias completas — desde estatísticas descritivas e análise de cohort até testes de hipótese com Mann-Whitney U, e segmentação por K-Means com Análise RFM.*
>
> *Os achados nos surpreenderam."*

> 🖥️ **SLIDE:** Card vermelho grande com "⚠️ Taxa de Recompra: 3%"

> *"Achado número 1: apenas 3% dos clientes voltam para fazer uma segunda compra. Isso significa que a Olist gasta para adquirir um cliente… e 97% das vezes, ele vai embora para sempre. O LTV médio estimado é de apenas R$165 — praticamente o valor de um único pedido."*

> 🖥️ **SLIDE:** Gráfico de barras "Gargalos Logísticos" — Processamento: 3,3d | Trânsito: 9,2d

> *"Achado número 2: a logística. O tempo médio de entrega é de 12,5 dias. Mas quando abrimos esse número, descobrimos que 74% desse tempo — mais de 9 dias — está em trânsito com a transportadora. O vendedor processa em 3 dias. O gargalo não está no vendedor. Está na última milha.*
>
> *E o impacto disso é direto na satisfação: encontramos uma correlação de -0,229 entre atraso e nota de avaliação — confirmada estatisticamente com p menor que 0,001. Os estados do Norte e Nordeste chegam a 24% de taxa de atraso."*

> 🖥️ **SLIDE:** Cluster RFM — 4 segmentos coloridos

> *"E por fim: nossa segmentação identificou que 40% dos clientes — mais de 38 mil pessoas — já estão no grupo 'Em Risco', inativos há mais de 439 dias. São clientes recuperáveis... mas que hoje não recebem nenhuma ação proativa da plataforma."*

---

## 🎬 CENA 3 — PROPOSTA DE IA AGÊNTICA
**Apresentador: Caio Sousa** | ⏱️ ~90 segundos

> 🖥️ **SLIDE:** Título "Nossa Proposta — 6 Agentes de IA Autônomos"

---

**[CAIO — câmera ligada ou voz sobre slides]**

> *"Com base nesses achados, propomos uma arquitetura de IA Agêntica com 6 agentes especializados, cada um atacando um problema específico identificado nos dados."*

> 🖥️ **SLIDE:** Diagrama com os 6 agentes (pode usar o ARQUITETURA.html como base)

> *"O Agente 1 é o Anti-Churn: ele monitora continuamente a base de clientes, identifica quem está entrando no segmento 'Em Risco', e dispara automaticamente campanhas personalizadas de reativação. Nosso target são os 38.655 clientes mapeados no cluster de risco.*
>
> *O Agente 2 é o de Logística Preditiva: ele cruza dados de produto, distância, CEP e histórico da transportadora para prever, antes que aconteça, quais pedidos têm alta probabilidade de atraso — e comunica o cliente proativamente.*
>
> *O Agente 3 monitora Reviews em tempo real, classifica o sentimento com NLP, extrai os temas mais frequentes e dispara alertas imediatos para a equipe de operações.*
>
> *O Agente 4 é o de Sucesso do Vendedor: dos 3.095 sellers, identificamos 527 no cluster 'Problemático' — com nota média de 2,2 e entrega em 14 dias. Esse agente monitora KPIs de cada seller, envia relatórios de coaching automatizados e escala para suspensão quando necessário.*
>
> *O Agente 5 otimiza Precificação e Frete: o frete representa 21% do valor total de um pedido médio. Em algumas categorias passa de 40%. Esse agente sugere otimizações de embalagem e precificação para reduzir o impacto na conversão.*
>
> *E coordenando todos: o Agente 6 — o Orquestrador Executivo de BI. Ele responde perguntas em linguagem natural para a diretoria, gera relatórios sob demanda e roteia decisões entre os demais agentes."*

> 🖥️ **SLIDE:** Diagrama de arquitetura em camadas (Dados → ETL → Agentes → Orquestrador → Usuários)

---

## 🎬 CENA 4 — IMPACTO E CONCLUSÃO
**Apresentador: Lucas Vinicius Oliveira Mendes** | ⏱️ ~40 segundos

> 🖥️ **SLIDE:** Título "Impacto Esperado" com cards de métricas

---

**[LUCAS — câmera ligada ou voz sobre slides]**

> *"Quando colocamos esse sistema para funcionar de forma integrada, o impacto projetado é significativo.*
>
> *Dobrar a taxa de recompra — de 3% para apenas 6% — representaria aproximadamente R$480 mil em receita incremental ao ano, só no segmento de clientes em risco.*
>
> *Reduzir a taxa de atrasos de 8% para 4% significaria 4 mil pedidos a mais por ano chegando no prazo — e com a correlação que provamos, isso se traduz diretamente em NPS e retenção.*
>
> *E reduzir de 527 para menos de 200 vendedores no cluster problemático elevaria a nota média da plataforma de 3,97 para acima de 4,2."*

> 🖥️ **SLIDE:** Quadro final — logo FIAP + nomes do grupo + link do GitHub

> *"Esse é o Tech Challenge Fase 1 do nosso grupo. Não trouxemos apenas uma análise de dados — trouxemos um plano de ação baseado em evidências, com arquitetura técnica, prompts estruturados e agentes prontos para serem implementados nas próximas fases.*
>
> *Obrigado!"*

---

## 📐 Notas de Produção

### Slides Recomendados (sequência)
| # | Conteúdo | Momento |
|---|----------|---------|
| 1 | Capa — Logo FIAP + Título + Nomes | Abertura |
| 2 | "Dataset: 99.441 pedidos — Olist 2016-2018" + mapa Brasil | Cena 1 |
| 3 | **"Taxa de Recompra: 3%"** em vermelho + indicador visual | Cena 2 |
| 4 | Gráfico: decomposição do tempo de entrega (vendedor vs transportadora) | Cena 2 |
| 5 | Heatmap de cohort + mapa de atrasos por estado | Cena 2 |
| 6 | Cluster RFM — 4 bolhas coloridas | Cena 2 |
| 7 | Hexágonos ou cards dos 6 agentes com ícone e nome | Cena 3 |
| 8 | Diagrama de arquitetura em camadas | Cena 3 |
| 9 | Cards de impacto: Receita +R$480K / Atrasos -50% / Sellers -60% | Cena 4 |
| 10 | Quadro final com nomes, FIAP e GitHub | Cena 4 |

### Dicas de Gravação
- 🎙️ Um apresentador por vez, sem sobreposição de vozes
- 🖥️ Mostrar tela com os gráficos dos notebooks durante a Cena 2 agrega muito
- ⏱️ Respeitar os tempos para não ultrapassar 5 min
- 🎞️ Usar transição simples (fade) entre cenas
- 📹 Resolução mínima recomendada: 1080p (Full HD)
- 🎯 O diagrama de arquitetura está pronto em `docs/ARQUITETURA.html` — abrir no navegador e capturar tela

### Ferramentas Sugeridas
- **Gravação de tela:** OBS Studio (gratuito) ou Loom
- **Slides:** Google Slides, Canva ou PowerPoint
- **Edição:** DaVinci Resolve (gratuito) ou CapCut
- **Diagrama de arquitetura:** abrir o `docs/ARQUITETURA.html` no navegador e capturar tela

---

## 📝 Checklist de Pré-Gravação

- [ ] Cada apresentador ensaiou sua parte ao menos 2×
- [ ] Slides revisados e alinhados com o roteiro
- [ ] Microfone testado (sem ruído de fundo)
- [ ] `docs/ARQUITETURA.html` aberto e pronto para captura de tela
- [ ] Gráficos dos notebooks abertos nos momentos certos (Cluster RFM, Gráfico logístico)
- [ ] Cronometrar o ensaio completo para garantir ≤ 5 min
