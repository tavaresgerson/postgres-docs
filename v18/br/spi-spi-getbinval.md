## SPI_getbinval

SPI_getbinval — retornar o valor binário da coluna especificada

## Sinopse

```
Datum SPI_getbinval(HeapTuple row, TupleDesc rowdesc, int colnumber,
                    bool * isnull)
```

## Descrição

`SPI_getbinval` retorna o valor da coluna especificada na forma interna (como tipo `Datum`).

Essa função não aloca um novo espaço para o dado. No caso de um tipo de dados de passagem por referência, o valor de retorno será um ponteiro para a linha passada.

## Argumentos

`HeapTuple row`: linha de entrada a ser examinada

`TupleDesc rowdesc`: descrição da linha de entrada

`int colnumber`: número da coluna (o contagem começa no número 1)

`bool * isnull`: bandeira para um valor nu na coluna

## Valor de retorno

O valor binário da coluna é retornado. A variável apontada por *`isnull`* é definida como verdadeira se a coluna for nula, caso contrário, como falsa.

`SPI_result` está definido para `SPI_ERROR_NOATTRIBUTE` em erro.