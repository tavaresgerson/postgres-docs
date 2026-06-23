## 32.9. Notificação Assíncrona [#](#LIBPQ-NOTIFY)

O PostgreSQL oferece notificação assíncrona via os comandos `LISTEN` e `NOTIFY`. Uma sessão do cliente registra seu interesse em um canal de notificação específico com o comando `LISTEN` (e pode parar de ouvir com o comando `UNLISTEN`). Todas as sessões que estão ouvindo em um canal específico serão notificadas assincronicamente quando um comando `NOTIFY` com esse nome de canal for executado por qualquer sessão. Uma string de "carga" pode ser passada para comunicar dados adicionais aos ouvintes.

As aplicações libpq enviam os comandos `LISTEN`, `UNLISTEN` e `NOTIFY` como comandos SQL comuns. A chegada das mensagens `NOTIFY` pode ser detectada posteriormente, chamando `PQnotifies`.

A função `PQnotifies` retorna a próxima notificação de uma lista de mensagens de notificação não tratadas recebidas do servidor. Ela retorna um ponteiro nulo se não houver notificações pendentes. Uma vez que uma notificação é devolvida a partir de `PQnotifies`, ela é considerada tratada e será removida da lista de notificações.

```
PGnotify *PQnotifies(PGconn *conn);

typedef struct pgNotify
{
    char *relname;              /* notification channel name */
    int  be_pid;                /* process ID of notifying server process */
    char *extra;                /* notification payload string */
} PGnotify;
```

Após processar um objeto `PGnotify` retornado por `PQnotifies`, certifique-se de liberá-lo com [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM). É suficiente liberar o ponteiro `PGnotify`; os campos `relname` e `extra` não representam alocações separadas. (Os nomes desses campos são históricos; em particular, os nomes dos canais não precisam ter nada a ver com os nomes das relações.)

[Exemplo 32.2](libpq-example.md#LIBPQ-EXAMPLE-2) fornece um programa de amostra que ilustra o uso de notificação assíncrona.

`PQnotifies` não lê dados do servidor; ele apenas retorna mensagens que foram absorvidas anteriormente por outra função do libpq. Em versões antigas do libpq, a única maneira de garantir a recepção oportuna das mensagens `NOTIFY` era submeter constantemente comandos, mesmo que vazios, e depois verificar `PQnotifies` após cada [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC). Embora isso ainda funcione, é desaconselhável como um desperdício de poder de processamento.

Uma maneira melhor de verificar mensagens de `NOTIFY` quando você não tem comandos úteis para executar é chamar `PQconsumeInput`(libpq-async.md#LIBPQ-PQCONSUMEINPUT), em seguida, verificar `PQnotifies`. Você pode usar `select()` para esperar pelos dados chegarem do servidor, não usando, assim, nenhuma energia da CPU, a menos que haja algo a ser feito. (Veja [`PQsocket`](libpq-status.md#LIBPQ-PQSOCKET) para obter o número do descritor de arquivo a ser usado com `select()`.). Observe que isso funcionará bem, seja enviando comandos com `PQsendQuery`[[(libpq-async.md#LIBPQ-PQSENDQUERY)]/`PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) ou simplesmente usando `PQexec`(libpq-exec.md#LIBPQ-PQEXEC). No entanto, você deve lembrar-se de verificar `PQnotifies` após cada [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) ou [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC)], para ver se alguma notificação foi recebida durante o processamento do comando.