## SPI_prepare_params

SPI_prepare_params — preparar uma declaração, sem executá-la ainda

## Sinopse

```
SPIPlanPtr SPI_prepare_params(const char * command,
                              ParserSetupHook parserSetup,
                              void * parserSetupArg,
                              int cursorOptions)
```

## Descrição

`SPI_prepare_params` cria e retorna uma declaração preparada para o comando especificado, mas não executa o comando. Esta função é equivalente a `SPI_prepare_cursor`, com a adição de que o chamador pode especificar funções de gancho do analisador para controlar a análise de referências de parâmetros externos.

Essa função já foi descontinuada em favor de `SPI_prepare_extended`.

## Argumentos

`const char * command`: string de comando

`ParserSetupHook parserSetup`: Função de configuração do gancho do analisador

`void * parserSetupArg`: argumento de passagem para *`parserSetup`*

`int cursorOptions`: máscara de bits inteiro das opções do cursor; zero produz o comportamento padrão

## Valor de retorno

`SPI_prepare_params` tem as mesmas convenções de retorno que `SPI_prepare`.