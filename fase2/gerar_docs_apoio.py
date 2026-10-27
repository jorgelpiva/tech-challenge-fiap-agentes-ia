"""Gera dois documentos Word de apoio para o grupo:

  1. fase2/Alteracoes_Relatorio_v1_para_v2.docx — o que mudou, seção por seção,
     do relatório da Fase 1 (v1.0) para o relatório da Fase 2 (v2.0)
  2. fase2/Entregaveis_Fase2.docx — entregáveis do enunciado da Fase 2 com a
     seção/página do relatório e o caminho na árvore de arquivos

Uso (na raiz do repo):  python fase2/gerar_docs_apoio.py
Rode DEPOIS de gerar_relatorio.py: as páginas são lidas do PDF gerado
(FINAL, se existir; senão o RASCUNHO).
"""
from pathlib import Path
import pymupdf
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parent
PDF = AQUI / 'Relatorio_Executivo_Fase2_Olist_FINAL.pdf'
if not PDF.exists():
    PDF = AQUI / 'Relatorio_Executivo_Fase2_Olist_RASCUNHO.pdf'
PAGINAS_V2 = [pg.get_text() for pg in pymupdf.open(PDF)]

AZUL_ESC, AZUL, CINZA = RGBColor(0x1F, 0x3A, 0x5F), RGBColor(0x2A, 0x78, 0xD6), RGBColor(0x52, 0x51, 0x4E)
COR_TIPO = {'Mantido': 'EEF1F5', 'Corrigido': 'FDF0CF', 'Acrescentado': 'DCF2E8', 'Substituído': 'E4E0F8', 'Retirado': 'FDE6DC'}


def pagina(titulo):
    """Página (1-based) do relatório v2 em que o título aparece pela primeira vez como cabeçalho."""
    for i, txt in enumerate(PAGINAS_V2[1:], start=2):   # pula a capa
        if titulo in txt:
            return i
    return '?'


# ----------------------------------------------------------------------------- helpers de formatação
def novo_doc(titulo_cab):
    doc = Document()
    st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)
    st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri'); st.paragraph_format.space_after = Pt(4)
    for nome, tam, cor in (('Heading 1', 16, AZUL_ESC), ('Heading 2', 12.5, AZUL)):
        h = doc.styles[nome]; h.font.name = 'Calibri'; h.font.size = Pt(tam); h.font.color.rgb = cor; h.font.bold = True
        h.paragraph_format.space_before = Pt(10); h.paragraph_format.space_after = Pt(5)
    s = doc.sections[0]
    s.page_width, s.page_height = Cm(21.59), Cm(27.94)
    s.left_margin = s.right_margin = Cm(1.8); s.top_margin, s.bottom_margin = Cm(1.6), Cm(1.5)
    r = s.header.paragraphs[0].add_run(titulo_cab); r.font.size = Pt(8); r.font.color.rgb = CINZA
    return doc


def par(doc, texto, tam=10, cor=None, negrito=False, italico=False, depois=4):
    p = doc.add_paragraph()
    for k, parte in enumerate(texto.split('**')):
        if not parte:
            continue
        r = p.add_run(parte); r.font.size = Pt(tam); r.bold = negrito or k % 2 == 1; r.italic = italico
        if cor is not None:
            r.font.color.rgb = cor
    p.paragraph_format.space_after = Pt(depois)
    return p


def sombrear(cel, cor):
    tcPr = cel._tc.get_or_add_tcPr(); shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), cor); tcPr.append(shd)


