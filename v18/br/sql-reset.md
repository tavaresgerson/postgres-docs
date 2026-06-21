## RESET

RESET — restaurar o valor de um parâmetro de execução ao valor padrão

## Sinopse

```
RESET configuration_parameter
RESET ALL
```

## Descrição

`RESET` restaura os parâmetros de execução aos seus valores padrão. `RESET` é uma grafia alternativa para

```
SET configuration_parameter TO DEFAULT
```

Consulte [SET](sql-set.md "SET") para obter detalhes.

O valor padrão é definido como o valor que o parâmetro teria tido, se nunca tivesse sido emitido um `SET` para ele na sessão atual. A fonte real desse valor pode ser um valor padrão incorporado, o arquivo de configuração, opções de linha de comando ou configurações padrão por banco de dados ou por usuário. Isso é sutilmente diferente de defini-lo como “o valor que o parâmetro tinha no início da sessão”, porque, se o valor vier do arquivo de configuração, ele será redefinido para o que for especificado pelo arquivo de configuração agora. Veja [Capítulo 19](runtime-config.md) para detalhes.

O comportamento transacional de `RESET` é o mesmo que o de `SET`: seus efeitos serão anulados pelo rollback de transação.

## Parâmetros

*`configuration_parameter`*: Nome de um parâmetro de execução configurável. Os parâmetros disponíveis estão documentados no [Capítulo 19](runtime-config.md) e na página de referência [SET](sql-set.md).

`ALL`: Redefine todos os parâmetros configuráveis do tempo de execução aos valores padrão.

## Exemplos

Defina a variável de configuração `timezone` para seu valor padrão:

```
RESET timezone;
```

## Compatibilidade

`RESET` é uma extensão do PostgreSQL.

## Veja também

[SET](sql-set.md "SET"), [SHOW](sql-show.md "SHOW")