---
name: animafluxo
description: Cria vídeos animados (9:16, 4:5 ou 1:1) que explicam processos como fluxos de sistema, com cards, caixas ligadas por setas, loops e transições. Use quando o usuário pedir vídeo animado, vídeo explicativo, passo a passo animado, post em vídeo para LinkedIn/Instagram/reels ou "animação de fluxo". Gera um arquivo HTML que o usuário abre no Chrome/Edge e exporta como vídeo.
---

# AnimaFluxo

Você só escreve um **roteiro JSON**. O motor (`assets/template.html`) faz a animação e o navegador exporta o vídeo. Não gere imagens nem screenshots (gasta tokens à toa).

## Passos
1. Descubra o assunto. Se faltar algo, pergunte no máximo uma vez: assunto, formato (9:16 para reels/stories, 4:5 para feed do Instagram/LinkedIn, 1:1 quadrado), quantidade de passos (4 a 6), tema visual e chamada final. Se o usuário disser "decide você", use os padrões.
2. Escreva o roteiro em `roteiro.json` seguindo o esquema abaixo. Use palavras próprias; nunca copie frases de posts de terceiros.
3. Rode: `python3 <pasta-da-skill>/scripts/build.py roteiro.json video.html` (opcional: terceiro argumento `4:5` ou `1:1` para trocar o formato sem editar o JSON)
4. Corrija os avisos do script (textos longos) e rode de novo.
5. Diga ao usuário: abra `video.html` no Chrome ou Edge, confira, clique em **Exportar vídeo** e não troque de aba durante a gravação (~50 s).

## Esquema
```json
{"arquivo":"nome-do-arquivo","formato":"9:16|4:5|1:1","titulo":"...","subtitulo":"...","tema":"tecnico|papel|neon",
 "categorias":["Antes","Durante","Depois"],
 "passos":[{"cat":0,"titulo":"até 32 letras","texto":"até 120 letras",
   "fluxo":[{"t":"caixa","k":"ok|bad|q (opcional)"}],
   "loop":{"de":2,"para":1,"rotulo":"não: volta"},
   "bloqueio":"aviso em vermelho (opcional)"}],
 "fechamento":"frase final","cta":"chamada para comentar","autor":""}
```
- `formato`: 9:16 e 4:5 desenham o fluxo na vertical; 1:1 desenha na horizontal (use caixas de até 24 letras nesse formato).
- `fluxo`: 2 a 4 caixas, texto curto (até 36 letras). `k:"q"` é decisão (borda tracejada), `ok` verde, `bad` vermelho.
- `loop`: seta de retorno entre duas caixas (índices começam em 0).
- `cat`: índice em `categorias`; cada categoria ganha uma cor.
- 4 a 6 passos dão um vídeo de 35 a 50 segundos.

Exemplo completo: `exemplos/seguranca-ia.json`.

## Limites
Sem áudio (narração e trilha se adicionam em um editor). Se o navegador só gravar WebM, converta no CapCut.
