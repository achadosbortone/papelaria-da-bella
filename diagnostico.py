#!/usr/bin/env python3
"""Testa como o Mercado Livre responde ao seu app e mostra o resultado de cada consulta.

Como usar: coloque este arquivo na mesma pasta do atualizar.bat e de um duplo clique.
Ele le suas chaves do atualizar.bat (ou das variaveis ML_CLIENT_ID e ML_CLIENT_SECRET).
Nenhuma chave e mostrada na tela nem salva no resultado.
"""
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(errors="replace")
except Exception:  # noqa: BLE001
    pass

BASE = Path(__file__).parent
API = "https://api.mercadolibre.com"
saida = []


def p(texto=""):
    print(texto)
    saida.append(texto)


def ler_chaves():
    cid, secret = os.environ.get("ML_CLIENT_ID", ""), os.environ.get("ML_CLIENT_SECRET", "")
    bat = BASE / "atualizar.bat"
    if (not cid or not secret) and bat.exists():
        txt = bat.read_text(encoding="utf-8", errors="ignore")
        m1 = re.search(r"^\s*set\s+ML_CLIENT_ID=(.*)$", txt, re.M | re.I)
        m2 = re.search(r"^\s*set\s+ML_CLIENT_SECRET=(.*)$", txt, re.M | re.I)
        cid = cid or (m1.group(1).strip() if m1 else "")
        secret = secret or (m2.group(1).strip() if m2 else "")
    return cid, secret


def chamar(metodo, url, headers=None, dados=None):
    """Devolve (codigo, texto). Nunca levanta erro."""
    req = urllib.request.Request(url, data=dados, method=metodo,
                                 headers={"User-Agent": "achados-som-diagnostico/1.0", **(headers or {})})
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:  # noqa: BLE001
        return None, f"falha de conexao: {e}"


def resumo(texto, n=220):
    return re.sub(r"\s+", " ", texto)[:n]


def teste(titulo, metodo, caminho, token=None, dados=None, extra_headers=None):
    headers = dict(extra_headers or {})
    if token:
        headers["Authorization"] = f"Bearer {token}"
    codigo, corpo = chamar(metodo, API + caminho, headers, dados)
    p(f"[{titulo}]")
    p(f"  consulta: {metodo} {caminho}" + ("  (com token)" if token else "  (sem token)"))
    p(f"  resposta: {codigo}")
    p(f"  trecho:   {resumo(corpo)}")
    p()
    return codigo, corpo


def main():
    p("DIAGNOSTICO DO MERCADO LIVRE")
    p("=" * 60)
    cid, secret = ler_chaves()
    p(f"Chaves encontradas: ID={'sim' if cid and 'COLE_AQUI' not in cid else 'NAO'}, "
      f"SECRET={'sim' if secret and 'COLE_AQUI' not in secret else 'NAO'}")
    p(f"Tamanho do ID: {len(cid)} caracteres | Tamanho do SECRET: {len(secret)} caracteres")
    p()

    teste("1. Conexao basica (publica)", "GET", "/sites/MLB")

    token = None
    if cid and secret and "COLE_AQUI" not in cid and "COLE_AQUI" not in secret:
        corpo = urllib.parse.urlencode({"grant_type": "client_credentials", "client_id": cid,
                                        "client_secret": secret}).encode()
        codigo, texto = chamar("POST", API + "/oauth/token",
                               {"Content-Type": "application/x-www-form-urlencoded", "Accept": "application/json"}, corpo)
        p("[2. Token do app]")
        p(f"  resposta: {codigo}")
        try:
            d = json.loads(texto)
            if d.get("access_token"):
                token = d["access_token"]
                p("  resultado: token obtido com sucesso")
                p(f"  escopo: {d.get('scope')} | validade (s): {d.get('expires_in')}")
            else:
                p("  resultado: SEM token. Mensagem: " + resumo(texto))
        except Exception:  # noqa: BLE001
            p("  resultado: resposta inesperada: " + resumo(texto))
        p()
    else:
        p("[2. Token do app]\n  PULADO: chaves nao preenchidas no atualizar.bat\n")

    cod, corpo = teste("3. Busca de produtos (sem token)", "GET", "/sites/MLB/search?q=microfone&limit=3")
    cod2, corpo2 = teste("4. Busca de produtos (com token)", "GET", "/sites/MLB/search?q=microfone&limit=3", token)
    codc, corpoc = teste("5. Busca no catalogo (com token)", "GET",
                         "/products/search?status=active&site_id=MLB&q=microfone&limit=3", token)

    item_id = None
    for texto in (corpo2, corpo):
        try:
            res = json.loads(texto).get("results") or []
            if res and res[0].get("id"):
                item_id = res[0]["id"]
                r0 = res[0]
                p(f"Campos do 1o resultado da busca: preco={r0.get('price')}, preco_original={r0.get('original_price')}, "
                  f"loja_oficial={r0.get('official_store_id')}, "
                  f"reputacao={((r0.get('seller') or {}).get('seller_reputation') or {}).get('power_seller_status')}")
                p()
                break
        except Exception:  # noqa: BLE001
            pass

    if item_id:
        teste("6. Dados de um item", "GET", f"/items/{item_id}", token)
        teste("7. Avaliacoes de um item", "GET", f"/reviews/item/{item_id}", token)
    else:
        p("[6 e 7] PULADOS: nenhuma busca devolveu itens para testar.\n")

    teste("8. Categorias (publica)", "GET", "/sites/MLB/categories")

    p("=" * 60)
    p("FIM. Copie TODO o texto desta janela e cole na conversa.")
    try:
        (BASE / "diagnostico.txt").write_text("\n".join(saida), encoding="utf-8")
        p("(Uma copia foi salva em diagnostico.txt, na mesma pasta.)")
    except Exception:  # noqa: BLE001
        pass
    try:
        input("\nPressione Enter para fechar...")
    except EOFError:
        pass


if __name__ == "__main__":
    main()
