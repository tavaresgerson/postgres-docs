## SPI_cursor_parse_open

SPI_cursor_parse_open — configurar um cursor usando uma string de consulta e parâmetros

## Sinopse

```
Portal SPI_cursor_parse_open(const char *name,
                             const char *command,
                             const SPIParseOpenOptions * options)
```

## Descrição

`SPI_cursor_parse_open` configura um cursor (internamente, um portal) que executará a string de consulta especificada. Isso é comparável a `SPI_prepare_cursor` seguido por `SPI_cursor_open_with_paramlist`, exceto que as referências de parâmetro dentro da string de consulta são tratadas inteiramente fornecendo um objeto `ParamListInfo`.

Para a execução de uma consulta única, essa função deve ser preferida em relação a `SPI_prepare_cursor` seguida de `SPI_cursor_open_with_paramlist`. Se o mesmo comando deve ser executado com muitos parâmetros diferentes, qualquer um dos métodos pode ser mais rápido, dependendo do custo de replanejamento em relação ao benefício dos planos personalizados.

O objeto *`options->params`* deve normalmente marcar cada parâmetro com a bandeira `PARAM_FLAG_CONST`, uma vez que um plano único é sempre utilizado para a consulta.

Os dados dos parâmetros passados serão copiados no portal do cursor, para que possam ser liberados enquanto o cursor ainda existe.

## Argumentos

`const char * name`: nome para o portal, ou `NULL` para permitir que o sistema selecione um nome

`const char * command`: string de comando

`const SPIParseOpenOptions * options`: estrutura contendo argumentos opcionais

Os chamados devem sempre zerar toda a estrutura *`options`*, depois preencher os campos que desejam definir. Isso garante a compatibilidade futura do código, pois quaisquer campos que sejam adicionados à estrutura no futuro serão definidos para se comportar de forma compatível com versões anteriores se forem zerados. Os campos atualmente disponíveis de *`options`* são:

`ParamListInfo params`: estrutura de dados contendo tipos e valores de parâmetros de consulta; NULL se nenhum

`int cursorOptions`: máscara de bits inteiro das opções do cursor; zero produz o comportamento padrão

`bool read_only`: `true` para execução apenas de leitura

## Valor de retorno

Indicador para o portal que contém o cursor. Observe que não há convenção de retorno de erro; qualquer erro será relatado via `elog`.