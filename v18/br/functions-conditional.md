## 9.18. Expressões Condicionais [#](#FUNCTIONS-CONDITIONAL)

* [9.18.1. `CASE`](functions-conditional.md#FUNCTIONS-CASE)
* [9.18.2. `COALESCE`](functions-conditional.md#FUNCTIONS-COALESCE-NVL-IFNULL)
* [9.18.3. `NULLIF`](functions-conditional.md#FUNCTIONS-NULLIF)
* [9.18.4. `GREATEST` e `LEAST`](functions-conditional.md#FUNCTIONS-GREATEST-LEAST)

Esta seção descreve as expressões condicionais compatíveis com SQL disponíveis no PostgreSQL.

### DICA

Se suas necessidades vão além das capacidades dessas expressões condicionais, você pode querer considerar a escrita de uma função no lado do servidor em uma linguagem de programação mais expressiva.

### Nota

Embora `COALESCE`, `GREATEST` e `LEAST` sejam sintaticamente semelhantes a funções, não são funções comuns e, portanto, não podem ser usadas com argumentos explícitos de matriz `VARIADIC`.

### 9.18.1. `CASE` [#](#FUNCTIONS-CASE)

A expressão SQL `CASE` é uma expressão condicional genérica, semelhante às instruções if/else em outras linguagens de programação:

```
CASE WHEN condition THEN result
     [WHEN ...]
     [ELSE result]
END
```

As cláusulas `CASE` podem ser usadas sempre que uma expressão é válida. Cada *`condition`* é uma expressão que retorna um resultado `boolean`. Se o resultado da condição for verdadeiro, o valor da expressão `CASE` é o *`result`* que segue a condição, e o restante da expressão `CASE` não é processado. Se o resultado da condição não for verdadeiro, quaisquer cláusulas subsequentes `WHEN` são examinadas da mesma maneira. Se nenhum *`WHEN`* `condition` gerar verdadeiro, o valor da expressão `CASE` é o *`result`* da cláusula `ELSE`. Se a cláusula `ELSE` é omitida e nenhuma condição é verdadeira, o resultado é nulo.

Um exemplo:

```
SELECT * FROM test;

 a
---
 1
 2
 3


SELECT a,
       CASE WHEN a=1 THEN 'one'
            WHEN a=2 THEN 'two'
            ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

Os tipos de dados de todas as expressões *`result`* devem ser convertidos em um único tipo de saída. Consulte a Seção 10.5 [(typeconv-union-case.md "10.5. UNION, CASE, and Related Constructs")] para obter mais detalhes.

Existe uma forma “simples” de expressão de `CASE` que é uma variante da forma geral acima:

```
CASE expression
    WHEN value THEN result
    [WHEN ...]
    [ELSE result]
END
```

O primeiro *`expression`* é calculado, em seguida, comparado a cada uma das expressões *`value`* nas cláusulas `WHEN`, até que uma delas seja encontrada igual a ele. Se nenhuma correspondência for encontrada, o *`result`* da cláusula `ELSE` (ou um valor nulo) é retornado. Isso é semelhante à declaração `switch` em C.

O exemplo acima pode ser escrito usando a sintaxe simples `CASE`:

```
SELECT a,
       CASE a WHEN 1 THEN 'one'
              WHEN 2 THEN 'two'
              ELSE 'other'
       END
    FROM test;

 a | case
---+-------
 1 | one
 2 | two
 3 | other
```

Uma expressão `CASE` não avalia nenhuma subexpressão que não seja necessária para determinar o resultado. Por exemplo, essa é uma maneira possível de evitar uma falha de divisão por zero:

```
SELECT ... WHERE CASE WHEN x <> 0 THEN y/x > 1.5 ELSE false END;
```

### Nota

Como descrito na [Seção 4.2.14][(sql-expressions.md#SYNTAX-EXPRESS-EVAL "4.2.14. Expression Evaluation Rules")], existem várias situações em que subexpressiones de uma expressão são avaliadas em diferentes momentos, de modo que o princípio de que “`CASE` avalia apenas as subexpressiones necessárias” não é absoluto. Por exemplo, uma constante subexpressão `1/0` geralmente resultará em uma falha de divisão por zero no momento do planejamento, mesmo que esteja dentro de um braço `CASE` que nunca seria acessado no momento da execução.

### 9.18.2. `COALESCE` [#](#FUNCTIONS-COALESCE-NVL-IFNULL)

```
COALESCE(value [, ...])
```

A função `COALESCE` retorna o primeiro de seus argumentos que não é nulo. O nulo é retornado apenas se todos os argumentos forem nulos. Ela é frequentemente usada para substituir um valor padrão para valores nulos ao recuperar dados para exibição, por exemplo:

```
SELECT COALESCE(description, short_description, '(none)') ...
```

Isso retorna `description` se não for nulo, caso contrário, `short_description` se não for nulo, caso contrário, `(none)`.

Todos os argumentos devem ser convertidos para um tipo de dados comum, que será o tipo do resultado (consulte [Seção 10.5] para detalhes).

Assim como uma expressão `CASE`, `COALESCE` avalia apenas os argumentos necessários para determinar o resultado; ou seja, os argumentos à direita do primeiro argumento não nulo não são avaliados. Essa função padrão do SQL oferece capacidades semelhantes às de `NVL` e `IFNULL`, que são usadas em alguns outros sistemas de banco de dados.

### 9.18.3. `NULLIF` [#](#FUNCTIONS-NULLIF)

```
NULLIF(value1, value2)
```

A função `NULLIF` retorna um valor nulo se *`value1`* for igual a *`value2`*; caso contrário, ela retorna *`value1`*. Isso pode ser usado para realizar a operação inversa do exemplo `COALESCE` dado acima:

```
SELECT NULLIF(value, '(none)') ...
```

Neste exemplo, se `value` for `(none)`, é retornado nulo, caso contrário, o valor de `value` é retornado.

Os dois argumentos devem ser de tipos comparáveis. Para ser específico, eles são comparados exatamente como se você tivesse escrito `value1 = value2`, então deve haver um operador adequado disponível `=`.

O resultado tem o mesmo tipo que o primeiro argumento — mas há uma sutileza. O que é realmente retornado é o primeiro argumento do operador implícito `=`, e, em alguns casos, isso será promovido para corresponder ao tipo do segundo argumento. Por exemplo, `NULLIF(1, 2.2)` gera `numeric`, porque não há operador `integer` `=` `numeric`, apenas `numeric` `=` `numeric`.

### 9.18.4. `GREATEST` e `LEAST` [#](#FUNCTIONS-GREATEST-LEAST)

```
GREATEST(value [, ...])
```

```
LEAST(value [, ...])
```

As funções `GREATEST` e `LEAST` selecionam o maior ou menor valor de uma lista de qualquer número de expressões. As expressões devem ser todas convertidas em um tipo de dados comum, que será o tipo do resultado (consulte [Seção 10.5][(typeconv-union-case.md "10.5. UNION, CASE, and Related Constructs")] para detalhes).

Os valores nulos na lista de argumentos são ignorados. O resultado será nulo apenas se todas as expressões forem avaliadas como nulos. (Isso é uma exceção ao padrão SQL. De acordo com o padrão, o valor de retorno é nulo se qualquer argumento for nulo. Algumas outras bases de dados se comportam dessa maneira.)