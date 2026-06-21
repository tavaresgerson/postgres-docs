## DROP SERVER

DROP SERVER — remova um descritor de servidor estrangeiro

## Sinopse

```
DROP SERVER [ IF EXISTS ] name [, ...] [ CASCADE | RESTRICT ]
```

## Descrição

`DROP SERVER` remove um descritor de servidor estrangeiro existente. Para executar este comando, o usuário atual deve ser o proprietário do servidor.

## Parâmetros

`IF EXISTS`: Não exija erro se o servidor não existir. Um aviso é emitido neste caso.

*`name`*: O nome de um servidor existente.

`CASCADE`: Descarte automaticamente os objetos que dependem do servidor (como mapeamentos de usuários) e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a interrupção do servidor se quaisquer objetos dependere disso. Esse é o padrão.

## Exemplos

Deixe um servidor `foo` se ele existir:

```
DROP SERVER IF EXISTS foo;
```

## Compatibilidade

`DROP SERVER` está em conformidade com a ISO/IEC 9075-9 (SQL/MED). A cláusula `IF EXISTS` é uma extensão do PostgreSQL.

## Veja também

[Crie servidor](sql-createserver.md "CREATE SERVER"), [Alterar servidor](sql-alterserver.md "ALTER SERVER")