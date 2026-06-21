## 11.10. Classes e famílias de operadores [#](#INDEXES-OPCLASS)

Uma definição de índice pode especificar uma *classe de operador* para cada coluna de um índice.

```
CREATE INDEX name ON table (column opclass [ ( opclass_options ) ] [sort options] [, ...]);
```

A classe de operador identifica os operadores a serem utilizados pelo índice para aquela coluna. Por exemplo, um índice de árvore B no tipo `int4` usaria a classe `int4_ops`; essa classe de operador inclui funções de comparação para valores do tipo `int4`. Na prática, a classe de operador padrão para o tipo de dados da coluna geralmente é suficiente. A principal razão para ter classes de operador é que, para alguns tipos de dados, pode haver mais de um comportamento de índice significativo. Por exemplo, podemos querer ordenar um tipo de número complexo ou pelo valor absoluto ou pela parte real. Podemos fazer isso definindo duas classes de operador para o tipo de dados e, em seguida, selecionando a classe apropriada ao fazer um índice. A classe de operador determina a ordem básica de classificação (que pode então ser modificada adicionando opções de classificação `COLLATE`, `ASC`/`DESC` e/ou `NULLS FIRST`/`NULLS LAST`).

Existem também algumas classes de operadores embutidas além das de padrão:

As classes de operador `text_pattern_ops`, `varchar_pattern_ops` e `bpchar_pattern_ops` suportam índices B-tree nos tipos `text`, `varchar` e `char`, respectivamente. A diferença em relação às classes de operador padrão é que os valores são comparados estritamente caracter a caractere, em vez de de acordo com as regras de ordenação específicas do local. Isso torna essas classes de operador adequadas para uso em consultas que envolvem expressões de correspondência de padrões (`LIKE` ou expressões regulares POSIX) quando o banco de dados não usa o local padrão “C”. Como exemplo, você pode indexar uma coluna `varchar` assim:

  ```
  CREATE INDEX test_index ON test_table (col varchar_pattern_ops);
  ```

Observe que você também deve criar um índice com a classe do operador padrão se quiser que consultas que envolvam comparações comuns de `<`, `<=`, `>` ou `>=` usem um índice. Tais consultas não podem usar as classes de operadores `xxx_pattern_ops`. (As comparações de igualdade comuns podem usar essas classes de operadores, no entanto.) É possível criar vários índices na mesma coluna com diferentes classes de operadores. Se você usar o C locale, não precisa das classes de operadores `xxx_pattern_ops`, porque um índice com a classe do operador padrão é utilizável para consultas de correspondência de padrões no C locale.

A consulta a seguir mostra todas as classes de operadores definidas:

```
SELECT am.amname AS index_method,
       opc.opcname AS opclass_name,
       opc.opcintype::regtype AS indexed_type,
       opc.opcdefault AS is_default
    FROM pg_am am, pg_opclass opc
    WHERE opc.opcmethod = am.oid
    ORDER BY index_method, opclass_name;
```

Uma classe de operador é, na verdade, apenas um subconjunto de uma estrutura maior chamada *família de operadores*. Nos casos em que vários tipos de dados têm comportamentos semelhantes, é frequentemente útil definir operadores entre tipos de dados e permitir que esses operadores trabalhem com índices. Para fazer isso, as classes de operador para cada um dos tipos devem ser agrupadas na mesma família de operadores. Os operadores entre tipos são membros da família, mas não estão associados a nenhuma classe única dentro da família.

Esta versão expandida da consulta anterior mostra a família de operadores a que cada classe de operador pertence:

```
SELECT am.amname AS index_method,
       opc.opcname AS opclass_name,
       opf.opfname AS opfamily_name,
       opc.opcintype::regtype AS indexed_type,
       opc.opcdefault AS is_default
    FROM pg_am am, pg_opclass opc, pg_opfamily opf
    WHERE opc.opcmethod = am.oid AND
          opc.opcfamily = opf.oid
    ORDER BY index_method, opclass_name;
```

Essa consulta mostra todas as famílias de operadores definidos e todos os operadores incluídos em cada família:

```
SELECT am.amname AS index_method,
       opf.opfname AS opfamily_name,
       amop.amopopr::regoperator AS opfamily_operator
    FROM pg_am am, pg_opfamily opf, pg_amop amop
    WHERE opf.opfmethod = am.oid AND
          amop.amopfamily = opf.oid
    ORDER BY index_method, opfamily_name, opfamily_operator;
```

### DICA

[psql](app-psql.md "psql") possui comandos `\dAc`, `\dAf` e `\dAo`, que oferecem versões um pouco mais sofisticadas dessas consultas.