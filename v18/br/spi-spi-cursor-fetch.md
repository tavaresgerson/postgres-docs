## SPI_cursor_fetch

SPI_cursor_fetch — obter algumas linhas de um cursor

## Sinopse

```
void SPI_cursor_fetch(Portal portal, bool forward, long count)
```

## Descrição

`SPI_cursor_fetch` recupera algumas linhas de um cursor. Isso é equivalente a um subconjunto do comando SQL `FETCH` (consulte `SPI_scroll_cursor_fetch` para mais funcionalidades).

## Argumentos

`Portal portal`: portal contendo o cursor

`bool forward`: verdadeiro para pegar para frente, falso para pegar para trás

`long count`: número máximo de linhas a serem recuperadas

## Valor de retorno

`SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute`, se for bem-sucedido.

## Notas

A recuperação para trás pode falhar se o plano do cursor não foi criado com a opção `CURSOR_OPT_SCROLL`.