## 38.3. Um exemplo completo de gatilho de evento [#](#EVENT-TRIGGER-EXAMPLE)

Aqui está um exemplo muito simples de uma função de gatilho de evento escrita em C. (Exemplos de gatilhos escritos em linguagens procedimentais podem ser encontrados na documentação das linguagens procedimentais.)

A função `noddl` gera uma exceção cada vez que é chamada. A definição do gatilho de evento associou a função ao evento `ddl_command_start`. O efeito é que todos os comandos DDL (com as exceções mencionadas no [Seção 38.1](event-trigger-definition.md)) são impedidos de serem executados.

Este é o código-fonte da função de gatilho:

```
#include "postgres.h"

#include "commands/event_trigger.h"
#include "fmgr.h"

PG_MODULE_MAGIC;

PG_FUNCTION_INFO_V1(noddl);

Datum
noddl(PG_FUNCTION_ARGS)
{
    EventTriggerData *trigdata;

    if (!CALLED_AS_EVENT_TRIGGER(fcinfo))  /* internal error */
        elog(ERROR, "not fired by event trigger manager");

    trigdata = (EventTriggerData *) fcinfo->context;

    ereport(ERROR,
            (errcode(ERRCODE_INSUFFICIENT_PRIVILEGE),
             errmsg("command \"%s\" denied",
                    GetCommandTagName(trigdata->tag))));

    PG_RETURN_NULL();
}
```

Depois de compilar o código-fonte (consulte [Seção 36.10.5](xfunc-c.md#DFUNC)), declare a função e os gatilhos:

```
CREATE FUNCTION noddl() RETURNS event_trigger
    AS 'noddl' LANGUAGE C;

CREATE EVENT TRIGGER noddl ON ddl_command_start
    EXECUTE FUNCTION noddl();
```

Agora você pode testar o funcionamento do gatilho:

```
=# \dy
                     List of event triggers
 Name  |       Event       | Owner | Enabled | Function | Tags
-------+-------------------+-------+---------+----------+------
 noddl | ddl_command_start | dim   | enabled | noddl    |
(1 row)

=# CREATE TABLE foo(id serial);
ERROR:  command "CREATE TABLE" denied
```

Nessa situação, para poder executar alguns comandos DDL quando você precisar, você deve descartar o gatilho do evento ou desativá-lo. Pode ser conveniente desativar o gatilho apenas durante a duração de uma transação:

```
BEGIN;
ALTER EVENT TRIGGER noddl DISABLE;
CREATE TABLE foo (id serial);
ALTER EVENT TRIGGER noddl ENABLE;
COMMIT;
```

(Lembre-se de que os comandos DDL em gatilhos de eventos não são afetados por gatilhos de eventos.)