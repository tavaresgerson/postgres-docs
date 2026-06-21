## 68.6. BKI Exemplo [#](#BKI-EXAMPLE)

A sequência de comandos a seguir criará a tabela `test_table` com OID 420, com três colunas `oid`, `cola` e `colb` do tipo `oid`, `int4` e `text`, respectivamente, e inserirá duas linhas na tabela:

```
create test_table 420 (oid = oid, cola = int4, colb = text)
open test_table
insert ( 421 1 'value 1' )
insert ( 422 2 _null_ )
close test_table
```
