## 42.5. Acesso ao banco de dados a partir de PL/Tcl [#](#PLTCL-DBACCESS)

Nesta seção, seguimos a convenção usual do Tcl de usar pontos finais, em vez de colchetes, para indicar um elemento opcional em um sinopse de sintaxe. Os seguintes comandos estão disponíveis para acessar o banco de dados a partir do corpo de uma função PL/Tcl:

`spi_exec ?-count n? ?-array name? command ?loop-body?`: Executa um comando SQL fornecido como uma string. Um erro no comando causa a geração de um erro. Caso contrário, o valor de retorno de `spi_exec` é o número de linhas processadas (selecionadas, inseridas, atualizadas ou excluídas) pelo comando, ou zero se o comando for uma declaração de utilitário. Além disso, se o comando for uma declaração `SELECT`, os valores das colunas selecionadas são colocados em variáveis Tcl conforme descrito abaixo.

O valor opcional `-count` informa ao `spi_exec` para parar assim que as *`n`* linhas forem recuperadas, muito como se a consulta incluísse uma cláusula `LIMIT`. Se *`n`* for zero, a consulta é executada até o término, o mesmo que quando `-count` é omitido.

Se o comando for uma declaração `SELECT`, os valores das colunas de resultado são colocados em variáveis Tcl com nomes baseados nas colunas. Se a opção `-array` for fornecida, os valores das colunas são armazenados, em vez disso, em elementos do array associativo nomeado, com os nomes das colunas usados como índices do array. Além disso, o número atual da linha dentro do resultado (contando a partir de zero) é armazenado no elemento do array denominado “`.tupno`”, a menos que esse nome esteja em uso como um nome de coluna no resultado.

Se o comando for uma declaração `SELECT` e não for fornecido um script *`loop-body`*, apenas a primeira linha dos resultados é armazenada em variáveis Tcl ou elementos de matriz; as linhas restantes, se houver, são ignoradas. Não ocorre armazenamento se a consulta retornar nenhuma linha. (Este caso pode ser detectado verificando o resultado de `spi_exec`.) Por exemplo:

``` spi_exec "SELECT count(*) AS cnt FROM pg_proc"
    ```

definirá a variável Tcl `$cnt` com o número de linhas no catálogo do sistema `pg_proc`.

Se o argumento opcional *`loop-body`* for fornecido, é um trecho de script Tcl que é executado uma vez para cada linha no resultado da consulta. (*`loop-body`* é ignorado se o comando fornecido não for um `SELECT`.) Os valores das colunas da linha atual são armazenados em variáveis Tcl ou elementos de matriz antes de cada iteração. Por exemplo:

    ```
    spi_exec -array C "SELECT * FROM pg_class" { elog DEBUG "have table $C(relname)" }
    ```

imprimirá uma mensagem de registro para cada linha de `pg_class`. Esse recurso funciona de maneira semelhante a outras construções de laço do Tcl; em particular, `continue` e `break` funcionam da maneira usual dentro do corpo do laço.

Se uma coluna de um resultado de consulta for nula, a variável de destino para ela é "desdefinida" em vez de ser definida.

`spi_prepare` *`query`* *`typelist`*: Prepara e salva um plano de consulta para execução posterior. O plano salvo será mantido durante a vida da sessão atual.

A consulta pode usar parâmetros, ou seja, marcadores para valores que devem ser fornecidos sempre que o plano for executado. Na string de consulta, consulte os parâmetros pelos símbolos `$1`... `$n`. Se a consulta usar parâmetros, os nomes dos tipos de parâmetros devem ser fornecidos como uma lista Tcl. (Escreva uma lista vazia para *`typelist`* se nenhum parâmetro for usado.)

O valor de retorno de `spi_prepare` é um ID de consulta que deve ser usado em chamadas subsequentes a `spi_execp`. Consulte `spi_execp` para um exemplo.

`spi_execp ?-count n? ?-array name? ?-nulls string? queryid ?value-list? ?loop-body?`: Realiza uma consulta previamente preparada com `spi_prepare`. *`queryid`* é o ID retornado por `spi_prepare`. Se a consulta fizer referência a parâmetros, um *`value-list`* deve ser fornecido. Esta é uma lista Tcl de valores reais para os parâmetros. A lista deve ter o mesmo comprimento que a lista de tipos de parâmetros previamente fornecida a `spi_prepare`. Omit *`value-list`* se a consulta não tiver parâmetros.

