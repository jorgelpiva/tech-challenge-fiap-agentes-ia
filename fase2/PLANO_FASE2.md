# 🧭 Plano de Implementação — Tech Challenge Fase 2

> **Arquivo-mestre da Fase 2.** Comece qualquer sessão de trabalho por aqui.
> Guia da reunião e mapa dos entregáveis: [EVOLUCAO_FASE2.md](EVOLUCAO_FASE2.md)
> Enunciado: [`POSTECH - Tech Challenge - Fase 2.pdf`](POSTECH%20-%20Tech%20Challenge%20-%20Fase%202.pdf) · Fase 1 entregue: [`Relatorio_Executivo_Fase1_Olist_FINAL.pdf`](../fase1/Relatorio_Executivo_Fase1_Olist_FINAL.pdf)
> **Prazo: 27/10/2026** · Nota da Fase 1: 80/90 (inicialmente 60; ver §3) · Meta: superar a Fase 1

---

## 1. TL;DR
- **Pergunta da Fase 2:** *"Como os agentes de IA irão interagir com usuários, dados e processos da Olist para gerar valor real ao negócio?"*
- **Estratégia adotada:** 3 agentes especializados na **jornada do pedido**, **LogiPredict → SentimentDesk → WinBack**, cada um com um objetivo, gatilhos, lista fechada de ações e humano no loop. Os outros 3 agentes da Fase 1 foram priorizados para fora com critério explícito.
- **Situação em 12/10:** todos os entregáveis estão em **rascunho completo**. Falta revisão do grupo, gravação do vídeo e geração da versão FINAL.

## 2. O que a Fase 2 pede
| # | Entregável | Requisitos obrigatórios |
|---|---|---|
| 1 | **Evolução do Relatório Executivo** | Evoluir o da Fase 1 (sem recomeçar), demonstrar evolução, 15–30 págs. Os itens 2, 3, 4 e o link do 5 ficam **dentro** dele |
| 2 | **Casos de uso** | ≥ 3 agentes; para cada um: a) objetivo, b) problema (dor, impacto atual, consequências), c) usuários, d) dados (tabelas, informações, **externos**), e) entradas/saídas, f) indicadores |
| 3 | **Jornadas** | Fluxos com gatilhos, entradas, decisões, ações, interação humana e saída; simples e com decisões destacadas |
| 4 | **Prompts** | a) objetivo, b) contexto, c) instrução principal, d) resultado esperado |
| 5 | **Vídeo ≤ 5 min** | Evolução, agentes, fluxos, funcionamento e **exemplos de interação**, para executivos que aprovam investimento |

Critérios de avaliação (iguais aos da Fase 1): visão estratégica · IA × objetivos do negócio · capacidade analítica · profundidade dos insights · estruturação executiva · clareza · **qualidade visual** · **organização/profissionalismo** · criatividade · **evolução do projeto**.

## 3. Feedback da Fase 1 (real)
Nota inicial 60/90, revisada para 80/90 após contato no Discord (29/09). O professor justificou a revisão pelo link do vídeo: o PDF dizia "[INSERIR LINK]" no apêndice, embora o link estivesse na página 2. O feedback escrito permanece válido e guiou a Fase 2:
1. Detalhar o racional de onde partiram os achados → **cadeia de evidência** (relatório §4.5).
2. Ações dos agentes muito amplas, carecendo de especialização → **escopo fechado por agente** (§8–§10).
3. Múltiplos objetivos; priorizar o mais próximo do negócio → **matriz de priorização, 6 → 3 agentes** (§5.3).
4. Falha de revisão → **fonte única de números + QA automático no gerador** (sem placeholders).

Também observado na revisão do PDF: nenhuma imagem em 17 páginas, roadmap contraditório (Wave 1 × Fase A) e divergência 12,47 × 12,56 dias. Tudo corrigido.

