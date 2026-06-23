## SPI_scroll_cursor_move

SPI_scroll_cursor_move — mover um cursor

## Sinopse

```
void SPI_scroll_cursor_move(Portal portal, FetchDirection direction,
                            long count)
```

## Descrição

`SPI_scroll_cursor_move` pula alguns números de linhas em um cursor. Isso é equivalente ao comando SQL `MOVE`.

## Argumentos

`Portal portal`: portal contendo o cursor

`FetchDirection direction`: uma das `FETCH_FORWARD`, `FETCH_BACKWARD`, `FETCH_ABSOLUTE` ou `FETCH_RELATIVE`

`long count`: número de linhas a serem movidas para `FETCH_FORWARD` ou `FETCH_BACKWARD`; número absoluto de linha a ser movida para `FETCH_ABSOLUTE`; ou número relativo de linha a ser movida para `FETCH_RELATIVE`

## Valor de retorno

`SPI_processed` é definido como em `SPI_execute` se for bem-sucedido. `SPI_tuptable` é definido como `NULL`, uma vez que não são retornadas linhas por esta função.

## Notas

Consulte o comando SQL [FETCH](sql-fetch.md "FETCH") para obter detalhes sobre a interpretação dos parâmetros *`direction`* e *`count`*.

Os valores de direção que não são `FETCH_FORWARD` podem falhar se o plano do cursor não foi criado com a opção `CURSOR_OPT_SCROLL`.