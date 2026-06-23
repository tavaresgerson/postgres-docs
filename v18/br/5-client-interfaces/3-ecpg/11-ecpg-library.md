## 34.11. Funções de biblioteca [#](#ECPG-LIBRARY)

A biblioteca `libecpg` contém principalmente funções “ocultas” que são usadas para implementar a funcionalidade expressa pelos comandos SQL embutidos. Mas há algumas funções que podem ser úteis para serem chamadas diretamente. Note que isso torna seu código não portável.

* `ECPGdebug(int on, FILE *stream)` ativa o registro de depuração se chamado com o primeiro argumento não nulo. O registro de depuração é feito em *`stream`*. O log contém todas as instruções SQL com todas as variáveis de entrada inseridas e os resultados do servidor PostgreSQL. Isso pode ser muito útil ao procurar erros em suas instruções SQL.

Nota

Em Windows, se as bibliotecas ecpg e um aplicativo forem compilados com diferentes flags, essa chamada de função causará o crash do aplicativo porque a representação interna dos ponteiros `FILE` difere. Especificamente, as flags multithread/single-threaded, release/debug e static/dynamic devem ser as mesmas para a biblioteca e todos os aplicativos que utilizam essa biblioteca.
* `ECPGget_PGconn(const char *connection_name)` retorna o handle de conexão do banco de dados da biblioteca identificado pelo nome fornecido. Se *`connection_name`* estiver definido como `NULL`, o handle de conexão atual é retornado. Se não puder ser identificado nenhum handle de conexão, a função retorna `NULL`. O handle de conexão retornado pode ser usado para chamar quaisquer outras funções da libpq, se necessário.

Nota

É uma má ideia manipular as conexões de banco de dados feitas diretamente com ecpg usando rotinas da libpq.
* `ECPGtransactionStatus(const char *connection_name)` retorna o status atual da transação da conexão identificada por *`connection_name`*. Veja [Seção 32.2](libpq-status.md "32.2. Connection Status Functions") e [`PQtransactionStatus`](libpq-status.md#LIBPQ-PQTRANSACTIONSTATUS) da libpq para detalhes sobre os códigos de status retornados.
* `ECPGstatus(int lineno, const char* connection_name)` retorna verdadeiro se você estiver conectado a um banco de dados e falso se não estiver. *`connection_name`* pode ser `NULL` se uma única conexão estiver sendo usada.