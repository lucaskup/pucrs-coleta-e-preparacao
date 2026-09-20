# CLAUDE.md

## O que é este repositório

Repositório com **todo o conteúdo prático** da disciplina **Coleta e Preparação de Dados**
(PUCRS Online — graduação, modalidade síncrona), ministrada por **Lucas Silveira Kupssinskü**
(professor conteudista e regente).

O objetivo é hospedar os **artefatos que os alunos vão manipular nos exercícios**:

- arquivos de dados: `.txt`, `.csv`, `.json`, `.xml`
- páginas web **estáticas** (HTML puro) para scraping com Beautiful Soup / seletores CSS / XPath
- páginas web **dinâmicas** (conteúdo renderizado por JavaScript) para scraping com Selenium
- notebooks / scripts de apoio quando fizer sentido

Ou seja: este repositório é a **fonte dos dados e dos alvos de scraping** usados nas aulas, não o
material expositivo (slides e videoaulas ficam fora daqui).

## Estrutura

Uma pasta por encontro síncrono, com `index.html` (navegação para os alunos) e `README.md`
(descrição dos arquivos e comandos, lido no GitHub):

```
index.html        landing page do GitHub Pages
.nojekyll
aula1/
  index.html      índice dos arquivos da aula
  README.md       o que é cada arquivo, de qual slide vem, comandos
  txt/ csv/ xml/ json/
  site/index.html página estática de corpo docente (alvo de wget/scraping)
aula2/ … aula6/   ainda vazias
```

## Mapa de conteúdos por aula

| Aula | Conteúdo | Artefatos esperados no repo |
| --- | --- | --- |
| 1 | Abertura e manipulação de arquivos TXT, CSV e JSON | `.txt`, `.csv`, `.json` (incluindo casos sujos: encoding, separadores, aninhamento) |
| 2 | Expressões regulares | arquivos texto com logs, e-mails, telefones, datas, CPF/CNPJ, etc. |
| 3 | Web scraping: Beautiful Soup, Selenium, seletores CSS, XPath | páginas HTML estáticas e páginas dinâmicas com JS (paginação, lazy load, filtros) |
| 4 | Etapas do processo de KDD; objetos de dados e seus atributos; estatística descritiva | datasets tabulares com tipos de atributo variados (nominal, ordinal, intervalar, razão) |
| 5 | Visualização de dados; similaridade e dissimilaridade; introdução ao pré-processamento | datasets adequados a gráficos e a cálculo de distâncias/similaridade |
| 6 | Limpeza, integração, redução, transformação e discretização de dados | datasets com valores faltantes, ruído, outliers, duplicatas; múltiplas fontes para integrar |

O **encontro 7** é revisão/tira-dúvidas (sem conteúdo novo).

## Contexto do formato da disciplina

- 7 encontros síncronos semanais conduzidos por um **mediador pedagógico**.
- Os 6 primeiros encontros são estruturados em torno de uma **videoaula gravada** pelo professor
  conteudista (conteúdo estável: conceitos, fundamentos, teoria). No tempo restante do encontro,
  o mediador conduz **dinâmicas e exercícios de aprofundamento** — é exatamente aí que o material
  deste repositório é usado.
- Cada bloco de 1 hora tem um **checkpoint** associado.
- Há também **TDE** (Trabalho Discente Efetivo), atividades fora do horário de aula, limitadas a
  20% da carga horária.

### Ementa (PPC, não alterável)

> Visão geral sobre obtenção e transformação de dados. Compreensão e aplicação prática de técnicas
> de transformação de dados estruturados e não estruturados (pré-processamento). Aprofundamento em
> normalização de dados para tarefas de análise e aprendizado de máquina. Introdução a conceitos de
> dados na web. Aplicação de bibliotecas scraping, de análise numérica e manipulação vetorial de dados.

### Objetivos de aprendizagem

- Usar expressões regulares para extrair informações de arquivos em formato texto.
- Compreender o processo de webscraping para obtenção de informações da web.
- Compreender o processo de KDD (Knowledge Discovery in Databases) e suas etapas: preparação de
  dados, data warehousing, mineração de dados, visualização e interpretação de padrões.
