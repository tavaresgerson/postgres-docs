## SPI_fnumber

SPI_fnumber — determinar o número da coluna para o nome de coluna especificado

## Sinopse

```
int SPI_fnumber(TupleDesc rowdesc, const char * colname)
```

## Descrição

`SPI_fnumber` retorna o número da coluna para a coluna com o nome especificado.

Se *`colname`* se referir a uma coluna de sistema (por exemplo, `ctid`), o número de coluna negativa apropriado será retornado. O chamador deve ter cuidado para testar o valor de retorno para igualdade exata a `SPI_ERROR_NOATTRIBUTE` para detectar um erro; testar o resultado para menos ou igual a 0 não é correto, a menos que as colunas do sistema devam ser rejeitadas.

## Argumentos

`TupleDesc rowdesc`: descrição da linha de entrada

`const char * colname`: nome da coluna

## Valor de retorno

Número da coluna (o contagem começa em 1 para colunas definidas pelo usuário), ou `SPI_ERROR_NOATTRIBUTE` se a coluna nomeada não foi encontrada.