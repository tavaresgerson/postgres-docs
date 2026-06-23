## SPI_getnspname

SPI_getnspname — retornar o namespace da relação especificada

## Sinopse

```
char * SPI_getnspname(Relation rel)
```

## Descrição

`SPI_getnspname` retorna uma cópia do nome do namespace ao qual o `Relation` especificado pertence. Isso é equivalente ao esquema da relação. Você deve `pfree` o valor de retorno desta função quando estiver terminado com ela.

## Argumentos

`Relation rel`: relação de entrada

## Valor de retorno

O nome do espaço de nomes da relação especificada.