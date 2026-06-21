## SPI_cursor_move

SPI_cursor_move — mover um cursor

## Sinopse

```
void SPI_cursor_move(Portal portal, bool forward, long count)
```

## Descrição

`SPI_cursor_move` pula alguns números de linhas em um cursor. Isso é equivalente a um subconjunto do comando SQL `MOVE` (consulte `SPI_scroll_cursor_move` para mais funcionalidades).

## Argumentos

`Portal portal`: portal contendo o cursor

`bool forward`: verdadeiro para avançar, falso para recuar

`long count`: número máximo de linhas a serem movidas

## Notas

A movimentação para trás pode falhar se o plano do cursor não foi criado com a opção `CURSOR_OPT_SCROLL`.