- Compreender as técnicas e algoritmos de preparação de dados: imputação de valores faltantes,
  tratamento de ruídos, normalização, discretização, amostragem, análise de outliers.

### Avaliação

Nota mínima 6,0 — exercício online objetivo (4,5) + prova objetiva presencial (3,5) +
prova discursiva presencial (2,0). Frequência mínima de 75%.

## Convenções

- **Idioma**: conteúdo voltado ao aluno em **português (pt-BR)**.
- Os dados devem ser **realistas e didáticos**: preferir domínios concretos (vendas, clima, saúde,
  transporte público, e-commerce) a dados abstratos.
- Incluir deliberadamente **imperfeições** quando o tópico pedir (valores faltantes, encodings
  diferentes, datas em formatos mistos, duplicatas, outliers) — é isso que dá o que fazer no exercício.
- Páginas web devem ser **autocontidas** e servíveis localmente (`python -m http.server`) ou via
  GitHub Pages; não depender de sites de terceiros, que mudam e quebram os exercícios.
- Não usar dados pessoais reais; qualquer dado que pareça pessoal deve ser sintético.

## Publicação

O repositório é publicado via **GitHub Pages** em
`https://lucaskup.github.io/pucrs-coleta-e-preparacao/`
(remote: `git@github.com:lucaskup/pucrs-coleta-e-preparacao`).

- Existe um `.nojekyll` na raiz: o Jekyll não processa nada, então **não há listagem automática de
  diretório** — toda pasta que o aluno precisa acessar tem seu próprio `index.html`
  (`/index.html`, `/aula1/index.html`).
- Ao adicionar arquivos novos, incluir o link no `index.html` da aula correspondente.

## Decisões já tomadas (aula 1)

- Páginas-alvo de scraping usam **instituição e pessoas fictícias** ("Escola Politécnica —
  Universidade Aurora"), com e-mails no domínio reservado `example.edu`. Não clonar sites reais
  nem usar nomes de pessoas reais.
- A marcação HTML é **semântica e moderna** (`<article class="docente">`, `<h3 class="docente__nome">`),
  não a marcação `<b>` da página antiga da PUCRS. Os comandos da videoaula foram adaptados ao novo
  seletor e estão documentados em `aula1/README.md`.
- **A URL do slide 7 morreu**: `https://www.pucrs.br/politecnica/a-escola/professores/` hoje
  redireciona para uma notícia de 2018 e não tem nenhuma tag `<b>`. O slide precisa ser atualizado
  para apontar para a cópia estática.
- Os arquivos de dados reproduzem **os exemplos literais dos slides** (pequenos), acrescidos de
  variantes de codificação (UTF-8, ISO-8859-1, UTF-8 com BOM), CSV em padrão brasileiro
  (`;` e vírgula decimal) e JSON aninhado para `json_normalize`.

## Materiais de origem (fora do repositório)

Documentos institucionais em
`/mnt/g/Meu Drive/Documentos/cursos/gpo/Graduação Online/Coleta e Preparacao/2026/entrega/`:

- `01-GPO_TEMPLATE_plano_de_ensino.docx` — ementa, objetivos, cronograma, bibliografia
- `01-GPO_TEMPLATE_roteiro_de_aulas.docx` — roteiro das 6 videoaulas
- `01-GPO_TEMPLATE_guia_de_leitura.docx`
- `01-GPO_TEMPLATE_checkpoint_aula.pptx`

## Bibliografia

Básica:
- Prakash, K. B. (2022). *Data Science Handbook: A Practical Approach* (1st ed.). Wiley.
- Cremonini, M. (2024). *Data Science Fundamentals with R, Python, and Open Data* (1st ed.). Wiley.
- Cady, F. (2025). *The Data Science Handbook* (2nd ed.).

Complementar:
- Castro, L. N. de, & Ferrari, D. G. (2016). *Introdução à Mineração de Dados: Conceitos Básicos,
  Algoritmos e Aplicações*. Saraiva.
