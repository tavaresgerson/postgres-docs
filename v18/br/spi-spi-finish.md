## SPI_finish

SPI_finish — desconectar uma função C do gerenciador SPI

## Sinopse

```
int SPI_finish(void)
```

## Descrição

`SPI_finish` fecha uma conexão existente com o gerenciador SPI. Você deve chamar essa função após completar as operações SPI necessárias durante a invocação atual da sua função C. No entanto, você não precisa se preocupar em fazer isso, se você abortar a transação via `elog(ERROR)`. Nesse caso, o SPI se limpará automaticamente.

## Valor de retorno

`SPI_OK_FINISH`: se desconectada corretamente

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada