"""Gera o Relatório Executivo da Fase 2 (.docx e .pdf) a partir do Markdown.

Uso (na raiz do repo):  python fase2/gerar_relatorio.py
  - Fonte: fase2/RELATORIO_EXECUTIVO_FASE2.md
  - Links/equipe: fase2/config_relatorio.json
  - Sem LINK_VIDEO preenchido → gera *_RASCUNHO (com marca "RASCUNHO").
  - Com LINK_VIDEO → gera fase2/Relatorio_Executivo_Fase2_Olist_FINAL.(docx|pdf)
  - Ao final roda o QA: falha se sobrar placeholder, TODO etc. no texto.
PDF via Microsoft Word (docx2pdf).
"""
import json, re, sys
from pathlib import Path
from docx import Document
from docx.enum.section import WD_SECTION, WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

AQUI = Path(__file__).resolve().parent
ROOT = AQUI.parent
MD = AQUI / 'RELATORIO_EXECUTIVO_FASE2.md'
CFG = json.loads((AQUI / 'config_relatorio.json').read_text(encoding='utf-8'))
FINAL = bool(CFG.get('LINK_VIDEO'))
SAIDA = (AQUI / 'Relatorio_Executivo_Fase2_Olist_FINAL') if FINAL else (AQUI / 'Relatorio_Executivo_Fase2_Olist_RASCUNHO')

AZUL_ESC = RGBColor(0x1F, 0x3A, 0x5F)
AZUL = RGBColor(0x2A, 0x78, 0xD6)
CINZA = RGBColor(0x52, 0x51, 0x4E)
FUNDO_TAB, FUNDO_CALLOUT, FUNDO_CODE = 'E8EEF7', 'FDF3EC', 'F4F4F2'
LARG = {'util': Cm(21.59 - 2 * 1.8)}   # muda nas páginas em paisagem


# ----------------------------------------------------------------------------- utilitários
def sombrear(celula, cor):
    tcPr = celula._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd'); shd.set(qn('w:val'), 'clear'); shd.set(qn('w:color'), 'auto'); shd.set(qn('w:fill'), cor)
    tcPr.append(shd)


def bordas_tabela(tabela, cor='C9CED6', esp=4):
    tblPr = tabela._tbl.tblPr
    b = OxmlElement('w:tblBorders')
    for lado in ('top', 'left', 'bottom', 'right', 'insideH', 'insideV'):
        e = OxmlElement(f'w:{lado}'); e.set(qn('w:val'), 'single'); e.set(qn('w:sz'), str(esp)); e.set(qn('w:color'), cor)
        b.append(e)
    tblPr.append(b)


def margens_celula(tabela, cm=0.12):
    tblPr = tabela._tbl.tblPr
    m = OxmlElement('w:tblCellMar')
    for lado in ('top', 'bottom', 'left', 'right'):
        e = OxmlElement(f'w:{lado}'); e.set(qn('w:w'), str(int(cm * 567))); e.set(qn('w:type'), 'dxa'); m.append(e)
    tblPr.append(m)


def repetir_cabecalho(linha):
    trPr = linha._tr.get_or_add_trPr()
    e = OxmlElement('w:tblHeader'); e.set(qn('w:val'), 'true'); trPr.append(e)


def nao_quebrar_linha(linha):
    trPr = linha._tr.get_or_add_trPr()
    e = OxmlElement('w:cantSplit'); e.set(qn('w:val'), 'true'); trPr.append(e)


def substituir(texto):
    for k, v in CFG.items():
        if isinstance(v, str):
            texto = texto.replace('{{' + k + '}}', v if v else '[link do vídeo pendente]')
    return texto


INLINE = re.compile(r'(\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`|https?://\S+)')


