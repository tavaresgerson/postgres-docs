## SPI_execute_plan_with_paramlist

SPI_execute_plan_with_paramlist — execute uma declaração preparada por `SPI_prepare`

## Sinopse

```
int SPI_execute_plan_with_paramlist(SPIPlanPtr plan,
                                    ParamListInfo params,
                                    bool read_only,
                                    long count)
```

## Descrição

`SPI_execute_plan_with_paramlist` executa uma declaração preparada por `SPI_prepare`. Esta função é equivalente a `SPI_execute_plan`, exceto que as informações sobre os valores dos parâmetros a serem passados para a consulta são apresentadas de maneira diferente. A representação `ParamListInfo` pode ser conveniente para passar valores que já estão disponíveis nesse formato. Também suporta o uso de conjuntos de parâmetros dinâmicos através de funções de gancho especificadas em `ParamListInfo`.

Essa função já foi descontinuada em favor de `SPI_execute_plan_extended`.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`ParamListInfo params`: estrutura de dados contendo tipos e valores de parâmetros; NULL se nenhum

`bool read_only`: `true` para execução apenas de leitura

`long count`: número máximo de linhas a serem retornadas, ou `0` para sem limite

## Valor de retorno

O valor de retorno é o mesmo que para `SPI_execute_plan`.

`SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute_plan`, se for bem-sucedido.