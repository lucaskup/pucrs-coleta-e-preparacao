# Aula 3 — Web scraping: HTML, CSS, seletores e BeautifulSoup

Páginas usadas nos exemplos da videoaula 3 e nos exercícios do encontro síncrono.
Todas são fictícias e autocontidas: o exercício não depende de nenhum site de terceiros.

Publicadas via GitHub Pages em
`https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula3/`.

| Pasta | Serve para | Slides |
| --- | --- | --- |
| `livraria/` | o documento mínimo de HTML e DOM | 19, 25, 49–51 |
| `produtos/` | o exercício de seletor CSS × XPath | 43–44 |
| `paises/` | XPath: predicados, funções e eixos | 39–41 |
| `tabela/` | `pandas.read_html` | 21 |
| `catalogo/` | o pipeline completo: seletores, paginação, links | 22, 52–55, 62 |
| `dinamica/` | conteúdo montado por JavaScript | 27, 56 |

---

## `livraria/` — o documento dos slides 19 e 25

Exatamente o HTML que aparece na apresentação, com `p.nota`, dois `<a>` irmãos e `ul#livros`.
É o alvo dos exemplos de navegação no BeautifulSoup:

```python
from bs4 import BeautifulSoup
import requests
soup = BeautifulSoup(requests.get(URL + 'livraria/', timeout=20).text, 'lxml')

soup.body.p['class']                    # ['nota']
ul = soup.find('ul', id='livros')
len(ul.contents)                         # não é 2: os \n entre as tags contam
[li.get_text(strip=True) for li in ul.find_all('li')]
soup.a.find_next_sibling('a')            # <a href="/cambio">câmbio</a>
soup.a.find_parent('p')['class']          # ['nota']
```

> Os dois links da página (`/moeda` e `/cambio`) apontam para lugar nenhum, como no slide. Eles existem para exercitar `find_next_sibling` e `href`, não para serem seguidos.

## `produtos/` — exercício dos slides 43 e 44

```python
soup.select('p.preco')                       # CSS
arvore.xpath("//p[@class='preco']/text()")   # XPath — ['R$ 4.299,00', 'R$ 129,00']
```

## `paises/` — XPath de verdade

16 países em cartões `div.country`, cada um com `h3.country-name` e um `div.country-info`
contendo `span.country-capital`, `span.country-population`, `span.country-area` e
`span.country-continent`. A estrutura reproduz a de `scrapethissite.com/pages/simple/`, usada
no slide 41, **incluindo as duas armadilhas que o slide comenta**:

```python
from lxml import html
arvore = html.fromstring(requests.get(URL + 'paises/', timeout=20).content)

# 1. text() pega a indentação junto, porque há um <i> dentro do h3
brutos = arvore.xpath("//h3[@class='country-name']/text()")
nomes  = [n.strip() for n in brutos if n.strip()]      # 16 nomes

# 2. contains(@class,'country') casa com country E country-info: 32 nós, não 16
len(arvore.xpath("//div[contains(@class,'country')]"))   # 32
TEM = "contains(concat(' ', normalize-space(@class), ' '), ' country ')"
len(arvore.xpath(f"//div[{TEM}]"))                       # 16

# 3. XPath relativo: sem o ponto, volta a varrer o documento inteiro
for pais in arvore.xpath(f"//div[{TEM}]"):
    nome = pais.xpath('normalize-space(./h3)')
    pop  = int(pais.xpath("./div/span[@class='country-population']/text()")[0])

# 4. o eixo following-sibling, do slide 40
arvore.xpath("//strong[normalize-space()='Capital:']/following-sibling::span[1]/text()")
```

## `tabela/` — `pandas.read_html`

Duas tabelas na mesma página:

- `#populacao` — regular, 16 linhas: `pd.read_html(StringIO(r.text))[0]` resolve.
- `#dificil` — cabeçalho em duas linhas, `rowspan`, `colspan` e uma linha de rodapé: o caso que
  o slide 21 avisa que quebra. Boa discussão no encontro: o que sai, e o que fazer depois.

```python
from io import StringIO
tabelas = pd.read_html(StringIO(r.text))
len(tabelas)                 # 2
tabelas[0].shape             # (16, 3)
```

## `catalogo/` — o pipeline completo

Livraria Aurora: 24 livros fictícios, 8 por página, 3 páginas de listagem e uma página de detalhe
por livro. A marcação repete as classes usadas nos slides: `article.product_pod`, `h3 a[title]`,
`p.price_color`, `p.instock.availability`, `p.star-rating`, `li.next > a`.

```
catalogo/index.html          página 1        catalogo/livro/<slug>.html   detalhe (24)
catalogo/pagina-2.html       página 2        catalogo/sitemap.xml         27 URLs
catalogo/pagina-3.html       página 3        catalogo/robots.txt          exemplo
```

### O pipeline do slide 62, adaptado

Só muda a conversão do preço: aqui é `R$ 4.299,00`, e não `£51.77`.