def tabela(doc, cab, linhas, larguras, tam=8.5, col_tipo=None, mono_col=None):
    t = doc.add_table(rows=1 + len(linhas), cols=len(cab)); t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, w in enumerate(larguras):
        for c in t.columns[j].cells:
            c.width = Cm(w)
    for i, linha in enumerate([cab] + linhas):
        if i == 0:
            trPr = t.rows[0]._tr.get_or_add_trPr(); h = OxmlElement('w:tblHeader'); h.set(qn('w:val'), 'true'); trPr.append(h)
        for j, txt in enumerate(linha):
            c = t.cell(i, j); c.text = ''
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
            for k, parte in enumerate(str(txt).split('**')):
                if not parte:
                    continue
                r = p.add_run(parte); r.font.size = Pt(tam); r.bold = (i == 0) or k % 2 == 1
                if i == 0:
                    r.font.color.rgb = AZUL_ESC
                if mono_col is not None and j == mono_col and i > 0:
                    r.font.name = 'Consolas'; r.font.size = Pt(tam - 0.5)
            if i == 0:
                sombrear(c, 'E8EEF7')
            elif col_tipo is not None and j == col_tipo and txt in COR_TIPO:
                sombrear(c, COR_TIPO[txt])
    doc.add_paragraph().paragraph_format.space_after = Pt(2)
    return t


