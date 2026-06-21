## SPI_freeplan

SPI_freeplan — libere uma declaração preparada salva anteriormente

## Sinopse

```
int SPI_freeplan(SPIPlanPtr plan)
```

## Descrição

`SPI_freeplan` emite uma declaração preparada que foi previamente devolvida por `SPI_prepare` ou salva por `SPI_keepplan` ou `SPI_saveplan`.

## Argumentos

`SPIPlanPtr plan`: ponteiro para declaração de liberação

## Valor de retorno

0 para sucesso; `SPI_ERROR_ARGUMENT` se *`plan`* for `NULL` ou inválido