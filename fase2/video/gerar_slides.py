"""Atualiza a apresentação V5 preservando o desenho original de Leonardo.

Uso: python fase2/video/gerar_slides.py [--output arquivo.pptx]
Usa somente a biblioteca padrão. Fonte visual: modelos/*_V5_BASE.pptx.
Textos pontuais: ajustes_v5.json. Notas: ROTEIRO_VIDEO_FASE2.md.
Não executar o gerador anterior, que recriava o desenho e as falas da v2.
"""
from pathlib import Path
import argparse, json, re, zipfile
import xml.etree.ElementTree as ET

AQUI = Path(__file__).resolve().parent
BASE = AQUI / 'modelos/Apresentacao_Fase2_Olist_V5_BASE.pptx'
NS = {'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',
      'p': 'http://schemas.openxmlformats.org/presentationml/2006/main'}
for prefix, uri in NS.items():
    ET.register_namespace(prefix, uri)
ET.register_namespace('r', 'http://schemas.openxmlformats.org/officeDocument/2006/relationships')

def falas():
    roteiro = (AQUI / 'ROTEIRO_VIDEO_FASE2.md').read_text(encoding='utf-8')
    padrao = r'### Slide (\d+) \| ([^\n]+)\n\n([\s\S]*?)(?=\n### Slide|\n## Bloco|\n---)'
    itens = re.findall(padrao, roteiro)
    if len(itens) != 12 or [int(i[0]) for i in itens] != list(range(1, 13)):
        raise ValueError('Roteiro precisa conter os slides1–12, uma fala por slide.')
    return {int(n): f"{('LEONARDO' if int(n)<=3 else 'JORGE' if int(n)<=6 else 'CAIO' if int(n)<=9 else 'LUCAS')} · Slide {n} · {titulo}\n\n{fala.strip()}"
            for n, titulo, fala in itens}

def xml_bytes(root):
    return ET.tostring(root, encoding='utf-8', xml_declaration=True)

def gerar(saida):
    ajustes = json.loads((AQUI / 'ajustes_v5.json').read_text(encoding='utf-8'))
    notas = falas()
    encontrados = {str(i): set() for i in (7,8,9)}
    with zipfile.ZipFile(BASE) as zin, zipfile.ZipFile(saida, 'w', zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = zin.read(item.filename)
            match = re.fullmatch(r'ppt/slides/slide(\d+)\.xml', item.filename)
            if match:
                numero = match[1]; root = ET.fromstring(data)
                for shape in root.findall('.//p:sp', NS):
                    ts = shape.findall('.//a:t', NS)
                    original = '\n'.join(''.join(x.itertext()) for x in shape.findall('.//a:p', NS))
                    if original in ajustes.get(numero, {}):
                        if len(ts) != 1:
                            raise ValueError(f'Texto dividido em runs, revisar edição: {original}')
                        ts[0].text = ajustes[numero][original]; encontrados[numero].add(original)
                    body = shape.find('.//a:bodyPr', NS)
                    if body is not None and original == original.upper() and len(original)<=30 and '\n' not in original:
                        body.set('wrap','none')
                    if original in ('DESCOBRIR','DESENHAR','ESCALAR'):
                        ext = shape.find('./p:spPr/a:xfrm/a:ext', NS)
                        if ext is not None: ext.set('cx',str(int(ext.get('cx')) + 24*9525))
                data = xml_bytes(root)
            match = re.fullmatch(r'ppt/notesSlides/notesSlide(\d+)\.xml', item.filename)
            if match:
                root = ET.fromstring(data); n = int(match[1]); found=False
                for shape in root.findall('.//p:sp', NS):
                    ph=shape.find('./p:nvSpPr/p:nvPr/p:ph', NS)
                    if ph is None or ph.get('type') != 'body': continue
                    tx=shape.find('p:txBody',NS)
                    if tx is None: continue
                    for par in list(tx.findall('a:p',NS)): tx.remove(par)
                    for line in notas[n].split('\n'):
                        par=ET.SubElement(tx,'{'+NS['a']+'}p')
                        run=ET.SubElement(par,'{'+NS['a']+'}r')
                        ET.SubElement(run,'{'+NS['a']+'}t').text=line
                    found=True
                if not found: raise ValueError(f'Notas sem placeholder body: {n}')
                data=xml_bytes(root)
            zout.writestr(item, data)
    for n, items in ajustes.items():
        if encontrados.get(n,set()) != set(items):
            raise ValueError(f'Ajuste não aplicado no slide{n}')
    print('OK:', saida, '12 slides, notas sincronizadas ao roteiro.')

if __name__ == '__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--output',type=Path,default=AQUI/'Apresentacao_Fase2_Olist.pptx')
    gerar(parser.parse_args().output)
