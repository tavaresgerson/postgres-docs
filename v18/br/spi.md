## Capítulo 45. Interface de Programação do Servidor

**Índice**

* [45.1. Funções de Interface](spi-interface.md)

+ [SPI_connect](spi-spi-connect.md) — conectar uma função C ao gerenciador SPI
+ [SPI_finish](spi-spi-finish.md) — desconectar uma função C do gerenciador SPI
+ [SPI_execute](spi-spi-execute.md) — executar um comando
+ [SPI_exec](spi-spi-exec.md) — executar um comando de leitura/escrita
+ [SPI_execute_extended](spi-spi-execute-extended.md) — executar um comando com parâmetros fora da linha
+ [SPI_execute_with_args](spi-spi-execute-with-args.md) — executar um comando com parâmetros fora da linha
+ [SPI_prepare](spi-spi-prepare.md) — preparar uma declaração, sem executá-la ainda
+ [SPI_prepare_cursor](spi-spi-prepare-cursor.md) — preparar uma declaração, sem executá-la ainda
+ [SPI_prepare_extended](spi-spi-prepare-extended.md) — preparar uma declaração, sem executá-la ainda
+ [SPI_prepare_params](spi-spi-prepare-params.md) — preparar uma declaração, sem executá-la ainda
+ [SPI_getargcount](spi-spi-getargcount.md) — retornar o número de argumentos necessários por uma declaração preparada por `SPI_prepare`
+ [SPI_getargtypeid](spi-spi-getargtypeid.md) — retornar o OID do tipo de dados para um argumento de uma declaração preparada por `SPI_prepare`
+ [SPI_is_cursor_plan](spi-spi-is-cursor-plan.md) — retornar `true` se uma declaração preparada por `SPI_prepare` pode ser usada com `SPI_cursor_open`
+ [SPI_execute_plan](spi-spi-execute-plan.md) — executar uma declaração preparada por `SPI_prepare`
+ [SPI_execute_plan_extended](spi-spi-execute-plan-extended.md) — executar uma declaração preparada por `SPI_prepare`
+ [SPI_execute_plan_with_paramlist](spi-spi-execute-plan-with-paramlist.md) — executar uma declaração preparada por `SPI_prepare`
+ [SPI_execp](spi-spi-execp.md) — executar uma declaração em modo de leitura/escrita
+ [SPI_cursor_open](spi-spi-cursor-open.md) — configurar um cursor usando uma declaração criada com `SPI_prepare`
+ [SPI_cursor_open_with_args](spi-spi-cursor-open-with-args.md) — configurar um cursor usando uma consulta e parâmetros
+ [SPI_cursor_open_with_paramlist](spi-spi-cursor-open-with-paramlist.md) — configurar um cursor usando parâmetros
+ [SPI_cursor_parse_open](spi-spi-cursor-parse-open.md) — configurar um cursor usando uma string de consulta e parâmetros
+ [SPI_cursor_find](spi-spi-cursor-find.md) — encontrar um cursor existente pelo nome
+ [SPI_cursor_fetch](spi-spi-cursor-fetch.md) — obter algumas linhas de um cursor
+ [SPI_cursor_move](spi-spi-cursor-move.md) — mover um cursor
+ [SPI_scroll_cursor_fetch](spi-spi-scroll-cursor-fetch.md) — obter algumas linhas de um cursor
+ [SPI_scroll_cursor_move](spi-spi-scroll-cursor-move.md) — mover um cursor
+ [SPI_cursor_close](spi-spi-cursor-close.md) — fechar um cursor

* [45.2. Funções de Suporte de Interface](spi-interface-support.md)

+ [SPI_fname](spi-spi-fname.md) — determinar o nome da coluna para o número de coluna especificado
+ [SPI_fnumber](spi-spi-fnumber.md) — determinar o número de coluna para o nome de coluna especificado
+ [SPI_getvalue](spi-spi-getvalue.md) — retornar o valor de string da coluna especificada
+ [SPI_getbinval](spi-spi-getbinval.md) — retornar o valor binário da coluna especificada
+ [SPI_gettype](spi-spi-gettype.md) — retornar o nome do tipo de dados da coluna especificada
+ [SPI_gettypeid](spi-spi-gettypeid.md) — retornar o OID do tipo de dados da coluna especificada
+ [SPI_getrelname](spi-spi-getrelname.md) — retornar o nome da relação especificada
+ [SPI_getnspname](spi-spi-getnspname.md) — retornar o namespace da relação especificada
+ [SPI_result_code_string](spi-spi-result-code-string.md) — retornar o código de erro como string

* [45.3. Gerenciamento de memória](spi-memory.md)

+ [SPI_palloc](spi-spi-palloc.md) — alocar memória no contexto do executor superior
+ [SPI_repalloc](spi-realloc.md) — realocar memória no contexto do executor superior
+ [SPI_pfree](spi-spi-pfree.md) — liberar memória no contexto do executor superior
+ [SPI_copytuple](spi-spi-copytuple.md) — fazer uma cópia de uma linha no contexto do executor superior
+ [SPI_returntuple](spi-spi-returntuple.md) — preparar para retornar uma tupla como um Datum
+ [SPI_modifytuple](spi-spi-modifytuple.md) — criar uma linha substituindo os campos selecionados de uma linha dada
+ [SPI_freetuple](spi-spi-freetuple.md) — liberar uma linha alocada no contexto do executor superior
+ [SPI_freetuptable](spi-spi-freetupletable.md) — liberar uma linha definida criada por `SPI_execute` ou uma função semelhante
+ [SPI_freeplan](spi-spi-freeplan.md) — liberar uma declaração preparada salva anteriormente

* [45.4. Gerenciamento de Transações](spi-transaction.md)

+ [SPI_commit](spi-spi-commit.md) — confirmar a transação atual

* [45.5. Visibilidade das Alterações de Dados](spi-visibility.md)
* [45.6. Exemplos](spi-examples.md)

A *Interface de Programação do Servidor* (SPI) permite que os autores de funções C definidas pelo usuário executem comandos SQL dentro de suas funções ou procedimentos. A SPI é um conjunto de funções de interface para simplificar o acesso ao analisador, planejador e executor. A SPI também realiza alguma gestão de memória.

### Nota

Os idiomas processuais disponíveis oferecem vários meios para executar comandos SQL a partir de funções. A maioria dessas facilidades é baseada no SPI, portanto, essa documentação pode ser útil também para usuários desses idiomas.

Observe que, se um comando invocado via SPI falhar, o controle não será devolvido à sua função C. Em vez disso, a transação ou subtransação na qual sua função C é executada será revertida. (Isso pode parecer surpreendente, dado que as funções SPI na maioria das vezes têm convenções documentadas de retorno de erro. Essas convenções, no entanto, só se aplicam para erros detectados dentro das próprias funções SPI.) É possível recuperar o controle após um erro, estabelecendo sua própria subtransação em torno de chamadas SPI que possam falhar.

As funções do SPI retornam um resultado não negativo em caso de sucesso (por meio de um valor inteiro retornado ou na variável global `SPI_result`, conforme descrito abaixo). Em caso de erro, será retornado um resultado negativo ou `NULL`.

Os arquivos de código-fonte que utilizam SPI devem incluir o arquivo de cabeçalho `executor/spi.h`.