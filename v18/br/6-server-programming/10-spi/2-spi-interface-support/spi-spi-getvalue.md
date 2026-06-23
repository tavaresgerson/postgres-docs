## SPI_getvalue

SPI_getvalue — retornar o valor de string da coluna especificada

## Sinopse

```
char * SPI_getvalue(HeapTuple row, TupleDesc rowdesc, int colnumber)
```

## Descrição

`SPI_getvalue` retorna a representação em cadeia do valor da coluna especificada.

O resultado é retornado na memória alocada usando `palloc`. (Você pode usar `pfree` para liberar a memória quando você não precisa mais dela.)

## Argumentos

`HeapTuple row`: linha de entrada a ser examinada

`TupleDesc rowdesc`: descrição da linha de entrada

`int colnumber`: número da coluna (o contagem começa no número 1)

## Valor de retorno

O valor da coluna, ou `NULL` se a coluna estiver em branco, *`colnumber`* está fora do intervalo (`SPI_result` está definido como `SPI_ERROR_NOATTRIBUTE`), ou não há função de saída disponível (`SPI_result` está definido como `SPI_ERROR_NOOUTFUNC`).