# ============================================================================= 1. ALTERAÇÕES v1 → v2
ALTERACOES = [  # (seção v1 → seção v2, título para achar a página na v2, [(tipo, item, v1.0, v2.0)])
    ('Capa', None, [
        ('Corrigido', 'Fase e versão', 'TECH CHALLENGE · FASE 1 · versão final 26/08/2026', 'TECH CHALLENGE · FASE 2 · **versão 2.1**, evolução do relatório da Fase 1'),
        ('Acrescentado', 'Perguntas', 'Só a pergunta central da Fase 1', 'Pergunta da Fase 1 **e** pergunta da Fase 2'),
        ('Acrescentado', 'Links', 'Sem links na capa', 'Vídeo da Fase 2 e repositório'),
    ]),
    ('(novo) Histórico do Documento', 'Histórico do Documento', [
        ('Acrescentado', 'Controle de versões', '—', 'Tabela v1.0 → v2.0 → v2.1, resposta a cada ponto do feedback e lista das correções'),
    ]),
    ('1. Sumário Executivo', '1. Sumário Executivo', [
        ('Mantido', 'Diagnóstico de abertura', 'Recompra 3,00%; atraso 8,11%; frete 21,34%; 14,7% notas 1–2', 'Mesmos números'),
        ('Retirado', 'Tabela de desafios', 'Desafio · Evidência · Resposta agêntica · KPI (6 agentes)', 'Substituída por texto: destino de cada um dos 6 agentes (3 priorizados, SellerCare absorvido, SmartFreight no backlog, Maestro na Fase 4)'),
        ('Substituído', 'Recomendação', '"Jornada progressiva com cinco agentes especialistas e um orquestrador"', '**Abre com o pedido:** piloto de 90 dias de LogiPredict + SentimentDesk no Nordeste, condicionado a volume elegível, controle e orçamento'),
        ('Acrescentado', 'Pergunta e resposta da Fase 2', '—', 'Atraso → 54% de notas 1–2; 27% dos atrasos nascem na postagem; atraso reduz recompra'),
        ('Acrescentado', 'Valor esperado', '—', 'Piloto: 672 atrasos evitados e 1.230 h poupadas (≈ R$ 55 mil de capacidade); expansão futura: WinBack 358 2ªs compras (≈ R$ 53 mil de receita bruta); memória de cálculo na Seção 13.4'),
        ('Corrigido', 'Links', 'Vídeo da Fase 1 + GitHub', 'Vídeo da Fase 2 + vídeo da Fase 1 + GitHub'),
    ]),
    ('2. Contexto e Problema de Negócio', '2. Contexto e Problema', [
        ('Mantido', '2.1 Quatro fricções', 'Retenção, logística, experiência, sellers (texto)', 'Mesmo conteúdo, organizado em tabela'),
        ('Corrigido', 'Tempo de entrega', '"próximo de 12,5 dias"', '**12,56 dias**'),
        ('Retirado', 'Parágrafo de critério', '"o agente só é proposto quando existe um problema claro..."', 'Substituído pela matriz de priorização (5.3)'),
        ('Acrescentado', '2.2 A pergunta da Fase 2', '—', 'Do "onde" (Fase 1) para o "como" (Fase 2)'),
    ]),
    ('3. Abordagem Analítica', '3. Abordagem Analítica', [
        ('Corrigido', 'Frentes de análise', 'Sete dimensões', '**Oito frentes**: nova linha "Evidências para desenho dos agentes (notebook 08)"'),
        ('Mantido', '3.1 Nota estatística', 'Associação, não causalidade', 'Mantida + grupo controle no piloto'),
        ('Acrescentado', '3.2 Evidência, premissa e validação', '—', 'Cada número classificado como **observado**, **premissa** ou **projeção**'),
        ('Acrescentado', '3.3 Limitações', '3 limitações', '+ "o dataset não contém o tempo de resposta da Olist às avaliações"'),
    ]),
    ('4. Principais Achados', '4. Principais Achados', [
        ('Mantido', '4.1 a 4.4', 'Retenção, logística, reviews, sellers', 'Texto da Fase 1 mantido'),
        ('Corrigido', '4.2 Tempo de entrega e etapas', '~12,5 dias; trânsito 9,19 dias; processamento 3,28 dias', '**12,56** dias; trânsito **9,33** dias (74%); processamento **3,23** dias'),
        ('Acrescentado', 'Achados novos em 4.1 a 4.3', '—', 'Janela da 2ª compra (54% em 90 dias; 37% na janela do WinBack); postagem atrasada (24,4% vs 6,5%); 54,1% notas 1–2 com atraso; 47% dos comentários sobre entrega'),
        ('Acrescentado', '4.5 Da evidência à decisão', '—', 'Tabela E1–E6 (pergunta → dado → método → resultado → decisão) + 3 gráficos'),
    ]),
    ('5. Segmentação e Priorização', '5. Segmentação e Priorização', [
        ('Mantido', '5.1 RFM e 5.2 sellers', 'Tabelas K=4 e K=3', 'Mesmas tabelas; leitura de "Novos" e "Em Risco" ligada ao WinBack'),
        ('Acrescentado', '5.2.1 Por que o Nordeste', '—', '**14,3%** de atraso no agregado dos 9 estados (10,8% a 23,9% por UF) + desenho de medição'),
        ('Substituído', '5.3 Critério de priorização', 'Critério qualitativo + ondas (Wave 1 SentimentDesk + LogiPredict; Wave 2 WinBack + SellerCare; Wave 3 SmartFreight + Maestro)', '**Matriz ponderada** (5 critérios, pesos 30/25/20/15/10) + gráfico; ondas movidas para a Seção 12'),
    ]),
    ('6. Mapa de Agentes de IA', '6. Mapa de Agentes', [
        ('Mantido', 'Os 6 agentes', 'WinBack, LogiPredict, SentimentDesk, SellerCare, SmartFreight, Maestro', 'Mesmos 6, como visão de longo prazo'),
        ('Substituído', 'Coluna "Benefício esperado"', 'Hipóteses: recompra 3% → 7%; atrasos < 4%; reverter 30% das notas 1; recuperar 50% dos sellers; +12% de conversão; 40 h/semana', 'Coluna **"Fase 2"** (decisão por agente); hipóteses viraram metas de piloto e business case (Seção 13)'),
        ('Corrigido', 'Objetivo do WinBack', 'Reativar clientes do segmento Em Risco (38.655, +439 dias)', '**Converter a 1ª compra em 2ª na janela de 90 dias**'),
        ('Substituído', '6.1 Interações', '6 interações entre 6 agentes', '**3 sinais** entre os agentes priorizados'),
        ('Corrigido', '6.2 Decisões de escopo', 'Agente de SAC "candidato natural para a Fase 2"; cross-sell no SmartFreight', 'SAC **não criado** (coberto por SentimentDesk e LogiPredict); recomendação de categoria no WinBack'),
    ]),
    ('7. Arquitetura Conceitual', '7. Arquitetura Conceitual', [
        ('Substituído', 'Representação', 'Tabela de 5 camadas (texto)', '**Imagem da arquitetura da Fase 1** (não estava no PDF entregue)'),
        ('Mantido', '7.1 Autonomia responsável', 'Princípio', 'Mantido'),
        ('Acrescentado', '7.2 Visão operacional', '—', 'Momento, frequência, usuários, sistemas e limites dos 3 agentes'),
    ]),
    ('8. Casos de Uso e Guardrails', '8. Casos de Uso Detalhados', [
        ('Substituído', 'Casos de uso', '1 parágrafo por agente (6 agentes): caso, autonomia, guardrails', '**3 agentes completos** nos itens a) a f) + faz/não faz + hoje × com o agente'),
        ('Mantido', '8.4 Demais agentes', 'SellerCare, SmartFreight, Maestro', 'Caso de uso e guardrails da Fase 1 em tabela'),
    ]),
    ('(novo) 9. Jornadas de Funcionamento', '9. Jornadas de Funcionamento', [
        ('Acrescentado', 'Fluxos', '—', '3 fluxos (raias, gatilhos, decisões, humano no loop, saídas) + jornada multiagente com pedido real (caso observado × atuação simulada)'),
        ('Acrescentado', '9.5 e 9.6', '—', 'Natureza das decisões (regras, score heurístico, IA generativa, agentes) + tabela de exceções'),
    ]),
    ('9. Prompts → 10. Prompts Estruturados', '10. Prompts Estruturados', [
        ('Mantido', 'Estrutura', 'Objetivo · contexto · instrução · resultado', 'Mesma estrutura'),
        ('Substituído', 'Prompts', '6 prompts genéricos', '**3 prompts v2**: ações fechadas, evidência, "não faça", humano no loop'),
        ('Acrescentado', 'Exemplos', 'Sem exemplos', '**Exemplos com casos reais do dataset** (10 no PROMPTS_V2.md)'),
        ('Mantido', 'Prompts dos demais agentes', 'No relatório', 'Referenciados em fase1/PROMPTS_ESTRUTURADOS.md'),
    ]),
    ('10. Riscos → 11. Riscos, Governança e HITL', '11. Riscos, Governança', [
        ('Mantido', 'Tabela de riscos', '7 riscos', 'Mesmos 7, com controles concretos dos agentes priorizados'),
        ('Acrescentado', 'Novos riscos', '—', '"Classificação errada" (SentimentDesk) e "Gargalo de aprovação" (fila humana)'),
        ('Mantido', 'Matriz de autonomia', '6 tipos de ação', 'Idêntica'),
        ('Acrescentado', '11.3 Política econômica dos incentivos', '—', 'Teto de 10% é regra proposta; exige margem, orçamento e política aprovada'),
        ('Acrescentado', '11.4 Quem decide o quê', '—', 'Tabela agente × analista × gestor'),
        ('Acrescentado', '11.5 Feedback loop e filas humanas', '—', 'Correções humanas recalibram os agentes; **SLA de 4 horas úteis** para decisões humanas'),
    ]),
    ('11. Roadmap → 12. Roadmap', '12. Roadmap', [
        ('Corrigido', 'Ordem de implantação', 'Fase A: SentimentDesk + WinBack + SellerCare; Fase B: LogiPredict + SmartFreight; Fase C: Maestro (contradizia a Seção 5.3)', '**Roadmap único**: Wave 1 LogiPredict + SentimentDesk; Wave 2 WinBack; Wave 3 SellerCare + SmartFreight; Maestro na Fase 4'),
        ('Acrescentado', 'Critério para avançar', '—', 'Meta mínima por onda'),
        ('Substituído', '11.1 Hipóteses de impacto', 'Tabela de hipóteses por agente', 'Metas do piloto (13.2) e business case (13.3)'),
        ('Acrescentado', 'Próximos passos', '—', 'Fase 3: protótipo low-code, mini-avaliação de acurácia, calibração do score'),
    ]),
    ('12. Indicadores → 13. Indicadores e Business Case', '13. Indicadores de Sucesso', [
        ('Corrigido', 'Tempo médio total', '12,47 dias', '**12,56 dias**'),
        ('Corrigido', 'Processamento', '3,28 dias', '**3,23 dias**'),
        ('Corrigido', 'Tempo de resposta a reviews', '3,15 dias', '**A medir no piloto** (a coluna era a resposta do cliente à pesquisa)'),
        ('Retirado', 'Nota sobre divergência', '"essa divergência deve ser conferida antes da submissão"', 'Divergência resolvida'),
        ('Acrescentado', 'Novos baselines', '—', 'Conversão em 2ª compra de D+7 a D+90 após a entrega (**0,90%**); postagem após o limite (9,0%)'),
        ('Acrescentado', '13.2 a 13.4', '—', 'Metas do piloto (Nordeste: −1 p.p. sobre o baseline das rotas selecionadas, referência histórica 14,3%; SLA humano 4h; WinBack 0,90% → 1,40% na Wave 2) + protocolo do piloto + business case em 3 cenários + **memória de cálculo**'),
    ]),
    ('13. Recomendação → 14. Recomendação Executiva', '14. Recomendação Executiva', [
        ('Substituído', 'Recomendação', 'Começar por experiência e logística; depois retenção e sellers; depois frete e orquestração', '**Aprovar piloto de 90 dias da Wave 1** com grupo controle e metas'),
        ('Mantido', 'Mensagem final', '"IA Agêntica como capacidade de negócio, não coleção de chatbots"', 'Mantida + "não propomos mais agentes; propomos agentes melhores"'),
    ]),
    ('14. Fontes → 15. Fontes · Apêndices', '15. Fontes do Projeto', [
        ('Corrigido', 'Fontes', 'Enunciado Fase 1 + artefatos da Fase 1', 'Enunciados das 2 fases + notebook 08 + NUMEROS_OFICIAIS + PROMPTS_V2 + fluxos'),
        ('Corrigido', 'Apêndice A', 'Requisitos da Fase 1, com "Inserir link final nesta seção"', 'Requisitos das Fases 1 **e** 2, **sem placeholder**'),
        ('Substituído', 'Apêndice B', 'Lista de materiais com "[INSERIR LINK APÓS PUBLICAÇÃO]"', '**Limitações e próximos passos de validação** (materiais incorporados às Fontes)'),
    ]),
    ('Formato geral', None, [
        ('Corrigido', 'Imagens', '**0 imagens** em 17 páginas', f'**9 imagens** (4 gráficos, arquitetura, 3 fluxos, jornada) em {len(PAGINAS_V2)} páginas'),
        ('Acrescentado', 'Sinalização de evolução', '—', 'Títulos marcados "(atualizado na Fase 2)" ou "(novo na Fase 2)"'),
    ]),
]

