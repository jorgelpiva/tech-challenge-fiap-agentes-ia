# 🚀 Fase 2: Evolução do Projeto e Entregáveis

> **Documento-guia para a reunião do grupo.** Explica o que foi feito na Fase 2, onde está cada entregável, quais decisões precisam do aval do grupo e quem revisa o quê.
> Prazo de entrega: **27/10/2026** · Versão: rascunho completo de 12/10/2026 · Plano e log de sessões: [PLANO_FASE2.md](PLANO_FASE2.md)

---

## 1. Situação em uma tela

| Entregável do enunciado | Status | Arquivo |
|---|---|---|
| 1. Relatório Executivo evoluído (15–30 págs.) | ✅ Rascunho completo, **21 páginas** | [Relatorio_Executivo_Fase2_Olist_RASCUNHO.pdf](Relatorio_Executivo_Fase2_Olist_RASCUNHO.pdf) (fonte editável: [RELATORIO_EXECUTIVO_FASE2.md](RELATORIO_EXECUTIVO_FASE2.md)) |
| 2. Casos de uso de ≥ 3 agentes (a–f) | ✅ No relatório, Seção 6 | idem |
| 3. Jornadas / fluxos | ✅ 3 fluxos + jornada multiagente, Seção 7 | [fluxos/](fluxos/) |
| 4. Prompts estruturados | ✅ Resumo no relatório (Seção 8) + versão completa com 10 casos reais | [prompts/PROMPTS_V2.md](prompts/PROMPTS_V2.md) |
| 5. Vídeo executivo (≤ 5 min) | 🟨 Roteiro e slides prontos; **falta gravar** | [video/ROTEIRO_VIDEO_FASE2.md](video/ROTEIRO_VIDEO_FASE2.md) · [video/Apresentacao_Fase2_Olist.pptx](video/Apresentacao_Fase2_Olist.pptx) |

**O que falta para entregar:** (1) revisão do grupo, (2) gravar o vídeo, (3) colar o link e gerar a versão FINAL (um comando), (4) submeter.

> A versão FINAL só é gerada quando o link do vídeo estiver preenchido. Isso evita repetir a "falha de revisão" da Fase 1, quando foi entregue um PDF com "[INSERIR LINK]".

---

## 2. O feedback da Fase 1 e como respondemos

**Feedback recebido (Fase 1, nota 60 → revisada para 80/90):**
- *Oportunidade:* detalhar o racional de onde partiram os achados dos problemas estruturais da empresa.
- *Oportunidade:* ações planejadas para os agentes de forma muito ampla, carecendo de maior especialização.
- *Oportunidade:* múltiplos objetivos propostos; é importante priorizar a criação de agentes para o que faz mais sentido e tem maior proximidade com o negócio.
- *Falha de revisão* (o PDF dizia que faltava o link do vídeo, embora ele estivesse na página 2).

**Mesmo com a nota revisada, os quatro pontos são legítimos e foram tratados como requisitos da Fase 2:**

| Feedback | Resposta na Fase 2 | Onde |
|---|---|---|
| Racional dos achados | **Cadeia de evidência** E1–E6: pergunta → tabela/coluna → método → resultado → decisão de desenho | Relatório §3; notebook 08 |
| Ações amplas, sem especialização | Cada agente com **1 objetivo**, **gatilhos**, **lista fechada de ações**, quadro **faz / não faz** e escopo escrito no próprio fluxo | Relatório §5–§7; prompts |
| Muitos objetivos; priorizar | **Matriz de priorização** ponderada: de 6 para **3 agentes**, todos na jornada do pedido | Relatório §4 |
| Falha de revisão | **Fonte única de números** gerada pelo notebook; **QA automático** no gerador do PDF; apêndice de rastreabilidade | [NUMEROS_OFICIAIS.md](NUMEROS_OFICIAIS.md); `gerar_relatorio.py` |

---

## 3. A história da Fase 2 (para todos contarem igual)

1. **O problema nasce na jornada do pedido.** Atraso leva 54% dos clientes a dar nota 1–2 (contra 9% no prazo). 27% dos atrasos começam com o seller postando depois do limite (atraso de 24,4% vs 6,5%).
2. **Por isso, três agentes em sequência na jornada:**
   - **LogiPredict · Guardião do Prazo:** age no limite de postagem, na postagem e no D-3; avisa o cliente só se a projeção estourar o prazo.
   - **SentimentDesk · Triagem de Avaliações Negativas:** classifica o motivo (taxonomia de 8), responde e roteia; casos críticos vão para pessoa.
   - **WinBack · Segunda Compra:** só a janela de D+7 a D+90 após a 1ª entrega; pausa a oferta se a 1ª experiência foi ruim.
