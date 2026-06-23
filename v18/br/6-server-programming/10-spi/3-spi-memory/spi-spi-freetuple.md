## SPI_freetuple

SPI_freetuple — liberar uma linha alocada no contexto do executor superior

## Sinopse

```
void SPI_freetuple(HeapTuple row)
```

## Descrição

`SPI_freetuple` libera uma linha previamente alocada no contexto superior do executor.

Essa função não é mais diferente do simples `heap_freetuple`. Ela é mantida apenas para compatibilidade reversa de código existente.

## Argumentos

`HeapTuple row`: linha para livre