doc = novo_doc('Tech Challenge · Fase 2 · Alterações do relatório v1.0 → v2.1')
doc.add_heading('Alterações do Relatório Executivo: versão 1.0 (Fase 1) → versão 2.1 (Fase 2)', 1)
par(doc, f'Documento de apoio ao grupo. Compara o relatório entregue na Fase 1 (fase1/Relatorio_Executivo_Fase1_Olist_FINAL.pdf, 17 páginas) com a versão 2.1 (fase2/{PDF.name}, {len(PAGINAS_V2)} páginas). A coluna "pág. v2" indica onde a seção está na versão 2.1.', 9.5, CINZA)

contagem = {}
for _, _, itens in ALTERACOES:
    for tipo, *_ in itens:
        contagem[tipo] = contagem.get(tipo, 0) + 1
doc.add_heading('Resumo', 2)
tabela(doc, ['Tipo de alteração', 'Quantidade', 'Significado'],
       [[t, contagem.get(t, 0), s] for t, s in (
           ('Mantido', 'Conteúdo da Fase 1 preservado (eventualmente reorganizado)'),
           ('Corrigido', 'Número, texto ou inconsistência da Fase 1 corrigido'),
           ('Acrescentado', 'Conteúdo novo da Fase 2'),
           ('Substituído', 'Conteúdo da Fase 1 trocado por versão evoluída'),
           ('Retirado', 'Removido por estar errado ou ser placeholder'))],
       [4, 2.5, 11.4], col_tipo=0)

