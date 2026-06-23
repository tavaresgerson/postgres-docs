## DROP STATISTICS

DROP STATISTICS — remova estatísticas extensas

## Sinopse

```
DROP STATISTICS [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP STATISTICS` remove o(s) objeto(s) de estatísticas do banco de dados. Apenas o proprietário do objeto de estatísticas, o proprietário do esquema ou um superusuário pode descartar um objeto de estatísticas.

## Parâmetros

`IF EXISTS`: Não exija erro se o objeto de estatísticas não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) do objeto de estatísticas a ser excluído.

`CASCADE` `RESTRICT`: Essas palavras-chave não têm efeito, uma vez que não há dependências em estatísticas.

## Exemplos

Para destruir dois objetos de estatísticas em esquemas diferentes, sem falhar se eles não existirem:

```
DROP STATISTICS IF EXISTS
    accounting.users_uid_creation,
    public.grants_user_role;
```

## Compatibilidade

Não existe comando `DROP STATISTICS` no padrão SQL.

## Veja também

[ALTER STATISTICS](sql-alterstatistics.md "ALTER STATISTICS"), [CREATE STATISTICS](sql-createstatistics.md "CREATE STATISTICS")