## 43.7. Gatilhos de eventos PL/Perl [#](#PLPERL-EVENT-TRIGGERS)

O PL/Perl pode ser usado para escrever funções de gatilho de evento. Em uma função de gatilho de evento, a referência de hash `$_TD` contém informações sobre o evento de gatilho atual. `$_TD` é uma variável global, que recebe um valor local separado para cada invocação do gatilho. Os campos da referência de hash `$_TD` são:

`$_TD->{event}`: O nome do evento para o qual o gatilho é disparado.

`$_TD->{tag}`: O rótulo do comando para o qual o gatilho é disparado.

O valor de retorno da função de gatilho é ignorado.

Aqui está um exemplo de uma função de gatilho de evento, que ilustra alguns dos pontos acima:

```
CREATE OR REPLACE FUNCTION perlsnitch() RETURNS event_trigger AS $$
  elog(NOTICE, "perlsnitch: " . $_TD->{event} . " " . $_TD->{tag} . " ");
$$ LANGUAGE plperl;

CREATE EVENT TRIGGER perl_a_snitch
    ON ddl_command_start
    EXECUTE FUNCTION perlsnitch();
```