doc.add_heading('Principais correções de números', 2)
tabela(doc, ['Indicador', 'v1.0', 'v2.0', 'Motivo'], [
    ['Tempo médio de entrega', '12,47 / 12,5 / 12,56 dias (variava)', '**12,56 dias**', 'Valor único, calculado no notebook 08 (compra → entrega, pedidos entregues)'],
    ['Tempo em trânsito', '9,19 dias', '**9,33 dias** (74%)', 'Recalculado com a mesma definição'],
    ['Processamento do seller', '3,28 dias', '**3,23 dias**', 'Recalculado com a mesma definição'],
    ['Tempo de resposta a reviews', '3,15 dias', '**A medir no piloto**', 'A coluna review_answer_timestamp é a resposta do cliente à pesquisa, não da Olist'],
    ['Público do WinBack', '38.655 inativos (+439 dias)', '**1ª compra, D+7 a D+90**', '54% das 2ªs compras ocorrem em até 90 dias'],
    ['Ordem de implantação', 'Duas ordens diferentes (Seções 5.3 e 11)', '**Roadmap único**', 'Inconsistência interna'],
    ['Baseline do WinBack', '— (na v2.0: 1,13%)', '**0,90%** (D+7 a D+90 após a entrega)', 'Medido na janela em que o agente atua, só clientes com janela completa; business case inalterado'],
    ['Atraso no Nordeste (piloto)', '— (na v2.0: "15–24%")', '**14,3%** (10,8% a 23,9% por UF)', 'Agregado dos 9 estados calculado no notebook 08 (referência histórica); meta = −1 p.p. sobre o baseline das rotas selecionadas, contra controle'],
], [3.6, 4.2, 3.6, 6.5])

