## F.7. btree_gin — Classes de operadores GIN com comportamento de árvore B-tree [#](#BTREE-GIN)

* [F.7.1. Exemplo de uso](btree-gin.md#BTREE-GIN-EXAMPLE-USAGE)
* [F.7.2. Autores](btree-gin.md#BTREE-GIN-AUTHORS)

O `btree_gin` fornece classes de operadores GIN que implementam comportamento equivalente a árvore B para os tipos de dados `int2`, `int4`, `int8`, `float4`, `float8`, `timestamp with time zone`, `timestamp without time zone`, `time with time zone`, `time without time zone`, `date`, `interval`, `oid`, `money`, `"char"`, `varchar`, `text`, `bytea`, `bit`, `varbit`, `macaddr`, `macaddr8`, `inet`, `cidr`, `uuid`, `name`, `bool`, `bpchar` e todos os tipos de `enum`.

De modo geral, essas classes de operadores não superam os métodos equivalentes de índice padrão de árvore B, e elas carecem de uma característica importante do código padrão de árvore B: a capacidade de impor a unicidade. No entanto, elas são úteis para testes de GIN e como base para o desenvolvimento de outras classes de operadores de GIN. Além disso, para consultas que testam tanto uma coluna indexável por GIN quanto uma coluna indexável por árvore B, pode ser mais eficiente criar um índice multicoluna de GIN que use uma dessas classes de operadores do que criar dois índices separados que teriam que ser combinados por meio de AND de bitmap.

Este módulo é considerado "confiável", ou seja, pode ser instalado por usuários não superusuários que possuem privilégio `CREATE` no banco de dados atual.

### F.7.1. Uso Exemplo [#](#BTREE-GIN-EXAMPLE-USAGE)

```
CREATE TABLE test (a int4);
-- create index
CREATE INDEX testidx ON test USING GIN (a);
-- query
SELECT * FROM test WHERE a < 10;
```

### F.7.2. Autores [#](#BTREE-GIN-AUTHORS)

Teodor Sigaev (`<teodor@stack.net>`) e Oleg Bartunov (`<oleg@sai.msu.su>`). Consulte <http://www.sai.msu.su/~megera/oddmuse/index.cgi/Gin> para informações adicionais.