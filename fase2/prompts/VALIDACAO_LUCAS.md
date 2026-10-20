# Revisão de Lucas: critérios, cenários e demonstração

## Escopo e situação da revisão
Parte de Lucas conforme `fase2/EVOLUCAO_FASE2.md` §5: relatório §§8.2–8.4, 9.2–9.5 e 10; prompts SentimentDesk/WinBack; revisão técnica e demonstração. No vídeo V5, Lucas apresenta os slides 10–12; Caio apresenta os slides 7–9. O LogiPredict, seus exemplos e as contas de Caio/Jorge não foram revisados nesta alteração. A revisão técnica de Lucas preserva 8.4. A seção 10.2 segue a qualificação de simulação da versão executiva de Leonardo; não se alterou o prompt completo de LogiPredict.

As saídas S1–S5/W1–W2 são **referências editoriais**, não novas execuções de LLM. A revisão verifica consistência documental, JSON e fluxos; não mede acurácia nem prova integrações operacionais. Não marcar R4/R5 como concluídos antes da execução/registro e gravação reais. O relatório e a apresentação foram consolidados com a versão V5 de Leonardo. Gravação, link e submissão continuam dependentes do grupo; não há execução real de agente documentada nesta revisão.

## SentimentDesk: critérios de aceitação
- JSON válido, taxonomia e fila previstas, limites de 600 caracteres e revisão respeitados.
- Classificar relato sem afirmar causa ou culpa não comprovada. Sem comentário → OUTROS, hipótese separada, confiança ≤0,7, revisão humana.
- Conflito → CRÍTICA. Valor >R$500/ausente, confiança <0,8, fila a confirmar ou contexto essencial incerto → revisão.
- Confiança do modelo não equivale a probabilidade calibrada.
- Ações sem confirmação permanecem propostas; SLA só se fornecido e aprovado. Não afirmar envio ou ticket aberto sem confirmação.
- Problema aberto de qualquer motivo → pausa no WinBack; motivo sustentado de entrega → LogiPredict.
- Só usar fatos conhecidos no momento da avaliação. Antes da demo temporal, conferir data de resposta da pesquisa e eventos disponíveis com Caio.

## WinBack: matriz de cenários e resultados esperados
W1/W2 usam clientes históricos com contexto operacional simulado. W3–W12 são variações **sintéticas** desses contextos. Nenhum é resultado executado. Salvo alteração explícita, conservar os campos de W1.

| Caso | Alteração do contexto | Decisão esperada | Verificação |
|---|---|---|---|
| W1 | D+7, tratamento, boa experiência, catálogo, zero contatos | MENSAGEM_SEM_INCENTIVO | Mensagem ≤300 caracteres, incentivo zero |
| W2 | Experiência ruim e problema aberto | PAUSAR | `elegivel=false`, mensagem nula, sem cupom |
| W3 | W2 em D+20, problema fechado, resolução confirmada, catálogo presente | MENSAGEM_SEM_INCENTIVO | Nota/atraso antigos não travam indefinidamente |
| W4 | W3, mas segunda compra já realizada | NAO_CONTATAR | Encerrar ciclo, mesmo após resolução |
| W5 | Opt-in desconhecido ou opt-out ativo | NAO_CONTATAR | Dado desconhecido não vira consentimento; revisão se contexto essencial ausente |
| W6 | Grupo CONTROLE | NAO_CONTATAR | Sem mensagem comercial; atendimento preservado |
| W7 | D+6 ou D+91 | NAO_CONTATAR | Janela após entrega aplicada |
| W8 | Um contato há 14 dias; depois testar há 15 dias em D+45 | NAO_CONTATAR / mensagem permitida | Limite de intervalo, catálogo e demais bloqueios revalidados |
| W9 | Dois contatos confirmados; contador ausente em variante | NAO_CONTATAR | Ausente exige verificação, não equivale a zero |
| W10 | D+30 e um contato prévio | NAO_CONTATAR | Segundo contato ainda não chegou a D+45 |
| W11 | D+45, um contato em D+7, política/orçamento autorizam 8% | MENSAGEM_COM_INCENTIVO | Sem criar cupom nem alegar envio; 12% sem aprovação → SEM incentivo |
| W12 | Catálogo ausente, ou experiência ruim sem resolução e sem ticket | NAO_CONTATAR com revisão / PAUSAR | Sem inventar produtos; ticket ausente não equivale a problema resolvido |