doc.add_heading('Alterações seção por seção', 2)
for secao, titulo_v2, itens in ALTERACOES:
    pg = pagina(titulo_v2) if titulo_v2 else '—'
    par(doc, f'**{secao}**   ·   pág. v2: {pg}', 10.5, AZUL_ESC, depois=2)
    tabela(doc, ['Tipo', 'Item', 'Versão 1.0 (Fase 1)', 'Versão 2.0 (Fase 2)'],
           [list(i) for i in itens], [2.4, 3.3, 5.6, 6.6], tam=8.2, col_tipo=0)

saida1 = AQUI / 'Alteracoes_Relatorio_v1_para_v2.docx'
doc.save(saida1); print('ok', saida1)

# ============================================================================= 2. ENTREGÁVEIS DA FASE 2
DESCR = {  # caminho relativo a fase2/ → descrição (ordem = ordem da árvore)
    'POSTECH - Tech Challenge - Fase 2.pdf': 'Enunciado oficial da Fase 2',
    'EVOLUCAO_FASE2.md': 'Guia do grupo: entregáveis, decisões, divisão da revisão',
    'PLANO_FASE2.md': 'Plano, backlog e log de sessões',
    'Relatorio_Executivo_Fase2_Olist_RASCUNHO.pdf': '**ENTREGÁVEL 1** · relatório v2.0 (rascunho)',
    'Relatorio_Executivo_Fase2_Olist_RASCUNHO.docx': 'Mesmo relatório em Word (para comentários)',
    'Relatorio_Executivo_Fase2_Olist_FINAL.pdf': '**ENTREGÁVEL 1** · versão final (gerada com o link do vídeo)',
    'RELATORIO_EXECUTIVO_FASE2.md': 'Fonte do relatório (editar aqui)',
    'gerar_relatorio.py': 'Gera o .docx/.pdf do relatório',
    'config_relatorio.json': 'Links (vídeo, GitHub) e equipe',
    'Alteracoes_Relatorio_v1_para_v2.docx': 'O que mudou da v1.0 para a v2.0',
    'Entregaveis_Fase2.docx': 'Este documento',
    'gerar_docs_apoio.py': 'Gera os dois documentos de apoio',
    'NUMEROS_OFICIAIS.md': 'Fonte única de números (gerada pelo notebook 08)',
    'dados/numeros_fase2.json': 'Os mesmos números em JSON',
    'img/': 'Gráficos do relatório (gerados pelo notebook 08)',
    'fluxos/': '**ENTREGÁVEL 3** · fluxos PNG + gerar_fluxos.py',
    'prompts/PROMPTS_V2.md': '**ENTREGÁVEL 4** · prompts completos + 10 casos reais',
    'prompts/VALIDACAO_LUCAS.md': 'Critérios e 22 cenários de validação dos prompts',
    'prompts/exemplos/casos_reais.json': 'Casos reais usados nos exemplos',
    'video/ROTEIRO_VIDEO_FASE2.md': '**ENTREGÁVEL 5** · roteiro com falas e tempos',
    'video/Apresentacao_Fase2_Olist.pptx': '**ENTREGÁVEL 5** · slides de apoio (falas nas notas)',
    'video/gerar_slides.py': 'Aplica ajustes e falas sobre o modelo da apresentação',
    'video/ajustes_v5.json': 'Ajustes de texto aplicados aos slides',
    'video/modelos/Apresentacao_Fase2_Olist_V5_BASE.pptx': 'Modelo visual da apresentação',
}