3. **Exemplo que amarra tudo:** um pedido real MG → MA, postado 4 dias atrasado e entregue 10 dias depois do prazo. Com os agentes, operações seria acionada 19 dias antes do vencimento e o cliente avisado com nova data.
4. **Pedido à diretoria:** piloto de 90 dias da Wave 1 (LogiPredict + SentimentDesk), rotas do Nordeste, com grupo controle.
5. **Frase de fechamento:** *"Não propomos mais agentes; propomos agentes melhores."*

---

## 4. Decisões que o grupo precisa validar na reunião

| # | Decisão tomada no rascunho | Por quê | Alternativa |
|---|---|---|---|
| D1 | **3 agentes detalhados** (o enunciado pede ≥ 3), não 4–6 | Feedback pediu priorização; os 3 formam uma cadeia na mesma jornada | Detalhar também o SellerCare (mais trabalho, contradiz o feedback) |
| D2 | **WinBack reposicionado** para a 2ª compra (D+7 a D+90), deixando de mirar os 38.655 inativos | 54% das 2ªs compras ocorrem em até 90 dias; inativo antigo raramente volta | Manter o público da Fase 1 (fraco nos dados) |
| D3 | **SellerCare absorvido** (lembrete de postagem → LogiPredict; ticket ao seller → SentimentDesk) | Mantém as ações de maior evidência sem criar um 4º agente | Mantê-lo como agente próprio na Wave 3 (já está no roadmap) |
| D4 | **Correções de números da Fase 1** declaradas no relatório (12,47 → 12,56 dias; "tempo de resposta 3,15 dias" retirado) | Rigor: `review_answer_timestamp` é a resposta do **cliente** à pesquisa, não da Olist | Não mencionar (arriscado se a banca perceber) |
| D5 | **Premissas do business case:** R$ 45/h de analista; 12 → 3 min por avaliação; +0,25/+0,5/+1,0 p.p. de conversão | Conservadoras e explícitas | Ajustar se alguém tiver referência de mercado |
| D6 | **Saídas dos prompts** geradas com Claude (Opus 5.5) sobre casos reais | Garante formato consistente | **Reproduzir no claude.ai/ChatGPT** antes da gravação (ver §5, Lucas) |
| D7 | Fluxos gerados por script (matplotlib), não Draw.io | Reproduzível e versionado; padrão visual único | Redesenhar no Draw.io/Figma se o grupo quiser outro estilo |

---

## 5. Divisão sugerida da revisão (ajustar na reunião)

Critério da divisão: **Leonardo** (perfil de negócio) fica com leitura, narrativa executiva, Word e PowerPoint, sem rodar nada. **Jorge, Caio e Lucas** (perfil técnico) ficam com notebooks, scripts e geração dos arquivos.

| Pessoa | Revisa no relatório | Revisa nos artefatos | Prepara para o vídeo |
|---|---|---|---|
| **Leonardo** (negócio) | **Dono do §1 Sumário Executivo** (como na Fase 1) + leitura executiva do relatório inteiro, com foco em §2 Evolução, §4 Priorização, §11 Roadmap e §12 Recomendação | **Dono da apresentação** (como na Fase 1): slides (`.pptx`) e roteiro do vídeo; premissas de negócio D5 (junto com o Jorge) | Slides 3, 4, 10; condução do ensaio geral (o "olhar do executivo") |
| **Jorge** (técnico) | §9 Business case | Rodar `gerar_relatorio.py` e `gerar_slides.py`; aplicar nas fontes os comentários do Leonardo; `config_relatorio.json` e versão FINAL | Slides 1, 2, 11, 12; edição final; submissão |
| **Caio** (técnico) | §3 Evidências, §5 Visão operacional, §6.1 LogiPredict, §7.1, §10 Governança | **Rodar o notebook 08** e conferir [NUMEROS_OFICIAIS.md](NUMEROS_OFICIAIS.md); `gerar_fluxos.py`; prompts do LogiPredict (casos L1–L3) | Slides 5, 6 |
| **Lucas** (técnico) | §6.2 SentimentDesk, §6.3 WinBack, §7.2–7.5, §8 Prompts | [PROMPTS_V2.md](prompts/PROMPTS_V2.md): reproduzir os casos S1 e W1 no claude.ai/ChatGPT; gravar a demo | Slides 7, 8, 9 |

