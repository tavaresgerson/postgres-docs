## VALORES

VALUES — calcular um conjunto de linhas

## Sinopse

```
VALUES ( expression [, ...] ) [, ...]
    [ ORDER BY sort_expression [ ASC | DESC | USING operator ] [, ...] ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start [ ROW | ROWS ] ]
    [ FETCH { FIRST | NEXT } [ count ] { ROW | ROWS } ONLY ]
```

## Descrição

`VALUES` calcula um valor de linha ou um conjunto de valores de linha especificados por expressões de valor. É comumente usado para gerar uma "tabela constante" dentro de um comando maior, mas pode ser usado por si só.

Quando mais de uma linha é especificada, todas as linhas devem ter o mesmo número de elementos. Os tipos de dados das colunas da tabela resultante são determinados combinando os tipos explícitos ou inferidos das expressões que aparecem naquela coluna, usando as mesmas regras que para `UNION` (ver [Seção 10.5] (typeconv-union-case.md "10.5. UNION, CASE, and Related Constructs")).

Dentro de comandos maiores, `VALUES` é permitido sintaticamente em qualquer lugar onde `SELECT` está. Como é tratado como um `SELECT` pela gramática, é possível usar as cláusulas `ORDER BY`, `LIMIT` (ou equivalentemente `FETCH FIRST`), e `OFFSET` com um comando `VALUES`.

## Parâmetros

*`expression`*: Uma constante ou expressão para calcular e inserir no local indicado na tabela resultante (conjunto de linhas). Em uma lista `VALUES` que aparece no nível superior de um `INSERT`, um *`expression`* pode ser substituído por `DEFAULT` para indicar que o valor padrão da coluna de destino deve ser inserido. `DEFAULT` não pode ser usado quando `VALUES` aparece em outros contextos.

*`sort_expression`*: Uma expressão ou constante inteira que indica como ordenar as linhas do resultado. Essa expressão pode se referir às colunas do resultado do `VALUES` como `column1`, `column2`, etc. Para mais detalhes, consulte a cláusula [ORDER BY](sql-select.md#SQL-ORDERBY "ORDER BY Clause") na documentação do [SELECT](sql-select.md "SELECT").

*`operator`*: Um operador de ordenação. Para detalhes, consulte a cláusula [ORDEM POR](sql-select.md#SQL-ORDERBY "ORDER BY Clause") na documentação do [SELECT](sql-select.md "SELECT").

*`count`*: O número máximo de linhas a serem retornadas. Para detalhes, consulte a cláusula LIMIT em [SELECT](sql-select.md#SQL-LIMIT)[(sql-select.md "SELECT")], na documentação.

*`start`*: O número de linhas a ignorar antes de começar a retornar as linhas. Para detalhes, consulte a cláusula LIMIT em [SELECT](sql-select.md#SQL-LIMIT)[(sql-select.md "SELECT")], na documentação.

## Notas

`VALUES` listas com números muito grandes de linhas devem ser evitadas, pois você pode encontrar falhas de memória ou desempenho ruim. `VALUES` aparecendo dentro de `INSERT` é um caso especial (porque os tipos de coluna desejados são conhecidos da tabela de destino do `INSERT`, e não precisam ser inferidos por digitalização da lista de `VALUES`), então ele pode lidar com listas maiores do que são práticas em outros contextos.

## Exemplos

Um comando simples `VALUES`:

```
VALUES (1, 'one'), (2, 'two'), (3, 'three');
```

Isso retornará uma tabela com duas colunas e três linhas. É efetivamente equivalente a:

```
SELECT 1 AS column1, 'one' AS column2
UNION ALL
SELECT 2, 'two'
UNION ALL
SELECT 3, 'three';
```

Mais comumente, `VALUES` é usado dentro de um comando SQL maior. O uso mais comum é no `INSERT`:

```
INSERT INTO films (code, title, did, date_prod, kind)
    VALUES ('T_601', 'Yojimbo', 106, '1961-06-16', 'Drama');
```

No contexto de `INSERT`, as entradas de uma lista de `VALUES` podem ser `DEFAULT` para indicar que a coluna padrão deve ser usada aqui em vez de especificar um valor:

```
INSERT INTO films VALUES
    ('UA502', 'Bananas', 105, DEFAULT, 'Comedy', '82 minutes'),
    ('T_601', 'Yojimbo', 106, DEFAULT, 'Drama', DEFAULT);
```

`VALUES` também pode ser usado onde uma sub`SELECT` poderia ser escrita, por exemplo, em uma cláusula `FROM`:

```
SELECT f.*
  FROM films f, (VALUES('MGM', 'Horror'), ('UA', 'Sci-Fi')) AS t (studio, kind)
  WHERE f.studio = t.studio AND f.kind = t.kind;

UPDATE employees SET salary = salary * v.increase
  FROM (VALUES(1, 200000, 1.2), (2, 400000, 1.4)) AS v (depno, target, increase)
  WHERE employees.depno = v.depno AND employees.sales >= v.target;
```

Observe que uma cláusula `AS` é necessária quando `VALUES` é usada em uma cláusula `FROM`, assim como é verdade para `SELECT`. Não é necessário que a cláusula `AS` especifique nomes para todas as colunas, mas é uma boa prática fazê-lo. (Os nomes padrão das colunas para `VALUES` são `column1`, `column2`, etc. no PostgreSQL, mas esses nomes podem ser diferentes em outros sistemas de banco de dados.)

Quando o `VALUES` é usado no `INSERT`, os valores são todos automaticamente coercidos para o tipo de dados da coluna de destino correspondente. Quando é usado em outros contextos, pode ser necessário especificar o tipo de dados correto. Se as entradas forem todas constantes literais com aspas, coercer a primeira é suficiente para determinar o tipo assumido para todas:

```
SELECT * FROM machines
WHERE ip_address IN (VALUES('192.168.0.1'::inet), ('192.168.0.10'), ('192.168.1.43'));
```

DICA

Para testes simples de `IN`, é melhor confiar na forma de (functions-comparisons.md#FUNCTIONS-COMPARISONS-IN-SCALAR "9.25.1. IN") da lista de escalares `IN` do que escrever uma consulta `VALUES` como mostrado acima. O método de lista de escalares exige menos escrita e é frequentemente mais eficiente.

## Compatibilidade

`VALUES` está em conformidade com o padrão SQL. `LIMIT` e `OFFSET` são extensões do PostgreSQL; veja também em [SELECT](sql-select.md "SELECT").

## Veja também

[INSERT](sql-insert.md "INSERT"), [SELECT](sql-select.md "SELECT")