ENTREGAVEIS = [
    ('1. Evolução do Relatório Executivo', 'Evoluir o relatório da Fase 1 (sem recomeçar), demonstrar evolução, 15–30 págs.',
     [('Histórico do Documento', 'Histórico do Documento'), ('Marcas "atualizado/novo" em cada seção', '1. Sumário Executivo')],
     ['fase2/Relatorio_Executivo_Fase2_Olist_RASCUNHO.pdf', 'fase2/RELATORIO_EXECUTIVO_FASE2.md']),
    ('2. Detalhamento dos Casos de Uso', '≥ 3 agentes com a) objetivo, b) problema, c) usuários, d) dados, e) entradas/saídas, f) indicadores',
     [('8.1 LogiPredict', '8.1 LogiPredict'), ('8.2 SentimentDesk', '8.2 SentimentDesk'), ('8.3 WinBack', '8.3 WinBack'), ('5.3 Priorização (por que estes 3)', '5.3 Priorização dos agentes')],
     ['fase2/RELATORIO_EXECUTIVO_FASE2.md (Seção 8)']),
    ('3. Jornada de Funcionamento dos Agentes', 'Fluxos com gatilhos, entradas, decisões, ações, interação humana e saída',
     [('9.1 a 9.3 Fluxos', '9.1 LogiPredict'), ('9.4 Jornada multiagente', '9.4 Jornada multiagente'), ('9.6 Exceções', '9.6 Tratamento de exceções')],
     ['fase2/fluxos/fluxo_logipredict.png', 'fase2/fluxos/fluxo_sentimentdesk.png', 'fase2/fluxos/fluxo_winback.png', 'fase2/fluxos/jornada_multiagente.png']),
    ('4. Estruturação Inicial de Prompts', 'a) objetivo, b) contexto, c) instrução principal, d) resultado esperado',
     [('10.1 a 10.3 Prompts com exemplo real', '10. Prompts Estruturados')],
     ['fase2/prompts/PROMPTS_V2.md', 'fase2/prompts/VALIDACAO_LUCAS.md', 'fase2/prompts/exemplos/casos_reais.json']),
    ('5. Vídeo Executivo (≤ 5 min)', 'Evolução, agentes, fluxos, funcionamento e exemplos de interação; link no relatório',
     [('Link na capa e no Sumário', '1. Sumário Executivo')],
     ['fase2/video/ROTEIRO_VIDEO_FASE2.md', 'fase2/video/Apresentacao_Fase2_Olist.pptx', 'fase2/config_relatorio.json (LINK_VIDEO)']),
]
APOIO = [
    ('Cadeia de evidência (racional dos achados)', '4.5 Da evidência à decisão', 'notebooks/08_fase2_evidencias_business_case.ipynb'),
    ('Fonte única de números', '15. Fontes do Projeto', 'fase2/NUMEROS_OFICIAIS.md'),
    ('Business case e metas do piloto', '13.3 Business case', 'notebooks/08_fase2_evidencias_business_case.ipynb'),
    ('Memória de cálculo (conta passo a passo)', '13.4 Memória de cálculo', 'fase2/RELATORIO_EXECUTIVO_FASE2.md (Seção 13.4)'),
    ('Governança e humano no loop', '11.4 Quem decide', 'fase2/RELATORIO_EXECUTIVO_FASE2.md (Seção 11)'),
    ('Validação dos prompts (22 cenários)', '10. Prompts Estruturados', 'fase2/prompts/VALIDACAO_LUCAS.md'),
    ('Rastreabilidade dos requisitos', 'Apêndice A', 'fase2/RELATORIO_EXECUTIVO_FASE2.md (Apêndice A)'),
]

