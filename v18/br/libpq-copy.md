## 32.10. Funções associadas ao comando `COPY` [#](#LIBPQ-COPY)

* [32.10.1. Funções para enviar dados do `COPY`](libpq-copy.md#LIBPQ-COPY-SEND)
* [32.10.2. Funções para receber dados do `COPY`](libpq-copy.md#LIBPQ-COPY-RECEIVE)
* [32.10.3. Funções obsoletas para `COPY`](libpq-copy.md#LIBPQ-COPY-DEPRECATED)

O comando `COPY` no PostgreSQL tem opções para ler ou escrever na conexão de rede usada pelo libpq. As funções descritas nesta seção permitem que as aplicações aproveitem essa capacidade fornecendo ou consumindo dados copiados.

O processo geral é que o aplicativo emite primeiro o comando SQL `COPY` via [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) ou uma das funções equivalentes. A resposta a isso (se não houver erro no comando) será um objeto `PGresult` com um código de status de `PGRES_COPY_OUT` ou `PGRES_COPY_IN` (dependendo da direção de cópia especificada). O aplicativo deve então usar as funções desta seção para receber ou transmitir linhas de dados. Quando a transferência de dados estiver completa, outro objeto `PGresult` será retornado para indicar o sucesso ou o fracasso da transferência. Seu status será `PGRES_COMMAND_OK` para sucesso ou `PGRES_FATAL_ERROR` se algum problema for encontrado. Neste ponto, outros comandos SQL podem ser emitidos via [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC). (Não é possível executar outros comandos SQL usando a mesma conexão enquanto a operação `COPY` está em andamento.)

Se um comando `COPY` for emitido via [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) em uma string que pode conter comandos adicionais, o aplicativo deve continuar a obter resultados via [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) após completar a sequência `COPY`. Somente quando [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) retorna `NULL` é certo que a string de comandos [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) está concluída e é seguro emitir mais comandos.

As funções desta seção devem ser executadas apenas após obter um status de resultado de `PGRES_COPY_OUT` ou `PGRES_COPY_IN` de [`PQexec`](libpq-exec.md#LIBPQ-PQEXEC) ou [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT).

Um objeto `PGresult` que possui um desses valores de status carrega alguns dados adicionais sobre a operação `COPY` que está começando. Esses dados adicionais estão disponíveis usando funções que também são usadas em conexão com os resultados da consulta:

`PQnfields` [#](#LIBPQ-PQNFIELDS-1): Retorna o número de colunas (campos) a serem copiadas.

`PQbinaryTuples` [#](#LIBPQ-PQBINARYTUPLES-1): 0 indica que o formato geral de cópia é textual (linhas separadas por novas linhas, colunas separadas por caracteres de separador, etc.). 1 indica que o formato geral de cópia é binário. Consulte [COPY](sql-copy.md "COPY") para obter mais informações.

`PQfformat` [#](#LIBPQ-PQFFORMAT-1): Retorna o código de formato (0 para texto, 1 para binário) associado a cada coluna da operação de cópia. Os códigos de formato por coluna sempre serão zero quando o formato geral de cópia for textual, mas o formato binário pode suportar colunas de texto e binário. (No entanto, a partir da implementação atual de `COPY`, apenas colunas binárias aparecem em uma cópia binária; portanto, os formatos por coluna sempre correspondem ao formato geral no momento.)

### 32.10.1. Funções para envio de dados `COPY` [#](#LIBPQ-COPY-SEND)

Essas funções são usadas para enviar dados durante `COPY FROM STDIN`. Elas falharão se chamadas quando a conexão não estiver no estado `COPY_IN`.

`PQputCopyData` [#](#LIBPQ-PQPUTCOPYDATA): Envia dados para o servidor durante o estado `COPY_IN`.

```
int PQputCopyData(PGconn *conn, const char *buffer, int nbytes);
```

Transmite os dados `COPY` no *`buffer` especificado, com comprimento *`nbytes`*, para o servidor. O resultado é 1 se os dados estiverem em fila, zero se não estiverem em fila devido a buffers cheios (isso ocorrerá apenas no modo não bloqueante), ou -1 se ocorrer um erro. (Use `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter detalhes se o valor de retorno for -1. Se o valor for zero, espere pela escrita pronta e tente novamente.)

O aplicativo pode dividir o fluxo de dados `COPY` em cargas de buffer de qualquer tamanho conveniente. Os limites de carga de buffer não têm significado semântico durante a transmissão. O conteúdo do fluxo de dados deve corresponder ao formato de dados esperado pelo comando `COPY`; consulte [COPY](sql-copy.md "COPY") para detalhes.

`PQputCopyEnd` [#](#LIBPQ-PQPUTCOPYEND): Envia indicação de fim de dados ao servidor durante o estado `COPY_IN`.

```
int PQputCopyEnd(PGconn *conn, const char *errormsg);
```

Finaliza a operação `COPY_IN` com sucesso se *`errormsg`* for `NULL`. Se *`errormsg`* não for `NULL`, então o `COPY` é forçado a falhar, com a string apontada por *`errormsg`* usada como a mensagem de erro. (Não se deve asumir que essa mensagem de erro exata será devolvida pelo servidor, no entanto, pois o servidor pode ter já falhado a `COPY` por suas próprias razões.)

O resultado é 1 se a mensagem de término foi enviada; ou, em modo não bloqueante, isso pode indicar apenas que a mensagem de término foi colocada com sucesso na fila. (Em modo não bloqueante, para ter certeza de que os dados foram enviados, você deve esperar pela condição de escrita pronta e chamar `PQflush`(libpq-async.md#LIBPQ-PQFLUSH), repetindo até que retorne zero.) Zero indica que a função não pôde colocar a mensagem de término devido a buffers completos; isso só acontece em modo não bloqueante. (Neste caso, espere pela condição de escrita pronta e tente novamente a chamada `PQputCopyEnd`(libpq-copy.md#LIBPQ-PQPUTCOPYEND). ) Se ocorrer um erro grave, -1 é retornado; você pode usar `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter detalhes.

Após chamar com sucesso `PQputCopyEnd`](libpq-copy.md#LIBPQ-PQPUTCOPYEND), chame `PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) para obter o status final do resultado do comando `COPY`. Pode esperar que esse resultado esteja disponível de forma usual. Em seguida, volte à operação normal.

### 32.10.2. Funções para Receber Dados do `COPY` [#](#LIBPQ-COPY-RECEIVE)

Essas funções são usadas para receber dados durante `COPY TO STDOUT`. Elas falharão se chamadas quando a conexão não estiver no estado de `COPY_OUT`.

`PQgetCopyData` [#](#LIBPQ-PQGETCOPYDATA): Recebe dados do servidor durante o estado `COPY_OUT`.

```
int PQgetCopyData(PGconn *conn, char **buffer, int async);
```

Tentados para obter outra linha de dados do servidor durante um `COPY`. Os dados são sempre retornados uma linha de dados de cada vez; se apenas uma linha parcial estiver disponível, ela não é retornada. O retorno bem-sucedido de uma linha de dados envolve a alocação de um pedaço de memória para armazenar os dados. O parâmetro *`buffer`* deve ser não `NULL`. *`*buffer`* é definido para apontar para a memória alocada, ou para `NULL` em casos onde nenhum buffer é retornado. Um buffer com resultado não `NULL` deve ser liberado usando [`PQfreemem`](libpq-misc.md#LIBPQ-PQFREEMEM) quando não for mais necessário.

Quando uma linha é devolvida com sucesso, o valor de retorno é o número de bytes de dados na linha (este sempre será maior que zero). A string devolvida é sempre terminada com um nulo, embora isso provavelmente seja útil apenas para texto `COPY`. Um resultado de zero indica que o `COPY` ainda está em progresso, mas ainda não há uma linha disponível (isso é possível apenas quando *`async`* é verdadeiro). Um resultado de -1 indica que o `COPY` está concluído. Um resultado de -2 indica que ocorreu um erro (consulte `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para o motivo).

Quando *`async`* é verdadeiro (não zero), [[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA) não bloqueará a espera por entrada; ele retornará zero se o [[`COPY`]] ainda estiver em andamento, mas não houver uma linha completa disponível. (Neste caso, espere pela leitura pronta e, em seguida, chame [[`PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT)]] antes de chamar novamente [[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA)].) Quando *`async`* é falso (zero), [[`PQgetCopyData`](libpq-copy.md#LIBPQ-PQGETCOPYDATA) bloqueará até que os dados estejam disponíveis ou a operação seja concluída.

Após `PQgetCopyData` retornar -1, chame (libpq-copy.md#LIBPQ-PQGETCOPYDATA) para obter o status final do resultado do comando `PQgetResult`. Pode esperar que esse resultado esteja disponível da maneira usual. Em seguida, volte à operação normal.

### 32.10.3. Funções obsoletas para `COPY` [#](#LIBPQ-COPY-DEPRECATED)

Essas funções representam métodos mais antigos de manipulação do `COPY`. Embora ainda funcionem, elas são desaconselhadas devido ao mau gerenciamento de erros, métodos inconvenientes de detecção de fim de dados e falta de suporte para transferências binárias ou não bloqueáveis.

`PQgetline` [#](#LIBPQ-PQGETLINE) :   Leia uma linha de caracteres (transmitida pelo servidor) terminada por nova linha em uma string de buffer do tamanho de *`length`*.

```
int PQgetline(PGconn *conn, char *buffer, int length);
```

Essa função copia até *`length`*-1 caracteres no buffer e converte o caractere de nova linha final em um byte zero. `PQgetline`(libpq-copy.md#LIBPQ-PQGETLINE) retorna `EOF` no final da entrada, 0 se toda a linha tiver sido lida e 1 se o buffer estiver cheio, mas o caractere de nova linha final ainda não tiver sido lido.

Observe que o aplicativo deve verificar se uma nova linha consiste nos dois caracteres `\.`, que indica que o servidor terminou de enviar os resultados do comando `COPY`. Se o aplicativo pode receber linhas que têm mais de *`length`*-1 caracteres, é necessário ter certeza de que reconhece a linha `\.` corretamente (e não, por exemplo, confunde o final de uma linha de dados longa por uma linha de terminação).

`PQgetlineAsync` [#](#LIBPQ-PQGETLINEASYNC) :   Leia uma linha de dados `COPY` (transmitida pelo servidor) em um buffer sem bloquear.

```
int PQgetlineAsync(PGconn *conn, char *buffer, int bufsize);
```

Essa função é semelhante a `PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE), mas pode ser usada por aplicativos que precisam ler os dados do `COPY` de forma assíncrona, ou seja, sem bloquear. Após emitir o comando `COPY` e receber uma resposta do `PGRES_COPY_OUT`, o aplicativo deve chamar `PQconsumeInput`](libpq-async.md#LIBPQ-PQCONSUMEINPUT) e `PQgetlineAsync`](libpq-copy.md#LIBPQ-PQGETLINEASYNC) até que o sinal de fim de dados seja detectado.

Ao contrário de `PQgetline`(libpq-copy.md#LIBPQ-PQGETLINE), esta função assume a responsabilidade de detectar o fim de dados.

Em cada chamada, `PQgetlineAsync`(libpq-copy.md#LIBPQ-PQGETLINEASYNC) retornará dados se uma linha de dados completa estiver disponível no buffer de entrada do libpq. Caso contrário, nenhum dado será retornado até que o restante da linha chegue. A função retornará -1 se o marcador de fim de dados de cópia tiver sido reconhecido, ou 0 se nenhum dado estiver disponível, ou um número positivo que indique o número de bytes de dados retornados. Se -1 for retornado, o chamador deve então chamar `PQendcopy`(libpq-copy.md#LIBPQ-PQENDCOPY) e, em seguida, retornar ao processamento normal.

Os dados retornados não se estenderão além de um limite de linha de dados. Se possível, uma linha inteira será retornada de uma só vez. Mas se o buffer oferecido pelo solicitante for muito pequeno para conter uma linha enviada pelo servidor, então uma linha de dados parcial será retornada. Com dados textuais, isso pode ser detectado testando se o último byte retornado é `\n` ou não. (Em um binário `COPY`, será necessário fazer uma análise real do formato de dados `COPY` para fazer a determinação equivalente.) A string retornada não é terminada com um null. (Se você deseja adicionar um null de término, certifique-se de passar um *`bufsize`* menor que o espaço disponível.)

`PQputline` [#](#LIBPQ-PQPUTLINE) :   Envia uma cadeia de caracteres terminada por nulo para o servidor. Retorna 0 se OK e `EOF` se não conseguir enviar a cadeia de caracteres.

```
int PQputline(PGconn *conn, const char *string);
```

O fluxo de dados `COPY` enviado por uma série de chamadas para `PQputline`(libpq-copy.md#LIBPQ-PQPUTLINE) tem o mesmo formato que o retornado por `PQgetlineAsync`(libpq-copy.md#LIBPQ-PQGETLINEASYNC), exceto que as aplicações não são obrigadas a enviar exatamente uma linha de dados por chamada; é permitido enviar uma linha parcial ou várias linhas por chamada.

### Nota

Antes do protocolo PostgreSQL 3.0, era necessário que o aplicativo enviasse explicitamente os dois caracteres `\.` como uma linha final para indicar ao servidor que ele havia terminado de enviar os dados `COPY`. Embora isso ainda funcione, ele é desaconselhável e o significado especial de `\.` pode ser esperado para ser removido em um lançamento futuro. (Ele já vai se comportar mal no modo `CSV`.) É suficiente chamar `PQendcopy`(libpq-copy.md#LIBPQ-PQENDCOPY) após ter enviado os dados reais.

`PQputnbytes` [#](#LIBPQ-PQPUTNBYTES) : Envia uma string sem nulos para o servidor. Retorna 0 se OK e `EOF` se não conseguir enviar a string.

```
int PQputnbytes(PGconn *conn, const char *buffer, int nbytes);
```

Isso é exatamente como `PQputline`(libpq-copy.md#LIBPQ-PQPUTLINE), exceto que o buffer de dados não precisa ser terminado com nulo, pois o número de bytes a serem enviados é especificado diretamente. Use este procedimento ao enviar dados binários.

`PQendcopy` [#](#LIBPQ-PQENDCOPY) :  Sincroniza com o servidor.

```
int PQendcopy(PGconn *conn);
```

Essa função aguarda até que o servidor tenha terminado a cópia. Deve ser emitida quando a última string tiver sido enviada ao servidor usando `PQputline`(libpq-copy.md#LIBPQ-PQPUTLINE) ou quando a última string tiver sido recebida do servidor usando `PQgetline`. Deve ser emitida ou o servidor ficará "fora de sincronia" com o cliente. Após o retorno dessa função, o servidor está pronto para receber o próximo comando SQL. O valor de retorno é 0 em caso de conclusão bem-sucedida, diferente de zero caso contrário. (Use `PQerrorMessage`(libpq-status.md#LIBPQ-PQERRORMESSAGE) para obter detalhes se o valor de retorno for diferente de zero.)

Ao usar `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT), o aplicativo deve responder a um resultado de `PGRES_COPY_OUT` executando [`PQgetline`](libpq-copy.md#LIBPQ-PQGETLINE) repetidamente, seguido por [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY) após a linha terminadora ser vista. Em seguida, deve retornar ao loop de `PQgetResult`(libpq-async.md#LIBPQ-PQGETRESULT) até que [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT) retorne um ponteiro nulo. Da mesma forma, um resultado de `PGRES_COPY_IN` é processado por uma série de [`PQputline`](libpq-copy.md#LIBPQ-PQPUTLINE) chamadas seguidas por [`PQendcopy`](libpq-copy.md#LIBPQ-PQENDCOPY), então retorne ao loop de [`PQgetResult`](libpq-async.md#LIBPQ-PQGETRESULT). Esta disposição garantirá que um comando de `COPY` incorporado em uma série de comandos SQL será executado corretamente.

Aplicativos mais antigos provavelmente enviarão um `COPY` via `PQexec`(libpq-exec.md#LIBPQ-PQEXEC) e assumirão que a transação foi realizada após `PQendcopy`(libpq-copy.md#LIBPQ-PQENDCOPY). Isso funcionará corretamente apenas se o `COPY` for o único comando SQL na string de comando.