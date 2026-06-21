## SPI_execute_with_args

SPI_execute_with_args — execute um comando com parâmetros fora da linha

## Sinopse

```
int SPI_execute_with_args(const char *command,
                          int nargs, Oid *argtypes,
                          Datum *values, const char *nulls,
                          bool read_only, long count)
```

## Descrição

`SPI_execute_with_args` executa um comando que pode incluir referências a parâmetros fornecidos externamente. O texto do comando refere-se a um parâmetro como `$n`, e a chamada especifica os tipos de dados e valores para cada símbolo desse tipo. *`read_only`* e *`count`* têm a mesma interpretação que em `SPI_execute`.

A principal vantagem dessa rotina em comparação com `SPI_execute` é que os valores dos dados podem ser inseridos no comando sem a necessidade de citação/escapariedade tediosa, e, assim, com muito menos risco de ataques de injeção SQL.

Resultados semelhantes podem ser alcançados com `SPI_prepare` seguido de `SPI_execute_plan`; no entanto, ao usar essa função, o plano da consulta é sempre personalizado para os valores específicos dos parâmetros fornecidos. Para execução de consulta única, essa função deve ser preferida. Se o mesmo comando deve ser executado com muitos parâmetros diferentes, qualquer um dos métodos pode ser mais rápido, dependendo do custo de replanejamento versus o benefício dos planos personalizados.

## Argumentos

`const char * command`: string de comando

`int nargs`: número de parâmetros de entrada (`$1`, `$2`, etc.)

`Oid * argtypes`: um array de comprimento *`nargs`*, contendo os OIDs dos tipos de dados dos parâmetros

`Datum * values`: um array de comprimento *`nargs`*, contendo os valores reais dos parâmetros

`const char * nulls`: um array de comprimento *`nargs`*, descrevendo quais parâmetros são nulos

Se *`nulls`* for `NULL`, então `SPI_execute_with_args` assume que nenhum parâmetro é nulo. Caso contrário, cada entrada do *`nulls`* deve ser `' '` se o valor do parâmetro correspondente for não nulo, ou `'n'` se o valor do parâmetro correspondente for nulo. (Neste último caso, o valor real na entrada correspondente de *`values`* não importa.) Note que *`nulls`* não é uma string de texto, apenas um array: ele não precisa de um `'\0'` terminator.

`bool read_only`: `true` para execução somente de leitura

`long count`: número máximo de linhas a serem retornadas, ou `0` para sem limite

## Valor de retorno

O valor de retorno é o mesmo que para `SPI_execute`.

`SPI_processed` e `SPI_tuptable` são definidos como em `SPI_execute` se o sucesso for alcançado.