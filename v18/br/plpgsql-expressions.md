## 41.4. Expressões [#](#PLPGSQL-EXPRESSIONS)

Todas as expressões usadas em declarações PL/pgSQL são processadas usando o executor SQL principal do servidor. Por exemplo, quando você escreve uma declaração PL/pgSQL como

```
IF expression THEN ...
```

O PL/pgSQL avaliará a expressão fornecendo uma consulta como

```
SELECT expression
```

para o motor SQL principal. Ao formar o comando `SELECT`, quaisquer ocorrências de nomes de variáveis PL/pgSQL são substituídas por parâmetros de consulta, conforme discutido em detalhe na [Seção 41.11.1](plpgsql-implementation.md#PLPGSQL-VAR-SUBST). Isso permite que o plano de consulta para o `SELECT` seja preparado apenas uma vez e, em seguida, reutilizado para avaliações subsequentes com diferentes valores das variáveis. Assim, o que realmente acontece na primeira utilização de uma expressão é essencialmente um comando `PREPARE`. Por exemplo, se tivermos declarado duas variáveis inteiras `x` e `y`, e escrevermos

```
IF x < y THEN ...
```

o que acontece nos bastidores é equivalente a

```
PREPARE statement_name(integer, integer) AS SELECT $1 < $2;
```

e, em seguida, esta declaração preparada é `EXECUTE`ada para cada execução da declaração `IF`, com os valores atuais das variáveis PL/pgSQL fornecidos como valores de parâmetro. Normalmente, esses detalhes não são importantes para um usuário PL/pgSQL, mas são úteis para saber quando se tenta diagnosticar um problema. Mais informações aparecem em [Seção 41.11.2](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING).

Como um *`expression`* é convertido em um comando `SELECT`, ele pode conter as mesmas cláusulas que um `SELECT` comum, exceto que não pode incluir uma cláusula de nível superior `UNION`, `INTERSECT` ou `EXCEPT`. Assim, por exemplo, pode-se testar se uma tabela está não vazia com

```
IF count(*) > 0 FROM my_table THEN ...
```

já que o *`expression`* entre `IF` e `THEN` é analisado como se fosse `SELECT count(*) > 0 FROM my_table`. O `SELECT` deve produzir uma única coluna e não mais de uma linha. (Se não produzir nenhuma linha, o resultado é considerado NULL.)