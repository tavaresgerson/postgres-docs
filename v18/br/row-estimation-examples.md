## 69.1. Exemplos de Estimação de Linha [#](#ROW-ESTIMATION-EXAMPLES)

Os exemplos mostrados abaixo utilizam tabelas no banco de dados de teste de regressão do PostgreSQL. Observe também que, uma vez que `ANALYZE` utiliza amostragem aleatória ao produzir estatísticas, os resultados mudarão ligeiramente após qualquer nova `ANALYZE`.

Vamos começar com uma pergunta muito simples:

```
EXPLAIN SELECT * FROM tenk1;

                         QUERY PLAN
-------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..458.00 rows=10000 width=244)
```

Como o planejador determina a cardinalidade de `tenk1` é abordado na [Seção 14.2](planner-stats.md "14.2. Statistics Used by the Planner"), mas é repetido aqui para completude. O número de páginas e linhas é procurado em `pg_class`:

```
SELECT relpages, reltuples FROM pg_class WHERE relname = 'tenk1';

 relpages | reltuples
----------+-----------
      358 |     10000
```

Esses números são atuais a partir da última `VACUUM` ou `ANALYZE` na tabela. O planejador, em seguida, obtém o número atual real de páginas na tabela (esta é uma operação barata, que não requer uma varredura da tabela). Se isso for diferente de `relpages`, então `reltuples` é ajustado conforme necessário para chegar a uma estimativa do número de linhas atual. No exemplo acima, o valor de `relpages` está atualizado, então a estimativa de linhas é a mesma que `reltuples`.

Vamos passar para um exemplo com uma condição de intervalo na sua cláusula `WHERE`:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 1000;

                                   QUERY PLAN
-------------------------------------------------------------------​-------------
 Bitmap Heap Scan on tenk1  (cost=24.06..394.64 rows=1007 width=244)
   Recheck Cond: (unique1 < 1000)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..23.80 rows=1007 width=0)
         Index Cond: (unique1 < 1000)
```

O planejador examina a condição da cláusula `WHERE` e busca a função de seletividade para o operador `<` em `pg_operator`. Isso é mantido na coluna `oprrest`, e a entrada neste caso é `scalarltsel`. A função `scalarltsel` recupera o histograma para `unique1` a partir de `pg_statistic`. Para consultas manuais, é mais conveniente olhar na visão mais simples `pg_stats`:

```
SELECT histogram_bounds FROM pg_stats
WHERE tablename='tenk1' AND attname='unique1';

                   histogram_bounds
------------------------------------------------------
 {0,993,1997,3050,4040,5036,5957,7057,8029,9016,9995}
```

Em seguida, a fração do histograma ocupada por “< 1000” é calculada. Esta é a seletividade. O histograma divide a faixa em compartimentos de frequência iguais, então tudo o que temos que fazer é localizar o compartimento em que nosso valor está e contar *parte* dele e *todos* dos que vêm antes. O valor 1000 está claramente no segundo compartimento (993–1997). Supondo uma distribuição linear dos valores dentro de cada compartimento, podemos calcular a seletividade como:

```
selectivity = (1 + (1000 - bucket[2].min)/(bucket[2].max - bucket[2].min))/num_buckets
            = (1 + (1000 - 993)/(1997 - 993))/10
            = 0.100697
```

Ou seja, um balde inteiro mais uma fração linear do segundo, dividido pelo número de baldes. O número estimado de linhas pode agora ser calculado como o produto da seletividade e da cardinalidade de `tenk1`:

```
rows = rel_cardinality * selectivity
     = 10000 * 0.100697
     = 1007  (rounding off)
```

Em seguida, vamos considerar um exemplo com uma condição de igualdade na sua cláusula `WHERE`:

```
EXPLAIN SELECT * FROM tenk1 WHERE stringu1 = 'CRAAAA';

                        QUERY PLAN
----------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=30 width=244)
   Filter: (stringu1 = 'CRAAAA'::name)
