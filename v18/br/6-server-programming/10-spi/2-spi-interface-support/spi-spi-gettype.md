## SPI_gettype

SPI_gettype — retornar o nome do tipo de dados da coluna especificada

## Sinopse

```
char * SPI_gettype(TupleDesc rowdesc, int colnumber)
```

## Descrição

`SPI_gettype` retorna uma cópia do nome do tipo de dados da coluna especificada. (Você pode usar `pfree` para liberar a cópia do nome quando você não precisa mais dela.)

## Argumentos

`TupleDesc rowdesc`: descrição da linha de entrada

`int colnumber`: número da coluna (o contagem começa no número 1)

## Valor de retorno

O nome do tipo de dados da coluna especificada, ou `NULL` em caso de erro. `SPI_result` é definido como `SPI_ERROR_NOATTRIBUTE` em caso de erro.