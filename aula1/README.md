# Aula 1 — Arquivos de Texto, CSV, XML e JSON

Arquivos usados nos exemplos da videoaula 1 e nos exercícios do encontro síncrono.

Publicados via GitHub Pages em
`https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula1/`.

---

## `txt/` — arquivos de texto e codificação

| Arquivo | Codificação | De onde vem |
| --- | --- | --- |
| `primeiro_arquivo.txt` | UTF-8 | slide 11 (`echo lucas >> ...` + `xxd`) |
| `segundo_arquivo.txt` | UTF-8 | slide 11 |
| `acentuacao_utf8.txt` | UTF-8 | slides 12–13 |
| `acentuacao_iso8859_1.txt` | ISO-8859-1 (latin-1) | slides 12–13 |
| `acentuacao_utf8_bom.txt` | UTF-8 com BOM | slides 12–13 |

Os três arquivos `acentuacao_*` têm **o mesmo texto** e bytes diferentes:

```bash
xxd primeiro_arquivo.txt          # 6c75 6361 730a
xxd segundo_arquivo.txt           # 7075 6372 730a

xxd acentuacao_utf8.txt           # "ç" = c3a7  (2 bytes)
xxd acentuacao_iso8859_1.txt      # "ç" = e7    (1 byte)
xxd acentuacao_utf8_bom.txt       # começa com efbb bf
```

Em Python, abrir com a codificação errada falha de forma visível:

```python
open('acentuacao_iso8859_1.txt', encoding='utf-8').read()     # UnicodeDecodeError
open('acentuacao_iso8859_1.txt', encoding='iso-8859-1').read() # correto
open('acentuacao_utf8_bom.txt', encoding='utf-8').readline()   # '﻿coracao\n'
open('acentuacao_utf8_bom.txt', encoding='utf-8-sig').readline() # 'coracao\n'
```

## `csv/`

| Arquivo | Observação |
| --- | --- |
| `pessoas.csv` | exemplo do slide 17, UTF-8, separador `,` (ver nota abaixo) |
| `pessoas_iso8859_1.csv` | mesmo conteúdo em latin-1 → exige `encoding='iso-8859-1'` |
| `pessoas_utf8_bom.csv` | mesmo conteúdo com BOM |
| `produtos_ptbr.csv` | padrão brasileiro: separador `;` e vírgula decimal |

> **Divergência proposital do slide 17:** a data de nascimento de Tim Berners-Lee está
> `08-jun-1955` nos arquivos. O slide traz `12-mar-1989`, que é a data da proposta da Web,
> não o nascimento dele — corrigir também na apresentação.

```python
import pandas as pd

pd.read_csv('csv/pessoas.csv')
pd.read_csv('csv/pessoas_iso8859_1.csv', encoding='iso-8859-1')
pd.read_csv('csv/produtos_ptbr.csv', sep=';', decimal=',')   # slide 19
pd.read_csv('csv/produtos_ptbr.csv')                          # 3 linhas × 1 coluna: errado
```

## `xml/`

| Arquivo | De onde vem |
| --- | --- |
| `bookstore.xml` | slides 23–24 (estrutura em árvore, atributos `category` e `lang`) |
| `filme.xml` | slide 32 (comparação XML × JSON) |

```python
import pandas as pd, xml.etree.ElementTree as ET

pd.read_xml('xml/bookstore.xml')      # tabular: funciona bem
pd.read_xml('xml/filme.xml')          # aninhado: resultado ruim, 4 linhas com NaN

arvore = ET.parse('xml/bookstore.xml')
[t.text for t in arvore.getroot().iter('title')]
```

`filme.xml` é o contraexemplo do slide 26: `read_xml` só funciona bem quando a estrutura é
razoavelmente tabular. Com `<categories>` aninhado, o DataFrame sai quebrado — bom gancho para
discutir por que às vezes é preciso percorrer a árvore na mão.

## `json/`

