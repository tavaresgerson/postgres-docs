## POLÍTICA DE RETIRADA

POLÍTICA DE EXCLUSÃO — remova uma política de segurança de nível de linha de uma tabela

## Sinopse

```
DROP POLICY [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP POLICY` remove a política especificada da tabela. Observe que, se a última política for removida de uma tabela e a tabela ainda tiver segurança de nível de linha habilitada via `ALTER TABLE`, então a política de negação padrão será usada. `ALTER TABLE ... DISABLE ROW LEVEL SECURITY` pode ser usado para desabilitar a segurança de nível de linha para uma tabela, independentemente de existir políticas para a tabela ou

## Parâmetros

`IF EXISTS`: Não exija erro se a política não existir. Um aviso é emitido neste caso.

*`name`*: O nome da política a ser excluída.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela na qual a política está.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm efeito, uma vez que não há dependências em políticas.

## Exemplos

Para descartar a política chamada `p1` na tabela chamada `my_table`:

```
DROP POLICY p1 ON my_table;
```

## Compatibilidade

`DROP POLICY` é uma extensão do PostgreSQL.

## Veja também

[Crie a política](sql-createpolicy.md "CREATE POLICY"), [Altere a política](sql-alterpolicy.md "ALTER POLICY")