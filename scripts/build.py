#!/usr/bin/env python3
"""Uso: python3 build.py roteiro.json saida.html [formato]
formato opcional (9:16, 4:5 ou 1:1) sobrescreve o campo "formato" do roteiro.
Valida o roteiro e injeta no motor (assets/template.html)."""
import json, re, sys, pathlib

def erro(m): sys.exit("ERRO: " + m)

def main():
    if len(sys.argv) < 3: erro("uso: build.py roteiro.json saida.html")
    r = json.load(open(sys.argv[1], encoding="utf-8"))
    if len(sys.argv) > 3: r["formato"] = sys.argv[3]
    for k in ("titulo", "categorias", "passos", "fechamento", "cta"):
        if k not in r: erro("campo faltando: " + k)
    if r.get("tema", "tecnico") not in ("tecnico", "papel", "neon"): erro("tema deve ser tecnico, papel ou neon")
    if r.get("formato", "9:16") not in ("9:16", "4:5", "1:1"): erro("formato deve ser 9:16, 4:5 ou 1:1")
    if not 2 <= len(r["passos"]) <= 8: erro("use de 2 a 8 passos")
    for i, p in enumerate(r["passos"], 1):
        for k in ("cat", "titulo", "texto", "fluxo"):
            if k not in p: erro(f"passo {i}: falta '{k}'")
        if not 0 <= p["cat"] < len(r["categorias"]): erro(f"passo {i}: 'cat' fora das categorias")
        n = len(p["fluxo"])
        if not 2 <= n <= 4: erro(f"passo {i}: fluxo precisa de 2 a 4 caixas")
        if len(p["titulo"]) > 32: print(f"aviso: passo {i}: título longo ({len(p['titulo'])} letras)")
        if len(p["texto"]) > 120: print(f"aviso: passo {i}: texto longo ({len(p['texto'])} letras)")
        for nd in p["fluxo"]:
            if len(nd["t"]) > 36: print(f"aviso: passo {i}: caixa longa '{nd['t']}'")
            if nd.get("k") not in (None, "ok", "bad", "q"): erro(f"passo {i}: 'k' deve ser ok, bad ou q")
        lp = p.get("loop")
        if lp and not (0 <= lp["de"] < n and 0 <= lp["para"] < n and lp["de"] != lp["para"]): erro(f"passo {i}: loop com índices inválidos")
    tpl = (pathlib.Path(__file__).parent.parent / "assets" / "template.html").read_text(encoding="utf-8")
    dados = "/*ROTEIRO_INICIO*/" + json.dumps(r, ensure_ascii=False) + "/*ROTEIRO_FIM*/"
    out, n = re.subn(r"/\*ROTEIRO_INICIO\*/.*?/\*ROTEIRO_FIM\*/", lambda m: dados, tpl, flags=re.S)
    if n != 1: erro("marcadores do roteiro não encontrados no template")
    pathlib.Path(sys.argv[2]).write_text(out, encoding="utf-8")
    print("OK:", sys.argv[2], "-", len(r["passos"]), "passos")

main()
