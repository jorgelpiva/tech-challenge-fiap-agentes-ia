"""Gera os fluxos (swimlanes) dos agentes da Fase 2 em PNG.

Uso (na raiz do repo):  python fase2/fluxos/gerar_fluxos.py
Cada fluxo é declarado como dados (raias, nós, arestas): para alterar um texto
ou uma decisão, edite a definição e rode de novo.

Legenda fixa: gatilho (cinza escuro) · ação do agente (cor do agente) ·
decisão (losango amarelo) · humano no loop (borda laranja) · saída (verde).
"""
from pathlib import Path
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, Rectangle

OUT = Path(__file__).resolve().parent
INK, INK2, LANE_BG, LANE_LINE = '#0b0b0b', '#52514e', '#f6f6f4', '#dddcd6'
COR = {
    'gatilho': ('#3b3a37', 'white'),
    'decisao': ('#fdf0cf', INK),
    'humano':  ('#fde6dc', INK),
    'saida':   ('#dcf2e8', INK),
}
DEC_BORDA, HUM_BORDA, SAI_BORDA = '#eda100', '#eb6834', '#1baf7a'
AGENTE = {'LogiPredict': ('#2a78d6', '#dbe8f9'), 'SentimentDesk': ('#6250d6', '#e4e0f8'), 'WinBack': ('#008300', '#dcefdc')}

CW, LH = 2.05, 1.55          # largura da coluna, altura da raia
NW, NH = 1.78, 0.98          # tamanho do nó
DW, DH = 1.90, 1.30          # tamanho do losango


