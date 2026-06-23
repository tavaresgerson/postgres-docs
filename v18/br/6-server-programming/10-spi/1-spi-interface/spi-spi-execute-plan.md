## SPI_execute_plan

SPI_execute_plan — execute uma declaração preparada por `SPI_prepare`

## Sinopse

```
int SPI_execute_plan(SPIPlanPtr plan, Datum * values, const char * nulls,
                     bool read_only, long count)
```

## Descrição

`SPI_execute_plan` executa uma declaração preparada por `SPI_prepare` ou uma de suas irmãs. *`read_only`* e *`count`* têm a mesma interpretação que em `SPI_execute`.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`Datum * values`: Uma matriz de valores de parâmetros reais. Deve ter o mesmo comprimento que o número de argumentos da declaração.

`const char * nulls`: Uma matriz que descreve quais parâmetros são nulos. Deve ter o mesmo comprimento que o número de argumentos da declaração.

Se *`nulls`* for `NULL` então `SPI_execute_plan` assume que nenhum parâmetro é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor do parâmetro correspondente for não nulo, ou `'n'` se o valor do parâmetro correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

`bool read_only`: `true` para execução apenas de leitura

`long count`: número máximo de linhas a serem retornadas, ou `0` para sem limite

## Valor de retorno

O valor de retorno é o mesmo que para `SPI_execute`, com os seguintes resultados adicionais possíveis de erro (negativo):

`SPI_ERROR_ARGUMENT`: se *`plan`* é `NULL` ou inválido, ou *`count`* é menor que 0

`SPI_ERROR_PARAM`: se *`values`* é `NULL` e *`plan`* foi preparado com alguns parâmetros

`SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute` se o sucesso for alcançado.