## SPI_keepplan

SPI_keepplan — salvar uma declaração preparada

## Sinopse

```
int SPI_keepplan(SPIPlanPtr plan)
```

## Descrição

`SPI_keepplan` salva uma declaração passada (preparada por `SPI_prepare`) para que ela não seja liberada por `SPI_finish` nem pelo gerenciador de transação. Isso lhe dá a capacidade de reutilizar declarações preparadas nas invocações subsequentes da sua função C na sessão atual.

## Argumentos

`SPIPlanPtr plan`: a declaração preparada a ser salva

## Valor de retorno

0 para sucesso; `SPI_ERROR_ARGUMENT` se *`plan`* for `NULL` ou inválido

## Notas

A declaração passada é realocada para armazenamento permanente por meio de ajuste de ponteiro (não é necessário copiar dados). Se você quiser excluí-la mais tarde, use `SPI_freeplan` sobre ela.