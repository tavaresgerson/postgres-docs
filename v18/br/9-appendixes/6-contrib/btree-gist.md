## F.8. btree_gist — Classes de operadores GiST com comportamento de árvore B [#](#BTREE-GIST)

* [F.8.1. Exemplo de uso](btree-gist.md#BTREE-GIST-EXAMPLE-USAGE)
* [F.8.2. Autores](btree-gist.md#BTREE-GIST-AUTHORS)

`btree_gist` fornece classes de operadores de índice GiST que implementam comportamento equivalente a árvore B para os tipos de dados `int2`, `int4`, `int8`, `float4`, `float8`, `numeric`, `timestamp with time zone`, `timestamp without time zone`, `time with time zone`, `time without time zone`, `date`, `interval`, `oid`, `money`, `char`, `varchar`, `text`, `bytea`, `bit`, `varbit`, `macaddr`, `macaddr8`, `inet`, `cidr`, `uuid`, `bool` e todos os tipos `enum`.

De modo geral, essas classes de operadores não superam os métodos equivalentes de índice padrão de árvore B, e elas carecem de uma característica importante do código padrão de árvore B: a capacidade de impor a unicidade. No entanto, elas oferecem algumas outras características que não estão disponíveis com um índice de árvore B, conforme descrito abaixo. Além disso, essas classes de operadores são úteis quando é necessário um índice multicoluna GiST, onde algumas das colunas são de tipos de dados que só podem ser indexados com GiST, mas outras colunas são apenas tipos de dados simples. Por último, essas classes de operadores são úteis para testes de GiST e como base para o desenvolvimento de outras classes de operador GiST.

Além dos operadores de busca típicos de árvore B, `btree_gist` também oferece suporte ao índice para `<>` (“não igual”). Isso pode ser útil em combinação com uma restrição de exclusão (sql-createtable.md#SQL-CREATETABLE-EXCLUDE), conforme descrito abaixo.

Além disso, para os tipos de dados para os quais existe uma métrica de distância natural, o `btree_gist` define um operador de distância `<->` e fornece suporte ao índice GiST para pesquisas de vizinhança mais próxima usando este operador. Operadores de distância são fornecidos para `int2`, `int4`, `int8`, `float4`, `float8`, `timestamp with time zone`, `timestamp without time zone`, `time without time zone`, `date`, `interval`, `oid` e `money`.

Por padrão, o `btree_gist` constrói o índice GiST com o `sortsupport` no modo *sorteado*. Isso geralmente resulta em uma velocidade de construção do índice muito mais rápida. Ainda é possível reverter para a estratégia de construção com buffer usando o parâmetro `buffering` ao criar o índice.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.8.1. Uso Exemplo [#](#BTREE-GIST-EXAMPLE-USAGE)

Exemplo simples usando `btree_gist` em vez de `btree`:

```
CREATE TABLE test (a int4);
-- create index
CREATE INDEX testidx ON test USING GIST (a);
-- query
SELECT * FROM test WHERE a < 10;
-- nearest-neighbor search: find the ten entries closest to "42"
SELECT *, a <-> 42 AS dist FROM test ORDER BY a <-> 42 LIMIT 10;
```

Utilize uma restrição de exclusão (sql-createtable.md#SQL-CREATETABLE-EXCLUDE) para impor a regra de que uma jaula em um zoológico pode conter apenas um tipo de animal:

```
=> CREATE TABLE zoo (
  cage   INTEGER,
  animal TEXT,
  EXCLUDE USING GIST (cage WITH =, animal WITH <>)
);

=> INSERT INTO zoo VALUES(123, 'zebra');
INSERT 0 1
=> INSERT INTO zoo VALUES(123, 'zebra');
INSERT 0 1
=> INSERT INTO zoo VALUES(123, 'lion');
ERROR:  conflicting key value violates exclusion constraint "zoo_cage_animal_excl"
DETAIL:  Key (cage, animal)=(123, lion) conflicts with existing key (cage, animal)=(123, zebra).
=> INSERT INTO zoo VALUES(124, 'lion');
INSERT 0 1
```

### F.8.2. Autores [#](#BTREE-GIST-AUTHORS)

Teodor Sigaev (`<teodor@stack.net>`), Oleg Bartunov (`<oleg@sai.msu.su>`), Janko Richter (`<jankorichter@yahoo.de>`) e Paul Jungwirth (`<pj@illuminatedcomputing.com>`). Consulte <http://www.sai.msu.su/~megera/postgres/gist/> para informações adicionais.