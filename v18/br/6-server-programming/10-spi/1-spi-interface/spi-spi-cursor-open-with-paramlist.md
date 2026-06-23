## SPI_cursor_open_with_paramlist

SPI_cursor_open_with_paramlist — configurar um cursor usando parâmetros

## Sinopse

```
Portal SPI_cursor_open_with_paramlist(const char *name,
                                      SPIPlanPtr plan,
                                      ParamListInfo params,
                                      bool read_only)
```

## Descrição

`SPI_cursor_open_with_paramlist` configura um cursor (internamente, um portal) que executará uma declaração preparada por `SPI_prepare`. Esta função é equivalente a `SPI_cursor_open`, exceto que as informações sobre os valores dos parâmetros a serem passados para a consulta são apresentadas de maneira diferente. A representação `ParamListInfo` pode ser conveniente para passar valores que já estão disponíveis nesse formato. Também suporta o uso de conjuntos de parâmetros dinâmicos através de funções de gancho especificadas em `ParamListInfo`.

Os dados dos parâmetros passados serão copiados no portal do cursor, para que possam ser liberados enquanto o cursor ainda existe.

## Argumentos

`const char * name`: nome para o portal, ou `NULL` para permitir que o sistema selecione um nome

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`ParamListInfo params`: estrutura de dados contendo tipos e valores de parâmetros; NULL se nenhum

`bool read_only`: `true` para execução apenas de leitura

## Valor de retorno

Indicador para o portal que contém o cursor. Observe que não há convenção de retorno de erro; qualquer erro será relatado via `elog`.