def desenhar(nome, titulo, agente, raias, nos, arestas, ncols, subtitulo=''):
    cor_ag, fundo_ag = AGENTE[agente]
    L = len(raias)
    largura = 1.25 + ncols * CW
    fig, ax = plt.subplots(figsize=(largura * 0.98, L * LH * 0.98 + 0.9))
    ax.set_xlim(0, largura); ax.set_ylim(-0.15, L * LH + 0.75); ax.axis('off')
    ax.text(0.02, L * LH + 0.5, titulo, fontsize=13, fontweight='bold', color=INK, va='center')
    if subtitulo:
        ax.text(0.02, L * LH + 0.15, subtitulo, fontsize=9, color=INK2, va='center')

    # raias
    for i, r in enumerate(raias):
        y0 = (L - 1 - i) * LH
        ax.add_patch(Rectangle((0, y0), largura, LH, facecolor=LANE_BG if i % 2 == 0 else 'white', edgecolor=LANE_LINE, lw=0.8))
        ax.add_patch(Rectangle((0, y0), 1.1, LH, facecolor=cor_ag if r == 'Agente' else '#ecebe6', edgecolor=LANE_LINE, lw=0.8))
        rot = agente if r == 'Agente' else r
        ax.text(0.55, y0 + LH / 2, rot, ha='center', va='center', fontsize=10 if len(rot) <= 11 else 8.4, fontweight='bold',
                color='white' if r == 'Agente' else INK2, wrap=True)

    pos = {}
    for n in nos:
        nid, raia, col, tipo, texto = n
        i = raias.index(raia)
        cx, cy = 1.25 + col * CW + CW / 2 - 0.05, (L - 1 - i) * LH + LH / 2
        pos[nid] = (cx, cy, tipo)
        if tipo == 'decisao':
            w, h = DW / 2, DH / 2
            ax.add_patch(Polygon([(cx, cy + h), (cx + w, cy), (cx, cy - h), (cx - w, cy)], closed=True,
                                 facecolor=COR['decisao'][0], edgecolor=DEC_BORDA, lw=1.6, zorder=3))
            ax.text(cx, cy, texto, ha='center', va='center', fontsize=8.6, color=INK, zorder=4, linespacing=1.12)
            continue
        if tipo == 'agente':
            fc, tc, ec, lw = fundo_ag, INK, cor_ag, 1.3
        elif tipo == 'humano':
            fc, tc, ec, lw = COR['humano'][0], INK, HUM_BORDA, 2.2
        elif tipo == 'saida':
            fc, tc, ec, lw = COR['saida'][0], INK, SAI_BORDA, 1.3
        elif tipo == 'fim':
            fc, tc, ec, lw = 'white', INK2, LANE_LINE, 1.0
        else:
            fc, tc, ec, lw = COR['gatilho'][0], 'white', COR['gatilho'][0], 1.0
        ax.add_patch(FancyBboxPatch((cx - NW / 2, cy - NH / 2), NW, NH, boxstyle='round,pad=0.02,rounding_size=0.12',
                                    facecolor=fc, edgecolor=ec, lw=lw, zorder=3))
        prefixo = {'humano': 'HUMANO · ', 'gatilho': 'GATILHO · ', 'saida': 'SAÍDA · '}.get(tipo, '')
        if prefixo:
            ax.text(cx, cy + NH / 2 - 0.13, prefixo.strip(' ·'), ha='center', va='center', fontsize=6.8,
                    fontweight='bold', color=HUM_BORDA if tipo == 'humano' else (tc if tipo == 'gatilho' else '#11704d'), zorder=4)
            ax.text(cx, cy - 0.07, texto, ha='center', va='center', fontsize=8.5, color=tc, zorder=4, linespacing=1.15)
        else:
            ax.text(cx, cy, texto, ha='center', va='center', fontsize=8.6, color=tc, zorder=4, linespacing=1.15)

    def borda(nid, direcao):
        cx, cy, tipo = pos[nid]
        w = (DW if tipo == 'decisao' else NW) / 2
        h = (DH if tipo == 'decisao' else NH) / 2
        return {'d': (cx + w, cy), 'e': (cx - w, cy), 'c': (cx, cy + h), 'b': (cx, cy - h)}[direcao]

    for a in arestas:
        src, dst = a[0], a[1]
        rotulo = a[2] if len(a) > 2 else ''
        modo = a[3] if len(a) > 3 else 'auto'
        sx, sy, _ = pos[src]; tx, ty, _ = pos[dst]
        if modo == 'auto':
            modo = 'h' if abs(sy - ty) < 0.01 else ('v' if abs(sx - tx) < 0.01 else 'hv')
        if modo == 'h':
            p0 = borda(src, 'd' if tx > sx else 'e'); p1 = borda(dst, 'e' if tx > sx else 'd'); pts = [p0, p1]
        elif modo == 'v':
            p0 = borda(src, 'b' if ty < sy else 'c'); p1 = borda(dst, 'c' if ty < sy else 'b'); pts = [p0, p1]
        elif modo == 'hv':   # sai pela lateral, desce/sobe até o destino
            p0 = borda(src, 'd' if tx > sx else 'e'); p1 = borda(dst, 'c' if ty < sy else 'b'); pts = [p0, (p1[0], p0[1]), p1]
        else:                # 'vh': sai por cima/baixo, segue na horizontal até o destino
            p0 = borda(src, 'b' if ty < sy else 'c'); p1 = borda(dst, 'e' if tx > sx else 'd'); pts = [p0, (p0[0], p1[1]), p1]
        xs, ys = zip(*pts)
        ax.plot(xs[:-1] + (xs[-1],), ys[:-1] + (ys[-1],), color=INK2, lw=1.1, zorder=2)
        ax.annotate('', xy=pts[-1], xytext=pts[-2], arrowprops=dict(arrowstyle='-|>', color=INK2, lw=1.1, mutation_scale=11), zorder=2)
        if rotulo:
            mx, my = (pts[0][0] + pts[1][0]) / 2, (pts[0][1] + pts[1][1]) / 2
            ax.text(mx, my + 0.09, rotulo, ha='center', va='bottom', fontsize=8.4, color=INK, fontweight='bold',
                    bbox=dict(boxstyle='round,pad=0.12', fc='white', ec='none'), zorder=5)

    fig.tight_layout()
    fig.savefig(OUT / f'{nome}.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('ok', nome)


RAIAS = ['Gatilho', 'Agente', 'Humano', 'Saída']

# --------------------------------------------------------------------------- LogiPredict
desenhar('fluxo_logipredict', 'LogiPredict · Guardião do Prazo de Entrega', 'LogiPredict', RAIAS,
    nos=[
        ('t1', 'Gatilho', 0, 'gatilho', 'Pedido aprovado\nou evento de rastreio\n(varredura a cada 6h)'),
        ('a1', 'Agente', 0, 'agente', 'Calcula risco de atraso\n(postagem, UF destino,\nrota, histórico seller)'),
        ('d1', 'Agente', 1, 'decisao', 'Seller vai estourar\no limite de\npostagem (24h)?'),
        ('a2', 'Saída', 1, 'saida', 'Lembrete ao seller\n+ ocorrência registrada'),
        ('d2', 'Agente', 2, 'decisao', 'Risco de atraso\n≥ limiar?'),
        ('a3', 'Gatilho', 2, 'fim', 'Segue monitorando\n(sem ação)'),
        ('h1', 'Humano', 3, 'humano', 'Analista de Operações\naciona transportadora\n/ prioriza tratativa'),
        ('d3', 'Agente', 4, 'decisao', 'Nova data\nprevista após\no prazo?'),
        ('a4', 'Agente', 5, 'agente', 'Avisa cliente com\nnova data (template\naprovado)'),
        ('o1', 'Saída', 5, 'saida', 'Painel de risco por\nrota + sinal ao\nSentimentDesk'),
    ],
    arestas=[('t1', 'a1'), ('a1', 'd1'), ('d1', 'a2', 'sim'), ('d1', 'd2', 'não'), ('d2', 'a3', 'não'),
             ('d2', 'h1', 'sim'), ('h1', 'd3', '', 'hv'), ('d3', 'a4', 'sim'), ('a4', 'o1'), ('d3', 'a3', 'não', 'vh')],
    ncols=6, subtitulo='Escopo: só pedidos entre a aprovação e a entrega. Não negocia frete nem troca transportadora sozinho.')

# --------------------------------------------------------------------------- SentimentDesk
desenhar('fluxo_sentimentdesk', 'SentimentDesk · Triagem e Resposta de Avaliações Negativas', 'SentimentDesk', RAIAS,
    nos=[
        ('t1', 'Gatilho', 0, 'gatilho', 'Avaliação nota 1–3\npublicada (com ou\nsem comentário)'),
        ('a1', 'Agente', 0, 'agente', 'Classifica motivo\n(texto + dados do\npedido), severidade'),
        ('d1', 'Agente', 1, 'decisao', 'Confiança da\nclassificação\n≥ 80%?'),
        ('h0', 'Humano', 1, 'humano', 'Analista CX\nclassifica\nmanualmente'),
        ('d2', 'Agente', 2, 'decisao', 'Caso crítico?\n(Procon, fraude,\nnão recebido)'),
        ('h1', 'Humano', 3, 'humano', 'Analista CX revisa\nresposta e define\ncompensação (alçada)'),
        ('a2', 'Agente', 4, 'agente', 'Envia resposta\naprovada + abre ticket\nao responsável'),
        ('d3', 'Agente', 5, 'decisao', 'Motivo =\nentrega?'),
        ('o1', 'Saída', 5, 'saida', 'Sinal ao LogiPredict\n+ pausa no WinBack'),
        ('o2', 'Saída', 6, 'saida', 'Ticket ao seller +\ndashboard semanal\nde motivos'),
    ],
    arestas=[('t1', 'a1'), ('a1', 'd1'), ('d1', 'h0', 'não'), ('h0', 'h1'), ('d1', 'd2', 'sim'),
             ('d2', 'h1', 'sim', 'vh'), ('d2', 'a2', 'não'), ('h1', 'a2', '', 'hv'), ('a2', 'd3'), ('d3', 'o1', 'sim'), ('d3', 'o2', 'não', 'hv')],
    ncols=7, subtitulo='Escopo: só avaliações negativas/neutras. Não concede reembolso nem penaliza seller; responde e roteia.')

# --------------------------------------------------------------------------- WinBack
desenhar('fluxo_winback', 'WinBack · Conversão da 1ª para a 2ª Compra (janela de 90 dias)', 'WinBack', RAIAS,
    nos=[
        ('t1', 'Gatilho', 0, 'gatilho', '7 dias após a\nentrega do\n1º pedido'),
        ('d1', 'Agente', 0, 'decisao', 'Opt-in LGPD e\nsem contato nos\núltimos 15 dias?'),
        ('f1', 'Saída', 0, 'fim', 'Não contata\n(registra motivo)'),
        ('d2', 'Agente', 1, 'decisao', '1ª experiência\nnegativa? (nota ≤2,\natraso, ticket)'),
        ('a0', 'Saída', 1, 'saida', 'Pausa: aguarda\nresolução do\nSentimentDesk'),
        ('a1', 'Agente', 2, 'agente', 'Escolhe categoria,\nmomento e mensagem\n(grupo controle 10%)'),
        ('d3', 'Agente', 3, 'decisao', 'Incentivo acima\ndo teto (cupom\n> 10%)?'),
        ('h1', 'Humano', 3, 'humano', 'Gestor de CRM\naprova ou ajusta\na oferta'),
        ('a2', 'Agente', 4, 'agente', 'Dispara mensagem;\n2ª tentativa em D+45\n(máx. 2 contatos)'),
        ('o1', 'Saída', 5, 'saida', 'Relatório de uplift\nvs. grupo controle'),
    ],
    arestas=[('t1', 'd1'), ('d1', 'f1', 'não'), ('d1', 'd2', 'sim'), ('d2', 'a0', 'sim'), ('d2', 'a1', 'não'),
             ('a1', 'd3'), ('d3', 'h1', 'sim'), ('d3', 'a2', 'não'), ('h1', 'a2', '', 'hv'), ('a2', 'o1', '', 'hv')],
    ncols=6, subtitulo='Escopo: só clientes de 1ª compra, até 90 dias. Não reativa base inativa antiga nem cria campanhas de massa.')


# --------------------------------------------------------------------------- Jornada multiagente
def jornada():
    raias = ['Cliente', 'LogiPredict', 'SentimentDesk', 'WinBack', 'Humano']
    cores = {'LogiPredict': AGENTE['LogiPredict'], 'SentimentDesk': AGENTE['SentimentDesk'], 'WinBack': AGENTE['WinBack'],
             'Cliente': ('#3b3a37', '#ecebe6'), 'Humano': (HUM_BORDA, COR['humano'][0])}
    eventos = [  # (coluna, raia, dia, texto)
        (0, 'Cliente', 'D0', 'Compra\n(destino MA)'),
        (1, 'LogiPredict', 'D+6', 'Seller perto do\nlimite: lembrete'),
        (2, 'LogiPredict', 'D+11', 'Postou atrasado +\nrota MA: risco alto'),
        (2, 'Humano', 'D+11', 'Ops prioriza\ncom transportadora'),
        (3, 'Cliente', 'D+27', 'D-3: recebe aviso\ncom nova data (03/04)'),
        (4, 'Cliente', 'D+40', 'Entrega com\natraso; nota 1'),
        (5, 'SentimentDesk', 'D+40', 'Sem texto: motivo\ninferido = atraso;\nresposta + ticket'),
        (5, 'WinBack', 'D+40', 'Pausa oferta\n(experiência ruim)'),
        (6, 'Humano', 'D+41', 'CX aprova\ncupom de desculpas'),
        (7, 'WinBack', 'D+55', 'Oferta de 2ª compra\n(categoria afim)'),
    ]
    ncols = 8
    L = len(raias)
    largura = 1.25 + ncols * 1.75
    fig, ax = plt.subplots(figsize=(largura * 0.98, L * 1.05 + 1.1))
    ax.set_xlim(0, largura); ax.set_ylim(-0.55, L * 1.05 + 0.75); ax.axis('off')
    ax.text(0.02, L * 1.05 + 0.5, 'Jornada multiagente · "O pedido que ia atrasar"', fontsize=13, fontweight='bold', color=INK)
    ax.text(0.02, L * 1.05 + 0.15, 'Pedido real do dataset (MG → MA, postagem 4 dias após o limite, entregue 10 dias após o prazo). Linha do tempo com os agentes atuando.',
            fontsize=9, color=INK2)
    for i, r in enumerate(raias):
        y0 = (L - 1 - i) * 1.05
        ax.add_patch(Rectangle((0, y0), largura, 1.05, facecolor=LANE_BG if i % 2 == 0 else 'white', edgecolor=LANE_LINE, lw=0.8))
        ax.add_patch(Rectangle((0, y0), 1.1, 1.05, facecolor=cores[r][0], edgecolor=LANE_LINE, lw=0.8))
        ax.text(0.55, y0 + 0.525, r, ha='center', va='center', fontsize=9.5 if len(r) <= 11 else 8.2, fontweight='bold', color='white')
    prev = None
    for col, r, dia, txt in eventos:
        i = raias.index(r)
        cx, cy = 1.25 + col * 1.75 + 0.85, (L - 1 - i) * 1.05 + 0.525
        ec = cores[r][0]
        ax.add_patch(FancyBboxPatch((cx - 0.78, cy - 0.38), 1.56, 0.76, boxstyle='round,pad=0.02,rounding_size=0.1',
                                    facecolor=cores[r][1], edgecolor=ec, lw=2.0 if r == 'Humano' else 1.2, zorder=3))
        ax.text(cx, cy, txt, ha='center', va='center', fontsize=8.4, color=INK, zorder=4, linespacing=1.12)
        ax.text(cx, -0.35, dia, ha='center', va='center', fontsize=8, color=INK2, fontweight='bold')
        if prev is not None:
            px, py = prev
            if abs(px - cx) < 0.1:      # mesma coluna: seta vertical
                sgn = 1 if cy < py else -1
                pts = [(px, py - sgn * 0.38), (cx, cy + sgn * 0.38)]
            else:                       # cotovelo: sai pela direita, troca de raia no meio do vão
                xm = (px + 0.78 + cx - 0.78) / 2
                pts = [(px + 0.78, py), (xm, py), (xm, cy), (cx - 0.78, cy)]
            xs, ys = zip(*pts)
            ax.plot(xs, ys, color=INK2, lw=1, zorder=2)
            ax.annotate('', xy=pts[-1], xytext=pts[-2], arrowprops=dict(arrowstyle='-|>', color=INK2, lw=1, mutation_scale=10), zorder=2)
        prev = (cx, cy)
    fig.tight_layout()
    fig.savefig(OUT / 'jornada_multiagente.png', dpi=200, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print('ok jornada_multiagente')


jornada()
