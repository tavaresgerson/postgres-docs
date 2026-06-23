## ALTER EVENT TRIGGER

ALTER EVENT TRIGGER — alterar a definição de um gatilho de evento

## Sinopse

```
ALTER EVENT TRIGGER name DISABLE
ALTER EVENT TRIGGER name ENABLE [ REPLICA | ALWAYS ]
ALTER EVENT TRIGGER name OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
ALTER EVENT TRIGGER name RENAME TO new_name
```

## Descrição

`ALTER EVENT TRIGGER` altera as propriedades de um gatilho de evento existente.

Você deve ser um superusuário para alterar um gatilho de evento.

## Parâmetros

*`name`*: O nome de um gatilho existente para alterar.

*`new_owner`*: O nome do usuário do novo proprietário do gatilho de evento.

*`new_name`*: O novo nome do gatilho do evento.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ]`: Esses formulários configuram o disparo dos gatilhos de evento. Ainda é conhecido ao sistema que um gatilho desativado é executado, mas não é executado quando seu evento de disparo ocorre. Veja também [session_replication_role](runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE).

## Compatibilidade

Não há nenhuma declaração `ALTER EVENT TRIGGER` no padrão SQL.

## Veja também

[Crie um gatilho de evento](sql-createeventtrigger.md "CREATE EVENT TRIGGER"), [Remova um gatilho de evento](sql-dropeventtrigger.md "DROP EVENT TRIGGER")