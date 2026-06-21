## 32.14. Sistema de Eventos [#](#LIBPQ-EVENTS)

* [32.14.1. Tipos de Evento](libpq-events.md#LIBPQ-EVENTS-TYPES)
* [32.14.2. Procedimento de Callback de Evento](libpq-events.md#LIBPQ-EVENTS-PROC)
* [32.14.3. Funções de Suporte de Evento](libpq-events.md#LIBPQ-EVENTS-FUNCS)
* [32.14.4. Exemplo de Evento](libpq-events.md#LIBPQ-EVENTS-EXAMPLE)

O sistema de eventos do libpq é projetado para notificar os manipuladores de eventos registrados sobre eventos interessantes do libpq, como a criação ou destruição de objetos `PGconn` e `PGresult`. Um caso de uso principal é que isso permite que as aplicações associem seus próprios dados a um `PGconn` ou `PGresult` e garantam que esses dados sejam liberados em um momento apropriado.

Cada manipulador de evento registrado é associado a dois pedaços de dados, conhecidos apenas pelo libpq como ponteiros opacos `void *`. Há um ponteiro *pass-through* que é fornecido pelo aplicativo quando o manipulador de evento é registrado com um `PGconn`. O ponteiro de passagem nunca muda ao longo da vida do `PGconn` e todos os `PGresult`s gerados a partir dele; portanto, se usado, ele deve apontar para dados de longa duração. Além disso, há um ponteiro de *dados de instância*, que começa com `NULL` em cada `PGconn` e `PGresult`. Esse ponteiro pode ser manipulado usando as funções [`PQinstanceData`](libpq-events.md#LIBPQ-PQINSTANCEDATA), [`PQsetInstanceData`](libpq-events.md#LIBPQ-PQSETINSTANCEDATA), [`PQresultInstanceData`](libpq-events.md#LIBPQ-PQRESULTINSTANCEDATA) e [`PQresultSetInstanceData`](libpq-events.md#LIBPQ-PQRESULTSETINSTANCEDATA). Note que, ao contrário do ponteiro de passagem, os dados de instância de um `PGconn` não são automaticamente herdados pelos `PGresult`s criados a partir dele. O libpq não sabe para o que os ponteiros de passagem e dados de instância apontam (se algo) e nunca tentará liberá-los — essa é a responsabilidade do manipulador de evento.

### 32.14.1. Tipos de evento [#](#LIBPQ-EVENTS-TYPES)

O enum `PGEventId` nomeia os tipos de eventos que são tratados pelo sistema de eventos. Todos os seus valores têm nomes que começam com `PGEVT`. Para cada tipo de evento, há uma estrutura de informações de evento correspondente que carrega os parâmetros passados aos manipuladores de eventos. Os tipos de eventos são:

`PGEVT_REGISTER` [#](#LIBPQ-PGEVT-REGISTER): O evento de registro ocorre quando [`PQregisterEventProc`](libpq-events.md#LIBPQ-PQREGISTEREVENTPROC) é chamado. É o momento ideal para inicializar qualquer procedimento de evento que possa ser necessário. Apenas um evento de registro será disparado por manipulador de evento por conexão. Se o procedimento de evento falhar (retorna zero), o registro é cancelado.

``` typedef struct { PGconn *conn; } PGEventRegister;
    ```

Quando um evento `PGEVT_REGISTER` é recebido, o ponteiro *`evtInfo`* deve ser convertido para um `PGEventRegister *`. Esta estrutura contém um `PGconn` que deve estar no status `CONNECTION_OK`; garantido se um chama `PQregisterEventProc`(libpq-events.md#LIBPQ-PQREGISTEREVENTPROC) logo após obter um bom `PGconn`. Ao retornar um código de falha, toda a limpeza deve ser realizada, pois nenhum evento `PGEVT_CONNDESTROY` será enviado.

`PGEVT_CONNRESET` [#](#LIBPQ-PGEVT-CONNRESET): O evento de reinicialização da conexão é disparado após a conclusão de [`PQreset`](libpq-connect.md#LIBPQ-PQRESET) ou `PQresetPoll`. Em ambos os casos, o evento só é disparado se o reinicialização foi bem-sucedida. O valor de retorno do procedimento do evento é ignorado no PostgreSQL v15 e versões posteriores. Com versões anteriores, no entanto, é importante retornar sucesso (não nulo) ou a conexão será abortado.

``` typedef struct { PGconn *conn; } PGEventConnReset;
    ```

Quando um evento `PGEVT_CONNRESET` é recebido, o ponteiro `evtInfo` deve ser convertido em um
*`PGEventConnReset *`*. Embora o conteúdo `PGconn` tenha sido apenas redefinido, todos os dados do evento permanecem inalterados. Este evento deve ser usado para redefinir/recarregar/requerir qualquer
`instanceData` associado. Note que, mesmo que o procedimento do evento não consiga processar `PGEVT_CONNRESET`, ele ainda receberá um evento `PGEVT_CONNDESTROY` quando a conexão for fechada.

`PGEVT_CONNDESTROY` [#](#LIBPQ-PGEVT-CONNDESTROY)
:   O evento de destruição de conexão é disparado em resposta a
    [`PQfinish`](libpq-connect.md#LIBPQ-PQFINISH). É responsabilidade do procedimento de evento limpar adequadamente seus dados de evento, pois o libpq não tem capacidade de gerenciar essa memória. A falha em limpar levará a vazamentos de memória.

    ```
    typedef struct { PGconn *conn; } PGEventConnDestroy;
    ```

Quando um evento `PGEVT_CONNDESTROY` é recebido, o ponteiro `evtInfo` deve ser convertido em um
*`PGEventConnDestroy *`*. Esse evento é disparado
antes de `PQfinish`(libpq-connect.md#LIBPQ-PQFINISH) realizar qualquer outra limpeza.
O valor de retorno do procedimento do evento é ignorado, uma vez que não há
sposób de indicar uma falha de `PQfinish`(libpq-connect.md#LIBPQ-PQFINISH). Além disso,
um falha no procedimento do evento não deve abortar o processo de limpeza
de memória indesejada.

O evento de criação de resultado é disparado em resposta a qualquer função de execução de consulta que gere um resultado, incluindo `PQgetResult` (libpq-async.md#LIBPQ-PQGETRESULT). Este evento só será disparado após o resultado ter sido criado com sucesso.

    ```
    typedef struct { PGconn *conn; PGresult *result; } PGEventResultCreate;
    ```

Quando um evento `PGEVT_RESULTCREATE` é recebido, o ponteiro *`evtInfo`* deve ser convertido em um
*`PGEventResultCreate *`*. O
*`conn`* é a conexão usada para gerar o
resultado. Este é o local ideal para inicializar qualquer
*`instanceData` que precisa ser associado ao
resultado. Se um procedimento de evento falhar (retorna zero), esse procedimento de evento será ignorado pelo restante da vida útil do resultado; ou seja, ele não receberá eventos
`PGEVT_RESULTCOPY` ou `PGEVT_RESULTDESTROY` para este resultado ou
resultados copiados a partir dele.

O evento de cópia de resultado é disparado em resposta a [#](#LIBPQ-PGEVT-RESULTCOPY). Este evento só será disparado após a cópia estar completa. Apenas os procedimentos de evento que tenham mantido com sucesso o evento `PGEVT_RESULTCREATE` ou `PGEVT_RESULTCOPY` para o resultado de origem receberão eventos `PGEVT_RESULTCOPY`.

    ```
    typedef struct { const PGresult *src; PGresult *dest; } PGEventResultCopy;
    ```

Quando um evento `PGEVT_RESULTCOPY` é recebido, o ponteiro *`evtInfo`* deve ser convertido para um
*`PGEventResultCopy *`*. O
*`src`* é o que foi copiado enquanto o
*`dest`* é o destino da cópia. Este evento pode ser usado para fornecer uma cópia profunda de `instanceData`,
já que `PQcopyResult` não pode fazer isso. Se um procedimento de evento falhar (retorna zero), esse procedimento de evento será
ignorado pelo restante da vida útil do novo resultado; ou seja, ele não receberá eventos
*`PGEVT_RESULTCOPY`
ou *`PGEVT_RESULTDESTROY`* para esse resultado ou
resultados copiados a partir dele.

O evento de destruição de resultado é disparado em resposta a um [#](#LIBPQ-PGEVT-RESULTDESTROY) . É responsabilidade do procedimento de evento limpar adequadamente seus dados de evento, pois o libpq não tem capacidade de gerenciar essa memória. A falha em limpar levará a vazamentos de memória.

    ```
    typedef struct { PGresult *result; } PGEventResultDestroy;
    ```

Quando um evento `PGEVT_RESULTDESTROY` é recebido, o ponteiro `evtInfo` deve ser convertido em um
*`PGEventResultDestroy *`. Este evento é disparado
antes de `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR) realizar qualquer outra limpeza.
O valor de retorno do procedimento do evento é ignorado, uma vez que não há
sposób de indicar uma falha de `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR). Além disso,
um falha no procedimento do evento não deve abortar o processo de limpeza
de memória indesejada.

### 32.14.2. Procedimento de Callback de Evento [#](#LIBPQ-EVENTS-PROC)

`PGEventProc` [#](#LIBPQ-PGEVENTPROC)
:   `PGEventProc` é um typedef para um ponteiro para um
    procedimento de evento, ou seja, a função de chamada de usuário que recebe
    eventos do libpq. A assinatura de um procedimento de evento deve ser

    ```
    int eventproc(PGEventId evtId, void *evtInfo, void *passThrough)
    ```

O parâmetro *`evtId`* indica qual evento ocorreu. O
*`PGEVT`* ponteiro deve ser convertido para o tipo de estrutura
apropriado para obter informações adicionais sobre o evento.
O parâmetro *`passThrough`* é o ponteiro fornecido ao
[`PQregisterEventProc`](libpq-events.md#LIBPQ-PQREGISTEREVENTPROC) quando o procedimento do evento foi
registrado. A função deve retornar um valor não nulo se tiver
sucesso e zero se falhar.

Um procedimento de evento específico pode ser registrado apenas uma vez em qualquer `PGconn`. Isso ocorre porque o endereço do procedimento é usado como uma chave de pesquisa para identificar os dados da instância associados.

### Atenção

Em Windows, as funções podem ter dois endereços diferentes: um visível de fora de uma DLL e outro visível de dentro da DLL. Deve-se ter cuidado para que apenas um desses endereços seja usado com as funções de procedimento de evento do libpq, caso contrário, haverá confusão. A regra mais simples para escrever código que funcionará é garantir que os procedimentos de evento sejam declarados `static`. Se o endereço do procedimento deve estar disponível fora de seu próprio arquivo de origem, exponha uma função separada para retornar o endereço.

### 32.14.3. Funções de Suporte a Eventos [#](#LIBPQ-EVENTS-FUNCS)

`PQregisterEventProc` [#](#LIBPQ-PQREGISTEREVENTPROC)
:   Registra um procedimento de callback de evento com o libpq.

    ```
    int PQregisterEventProc(PGconn *conn, PGEventProc proc, const char *name, void *passThrough);
    ```

Um procedimento de evento deve ser registrado uma vez em cada `PGconn` que você deseja receber eventos sobre. Não há limite, exceto a memória, sobre o número de procedimentos de evento que podem ser registrados com uma conexão. A função retorna um valor não nulo se for bem-sucedida e zero se falhar.

O argumento *`proc`* será chamado quando um evento do libpq for disparado. Seu endereço de memória também é usado para procurar `instanceData`. O argumento *`name`* é usado para referenciar o procedimento do evento em mensagens de erro. Este valor não pode ser `NULL` ou uma string de comprimento zero. A string de nome é copiada para o `PGconn`, então o que é passado não precisa ser de longa duração. O ponteiro *`passThrough`* é passado para o *`proc`* sempre que um evento ocorre. Este argumento pode ser `NULL`.

`PQsetInstanceData` [#](#LIBPQ-PQSETINSTANCEDATA)
:   Define a conexão do *`conn`*'s `instanceData`
    para o procedimento *`proc`* a *`data`*. Isso
    retorna não zero para sucesso e zero para falha. (A falha é
    possível apenas se *`proc`* não tiver sido registrado
    adequadamente em *`conn`*.)

    ```
    int PQsetInstanceData(PGconn *conn, PGEventProc proc, void *data);
    ```

`PQinstanceData` [#](#LIBPQ-PQINSTANCEDATA) Retorna a
    conexão *`conn`*'s `instanceData`
    associada ao procedimento *`proc`*,
    ou `NULL` se não houver nenhuma.

    ```
    void *PQinstanceData(const PGconn *conn, PGEventProc proc);
    ```

`PQresultSetInstanceData` [#](#LIBPQ-PQRESULTSETINSTANCEDATA)
:   Define o resultado `instanceData` para *`proc`* a *`data`*. Isso retorna não zero para sucesso e zero para falha. (A falha é apenas possível se *`proc`* não tiver sido registrado corretamente no resultado.)

    ```
    int PQresultSetInstanceData(PGresult *res, PGEventProc proc, void *data);
    ```

Cuidado para que qualquer armazenamento representado por *`data`* não seja contabilizado por `PQresultMemorySize` e (libpq-misc.md#LIBPQ-PQRESULTMEMORYSIZE), a menos que seja alocado usando `PQresultAlloc` e (libpq-misc.md#LIBPQ-PQRESULTALLOC). (Fazer isso é recomendável porque elimina a necessidade de liberar explicitamente tal armazenamento quando o resultado é destruído.)

`PQresultInstanceData` [#](#LIBPQ-PQRESULTINSTANCEDATA)  Retorna o resultado associado ao *`proc`*, ou `NULL`, se não houver nenhum.

    ```
    void *PQresultInstanceData(const PGresult *res, PGEventProc proc);
    ```

### 32.14.4. Exemplo de evento [#](#LIBPQ-EVENTS-EXAMPLE)

Aqui está um exemplo básico de gerenciamento de dados privados associados a conexões e resultados do libpq.

```
/* required header for libpq events (note: includes libpq-fe.h) */
#include <libpq-events.h>

/* The instanceData */ typedef struct { int n; char *str; } mydata;

/* PGEventProc */ static int myEventProc(PGEventId evtId, void *evtInfo, void *passThrough);

int main(void) { mydata *data; PGresult *res; PGconn *conn = PQconnectdb("dbname=postgres options=-csearch_path=");

    if (PQstatus(conn) != CONNECTION_OK) { /* PQerrorMessage's result includes a trailing newline */ fprintf(stderr, "%s", PQerrorMessage(conn)); PQfinish(conn); return 1; }

    /* called once on any connection that should receive events.
     * Sends a PGEVT_REGISTER to myEventProc. */ if (!PQregisterEventProc(conn, myEventProc, "mydata_proc", NULL)) { fprintf(stderr, "Cannot register PGEventProc\n"); PQfinish(conn); return 1; }

    /* conn instanceData is available */ data = PQinstanceData(conn, myEventProc);

    /* Sends a PGEVT_RESULTCREATE to myEventProc */ res = PQexec(conn, "SELECT 1 + 1");

    /* result instanceData is available */ data = PQresultInstanceData(res, myEventProc);

    /* If PG_COPYRES_EVENTS is used, sends a PGEVT_RESULTCOPY to myEventProc */ res_copy = PQcopyResult(res, PG_COPYRES_TUPLES | PG_COPYRES_EVENTS);

    /* result instanceData is available if PG_COPYRES_EVENTS was
     * used during the PQcopyResult call. */ data = PQresultInstanceData(res_copy, myEventProc);

    /* Both clears send a PGEVT_RESULTDESTROY to myEventProc */ PQclear(res); PQclear(res_copy);

    /* Sends a PGEVT_CONNDESTROY to myEventProc */ PQfinish(conn);

    return 0; }

static int myEventProc(PGEventId evtId, void *evtInfo, void *passThrough) { switch (evtId) { case PGEVT_REGISTER: { PGEventRegister *e = (PGEventRegister *)evtInfo; mydata *data = get_mydata(e->conn);

            /* associate app specific data with connection */ PQsetInstanceData(e->conn, myEventProc, data); break; }

        case PGEVT_CONNRESET: { PGEventConnReset *e = (PGEventConnReset *)evtInfo; mydata *data = PQinstanceData(e->conn, myEventProc);

            if (data) memset(data, 0, sizeof(mydata)); break; }

        case PGEVT_CONNDESTROY: { PGEventConnDestroy *e = (PGEventConnDestroy *)evtInfo; mydata *data = PQinstanceData(e->conn, myEventProc);

            /* free instance data because the conn is being destroyed */ if (data) free_mydata(data); break; }

        case PGEVT_RESULTCREATE: { PGEventResultCreate *e = (PGEventResultCreate *)evtInfo; mydata *conn_data = PQinstanceData(e->conn, myEventProc); mydata *res_data = dup_mydata(conn_data);

            /* associate app specific data with result (copy it from conn) */ PQresultSetInstanceData(e->result, myEventProc, res_data); break; }

        case PGEVT_RESULTCOPY: { PGEventResultCopy *e = (PGEventResultCopy *)evtInfo; mydata *src_data = PQresultInstanceData(e->src, myEventProc); mydata *dest_data = dup_mydata(src_data);

            /* associate app specific data with result (copy it from a result) */ PQresultSetInstanceData(e->dest, myEventProc, dest_data); break; }

        case PGEVT_RESULTDESTROY: { PGEventResultDestroy *e = (PGEventResultDestroy *)evtInfo; mydata *data = PQresultInstanceData(e->result, myEventProc);

            /* free instance data because the result is being destroyed */ if (data) free_mydata(data); break; }

        /* unknown event ID, just return true. */ default: break; }

    return true; /* event processing succeeded */ }
```
