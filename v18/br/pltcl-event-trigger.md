## 42.7. Funções de Desempenho de Eventos em PL/Tcl [#](#PLTCL-EVENT-TRIGGER)

As funções de disparo de eventos podem ser escritas em PL/Tcl. O PostgreSQL exige que uma função que deve ser chamada como um disparador de eventos seja declarada como uma função sem argumentos e com um tipo de retorno de `event_trigger`.

As informações do gerenciador de gatilho são passadas para o corpo da função nas seguintes variáveis:

`$TG_event`: O nome do evento para o qual o gatilho é disparado.

`$TG_tag`: O rótulo do comando para o qual o gatilho é disparado.

O valor de retorno da função de gatilho é ignorado.

Aqui está um pequeno exemplo de função de gatilho de evento que simplesmente emite uma mensagem `NOTICE` toda vez que um comando compatível é executado:

```
CREATE OR REPLACE FUNCTION tclsnitch() RETURNS event_trigger AS $$
  elog NOTICE "tclsnitch: $TG_event $TG_tag"
$$ LANGUAGE pltcl;

CREATE EVENT TRIGGER tcl_a_snitch ON ddl_command_start EXECUTE FUNCTION tclsnitch();
```
