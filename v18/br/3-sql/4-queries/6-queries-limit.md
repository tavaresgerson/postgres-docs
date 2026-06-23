## 7.6. `LIMIT` e `OFFSET` [#](#QUERIES-LIMIT)

`LIMIT` e `OFFSET` permitem que você retorne apenas uma parte das linhas geradas pelo resto da consulta:

```
SELECT select_list
    FROM table_expression
    [ ORDER BY ... ]
    [ LIMIT { count | ALL } ]
    [ OFFSET start ]
```

Se um número máximo de registros for especificado, não serão retornados mais do que esse número (mas, possivelmente, menos, se a própria consulta produzir menos registros). `LIMIT ALL` é o mesmo que omitir a cláusula `LIMIT`, assim como `LIMIT` com um argumento NULL.

`OFFSET` diz para ignorar tantas linhas antes de começar a retornar linhas. `OFFSET 0` é o mesmo que omitir a cláusula `OFFSET`, assim como `OFFSET` com um argumento NULL.

Se ambos os registros `OFFSET` e `LIMIT` aparecerem, os registros `OFFSET` são ignorados antes de começar a contar os registros `LIMIT` que são retornados.

Ao usar `LIMIT`, é importante usar uma cláusula `ORDER BY` que restrinja as linhas de resultado a uma ordem única. Caso contrário, você obterá um subconjunto imprevisível das linhas da consulta. Você pode estar solicitando as décima a vigésima linhas, mas em que ordem? A ordem é desconhecida, a menos que você tenha especificado `ORDER BY`.

O otimizador de consulta leva em consideração `LIMIT` ao gerar planos de consulta, portanto, é muito provável que você obtenha diferentes planos (que gerem diferentes ordens de linhas) dependendo do que você fornece para `LIMIT` e `OFFSET`. Assim, usar diferentes valores de `LIMIT`/`OFFSET` para selecionar diferentes subconjuntos de um resultado de consulta *dará resultados inconsistentes*, a menos que você imponha uma ordem de resultado previsível com `ORDER BY`. Isso não é um erro; é uma consequência inerente do fato de que o SQL não promete entregar os resultados de uma consulta em qualquer ordem específica, a menos que `ORDER BY` seja usado para restringir a ordem.

As linhas ignoradas por uma cláusula `OFFSET` ainda precisam ser calculadas dentro do servidor; portanto, um grande `OFFSET` pode ser ineficiente.