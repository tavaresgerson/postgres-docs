## 7.7. `VALUES` Listas [#](#QUERIES-VALUES)

`VALUES` fornece uma maneira de gerar uma "tabela constante" que pode ser usada em uma consulta sem a necessidade de criar e preencher uma tabela no disco. A sintaxe é

```
VALUES ( expression [, ...] ) [, ...]
```

Cada lista entre parênteses de expressões gera uma linha na tabela. Todas as listas devem ter o mesmo número de elementos (ou seja, o número de colunas na tabela), e as entradas correspondentes em cada lista devem ter tipos de dados compatíveis. O tipo de dados real atribuído a cada coluna do resultado é determinado usando as mesmas regras que para `UNION` (consulte [Seção 10.5](typeconv-union-case.md)).

Como exemplo:

```
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

retornará uma tabela com duas colunas e três linhas. É efetivamente equivalente a:

```
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

Por padrão, o PostgreSQL atribui os nomes `column1`, `column2`, etc., às colunas de uma tabela `VALUES`. Os nomes das colunas não são especificados pelo padrão SQL e diferentes sistemas de banco de dados fazem isso de maneira diferente, então geralmente é melhor substituir os nomes padrão com uma lista de aliases de tabela, como este:

```
=> SELECT * FROM (VALUES (1, 'one'), (2, 'two'), (3, 'three')) AS t (num,letter);
 num | letter
-----+--------
   1 | one
   2 | two
   3 | three
(3 rows)
```

Sintaticamente, `VALUES` seguido de listas de expressão é tratado como equivalente a:

```
SELECT select_list FROM table_expression
```

e pode aparecer em qualquer lugar onde um `SELECT` pode. Por exemplo, você pode usá-lo como parte de um `UNION`, ou anexar um *`sort_specification`* (`ORDER BY`, `LIMIT` e/ou `OFFSET`) a ele. O `VALUES` é mais comumente usado como fonte de dados em um comando `INSERT`, e em seguida, mais comumente como uma subconsulta.

Para mais informações, consulte [VALUES](sql-values.md "VALUES").