## 4. Decisões (detalhe e alternativas em [EVOLUCAO_FASE2.md §4](EVOLUCAO_FASE2.md))
| ID | Decisão | Status |
|---|---|---|
| D1 | 3 agentes detalhados: LogiPredict, SentimentDesk, WinBack | Proposta; validar na reunião |
| D2 | WinBack reposicionado para a 2ª compra (D+7 a D+90) | Proposta |
| D3 | SellerCare absorvido; SmartFreight no backlog; Maestro na Fase 4 | Proposta |
| D4 | Correções de rigor declaradas (12,56 dias; `review_answer_timestamp`) | Proposta |
| D5 | Premissas do business case (R$ 45/h; 12 → 3 min; +0,25/0,5/1,0 p.p.) | Proposta |
| D6 | Saídas ilustrativas revisadas; reproduzir com modelo/data antes do vídeo | Proposta |
| D7 | Fluxos por script (matplotlib) com legenda única | Proposta |
| D8 | Roadmap: Wave 1 LogiPredict + SentimentDesk · Wave 2 WinBack · Wave 3 SellerCare/SmartFreight · Fase 4 Maestro | Proposta |
| D9 | Baseline do WinBack = **0,90%** (D+7 a D+90 após a entrega, janela completa); meta Wave 2 = 1,40% (+0,5 p.p.); business case inalterado | ✅ Jorge, 21/10 |
| D10 | Baseline do piloto no Nordeste = **14,3%** (10,8% a 23,9% por UF); meta −1 p.p. (13,3%) | ✅ Jorge, 21/10 |
| D11 | SLA de 4h úteis para decisões humanas (11.5) vira meta do piloto: 95% dentro do prazo | ✅ Jorge, 21/10 |
| D12 | Tom: manter as ressalvas da revisão técnica como estão | ✅ Jorge, 21/10 |

## 5. Backlog
> ✅ feito · 🟨 em andamento · ⬜ a fazer. Resp. = quem executa (ver divisão em EVOLUCAO §5).

### Feito em 12/10 (rascunho completo)
| ID | Entrega | Status |
|---|---|---|
| T0.1 | Prazo confirmado: 27/10 | ✅ |
| T0.2 | Feedback da Fase 1 registrado (§3) | ✅ |
| T1.1 | Divergência 12,47 × 12,56 resolvida (12,56; definição no JSON) | ✅ |
| T1.2 | Roadmap unificado | ✅ |
| T1.3 | Fonte única de números: `NUMEROS_OFICIAIS.md` + `dados/numeros_fase2.json` | ✅ |
| T1.4 | 5 gráficos novos (`img/`) | ✅ |
| W2 | Casos de uso a–f + faz/não faz + AS-IS/TO-BE dos 3 agentes | ✅ |
| W3 | 3 fluxos swimlane + jornada multiagente + tabela de exceções + RACI | ✅ |
| W4 | Prompts v2 + 10 exemplos com casos reais (`prompts/PROMPTS_V2.md`) | ✅ |
| W5 | Business case em 3 cenários + indicadores com metas do piloto | ✅ |
| W6 | Relatório v2: fonte MD + gerador DOCX/PDF + QA automático | ✅ rascunho |
| W6b | Relatório reestruturado como **versão 2.0 do relatório da Fase 1** (mesmas seções, Fase 1 corrigida + Fase 2 incrementada; 26 págs.) | ✅ 14/10 |
| W7 | Roteiro do vídeo + 12 slides com notas do apresentador | ✅ |

### A fazer até 27/10
| ID | Tarefa | Resp. | Status |
|---|---|---|---|
| R1 | Reunião: validar D1–D8 e dividir a revisão | Grupo | ⬜ |
| R2 | Revisão por seção (divisão em EVOLUCAO §5): Leonardo comenta no Word/PPT, técnicos aplicam nas fontes | Todos | ✅ 20–21/10 |
| R2b | Leitura executiva do relatório inteiro + revisão dos slides e do roteiro | Leonardo | ✅ 20/10 (apresentação executiva) |
| R3 | Rodar o notebook 08 em outra máquina e conferir números | Caio | ✅ 19/10 (números conferem) |
| J1 | Revisar §13 (indicadores e business case) e baseline do WinBack com janela completa | Jorge | ✅ 21/10 |
| J2 | Corrigir os gaps da análise de versão (11.3 restaurada, fluxo LogiPredict, Apêndice B, jargão, datas, QA) e regerar relatório, slides e docs | Jorge | ✅ 21/10 |
| R4 | Reproduzir os casos S1 e W1 no claude.ai/ChatGPT; gravar a demo | Lucas | ⬜ |
| R5 | (Opcional, diferencial) mini-avaliação: 30 a 50 avaliações rotuladas × agente | Lucas/Caio | ⬜ |
| V1 | Ensaiar e gravar o vídeo (≤ 5:00); publicar e testar o link em aba anônima | Todos / Jorge | ⬜ |
| F1 | Preencher `LINK_VIDEO` e gerar a versão FINAL (`gerar_relatorio.py`) | Jorge | ⬜ |
| F2 | Leitura completa do PDF FINAL por 2 pessoas | 2 pessoas | ⬜ |
| F3 | Commit/PR/merge + submissão (alvo 26/10) | Jorge | ⬜ |

