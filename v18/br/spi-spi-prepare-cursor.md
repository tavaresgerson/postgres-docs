## SPI_prepare_cursor

SPI_prepare_cursor — preparar uma declaração, sem executá-la ainda

## Sinopse

```
SPIPlanPtr SPI_prepare_cursor(const char * command, int nargs,
                              Oid * argtypes, int cursorOptions)
```

## Descrição

`SPI_prepare_cursor` é idêntico a `SPI_prepare`, exceto que também permite a especificação do parâmetro de "opções do cursor" do planejador. Esta é uma máscara de bits com os valores mostrados em `nodes/parsenodes.h` para o campo `options` de `DeclareCursorStmt`. `SPI_prepare` sempre assume as opções do cursor como zero.

Essa função já foi descontinuada em favor de `SPI_prepare_extended`.

## Argumentos

`const char * command`: string de comando

`int nargs`: número de parâmetros de entrada (`$1`, `$2`, etc.)

`Oid * argtypes`: ponteiro para um array contendo os OIDs dos tipos de dados dos parâmetros

`int cursorOptions`: máscara de bits inteiro das opções do cursor; zero produz o comportamento padrão

## Valor de retorno

`SPI_prepare_cursor` tem as mesmas convenções de retorno que `SPI_prepare`.

## Notas

Os campos úteis para definir em *`cursorOptions`* incluem `CURSOR_OPT_SCROLL`, `CURSOR_OPT_NO_SCROLL`, `CURSOR_OPT_FAST_PLAN`, `CURSOR_OPT_GENERIC_PLAN` e `CURSOR_OPT_CUSTOM_PLAN`. Note, em particular, que `CURSOR_OPT_HOLD` é ignorado.