## DROP TABLE

DROP TABLE — remova uma tabela

## Sinopse

```
DROP TABLE [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP TABLE` remove tabelas do banco de dados. Somente o proprietário da tabela, o proprietário do esquema e o superusuário podem descartar uma tabela. Para esvaziar uma tabela sem destruir a tabela, use [`DELETE`](sql-delete.md "DELETE") ou [`TRUNCATE`](sql-truncate.md "TRUNCATE").

`DROP TABLE` sempre remove quaisquer índices, regras, gatilhos e restrições que existem para a tabela alvo. No entanto, para descartar uma tabela que é referenciada por uma visão ou uma restrição de chave estrangeira de outra tabela, `CASCADE` deve ser especificado. (`CASCADE` removerá uma visão dependente inteiramente, mas no caso da chave estrangeira, apenas removerá a restrição de chave estrangeira, não a outra tabela inteiramente.)

## Parâmetros

`IF EXISTS`: Não exija erro se a tabela não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) da tabela a ser excluída.

`CASCADE`: Descarte automaticamente os objetos que dependem da tabela (como vistas), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Não se recusar a descartar a tabela se algum objeto depender dela. Esse é o padrão.

## Exemplos

Para destruir duas tabelas, `films` e `distributors`:

```
DROP TABLE films, distributors;
```

## Compatibilidade

Este comando está de acordo com o padrão SQL, exceto pelo fato de que o padrão só permite que uma tabela seja excluída por comando, e, além da opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[ALTER TABLE](sql-altertable.md "ALTER TABLE"), [CREATE TABLE](sql-createtable.md "CREATE TABLE")