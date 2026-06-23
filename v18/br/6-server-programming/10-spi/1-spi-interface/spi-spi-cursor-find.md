## SPI_cursor_find

SPI_cursor_find — encontrar um cursor existente pelo nome

## Sinopse

```
Portal SPI_cursor_find(const char * name)
```

## Descrição

`SPI_cursor_find` encontra um portal existente pelo nome. Isso é principalmente útil para resolver o nome do cursor retornado como texto por outra função.

## Argumentos

`const char * name`: nome do portal

## Valor de retorno

ponteiro para o portal com o nome especificado, ou `NULL` se nenhum foi encontrado

## Notas

Cuidado, pois essa função pode retornar um objeto `Portal` que não possui propriedades semelhantes a cursor; por exemplo, ela pode não retornar tuplas. Se você simplesmente passar o ponteiro `Portal` para outras funções SPI, elas podem se defender contra tais casos, mas é apropriado ter cautela ao inspecionar diretamente o `Portal`.