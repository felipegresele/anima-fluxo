# AnimaFluxo

Skill para o Claude que transforma um roteiro em **vídeo animado de fluxo de sistema**: cards com título e explicação, caixas ligadas por setas, decisões, loops de retorno, avisos de bloqueio e transições de câmera entre os passos.

O Claude escreve apenas um **roteiro em JSON**. Um motor próprio, feito com `canvas`, anima o roteiro, e o próprio navegador exporta o vídeo. Não há dependências, não há servidor e não há biblioteca externa.

> Exemplo incluído: "Estagiário rápido, revisor atento", sobre como programar com IA sem criar código inseguro.

---

## Sumário

- [O que ele faz](#o-que-ele-faz)
- [Exemplos](#exemplos)
- [Como funciona](#como-funciona)
- [Estrutura do projeto](#estrutura-do-projeto)
- [Requisitos](#requisitos)
- [Instalação como skill](#instalação-como-skill)
- [Como usar](#como-usar)
- [Uso manual, sem Claude](#uso-manual-sem-claude)
- [Exportar o vídeo](#exportar-o-vídeo)
- [Formatos](#formatos)
- [Temas visuais](#temas-visuais)
- [Esquema do roteiro (JSON)](#esquema-do-roteiro-json)
- [Limites recomendados de texto](#limites-recomendados-de-texto)
- [Linha do tempo do vídeo](#linha-do-tempo-do-vídeo)
- [Limitações](#limitações)
- [Solução de problemas](#solução-de-problemas)
- [Créditos e licença](#créditos-e-licença)

---

## O que ele faz

- Gera um vídeo de **35 a 60 segundos** a partir de 2 a 8 passos.
- Cada passo vira um card com **categoria colorida**, **título**, **texto curto** e um **mini fluxo** que se monta em sequência.
- Suporta **decisões** (caixa tracejada), **etapas aprovadas** (verde), **bloqueios** (vermelho) e **loops de retorno** ("não: volta e tenta de novo").
- Mostra uma **barra de progresso** no topo e faz a câmera **deslizar** de um passo para o outro.
- Exporta em **MP4** (ou WebM, conforme o navegador), sem programa extra.

## Exemplos

### Quadros gerados pela AnimaFluxo

Mesmo roteiro (`exemplos/seguranca-ia.json`), nos três formatos:

| 9:16 (passo 5) | 4:5 (passo 3) | 1:1 (passo 3) |
|---|---|---|
| ![9:16](docs/animafluxo-9x16-passo5.png) | ![4:5](docs/animafluxo-4x5-passo3.png) | ![1:1](docs/animafluxo-1x1-passo3.png) |

### Referência visual: vídeo "mito × verdade"

Estes dois quadros são de um vídeo feito antes, em formato 1:1 e estilo noturno, com a skill [video-animado-skill](https://github.com/eduardo-toste/video-animado-skill) (não com a AnimaFluxo). Ficam aqui como **referência do estilo de conteúdo** que inspirou o projeto: cada card compara o que as pessoas acreditam com o que de fato acontece.

| Mito 1 | Mito 2 |
|---|---|
| ![Mito 1](docs/referencia-mito-1.png) | ![Mito 2](docs/referencia-mito-2.png) |

> A AnimaFluxo desenha **fluxos** (caixas, setas, decisões e loops). O layout "mito × verdade" em duas colunas ainda não existe nela.

---

## Como funciona

```
Você descreve o assunto
        │
        ▼
Claude escreve o roteiro.json   ← só texto, poucos tokens
        │
        ▼
scripts/build.py valida o JSON e injeta no assets/template.html
        │
        ▼
video.html  (player com o vídeo dentro)
        │
        ▼
Chrome/Edge abre o HTML → botão "Exportar vídeo" → .mp4 / .webm
```

A animação é desenhada quadro a quadro em um `<canvas>`. A exportação grava esse canvas em tempo real com a API `MediaRecorder` do navegador. Por isso a exportação **não gasta tokens** do Claude.

## Estrutura do projeto

```
animafluxo/
├── SKILL.md                  # instruções que o Claude lê (a skill em si)
├── README.md                 # este arquivo
├── assets/
│   └── template.html         # motor de animação (canvas + exportação)
├── scripts/
│   └── build.py              # valida o roteiro e gera o HTML final
├── exemplos/
│   └── seguranca-ia.json     # roteiro de exemplo completo
└── docs/                     # imagens usadas neste README
```

## Requisitos

| Item | Para quê |
|---|---|
| **Python 3** | rodar o `build.py` (sem bibliotecas extras) |
| **Chrome ou Edge** atualizado | abrir o vídeo e exportar |
| **Claude** (claude.ai ou Claude Code) | opcional: escrever o roteiro por você |

Firefox e Safari podem reproduzir o vídeo, mas a exportação foi pensada para Chrome e Edge.

---

## Instalação como skill

### No Claude Code

1. Copie a pasta do projeto para o diretório de skills:

   ```bash
   mkdir -p ~/.claude/skills/animafluxo
   cp -r . ~/.claude/skills/animafluxo
   ```

   Rode o comando de dentro da pasta `animafluxo`. No Windows, `~` equivale a `C:\Users\SEU_USUARIO`.

2. Confira se o arquivo ficou no lugar certo:

   ```bash
   ls ~/.claude/skills/animafluxo/SKILL.md
   ```

3. **Reinicie o Claude Code** (`/exit` e `claude`). As skills só são carregadas na abertura.
4. Digite `/` e confirme que `animafluxo` aparece na lista.

Para usar a skill só em um projeto, copie para `.claude/skills/animafluxo` dentro da pasta dele.

### No claude.ai (web, desktop e app)

1. Compacte a pasta `animafluxo` em um `.zip` (a pasta deve ficar na raiz do zip, com o `SKILL.md` dentro dela).
2. Vá em **Configurações → Skills**.
3. Envie o `.zip` (ou o arquivo `.skill`) e ative a skill.
4. Deixe a opção de **execução de código e criação de arquivos** ligada, porque o Claude precisa rodar o `build.py`.

---

## Como usar

Depois de instalada, peça o vídeo em linguagem normal ou chame a skill pelo nome:

```
/animafluxo
Assunto: 4 hábitos para revisar código gerado por IA
Formato: 4:5
Estilo: papel
Passos: 4
Chamada final: comentar
Não gere screenshots nem prévia.
```

O Claude vai:

1. perguntar o que faltar (no máximo uma vez);
2. escrever o `roteiro.json`;
3. rodar o `build.py`;
4. entregar o `video.html`.

Depois, abra o HTML no Chrome ou Edge e [exporte o vídeo](#exportar-o-vídeo).

### Ficha de briefing (para pular as perguntas)

```
/animafluxo
Assunto: [tema do vídeo]
Formato: 9:16 | 4:5 | 1:1
Estilo: tecnico | papel | neon
Passos: [4 a 6]
Público: [quem vai assistir]
Chamada final: [ex.: comentar]
Pontos obrigatórios: [o que precisa aparecer]
Não gere screenshots nem prévia.
```

### Ajustes depois de gerado

Peça tudo em uma mensagem só, por exemplo:

> "Troque para o estilo neon, mude para 1:1 e encurte o texto do passo 3."

---

## Uso manual, sem Claude

Você pode escrever o roteiro à mão e gerar o vídeo sem gastar nada:

```bash
python3 scripts/build.py exemplos/seguranca-ia.json video.html
```

Para trocar o formato sem editar o JSON, passe um terceiro argumento:

```bash
python3 scripts/build.py exemplos/seguranca-ia.json video-quadrado.html 1:1
python3 scripts/build.py exemplos/seguranca-ia.json video-feed.html 4:5
```

O script valida o roteiro e mostra avisos de texto longo. Se houver erro, ele diz qual passo e qual campo corrigir.

---

## Exportar o vídeo

1. Abra o `.html` gerado no **Chrome ou Edge** (dois cliques ou arrastar para o navegador).
2. Clique em **▶ Reproduzir** para conferir.
3. Clique em **⬇ Exportar vídeo**.
4. **Deixe a aba aberta e visível** até aparecer "Pronto! Arquivo salvo".
5. O arquivo vai para a pasta de downloads, com o nome definido em `"arquivo"` no roteiro.

O formato do arquivo depende do navegador: **MP4** quando houver suporte, **WebM** quando não houver. Um WebM pode ser convertido em qualquer editor (CapCut, DaVinci, HandBrake) ou com `ffmpeg -i video.webm video.mp4`.

### Modo gravação

O botão **⏺ Modo gravação** esconde os controles e toca o vídeo do zero em tela cheia. Use esse modo se quiser gravar a tela com outro programa (por exemplo, **Win + G** no Windows). Pressione **Esc** para sair.

---

## Formatos

| Formato | Resolução | Uso | Layout do fluxo |
|---|---|---|---|
| `9:16` | 1080 × 1920 | reels, stories, shorts | caixas na vertical |
| `4:5` | 1080 × 1350 | feed do Instagram e LinkedIn | caixas na vertical, tamanhos reduzidos |
| `1:1` | 1080 × 1080 | quadrado | caixas na horizontal, loop embaixo |

No formato `1:1` as caixas ficam lado a lado, então use textos de até **24 letras** nelas.

## Temas visuais

| Tema | Visual |
|---|---|
| `tecnico` | fundo azul-marinho com grade, destaques em azul, roxo e verde |
| `papel` | fundo bege claro, destaques em azul, laranja e verde |
| `neon` | fundo quase preto, destaques em rosa, amarelo e turquesa |

Cada categoria do roteiro recebe uma das três cores do tema.

---

## Esquema do roteiro (JSON)

```json
{
  "arquivo": "nome-do-video",
  "formato": "9:16",
  "tema": "tecnico",
  "titulo": "Título da abertura",
  "subtitulo": "Frase de apoio da abertura",
  "categorias": ["Antes", "Durante", "Depois"],
  "passos": [
    {
      "cat": 0,
      "titulo": "Faça o briefing",
      "texto": "Explicação curta do passo.",
      "fluxo": [
        { "t": "Você" },
        { "t": "Briefing claro" },
        { "t": "IA" }
      ],
      "bloqueio": "Aviso em vermelho (opcional)"
    },
    {
      "cat": 1,
      "titulo": "Leia antes de aceitar",
      "texto": "Se não consegue explicar, ainda não é seu.",
      "fluxo": [
        { "t": "Trecho recebido" },
        { "t": "Você lê" },
        { "t": "Entendi tudo?", "k": "q" },
        { "t": "Aceita", "k": "ok" }
      ],
      "loop": { "de": 2, "para": 1, "rotulo": "não: pede explicação" }
    }
  ],
  "fechamento": "Frase final em destaque.",
  "cta": "Chamada para o público comentar.",
  "autor": "@seuusuario (opcional)"
}
```

### Campos

| Campo | Obrigatório | Descrição |
|---|---|---|
| `arquivo` | não | nome do arquivo exportado (padrão: `video`) |
| `formato` | não | `9:16` (padrão), `4:5` ou `1:1` |
| `tema` | não | `tecnico` (padrão), `papel` ou `neon` |
| `titulo` | sim | título da abertura |
| `subtitulo` | não | frase de apoio da abertura |
| `categorias` | sim | lista de categorias (cada uma ganha uma cor) |
| `passos` | sim | de 2 a 8 passos |
| `fechamento` | sim | frase final em destaque |
| `cta` | sim | chamada para ação no cartão final |
| `autor` | não | assinatura no canto da cena final |

### Campos de cada passo

| Campo | Obrigatório | Descrição |
|---|---|---|
| `cat` | sim | índice da categoria (começa em 0) |
| `titulo` | sim | título do card |
| `texto` | sim | explicação curta |
| `fluxo` | sim | de 2 a 4 caixas |
| `fluxo[].t` | sim | texto da caixa |
| `fluxo[].k` | não | tipo da caixa: `ok` (verde), `bad` (vermelho) ou `q` (decisão, borda tracejada) |
| `loop` | não | seta de retorno: `de` e `para` são índices de caixas (começam em 0), `rotulo` é o texto da seta |
| `bloqueio` | não | faixa vermelha com um aviso, desenhada abaixo do fluxo |

## Limites recomendados de texto

O `build.py` mostra um aviso quando você passa destes valores:

| Campo | Limite |
|---|---|
| `titulo` do passo | 32 letras |
| `texto` do passo | 120 letras |
| caixa do fluxo | 36 letras (24 no formato 1:1) |

## Linha do tempo do vídeo

| Cena | Duração |
|---|---|
| Abertura | 3,2 s |
| Cada passo | 7 s |
| Fechamento | 4,6 s |

Exemplo: 6 passos resultam em cerca de 50 segundos. As transições entre cenas duram 0,7 s.

---

## Limitações

- **Não tem áudio.** Narração e trilha entram depois, em um editor de vídeo.
- A exportação roda **em tempo real** (um vídeo de 50 s leva cerca de 50 s para exportar).
- Se você **trocar de aba** ou minimizar o navegador durante a gravação, o vídeo pode sair com falhas.
- A fonte é a do sistema (Segoe UI, Arial ou equivalente), então o visual muda um pouco entre computadores.
- Máximo de 4 caixas por passo e 8 passos por vídeo.

## Solução de problemas

| Problema | O que fazer |
|---|---|
| A skill não aparece em `/` | Confira se o arquivo está em `~/.claude/skills/animafluxo/SKILL.md` (sem pasta extra no meio) e reinicie o Claude Code |
| `build.py` mostra "campo faltando" | Preencha o campo indicado na mensagem de erro |
| `build.py` mostra aviso de texto longo | Encurte o texto indicado; o vídeo ainda é gerado, mas pode ficar apertado |
| Botão "Exportar" avisa que não há suporte | Use Chrome ou Edge atualizado |
| O vídeo exportado travou ou tem cortes | Não troque de aba durante a exportação, ou use o Modo gravação |
| O arquivo saiu em `.webm` | Converta com `ffmpeg -i video.webm video.mp4` ou importe no CapCut |
| Texto cortado dentro da caixa | Encurte o texto da caixa ou use menos caixas no passo |

---

**Licença:** escolha uma (por exemplo, MIT) e adicione um arquivo `LICENSE` na raiz do projeto. Sem licença, o código não pode ser reutilizado por terceiros.