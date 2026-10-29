# Aula 2 — Expressões Regulares e Coleta em APIs REST

Arquivos usados nos exemplos da videoaula 2 e nos exercícios do encontro síncrono.

Publicados via GitHub Pages em
`https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula2/`.

---

# Parte 1 — Expressões regulares

## Testador com destaque dos casamentos

`aula2/testador/` — uma página para escrever a regex e ver, no texto, o que casa e o que não casa.

<https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula2/testador/>

- Os arquivos desta aula já vêm carregados em um clique: `datas.txt`, `emails.txt`,
  `latencia.log`, os trechos dos slides e o `mbox-short.txt` inteiro.
- Treze exemplos prontos, tirados direto dos slides 9 a 21.
- Flags `re.I`, `re.M`, `re.S` e `re.X`; a lista de casamentos mostra posição e grupos capturados.
- Referência rápida dos símbolos (slides 7 a 13) na própria página.
- O estado vai na URL: o padrão que estiver na tela gera um link que você pode colar no chat da
  aula, e abre no outro computador já com o padrão e o texto certos.

### Dois motores, de propósito

| Motor | Quando usar |
| --- | --- |
| **JavaScript** (padrão) | instantâneo, funciona sem rede — bom para a maior parte dos exercícios |
| **Python `re`** | baixa o Python de verdade (~11 MB, uns 3 s) e roda o mesmo `re` da aula |

A página avisa sozinha quando o padrão cai numa diferença entre os dois: `\w` e `\b` com letras
acentuadas, look-behind de largura variável, `(?P<nome>…)`, `\A`/`\Z` e `re.X`. Esses são
exatamente os pontos que os slides 9, 13 e 21 comentam — e a razão de o motor Python existir aqui.

Se a expressão travar o navegador (retrocesso catastrófico, o custo que o slide 10 cita), ela é
interrompida em 4 segundos e a página explica o que aconteceu.


## `regex/mbox-short.txt`

Caixa de e-mails usada nos slides 3, 14 e 15: 1910 linhas, 27 mensagens, com os cabeçalhos
`X-DSPAM-*` que aparecem nos exemplos.