| Arquivo | De onde vem |
| --- | --- |
| `exemplo.json` | slides 27 e 29 (objeto do Turing, lido com `json.load`) |
| `marie_curie.json` | slides 28 e 31 (array, booleano e objeto aninhado) |
| `cientistas.json` | três registros aninhados, para `pd.json_normalize` |
| `produtos.json` | slide 30, `orient='records'` |
| `produtos_values.json`, `produtos_columns.json`, `produtos_index.json`, `produtos_table.json` | os demais valores de `orient` do slide 30, com os mesmos dados |
| `filme.json` | slide 32 |

```python
import json, pandas as pd

with open('json/exemplo.json', encoding='utf-8') as f:
    dados = json.load(f)

pd.json_normalize(json.load(open('json/marie_curie.json', encoding='utf-8')))
# colunas: nome, profissao, idade, ganhou_nobel, conjuge.nome

for orient in ['records', 'values', 'columns', 'index', 'table']:
    arquivo = 'json/produtos.json' if orient == 'records' else f'json/produtos_{orient}.json'
    print(orient, pd.read_json(arquivo, orient=orient).shape)
```

Os cinco arquivos de `produtos` representam **a mesma tabela** em formatos diferentes — serve para
mostrar que `orient` não é detalhe: com o valor errado, o `read_json` falha ou devolve lixo.

## `site/` — página estática de corpo docente

Substitui, nos exercícios, a página de professores da PUCRS usada no slide 7.

> A URL original do slide (`https://www.pucrs.br/politecnica/a-escola/professores/`) **não existe
> mais** — hoje redireciona para uma notícia de 2018 e não tem nenhuma tag `<b>`. A cópia local
> garante que o exercício continue funcionando.

A página descreve uma **Escola Politécnica fictícia** (Universidade Aurora): 24 docentes em 5
departamentos, com nomes, titulação, área de pesquisa e e-mails inventados
(domínio `example.edu`, reservado para documentação).

A marcação é semântica, e não `<b>` como na página antiga:

```html
<article class="docente">
  <h3 class="docente__nome">Adriana Vasconcelos Prado</h3>
  <p class="docente__titulacao">Doutora em Ciência da Computação</p>
  <p class="docente__area">Aprendizado de máquina, visão computacional</p>
  <a class="docente__email" href="mailto:adriana.prado@poli.example.edu">…</a>
</article>
```

### Comando equivalente ao do slide 7

```bash
wget https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula1/site/
grep -Po '<h3 class="docente__nome">\K[^<]+' index.html | wc -l
# 24
```

Não é mais necessário o `head -n -1` do slide original: ele existia só para descartar um `<b>`
extra que a página da PUCRS tinha no fim. Aqui o padrão casa exatamente com os nomes.

Variações úteis para o encontro síncrono:

```bash
grep -Po '<h3 class="docente__nome">\K[^<]+' index.html              # listar os nomes
grep -Po 'class="departamento__nome">\K[^<]+' index.html             # listar departamentos
grep -Po 'mailto:\K[^"]+' index.html | sort | wc -l                  # contar e-mails
```

### Servindo localmente

```bash
python -m http.server 8000      # na raiz do repositório
wget http://localhost:8000/aula1/site/
```


---

## Prática do encontro síncrono 1

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula1/pratica/encontro1.ipynb)

`pratica/encontro1.ipynb` — notebook da atividade conduzida pelo mediador. O gabarito **não** fica
neste repositório (é distribuído ao mediador junto com os slides do encontro).

**Conserte a leitura** (15 min, em duplas): cinco leituras de arquivo escritas por um "colega" que
saem erradas. Para cada uma, o aluno observa o sintoma, explica a causa e corrige.

| Caso | Arquivo | Sintoma | Correção |
| --- | --- | --- | --- |
| 1 | `csv/pessoas_iso8859_1.csv` | `UnicodeDecodeError` | `encoding='iso-8859-1'` |
| 2 | `csv/produtos_ptbr.csv` | 3 linhas × 1 coluna | `sep=';', decimal=','` |
| 3 | `csv/pessoas_utf8_bom.csv` lido como latin-1 | `ï»¿nome`, `matemÃ¡tico` | `encoding='utf-8-sig'` |
| 4 | `json/cientistas.json` | `dict` dentro da célula | `pd.json_normalize` |
| 5 | `xml/filme.xml` | 4 linhas cheias de `NaN` | percorrer a árvore com `ElementTree` |
