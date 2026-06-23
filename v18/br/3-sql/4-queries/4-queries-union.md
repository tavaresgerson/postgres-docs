## 7.4. Combinando Perguntas (`UNION`, `INTERSECT`, `EXCEPT`) [#](#QUERIES-UNION)

Os resultados de duas consultas podem ser combinados usando as operações de conjunto união, interseção e diferença. A sintaxe é

```
query1 UNION [ALL] query2
query1 INTERSECT [ALL] query2
query1 EXCEPT [ALL] query2
```

onde *`query1`* e *`query2`* são consultas que podem usar qualquer uma das características discutidas até este ponto.

`UNION` efetivamente anexa o resultado de *`query2`* ao resultado de *`query1`* (embora não haja garantia de que essa seja a ordem em que as linhas são de fato retornadas). Além disso, ele elimina as linhas duplicadas de seu resultado, da mesma forma que `DISTINCT`, a menos que `UNION ALL` seja usado.

`INTERSECT` retorna todas as linhas que estão tanto no resultado de *`query1`* quanto no resultado de *`query2`*. As linhas duplicadas são eliminadas, a menos que `INTERSECT ALL` seja usado.

`EXCEPT` retorna todas as linhas que estão no resultado de *`query1`*, mas não no resultado de *`query2`*. (Isso é chamado às vezes de *diferença* entre duas consultas.) Novamente, os duplicados são eliminados, a menos que `EXCEPT ALL` seja usado.

Para calcular a união, interseção ou diferença de duas consultas, as duas consultas devem ser "compatíveis em união", o que significa que elas retornam o mesmo número de colunas e os tipos de dados correspondentes têm tipos de dados compatíveis, conforme descrito em [Seção 10.5](typeconv-union-case.md).

As operações de configuração podem ser combinadas, por exemplo

```
query1 UNION query2 EXCEPT query3
```

que é equivalente a

```
(query1 UNION query2) EXCEPT query3
```

Como mostrado aqui, você pode usar parênteses para controlar a ordem de avaliação. Sem parênteses, `UNION` e `EXCEPT` associam da esquerda para a direita, mas `INTERSECT` se liga mais firmemente do que esses dois operadores. Assim

```
query1 UNION query2 INTERSECT query3
```

significa

```
query1 UNION (query2 INTERSECT query3)
```

Você também pode envolver um indivíduo *`query`* entre parênteses. Isso é importante se o *`query`* precisar usar alguma das cláusulas discutidas nas seções seguintes, como `LIMIT`. Sem parênteses, você receberá um erro de sintaxe, ou, caso contrário, a cláusula será entendida como aplicando-se à saída da operação de conjunto, e não a um de seus inputs. Por exemplo,

```
SELECT a FROM b UNION SELECT x FROM y LIMIT 10
```

é aceito, mas isso significa

```
(SELECT a FROM b UNION SELECT x FROM y) LIMIT 10
```

não

```
SELECT a FROM b UNION (SELECT x FROM y LIMIT 10)
```
