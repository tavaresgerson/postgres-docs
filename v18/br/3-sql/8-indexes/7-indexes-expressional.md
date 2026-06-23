## 11.7. Índices de expressões [#](#INDEXES-EXPRESSIONAL)

Uma coluna de índice não precisa ser apenas uma coluna da tabela subjacente, mas pode ser uma função ou expressão escalar calculada a partir de uma ou mais colunas da tabela. Esse recurso é útil para obter acesso rápido a tabelas com base nos resultados de cálculos.

Por exemplo, uma maneira comum de fazer comparações não sensíveis a maiúsculas e minúsculas é usar a função `lower`:

```
SELECT * FROM test1 WHERE lower(col1) = 'value';
```

Essa consulta pode usar um índice se um tiver sido definido no resultado da função `lower(col1)`:

```
CREATE INDEX test1_lower_col1_idx ON test1 (lower(col1));
```

Se declarássemos este índice `UNIQUE`, isso impedirá a criação de linhas cujos valores de `col1` diferem apenas em caso, bem como linhas cujos valores de `col1` são, na verdade, idênticos. Assim, índices em expressões podem ser usados para impor restrições que não podem ser definidas como restrições únicas simples.

Como outro exemplo, se uma pessoa faz frequentemente consultas como:

```
SELECT * FROM people WHERE (first_name || ' ' || last_name) = 'John Smith';
```

então, talvez valha a pena criar um índice como este:

```
CREATE INDEX people_names ON people ((first_name || ' ' || last_name));
```

A sintaxe do comando `CREATE INDEX` normalmente exige que se escreva parênteses ao redor das expressões de índice, como mostrado no segundo exemplo. Os parênteses podem ser omitidos quando a expressão é apenas uma chamada de função, como no primeiro exemplo.

As expressões de índice são relativamente caras de manter, porque a(s) expressão(ões) derivada(s) deve(m) ser calculada(s) para cada inserção de linha e [não atualização HOT](storage-hot.md "66.7. Heap-Only Tuples (HOT)). No entanto, as expressões de índice não são recompiladas durante uma pesquisa indexada, uma vez que já estão armazenadas no índice. Em ambos os exemplos acima, o sistema vê a consulta como apenas `WHERE indexedcolumn = 'constant'` e, portanto, a velocidade da pesquisa é equivalente a qualquer outra consulta simples de índice. Assim, os índices em expressões são úteis quando a velocidade de recuperação é mais importante do que a velocidade de inserção e atualização.