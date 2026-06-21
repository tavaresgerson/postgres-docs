## Desconecte-se

DESESCONDO — parar de ouvir uma notificação

## Sinopse

```
UNLISTEN { channel | * }
```

## Descrição

`UNLISTEN` é usado para remover um registro existente para eventos `NOTIFY`. `UNLISTEN` anula qualquer registro existente da sessão atual do PostgreSQL como um ouvinte no canal de notificação denominado *`channel`*. O wildcard especial `*` anula todos os registros de ouvinte para a sessão atual.

[NOTIFICAR](sql-notify.md "NOTIFY") contém uma discussão mais extensa sobre o uso de `LISTEN` e `NOTIFY`.

## Parâmetros

*`channel`*: Nome de um canal de notificação (qualquer identificador).

`*`: Todos os registros de escuta atuais para esta sessão são limpos.

## Notas

Você pode desativar algo que não estava ouvindo; não haverá nenhum aviso ou erro.

No final de cada sessão, o `UNLISTEN *` é executado automaticamente.

Uma transação que foi executada com `UNLISTEN` não pode ser preparada para um compromisso de duas fases.

## Exemplos

Para fazer um registro:

```
LISTEN virtual;
NOTIFY virtual;
Asynchronous notification "virtual" received from server process with PID 8448.
```

Uma vez que `UNLISTEN` tenha sido executado, as mensagens adicionais de `NOTIFY` serão ignoradas:

```
UNLISTEN virtual;
NOTIFY virtual;
-- no NOTIFY event is received
```

## Compatibilidade

Não existe comando `UNLISTEN` no padrão SQL.

## Veja também

[ESCOLHER](sql-listen.md "LISTEN"), [NOTIFICAR](sql-notify.md "NOTIFY")