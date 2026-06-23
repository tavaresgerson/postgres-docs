### 2.6. Conexões entre tabelas [#](#TUTORIAL-JOIN)

Até agora, nossas consultas só acessaram uma tabela de cada vez. As consultas podem acessar múltiplas tabelas de uma vez, ou acessar a mesma tabela de uma maneira que várias linhas da tabela estão sendo processadas ao mesmo tempo. As consultas que acessam múltiplas tabelas (ou múltiplas instâncias da mesma tabela) de uma vez são chamadas de consultas de *join*. Elas combinam linhas de uma tabela com linhas de uma segunda tabela, com uma expressão que especifica quais linhas devem ser emparelhadas. Por exemplo, para retornar todos os registros meteorológicos junto com a localização da cidade associada, o banco de dados precisa comparar a coluna `city` de cada linha da tabela `weather` com a coluna `name` de todas as linhas na tabela `cities`, e selecionar os pares de linhas onde esses valores correspondem.[[4]](#ftn.id-1.4.4.7.3.6) Isso seria realizado pela seguinte consulta:

```
SELECT * FROM weather JOIN cities ON city = name;
```

```
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(2 rows)
```

Observe duas coisas sobre o conjunto de resultados:

* Não há uma linha de resultado para a cidade de Hayward. Isso ocorre porque não há uma entrada correspondente na tabela `cities` para Hayward, então a junção ignora as linhas não correspondentes na tabela `weather`. Veremos em breve como isso pode ser corrigido.
* Há duas colunas que contêm o nome da cidade. Isso é correto porque as listas de colunas das tabelas `weather` e `cities` são concatenadas. Na prática, isso é indesejável, embora, provavelmente, você deseje listar as colunas de saída explicitamente em vez de usar `*`:

```
SELECT city, temp_lo, temp_hi, prcp, date, location
    FROM weather JOIN cities ON city = name;
```

Como todas as colunas tinham nomes diferentes, o analisador encontrou automaticamente para qual tabela elas pertencem. Se houvesse nomes de colunas duplicados nas duas tabelas, você precisaria *qualificar* os nomes das colunas para mostrar qual deles você queria, como:

```
SELECT weather.city, weather.temp_lo, weather.temp_hi,
       weather.prcp, weather.date, cities.location
    FROM weather JOIN cities ON weather.city = cities.name;
```

É amplamente considerado um bom estilo qualificar todos os nomes de coluna em uma consulta de junção, para que a consulta não falhe se um nome de coluna duplicado for adicionado posteriormente a uma das tabelas.

Perguntas do tipo já vistas até agora também podem ser escritas nesta forma:

```
SELECT *
    FROM weather, cities
    WHERE city = name;
```

Essa sintaxe precede a sintaxe `JOIN`/`ON`, que foi introduzida no SQL-92. As tabelas são simplesmente listadas na cláusula `FROM`, e a expressão de comparação é adicionada à cláusula `WHERE`. Os resultados dessa sintaxe implícita mais antiga e da sintaxe explícita mais recente `JOIN`/`ON` são idênticos. Mas para um leitor da consulta, a sintaxe explícita torna seu significado mais fácil de entender: A condição de junção é introduzida por sua própria palavra-chave, enquanto anteriormente a condição era misturada na cláusula `WHERE` junto com outras condições.

Agora, vamos descobrir como podemos recuperar os registros do Hayward. O que queremos que a consulta faça é analisar a tabela `weather` e, para cada linha, encontrar a(s) linha(s) correspondente(s) ao `cities`. Se nenhuma linha correspondente for encontrada, queremos que alguns "valores em branco" sejam substituídos pelas colunas da tabela `cities`. Esse tipo de consulta é chamado de *conjunção externa*. (As junções que vimos até agora são *junções internas*. O comando parece assim:

```
SELECT *
    FROM weather LEFT OUTER JOIN cities ON weather.city = cities.name;
```

```
     city      | temp_lo | temp_hi | prcp |    date    |     name      | location
---------------+---------+---------+------+------------+---------------+-----------
 Hayward       |      37 |      54 |      | 1994-11-29 |               |
 San Francisco |      46 |      50 | 0.25 | 1994-11-27 | San Francisco | (-194,53)
 San Francisco |      43 |      57 |    0 | 1994-11-29 | San Francisco | (-194,53)
(3 rows)
```

Essa consulta é chamada de *conjunção externa esquerda* porque a tabela mencionada à esquerda do operador de junção terá cada uma de suas linhas no resultado pelo menos uma vez, enquanto a tabela à direita terá apenas aquelas linhas que correspondem a alguma linha da tabela esquerda. Ao emitir uma linha da tabela esquerda para a qual não há correspondência na tabela direita, valores vazios (nulos) são substituídos pelas colunas da tabela direita.

**Exercício:** Existem também junções externas à direita e junções externas completas. Tente descobrir o que elas fazem.

Também podemos unir uma tabela contra si mesma. Isso é chamado de *auto-junção*. Como exemplo, suponha que desejemos encontrar todos os registros climáticos que estão na faixa de temperatura de outros registros climáticos. Portanto, precisamos comparar as colunas `temp_lo` e `temp_hi` de cada linha `weather` com as colunas `temp_lo` e `temp_hi` de todas as outras linhas `weather`. Podemos fazer isso com a seguinte consulta:

```
SELECT w1.city, w1.temp_lo AS low, w1.temp_hi AS high,
       w2.city, w2.temp_lo AS low, w2.temp_hi AS high
    FROM weather w1 JOIN weather w2
        ON w1.temp_lo < w2.temp_lo AND w1.temp_hi > w2.temp_hi;
```

```
     city      | low | high |     city      | low | high
---------------+-----+------+---------------+-----+------
 San Francisco |  43 |   57 | San Francisco |  46 |   50
 Hayward       |  37 |   54 | San Francisco |  46 |   50
(2 rows)
```

Aqui, redefinimos a tabela de clima como `w1` e `w2` para podermos distinguir o lado esquerdo e direito da junção. Você também pode usar esse tipo de alias em outras consultas para economizar algumas digitações, por exemplo:

```
SELECT *
    FROM weather w JOIN cities c ON w.city = c.name;
```

Você vai encontrar esse estilo de abreviação com bastante frequência.

---

[[4]](#id-1.4.4.7.3.6) Este é apenas um modelo conceitual. A junção é geralmente realizada de uma maneira mais eficiente do que comparar realmente cada par possível de linhas, mas isso é invisível ao usuário.