## ALTER SYSTEM

ALTER SYSTEM — alterar um parâmetro de configuração do servidor

## Sinopse

```
ALTER SYSTEM SET configuration_parameter { TO | = } { value [, ...] | DEFAULT }

ALTER SYSTEM RESET configuration_parameter
ALTER SYSTEM RESET ALL
```

## Descrição

`ALTER SYSTEM` é usado para alterar os parâmetros de configuração do servidor em todo o clúster de bancos de dados. Pode ser mais conveniente do que o método tradicional de edição manual do arquivo `postgresql.conf`. `ALTER SYSTEM` escreve a configuração do parâmetro dado no arquivo `postgresql.auto.conf`, que é lido além de `postgresql.conf`. Definir um parâmetro para `DEFAULT`, ou usar a variante `RESET`, remove essa entrada de configuração do arquivo `postgresql.auto.conf`. Use `RESET ALL` para remover todas essas entradas de configuração.

Os valores definidos com `ALTER SYSTEM` serão eficazes após a próxima recarga da configuração do servidor, ou após o próximo reinício do servidor, no caso de parâmetros que só podem ser alterados no início do servidor. Uma recarga da configuração do servidor pode ser comandada chamando a função SQL `pg_reload_conf()`, executando `pg_ctl reload` ou enviando um sinal SIGHUP ao processo principal do servidor.

Apenas superusuários e usuários que tenham sido concedidos o privilégio `ALTER SYSTEM` em um parâmetro podem alterá-lo usando `ALTER SYSTEM`. Além disso, uma vez que este comando atua diretamente no sistema de arquivos e não pode ser desfeito, não é permitido dentro de um bloco de transação ou função.

## Parâmetros

*`configuration_parameter`*: Nome de um parâmetro de configuração configurável. Os parâmetros disponíveis estão documentados em [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")].

*`value`*: Novo valor do parâmetro. Os valores podem ser especificados como constantes de string, identificadores, números ou listas de vírgulas desses, conforme apropriado para o parâmetro específico. Os valores que não são números ou identificadores válidos devem ser citados. `DEFAULT` pode ser escrito para especificar a remoção do parâmetro e seu valor de `postgresql.auto.conf`.

Para alguns parâmetros que aceitam listas, os valores citados produzirão saída com aspas duplas para preservar espaços em branco e vírgulas; para outros, as aspas devem ser usadas dentro de strings com aspas simples para obter esse efeito.

## Notas

Este comando não pode ser usado para definir [data_directory][(runtime-config-file-locations.md#GUC-DATA-DIRECTORY)], [allow_alter_system][(runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM)] ou parâmetros que não são permitidos em `postgresql.conf` (por exemplo, [opções pré-definidas][(runtime-config-preset.md "19.15. Preset Options")]).

Veja [Seção 19.1][(config-setting.md "19.1. Setting Parameters")] para outras maneiras de definir os parâmetros.

`ALTER SYSTEM` pode ser desativado definindo [allow_alter_system](runtime-config-compatible.md#GUC-ALLOW-ALTER-SYSTEM) como `off`, mas este não é um mecanismo de segurança (como explicado em detalhes na documentação deste parâmetro).

## Exemplos

Defina o `wal_level`:

```
ALTER SYSTEM SET wal_level = replica;
```

Desfaça isso, restaurando qualquer configuração que fosse eficaz em `postgresql.conf`:

```
ALTER SYSTEM RESET wal_level;
```

## Compatibilidade

A declaração `ALTER SYSTEM` é uma extensão do PostgreSQL.

## Veja também

[SET](sql-set.md "SET"), [SHOW](sql-show.md "SHOW")