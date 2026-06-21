## DROP EVENT TRIGGER

DROP EVENT TRIGGER — remova um gatilho de evento

## Sinopse

```
DROP EVENT TRIGGER [ IF EXISTS ] name [ CASCADE | RESTRICT ]
```

## Descrição

`DROP EVENT TRIGGER` remove um gatilho de evento existente. Para executar este comando, o usuário atual deve ser o proprietário do gatilho de evento.

## Parâmetros

`IF EXISTS`: Não exija erro se o gatilho do evento não existir. Um aviso é emitido neste caso.

*`name`*: O nome do gatilho de evento a ser removido.

`CASCADE`: Descarte automaticamente os objetos que dependem do gatilho e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT`: Rejeitar a eliminação do gatilho se quaisquer objetos dependerem dele. Esse é o padrão.

## Exemplos

Destruir o gatilho `snitch`:

```
DROP EVENT TRIGGER snitch;
```

## Compatibilidade

Não há nenhuma declaração `DROP EVENT TRIGGER` no padrão SQL.

## Veja também

[Crie um gatilho de evento](sql-createeventtrigger.md "CREATE EVENT TRIGGER"), [Altere um gatilho de evento](sql-altereventtrigger.md "ALTER EVENT TRIGGER")