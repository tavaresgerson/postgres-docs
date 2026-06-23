## SPI_prepare_extended

SPI_prepare_extended — preparar uma declaração, sem executá-la ainda

## Sinopse

```
SPIPlanPtr SPI_prepare_extended(const char * command,
                                const SPIPrepareOptions * options)
```

## Descrição

`SPI_prepare_extended` cria e retorna uma declaração preparada para o comando especificado, mas não executa o comando. Esta função é equivalente a `SPI_prepare`, com a adição de que o solicitante pode especificar opções para controlar a análise de referências de parâmetros externos, bem como outros aspectos da análise e planejamento de consultas.

## Argumentos

`const char * command`: string de comando

`const SPIPrepareOptions * options`: estrutura contendo argumentos opcionais

Os chamados devem sempre zerar toda a estrutura *`options`*, depois preencher os campos que desejam definir. Isso garante a compatibilidade futura do código, pois quaisquer campos que sejam adicionados à estrutura no futuro serão definidos para se comportar de forma compatível com versões anteriores se forem zerados. Os campos atualmente disponíveis de *`options`* são:

`ParserSetupHook parserSetup`: Função de configuração do gancho do parser

`void * parserSetupArg`: argumento de passagem para *`parserSetup`*

`RawParseMode parseMode`: modo para análise bruta; `RAW_PARSE_DEFAULT` (zero) produz comportamento padrão

`int cursorOptions`: máscara de bits inteiro das opções do cursor; zero produz o comportamento padrão

## Valor de retorno

`SPI_prepare_extended` tem as mesmas convenções de retorno que `SPI_prepare`.