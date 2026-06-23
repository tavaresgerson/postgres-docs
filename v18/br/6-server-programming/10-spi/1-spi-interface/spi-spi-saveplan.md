## SPI_saveplan

SPI_saveplan — salvar uma declaração preparada

## Sinopse

```
SPIPlanPtr SPI_saveplan(SPIPlanPtr plan)
```

## Descrição

`SPI_saveplan` copia uma declaração passada (preparada por `SPI_prepare`) na memória que não será liberada por `SPI_finish` nem pelo gerenciador de transação, e retorna um ponteiro para a declaração copiada. Isso lhe dá a capacidade de reutilizar declarações preparadas nas subsequentes invocações da sua função C na sessão atual.

## Argumentos

`SPIPlanPtr plan`: a declaração preparada a ser salva

## Valor de retorno

Indicador para a declaração copiada; ou `NULL` se não for bem-sucedido. Em caso de erro, `SPI_result` é definido da seguinte forma:

`SPI_ERROR_ARGUMENT`: se *`plan`* for `NULL` ou inválido

`SPI_ERROR_UNCONNECTED`: se chamado a partir de uma função C não conectada

## Notas

A declaração originalmente passada não é liberada, então você pode querer fazer `SPI_freeplan` sobre ela para evitar vazamento de memória até `SPI_finish`.

Na maioria dos casos, `SPI_keepplan` é preferido a essa função, pois ela realiza em grande parte o mesmo resultado sem precisar copiar fisicamente as estruturas de dados da declaração preparada.