```

Novamente, o planejador examina a condição da cláusula `WHERE` e procura a função de seletividade para `=`, que é `eqsel`. Para a estimativa de igualdade, o histograma não é útil; em vez disso, a lista dos *valores mais comuns* (MCVs) é usada para determinar a seletividade. Vamos dar uma olhada nos MCVs, com algumas colunas adicionais que serão úteis mais tarde:

```
SELECT null_frac, n_distinct, most_common_vals, most_common_freqs FROM pg_stats
WHERE tablename='tenk1' AND attname='stringu1';

null_frac         | 0
n_distinct        | 676
most_common_vals  | {EJAAAA,BBAAAA,CRAAAA,FCAAAA,FEAAAA,GSAAAA,​JOAAAA,MCAAAA,NAAAAA,WGAAAA}
most_common_freqs | {0.00333333,0.003,0.003,0.003,0.003,0.003,​0.003,0.003,0.003,0.003}
```

Como o `CRAAAA` aparece na lista de MCVs, a seletividade é meramente a entrada correspondente na lista das frequências mais comuns (MCFs):

```
selectivity = mcf[3]
            = 0.003
```

Como antes, o número estimado de linhas é apenas o produto disso com a cardinalidade de `tenk1`:

```
rows = 10000 * 0.003
     = 30
```

Agora, considere a mesma consulta, mas com uma constante que não está na lista MCV:

```
EXPLAIN SELECT * FROM tenk1 WHERE stringu1 = 'xxx';

                        QUERY PLAN
----------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=15 width=244)
   Filter: (stringu1 = 'xxx'::name)
```

Este é um problema bastante diferente: como estimar a seletividade quando o valor *não* está na lista de MCV. A abordagem é usar o fato de que o valor não está na lista, combinado com o conhecimento das frequências para todos os MCVs:

```
selectivity = (1 - sum(mcv_freqs))/(num_distinct - num_mcv)
            = (1 - (0.00333333 + 0.003 + 0.003 + 0.003 + 0.003 + 0.003 +
                    0.003 + 0.003 + 0.003 + 0.003))/(676 - 10)
            = 0.0014559
```

Ou seja, some todas as frequências dos MCVs e subtraia-as de um, depois divida por o número de *outros* valores distintos. Isso equivale a assumir que a fração da coluna que não é nenhum dos MCVs está distribuída de forma uniforme entre todos os outros valores distintos. Observe que não há valores nulos, então não precisamos nos preocupar com esses (caso contrário, também subtrairiamos a fração nula do numerador). O número estimado de linhas é então calculado como de costume:

```
rows = 10000 * 0.0014559
     = 15  (rounding off)
```

O exemplo anterior com `unique1 < 1000` foi uma simplificação excessiva do que realmente faz `scalarltsel`; agora que vimos um exemplo do uso de MCVs, podemos preencher alguns detalhes a mais. O exemplo estava correto na medida em que foi, porque, como `unique1` é uma coluna única, não tem MCVs (obviamente, nenhum valor é mais comum do que qualquer outro valor). Para uma coluna não única, normalmente haverá tanto um histograma quanto uma lista de MCVs, e *o histograma não inclui a porção da população da coluna representada pelos MCVs*. Fazemos as coisas dessa maneira porque isso permite uma estimativa mais precisa. Nesta situação, `scalarltsel` aplica diretamente a condição (por exemplo, “< 1000”) a cada valor da lista de MCVs e soma as frequências dos MCVs para os quais a condição é verdadeira. Isso dá uma estimativa exata da seletividade na porção da tabela que é MCVs. O histograma é então usado da mesma maneira que acima para estimar a seletividade na porção da tabela que não é MCVs, e então os dois números são combinados para estimar a seletividade geral. Por exemplo, considere

```
EXPLAIN SELECT * FROM tenk1 WHERE stringu1 < 'IAAAAA';

                         QUERY PLAN
------------------------------------------------------------
 Seq Scan on tenk1  (cost=0.00..483.00 rows=3077 width=244)
   Filter: (stringu1 < 'IAAAAA'::name)
```

Já vimos as informações do MCV para `stringu1`, e aqui está seu histograma:

```
SELECT histogram_bounds FROM pg_stats
WHERE tablename='tenk1' AND attname='stringu1';

                                histogram_bounds
-------------------------------------------------------------------​-------------
 {AAAAAA,CQAAAA,FRAAAA,IBAAAA,KRAAAA,NFAAAA,PSAAAA,SGAAAA,VAAAAA,​XLAAAA,ZZAAAA}
```

Ao verificar a lista MCV, descobrimos que a condição `stringu1 < 'IAAAAA'` é satisfeita pelas primeiras seis entradas e não pelas últimas quatro, portanto, a seletividade dentro da parte MCV da população é

```
selectivity = sum(relevant mvfs)
            = 0.00333333 + 0.003 + 0.003 + 0.003 + 0.003 + 0.003
            = 0.01833333
```

Somando todos os MCFs também nos diz que a fração total da população representada pelos MCVs é de 0,03033333, e, portanto, a fração representada pelo histograma é de 0,96966667 (novamente, não há nulos, caso contrário, teríamos que excluí-los aqui). Podemos ver que o valor `IAAAAA` cai quase no final do terceiro cache do histograma. Usando algumas suposições bastante sem graça sobre a frequência de diferentes caracteres, o planejador chega à estimativa de 0,298387 para a porção da população do histograma que é menor que `IAAAAA`. Em seguida, combinamos as estimativas para as populações de MCV e não-MCV:

```
selectivity = mcv_selectivity + histogram_selectivity * histogram_fraction
            = 0.01833333 + 0.298387 * 0.96966667
            = 0.307669

rows        = 10000 * 0.307669
            = 3077  (rounding off)
```

Neste exemplo específico, a correção da lista de MCV é bastante pequena, porque a distribuição da coluna é, na verdade, bastante plana (as estatísticas que mostram esses valores específicos como sendo mais comuns do que outros são, na maioria das vezes, devido a erro de amostragem). Em um caso mais típico, onde alguns valores são significativamente mais comuns do que outros, esse processo complicado oferece uma melhoria útil na precisão, porque a seletividade para os valores mais comuns é encontrada exatamente.

Agora, vamos considerar um caso com mais de uma condição na cláusula `WHERE`:

```
EXPLAIN SELECT * FROM tenk1 WHERE unique1 < 1000 AND stringu1 = 'xxx';

                                   QUERY PLAN
-------------------------------------------------------------------​-------------
 Bitmap Heap Scan on tenk1  (cost=23.80..396.91 rows=1 width=244)
   Recheck Cond: (unique1 < 1000)
   Filter: (stringu1 = 'xxx'::name)
   ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..23.80 rows=1007 width=0)
         Index Cond: (unique1 < 1000)
```

O planejador assume que as duas condições são independentes, de modo que as seletividades individuais das cláusulas podem ser multiplicadas juntas:

```
selectivity = selectivity(unique1 < 1000) * selectivity(stringu1 = 'xxx')
            = 0.100697 * 0.0014559
            = 0.0001466

rows        = 10000 * 0.0001466
            = 1  (rounding off)
```

Observe que o número de linhas estimado para ser retornado da varredura do índice em bitmap reflete apenas a condição usada com o índice; isso é importante, pois afeta a estimativa do custo para as subsequentes fetches do heap.

Por fim, examinaremos uma consulta que envolve uma junção:

```
EXPLAIN SELECT * FROM tenk1 t1, tenk2 t2
WHERE t1.unique1 < 50 AND t1.unique2 = t2.unique2;

                                      QUERY PLAN
