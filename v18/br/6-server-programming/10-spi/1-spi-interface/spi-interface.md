## 45.1. Funções de Interface [#](#SPI-INTERFACE)

* [SPI_connect](spi-spi-connect.md) — conectar uma função C ao gerenciador SPI
* [SPI_finish](spi-spi-finish.md) — desconectar uma função C do gerenciador SPI
* [SPI_execute](spi-spi-execute.md) — executar um comando
* [SPI_exec](spi-spi-exec.md) — executar um comando de leitura/escrita
* [SPI_execute_extended](spi-spi-execute-extended.md) — executar um comando com parâmetros fora da linha
* [SPI_execute_with_args](spi-spi-execute-with-args.md) — executar um comando com parâmetros fora da linha
* [SPI_prepare](spi-spi-prepare.md) — preparar uma declaração, sem executá-la ainda
* [SPI_prepare_cursor](spi-spi-prepare-cursor.md) — preparar uma declaração, sem executá-la ainda
* [SPI_prepare_extended](spi-spi-prepare-extended.md) — preparar uma declaração, sem executá-la ainda
* [SPI_prepare_params](spi-spi-prepare-params.md) — preparar uma declaração, sem executá-la ainda
* [SPI_getargcount](spi-spi-getargcount.md) — retornar o número de argumentos necessários por uma declaração preparada por `SPI_prepare`
* [SPI_getargtypeid](spi-spi-getargtypeid.md) — retornar o OID do tipo de dados para um argumento de uma declaração preparada por `SPI_prepare`
* [SPI_is_cursor_plan](spi-spi-is-cursor-plan.md) — retornar `true` se uma declaração preparada por `SPI_prepare` pode ser usada com `SPI_cursor_open`
* [SPI_execute_plan](spi-spi-execute-plan.md) — executar uma declaração preparada por `SPI_prepare`
* [SPI_execute_plan_extended](spi-spi-execute-plan-extended.md) — executar uma declaração preparada por `SPI_prepare`
* [SPI_execute_plan_with_paramlist](spi-spi-execute-plan-with-paramlist.md) — executar uma declaração preparada por `SPI_prepare`
* [SPI_execp](spi-spi-execp.md) — executar uma declaração em modo de leitura/escrita
* [SPI_cursor_open](spi-spi-cursor-open.md) — configurar um cursor usando uma declaração criada com `SPI_prepare`
* [SPI_cursor_open_with_args](spi-spi-cursor-open-with-args.md) — configurar um cursor usando uma consulta e parâmetros
* [SPI_cursor_open_with_paramlist](spi-spi-cursor-open-with-paramlist.md) — configurar um cursor usando parâmetros
* [SPI_cursor_parse_open](spi-spi-cursor-parse-open.md) — configurar um cursor usando uma string de consulta e parâmetros
* [SPI_cursor_find](spi-spi-cursor-find.md) — encontrar um cursor existente pelo nome
* [SPI_cursor_fetch](spi-spi-cursor-fetch.md) — obter algumas linhas de um cursor
* [SPI_cursor_move](spi-spi-cursor-move.md) — mover um cursor
* [SPI_scroll_cursor_fetch](spi-spi-scroll-cursor-fetch.md) — obter algumas linhas de um cursor
* [SPI_scroll_cursor_move](spi-spi-scroll-cursor-move.md) — mover um cursor
* [SPI_cursor_close](spi-spi-cursor-close.md) — fechar um cursor
* [SPI_keepplan](spi-spi-keepplan.md) — salvar uma declaração preparada
* [SPI_saveplan](spi-spi-saveplan.md) — salvar uma declaração preparada
* [SPI_register_relation](spi-spi-register-relation.md) — tornar uma relação nomeada efêmera disponível pelo nome em consultas SPI
* [SPI_unregister_relation](spi-spi-unregister-relation.md) — remover uma relação nomeada efêmera do registro
* [SPI_register_trigger_data](spi-spi-register-trigger-data.md) — tornar dados de gatilho efêmeros disponíveis em consultas SPI