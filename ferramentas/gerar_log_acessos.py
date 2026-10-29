"""Gera aula2/pratica/acessos.log: log de acesso fictício do servidor da "Aurora Imóveis".

Formato "combined" do Apache/Nginx acrescido do tempo de resposta no fim da linha:

  IP - - [dd/Mon/aaaa:hh:mm:ss -0300] "MÉTODO caminho HTTP/1.1" status bytes "referer" "user-agent" rt=NNNms

Os IPs pertencem às faixas reservadas para documentação (RFC 5737: 192.0.2.0/24,
198.51.100.0/24 e 203.0.113.0/24) e os e-mails usam domínios example.*: nada aqui é real.

Uso:  python ferramentas/gerar_log_acessos.py   (determinístico)
"""
import os
import random
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rng = random.Random(2026_10_05)
MESES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
BAIRROS = ["Moinhos%20de%20Vento", "Petr%C3%B3polis", "Menino%20Deus", "Bom%20Fim", "Tristeza", "Sarandi"]

CLIENTES = [
    # (ip, user-agent, peso, perfil)
    ("192.0.2.14", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/129.0 Safari/537.36", 30, "pessoa"),
    ("192.0.2.88", "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_6) AppleWebKit/605.1.15 Safari/605.1.15", 20, "pessoa"),
    ("198.51.100.23", "coletor-pucrs/1.0 (ana.souza@aluno.example.edu)", 25, "educado"),
    ("198.51.100.57", "pesquisa-imoveis/2.1 (+https://observatorio.example.org; dados@observatorio.example.org)", 15, "educado"),
    ("203.0.113.9", "python-requests/2.32.3", 12, "apressado"),
    ("203.0.113.200", "BuscadorMalEducado/0.1", 18, "mal"),
]


def caminho(perfil):
    r = rng.random()
    if perfil == "mal" and r < 0.4:
        return rng.choice(["/painel-corretor/", "/painel-corretor/login", "/admin/"])
    if r < 0.45:
        q = f"pagina={rng.randint(1, 6)}"
        if rng.random() < 0.4:
            q = f"bairro={rng.choice(BAIRROS)}&" + q
        return f"/api/v1/imoveis?{q}"
    if r < 0.8:
        return f"/api/v1/imoveis/AUR-{rng.randint(1, 320):04d}"
    if r < 0.88:
        return "/robots.txt"
    if r < 0.95:
        return "/sitemap.xml"
    return rng.choice(["/", "/contato", "/sobre"])


def status_para(c, perfil, rajada):
    if perfil == "apressado" and rajada >= 5 and rng.random() < 0.6:
        return 429
    if c.startswith("/painel-corretor") or c == "/admin/":
        return rng.choice([401, 403, 403])
    if c.startswith("/api/v1/imoveis/AUR-") and int(c[-4:]) > 300:
        return 404
    if "pagina=6" in c:
        return 200  # página vazia, mas existe
    r = rng.random()
    if r < 0.015:
        return 500
    if r < 0.03:
        return 503
    if c == "/sobre":
        return 301
    return 200


linhas = []
t = datetime(2026, 10, 5, 8, 0, 0)
while len(linhas) < 420:
    ip, ua, _, perfil = rng.choices(CLIENTES, [c[2] for c in CLIENTES])[0]
    t += timedelta(seconds=rng.randint(1, 40))
    # o cliente "apressado" dispara rajadas sem intervalo entre as requisições
    n = rng.randint(4, 12) if perfil == "apressado" else 1
    for k in range(n):
        if k:
            t += timedelta(milliseconds=rng.randint(80, 300))
        c = caminho(perfil)
        st = status_para(c, perfil, k)
        metodo = "GET" if rng.random() > 0.03 or perfil == "pessoa" else "HEAD"
        if c == "/contato" and rng.random() < 0.5:
            metodo = "POST"
        tamanho = 0 if st in (301, 429) or metodo == "HEAD" else rng.randint(300, 48000)
        if st >= 500:
            rt = rng.randint(1500, 9000)
        elif st == 429:
            rt = rng.randint(2, 15)
        else:
            rt = rng.randint(20, 900) if rng.random() > 0.05 else rng.randint(1000, 3000)
        ref = '"-"' if perfil != "pessoa" else '"https://aurora-imoveis.example.com/"'
        data = f"{t.day:02d}/{MESES[t.month - 1]}/{t.year}:{t:%H:%M:%S} -0300"
        linhas.append(f'{ip} - - [{data}] "{metodo} {c} HTTP/1.1" {st} {tamanho} {ref} "{ua}" rt={rt}ms')
linhas = linhas[:420]

os.makedirs(os.path.join(RAIZ, "aula2", "pratica"), exist_ok=True)
with open(os.path.join(RAIZ, "aula2", "pratica", "acessos.log"), "w", encoding="utf-8") as f:
    f.write("\n".join(linhas) + "\n")
print(len(linhas), "linhas;", linhas[0])
