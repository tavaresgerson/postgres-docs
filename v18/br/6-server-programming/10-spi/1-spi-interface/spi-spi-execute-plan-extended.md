## SPI_execute_plan_extended

SPI_execute_plan_extended — execute uma declaração preparada por `SPI_prepare`

## Sinopse

```
int SPI_execute_plan_extended(SPIPlanPtr plan,
                              const SPIExecuteOptions * options)
```

## Descrição

`SPI_execute_plan_extended` executa uma declaração preparada por `SPI_prepare` ou uma de suas irmãs. Esta função é equivalente a `SPI_execute_plan`, exceto que as informações sobre os valores dos parâmetros a serem passados para a consulta são apresentadas de maneira diferente, e opções adicionais de controle de execução podem ser passadas.

Os valores dos parâmetros de consulta são representados por uma estrutura `ParamListInfo`, o que é conveniente para passar valores que já estão disponíveis nesse formato. Conjuntos de parâmetros dinâmicos também podem ser usados, por meio de funções de gancho especificadas em `ParamListInfo`.

Além disso, em vez de sempre acumular os tuplos de resultado em uma estrutura `SPI_tuptable`, os tuplos podem ser passados para um objeto `DestReceiver` fornecido pelo chamador conforme eles são gerados pelo executor. Isso é particularmente útil para consultas que podem gerar muitos tuplos, uma vez que os dados podem ser processados em tempo real, em vez de serem acumulados na memória.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`const SPIExecuteOptions * options`: estrutura contendo argumentos opcionais

Os chamados devem sempre zerar toda a estrutura *`options`*, depois preencher os campos que desejam definir. Isso garante a compatibilidade futura do código, pois quaisquer campos que sejam adicionados à estrutura no futuro serão definidos para se comportar de forma compatível com versões anteriores se forem zerados. Os campos atualmente disponíveis de *`options`* são:

`ParamListInfo params`: estrutura de dados contendo tipos e valores de parâmetros de consulta; NULL se nenhum

`bool read_only`: `true` para execução somente de leitura

`bool allow_nonatomic`: `true` permite a execução não-atômica das instruções CALL e DO (mas este campo é ignorado a menos que a bandeira `SPI_OPT_NONATOMIC` tenha sido passada para `SPI_connect_ext`)

`bool must_return_tuples`: se `true`, levante um erro se a consulta não for do tipo que retorna tuplas (isto não impede o caso em que ela retorne zero tuplas)

`uint64 tcount`: número máximo de linhas a serem devolvidas, ou `0` para sem limite

`DestReceiver * dest`: `DestReceiver` objeto que receberá quaisquer tuplas emitidas pela consulta; se NULL, os tuplos de resultado são acumulados em uma estrutura `SPI_tuptable`, como em `SPI_execute_plan`

`ResourceOwner owner`: O proprietário do recurso que manterá um contador de referência no plano enquanto ele estiver sendo executado. Se NULL, o CurrentResourceOwner é usado. Ignorado para planos não salvos, pois o SPI não obtém contagem de referência nessas situações.

## Valor de retorno

O valor de retorno é o mesmo que para `SPI_execute_plan`.

Quando *`options->dest`* é NULL, `SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute_plan`. Quando *`options->dest`* não é NULL, `SPI_processed` é definido como zero e `SPI_tuptable` é definido como NULL. Se for necessário um contador de tuplas, o objeto `DestReceiver` do chamador deve calculá-lo.