def runs(par, texto, tam=None, cor=None, negrito=False):
    texto = substituir(texto)
    for parte in INLINE.split(texto):
        if not parte:
            continue
        if parte.startswith('**'):
            r = par.add_run(parte[2:-2]); r.bold = True
        elif parte.startswith('*') and len(parte) > 2:
            r = par.add_run(parte[1:-1]); r.italic = True
        elif parte.startswith('`'):
            r = par.add_run(parte[1:-1]); r.font.name = 'Consolas'; r.font.size = Pt((tam or 10) - 1)
            r.font.color.rgb = AZUL_ESC
            continue
        elif parte.startswith('http'):
            fim = ''
            while parte and parte[-1] in '.,;)':
                fim = parte[-1] + fim; parte = parte[:-1]
            hyperlink(par, parte, parte, tam)
            if fim:
                par.add_run(fim)
            continue
        else:
            r = par.add_run(parte)
        if negrito:
            r.bold = True
        if tam:
            r.font.size = Pt(tam)
        if cor is not None:
            r.font.color.rgb = cor


def hyperlink(par, url, texto, tam=None):
    rid = par.part.relate_to(url, 'http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink', is_external=True)
    h = OxmlElement('w:hyperlink'); h.set(qn('r:id'), rid)
    r = OxmlElement('w:r'); rPr = OxmlElement('w:rPr')
    c = OxmlElement('w:color'); c.set(qn('w:val'), '2A78D6'); rPr.append(c)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    if tam:
        s = OxmlElement('w:sz'); s.set(qn('w:val'), str(int(tam * 2))); rPr.append(s)
    r.append(rPr); t = OxmlElement('w:t'); t.text = texto; t.set(qn('xml:space'), 'preserve'); r.append(t); h.append(r)
    par._p.append(h)


def campo_pagina(par):
    r = par.add_run()
    for tipo, txt in (('begin', None), (None, 'PAGE'), ('end', None)):
        if tipo:
            f = OxmlElement('w:fldChar'); f.set(qn('w:fldCharType'), tipo); r._r.append(f)
        else:
            it = OxmlElement('w:instrText'); it.set(qn('xml:space'), 'preserve'); it.text = txt; r._r.append(it)


# ----------------------------------------------------------------------------- documento
doc = Document()
st = doc.styles['Normal']; st.font.name = 'Calibri'; st.font.size = Pt(10)
st.element.rPr.rFonts.set(qn('w:eastAsia'), 'Calibri')
st.paragraph_format.space_after = Pt(5); st.paragraph_format.line_spacing = 1.12
for nome, tam, cor, antes in (('Heading 1', 17, AZUL_ESC, 0), ('Heading 2', 12.5, AZUL, 10), ('Heading 3', 11, AZUL_ESC, 8)):
    h = doc.styles[nome]; h.font.name = 'Calibri'; h.font.size = Pt(tam); h.font.bold = True; h.font.color.rgb = cor
    h.paragraph_format.space_before = Pt(antes); h.paragraph_format.space_after = Pt(6); h.paragraph_format.keep_with_next = True

sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.59), Cm(27.94)
for lado in ('left_margin', 'right_margin'):
    setattr(sec, lado, Cm(1.8))
sec.top_margin, sec.bottom_margin = Cm(1.7), Cm(1.6)
sec.different_first_page_header_footer = True

cab = sec.header.paragraphs[0]
runs(cab, 'FIAP · Tech Challenge Agentic AI · Fase 2' + ('' if FINAL else '   ·   RASCUNHO, NÃO SUBMETER'), tam=8, cor=CINZA)
rod = sec.footer.paragraphs[0]; rod.alignment = WD_ALIGN_PARAGRAPH.RIGHT
runs(rod, 'Olist Intelligent Marketplace · Relatório Executivo   |   ', tam=8, cor=CINZA); campo_pagina(rod)

# ---- capa
def p(texto='', tam=10, cor=None, negrito=False, alinh=None, depois=None, antes=None):
    par = doc.add_paragraph()
    if texto:
        runs(par, texto, tam=tam, cor=cor, negrito=negrito)
    if alinh is not None:
        par.alignment = alinh
    if depois is not None:
        par.paragraph_format.space_after = Pt(depois)
    if antes is not None:
        par.paragraph_format.space_before = Pt(antes)
    return par

