### 2.5. Consultando uma tabela [#](#TUTORIAL-SELECT)

Para recuperar dados de uma tabela, a tabela é *consultada*. Uma declaração SQL `SELECT` é usada para isso. A declaração é dividida em uma lista de seleção (a parte que lista as colunas a serem retornadas), uma lista de tabelas (a parte que lista as tabelas de onde se deve recuperar os dados) e uma qualificação opcional (a parte que especifica quaisquer restrições). Por exemplo, para recuperar todas as linhas da tabela `weather`, digite:

```
SELECT * FROM weather;
```

Aqui `*` é uma abreviação para “todas as colunas”. [[2]](#ftn.id-1.4.4.6.2.10) Assim, o mesmo resultado seria obtido com:

```
SELECT city, temp_lo, temp_hi, prcp, date FROM weather;
```

A saída deve ser:

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
 San Francisco |      43 |      57 |    0 | 1994-11-29
 Hayward       |      37 |      54 |      | 1994-11-29
(3 rows)
```

Você pode escrever expressões, não apenas referências simples de coluna, na lista de seleção. Por exemplo, você pode fazer:

```
SELECT city, (temp_hi+temp_lo)/2 AS temp_avg, date FROM weather;
```

Isso deve dar:

```
     city      | temp_avg |    date
---------------+----------+------------
 San Francisco |       48 | 1994-11-27
 San Francisco |       50 | 1994-11-29
 Hayward       |       45 | 1994-11-29
(3 rows)
```

Observe como a cláusula `AS` é usada para rebatizar a coluna de saída. (A cláusula `AS` é opcional.)

Uma consulta pode ser "qualificada" adicionando uma cláusula `WHERE` que especifica quais linhas são desejadas. A cláusula `WHERE` contém uma expressão booleana (verdadeiro ou falso) e apenas as linhas para as quais a expressão booleana é verdadeira são retornadas. Os operadores booleanos comuns (`AND`, `OR` e `NOT`) são permitidos na qualificação. Por exemplo, o seguinte recupera o tempo em São Francisco em dias chuvosos:

```
SELECT * FROM weather
    WHERE city = 'San Francisco' AND prcp > 0.0;
```

Resultado:

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
(1 row)
```

Você pode solicitar que os resultados de uma consulta sejam retornados em ordem de classificação:

```
SELECT * FROM weather
    ORDER BY city;
```

```
     city      | temp_lo | temp_hi | prcp |    date
---------------+---------+---------+------+------------
 Hayward       |      37 |      54 |      | 1994-11-29
 San Francisco |      43 |      57 |    0 | 1994-11-29
 San Francisco |      46 |      50 | 0.25 | 1994-11-27
```

Neste exemplo, o pedido de classificação não é totalmente especificado, e, portanto, você pode receber as linhas de São Francisco em qualquer ordem. Mas você sempre obterá os resultados mostrados acima se fizer:

```
SELECT * FROM weather
    ORDER BY city, temp_lo;
```

Você pode solicitar que as linhas duplicadas sejam removidas do resultado de uma consulta:

```
SELECT DISTINCT city
    FROM weather;
```

```
     city
---------------
 Hayward
 San Francisco
(2 rows)
```

Aqui, novamente, a ordem dos resultados pode variar. Você pode garantir resultados consistentes usando `DISTINCT` e `ORDER BY` juntos: [[3]](#ftn.id-1.4.4.6.6.7)

```
SELECT DISTINCT city
    FROM weather
    ORDER BY city;
```

---

[[2]](#id-1.4.4.6.2.10) Embora `SELECT *` seja útil para consultas rápidas, é amplamente considerado um mau estilo em código de produção, pois adicionar uma coluna à tabela mudaria os resultados.

[[3]](#id-1.4.4.6.6.7) Em alguns sistemas de banco de dados, incluindo versões mais antigas do PostgreSQL, a implementação do `DISTINCT` ordena automaticamente as linhas, e assim o `ORDER BY` não é necessário. Mas isso não é exigido pelo padrão SQL, e o PostgreSQL atual não garante que o `DISTINCT` faça com que as linhas sejam ordenadas.