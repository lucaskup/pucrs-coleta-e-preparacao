# Aula 6: Limpeza, integração, redução e transformação

Publicado em `https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula6/`. Tudo sintético, gerado
por `ferramentas/gerar_imoveis.py`.

| Arquivo | Conteúdo |
| --- | --- |
| `imoveis_aurora.csv` | cópia de `aula4/imoveis_aurora.csv` (mesmos problemas plantados) |
| `casa_sul.json` | 80 anúncios de outra imobiliária fictícia, com `dicionario` de campos |
| `bairros_poa.csv` | bairro → zona → cidade → UF (zona é um agrupamento didático simplificado) |

### Conflitos plantados em `casa_sul.json`

- preço em **milhares** (`valor_mil`); CS-120 veio em reais (conflito de unidade); CS-108 sem valor;
- `metragem` como texto (`"85m2"`); `condominio` como texto (`"R$ 1.170,00"`), `null` nas casas;
- `conservacao` codificada de 1 a 4; `pet` como `S`/`N`; `anunciado_em` em `mm/dd/aaaa`;
- bairros abreviados (`Moinhos`, `Cid. Baixa`, `Centro`, `Jd. Botânico`, `Passo da Areia`…);
- logradouro abreviado (`R.`, `Av.`, `Tv.`), às vezes sem acento e sem vírgula;
- comodidades em maiúsculas e sem acento;
- **15 imóveis anunciados nas duas imobiliárias**, com preços até 5% diferentes. Com *blocking*
  por (bairro, quartos), Jaccard de bigramas do endereço ≥ 0,8 e área ±2 m², saem os 15 pares.


---

## Prática do encontro síncrono 6

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula6/pratica/encontro6.ipynb)

`pratica/encontro6.ipynb`: notebook da atividade conduzida pelo mediador. O gabarito fica fora
deste repositório e é distribuído ao mediador junto com os slides do encontro.

Estações (limpeza, outliers, integração, transformação e redução) com diário de decisões, e uma
caça a vazamentos de dados em um pipeline de colega (estatísticas calculadas antes da divisão
treino/teste e atributo derivado do alvo).
