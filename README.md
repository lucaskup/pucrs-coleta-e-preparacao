# Coleta e Preparação de Dados

Material prático da disciplina **Coleta e Preparação de Dados** (PUCRS Online, graduação,
modalidade síncrona), ministrada pelo Prof. Lucas Silveira Kupssinskü. O repositório hospeda os
arquivos que os alunos manipulam nos exercícios: dados em texto, CSV, XML e JSON, páginas web para
scraping, uma API REST estática e os notebooks dos encontros síncronos. Slides e videoaulas ficam
fora daqui.

Tudo é publicado via GitHub Pages em <https://lucaskup.github.io/pucrs-coleta-e-preparacao/>, então
os arquivos podem ser lidos direto da URL (`pd.read_csv("https://lucaskup.github.io/...")`) ou
baixados de uma vez:

```bash
git clone https://github.com/lucaskup/pucrs-coleta-e-preparacao.git
```

## Conteúdo por aula

| Aula | Tema | O que há no repositório |
| --- | --- | --- |
| [1](aula1/) | Arquivos de texto, CSV, XML e JSON | Exemplos dos slides em três codificações (UTF-8, ISO-8859-1, UTF-8 com BOM), CSV em padrão brasileiro, XML tabular e aninhado, JSON em todos os `orient` do pandas; página estática de corpo docente para `wget` + `grep` |
| [2](aula2/) | Expressões regulares e APIs REST | `mbox-short.txt`, logs, e-mails e datas para regex; [testador de regex](https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula2/testador/) com motor JavaScript e Python; API estática com JSONs paginados imitando uma API REST |
| [3](aula3/) | Web scraping | Páginas HTML estáticas dos exemplos (livraria, produtos, tabela, países), catálogo com paginação, páginas de detalhe, `sitemap.xml` e `robots.txt`; página dinâmica montada por JavaScript |
| [4](aula4/) | KDD, tipos de dados e estatística descritiva | `imoveis_aurora.csv`: 300 anúncios sintéticos com atributos de todos os níveis de medição e problemas plantados |
| [5](aula5/) | Visualização, similaridade e pré-processamento | Usa a base da aula 4 |
| [6](aula6/) | Limpeza, integração, redução e transformação | A base da aula 4, uma segunda fonte em JSON com esquema diferente e uma tabela de bairros para integrar |

Cada pasta tem um `index.html` (navegação para os alunos no GitHub Pages) e um `README.md` com a
descrição de cada arquivo, o slide de origem e os comandos usados na videoaula.

## Práticas dos encontros síncronos

Cada encontro tem um notebook em `aulaN/pratica/encontroN.ipynb`, pensado para o Google Colab e
lendo os dados direto do GitHub Pages. Os encontros 3 a 6 seguem um fio condutor: a imobiliária
fictícia **Aurora Imóveis**, de Porto Alegre. O mini-site raspado no encontro 3 contém os 60
primeiros anúncios da base de 300 usada nos encontros 4 a 6.

| Encontro | Atividade | Formato |
| --- | --- | --- |
| [1](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula1/pratica/encontro1.ipynb) | Conserte a leitura | corrigir cinco leituras de arquivo que deram errado |
| [2](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula2/pratica/encontro2.ipynb) | O log da Aurora Imóveis e o coletor do colega | regex sobre um log de acesso e revisão de um coletor de API |
| [3](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula3/pratica/encontro3.ipynb) | Raspando a Aurora Imóveis | escrever o scraper com revisão cruzada por checklist |
| [4](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula4/pratica/encontro4.ipynb) | Descreva os dados antes de modelar | classificar atributos e seguir o roteiro de análise exploratória |
| [5](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula5/pratica/encontro5.ipynb) | Integridade de gráficos e imóveis parecidos | refazer gráficos e comparar medidas de similaridade |
| [6](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula6/pratica/encontro6.ipynb) | Da base suja à base pronta para o modelo | estações de limpeza, integração e transformação com diário de decisões |

Os gabaritos ficam fora deste repositório, que é público.

## Estrutura

```
index.html          landing page do GitHub Pages
assets/             estilo.css e tema.js compartilhados pelas páginas de navegação
aula1/ … aula6/     um diretório por aula: index.html, README.md, dados e pratica/
ferramentas/        geradores determinísticos dos dados sintéticos
```

## Dados sintéticos e proveniência

Pessoas, instituições, imóveis, preços, endereços e e-mails são inventados. Os bairros de Porto
Alegre existem, mas os valores associados a eles não servem para nada além da aula. Endereços IP
usam as faixas reservadas para documentação e e-mails usam domínios `example.*`.

Os dados da Aurora Imóveis e o log de acessos são gerados por scripts com semente fixa em
`ferramentas/`, então regenerá-los produz os mesmos arquivos:

```bash
python ferramentas/gerar_imoveis.py        # aula3/pratica/imoveis/, aula4 e aula6
python ferramentas/gerar_log_acessos.py    # aula2/pratica/acessos.log
```

Ao alterar os geradores, confira os números de referência citados nos READMEs e nos notebooks.

Dois insumos externos são redistribuídos com atribuição, documentada em `aula2/README.md`:
`mbox-short.txt`, de *Python for Everybody* (Charles Severance, CC BY 4.0), e a resposta da API de
Localidades do IBGE (dado público, copiado sem alteração, com arquivo de proveniência ao lado).

## Rodando localmente

As páginas são autocontidas e não dependem de sites de terceiros. Para servi-las:

```bash
python -m http.server 8000
```

O servidor embutido do Python responde `text/html` sem `charset`, então `requests` pode mostrar a
acentuação quebrada em `r.text`. O GitHub Pages envia `charset=utf-8`. Essa diferença é usada como
exercício na aula 2.

## Licença

O conteúdo deste repositório (dados sintéticos, páginas, notebooks e scripts) está sob a licença
[Creative Commons Atribuição 4.0 Internacional (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/deed.pt-br).
Você pode copiar, redistribuir e adaptar o material, inclusive para fins comerciais, desde que
dê o crédito apropriado:

> Kupssinskü, L. S. *Coleta e Preparação de Dados: material prático*. PUCRS Online, 2026.
> <https://github.com/lucaskup/pucrs-coleta-e-preparacao>. Licença CC BY 4.0.

O texto completo está em [`LICENSE`](LICENSE). Os insumos de terceiros mantêm as licenças
originais indicadas acima.
