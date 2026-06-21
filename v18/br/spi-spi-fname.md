## SPI_fname

SPI_fname — determine o nome da coluna para o número de coluna especificado

## Sinopse

```
char * SPI_fname(TupleDesc rowdesc, int colnumber)
```

## Descrição

`SPI_fname` retorna uma cópia do nome da coluna da coluna especificada. (Você pode usar `pfree` para liberar a cópia do nome quando você não precisa mais.)

## Argumentos

`TupleDesc rowdesc`: descrição da linha de entrada

`int colnumber`: número da coluna (o contagem começa no número 1)

## Valor de retorno

O nome da coluna; `NULL` se *`colnumber`* estiver fora do intervalo. `SPI_result` definido como `SPI_ERROR_NOATTRIBUTE` em caso de erro.