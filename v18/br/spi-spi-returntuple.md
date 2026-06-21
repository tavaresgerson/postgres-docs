## SPI_returntuple

SPI_returntuple — prepare-se para retornar um tuplo como um Datum

## Sinopse

```
HeapTupleHeader SPI_returntuple(HeapTuple row, TupleDesc rowdesc)
```

## Descrição

`SPI_returntuple` faz uma cópia de uma linha no contexto superior do executor, devolvendo-a na forma de um tipo de linha `Datum`. O ponteiro retornado só precisa ser convertido para `Datum` via `PointerGetDatum` antes de ser devolvido.

Essa função só pode ser usada quando conectado ao SPI. Caso contrário, ela retorna NULL e define `SPI_result` para `SPI_ERROR_UNCONNECTED`.

Observe que isso deve ser usado para funções que são declaradas para retornar tipos compostos. Não é usado para gatilhos; use `SPI_copytuple` para retornar uma linha modificada em um gatilho.

## Argumentos

`HeapTuple row`: linha a ser copiada

`TupleDesc rowdesc`: descripto para linha (passe o mesmo descripto toda vez para o armazenamento de cache mais eficaz)

## Valor de retorno

`HeapTupleHeader` apontando para linha copiada, ou `NULL` em caso de erro (consulte `SPI_result` para indicação de erro)