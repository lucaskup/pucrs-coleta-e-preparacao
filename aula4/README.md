# Aula 4 — KDD, tipos de dados e estatística descritiva

Publicado em `https://lucaskup.github.io/pucrs-coleta-e-preparacao/aula4/`.

## `imoveis_aurora.csv`

Base **sintética** de anúncios da imobiliária fictícia Aurora Imóveis (Porto Alegre). Os bairros
existem; preços, endereços, CEPs e anúncios são inventados. Gerada por `ferramentas/gerar_imoveis.py`.

| Coluna | Armazenado como | Nível de medição |
| --- | --- | --- |
| `codigo` | texto | nominal (identificador) |
| `tipo`, `bairro`, `zona` | texto | nominal |
| `cep` | **inteiro** | **nominal** (código) |
| `endereco` | texto | nominal (texto livre) |
| `preco`, `area_m2`, `iptu_anual` | float | razão |
| `quartos`, `banheiros`, `vagas` | inteiro | razão (contagem) |
| `condominio` | float | razão — `0` nas casas é zero estrutural (isenta), vazio é ausência |
| `ano_construcao` | inteiro | intervalar |
| `andar` | float | ordinal/intervalar (discutível); vazio nas casas |
| `conservacao` | texto | ordinal |
| `aceita_pet` | texto | nominal binário |
| `comodidades` | texto separado por `;` | conjunto → binários assimétricos |
| `data_anuncio` | texto ISO | intervalar |

### Problemas plantados (o "gabarito" da EDA)

- 6 linhas duplicadas por inteiro (306 linhas, 300 imóveis);
- `ano_construcao = 0` em 8 linhas (sentinela);
- `condominio` vazio em 15 apartamentos, 12 deles de prédios anteriores a 1990 (ausência MAR);
- `preco` vazio em 3 anúncios (sob consulta);
- AUR-0060: preço com um zero a mais (R$ 14,56 mi); AUR-0199: área ×10 (670 m²);
  AUR-0147: área de 3,2 m²; AUR-0110: `quartos = -2`;
- `conservacao` com `otimo` (4) e `BOM` (3); `bairro` com `Petropolis` sem acento (2).

Efeito didático: a correlação de Pearson entre `preco` e `iptu_anual` é 0,62 com o erro de
AUR-0060 e 0,96 sem ele.


---

## Prática do encontro síncrono 4

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula4/pratica/encontro4.ipynb)

`pratica/encontro4.ipynb` — notebook da atividade conduzida pelo mediador. O gabarito **não** fica
neste repositório (é distribuído ao mediador junto com os slides do encontro).

Classificar os atributos, revisar a análise de um colega (CEP médio, idade média com sentinela,
média de ordinal, CV de atributo intervalar, Pearson sobre códigos de bairro…) e seguir o roteiro de
EDA da videoaula, com cada grupo aprofundando uma etapa.