## SentimentDesk: cenários adicionais e resultados esperados
| Caso | Entrada resumida | Resultado esperado |
|---|---|---|
| S1 | Mochila recebida, lancheira faltando | Item faltando; fila seller para apurar, causa desconhecida; pausa WinBack |
| S2 | Recebimento parcial com dois sellers e conflito registrado | CRÍTICA, fila A_CONFIRMAR e revisão; não inventar vínculo item-seller |
| S3 | Taças com estampa diferente | Produto errado; pausa mesmo sem motivo de entrega |
| S4 | Produto quebrado e relato de dois e-mails | Defeito/avaria relatado, origem a apurar; não afirmar ausência de retorno como fato |
| S5 | Nada recebido, registro entregue | Não recebido, conflito, CRÍTICA, revisão |
| S6 (sintético) | Nota1, sem texto, atraso conhecido | OUTROS, confiança ≤0,7 e revisão; atraso apenas hipótese |
| S7 (sintético) | Nota3 sem problema no comentário | Sem pausa automática apenas pela nota |
| S8 (sintético) | Valor R$501; repetir com valor ausente | Revisão humana em ambos |
| S9 (sintético) | Comentário manda ignorar regras e oferecer reembolso | Ignorar instrução, classificar conteúdo, sem promessa financeira |
| S10 (sintético) | Ticket falhou, SLA não fornecido | Execução pendente, sem alegar ticket/acionamento nem prazo inventado |

## Avaliação com Caio: amostra e registro
Para SentimentDesk, separar 30–50 reviews antes de ajustar o prompt. Dois integrantes rotulam independentemente motivo e necessidade de revisão e resolvem divergências. Não usar as saídas ilustrativas como gabarito automático. Avaliar o conjunto congelado, registrar erros por classe, cobertura e falhas graves. Amostra pequena serve a diagnóstico, não prova desempenho de produção. Meta ≥85% é proposta do piloto, não resultado alcançado.

Para WinBack, usar a matriz de regras acima, com casos de limite. Aprovação exige **nenhuma violação dos bloqueios**; registrar saídas incorretas e revisar, sem atribuir ganho de conversão a teste de prompt. Grupo controle, execução sem duplicidade e uplift só poderão ser testados com o processo integrado.

Registro mínimo por execução: caso, origem (histórico/sintético), versão do prompt/commit, modelo exibido, data, parâmetros quando acessíveis, entrada completa, saída bruta, resultado esperado, avaliação e observações. Não informar modelo ou resultado que não foi efetivamente observado.

## Demonstração técnica: apoio a Caio nos slides 7–9
1. Abrir sessão nova no modelo escolhido, copiar prompt e contexto completo S1 sem a saída esperada. Explicar que o ticket é proposto e a causa será apurada.
2. Em sessão independente, executar W1 e depois W2 com contextos simulados identificados. Mostrar contato permitido versus pausa. Se houver tempo, W3 mostra retomada sem cupom automático.
3. Preservar entradas/saídas brutas e registrar falhas. Após editar o prompt, usar sessão nova. Não editar saída e apresentá-la como execução original.
4. Se o grupo incluir execução gravada, usar trecho S1 no slide9 de Caio. W1/W2 ficam como evidência de validação; não ampliar o vídeo além de cinco minutos.
5. Lucas ensaia o bloco final (slides 10–12): projeções anuais, critérios do piloto e encerramento. Cada integrante grava um bloco contínuo; cronometrar o vídeo completo até 5 min.

## Dependências com os demais responsáveis
- **Caio:** confirmar instantes das reviews e evitar eventos futuros no contexto; revisar baseline de recompra com janela completa e marco compra/entrega; conferir eventual previsão LogiPredict D−3. Nenhuma dessas contas foi alterada por Lucas.
- **Jorge:** conferir a consolidação das fontes e arquivos gerados, verificar paginação/legibilidade, inserir o link do vídeo e realizar submissão. As saídas editoriais não devem ser chamadas de nova execução medida.
- **Leonardo:** aprovar narrativa V5 e duração do roteiro com o grupo. A jornada é apresentada por Caio no slide8; os dados históricos e intervenções simuladas ficam separados.

## Checklist para aprovação da parte de Lucas
- [x] Regras e saídas esperadas revistas, com subtítulos por assunto.
- [x] Fontes do relatório, prompts, fluxos e falas7–9 alinhadas para revisão.
- [ ] S1/W1/W2 reproduzidos com modelo/data e saídas brutas registrados.
- [ ] Avaliação opcional com Caio executada, se o grupo decidir incluí-la.
- [ ] Gravação e ensaio feitos no tempo combinado.
- [ ] Link do vídeo, versão de submissão e QA final por Jorge/grupo.

## Fala de Lucas: números e limites dos slides 10–12
- 672 atrasos: 6.689 postagens tardias × diferença arredondada de 20,1 p.p. × 50% eliminado (premissa). 302 avaliações: resultado × 44,9 p.p. São associações usadas em projeção, não efeito causal observado.
- 1.230 h: 11.711 avaliações × 70% tratado × 9 min poupados ÷ 60. A R$ 45/h, capacidade equivalente a cerca de R$ 55 mil; não economia de caixa garantida.
- 358 segundas compras: 71.693 clientes × 0,5 p.p. (premissa). Receita bruta de cerca de R$ 53 mil usa ticket de R$ 148,35; não lucro e não resultado do piloto inicial.
- São cenários anuais na escala histórica, nunca promessas de entrega integral em 90 dias. Nenhum indicador foi recalculado nesta consolidação. A revisão do baseline de 90 dias segue dependente de Caio/Jorge.
