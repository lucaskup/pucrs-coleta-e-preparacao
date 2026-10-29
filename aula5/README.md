# Aula 5 — Visualização, similaridade e pré-processamento

A prática usa a base `../aula4/imoveis_aurora.csv`.


---

## Prática do encontro síncrono 5

[![Abrir no Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/lucaskup/pucrs-coleta-e-preparacao/blob/main/aula5/pratica/encontro5.ipynb)

`pratica/encontro5.ipynb` — notebook da atividade conduzida pelo mediador. O gabarito **não** fica
neste repositório (é distribuído ao mediador junto com os slides do encontro).

- **Parte A:** cinco gráficos enganosos para diagnosticar e refazer (eixo truncado em barras, pizza
  com 16 fatias, histograma com 3 bins, linha ligando categorias, mapa de calor com `jet`).
- **Parte B:** imóveis parecidos com AUR-0137 por cinco medidas (Euclidiana, Euclidiana com z-score,
  Jaccard, SMC, Gower). Os top-5 praticamente não se sobrepõem: a medida define o que é "parecido".
