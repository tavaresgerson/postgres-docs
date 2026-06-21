## SPI_execute_extended

SPI_execute_extended — execute um comando com parâmetros fora da linha

## Sinopse

```
int SPI_execute_extended(const char *command,
                         const SPIExecuteOptions * options)
```

## Descrição

`SPI_execute_extended` executa um comando que pode incluir referências a parâmetros fornecidos externamente. O texto do comando refere-se a um parâmetro como `$n`, e o objeto *`options->params`* (se fornecido) fornece informações de valores e tipo para cada símbolo desse tipo. Várias opções de execução podem ser especificadas na estrutura *`options`*, também.

O objeto *`options->params`* deve normalmente marcar cada parâmetro com a bandeira `PARAM_FLAG_CONST`, uma vez que um plano único é sempre utilizado para a consulta.

Se *`options->dest`* não for NULL, então tuplas de resultado são passadas para esse objeto conforme elas são geradas pelo executor, em vez de serem acumuladas em `SPI_tuptable`. Usar um objeto `DestReceiver` fornecido pelo chamador é particularmente útil para consultas que podem gerar muitas tuplas, pois os dados podem ser processados em tempo real, em vez de serem acumulados na memória.

## Argumentos

`const char * command`: string de comando

`const SPIExecuteOptions * options`: estrutura contendo argumentos opcionais

Os chamados devem sempre zerar toda a estrutura *`options`*, depois preencher os campos que desejam definir. Isso garante a compatibilidade futura do código, pois quaisquer campos que sejam adicionados à estrutura no futuro serão definidos para se comportar de forma compatível com versões anteriores se forem zerados. Os campos atualmente disponíveis de *`options`* são:

`ParamListInfo params`: estrutura de dados contendo tipos e valores de parâmetros de consulta; NULL se nenhum

`bool read_only`: `true` para execução somente de leitura

`bool allow_nonatomic`: `true` permite a execução não-atômica das instruções CALL e DO (mas este campo é ignorado a menos que a bandeira `SPI_OPT_NONATOMIC` tenha sido passada para `SPI_connect_ext`)

`bool must_return_tuples`: se `true`, levante um erro se a consulta não for do tipo que retorna tuplas (isto não impede o caso em que ela retorne zero tuplas)

`uint64 tcount`: número máximo de linhas a serem devolvidas, ou `0` para sem limite

`DestReceiver * dest`: `DestReceiver` objeto que receberá quaisquer tuplas emitidas pela consulta; se NULL, os tuplos de resultado são acumulados em uma estrutura `SPI_tuptable`, como em `SPI_execute`

`ResourceOwner owner`: Este campo está presente para a consistência com `SPI_execute_plan_extended`, mas é ignorado, uma vez que o plano usado por `SPI_execute_extended` nunca é salvo.

## Valor de retorno

O valor de retorno é o mesmo que para `SPI_execute`.

Quando *`options->dest`* é NULL, `SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute`. Quando *`options->dest`* não é NULL, `SPI_processed` é definido como zero e `SPI_tuptable` é definido como NULL. Se for necessário um contador de tuplas, o objeto `DestReceiver` do chamador deve calculá-lo.