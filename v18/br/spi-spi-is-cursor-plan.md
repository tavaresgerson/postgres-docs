## SPI_is_cursor_plan

SPI_is_cursor_plan — retornar `true` se uma declaração preparada por `SPI_prepare` pode ser usada com `SPI_cursor_open`

## Sinopse

```
bool SPI_is_cursor_plan(SPIPlanPtr plan)
```

## Descrição

`SPI_is_cursor_plan` retorna `true` se uma declaração preparada por `SPI_prepare` pode ser passada como argumento para `SPI_cursor_open`, ou `false` se esse não for o caso. Os critérios são que o *`plan`* representa um único comando e que esse comando retorna tuplas para o chamador; por exemplo, `SELECT` é permitido, a menos que contenha uma cláusula `INTO`, e `UPDATE` é permitido apenas se contiver uma cláusula `RETURNING`.

## Argumentos

`SPIPlanPtr plan`: declaração preparada (retornada por `SPI_prepare`)

## Valor de retorno

`true` ou `false` para indicar se o *`plan`* pode ou não produzir um cursor, com `SPI_result` definido como zero. Se não for possível determinar a resposta (por exemplo, se o *`plan`* é `NULL` ou inválido, ou se é chamado quando não está conectado ao SPI), então `SPI_result` é definido com um código de erro adequado e `false` é retornado.