**Regra de revisão:**
- **Leonardo** comenta direto no Word ([Relatorio_Executivo_Fase2_Olist_RASCUNHO.docx](Relatorio_Executivo_Fase2_Olist_RASCUNHO.docx), com Revisão → Novo comentário) e no PowerPoint. Não precisa mexer em arquivo-fonte.
- **O pessoal técnico** aplica as correções na **fonte** (`RELATORIO_EXECUTIVO_FASE2.md`, `PROMPTS_V2.md`, `gerar_fluxos.py`, `build_notebook_08.py` ou `gerar_slides.py`) e roda o gerador. Ninguém edita o PDF, o .docx ou o .pptx gerados à mão, porque a próxima geração sobrescreve.

---

## 6. Cronograma até 27/10

| Data | Marco |
|---|---|
| até 15/10 | Reunião do grupo: validar decisões D1–D7 e dividir a revisão |
| 16–19/10 | Revisão individual (Leonardo comenta no Word/PPT; técnicos aplicam nas fontes) |
| 20–22/10 | Ensaio com cronômetro e gravação do vídeo (≤ 5:00) |
| 23/10 | Link no config → gerar versão FINAL do relatório |
| 24–25/10 | QA cruzado: cada um lê o PDF final inteiro como "executivo" |
| 26/10 | Submissão (1 dia de folga antes do prazo) |
| 27/10 | Prazo final |

---

## 7. Como regenerar tudo

```bash
# 0) Dataset (fora do Git). Se faltar data/olist/, baixe do Kaggle ou do repositório oficial da Olist
#    (https://github.com/olist/work-at-olist-data/tree/master/datasets)

# 1) Evidências, gráficos, números oficiais e casos reais
python notebooks/build_notebook_08.py

# 2) Fluxos (PNG)
python fase2/fluxos/gerar_fluxos.py

# 3) Relatório (.docx + .pdf). Precisa do Microsoft Word instalado (conversão para PDF)
python fase2/gerar_relatorio.py
#    Sem LINK_VIDEO no config → fase2/..._RASCUNHO.pdf
#    Com LINK_VIDEO           → fase2/Relatorio_Executivo_Fase2_Olist_FINAL.pdf

# 4) Slides do vídeo
python fase2/video/gerar_slides.py
```
Dependências: `pandas matplotlib scipy scikit-learn nbformat nbconvert python-docx docx2pdf python-pptx pymupdf`.

---

## 8. Mapa de arquivos da Fase 2

O repositório tem **uma pasta por fase na raiz**; `notebooks/` e `data/` são compartilhados.

```
fase1/                               ← Fase 1 entregue (não alterar)
└── Relatorio_Executivo_Fase1_Olist_FINAL.pdf, mapa de agentes, prompts, apresentacao/ …
fase2/
├── POSTECH - Tech Challenge - Fase 2.pdf  ← enunciado
├── EVOLUCAO_FASE2.md            ← ESTE ARQUIVO (guia da reunião)
├── PLANO_FASE2.md               ← plano, backlog e log de sessões
├── RELATORIO_EXECUTIVO_FASE2.md ← FONTE do relatório
├── gerar_relatorio.py · config_relatorio.json
├── Relatorio_Executivo_Fase2_Olist_RASCUNHO.(pdf|docx)
├── Relatorio_Executivo_Fase2_Olist_FINAL.(pdf|docx)   ← gerado quando o vídeo existir
├── NUMEROS_OFICIAIS.md · dados/numeros_fase2.json
├── img/        ← gráficos (gerados pelo notebook 08)
├── fluxos/     ← fluxos PNG + gerar_fluxos.py
├── prompts/    ← PROMPTS_V2.md + exemplos/casos_reais.json
└── video/      ← roteiro + slides (+ gerar_slides.py)
notebooks/
├── 08_fase2_evidencias_business_case.ipynb
└── build_notebook_08.py
```

---

## 9. Checklist final antes de submeter
- [ ] Decisões D1–D7 validadas pelo grupo
- [ ] Notebook 08 rodado; nenhum número no relatório fora de `NUMEROS_OFICIAIS.md`
- [ ] Casos S1 e W1 reproduzidos no claude.ai/ChatGPT (resultado coerente com o relatório)
- [ ] Vídeo ≤ 5:00, link testado em aba anônima
- [ ] `LINK_VIDEO` preenchido e versão FINAL gerada (QA do script = OK, 15–30 páginas)
- [ ] Leitura completa do PDF FINAL por pelo menos 2 pessoas
- [ ] Commit, PR e merge na `master`; submissão na plataforma
