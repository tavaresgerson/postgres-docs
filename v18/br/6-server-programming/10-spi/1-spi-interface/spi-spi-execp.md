## SPI_execp

SPI_execp — executar uma declaração em modo de leitura/escrita

## Sinopse

```
int SPI_execp(SPIPlanPtr plan, Datum * values, const char * nulls, long count)
```

## Descrição

`SPI_execp` é o mesmo que `SPI_execute_plan`, sendo que o parâmetro *`read_only`* do último é sempre considerado `false`.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`Datum * values`: Uma matriz de valores de parâmetros reais. Deve ter o mesmo comprimento que o número de argumentos da declaração.

`const char * nulls`: Uma matriz que descreve quais parâmetros são nulos. Deve ter o mesmo comprimento que o número de argumentos da declaração.

Se *`nulls`* for `NULL` então `SPI_execp` assume que nenhum parâmetro é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor do parâmetro correspondente for não nulo, ou `'n'` se o valor do parâmetro correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

`long count`: número máximo de linhas a serem devolvidas, ou `0` para sem limite

## Valor de retorno

Veja `SPI_execute_plan`.

`SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute` se for bem-sucedido.