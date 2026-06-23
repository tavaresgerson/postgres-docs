## SPI_pfree

SPI_pfree — memória livre no contexto superior do executor

## Sinopse

```
void SPI_pfree(void * pointer)
```

## Descrição

`SPI_pfree` libera memória previamente alocada usando `SPI_palloc` ou `SPI_repalloc`.

Essa função não é mais diferente do simples `pfree`. Ela é mantida apenas para compatibilidade reversa de código existente.

## Argumentos

`void * pointer`: ponteiro para armazenamento existente para liberar