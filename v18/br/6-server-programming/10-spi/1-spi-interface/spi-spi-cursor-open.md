## SPI_cursor_open

SPI_cursor_open — configurar um cursor usando uma declaração criada com `SPI_prepare`

## Sinopse

```
Portal SPI_cursor_open(const char * name, SPIPlanPtr plan,
                       Datum * values, const char * nulls,
                       bool read_only)
```

## Descrição

`SPI_cursor_open` configura um cursor (internamente, um portal) que executará uma declaração preparada por `SPI_prepare`. Os parâmetros têm os mesmos significados que os parâmetros correspondentes a `SPI_execute_plan`.

Usar um cursor em vez de executar a declaração diretamente tem dois benefícios. Primeiro, as linhas de resultado podem ser recuperadas algumas de cada vez, evitando a sobrecarga de memória para consultas que retornam muitas linhas. Segundo, um portal pode sobreviver ao atual C função (de fato, pode até chegar ao fim da transação atual). Retornar o nome do portal para o chamado da função C fornece uma maneira de retornar um conjunto de linhas como resultado.

Os dados dos parâmetros passados serão copiados no portal do cursor, para que possam ser liberados enquanto o cursor ainda existe.

## Argumentos

`const char * name`: nome para o portal, ou `NULL` para permitir que o sistema selecione um nome

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`Datum * values`: Uma matriz de valores de parâmetros reais. Deve ter o mesmo comprimento que o número de argumentos da declaração.

`const char * nulls`: Uma matriz que descreve quais parâmetros são nulos. Deve ter o mesmo comprimento que o número de argumentos da declaração.

Se *`nulls`* for `NULL` então `SPI_cursor_open` assume que nenhum parâmetro é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor do parâmetro correspondente for não nulo, ou `'n'` se o valor do parâmetro correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

`bool read_only`: `true` para execução apenas de leitura

## Valor de retorno

Indicador para o portal que contém o cursor. Observe que não há convenção de retorno de erro; qualquer erro será relatado via `elog`.