## SET

SET — alterar um parâmetro de execução

## Sinopse

```
SET [ SESSION | LOCAL ] configuration_parameter { TO | = } { value | 'value' | DEFAULT }
SET [ SESSION | LOCAL ] TIME ZONE { value | 'value' | LOCAL | DEFAULT }
```

## Descrição

Os parâmetros de configuração de tempo de execução são alterados pelo comando `SET`. Muitos dos parâmetros de tempo de execução listados em [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") podem ser alterados em tempo real com `SET`. (Alguns parâmetros só podem ser alterados por superusuários e usuários que tenham sido concedidos o privilégio `SET` nesse parâmetro. Há também parâmetros que não podem ser alterados após o início do servidor ou da sessão.) `SET` afeta apenas o valor usado pela sessão atual.

Se o `SET` (ou, equivalentemente, o `SET SESSION`) for emitido dentro de uma transação que é posteriormente abortado, os efeitos do comando `SET` desaparecerão quando a transação for revertida. Uma vez que a transação circunvizinha seja confirmada, os efeitos persistirão até o final da sessão, a menos que seja sobrescrito por outro `SET`.

Os efeitos do `SET LOCAL` duram apenas até o final da transação atual, seja ela comprometida ou não. Um caso especial é o `SET` seguido pelo `SET LOCAL` dentro de uma única transação: o valor do `SET LOCAL` será visto até o final da transação, mas depois (se a transação for comprometida) o valor do `SET` entrará em vigor.

Os efeitos de `SET` ou `SET LOCAL` também são cancelados ao retornar a um ponto de salvamento anterior ao comando.

Se `SET LOCAL` for usado dentro de uma função que tem uma opção [[PH_LNK_24]] para a mesma variável (ver [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION")), os efeitos do comando `SET LOCAL` desaparecem ao sair da função; ou seja, o valor em vigor quando a função foi chamada é restaurado de qualquer forma. Isso permite que `SET LOCAL` seja usado para mudanças dinâmicas ou repetidas de um parâmetro dentro de uma função, mantendo a conveniência de usar a opção `SET` para salvar e restaurar o valor do chamador. No entanto, um comando regular `SET` substitui qualquer opção `SET` de função circundante; seus efeitos persistirão a menos que sejam revertidos.

Nota

Nas versões do PostgreSQL de 8.0 a 8.2, os efeitos de um `SET LOCAL` seriam cancelados ao liberar um ponto de salvamento anterior ou ao sair com sucesso de um bloco de exceção PL/pgSQL. Esse comportamento foi alterado porque foi considerado pouco intuitivo.

## Parâmetros

`SESSION`: Especifica que o comando tem efeito para a sessão atual. (Isso é o padrão se nem `SESSION` nem `LOCAL` aparecerem.)

`LOCAL`: Especifica que o comando tem efeito apenas para a transação atual. Após `COMMIT` ou `ROLLBACK`, o ajuste do nível de sessão volta a ter efeito. Emitir isso fora de um bloco de transação emite um aviso e, de outra forma, não tem efeito.

*`configuration_parameter`*: Nome de um parâmetro de execução configurável. Os parâmetros disponíveis estão documentados no [Capítulo 19](runtime-config.md) e abaixo.

*`value`*: Novo valor do parâmetro. Os valores podem ser especificados como constantes de string, identificadores, números ou listas separadas por vírgula desses, conforme apropriado para o parâmetro específico. `DEFAULT` pode ser escrito para especificar o restabelecimento do parâmetro ao seu valor padrão (ou seja, qualquer valor que teria se não tivesse sido executado `SET` na sessão atual).

Além dos parâmetros de configuração documentados em [Capítulo 19](runtime-config.md), há alguns que só podem ser ajustados usando o comando `SET` ou que têm uma sintaxe especial:

`SCHEMA`: `SET SCHEMA 'value'` é um alias para `SET search_path TO value`. Apenas um esquema pode ser especificado usando essa sintaxe.

`NAMES`: `SET NAMES 'value'` é um alias para `SET client_encoding TO value`.

`SEED`: Define a semente interna para o gerador de números aleatórios (a função `random`). Os valores permitidos são números em ponto flutuante entre -1 e 1, inclusive.

A semente também pode ser definida ao invocar a função `setseed`:

```
SELECT setseed(value);
```

`TIME ZONE`: `SET TIME ZONE 'value'` é um alias para `SET timezone TO 'value'`. A sintaxe `SET TIME ZONE` permite uma sintaxe especial para a especificação do fuso horário. Aqui estão exemplos de valores válidos:

`'America/Los_Angeles'` :   O fuso horário para Berkeley, Califórnia.

`'Europe/Rome'` :   O fuso horário para a Itália.

`-7` :   O fuso horário 7 horas a oeste do UTC (equivalente ao PDT). Valores positivos são a leste do UTC.

`INTERVAL '-08:00' HOUR TO MINUTE` :   O fuso horário 8 horas a oeste do UTC (equivalente a PST).

`LOCAL` `DEFAULT` :   Defina o fuso horário para o seu fuso horário local (ou seja, o valor padrão do servidor de `timezone`).

As configurações de fuso horário fornecidas como números ou intervalos são traduzidas internamente para a sintaxe de fuso horário POSIX. Por exemplo, após `SET TIME ZONE -7`, `SHOW TIME ZONE` reportaria `<-07>+07`.

As abreviações dos fusos horários não são suportadas por `SET`; consulte [Seção 8.5.3](datatype-datetime.md#DATATYPE-TIMEZONES "8.5.3. Time Zones") para mais informações sobre fusos horários.

## Notas

A função `set_config` oferece funcionalidades equivalentes; veja [Seção 9.28.1](functions-admin.md#FUNCTIONS-ADMIN-SET "9.28.1. Configuration Settings Functions"). Além disso, é possível ATUALIZAR a visão do sistema [`pg_settings`](view-pg-settings.md) para realizar o equivalente a `SET`.

## Exemplos

Defina o caminho de pesquisa do esquema:

```
SET search_path TO my_schema, public;
```

Defina o estilo de data para POSTGRES tradicional com a convenção de entrada “dia antes do mês”:

```
SET datestyle TO postgres, dmy;
```

Defina o fuso horário para Berkeley, Califórnia:

```
SET TIME ZONE 'America/Los_Angeles';
```

Defina o fuso horário para a Itália:

```
SET TIME ZONE 'Europe/Rome';
```

## Compatibilidade

`SET TIME ZONE` estende a sintaxe definida no padrão SQL. O padrão permite apenas deslocamentos numéricos de fuso horário, enquanto o PostgreSQL permite especificações de fuso horário mais flexíveis. Todas as outras características `SET` são extensões do PostgreSQL.

## Veja também

[RESET](sql-reset.md "RESET"), [SHOW](sql-show.md "SHOW")