> Arquivo de Charles R. Severance, *Python for Everybody*, cap. 11 — [py4e.com](https://www.py4e.com/),
> licença CC BY 4.0. Redistribuído aqui com atribuição.

```bash
grep -Pc '^X.*:' mbox-short.txt                        # 216 linhas de cabeçalho X-
grep -Po '(?<=X-DSPAM-Confidence:\s)[\d.]+' mbox-short.txt | head
```

```python
import re
texto = open('regex/mbox-short.txt', encoding='utf-8').read()

re.findall(r'(?m)^X.*:', texto)                          # slide 14
re.findall(r'[\w.+-]+@[\w.-]+\.\w+', texto)              # slide 15 — 42 endereços distintos
re.findall(r'\b\d{2}:\d{2}:\d{2}\b', texto)
re.findall(r'(?<=X-DSPAM-Confidence:\s)[\d.]+', texto)   # ['0.8475', '0.6178', ...]
```

## Os três exercícios

| Arquivo | Slide | Resposta esperada |
| --- | --- | --- |
| `regex/datas.txt` | 16–17 | `\b\d{1,2}/\d{1,2}/\d{4}\b` → 3 datas; a versão estrita `\d{2}/\d{2}/\d{4}` perde `7/1/2026` |
| `regex/emails.txt` | 18–19 | `[\w.+-]+@[\w.-]+\.\w+` → 2 endereços; `www.pucrs.br` fica de fora |
| `regex/latencia.log` | 20–21 | `(?<=latencia=)\d+` → `['134', '87', '2041']` |

## `regex/trechos_dos_slides.txt`

Os mini-exemplos dos slides 8 a 13 (âncoras, classes, quantificadores, grupos, escape, look-around)
em um arquivo só, para colar no [regex101.com](https://regex101.com) com o *flavor* Python.

---

# Parte 2 — APIs REST

## A API estática

O GitHub Pages só serve arquivos estáticos, então esta "API" é um conjunto de JSONs com caminhos
que imitam uma API de verdade. Serve para praticar `requests`, paginação e `json_normalize` sem
depender de rede externa nem gastar cota de ninguém.

| Caminho | O que é |
| --- | --- |
| `api/v1/localidades/estados/RS/municipios.json` | cópia da resposta do IBGE usada no slide 30: 497 municípios |
| `api/v1/localidades/estados/RS/_proveniencia.json` | URL, data da coleta e versão da API — a proveniência que o slide 41 pede |
| `api/v1/municipios/pagina-1.json` … `pagina-6.json` | a mesma lista paginada, 100 por página; a 6ª vem vazia |
| `api/v1/processos.json` | registros com texto livre, para usar regex sobre o retorno da API (slide 40) |

> Os dados de municípios vêm da [API de Localidades do IBGE](https://servicodados.ibge.gov.br/api/docs/localidades),
> coletados em 20/09/2026. Dado público, redistribuído sem alteração.

### A primeira requisição (slide 30)

```python
import requests
base = "https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula2/api/v1"
r = requests.get(f"{base}/localidades/estados/RS/municipios.json", timeout=10)
r.status_code                  # 200
r.headers["Content-Type"]      # application/json; charset=utf-8
municipios = r.json()
len(municipios)                # 497
```

### Paginação (slide 37)

Cada página traz `pagina`, `total_paginas`, `proxima` e `dados`. O laço para quando `dados` vem
vazio — e a trava por contagem continua sendo obrigatória.

```python
dados, pagina = [], 1
while True:
    r = requests.get(f"{base}/municipios/pagina-{pagina}.json", timeout=30)
    r.raise_for_status()
    corpo = r.json()
    if not corpo["dados"]:
        break
    dados.extend(corpo["dados"])
    pagina += 1
    if pagina > 100:          # trava de segurança
        break
len(dados)                     # 497
```

### Do JSON ao DataFrame (slide 39)

```python
import pandas as pd
df = pd.json_normalize(municipios, sep="_")
df.shape        # (497, 22)
df.columns[:4]  # ['id', 'nome', 'microrregiao_id', 'microrregiao_nome']
```

### Regex sobre o retorno da API (slide 40)

```python
proc = requests.get(f"{base}/processos.json", timeout=10).json()
df = pd.DataFrame(proc)
df["protocolo"] = df["resumo"].str.extract(r"(\d{4}/\d{5}-\d)")
# ['2024/00123-4', '2025/00987-1', '2024/00456-9', NaN]
```

O último registro não tem número de processo e vira `NaN` — é o caso que o aluno precisa lembrar
de tratar.

## O que esta API estática **não** consegue fazer

| Assunto do slide | Por quê | Onde praticar de verdade |
| --- | --- | --- |
| Query string (`?orderBy=nome`) | arquivo estático ignora parâmetros | API do IBGE, ao vivo |
| Códigos 404, 429, 500 | o Pages devolve 200 ou 404, e só | [httpstat.us](https://httpstat.us) e [httpbin.org](https://httpbin.org) |
| Cabeçalhos `Link`, `Retry-After`, autenticação | não dá para definir cabeçalhos | httpbin.org |
| `POST`, `PUT`, `DELETE` | o Pages só responde `GET` e `HEAD` | httpbin.org |

A API do IBGE usada no slide 30 continua pública e funcionando; a cópia estática existe para o
exercício não depender dela.


---

## Prática do encontro síncrono 2

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula2/pratica/encontro2.ipynb)

`pratica/encontro2.ipynb`: notebook da atividade conduzida pelo mediador. O gabarito fica fora
deste repositório e é distribuído ao mediador junto com os slides do encontro.

**O log da Aurora Imóveis e o coletor do colega.**

`pratica/acessos.log`: 420 linhas de log de acesso fictício (formato *combined* do Apache/Nginx
com `rt=NNNms` no fim). IPs das faixas de documentação (RFC 5737) e e-mails em domínios `example.*`.
Gerado por `ferramentas/gerar_log_acessos.py` (determinístico).

| Pergunta | Resposta esperada |
| --- | --- |
| status mais comuns | 200 (325), 429 (59), 500 (7), 301 (7), 404, 401, 403 (6 cada), 503 (4) |
| latência média / máxima | 529,3 ms / 6733 ms; as 7 acima de 3 s são erros 5xx |
| quem levou 429 | `203.0.113.9`, `python-requests/2.32.3`, em rajadas sem intervalo |
| e-mails nos User-Agents | `ana.souza@aluno.example.edu`, `dados@observatorio.example.org` |
| acessos a áreas proibidas no robots | `203.0.113.200` (`BuscadorMalEducado/0.1`), 12 vezes |

A parte B é a revisão de um coletor da API estática (`api/v1/municipios/`) com problemas
plantados: o laço de paginação descarta a última página (400 municípios em vez de 497), falta
`timeout` e `raise_for_status()`, o token está no código, a query string é concatenada e a regex do
protocolo corta o dígito verificador e aceita o protocolo interno.
