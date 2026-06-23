## 2.7. Funções agregadas [#](#TUTORIAL-AGG)

Como a maioria dos outros produtos de banco de dados relacionais, o PostgreSQL suporta funções agregadas. Uma função agregada calcula um único resultado a partir de várias linhas de entrada. Por exemplo, existem agregados para calcular o `count`, `sum`, `avg` (média), `max` (máximo) e `min` (mínimo) sobre um conjunto de linhas.

Como exemplo, podemos encontrar a leitura da menor temperatura em qualquer lugar com:

```
SELECT max(temp_lo) FROM weather;
```

```
 max
-----
  46
(1 row)
```

Se quiséssemos saber em que cidade (ou cidades) ocorreu essa leitura, poderíamos tentar:

```
SELECT city FROM weather WHERE temp_lo = max(temp_lo);     -- WRONG
```

Mas isso não funcionará, pois o agregado `max` não pode ser usado na cláusula `WHERE`. (Essa restrição existe porque a cláusula `WHERE` determina quais linhas serão incluídas no cálculo do agregado; portanto, obviamente, ela deve ser avaliada antes que as funções agregadas sejam calculadas). No entanto, como é comum, a consulta pode ser reformulada para obter o resultado desejado, aqui usando uma *subconsulta*:

```
SELECT city FROM weather
    WHERE temp_lo = (SELECT max(temp_lo) FROM weather);
```

```
     city
---------------
 San Francisco
(1 row)
```

Isso está bem, porque a subconsulta é um cálculo independente que calcula seu próprio agregado separadamente do que está acontecendo na consulta externa.

Os agregados também são muito úteis em combinação com cláusulas `GROUP BY`. Por exemplo, podemos obter o número de leituras e a temperatura mínima máxima observada em cada cidade com:

```
SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city;
```

```
     city      | count | max
---------------+-------+-----
 Hayward       |     1 |  37
 San Francisco |     2 |  46
(2 rows)
```

que nos dá uma linha de saída por cidade. Cada resultado agregado é calculado sobre as linhas da tabela que correspondem a essa cidade. Podemos filtrar essas linhas agrupadas usando `HAVING`:

```
SELECT city, count(*), max(temp_lo)
    FROM weather
    GROUP BY city
    HAVING max(temp_lo) < 40;
```

```
  city   | count | max
---------+-------+-----
 Hayward |     1 |  37
(1 row)
```

que nos dá os mesmos resultados apenas para as cidades que têm todos os valores `temp_lo` abaixo de 40. Finalmente, se só nos importa que as cidades cujos nomes comecem com “`S`”, podemos fazer:

```
SELECT city, count(*), max(temp_lo)
    FROM weather
    WHERE city LIKE 'S%'            -- (1)
    GROUP BY city;
```

```
     city      | count | max
---------------+-------+-----
 San Francisco |     2 |  46
(1 row)
```



<table border="0" summary="Callout list">
 <tr>
  <td align="left" valign="top" width="5%">
   <p>
    <a href="#co.tutorial-agg-like">
     (1)
    </a>
   </p>
  </td>
  <td align="left" valign="top">
   <p>
    O
    <code class="literal">
     LIKE
    </code>
    o operador faz correspondência de padrões e é explicado em
    <a class="xref" href="functions-matching.md" title="9.7. Pattern Matching">
     Seção 9.7
    </a>
    .
   </p>
  </td>
 </tr>
</table>







É importante entender a interação entre agregados e as cláusulas `WHERE` e `HAVING` do SQL. A diferença fundamental entre `WHERE` e `HAVING` é esta: `WHERE` seleciona linhas de entrada antes que grupos e agregados sejam calculados (assim, controla quais linhas serão usadas na computação agregada), enquanto `HAVING` seleciona linhas de grupo após os grupos e agregados serem calculados. Assim, a cláusula `WHERE` não deve conter funções agregadas; não faz sentido tentar usar um agregado para determinar quais linhas serão entradas para os agregados. Por outro lado, a cláusula `HAVING` sempre contém funções agregadas. (Estritamente falando, você pode escrever uma cláusula `HAVING` que não use agregados, mas raramente é útil. A mesma condição poderia ser usada de forma mais eficiente na etapa `WHERE`).

No exemplo anterior, podemos aplicar a restrição do nome da cidade em `WHERE`, uma vez que não precisa de agregação. Isso é mais eficiente do que adicionar a restrição em `HAVING`, porque evitamos realizar os cálculos de agrupamento e agregação para todas as linhas que falham na verificação de `WHERE`.

Outra maneira de selecionar as linhas que entram em uma computação agregada é usar `FILTER`, que é uma opção por agregado:

```
SELECT city, count(*) FILTER (WHERE temp_lo < 45), max(temp_lo)
    FROM weather
    GROUP BY city;
```

```
     city      | count | max
---------------+-------+-----
 Hayward       |     1 |  37
 San Francisco |     1 |  46
(2 rows)
```

`FILTER` é muito semelhante a `WHERE`, exceto que ele remove linhas apenas da entrada da função agregada específica a que está anexado. Aqui, o agregado `count` conta apenas as linhas com `temp_lo` abaixo de 45; mas o agregado `max` ainda é aplicado a todas as linhas, então ele ainda encontra a leitura de 46.