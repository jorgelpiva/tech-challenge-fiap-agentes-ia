# 🎬 Roteiro do Vídeo Executivo — Fase 2 (≤ 5 min)

> **Slides:** [`Apresentacao_Fase2_Olist.pptx`](Apresentacao_Fase2_Olist.pptx). As falas abaixo também estão nas **notas do apresentador** de cada slide.
> **Público imaginado (enunciado):** executivos que vão aprovar o investimento. Linguagem de negócio, sem jargão técnico.
> **Divisão sugerida:** 4 falas, uma por integrante. Ajustem na reunião; a soma não pode passar de **5:00**.

## Requisitos do enunciado que o vídeo precisa cobrir
| Requisito | Slide(s) |
|---|---|
| Evolução do projeto | 2 |
| Detalhamento dos agentes | 4, 5 |
| Fluxos construídos | 6, 7, 8 |
| Funcionamento esperado | 10 (jornada com pedido real) |
| Exemplos de interação | 9 (+ demo ao vivo opcional) |
| Evolução clara vs. Fase 1 | 2 e 3 |

## Falas

| Tempo | Slide | Quem | Fala |
|---|---|---|---|
| 0:00–0:20 | 1 · Capa | Jorge | Na Fase 1 mostramos onde a Olist perde valor. A diretoria aprovou a continuidade, e hoje respondemos à pergunta seguinte: como os agentes vão funcionar dentro da operação e gerar valor real. |
| 0:20–0:50 | 2 · O que mudou | Jorge | Ouvimos a avaliação da Fase 1: faltava mostrar de onde vinham os achados, os agentes estavam amplos demais e havia objetivos demais. Respondemos com três mudanças: cada achado agora tem uma cadeia de evidência, priorizamos três agentes e cada agente ganhou um objetivo único, gatilhos e uma lista fechada de ações. |
| 0:50–1:20 | 3 · Evidência | Leonardo | Os dados mostram por onde começar. Quando o pedido atrasa, 54% dos clientes dão nota 1 ou 2, contra 9% no prazo. E um quarto dos atrasos começa antes da transportadora, com o seller postando depois do limite: aí o atraso sobe de 6,5% para 24,4%. Quem teve a primeira compra atrasada volta menos. |
| 1:20–1:40 | 4 · Priorização | Leonardo | Pontuamos os seis agentes em impacto, proximidade do core, evidência, viabilidade e risco. Três ficaram claramente à frente, e os três atuam em sequência na mesma jornada. SellerCare foi absorvido, SmartFreight foi para o backlog e o Maestro fica para a fase de orquestração. |
| 1:40–2:10 | 5 · Três agentes | Caio | O LogiPredict é o guardião do prazo: age no limite de postagem, na postagem e no D-3. O SentimentDesk faz a triagem de toda avaliação 1 a 3, responde e leva o problema a quem resolve. O WinBack trabalha só a janela da segunda compra, de 7 a 90 dias. Nenhum deles concede reembolso, troca transportadora ou dá incentivo alto sozinho. |
| 2:10–2:35 | 6 · Fluxo LogiPredict | Caio | No LogiPredict, três decisões: o seller vai estourar o limite? O risco passou do limiar? A nova data passa do prazo? Só a última autoriza falar com o cliente; o analista de operações decide a tratativa. |
| 2:35–2:55 | 7 · Fluxo SentimentDesk | Lucas | No SentimentDesk, o agente classifica com texto e dados do pedido. Confiança baixa ou caso crítico vai para o analista antes da resposta; motivo de entrega vira sinal para o LogiPredict. |
| 2:55–3:10 | 8 · Fluxo WinBack | Lucas | O WinBack checa consentimento e intervalo e pausa a oferta se a primeira experiência foi ruim. Incentivo acima de 10% precisa de aprovação, e 10% dos clientes ficam como grupo controle. |
| 3:10–3:40 | 9 · Exemplo real | Lucas | Um caso real. O cliente deu nota 1: "Só chegou a mochila, estou aguardando a lancheira". Uma regra de palavras-chave classificaria como "não recebido". O agente cruza com o pedido: 2 itens, entregue no prazo. Classifica como item faltando, responsabiliza o seller, abre ticket e responde ao cliente sem prometer o que não pode cumprir. |
| 3:40–4:10 | 10 · Jornada | Leonardo | Juntando tudo num pedido real: o LogiPredict lembra o seller, detecta o risco 19 dias antes do prazo e avisa o cliente com nova data. Na avaliação nota 1, o SentimentDesk responde e o WinBack pausa a oferta. Resolvido o caso, a oferta de segunda compra volta, no momento certo. |
| 4:10–4:35 | 11 · Valor | Jorge | No cenário base: 670 atrasos evitados e cerca de 300 avaliações negativas a menos, 1.229 horas de triagem poupadas e 358 segundas compras adicionais. O ganho maior vem da combinação: menos atraso gera menos detrator e preserva a recompra. |
| 4:35–5:00 | 12 · Recomendação | Jorge | Pedimos a aprovação de um piloto de 90 dias com LogiPredict e SentimentDesk, focado nas rotas do Nordeste, com grupo controle e as metas que mostramos. Não propomos mais agentes; propomos agentes melhores, começando pela origem do problema. Obrigado. |

## Demo ao vivo (opcional, substitui o slide 9 se couber no tempo)
1. Abrir claude.ai ou ChatGPT.
2. Colar o **prompt de sistema** do SentimentDesk (`docs/fase2/prompts/PROMPTS_V2.md`, seção 1c).
3. Colar a mensagem do **Caso S1** (mochila/lancheira) e mostrar a saída em JSON.
4. Gravar a tela em ~25 s (acelerar 1,5× na edição se precisar).

## Checklist de gravação
- [ ] Ensaiar com cronômetro; cada fala no tempo da tabela
- [ ] Gravar em 1080p, áudio sem eco (microfone de fone serve)
- [ ] Duração final **≤ 5:00**
- [ ] Publicar no Drive com "qualquer pessoa com o link pode ver"
- [ ] **Testar o link em aba anônima**
- [ ] Colar o link em `docs/fase2/config_relatorio.json` → `LINK_VIDEO` e rodar `python docs/fase2/gerar_relatorio.py` (gera a versão FINAL)
