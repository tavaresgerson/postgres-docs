## DROP DOMAIN

DROP DOMAIN — remova um domínio

## Sinopse

```
DROP DOMAIN [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP DOMAIN` remove um domínio. Apenas o proprietário de um domínio pode removê-lo.

## Parâmetros

`IF EXISTS`: Não exija erro se o domínio não existir. Um aviso é emitido neste caso.

*`name`*: O nome (opcionalmente qualificado por esquema) de um domínio existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do domínio (como as colunas de tabela) e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação do domínio se houver algum objeto dependente dele. Esse é o padrão.

## Exemplos

Para remover o domínio `box`:

```
DROP DOMAIN box;
```

## Compatibilidade

Este comando está de acordo com o padrão SQL, exceto pela opção `IF EXISTS`, que é uma extensão do PostgreSQL.

## Veja também

[Crie domínio](sql-createdomain.md "CREATE DOMAIN"), [Altere domínio](sql-alterdomain.md "ALTER DOMAIN")