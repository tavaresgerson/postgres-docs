## SPI_getargcount

SPI_getargcount — retornar o número de argumentos necessários por uma declaração preparada por `SPI_prepare`

## Sinopse

```
int SPI_getargcount(SPIPlanPtr plan)
```

## Descrição

`SPI_getargcount` retorna o número de argumentos necessários para executar uma declaração preparada por `SPI_prepare`.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

## Valor de retorno

O número de argumentos esperados para o *`plan`*. Se o *`plan`* for `NULL` ou inválido, o *`SPI_result` é definido como *`SPI_ERROR_ARGUMENT` e -1 é retornado.