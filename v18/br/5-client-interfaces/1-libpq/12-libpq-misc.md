## 32.12. Funções Diversas [#](#LIBPQ-MISC)

Como sempre, há algumas funções que simplesmente não cabem em nenhum lugar.

`PQfreemem` [#](#LIBPQ-PQFREEMEM): Libera a memória alocada pelo libpq.

```
void PQfreemem(void *ptr);
```

Libera a memória alocada pelo libpq, particularmente `PQescapeByteaConn`(libpq-exec.md#LIBPQ-PQESCAPEBYTEACONN), `PQescapeBytea`(libpq-exec.md#LIBPQ-PQESCAPEBYTEA), `PQunescapeBytea`(libpq-exec.md#LIBPQ-PQUNESCAPEBYTEA) e `PQnotifies`. É particularmente importante que esta função, em vez de `free()`, seja usada em sistemas Microsoft Windows. Isso ocorre porque alocar memória em uma DLL e liberá-la na aplicação só funciona se os flags multithread/single-threaded, release/debug e static/dynamic forem os mesmos para a DLL e a aplicação. Em plataformas que não são do Microsoft Windows, esta função é a mesma que a função da biblioteca padrão `free()`.

`PQconninfoFree` [#](#LIBPQ-PQCONNINFOFREE): Libera as estruturas de dados alocadas por [`PQconndefaults`](libpq-connect.md#LIBPQ-PQCONNDEFAULTS) ou [`PQconninfoParse`](libpq-connect.md#LIBPQ-PQCONNINFOPARSE).

```
void PQconninfoFree(PQconninfoOption *connOptions);
```

Se o argumento for um ponteiro `NULL`, nenhuma operação é realizada.

Um simples `PQfreemem` não será suficiente para isso, pois o array contém referências a strings subsidiárias.

`PQencryptPasswordConn` [#](#LIBPQ-PQENCRYPTPASSWORDCONN): Prepara a forma criptografada de uma senha do PostgreSQL.

```
char *PQencryptPasswordConn(PGconn *conn, const char *passwd, const char *user, const char *algorithm);
```

Essa função é destinada a ser usada por aplicativos de clientes que desejam enviar comandos como `ALTER USER joe PASSWORD 'pwd'`. É uma boa prática não enviar a senha em texto claro original em tal comando, porque ela pode ser exposta em logs de comando, exibições de atividade, e assim por diante. Em vez disso, use essa função para converter a senha para forma criptografada antes de enviá-la.

Os argumentos *`passwd`* e *`user`* são a senha em texto claro, e o nome SQL do usuário para o qual ela é destinada. *`algorithm`* especifica o algoritmo de criptografia a ser usado para criptografar a senha. Os algoritmos atualmente suportados são `md5` e `scram-sha-256` (`on` e `off` também são aceitos como aliases para `md5`, para compatibilidade com versões de servidor mais antigas). Note que o suporte para `scram-sha-256` foi introduzido na versão 10 do PostgreSQL, e não funcionará corretamente com versões de servidor mais antigas. Se *`algorithm`* é `NULL`, esta função consultará o servidor pelo valor atual do [[password_encryption](runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION)], o que pode bloquear e falhar se a transação atual for abortada, ou se a conexão estiver ocupada executando outra consulta. Se você deseja usar o algoritmo padrão do servidor, mas deseja evitar o bloqueio, consulte `password_encryption` você mesmo antes de chamar [`PQencryptPasswordConn`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORDCONN), e passe esse valor como o *`algorithm`*.

O valor de retorno é uma string alocada por `malloc`. O chamador pode assumir que a string não contém caracteres especiais que exijam escapagem. Use `PQfreemem`(libpq-misc.md#LIBPQ-PQFREEMEM) para liberar o resultado quando estiver pronto. Em caso de erro, retorna `NULL`, e uma mensagem adequada é armazenada no objeto de conexão.

`PQchangePassword` [#](#LIBPQ-PQCHANGEPASSWORD): Altera uma senha do PostgreSQL.

```
PGresult *PQchangePassword(PGconn *conn, const char *user, const char *passwd);
```

Essa função usa `PQencryptPasswordConn` para construir e executar o comando `ALTER USER ... PASSWORD '...'`, alterando assim a senha do usuário. Ela existe pelo mesmo motivo que `PQencryptPasswordConn`, mas é mais conveniente, pois constrói e executa o comando para você. `PQencryptPasswordConn` é passada um `NULL` para o argumento do algoritmo, portanto, a criptografia é feita de acordo com a configuração do servidor [criptografia de senha](runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION).

Os argumentos *`user`* e *`passwd`* são os nomes SQL do usuário alvo e a nova senha em texto claro.

Retorna um ponteiro `PGresult` que representa o resultado do comando `ALTER USER`, ou um ponteiro nulo se a rotina falhou antes de emitir qualquer comando. A função [[`PQresultStatus`](libpq-exec.md#LIBPQ-PQRESULTSTATUS)] deve ser chamada para verificar o valor de retorno por quaisquer erros (incluindo o valor de um ponteiro nulo, no caso, ela retornará `PGRES_FATAL_ERROR`). Use [[`PQerrorMessage`](libpq-status.md#LIBPQ-PQERRORMESSAGE)] para obter mais informações sobre tais erros.

`PQencryptPassword` [#](#LIBPQ-PQENCRYPTPASSWORD) :   Prepara o formulário criptografado md5 de uma senha do PostgreSQL.

```
char *PQencryptPassword(const char *passwd, const char *user);
```

[`PQencryptPassword`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORD) é uma versão mais antiga e descontinuada de [`PQencryptPasswordConn`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORDCONN). A diferença é que [`PQencryptPassword`](libpq-misc.md#LIBPQ-PQENCRYPTPASSWORD) não requer um objeto de conexão, e `md5` é sempre usado como o algoritmo de criptografia.

`PQmakeEmptyPGresult` [#](#LIBPQ-PQMAKEEMPTYPGRESULT): Construi um objeto vazio `PGresult` com o status fornecido.

```
PGresult *PQmakeEmptyPGresult(PGconn *conn, ExecStatusType status);
```

Esta é a função interna do libpq para alocar e inicializar um objeto vazio `PGresult`. Esta função retorna `NULL` se a memória não puder ser alocada. Ela é exportada porque algumas aplicações acham útil gerar objetos de resultado (particularmente objetos com status de erro) por si mesmos. Se *`conn`* não é nulo e *`status`* indica um erro, a mensagem de erro atual da conexão especificada é copiada no `PGresult`. Além disso, se *`conn`* não é nulo, quaisquer procedimentos de evento registrados na conexão são copiados no `PGresult`. (Eles não recebem chamadas de `PGEVT_RESULTCREATE`, mas veja [`PQfireResultCreateEvents`](libpq-misc.md#LIBPQ-PQFIRERESULTCREATEEVENTS).). Note que [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) deve ser chamado eventualmente no objeto, assim como com um `PGresult` retornado pelo próprio libpq.

`PQfireResultCreateEvents` [#](#LIBPQ-PQFIRERESULTCREATEEVENTS): Arremende o evento `PGEVT_RESULTCREATE` (ver [Seção 32.14](libpq-events.md "32.14. Event System")) para cada procedimento de evento registrado no `PGresult` objeto. Retorna não nulo para sucesso, zero se qualquer procedimento de evento falhar.

```
int PQfireResultCreateEvents(PGconn *conn, PGresult *res);
```

O argumento `conn` é passado para os procedimentos de evento, mas não é usado diretamente. Ele pode ser `NULL` se os procedimentos de evento não o usarem.

Os procedimentos de evento que já receberam um `PGEVT_RESULTCREATE` ou `PGEVT_RESULTCOPY` para este objeto não são acionados novamente.

A principal razão pela qual essa função é separada de `PQmakeEmptyPGresult`(libpq-misc.md#LIBPQ-PQMAKEEMPTYPGRESULT) é que, muitas vezes, é apropriado criar um `PGresult` e preenchê-lo com dados antes de invocar os procedimentos do evento.

`PQcopyResult` [#](#LIBPQ-PQCOPYRESULT)   Faz uma cópia de um objeto `PGresult`. A cópia não está vinculada à origem de qualquer forma e [`PQclear`](libpq-exec.md#LIBPQ-PQCLEAR) deve ser chamada quando a cópia não é mais necessária. Se a função falhar, `NULL` é retornado.

```
PGresult *PQcopyResult(const PGresult *src, int flags);
```

Este não é um objetivo de fazer uma cópia exata. O resultado retornado é sempre colocado no status `PGRES_TUPLES_OK`, e não copia nenhuma mensagem de erro na fonte. (Ele, no entanto, copia a string de status do comando.) O argumento *`flags`* determina o que mais é copiado. É uma OR bit a bit de várias flags. `PG_COPYRES_ATTRS` especifica a cópia dos atributos do resultado da fonte (definições de colunas). `PG_COPYRES_TUPLES` especifica a cópia dos tuplos do resultado da fonte. (Isso implica a cópia dos atributos também.) `PG_COPYRES_NOTICEHOOKS` especifica a cópia dos ganchos de notificação do resultado da fonte. `PG_COPYRES_EVENTS` especifica a cópia dos eventos do resultado da fonte. (Mas qualquer dado de instância associado à fonte não é copiado.) Os procedimentos de evento recebem eventos `PGEVT_RESULTCOPY`.

`PQsetResultAttrs` [#](#LIBPQ-PQSETRESULTATTRS) :   Define os atributos de um objeto `PGresult`.

```
int PQsetResultAttrs(PGresult *res, int numAttributes, PGresAttDesc *attDescs);
```

Os valores fornecidos em *`attDescs`* são copiados no resultado. Se o ponteiro *`attDescs`* for `NULL` ou *`numAttributes`* for menor que um, a solicitação é ignorada e a função tem sucesso. Se *`res`* já contiver atributos, a função falhará. Se a função falhar, o valor de retorno é zero. Se a função tiver sucesso, o valor de retorno é diferente de zero.

`PQsetvalue` [#](#LIBPQ-PQSETVALUE): Define o valor de um campo tupla de um objeto `PGresult`.

```
int PQsetvalue(PGresult *res, int tup_num, int field_num, char *value, int len);
```

A função aumentará automaticamente a matriz de tuplas internas do resultado conforme necessário. No entanto, o argumento *`tup_num`* deve ser menor ou igual a [[`PQntuples`](libpq-exec.md#LIBPQ-PQNTUPLES)], o que significa que essa função só pode aumentar a matriz de tuplas uma tupla de cada vez. Mas qualquer campo de qualquer tupla existente pode ser modificado em qualquer ordem. Se um valor em *`field_num`* já existir, ele será sobrescrito. Se *`len`* for -1 ou *`value`* for `NULL`, o valor do campo será definido como um valor nulo do SQL. O *`value`* é copiado no armazenamento privado do resultado, portanto, não é mais necessário após o retorno da função. Se a função falhar, o valor de retorno é zero. Se a função tiver sucesso, o valor de retorno não é nulo.

`PQresultAlloc` [#](#LIBPQ-PQRESULTALLOC): Alocar armazenamento subsidiário para um objeto `PGresult`.

```
void *PQresultAlloc(PGresult *res, size_t nBytes);
```

Qualquer memória alocada com essa função será liberada quando o *`res`* for limpo. Se a função falhar, o valor de retorno é `NULL`. O resultado é garantido para estar adequadamente alinhado para qualquer tipo de dados, assim como para `malloc`.

`PQresultMemorySize` [#](#LIBPQ-PQRESULTMEMORYSIZE): Retém o número de bytes alocados para um objeto `PGresult`.

```
size_t PQresultMemorySize(const PGresult *res);
```

Esse valor é a soma de todas as solicitações `malloc` associadas ao objeto `PGresult`, ou seja, toda a memória que será liberada por `PQclear`(libpq-exec.md#LIBPQ-PQCLEAR). Essa informação pode ser útil para gerenciar o consumo de memória.

`PQlibVersion` [#](#LIBPQ-PQLIBVERSION) : Retorne a versão do libpq que está sendo usada.

```
int PQlibVersion(void);
```

O resultado dessa função pode ser usado para determinar, no momento da execução, se uma funcionalidade específica está disponível na versão atualmente carregada do libpq. A função pode ser usada, por exemplo, para determinar quais opções de conexão estão disponíveis em `PQconnectdb`(libpq-connect.md#LIBPQ-PQCONNECTDB).

O resultado é formado pela multiplicação do número da versão principal da biblioteca por 10000 e pela adição do número da versão menor. Por exemplo, a versão 10.1 será retornada como 100001, e a versão 11.0 será retornada como 110000.

Antes da versão principal 10, o PostgreSQL usava números de versão de três partes, nas quais as duas primeiras partes juntas representavam a versão principal. Para essas versões, `PQlibVersion` (libpq-misc.md#LIBPQ-PQLIBVERSION) usa dois dígitos para cada parte; por exemplo, a versão 9.1.5 será retornada como 90105, e a versão 9.2.0 será retornada como 90200.

Portanto, para fins de determinação da compatibilidade de recursos, as aplicações devem dividir o resultado de `PQlibVersion`(libpq-misc.md#LIBPQ-PQLIBVERSION) por 100 e não por 10000 para determinar um número lógico de versão principal. Em todas as séries de lançamento, apenas os dois últimos dígitos diferem entre as versões menores (releases de correção de bugs).

Nota

Essa função apareceu na versão 9.1 do PostgreSQL, portanto, não pode ser usada para detectar funcionalidades necessárias em versões anteriores, pois chamá-la criará uma dependência de vínculo na versão 9.1 ou posterior.

`PQgetCurrentTimeUSec` [#](#LIBPQ-PQGETCURRENTTIMEUSEC): Retém o horário atual, expresso como o número de microsegundos desde a época Unix (ou seja, `time_t` vezes 1 milhão).

```
pg_usec_time_t PQgetCurrentTimeUSec(void);
```

Isso é principalmente útil para calcular os valores de tempo de espera a serem usados com `PQsocketPoll`(libpq-connect.md#LIBPQ-PQSOCKETPOLL).