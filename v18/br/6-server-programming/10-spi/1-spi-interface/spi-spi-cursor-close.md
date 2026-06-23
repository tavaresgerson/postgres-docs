## SPI_cursor_close

SPI_cursor_close — fechar um cursor

## Sinopse

```
void SPI_cursor_close(Portal portal)
```

## Descrição

`SPI_cursor_close` fecha um cursor criado anteriormente e libera seu armazenamento de portal.

Todos os cursos abertos são fechados automaticamente no final de uma transação. `SPI_cursor_close` só precisa ser invocado se for desejável liberar recursos mais cedo.

## Argumentos

`Portal portal`: portal contendo o cursor