## SPI_scroll_cursor_fetch

SPI_scroll_cursor_fetch — obter algumas linhas de um cursor

## Sinopse

```
void SPI_scroll_cursor_fetch(Portal portal, FetchDirection direction,
                             long count)
```

## Descrição

`SPI_scroll_cursor_fetch` recupera algumas linhas de um cursor. Isso é equivalente ao comando SQL `FETCH`.

## Argumentos

`Portal portal`: portal contendo o cursor

`FetchDirection direction`: uma das `FETCH_FORWARD`, `FETCH_BACKWARD`, `FETCH_ABSOLUTE` ou `FETCH_RELATIVE`

`long count`: número de linhas a serem recuperadas para `FETCH_FORWARD` ou `FETCH_BACKWARD`; número absoluto de linhas a serem recuperadas para `FETCH_ABSOLUTE`; ou número relativo de linhas a serem recuperadas para `FETCH_RELATIVE`

## Valor de retorno

`SPI_processed` e `SPI_tuptable` são definidos como no `SPI_execute`, se for bem-sucedido.

## Notas

Consulte o comando SQL [FETCH](sql-fetch.md "FETCH") para obter detalhes sobre a interpretação dos parâmetros *`direction`* e *`count`*.

Os valores de direção que não são `FETCH_FORWARD` podem falhar se o plano do cursor não foi criado com a opção `CURSOR_OPT_SCROLL`.