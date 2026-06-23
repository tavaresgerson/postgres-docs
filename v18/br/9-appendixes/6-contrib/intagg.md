## F.18. intagg — agregador e enumerador de inteiros [#](#INTAGG)

* [F.18.1. Funções](intagg.md#INTAGG-FUNCTIONS)
* [F.18.2. Exemplos de uso](intagg.md#INTAGG-SAMPLES)

O módulo `intagg` fornece um agregador de inteiros e um enumerador. `intagg` é agora obsoleto, porque existem funções embutidas que fornecem um conjunto superconjunto de suas capacidades. No entanto, o módulo ainda é fornecido como um wrapper de compatibilidade em torno das funções embutidas.

### F.18.1. Funções [#](#INTAGG-FUNCTIONS)

O agregador é uma função agregada `int_array_aggregate(integer)` que produz um array de inteiros contendo exatamente os inteiros que lhe são fornecidos. Este é um wrapper em torno de `array_agg`, que faz a mesma coisa para qualquer tipo de array.

O enumerador é uma função `int_array_enum(integer[])` que retorna `setof integer`. É essencialmente a operação inversa do agregador: dado um array de inteiros, expande-o em um conjunto de linhas. Este é um wrapper em torno de `unnest`, que faz a mesma coisa para qualquer tipo de array.

### F.18.2. Usos de amostra [#](#INTAGG-SAMPLES)

Muitos sistemas de banco de dados possuem a noção de uma tabela de muitos para muitos. Essa tabela geralmente fica entre duas tabelas indexadas, por exemplo:

```
CREATE TABLE left_table  (id INT PRIMARY KEY, ...);
CREATE TABLE right_table (id INT PRIMARY KEY, ...);
CREATE TABLE many_to_many(id_left  INT REFERENCES left_table,
                          id_right INT REFERENCES right_table);
```

É tipicamente usado assim:

```
SELECT right_table.*
FROM right_table JOIN many_to_many ON (right_table.id = many_to_many.id_right)
WHERE many_to_many.id_left = item;
```

Isso retornará todos os itens na tabela da direita para uma entrada na tabela da esquerda. Esse é um constrangimento muito comum no SQL.

Agora, essa metodologia pode ser complicada com um número muito grande de entradas na tabela `many_to_many`. Muitas vezes, uma junção como essa resultaria em uma varredura de índice e uma busca para cada entrada da mão direita na tabela para uma entrada da mão esquerda específica. Se você tem um sistema bastante dinâmico, não há muito o que fazer. No entanto, se você tem alguns dados que são bastante estáticos, você pode criar uma tabela resumida com o agregador.

```
CREATE TABLE summary AS
  SELECT id_left, int_array_aggregate(id_right) AS rights
  FROM many_to_many
  GROUP BY id_left;
```

Isso criará uma tabela com uma linha por item à esquerda e um array de itens à direita. Agora, isso é bastante inútil sem alguma maneira de usar o array; é por isso que existe um enumerador de array. Você pode fazer

```
SELECT id_left, int_array_enum(rights) FROM summary WHERE id_left = item;
```

A consulta acima usando `int_array_enum` produz os mesmos resultados que

```
SELECT id_left, id_right FROM many_to_many WHERE id_left = item;
```

A diferença é que a consulta à tabela de resumo só precisa obter uma linha da tabela, enquanto a consulta direta contra o `many_to_many` deve realizar uma varredura de índice e obter uma linha para cada entrada.

Em um sistema, uma consulta com um custo de 8488 foi reduzida a um custo de 329. A consulta original era uma junção que envolvia a tabela `many_to_many`, que foi substituída por:

```
SELECT id_right, count(id_right) FROM
  ( SELECT id_left, int_array_enum(rights) AS id_right
    FROM summary
    JOIN (SELECT id FROM left_table
          WHERE id = item) AS lefts
    ON (summary.id_left = lefts.id)
  ) AS list
  GROUP BY id_right
  ORDER BY count DESC;
```
