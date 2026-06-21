## DROP FOREIGN DATA WRAPPER

DROP FOREIGN DATA WRAPPER — remova um wrapper de dados externos

## Sinopse

```
DROP FOREIGN DATA WRAPPER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP FOREIGN DATA WRAPPER` remove um revestimento de dados externos existente. Para executar este comando, o usuário atual deve ser o proprietário do revestimento de dados externos.

## Parâmetros

`IF EXISTS`: Não exija erro se o wrapper de dados estrangeiros não existir. Um aviso é emitido neste caso.

*`name`*: O nome de um wrapper de dados estrangeiro existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do wrapper de dados externos (como tabelas e servidores externos), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação do wrapper de dados estrangeiros se houver objetos que dependem dele. Esse é o padrão.

## Exemplos

Deixe de lado o wrapper de dados estrangeiros `dbi`:

```
DROP FOREIGN DATA WRAPPER dbi;
```

## Compatibilidade

`DROP FOREIGN DATA WRAPPER` está em conformidade com a ISO/IEC 9075-9 (SQL/MED). A cláusula `IF EXISTS` é uma extensão do PostgreSQL.

## Veja também

[Crie um Wrapper de Dados Estrangeiro](sql-createforeigndatawrapper.md "CREATE FOREIGN DATA WRAPPER"), [Altere o Wrapper de Dados Estrangeiro](sql-alterforeigndatawrapper.md "ALTER FOREIGN DATA WRAPPER")