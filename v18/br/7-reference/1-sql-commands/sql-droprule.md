## DROP RULE

DROP RULE — remova uma regra de reescrita

## Sinopse

```
DROP RULE [ IF EXISTS ] name ON table_name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP RULE` descarrega uma regra de reescrita.

## Parâmetros

`IF EXISTS`: Não exija erro se a regra não existir. Neste caso, é emitido um aviso.

*`name`*: O nome da regra a ser excluída.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela ou visão a que a regra se aplica.

`CASCADE`: Descarte automaticamente os objetos que dependem da regra e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15](ddl-depend.md)).

`RESTRICT`: Rejeitar a eliminação da regra se houver objetos que dependem dela. Este é o padrão.

## Exemplos

Para descartar a regra de reescrita `newrule`:

```
DROP RULE newrule ON mytable;
```

## Compatibilidade

`DROP RULE` é uma extensão de linguagem do PostgreSQL, assim como todo o sistema de reescrita de consultas.

## Veja também

[Crie regra](sql-createrule.md "CREATE RULE"), [Altere regra](sql-alterrule.md "ALTER RULE")