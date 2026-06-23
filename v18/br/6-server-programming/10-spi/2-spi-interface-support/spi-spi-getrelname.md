## SPI_getrelname

SPI_getrelname — retornar o nome da relação especificada

## Sinopse

```
char * SPI_getrelname(Relation rel)
```

## Descrição

`SPI_getrelname` retorna uma cópia do nome da relação especificada. (Você pode usar `pfree` para liberar a cópia do nome quando você não precisa mais dela.)

## Argumentos

`Relation rel`: relação de entrada

## Valor de retorno

O nome da relação especificada.