```python
import re, time, requests, pandas as pd
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = 'https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula3/catalogo/'
HEAD = {'User-Agent': 'PUCRS-aula-coleta/1.0 (seu.email@edu.pucrs.br)'}
linhas, url = [], BASE
while url:
    r = requests.get(url, headers=HEAD, timeout=20); r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    for pod in soup.select('article.product_pod'):
        preco = pod.select_one('p.price_color').text          # 'R$ 4.299,00'
        linhas.append({
            'titulo': pod.select_one('h3 a')['title'],
            'preco': float(re.sub(r'[^0-9,]', '', preco).replace(',', '.')),
            'estrelas': [c for c in pod.select_one('p.star-rating')['class'] if c != 'star-rating'][0],
            'estoque': 'outofstock' not in pod.select_one('p.availability')['class'],
            'link': urljoin(url, pod.select_one('h3 a')['href']),
        })
    proxima = soup.select_one('li.next > a')
    url = urljoin(url, proxima['href']) if proxima else None
    time.sleep(1)
df = pd.DataFrame(linhas)      # (24, 5) — preço médio R$ 49,05, 3 esgotados
```

`re.sub(r'[^0-9.]', ...)` do slide original **não** funciona aqui: ele apagaria a vírgula decimal
e transformaria `R$ 4.299,00` em `4.29900`. Bom momento para relembrar o `decimal=','` da aula 1.

### `robots.txt` e `sitemap.xml` (slides 59 e 60)

```python
from urllib.robotparser import RobotFileParser
rp = RobotFileParser()
rp.set_url(BASE + 'robots.txt'); rp.read()
rp.can_fetch('*', BASE + 'index.html')    # True
rp.can_fetch('*', BASE + 'admin/')        # False
rp.crawl_delay('*')                       # 1

soup = BeautifulSoup(requests.get(BASE + 'sitemap.xml', timeout=20).content, 'lxml-xml')
locs = [u.loc.text for u in soup.find_all('url')]   # 27 URLs
```

> Em um site real, o `robots.txt` fica na **raiz do domínio**. Este repositório é um *project page*
> dentro de `lucaskup.github.io`, então o `robots.txt` que vale de verdade para os robôs é o da
> raiz daquele domínio, que não controlamos. O arquivo aqui é um exemplo para ler e interpretar
> no exercício — não uma diretiva com efeito.

## `dinamica/` — onde o BeautifulSoup para

Painel de 12 estações meteorológicas. A tabela é montada por JavaScript a partir de
`dinamica/dados.json`; o HTML entregue pelo servidor traz só "Carregando leituras…".

```python
r = requests.get(URL + 'dinamica/', timeout=20)
soup = BeautifulSoup(r.text, 'lxml')
len(soup.select('tr.leitura'))        # 0  ← o dado não está no HTML entregue

# no navegador (aba Elements) as 12 linhas existem. O caminho certo, como diz o slide 27:
# procurar na aba Network quem alimenta a página
requests.get(URL + 'dinamica/dados.json', timeout=20).json()['total']   # 12
```

É o roteiro do slide 27 inteiro: ver no inspetor, não achar em `r.text`, encontrar o endpoint e
resolver o problema sem navegador automatizado. Também serve de alvo se você quiser demonstrar
Selenium ou Playwright.

---

## Servindo localmente

```bash
python -m http.server 8000      # na raiz do repositório
# http://localhost:8000/aula3/catalogo/
```

**Atenção a um efeito colateral útil:** o `python -m http.server` responde `Content-type: text/html`
**sem** `charset`. Como ensina o slide 32 da aula 2, o `requests` então assume ISO-8859-1 e
`r.text` devolve `O Jardim das MarÃ©s`. O GitHub Pages envia `charset=utf-8` e o problema não
aparece. Se quiser o texto correto localmente:

```python
r.encoding = 'utf-8'                      # antes de ler r.text
html.fromstring(r.content)                # ou entregue bytes: o lxml lê o <meta charset>
```


---

## Prática do encontro síncrono 3

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula3/pratica/encontro3.ipynb)

`pratica/encontro3.ipynb` — notebook da atividade conduzida pelo mediador. O gabarito **não** fica
neste repositório (é distribuído ao mediador junto com os slides do encontro).

**Raspando a Aurora Imóveis.** Alvo novo, para não repetir o catálogo da videoaula:

```
pratica/imoveis/index.html, pagina-2.html … pagina-5.html   12 anúncios por página, link a[rel=next]
pratica/imoveis/imovel/aur-0001.html … aur-0060.html         ficha técnica em <dl><dt>/<dd>, ul.comodidades
pratica/imoveis/sitemap.xml                                 65 URLs
pratica/imoveis/robots.txt                                  exemplo (Disallow painel-corretor/, Crawl-delay 1)
```

Marcação: `article.imovel[data-codigo]`, `p.tipo`, `h2 a`, `p.bairro`, `p.preco` (`R$ 1.057.000` ou
`Consulte`), `li.area` (`72,6 m²`), `li.quartos`, `li.vagas` (`sem vaga`). Na ficha, o condomínio das
casas é `Isento` e o andar é `—`.

Números de referência: 60 anúncios, 2 com preço "Consulte" (AUR-0018 e AUR-0045), preço mediano
R$ 734.500. Os 60 anúncios são os 60 primeiros da base completa usada nas aulas 4 a 6.
Gerado por `ferramentas/gerar_imoveis.py`.
