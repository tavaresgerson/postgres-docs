## ALTER STATISTICS

ALTER STATISTICS — alterar a definição de um objeto de estatísticas estendida

## Sinopse

```
ALTER STATISTICS name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER STATISTICS name RENAME TO new_name
ALTER STATISTICS name SET SCHEMA new_schema
ALTER STATISTICS name SET STATISTICS { new_target | DEFAULT }
```

## Descrição

`ALTER STATISTICS` altera os parâmetros de um objeto de estatísticas estendido existente. Quaisquer parâmetros que não sejam especificamente definidos no comando `ALTER STATISTICS` retêm suas configurações anteriores.

Você deve possuir o objeto de estatísticas para usar `ALTER STATISTICS`. Para alterar o esquema de um objeto de estatísticas, você também deve ter privilégio `CREATE` no novo esquema. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter privilégio `CREATE` no esquema do objeto de estatísticas. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar o objeto de estatísticas. No entanto, um superusuário pode alterar a propriedade de qualquer objeto de estatísticas de qualquer maneira.)

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) do objeto de estatísticas que será alterado.

*`new_owner`*: O nome do usuário do novo proprietário do objeto de estatísticas.

*`new_name`*: O novo nome do objeto de estatísticas.

*`new_schema`*: O novo esquema para o objeto de estatísticas.

*`new_target`*: O objetivo de coleta estatística para este objeto de estatísticas para operações subsequentes `ANALYZE` (sql-analyze.md "ANALYZE"). O objetivo pode ser definido no intervalo de 0 a 10000. Defina-o como `DEFAULT` para reverter ao uso do objetivo de estatísticas padrão do sistema ([default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)). (Definir um valor de -1 é uma maneira obsoleta de obter o mesmo resultado.) Para mais informações sobre o uso de estatísticas pelo planejador de consultas do PostgreSQL, consulte [Seção 14.2](planner-stats.md).

## Compatibilidade

Não existe comando `ALTER STATISTICS` no padrão SQL.

## Veja também

[Crie estatísticas](sql-createstatistics.md "CREATE STATISTICS"), [Exclua estatísticas](sql-dropstatistics.md "DROP STATISTICS")