p('TECH CHALLENGE · FASE 2', 13, AZUL, True, antes=60)
p('Olist Intelligent Marketplace', 28, AZUL_ESC, True, depois=2)
p('Do diagnóstico à operação: como os agentes de IA vão funcionar na Olist', 16, CINZA, depois=26)
p('Relatório Executivo · evolução do relatório da Fase 1', 11, None, True)
p('Pós-graduação em IA Agêntica · FIAP', 10)
p('Base: Brazilian E-Commerce Public Dataset by Olist (2016–2018) · 99.441 pedidos · R$ 16 milhões', 10)
p(f"Versão {'final' if FINAL else 'rascunho para revisão do grupo'} · {CFG['DATA_VERSAO']}", 10, CINZA, depois=26)
p('Equipe', 10, None, True, depois=2)
for m in CFG['EQUIPE']:
    p(m, 9, depois=1)
p('Pergunta da Fase 2', 10, None, True, antes=22, depois=2)
p('“Como os agentes de IA irão interagir com usuários, dados e processos da Olist para gerar valor real ao negócio?”', 12, AZUL_ESC)
lk = p('', antes=18, depois=1); runs(lk, 'Vídeo executivo (Fase 2): ', tam=9, negrito=True); runs(lk, '{{LINK_VIDEO}}', tam=9)
lk = p('', depois=1); runs(lk, 'Repositório: ', tam=9, negrito=True); runs(lk, '{{LINK_GITHUB}}', tam=9)
doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)

# ---- corpo a partir do Markdown
linhas = MD.read_text(encoding='utf-8').splitlines()
i, primeiro_h1 = 0, True
lista_num = 0


def tabela_md(bloco):
    lin = [l.strip().strip('|').split('|') for l in bloco if not re.match(r'^\s*\|?\s*:?-{2,}', l)]
    lin = [[c.strip() for c in l] for l in lin]
    ncol = len(lin[0])
    t = doc.add_table(rows=len(lin), cols=ncol)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordas_tabela(t); margens_celula(t)
    tam = 8.5 if ncol <= 4 else (7.8 if ncol <= 6 else 7.2)
    # larguras: 1ª coluna mais estreita quando é rótulo curto
    comp = [max(len(re.sub(r'[*`]', '', l[j])) if j < len(l) else 0 for l in lin) for j in range(ncol)]
    comp = [min(max(c, 6), 60) for c in comp]
    tot = sum(comp)
    for j in range(ncol):
        for cel in t.columns[j].cells:
            cel.width = int(LARG['util'] * comp[j] / tot)
    for r, l in enumerate(lin):
        if r == 0:
            repetir_cabecalho(t.rows[0])
        nao_quebrar_linha(t.rows[r])
        for j in range(ncol):
            cel = t.cell(r, j); cel.text = ''
            par = cel.paragraphs[0]; par.paragraph_format.space_after = Pt(0); par.paragraph_format.line_spacing = 1.0
            runs(par, l[j] if j < len(l) else '', tam=tam, negrito=(r == 0), cor=AZUL_ESC if r == 0 else None)
            if r == 0:
                sombrear(cel, FUNDO_TAB)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


def caixa(texto_ou_linhas, fundo, mono=False):
    t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER
    bordas_tabela(t, cor='E0DED8' if mono else 'F2C6AE', esp=4); margens_celula(t, 0.2)
    cel = t.cell(0, 0); cel.width = LARG['util']; sombrear(cel, fundo)
    cel.text = ''
    linhas_c = texto_ou_linhas if isinstance(texto_ou_linhas, list) else [texto_ou_linhas]
    for k, tx in enumerate(linhas_c):
        par = cel.paragraphs[0] if k == 0 else cel.add_paragraph()
        par.paragraph_format.space_after = Pt(0 if mono else 3); par.paragraph_format.line_spacing = 1.0
        if mono:
            r = par.add_run(tx if tx else ' '); r.font.name = 'Consolas'; r.font.size = Pt(7.6)
            r._r.rPr.rFonts.set(qn('w:hAnsi'), 'Consolas')
        else:
            runs(par, tx, tam=9.5)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)


