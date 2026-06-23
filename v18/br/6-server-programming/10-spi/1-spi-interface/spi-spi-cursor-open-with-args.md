## SPI_cursor_open_with_args

SPI_cursor_open_with_args — configurar um cursor usando uma consulta e parâmetros

## Sinopse

```
Portal SPI_cursor_open_with_args(const char *name,
                                 const char *command,
                                 int nargs, Oid *argtypes,
                                 Datum *values, const char *nulls,
                                 bool read_only, int cursorOptions)
```

## Descrição

`SPI_cursor_open_with_args` configura um cursor (internamente, um portal) que executará a consulta especificada. A maioria dos parâmetros tem os mesmos significados que os parâmetros correspondentes a `SPI_prepare_cursor` e `SPI_cursor_open`.

Para a execução de uma consulta única, essa função deve ser preferida em relação a `SPI_prepare_cursor` seguida de `SPI_cursor_open`. Se o mesmo comando deve ser executado com muitos parâmetros diferentes, qualquer um dos métodos pode ser mais rápido, dependendo do custo de replanejamento em relação ao benefício dos planos personalizados.

Os dados dos parâmetros passados serão copiados no portal do cursor, para que possam ser liberados enquanto o cursor ainda existe.

Essa função já foi descontinuada em favor de `SPI_cursor_parse_open`, que oferece funcionalidades equivalentes usando uma API mais moderna para o tratamento de parâmetros de consulta.

## Argumentos

`const char * name`: nome para o portal, ou `NULL` para permitir que o sistema selecione um nome

`const char * command`: string de comando

`int nargs`: número de parâmetros de entrada (`$1`, `$2`, etc.)

`Oid * argtypes`: um array de comprimento *`nargs`*, contendo os OIDs dos tipos de dados dos parâmetros

`Datum * values`: um array de comprimento *`nargs`*, contendo os valores reais dos parâmetros

`const char * nulls`: um array de comprimento *`nargs`*, descrevendo quais parâmetros são nulos

Se *`nulls`* for `NULL`, então `SPI_cursor_open_with_args` assume que nenhum parâmetro é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor do parâmetro correspondente for não nulo, ou `'n'` se o valor do parâmetro correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

`bool read_only`: `true` para execução somente de leitura

`int cursorOptions`: máscara de bits inteiro das opções do cursor; zero produz o comportamento padrão

## Valor de retorno

Indicador para o portal que contém o cursor. Observe que não há convenção de retorno de erro; qualquer erro será relatado via `elog`.