doc = novo_doc('Tech Challenge · Fase 2 · Entregáveis e onde encontrá-los')
doc.add_heading('Entregáveis da Fase 2: onde encontrar cada item', 1)
par(doc, f'Documento de apoio ao grupo. Para cada entregável do enunciado: a seção e a **página** no relatório (fase2/{PDF.name}, {len(PAGINAS_V2)} páginas) e o **arquivo** no repositório.', 9.5, CINZA)

doc.add_heading('1. Entregáveis do enunciado', 2)
linhas = []
for nome, req, secoes, arqs in ENTREGAVEIS:
    onde = '\n'.join(f'{s} · pág. {pagina(t)}' for s, t in secoes)
    linhas.append([f'**{nome}**', req, onde, '\n'.join(arqs)])
tabela(doc, ['Entregável', 'O que o enunciado pede', 'Onde no relatório', 'Arquivo(s) no repositório'], linhas, [3.3, 4.6, 4.3, 5.7], tam=8.2, mono_col=3)

doc.add_heading('2. Itens de apoio (diferenciais)', 2)
tabela(doc, ['Item', 'Onde no relatório', 'Arquivo'],
       [[i, f'{s} · pág. {pagina(s)}', a] for i, s, a in APOIO], [5, 5, 7.9], tam=8.5, mono_col=2)

doc.add_heading('3. Árvore de arquivos da Fase 2', 2)
existentes = {p.relative_to(AQUI).as_posix() for p in AQUI.rglob('*') if p.is_file()}
linhas_arvore = ['tech-challenge-fiap-agentes-ia/',
                 '├── fase1/                                  Fase 1 entregue (não alterar)',
                 '├── fase2/']
itens = [k for k in DESCR if k.endswith('/') or k in existentes]
for k, item in enumerate(itens):
    ramo = '└──' if k == len(itens) - 1 else '├──'
    desc = DESCR[item].replace('**', '')
    linhas_arvore.append(f'│   {ramo} {item:<46} {desc}')
linhas_arvore += ['├── notebooks/',
                  '│   ├── 08_fase2_evidencias_business_case.ipynb   Evidências, priorização, business case',
                  '│   └── build_notebook_08.py                        Gera/executa o notebook 08',
                  '└── data/olist/                                     Dataset (fora do Git)']
t = doc.add_table(rows=1, cols=1); t.style = 'Table Grid'
c = t.cell(0, 0); sombrear(c, 'F4F4F2'); c.text = ''
for k, ln in enumerate(linhas_arvore):
    p = c.paragraphs[0] if k == 0 else c.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    r = p.add_run(ln); r.font.name = 'Consolas'; r.font.size = Pt(6.8)
    r._r.rPr.rFonts.set(qn('w:hAnsi'), 'Consolas')
par(doc, '', depois=2)
par(doc, 'Arquivos marcados como ENTREGÁVEL são os que respondem diretamente ao enunciado. O PDF FINAL aparece na árvore somente depois de gerado (com o link do vídeo).', 8.5, CINZA, italico=True)

saida2 = AQUI / 'Entregaveis_Fase2.docx'
doc.save(saida2); print('ok', saida2)
