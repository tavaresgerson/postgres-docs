## SPI_copytuple

SPI_copytuple — fazer uma cópia de uma linha no contexto do executor superior

## Sinopse

```
HeapTuple SPI_copytuple(HeapTuple row)
```

## Descrição

`SPI_copytuple` faz uma cópia de uma linha no contexto superior do executor. Isso normalmente é usado para retornar uma linha modificada de um gatilho. Em uma função declarada para retornar um tipo composto, use `SPI_returntuple` em vez disso.

Essa função só pode ser usada quando conectado ao SPI. Caso contrário, ela retorna NULL e define `SPI_result` para `SPI_ERROR_UNCONNECTED`.

## Argumentos

`HeapTuple row`: linha a ser copiada

## Valor de retorno

a linha copiada, ou `NULL` em caso de erro (consulte `SPI_result` para indicação de erro)