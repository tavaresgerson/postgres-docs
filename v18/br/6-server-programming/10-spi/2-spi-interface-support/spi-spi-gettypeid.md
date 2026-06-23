## SPI_gettypeid

SPI_gettypeid — retornar o OID do tipo de dados especificado da coluna especificada

## Sinopse

```
Oid SPI_gettypeid(TupleDesc rowdesc, int colnumber)
```

## Descrição

`SPI_gettypeid` retorna o OID do tipo de dados da coluna especificada.

## Argumentos

`TupleDesc rowdesc`: descrição da linha de entrada

`int colnumber`: número da coluna (o contagem começa no número 1)

## Valor de retorno

O OID do tipo de dados da coluna especificada ou `InvalidOid` gerou um erro. Em caso de erro, `SPI_result` é definido como `SPI_ERROR_NOATTRIBUTE`.