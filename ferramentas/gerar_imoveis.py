"""Gera os dados sintéticos da "Aurora Imóveis" usados nos encontros 3 a 6.

Tudo aqui é fictício: imobiliárias, anúncios, preços, CEPs e endereços. Os bairros são
bairros reais de Porto Alegre, mas as "zonas" são um agrupamento didático simplificado e os
preços por m² são inventados (não use estes números para nada além da aula).

Saídas (relativas à raiz do repositório):

  aula3/pratica/imoveis/            mini-site de 60 anúncios (5 páginas + 60 fichas), sitemap e robots
  aula4/imoveis_aurora.csv          base completa exportada pela imobiliária (300 linhas, com sujeira)
  aula6/imoveis_aurora.csv          a mesma base (cópia, para o encontro 6 ser autocontido)
  aula6/casa_sul.json               segunda fonte, outro esquema, 80 anúncios (15 em comum)
  aula6/bairros_poa.csv             tabela de referência bairro -> zona -> cidade

Uso:  python ferramentas/gerar_imoveis.py   (determinístico: semente fixa)
"""
from __future__ import annotations

import csv
import html
import json
import os
import random
import unicodedata
from datetime import date, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL_BASE = "https://lucaskup.github.io/pucrs-coleta-e-preparacao"
rng = random.Random(20261029)

# bairro: (zona didática, preço base R$/m², faixa de CEP fictícia)
BAIRROS = {
    "Moinhos de Vento": ("Centro", 13000, 90570),
    "Bela Vista": ("Centro", 12000, 90450),
    "Petrópolis": ("Leste", 10000, 90460),
    "Rio Branco": ("Centro", 9500, 90420),
    "Bom Fim": ("Centro", 9000, 90035),
    "Menino Deus": ("Sul", 8500, 90130),
    "Cidade Baixa": ("Centro", 8000, 90050),
    "Jardim Lindóia": ("Norte", 7800, 91050),
    "Jardim Botânico": ("Leste", 7500, 90690),
    "Tristeza": ("Sul", 7500, 91920),
    "Passo d'Areia": ("Norte", 7000, 91350),
    "Ipanema": ("Sul", 7000, 91760),
    "Centro Histórico": ("Centro", 6500, 90010),
    "Cristal": ("Sul", 6500, 90820),
    "Partenon": ("Leste", 5000, 90610),
    "Sarandi": ("Norte", 4200, 91140),
}
CONSERVACAO = ["Precisa de reforma", "Regular", "Bom", "Ótimo"]
COMODIDADES = ["Piscina", "Academia", "Churrasqueira", "Salão de festas", "Playground",
               "Portaria 24h", "Elevador", "Sacada", "Bicicletário"]
RUAS = ["Rua das Acácias", "Rua dos Ipês", "Avenida das Palmeiras", "Rua do Mirante",
        "Rua Quatro Ventos", "Travessa da Aurora", "Rua dos Jacarandás", "Rua da Ponte Velha",
        "Avenida do Lago", "Rua Sete Estrelas", "Rua das Hortênsias", "Rua do Farol"]


