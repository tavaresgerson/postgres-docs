## 32.21. Comportamento em programas em emaranhados [#](#LIBPQ-THREADING)

A partir da versão 17, a libpq é sempre reentrante e segura para múltiplos threads. No entanto, uma restrição é que nenhuma das duas threads tenta manipular o mesmo objeto `PGconn` ao mesmo tempo. Em particular, você não pode emitir comandos concorrentes de diferentes threads através do mesmo objeto de conexão. (Se você precisar executar comandos concorrentes, use múltiplas conexões.)

Os objetos `PGresult` são normalmente de leitura somente após a criação, e podem ser passados livremente entre os threads. No entanto, se você usar alguma das funções de modificação `PGresult` descritas em [Seção 32.12](libpq-misc.md "32.12. Miscellaneous Functions") ou [Seção 32.14](libpq-events.md "32.14. Event System"), cabe a você evitar operações concorrentes no mesmo `PGresult`, também.

Em versões anteriores, o libpq podia ser compilado com ou sem suporte a múltiplos threads, dependendo das opções do compilador. Esta função permite a consulta do status seguro para múltiplos threads do libpq:

`PQisthreadsafe` [#](#LIBPQ-PQISTHREADSAFE): Retorna o status de segurança de thread da biblioteca libpq.

```
int PQisthreadsafe();
```

Retorna 1 se a libpq for segura em relação a múltiplos threads e 0 se não for. Sempre retorna 1 na versão 17 e superior.

As funções obsoletas `PQrequestCancel` e (libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) e `PQoidStatus` e (libpq-exec.md#LIBPQ-PQOIDSTATUS) não são seguras em relação a múltiplos threads e não devem ser usadas em programas multithread. `PQrequestCancel` e (libpq-cancel.md#LIBPQ-PQREQUESTCANCEL) podem ser substituídas por `PQcancelBlocking` e (libpq-cancel.md#LIBPQ-PQCANCELBLOCKING). `PQoidStatus` e (libpq-exec.md#LIBPQ-PQOIDSTATUS) podem ser substituídas por `PQoidValue` e (libpq-exec.md#LIBPQ-PQOIDVALUE).

Se você estiver usando Kerberos dentro de sua aplicação (bem como dentro da libpq), você precisará realizar o bloqueio em torno das chamadas do Kerberos, pois as funções do Kerberos não são seguras para múltiplos threads. Consulte a função `PQregisterThreadLock` no código-fonte da libpq para uma maneira de realizar o bloqueio cooperativo entre a libpq e sua aplicação.

Da mesma forma, se você estiver usando o Curl dentro da sua aplicação e ainda não [inicializar o libcurl globalmente](https://curl.se/libcurl/c/curl_global_init.html) antes de iniciar novos threads, você precisará bloquear de forma cooperativa (novamente via `PQregisterThreadLock`) em torno de qualquer código que possa inicializar o libcurl. Essa restrição é levantada para versões mais recentes do Curl que são construídas para suportar inicialização segura para threads; essas compilações podem ser identificadas pela publicidade de uma característica `threadsafe` em seus metadados de versão.