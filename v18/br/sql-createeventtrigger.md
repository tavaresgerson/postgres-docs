## Crie um gatilho de evento

Crie um gatilho de evento — defina um novo gatilho de evento

## Sinopse

```
CREATE EVENT TRIGGER name
    ON event
    [ WHEN filter_variable IN (filter_value [, ... ]) [ AND ... ] ]
    EXECUTE { FUNCTION | PROCEDURE } function_name()
```

## Descrição

`CREATE EVENT TRIGGER` cria um novo gatilho de evento. Sempre que o evento designado ocorrer e a condição `WHEN` associada ao gatilho, se houver, for satisfeita, a função do gatilho será executada. Para uma introdução geral sobre gatilhos de evento, consulte o [Capítulo 38][(event-triggers.md "Chapter 38. Event Triggers")]. O usuário que cria um gatilho de evento se torna seu proprietário.

## Parâmetros

*`name`*: O nome que se deseja dar ao novo gatilho. Esse nome deve ser único dentro do banco de dados.

*`event`*: O nome do evento que aciona a chamada à função especificada. Consulte a [Seção 38.1][(event-trigger-definition.md "38.1. Overview of Event Trigger Behavior")] para obter mais informações sobre os nomes dos eventos.

*`filter_variable`*: O nome de uma variável usada para filtrar eventos. Isso permite restringir o disparo do gatilho a um subconjunto dos casos em que ele é suportado. Atualmente, o único *`filter_variable`* suportado é `TAG`.

*`filter_value`*: Uma lista de valores para o *`filter_variable`* associado para o qual o gatilho deve ser acionado. Para `TAG`, isso significa uma lista de tags de comando (por exemplo, `'DROP FUNCTION'`).

*`function_name`*: Uma função fornecida pelo usuário que é declarada sem argumentos e retorna o tipo `event_trigger`.

Na sintaxe do `CREATE EVENT TRIGGER`, as palavras-chave `FUNCTION` e `PROCEDURE` são equivalentes, mas a função referenciada deve, em qualquer caso, ser uma função, não um procedimento. O uso da palavra-chave `PROCEDURE` aqui é histórico e desaconselhado.

## Notas

Apenas superusuários podem criar gatilhos de evento.

Os gatilhos de evento são desativados no modo de usuário único (consulte [postgres][(app-postgres.md "postgres")]) e também quando [event_triggers][(runtime-config-client.md#GUC-EVENT-TRIGGERS)] está definido como `false`. Se um gatilho de evento errôneo desabilitar o banco de dados tanto que você não consegue até mesmo descartar o gatilho, reinicie com [event_triggers][(runtime-config-client.md#GUC-EVENT-TRIGGERS)] definido como `false` para desabilitar temporariamente os gatilhos de evento, ou no modo de usuário único, e você poderá fazer isso.

## Exemplos

Proíba a execução de qualquer comando [DDL][(ddl.md "Chapter 5. Data Definition")]

```
CREATE OR REPLACE FUNCTION abort_any_command()
  RETURNS event_trigger
 LANGUAGE plpgsql
  AS $$
BEGIN
  RAISE EXCEPTION 'command % is disabled', tg_tag;
END;
$$;

CREATE EVENT TRIGGER abort_ddl ON ddl_command_start
   EXECUTE FUNCTION abort_any_command();
```

## Compatibilidade

Não há nenhuma declaração `CREATE EVENT TRIGGER` no padrão SQL.

## Veja também

[ALTERAR TRIGGER DE EVENTO](sql-altereventtrigger.md "ALTER EVENT TRIGGER"), [DROP TRIGGER DE EVENTO](sql-dropeventtrigger.md "DROP EVENT TRIGGER"), [CADAQUE FUNÇÃO](sql-createfunction.md "CREATE FUNCTION")