while i < len(linhas):
    l = linhas[i]; s = l.strip()
    if s in ('<!-- paisagem -->', '<!-- retrato -->'):
        paisagem = 'paisagem' in s
        nova = doc.add_section(WD_SECTION.NEW_PAGE)
        nova.orientation = WD_ORIENT.LANDSCAPE if paisagem else WD_ORIENT.PORTRAIT
        nova.page_width, nova.page_height = (Cm(27.94), Cm(21.59)) if paisagem else (Cm(21.59), Cm(27.94))
        nova.left_margin = nova.right_margin = Cm(1.8)
        nova.top_margin, nova.bottom_margin = Cm(1.4), Cm(1.3)
        nova.different_first_page_header_footer = False
        LARG['util'] = nova.page_width - Cm(3.6)
        i += 1; continue
    if s.startswith('<!--') and 'pagebreak' not in s:
        while '-->' not in linhas[i]:
            i += 1
        i += 1; continue
    if 'pagebreak' in s:
        doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE); i += 1; continue
    if not s:
        lista_num = 0; i += 1; continue
    if s.startswith('# '):
        doc.add_heading(substituir(s[2:]), level=1); i += 1; continue
    if s.startswith('## '):
        doc.add_heading(substituir(s[3:]), level=2); i += 1; continue
    if s.startswith('### '):
        doc.add_heading(substituir(s[4:]), level=3); i += 1; continue
    if s.startswith('|'):
        bloco = []
        while i < len(linhas) and linhas[i].strip().startswith('|'):
            bloco.append(linhas[i]); i += 1
        tabela_md(bloco); continue
    if s.startswith('```'):
        i += 1; bloco = []
        while not linhas[i].strip().startswith('```'):
            bloco.append(linhas[i]); i += 1
        i += 1; caixa(bloco, FUNDO_CODE, mono=True); continue
    if s.startswith('>'):
        bloco = []
        while i < len(linhas) and linhas[i].strip().startswith('>'):
            bloco.append(linhas[i].strip()[1:].strip()); i += 1
        caixa([b for b in bloco if b], FUNDO_CALLOUT); continue
    m = re.match(r'!\[(.*)\]\((.*)\)', s)
    if m:
        cap, cam = m.groups()
        par = doc.add_paragraph(); par.alignment = WD_ALIGN_PARAGRAPH.CENTER; par.paragraph_format.keep_with_next = True
        larg_img = LARG['util'] if LARG['util'] < Cm(20) else Cm(23.5)
        par.add_run().add_picture(str(AQUI / cam), width=larg_img)
        c = doc.add_paragraph(); c.alignment = WD_ALIGN_PARAGRAPH.CENTER
        runs(c, cap, tam=8.5, cor=CINZA); c.runs[0].italic = True
        i += 1; continue
    if re.match(r'^[-*] ', s):
        par = doc.add_paragraph(style='List Bullet'); runs(par, s[2:]); par.paragraph_format.space_after = Pt(2)
        i += 1; continue
    mn = re.match(r'^(\d+)\. (.*)', s)
    if mn:
        par = doc.add_paragraph(style='List Number'); runs(par, mn.group(2)); par.paragraph_format.space_after = Pt(2)
        i += 1; continue
    # parágrafo (junta linhas consecutivas terminadas sem quebra de bloco)
    par = doc.add_paragraph(); runs(par, s); i += 1

docx_path = SAIDA.with_suffix('.docx')
doc.save(docx_path)
print('DOCX:', docx_path)

from docx2pdf import convert
convert(str(docx_path), str(SAIDA.with_suffix('.pdf')))
print('PDF :', SAIDA.with_suffix('.pdf'))

# ----------------------------------------------------------------------------- QA automático
import pymupdf
pdf = pymupdf.open(SAIDA.with_suffix('.pdf'))
texto = '\n'.join(pg.get_text() for pg in pdf)
proibidos = ['INSERIR', 'TODO', 'XXX', '{{', 'antes da submissão', 'deve ser conferid', 'Lorem']
if FINAL:
    proibidos += ['pendente', 'RASCUNHO']
achados = [w for w in proibidos if (w in texto if w.isupper() else w.lower() in texto.lower())]
print(f'Páginas: {len(pdf)}  (meta do enunciado: 15–30)')
print('QA placeholders:', 'OK' if not achados else f'ATENÇÃO → {achados}')
if not FINAL:
    print('Modo RASCUNHO: preencha LINK_VIDEO em fase2/config_relatorio.json para gerar a versão FINAL.')
