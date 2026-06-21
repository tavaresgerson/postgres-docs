## SPI_getargtypeid

SPI_getargtypeid — retornar o tipo de dado OID para um argumento de uma declaração preparada por `SPI_prepare`

## Sinopse

```
Oid SPI_getargtypeid(SPIPlanPtr plan, int argIndex)
```

## Descrição

`SPI_getargtypeid` retorna o OID que representa o tipo para o *`argIndex`*'º argumento de uma declaração preparada por `SPI_prepare`. O primeiro argumento está no índice zero.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

`int argIndex`: índice baseado em zero do argumento

## Valor de retorno

O tipo OID do argumento no índice especificado. Se o *`plan`* for *`NULL`* ou inválido, ou *`argIndex`* for menor que 0 ou não menor que o número de argumentos declarados para o *`plan`*, `SPI_result` é definido como *`SPI_ERROR_ARGUMENT`* e `InvalidOid` é retornado.