O valor opcional para `-nulls` é uma cadeia de espaços e caracteres `'n'` que informa ao `spi_execp` quais dos parâmetros são valores nulos. Se fornecido, ele deve ter exatamente o mesmo comprimento que o *`value-list`*. Se não for fornecido, todos os valores dos parâmetros são não nulos.

Exceto pela maneira como a consulta e seus parâmetros são especificados, `spi_execp` funciona da mesma forma que `spi_exec`. As opções `-count`, `-array` e *`loop-body`* são as mesmas, assim como o valor do resultado.

Aqui está um exemplo de uma função PL/Tcl que utiliza um plano preparado:

``` CREATE FUNCTION t1_count(integer, integer) RETURNS integer AS $$ if {![ info exists GD(plan) ]} { # prepare the saved plan on the first call set GD(plan) [ spi_prepare \ "SELECT count(*) AS cnt FROM t1 WHERE num >= \$1 AND num <= \$2" \ [ list int4 int4 ] ] } spi_execp -count 1 $GD(plan) [ list $1 $2 ] return $cnt $$ LANGUAGE pltcl;
    ```

Precisamos de barras invertidas dentro da string de consulta fornecida ao `spi_prepare` para garantir que os marcadores `$n` sejam passados para `spi_prepare` como estão, e não substituídos pela substituição de variáveis Tcl.

`subtransaction` *`command`*
:   O script Tcl contido em *`command`* é executado dentro de uma subtransação SQL. Se o script retornar um erro, toda a subtransação é revertida antes de retornar o erro para o código Tcl circundante. Consulte [Seção 42.9][(pltcl-subtransactions.md "42.9. Explicit Subtransactions in PL/Tcl")] para mais detalhes e um exemplo.

`quote` *`string`*
:   Duplica todas as ocorrências de caracteres de aspas simples e barras invertidas
    na string dada. Isso pode ser usado para citar strings
    que devem ser inseridas em comandos SQL dados
    a `spi_exec` ou
    `spi_prepare`.
    Por exemplo, pense em uma string de comando SQL como:

    ```
    "SELECT '$val' AS ret"
    ```

onde a variável Tcl `val` na verdade contém `doesn't`. Isso resultaria
na string de comando final:

    ```
    SELECT 'doesn't' AS ret
    ```

que causaria um erro de análise durante
`spi_exec` ou
`spi_prepare`. Para funcionar corretamente, o comando enviado deve conter:

    ```
    SELECT 'doesn''t' AS ret
    ```

que podem ser formados em PL/Tcl usando:

    ```
    "SELECT '[ quote $val ]' AS ret"
    ```

Uma vantagem do `spi_execp` é que você não precisa citar os valores dos parâmetros dessa forma, pois os parâmetros nunca são analisados como parte de uma cadeia de comando SQL.

`elog` *`level`* *`msg`*
:   Emissa uma mensagem de log ou erro. Os níveis possíveis são
    `DEBUG`, `LOG`, `INFO`,
    `NOTICE`, `WARNING`, `ERROR`, e
    `FATAL`. `ERROR`
    leva uma condição de erro; se não for capturada pelo código Tcl
    circundante, o erro se propaga para a consulta que o solicitou,
    causando o encerramento da transação ou subtransação atual. Isso
    é efetivamente o mesmo que o comando Tcl `error`.
    `FATAL` encerra a transação e faz com que a sessão atual
    se encerre. (Provavelmente não há um bom motivo para usar
    este nível de erro em funções PL/Tcl, mas é fornecido por
    completude.) Os outros níveis apenas geram mensagens de diferentes
    níveis de prioridade.
    Se mensagens de uma prioridade particular são relatadas ao cliente,
    escritas no log do servidor ou ambas, é controlado pelas
    variáveis de configuração [log_min_messages](runtime-config-logging.md#GUC-LOG-MIN-MESSAGES) e
    [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES)
    Consulte [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration")
    e [Seção 42.8](pltcl-error-handling.md "42.8. Error Handling in PL/Tcl")
    para mais informações.