def tirar_acento(s: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def slug(s: str) -> str:
    s = tirar_acento(s).lower()
    return "".join(c if c.isalnum() else "-" for c in s).strip("-").replace("--", "-")


def brl(v: float, casas: int = 0) -> str:
    txt = f"{v:,.{casas}f}"
    return "R$ " + txt.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar_imovel(i: int) -> dict:
    bairro = rng.choice(list(BAIRROS))
    zona, pm2, cep0 = BAIRROS[bairro]
    tipo = rng.choices(["Apartamento", "Casa", "Cobertura", "Studio"], [0.62, 0.18, 0.08, 0.12])[0]
    if tipo == "Studio":
        quartos, area = 1, rng.uniform(22, 40)
    elif tipo == "Apartamento":
        quartos = rng.choices([1, 2, 3, 4], [0.2, 0.45, 0.28, 0.07])[0]
        area = 28 + 24 * quartos + rng.gauss(0, 8)
    elif tipo == "Cobertura":
        quartos = rng.choice([3, 3, 4])
        area = 140 + 30 * (quartos - 3) + rng.uniform(0, 120)
    else:
        quartos = rng.choice([2, 3, 3, 4, 4, 5])
        area = 80 + 35 * quartos + rng.uniform(0, 90)
    area = round(area, 1) if rng.random() < 0.3 else round(area)
    banheiros = max(1, min(quartos + rng.choice([-1, 0, 0, 1]), 5))
    vagas = 0 if tipo == "Studio" and rng.random() < 0.7 else rng.choices([0, 1, 2, 3], [0.15, 0.5, 0.28, 0.07])[0]
    ano = rng.randint(1962, 2025)
    idade = 2026 - ano
    p = [0.05, 0.15, 0.45, 0.35] if idade < 15 else ([0.15, 0.35, 0.4, 0.1] if idade < 35 else [0.35, 0.4, 0.2, 0.05])
    cons = rng.choices(range(4), p)[0]
    fator_tipo = {"Apartamento": 1.0, "Casa": 0.85, "Cobertura": 1.25, "Studio": 1.15}[tipo]
    fator_cons = [0.78, 0.9, 1.0, 1.1][cons]
    preco = area * pm2 * fator_tipo * fator_cons * (1 + 0.04 * vagas) * rng.lognormvariate(0, 0.12)
    preco = round(preco / 1000) * 1000
    if tipo in ("Apartamento", "Studio"):
        andar = rng.randint(1, 18)
    elif tipo == "Cobertura":
        andar = rng.randint(6, 22)
    else:
        andar = None
    com = set()
    novo = idade < 20
    for c, pa, pc in [("Piscina", 0.35, 0.15), ("Academia", 0.4, 0.0), ("Churrasqueira", 0.6, 0.7),
                      ("Salão de festas", 0.55, 0.0), ("Playground", 0.4, 0.0), ("Portaria 24h", 0.45, 0.0),
                      ("Sacada", 0.55, 0.3), ("Bicicletário", 0.25, 0.0)]:
        prob = pa * (1.4 if novo else 0.7) if tipo != "Casa" else pc
        if rng.random() < min(prob, 0.95):
            com.add(c)
    if andar and andar > 3 and rng.random() < 0.9:
        com.add("Elevador")
    if tipo == "Casa":
        condominio = 0.0
    else:
        condominio = round(area * rng.uniform(7, 11) + 60 * len(com & {"Piscina", "Academia", "Portaria 24h"}), -1)
    iptu = round(preco * rng.uniform(0.0025, 0.0045), -1)
    pet = rng.random() < (0.85 if tipo == "Casa" else 0.6)
    anuncio = date(2026, 1, 5) + timedelta(days=rng.randint(0, 255))
    cep = cep0 * 1000 + rng.randint(0, 999)
    return {
        "codigo": f"AUR-{i:04d}", "tipo": tipo, "bairro": bairro, "zona": zona, "cep": cep,
        "endereco": f"{rng.choice(RUAS)}, {rng.randint(10, 2400)}",
        "preco": float(preco), "area_m2": float(area), "quartos": quartos, "banheiros": banheiros,
        "vagas": vagas, "condominio": condominio, "iptu_anual": iptu, "ano_construcao": ano,
        "andar": andar, "conservacao": CONSERVACAO[cons], "aceita_pet": "sim" if pet else "não",
        "comodidades": sorted(com), "data_anuncio": anuncio.isoformat(),
    }


IMOVEIS = [gerar_imovel(i) for i in range(1, 301)]

# --------------------------------------------------------------------------------------
# 1. Base exportada (aula 4 e 6): 300 linhas + 6 duplicatas, com sujeira deliberada
# --------------------------------------------------------------------------------------
SUJEIRA = []  # registro do que foi plantado, vai para o README


def exportar_base() -> list[dict]:
    linhas = []
    for im in IMOVEIS:
        r = dict(im)
        r["comodidades"] = ";".join(im["comodidades"])
        linhas.append(r)
    # condomínio ausente, mais frequente em prédios antigos (MAR: depende do ano, observado)
    aptos = [r for r in linhas if r["tipo"] != "Casa"]
    antigos = [r for r in aptos if r["ano_construcao"] < 1990]
    novos = [r for r in aptos if r["ano_construcao"] >= 1990]
    for r in rng.sample(antigos, min(12, len(antigos))) + rng.sample(novos, 3):
        r["condominio"] = None
    SUJEIRA.append("condominio vazio em 15 apartamentos (12 deles construídos antes de 1990: ausência MAR)")
    # ano desconhecido codificado como 0
    for r in rng.sample(linhas, 8):
        r["ano_construcao"] = 0
    SUJEIRA.append("ano_construcao = 0 em 8 linhas (sentinela de 'não informado')")
    # preço 'sob consulta'
    for r in rng.sample(linhas, 3):
        r["preco"] = None
    SUJEIRA.append("preco vazio em 3 linhas (anúncio 'sob consulta')")
    # erros de digitação
    alvo = rng.choice([r for r in linhas if r["tipo"] == "Apartamento" and r["preco"]])
    alvo["preco"] = alvo["preco"] * 10
    SUJEIRA.append(f"{alvo['codigo']}: preço multiplicado por 10 (zero a mais)")
    alvo = rng.choice([r for r in linhas if r["tipo"] == "Apartamento" and 60 < r["area_m2"] < 90])
    alvo["area_m2"] = alvo["area_m2"] * 10
    SUJEIRA.append(f"{alvo['codigo']}: área multiplicada por 10")
    alvo = rng.choice([r for r in linhas if r["tipo"] == "Studio"])
    alvo["area_m2"] = 3.2
    SUJEIRA.append(f"{alvo['codigo']}: área de 3,2 m² (impossível)")
    alvo = rng.choice([r for r in linhas if r["tipo"] == "Apartamento"])
    alvo["quartos"] = -2
    SUJEIRA.append(f"{alvo['codigo']}: quartos = -2 (valor inválido)")
    # categorias inconsistentes
    for r in rng.sample([r for r in linhas if r["conservacao"] == "Ótimo"], 4):
        r["conservacao"] = "otimo"
    for r in rng.sample([r for r in linhas if r["conservacao"] == "Bom"], 3):
        r["conservacao"] = "BOM"
    SUJEIRA.append("conservacao com grafias inconsistentes: 'otimo' (4) e 'BOM' (3)")
    for r in rng.sample([r for r in linhas if r["bairro"] == "Petrópolis"], 2):
        r["bairro"] = "Petropolis"
    SUJEIRA.append("bairro 'Petropolis' sem acento em 2 linhas")
    # duplicatas exatas (o mesmo anúncio exportado duas vezes)
    dup = rng.sample(linhas, 6)
    for r in dup:
        linhas.insert(rng.randint(0, len(linhas)), dict(r))
    SUJEIRA.append("6 linhas duplicadas por inteiro (mesmo codigo)")
    return linhas


BASE = exportar_base()
CAMPOS = ["codigo", "tipo", "bairro", "zona", "cep", "endereco", "preco", "area_m2", "quartos",
          "banheiros", "vagas", "condominio", "iptu_anual", "ano_construcao", "andar", "conservacao",
          "aceita_pet", "comodidades", "data_anuncio"]


def escrever_csv(caminho: str, linhas: list[dict]) -> None:
    os.makedirs(os.path.dirname(caminho), exist_ok=True)
    with open(caminho, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        w.writeheader()
        for r in linhas:
            w.writerow({k: ("" if r[k] is None else r[k]) for k in CAMPOS})


escrever_csv(os.path.join(RAIZ, "aula4", "imoveis_aurora.csv"), BASE)
escrever_csv(os.path.join(RAIZ, "aula6", "imoveis_aurora.csv"), BASE)

# --------------------------------------------------------------------------------------
# 2. Segunda fonte (aula 6): "Casa Sul Imóveis", JSON aninhado com outro esquema
# --------------------------------------------------------------------------------------
APELIDOS = {"Moinhos de Vento": "Moinhos", "Petrópolis": "Petropolis", "Cidade Baixa": "Cid. Baixa",
            "Centro Histórico": "Centro", "Passo d'Areia": "Passo da Areia",
            "Jardim Botânico": "Jd. Botânico", "Jardim Lindóia": "Jd. Lindóia"}


def logradouro_casa_sul(end: str) -> str:
    """O sistema da Casa Sul abrevia o tipo de logradouro, tira acentos e às vezes a vírgula."""
    for longo, curto in [("Rua ", "R. "), ("Avenida ", "Av. "), ("Travessa ", "Tv. ")]:
        if end.startswith(longo):
            end = curto + end[len(longo):]
    if rng.random() < 0.6:
        end = tirar_acento(end)
    if rng.random() < 0.5:
        end = end.replace(",", "")
    return end


def para_casa_sul(im: dict, ident: int) -> dict:
    bairro = APELIDOS.get(im["bairro"], im["bairro"]) if rng.random() < 0.8 else im["bairro"]
    d = date.fromisoformat(im["data_anuncio"]) + timedelta(days=rng.randint(-20, 20))
    return {
        "id": f"CS-{ident}",
        "titulo": f"{im['tipo']} {im['quartos']} dorm. - {bairro}",
        "_origem": im["codigo"],
        "endereco": {"logradouro": logradouro_casa_sul(im["endereco"]), "bairro": bairro, "cidade": "Porto Alegre", "uf": "RS"},
        "valor_mil": round(im["preco"] * rng.uniform(0.96, 1.05) / 1000, 1),
        "metragem": f"{im['area_m2']:.0f}m2",
        "dorms": im["quartos"],
        "vagas": im["vagas"],
        "condominio": None if im["tipo"] == "Casa" else brl(im["condominio"], 2),
        "conservacao": CONSERVACAO.index(im["conservacao"]) + 1,
        "pet": "S" if im["aceita_pet"] == "sim" else "N",
        "anunciado_em": d.strftime("%m/%d/%Y"),
        "comodidades": [tirar_acento(c).upper() for c in im["comodidades"]],
    }


comuns = rng.sample(IMOVEIS, 15)
so_casa_sul = [gerar_imovel(1000 + k) for k in range(65)]
casa_sul = [para_casa_sul(im, 100 + k) for k, im in enumerate(comuns + so_casa_sul)]
rng.shuffle(casa_sul)
for k, c in enumerate(casa_sul):
    c["id"] = f"CS-{101 + k}"
# uma ausência de valor e um conflito de unidade (valor em reais, não em mil)
casa_sul[7]["valor_mil"] = None
casa_sul[19]["valor_mil"] = casa_sul[19]["valor_mil"] * 1000 if casa_sul[19]["valor_mil"] else 450000.0
codigos_comuns = {im["codigo"] for im in comuns}
GABARITO_COMUNS = {c["_origem"]: c["id"] for c in casa_sul if c["_origem"] in codigos_comuns}
for c in casa_sul:
    del c["_origem"]
os.makedirs(os.path.join(RAIZ, "aula6"), exist_ok=True)
with open(os.path.join(RAIZ, "aula6", "casa_sul.json"), "w", encoding="utf-8") as f:
    json.dump({"fonte": "Casa Sul Imóveis (fictícia)", "gerado_em": "2026-10-01",
               "dicionario": {"valor_mil": "preço em milhares de reais",
                              "conservacao": "1 = precisa de reforma, 2 = regular, 3 = bom, 4 = ótimo",
                              "anunciado_em": "data no formato do sistema de origem"},
               "imoveis": casa_sul}, f, ensure_ascii=False, indent=2)

with open(os.path.join(RAIZ, "aula6", "bairros_poa.csv"), "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f)
    w.writerow(["bairro", "zona", "cidade", "uf"])
    for b, (z, _, _) in sorted(BAIRROS.items()):
        w.writerow([b, z, "Porto Alegre", "RS"])

# --------------------------------------------------------------------------------------
# 3. Mini-site (aula 3): os 60 primeiros anúncios, 12 por página
# --------------------------------------------------------------------------------------
SITE = os.path.join(RAIZ, "aula3", "pratica", "imoveis")
os.makedirs(os.path.join(SITE, "imovel"), exist_ok=True)
DESTAQUES = IMOVEIS[:60]
CONSULTE = {DESTAQUES[17]["codigo"], DESTAQUES[44]["codigo"]}  # preço "Consulte" no site

CSS = """
    :root { --fundo:#f5f6f8; --cartao:#fff; --texto:#1b1f24; --suave:#5a636e; --borda:#dfe3e8; --marca:#1d5c8c; }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) {
        --fundo:#14171b; --cartao:#1d2126; --texto:#eceff3; --suave:#a4adb8; --borda:#2c323a; --marca:#7fb8e6;
      }
    }
    * { box-sizing: border-box; }
    body { margin:0; background:var(--fundo); color:var(--texto); line-height:1.5;
           font-family: system-ui, -apple-system, "Segoe UI", Roboto, sans-serif; }
    .conteudo { max-width: 1000px; margin: 0 auto; padding: 2rem 1rem 4rem; }
    a { color: var(--marca); }
    h1 { font-size: 1.5rem; margin: 0 0 .2rem; }
    .sub { color: var(--suave); margin: 0 0 1.2rem; }
    .aviso { background:#fff8e1; border:1px solid #e8d48b; color:#5c4700; padding:.7rem .9rem;
             border-radius:8px; margin:0 0 1.5rem; font-size:.85rem; }
    @media (prefers-color-scheme: dark) {
      :root:not([data-theme="light"]) .aviso { background:#33290d; border-color:#6b5716; color:#f2e2b0; }
    }
    .resultados { display:grid; gap:1rem; grid-template-columns: repeat(auto-fill, minmax(220px, 1fr)); }
    article.imovel { background:var(--cartao); border:1px solid var(--borda); border-radius:10px; padding:.9rem;
                     display:flex; flex-direction:column; gap:.25rem; }
    .imovel .tipo { font-size:.75rem; text-transform:uppercase; letter-spacing:.05em; color:var(--suave); margin:0; }
    .imovel h2 { font-size:1rem; margin:0; line-height:1.3; }
    .imovel h2 a { text-decoration:none; }
    .imovel .bairro { margin:0; font-size:.9rem; }
    .imovel .preco { margin:.2rem 0 0; font-weight:700; font-size:1.05rem; }
    .imovel .preco.consulte { color:var(--suave); font-weight:600; }
    ul.caracteristicas { list-style:none; padding:0; margin:.2rem 0 0; display:flex; gap:.6rem;
                         flex-wrap:wrap; font-size:.85rem; color:var(--suave); }
    .paginacao { list-style:none; display:flex; gap:1rem; justify-content:center; padding:0; margin:2rem 0 0; }
    .paginacao .atual { color:var(--suave); }
    dl.ficha { display:grid; grid-template-columns:max-content 1fr; gap:.35rem 1.2rem; background:var(--cartao);
               border:1px solid var(--borda); border-radius:10px; padding:1rem 1.2rem; }
    dl.ficha dt { font-weight:600; }
    dl.ficha dd { margin:0; }
    ul.comodidades { display:flex; flex-wrap:wrap; gap:.4rem; list-style:none; padding:0; }
    ul.comodidades li { border:1px solid var(--borda); border-radius:999px; padding:.15rem .7rem; font-size:.85rem;
                        background:var(--cartao); }
    nav.trilha { font-size:.85rem; color:var(--suave); margin-bottom:1rem; }
"""


def pagina(titulo: str, corpo: str, descricao: str) -> str:
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titulo)}</title>
  <meta name="description" content="{html.escape(descricao)}">
  <style>{CSS}  </style>
</head>
<body>
  <main class="conteudo">
{corpo}
  </main>
</body>
</html>
"""


def fmt_area(a: float) -> str:
    return (f"{a:.1f}".replace(".", ",") if a != int(a) else f"{int(a)}") + " m²"


def titulo_anuncio(im: dict) -> str:
    q = "quarto" if im["quartos"] == 1 else "quartos"
    if im["tipo"] == "Studio":
        return f"Studio em {im['bairro']}"
    return f"{im['tipo']} com {im['quartos']} {q} em {im['bairro']}"


AVISO = ('    <p class="aviso"><strong>Site fictício.</strong> Imobiliária, anúncios, endereços e preços foram '
         'inventados para a disciplina Coleta e Preparação de Dados (PUCRS Online). Os nomes dos bairros são reais; '
         'os valores são inventados.</p>')
N_PAG = 5
for p in range(1, N_PAG + 1):
    itens = DESTAQUES[(p - 1) * 12: p * 12]
    cards = []
    for im in itens:
        arq = f"imovel/{im['codigo'].lower()}.html"
        if im["codigo"] in CONSULTE:
            preco = '<p class="preco consulte">Consulte</p>'
        else:
            preco = f'<p class="preco">{brl(im["preco"])}</p>'
        vagas = "sem vaga" if im["vagas"] == 0 else (f"{im['vagas']} vaga" + ("s" if im["vagas"] > 1 else ""))
        q = "quarto" if im["quartos"] == 1 else "quartos"
        cards.append(f"""      <article class="imovel" data-codigo="{im['codigo']}">
        <p class="tipo">{im['tipo']}</p>
        <h2><a href="{arq}">{html.escape(titulo_anuncio(im))}</a></h2>
        <p class="bairro">{html.escape(im['bairro'])}</p>
        {preco}
        <ul class="caracteristicas">
          <li class="area">{fmt_area(im['area_m2'])}</li>
          <li class="quartos">{im['quartos']} {q}</li>
          <li class="vagas">{vagas}</li>
        </ul>
      </article>""")
    nav = []
    if p > 1:
        ant = "index.html" if p == 2 else f"pagina-{p - 1}.html"
        nav.append(f'      <li class="anterior"><a href="{ant}" rel="prev">← anterior</a></li>')
    nav.append(f'      <li class="atual">página {p} de {N_PAG}</li>')
    if p < N_PAG:
        nav.append(f'      <li class="proxima"><a href="pagina-{p + 1}.html" rel="next">próxima →</a></li>')
    corpo = f"""    <h1>Aurora Imóveis, Porto Alegre</h1>
    <p class="sub">{len(DESTAQUES)} imóveis à venda · página {p} de {N_PAG}</p>
{AVISO}
    <section class="resultados">
{chr(10).join(cards)}
    </section>
    <ul class="paginacao">
{chr(10).join(nav)}
    </ul>"""
    nome = "index.html" if p == 1 else f"pagina-{p}.html"
    with open(os.path.join(SITE, nome), "w", encoding="utf-8") as f:
        f.write(pagina(f"Aurora Imóveis · página {p}", corpo, "Anúncios fictícios de imóveis para praticar web scraping."))

for im in DESTAQUES:
    cond = "Isento" if im["tipo"] == "Casa" else f"{brl(im['condominio'])}/mês"
    andar = "—" if im["andar"] is None else (f"{im['andar']}º")
    preco = "Consulte" if im["codigo"] in CONSULTE else brl(im["preco"])
    ficha = [("Código", im["codigo"]), ("Tipo", im["tipo"]), ("Bairro", im["bairro"]),
             ("Endereço", im["endereco"]), ("Preço", preco), ("Área privativa", fmt_area(im["area_m2"])),
             ("Quartos", str(im["quartos"])), ("Banheiros", str(im["banheiros"])), ("Vagas", str(im["vagas"])),
             ("Condomínio", cond), ("IPTU", f"{brl(im['iptu_anual'])}/ano"), ("Andar", andar),
             ("Ano de construção", str(im["ano_construcao"])), ("Conservação", im["conservacao"]),
             ("Aceita pets", "Sim" if im["aceita_pet"] == "sim" else "Não"),
             ("Anunciado em", date.fromisoformat(im["data_anuncio"]).strftime("%d/%m/%Y"))]
    dl = "\n".join(f"      <dt>{html.escape(k)}</dt><dd>{html.escape(v)}</dd>" for k, v in ficha)
    com = "\n".join(f"      <li>{html.escape(c)}</li>" for c in im["comodidades"]) or "      <li>Nenhuma informada</li>"
    desc = (f"{titulo_anuncio(im)}, com {fmt_area(im['area_m2'])} de área privativa, construído em "
            f"{im['ano_construcao']}. Conservação: {im['conservacao'].lower()}. "
            f"Para visitar, fale com a Aurora Imóveis pelo e-mail contato@aurora-imoveis.example.com "
            f"informando o código {im['codigo']}.")
    corpo = f"""    <nav class="trilha"><a href="../index.html">Aurora Imóveis</a> › {html.escape(im['bairro'])} › {im['codigo']}</nav>
    <h1>{html.escape(titulo_anuncio(im))}</h1>
    <p class="sub">{html.escape(im['endereco'])} · {html.escape(im['bairro'])} · Porto Alegre/RS</p>
{AVISO}
    <h2>Ficha técnica</h2>
    <dl class="ficha">
{dl}
    </dl>
    <h2>Comodidades</h2>
    <ul class="comodidades">
{com}
    </ul>
    <h2>Descrição</h2>
    <p id="descricao">{html.escape(desc)}</p>"""
    with open(os.path.join(SITE, "imovel", f"{im['codigo'].lower()}.html"), "w", encoding="utf-8") as f:
        f.write(pagina(f"{titulo_anuncio(im)} · Aurora Imóveis", corpo, "Anúncio fictício de imóvel."))

urls = ["index.html"] + [f"pagina-{p}.html" for p in range(2, N_PAG + 1)] + \
       [f"imovel/{im['codigo'].lower()}.html" for im in DESTAQUES]
with open(os.path.join(SITE, "sitemap.xml"), "w", encoding="utf-8") as f:
    f.write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n')
    for u in urls:
        f.write(f"  <url>\n    <loc>{URL_BASE}/aula3/pratica/imoveis/{u}</loc>\n    <lastmod>2026-10-01</lastmod>\n  </url>\n")
    f.write("</urlset>\n")
with open(os.path.join(SITE, "robots.txt"), "w", encoding="utf-8") as f:
    f.write("""# Exemplo de robots.txt para a disciplina (num site real ele fica na raiz do domínio).
User-agent: *
Disallow: /aula3/pratica/imoveis/painel-corretor/
Crawl-delay: 1

Sitemap: https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula3/pratica/imoveis/sitemap.xml
""")

# --------------------------------------------------------------------------------------
# Gabarito interno (não publicado): o que foi plantado e quais anúncios são comuns
# --------------------------------------------------------------------------------------
if __name__ == "__main__":
    print("Sujeira plantada na base:")
    for s in SUJEIRA:
        print("  -", s)
    print("Anúncios com preço 'Consulte' no site:", sorted(CONSULTE))
    print("Pares Aurora x Casa Sul (mesmo imóvel):")
    for k, v in sorted(GABARITO_COMUNS.items()):
        print("  ", k, "=", v)
    print("Casa Sul: valor ausente em", casa_sul[7]["id"], "| valor em reais (não em mil) em", casa_sul[19]["id"])
