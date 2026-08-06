# 🖼️ Planejamento de Diagramas — Prompts para Geração de Imagem

> Arquivo de apoio interno com os prompts prontos para uso em ferramentas de IA generativa.  
> Objetivo: gerar imagens profissionais dos diagramas do sistema multi-agente para o vídeo executivo e apresentações.  
> **Não é um entregável oficial** — serve como guia de produção visual do grupo.

---

## 📐 Diagrama 1 — Arquitetura do Sistema Multi-Agente

**Quando usar:** Slide de arquitetura, relatório executivo, thumbnail do vídeo.  
**Estilo alvo:** Isométrico, infográfico corporativo, dark mode, neon.

**Comentários sobre as escolhas de design:**  
Optou-se por um estilo *clean* focado em infraestrutura corporativa (isométrico ou infográfico de tecnologia), que comunica profissionalismo. O fundo escuro (Dark Mode) traz modernidade, enquanto o esquema de cores vibrantes separa logicamente os agentes por função.

### 🇺🇸 Versão em Inglês (recomendada — melhor performance nos modelos)

```text
A professional, high-end isometric technology architecture diagram showing a Multi-Agent AI system. At the center is a glowing core labeled "Executive Orchestrator Agent", with data streams connecting to 5 surrounding specialized nodes: "Anti-Churn", "Predictive Logistics", "Review Analysis", "Seller Success", and "Smart Pricing". Each node is represented by a sleek, minimalist futuristic server icon or geometric shape with neon accents. Tech infographic style, dark mode background with deep navy and subtle grid lines. The connection lines are glowing fiber optic cables (cyan, purple, and orange). Clean layout, corporate tech aesthetic, hyper-detailed, 8k resolution, UI/UX concept art. --ar 16:9 --stylize 250 --v 6.0
```

### 🇧🇷 Versão em Português

```text
Um diagrama de arquitetura de tecnologia isométrico, profissional e de alto padrão, mostrando um sistema de Inteligência Artificial Multi-Agente. No centro há um núcleo brilhante representando o "Agente Orquestrador Executivo", com fluxos de dados conectando a 5 nós especializados ao redor: "Anti-Churn", "Logística Preditiva", "Análise de Reviews", "Sucesso do Vendedor" e "Precificação Inteligente". Cada nó é representado por um ícone de servidor futurista minimalista ou forma geométrica com detalhes em neon. Estilo infográfico de tecnologia, fundo em modo escuro com azul-marinho profundo e linhas de grade sutis. As linhas de conexão brilham como cabos de fibra ótica (ciano, roxo e laranja). Layout limpo, estética corporativa de tecnologia, hiper detalhado, resolução 8k, arte conceitual UI/UX.
```

### ⚙️ Parâmetros recomendados (Midjourney)

| Parâmetro | Valor | Por quê |
|-----------|-------|---------|
| `--ar` | `16:9` | Proporção ideal para slides (PowerPoint/Keynote/Google Slides) |
| `--stylize` | `250` | Estilo artístico e refinado sem distorcer o aspecto técnico |
| `--v` | `6.0` | Versão mais recente e detalhada do Midjourney |

---

## 🗺️ Diagrama 2 — Mapa de Interação entre Agentes

**Quando usar:** Slide de mapa de agentes, documentação técnica para engenheiros.  
**Estilo alvo:** Blueprint digital, mind map, wireframe com nós e setas.

**Comentários sobre as escolhas de design:**  
Este prompt busca gerar um visual estilo *Blueprint* ou *Mind Map* digital. As representações são circulares (nós) conectados por vetores ou setas direcionalizadas, transmitindo chamadas de função, RAG (recuperação de dados) e chamadas a APIs.

### 🇺🇸 Versão em Inglês (recomendada)

```text
A digital blueprint-style interaction map diagram of a Multi-Agent AI ecosystem for an e-commerce platform. A complex, dynamic web of connections showing AI agents communicating with databases and APIs. Nodes are labeled as 'Orchestrator', 'NLP Agent', 'Predictive Agent', and 'Pricing Agent', interconnected with glowing dashed arrows and data packets. Included in the background are faint symbols of databases (SQL), document files (RAG), and gear icons (Tools). Cybernetic aesthetic, wireframe elements, dark blue and electric green color palette. Flat vector graphic style mixed with subtle 3D depth, highly professional, clean vector lines, data flow concept, UI dashboard layout. --ar 16:9 --style raw --v 6.0
```

### 🇧🇷 Versão em Português

```text
Um diagrama de mapa de interação estilo blueprint digital de um ecossistema de Inteligência Artificial Multi-Agente para uma plataforma de e-commerce. Uma teia dinâmica e complexa de conexões mostrando agentes de IA se comunicando com bancos de dados e APIs. Os nós estão interconectados com setas tracejadas brilhantes e pacotes de dados fluindo. No fundo, há símbolos sutis de bancos de dados (SQL), arquivos de documentos (RAG) e ícones de engrenagens (Ferramentas). Estética cibernética, elementos wireframe, paleta de cores azul escuro e verde elétrico. Estilo gráfico vetorial plano misturado com profundidade 3D sutil, design altamente profissional, linhas vetoriais limpas, conceito de fluxo de dados, layout de painel UI.
```

### ⚙️ Parâmetros recomendados (Midjourney)

| Parâmetro | Valor | Por quê |
|-----------|-------|---------|
| `--ar` | `16:9` | Proporção ideal para slides |
| `--style` | `raw` | Diminui floreios "fantasiosos", resultado mais sóbrio e técnico |
| `--v` | `6.0` | Versão mais recente |

> 💡 **Dica:** Se o modelo gerar algo muito realista (cabos físicos reais em vez de linhas gráficas), adicione `flat design` ou `vector art` ao prompt.

---

## 🔧 Ferramentas compatíveis

| Ferramenta | Observações |
|------------|-------------|
| **Midjourney v6** | Melhor qualidade geral para diagramas estilizados. Use os parâmetros `--ar`, `--stylize` e `--v` |
| **DALL-E 3** (ChatGPT) | Sem suporte a parâmetros — use o prompt em português diretamente na conversa |
| **Stable Diffusion** | Requer configuração de LoRA para estilo isométrico; mais controle técnico |
| **Adobe Firefly** | Boa opção para integrar direto ao fluxo de produção no Adobe |

---

## 📁 Onde salvar as imagens geradas

Salvar em `docs/assets/` com nomenclatura padronizada:

```
docs/assets/
├── diagrama_arquitetura_v1.png
├── diagrama_mapa_agentes_v1.png
└── ...
```
