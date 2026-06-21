## SPI_freetuptable

SPI_freetuptable — liberar um conjunto de linhas criado por `SPI_execute` ou uma função semelhante

## Sinopse

```
void SPI_freetuptable(SPITupleTable * tuptable)
```

## Descrição

`SPI_freetuptable` libera um conjunto de linhas criado por uma função anterior de execução de comandos SPI, como `SPI_execute`. Portanto, essa função é frequentemente chamada com a variável global `SPI_tuptable` como argumento.

Essa função é útil se uma função em C que utiliza SPI precisar executar vários comandos e não queira manter os resultados dos comandos anteriores até o término. Note que quaisquer conjuntos de linhas não liberados serão liberados de qualquer forma em `SPI_finish`. Além disso, se uma subtransação for iniciada e então interrompida durante a execução de uma função em C que utiliza SPI, o SPI libera automaticamente quaisquer conjuntos de linhas criados enquanto a subtransação estava em execução.

A partir do PostgreSQL 9.3, `SPI_freetuptable` contém lógica de proteção para evitar solicitações de exclusão duplicada para o mesmo conjunto de linhas. Em versões anteriores, as exclusões duplicadas causavam falhas.

## Argumentos

`SPITupleTable * tuptable`: ponteiro para o conjunto de linhas definido como livre, ou NULL para não fazer nada