## 6. Log de decisões e sessões
> Mais recente no topo.

### 2026-10-14 — Sessão 3: reorganização e relatório como evolução da Fase 1
- Repositório reorganizado: uma pasta por fase na raiz (`fase1/`, `fase2/`); `notebooks/` e `data/` compartilhados.
- Ponto levantado pelo Jorge: o enunciado pede **evoluir** o relatório da Fase 1. O rascunho anterior parecia um documento novo.
- Relatório reescrito como **versão 2.0**: mesmas seções da Fase 1 (1 a 14 + apêndices), conteúdo da Fase 1 corrigido, entregáveis da Fase 2 inseridos (seções 4.5, 5.3, 7.2, 8, 9, 10, 11.3, 13.2, 13.3), "Histórico do Documento" com as mudanças e marcas *atualizado/novo* nos títulos; arquitetura da Fase 1 incluída como imagem. 26 páginas.
- Arquivos de `fase1/` não alterados (registro do entregue); as correções aparecem na versão 2.0.

### 2026-10-12 — Sessão 2: execução do rascunho completo
- Dataset baixado do repositório oficial da Olist (`olist/work-at-olist-data`) em `data/olist/` (fora do Git).
- Notebook 08 criado: cadeia de evidência E1–E6, matriz de priorização, business case, casos reais e números oficiais.
- Achados novos que mudaram o desenho: postagem atrasada → atraso 24,4% vs 6,5% (27% dos atrasos); 54% das 2ªs compras em até 90 dias; motivos das avaliações 1–2 (47% entrega, 18% pedido incorreto); `review_answer_timestamp` ≠ tempo de resposta da Olist.
- Escopo reduzido para 3 agentes (resposta ao feedback de priorização).
- Gerados: relatório rascunho (21 págs.), fluxos, prompts v2, slides e roteiro, e o guia [EVOLUCAO_FASE2.md](EVOLUCAO_FASE2.md).
- **Próximo passo:** reunião do grupo (R1).

### 2026-10-12 — Sessão 1: planejamento
- Leitura do enunciado da Fase 2 e revisão do PDF da Fase 1; primeira versão deste plano.

### 2026-10-21 — Revisão do Jorge e correções de consistência
- §13 revisada: números conferem com a fonte única; tabela de metas tinha WinBack (Wave 2) dentro do piloto e faixa "15–24% no Nordeste" sem cálculo.
- Baseline do WinBack medido na janela do agente (notebook 08): **0,90%** (antes 1,13%); 37% das 2ªs compras caem em D+7–D+90 e 21% antes de D+7. Business case inalterado.
- Nordeste: **14,3%** de atraso no agregado (10,8%–23,9% por UF); meta 13,3%.
- Seção 11.3 (política econômica, do Lucas) restaurada após remoção acidental no PR #3; RACI → 11.4; feedback loop/SLA → 11.5; SLA 4h virou meta do piloto (13.2) e entrou no slide 11.
- Fluxo do LogiPredict: "confiança do modelo" → "projeção consistente e dentro da alçada" (score é heurístico); os dois caminhos agora registram e sinalizam o SentimentDesk.
- Apêndice B renomeado ("Limitações e próximos passos"), jargão interno removido, datas corrigidas (v2.0 = 14/10, v2.1 = 27/10), QA do gerador passou a comparar palavra inteira.
- Regerados: relatório (29 págs., QA OK), fluxos, slides e documentos Word de apoio.

### 2026-10-20 — Consolidação da narrativa V5 e revisão técnica
- Material executivo V5 de Leonardo adotado, mantendo observado/premissa/projeção e piloto de dois agentes.
- Revisão técnica de Lucas incorporada a relatório, prompts, fluxos e cenários. Sem recalcular indicadores.
- Vídeo em blocos: Leonardo 1–3, Jorge 4–6, Caio 7–9, Lucas 10–12. Reprodução de S1/W1/W2, ensaio, gravação e link continuam pendentes.