-------------------------------------------------------------------​-------------------
 Nested Loop  (cost=4.64..456.23 rows=50 width=488)
   ->  Bitmap Heap Scan on tenk1 t1  (cost=4.64..142.17 rows=50 width=244)
         Recheck Cond: (unique1 < 50)
         ->  Bitmap Index Scan on tenk1_unique1  (cost=0.00..4.63 rows=50 width=0)
               Index Cond: (unique1 < 50)
   ->  Index Scan using tenk2_unique2 on tenk2 t2  (cost=0.00..6.27 rows=1 width=244)
         Index Cond: (unique2 = t1.unique2)
```

A restrição em `tenk1`, `unique1 < 50`, é avaliada antes da junção de laço aninhado. Isso é tratado de forma análoga ao exemplo anterior de intervalo. Desta vez, o valor 50 cai no primeiro compartimento do histograma `unique1`:

```
selectivity = (0 + (50 - bucket[1].min)/(bucket[1].max - bucket[1].min))/num_buckets
            = (0 + (50 - 0)/(993 - 0))/10
            = 0.005035

rows        = 10000 * 0.005035
            = 50  (rounding off)
```

A restrição para a junção é `t2.unique2 = t1.unique2`. O operador é apenas o nosso familiar `=`, no entanto, a função de seletividade é obtida a partir da coluna `oprjoin` de `pg_operator`, e é `eqjoinsel`. `eqjoinsel` procura as informações estatísticas para ambos os `tenk2` e `tenk1`:

```
SELECT tablename, null_frac,n_distinct, most_common_vals FROM pg_stats
WHERE tablename IN ('tenk1', 'tenk2') AND attname='unique2';

tablename  | null_frac | n_distinct | most_common_vals
-----------+-----------+------------+------------------
 tenk1     |         0 |         -1 |
 tenk2     |         0 |         -1 |
```

Neste caso, não há informações sobre MCV para `unique2` e todos os valores parecem ser únicos (n_distinct = -1), então usamos um algoritmo que depende das estimativas do número de linhas para ambas as relações (num_rows, não mostrado, mas "tenk") juntamente com as frações de nulidade da coluna (zero para ambas):

```
selectivity = (1 - null_frac1) * (1 - null_frac2) / max(num_rows1, num_rows2)
            = (1 - 0) * (1 - 0) / max(10000, 10000)
            = 0.0001
```

Isso é, subtraia a fração nula de um para cada uma das relações, e divida pelo número de linhas da relação maior (esse valor é escalado no caso não único). O número de linhas que a junção provavelmente emitirá é calculado como a cardinalidade do produto cartesiano dos dois inputs, multiplicado pela seletividade:

```
rows = (outer_cardinality * inner_cardinality) * selectivity
     = (50 * 10000) * 0.0001
     = 50
```

Se houvesse listas de MCV para as duas colunas, o `eqjoinsel` teria utilizado a comparação direta das listas de MCV para determinar a seletividade de junção dentro da parte das populações da coluna representadas pelos MCVs. A estimativa para o restante das populações segue a mesma abordagem mostrada aqui.

Observe que mostramos `inner_cardinality` como 10000, ou seja, o tamanho não modificado de `tenk2`. Pode parecer, após a inspeção da saída do `EXPLAIN`, que a estimativa das linhas de junção vem de 50 * 1, ou seja, o número de linhas externas vezes o número estimado de linhas obtido por cada varredura de índice interno no `tenk2`. Mas isso não é o caso: o tamanho da relação de junção é estimado antes de qualquer plano de junção específico ter sido considerado. Se tudo estiver funcionando bem, então as duas maneiras de estimar o tamanho da junção produzirão uma resposta aproximadamente a mesma, mas devido ao erro de arredondamento e outros fatores, às vezes, divergem significativamente.

Para aqueles interessados em obter mais detalhes, a estimativa do tamanho de uma tabela (antes de quaisquer cláusulas `WHERE`) é feita em `src/backend/optimizer/util/plancat.c`. A lógica genérica para seletividade de cláusula está em `src/backend/optimizer/path/clausesel.c`. As funções de seletividade específicas para operadores são encontradas principalmente em `src/backend/utils/adt/selfuncs.c`.