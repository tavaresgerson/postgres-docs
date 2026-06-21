## 69.2. Exemplos de Estatística Multivariada [#](#MULTIVARIATE-STATISTICS-EXAMPLES)

* [69.2.1. Dependências Funcionais](multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES)
* [69.2.2. Contagem Múltipla N-Distanta](multivariate-statistics-examples.md#MULTIVARIATE-NDISTINCT-COUNTS)
* [69.2.3. Listas de MCV](multivariate-statistics-examples.md#MCV-LISTS)

### 69.2.1. Dependências Funcionais [#](#FUNCTIONAL-DEPENDENCIES)

A correlação multivariada pode ser demonstrada com um conjunto de dados muito simples — uma tabela com duas colunas, ambas contendo os mesmos valores:

```
CREATE TABLE t (a INT, b INT);
INSERT INTO t SELECT i % 100, i % 100 FROM generate_series(1, 10000) s(i);
ANALYZE t;
```

Como explicado na [Seção 14.2][(planner-stats.md "14.2. Statistics Used by the Planner")], o planejador pode determinar a cardinalidade do `t` usando o número de páginas e linhas obtidas do `pg_class`:

```
SELECT relpages, reltuples FROM pg_class WHERE relname = 't';

 relpages | reltuples
----------+-----------
       45 |     10000
```

A distribuição dos dados é muito simples; há apenas 100 valores distintos em cada coluna, distribuídos uniformemente.

O exemplo a seguir mostra o resultado da estimativa de uma condição `WHERE` na coluna `a`:

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1;
                                 QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..170.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: (a = 1)
   Rows Removed by Filter: 9900
```

O planejador examina a condição e determina que a seletividade desta cláusula é de 1%. Ao comparar essa estimativa com o número real de linhas, vemos que a estimativa é muito precisa (de fato exata, pois a tabela é muito pequena). Alterando a condição `WHERE` para usar a coluna `b`, um plano idêntico é gerado. Mas observe o que acontece se aplicarmos a mesma condição em ambas as colunas, combinando-as com `AND`:

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                 QUERY PLAN
-------------------------------------------------------------------​----------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

O planejador estima a seletividade para cada condição individualmente, chegando às mesmas estimativas de 1% mencionadas acima. Em seguida, assume que as condições são independentes, e, portanto, multiplica suas seletividades, produzindo uma estimativa final de seletividade de apenas 0,01%. Esse é um subestime significativo, pois o número real de linhas que correspondem às condições (100) é duas ordens de magnitude maior.

Esse problema pode ser resolvido criando um objeto de estatísticas que direcione `ANALYZE` para calcular estatísticas multivariadas de dependência funcional nas duas colunas:

```
CREATE STATISTICS stts (dependencies) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                  QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..195.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

### 69.2.2. Contagem N-distinta multivariada [#](#MULTIVARIATE-NDISTINCT-COUNTS)

Um problema semelhante ocorre com a estimativa da cardinalidade de conjuntos de múltiplas colunas, como o número de grupos que seriam gerados por uma cláusula `GROUP BY`. Quando `GROUP BY` lista uma única coluna, a estimativa n-distinta (que é visível como o número estimado de linhas devolvidas pelo nó HashAggregate) é muito precisa:

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a;
                                       QUERY PLAN
-------------------------------------------------------------------​----------------------
 HashAggregate  (cost=195.00..196.00 rows=100 width=12) (actual rows=100.00 loops=1)
   Group Key: a
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=4) (actual rows=10000.00 loops=1)
```

Mas sem estatísticas multivariadas, a estimativa para o número de grupos em uma consulta com duas colunas em `GROUP BY`, como no exemplo a seguir, está errada em uma ordem de magnitude:

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a, b;
                                       QUERY PLAN
-------------------------------------------------------------------​-------------------------
 HashAggregate  (cost=220.00..230.00 rows=1000 width=16) (actual rows=100.00 loops=1)
   Group Key: a, b
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=8) (actual rows=10000.00 loops=1)
```

Ao redefinir o objeto de estatísticas para incluir contagens n-distintas para as duas colunas, a estimativa é muito melhorada:

```
DROP STATISTICS stts;
CREATE STATISTICS stts (dependencies, ndistinct) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT COUNT(*) FROM t GROUP BY a, b;
                                       QUERY PLAN
-------------------------------------------------------------------​-------------------------
 HashAggregate  (cost=220.00..221.00 rows=100 width=16) (actual rows=100.00 loops=1)
   Group Key: a, b
   ->  Seq Scan on t  (cost=0.00..145.00 rows=10000 width=8) (actual rows=10000.00 loops=1)
```

### 69.2.3. Listas de MCV [#](#MCV-LISTS)

Como explicado na [Seção 69.2.1][(multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES "69.2.1. Functional Dependencies")], as dependências funcionais são um tipo de estatísticas muito econômico e eficiente, mas sua principal limitação é sua natureza global (apenas rastreando dependências no nível da coluna, não entre valores individuais de coluna).

Esta seção apresenta uma variante multivariada das listas de valores MCV (valores mais comuns), uma extensão direta das estatísticas por coluna descritas em [Seção 69.1] (row-estimation-examples.md "69.1. Row Estimation Examples"). Essas estatísticas abordam a limitação ao armazenar valores individuais, mas naturalmente é mais caro, tanto em termos de construção das estatísticas em `ANALYZE`, armazenamento e tempo de planejamento.

Vamos analisar a consulta da [Seção 69.2.1][(multivariate-statistics-examples.md#FUNCTIONAL-DEPENDENCIES "69.2.1. Functional Dependencies")] novamente, mas desta vez com uma lista MCV criada no mesmo conjunto de colunas (tenha certeza de que as dependências funcionais sejam descartadas, para garantir que o planejador use as estatísticas recém-criadas).

```
DROP STATISTICS stts;
CREATE STATISTICS stts2 (mcv) ON a, b FROM t;
ANALYZE t;
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 1;
                                   QUERY PLAN
-------------------------------------------------------------------​------------
 Seq Scan on t  (cost=0.00..195.00 rows=100 width=8) (actual rows=100.00 loops=1)
   Filter: ((a = 1) AND (b = 1))
   Rows Removed by Filter: 9900
```

A estimativa é tão precisa quanto com as dependências funcionais, principalmente graças à tabela ser relativamente pequena e ter uma distribuição simples com um número baixo de valores distintos. Antes de analisar a segunda consulta, que não foi tratada particularmente bem pelas dependências funcionais, vamos inspecionar um pouco a lista MCV.

A inspeção da lista MCV é possível usando a função de retorno de conjunto `pg_mcv_list_items`.

```
SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts2';
 index |  values  | nulls | frequency | base_frequency
-------+----------+-------+-----------+----------------
     0 | {0, 0}   | {f,f} |      0.01 |         0.0001
     1 | {1, 1}   | {f,f} |      0.01 |         0.0001
   ...
    49 | {49, 49} | {f,f} |      0.01 |         0.0001
    50 | {50, 50} | {f,f} |      0.01 |         0.0001
   ...
    97 | {97, 97} | {f,f} |      0.01 |         0.0001
    98 | {98, 98} | {f,f} |      0.01 |         0.0001
    99 | {99, 99} | {f,f} |      0.01 |         0.0001
(100 rows)
```

Isso confirma que há 100 combinações distintas nas duas colunas, e todas elas são igualmente prováveis (frequência de 1% para cada uma). A frequência base é a frequência calculada a partir das estatísticas por coluna, como se não houvesse estatísticas de múltiplas colunas. Se houvesse algum valor nulo em qualquer uma das colunas, isso seria identificado na coluna `nulls`.

Ao estimar a seletividade, o planejador aplica todas as condições sobre os itens da lista MCV e, em seguida, soma as frequências dos que correspondem. Veja `mcv_clauselist_selectivity` em `src/backend/statistics/mcv.c` para detalhes.

Em comparação com as dependências funcionais, as listas MCV têm duas vantagens principais. Em primeiro lugar, a lista armazena valores reais, o que permite decidir quais combinações são compatíveis.

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a = 1 AND b = 10;
                                 QUERY PLAN
-------------------------------------------------------------------​--------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=0.00 loops=1)
   Filter: ((a = 1) AND (b = 10))
   Rows Removed by Filter: 10000
```

Em segundo lugar, as listas MCV lidam com uma gama mais ampla de tipos de cláusulas, não apenas cláusulas de igualdade, como dependências funcionais. Por exemplo, considere a seguinte consulta de intervalo para a mesma tabela:

```
EXPLAIN (ANALYZE, TIMING OFF, BUFFERS OFF) SELECT * FROM t WHERE a <= 49 AND b > 49;
                                QUERY PLAN
-------------------------------------------------------------------​--------
 Seq Scan on t  (cost=0.00..195.00 rows=1 width=8) (actual rows=0.00 loops=1)
   Filter: ((a <= 49) AND (b > 49))
   Rows Removed by Filter: 10000
```
