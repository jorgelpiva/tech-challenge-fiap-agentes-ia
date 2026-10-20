# Roteiro executivo do vídeo | Tech Challenge Fase 2

**Projeto:** Olist Intelligent Marketplace
**Apresentação de referência:** V5 FINAL (12 slides)
**Formato:** quatro apresentadores, cada um em um bloco contínuo
**Duração máxima:** 5 minutos. **Atenção:** os tempos abaixo são estimativas e precisam ser confirmados em ensaio; esta versão prioriza uma fala mais natural e pode exigir cortes para respeitar o limite.

## Bloco 1 | Leonardo | Slides 1 a 3

### Slide 1 | Abertura

Olá, pessoal! Nós somos o grupo responsável pelo projeto Olist Intelligent Marketplace e, neste vídeo, vamos apresentar a evolução do nosso trabalho para a segunda fase do Tech Challenge.

Na primeira etapa, analisamos os dados da Olist e identificamos algumas oportunidades importantes para o uso de inteligência artificial. Agora, nosso desafio é mostrar como essas oportunidades podem se transformar em soluções práticas para o negócio.

### Slide 2 | Nossa recomendação

E a nossa proposta é começar de forma bem objetiva: com dois agentes, o LogiPredict e o SentimentDesk, em um piloto controlado de 90 dias.

A ideia é testar essas soluções em rotas selecionadas do Nordeste, comparar os resultados com um grupo de controle e manter a supervisão humana nas decisões mais sensíveis.

### Slide 3 | Evolução da Fase 1

Para chegar até aqui, partimos das seis oportunidades identificadas na primeira fase e priorizamos três agentes.

Mais do que definir o que cada um faz, detalhamos quais dados utilizam, como tomam decisões, quando devem agir e quais são seus limites.

Ou seja, saímos de um mapa de oportunidades para uma proposta que pode ser testada e medida.

## Bloco 2 | Jorge | Slides 4 a 6

### Slide 4 | Evidências

Mas por que começar justamente por esses agentes?

Quando olhamos os dados históricos da Olist, encontramos alguns sinais importantes.

Cerca de 8% das entregas chegaram atrasadas. E, entre esses pedidos, mais da metade recebeu avaliações negativas, contra apenas 9% dos pedidos entregues no prazo.

Outro ponto interessante é que aproximadamente 27% dos atrasos estão associados à postagem tardia dos vendedores.

Esses números não provam uma relação de causa e efeito, mas mostram onde temos oportunidades relevantes de intervenção.

### Slide 5 | Priorização

Com essas evidências, avaliamos os seis agentes considerando impacto, proximidade com o negócio, qualidade das evidências, viabilidade e risco.

E três se destacaram: o LogiPredict, que atua antes da entrega; o SentimentDesk, que entra na etapa de avaliação; e o WinBack, que busca estimular uma segunda compra.

São agentes diferentes, mas que trabalham em momentos complementares da mesma jornada.

### Slide 6 | Responsabilidades

E aqui existe um ponto importante: não estamos falando de chatbots que simplesmente respondem perguntas.

Cada agente tem uma missão específica, utiliza informações para tomar decisões e possui limites claros de atuação.

Quando existe algum risco maior, como uma compensação financeira ou uma decisão operacional sensível, a responsabilidade continua sendo humana.

## Bloco 3 | Caio | Slides 7 a 9

### Slide 7 | Funcionamento

Na prática, como isso funciona?

Os agentes seguem uma sequência de eventos, análise e decisão.

O LogiPredict acompanha os principais marcos da entrega, identifica possíveis atrasos e pode acionar a operação antes que o problema aconteça.

O SentimentDesk analisa as avaliações considerando não apenas o texto, mas também os dados do pedido.

Já o WinBack verifica se o cliente está elegível para uma nova abordagem, respeitando consentimento, prazo e eventuais problemas ainda não resolvidos.

Tudo isso com regras claras sobre o que pode ser automatizado e o que precisa passar por uma pessoa.

### Slide 8 | Caso real

Para ilustrar, usamos um pedido real do dataset, enviado de Minas Gerais para o Maranhão.

Nesse caso, o vendedor postou o produto quatro dias depois do limite, a entrega aconteceu dez dias após o prazo e o cliente deu nota um.

Com o LogiPredict, seria possível identificar antecipadamente alguns sinais de risco. Depois, o SentimentDesk poderia tratar a avaliação, enquanto o WinBack evitaria uma oferta comercial antes da resolução do problema.

É importante lembrar que essas intervenções são simulações. O que estamos mostrando é como os agentes poderiam atuar.

### Slide 9 | Exemplo do SentimentDesk

Outro exemplo interessante é uma avaliação em que o cliente diz: “Só chegou a mochila, estou aguardando a lancheira”.

Uma análise superficial poderia interpretar que o pedido inteiro não foi entregue.

Mas, ao cruzar a mensagem com os dados do pedido, o SentimentDesk deve identificar que existe um item faltante e encaminhar o caso para o responsável.

É esse contexto que permite uma decisão mais adequada.

## Bloco 4 | Lucas | Slides 10 a 12

### Slide 10 | Impacto esperado

No cenário base anual, estimamos 672 atrasos evitados, 302 avaliações negativas a menos e cerca de 1.230 horas de triagem liberadas. Na expansão futura, o WinBack poderia gerar 358 segundas compras adicionais.

São projeções sobre a amostra histórica, não resultados comprovados nem metas para os 90 dias. Horas liberadas representam capacidade operacional; compras adicionais representam receita bruta, não lucro.

### Slide 11 | Próximos passos

O piloto de 90 dias começa com LogiPredict e SentimentDesk. Vamos comparar qualidade, segurança e benefício incremental com o controle, além da viabilidade econômica. Os resultados orientarão escalar, ajustar ou encerrar.

Na Fase 3 acadêmica, desenvolveremos os protótipos low-code para testar esse funcionamento.

### Slide 12 | Encerramento

Queremos agentes com objetivos claros, decisões responsáveis e impacto mensurável. O próximo passo é validar. Muito obrigado!

---

## Orientações de gravação

- Cada integrante grava seu bloco sem alternar falas: Leonardo (1–3), Jorge (4–6), Caio (7–9), Lucas (10–12).
- As passagens de apresentador ocorrem antes dos slides 4, 7 e 10, com cortes simples na edição.
- O texto foi escrito para soar como uma apresentação conversada, não como leitura dos títulos.
- Os dados percentuais são arredondados na fala; os valores exatos permanecem na apresentação e no relatório.
- As ações dos agentes nos casos históricos são simulações; os benefícios financeiros e operacionais são projeções, não resultados medidos.
- **Ensaio obrigatório:** esta versão expandida ainda não foi cronometrada. Se ultrapassar cinco minutos, encurtar frases antes de acelerar a leitura.

## Apoio técnico à gravação
As falas foram mantidas nos blocos V5: Leonardo1–3, Jorge4–6, Caio7–9 e Lucas10–12. A revisão técnica está em `fase2/prompts/VALIDACAO_LUCAS.md`. Executar S1/W1/W2 com modelo e data registrados antes de apresentar qualquer saída como execução. Os exemplos do material são ilustrativos. O tempo depende de ensaio real, ainda não realizado nesta revisão.
