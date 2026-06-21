## Crie a função

Crie função — defina uma nova função

## Sinopse

```
CREATE [ OR REPLACE ] FUNCTION
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
    [ RETURNS rettype
      | RETURNS TABLE ( column_name column_type [, ...] ) ]
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | WINDOW
    | { IMMUTABLE | STABLE | VOLATILE }
    | [ NOT ] LEAKPROOF
    | { CALLED ON NULL INPUT | RETURNS NULL ON NULL INPUT | STRICT }
    | { [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER }
    | PARALLEL { UNSAFE | RESTRICTED | SAFE }
    | COST execution_cost
    | ROWS result_rows
    | SUPPORT support_function
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
    | sql_body
  } ...
```

## Descrição

`CREATE FUNCTION` define uma nova função. `CREATE OR REPLACE FUNCTION` irá criar uma nova função ou substituir uma definição existente. Para poder definir uma função, o usuário deve ter o privilégio `USAGE` na linguagem.

Se um nome de esquema for incluído, a função será criada no esquema especificado. Caso contrário, será criada no esquema atual. O nome da nova função não deve corresponder a nenhuma função ou procedimento existente com os mesmos tipos de argumentos de entrada no mesmo esquema. No entanto, funções e procedimentos de diferentes tipos de argumentos podem compartilhar um nome (isso é chamado de *sobrecarga*).

Para substituir a definição atual de uma função existente, use `CREATE OR REPLACE FUNCTION`. Não é possível alterar o nome ou os tipos de argumentos de uma função dessa forma (se você tentasse, na verdade, estaria criando uma nova função distinta). Além disso, `CREATE OR REPLACE FUNCTION` não permitirá que você altere o tipo de retorno de uma função existente. Para fazer isso, você deve descartar e recriar a função. (Ao usar os parâmetros `OUT`, isso significa que você não pode alterar os tipos de quaisquer parâmetros `OUT`, exceto descartando a função.)

Quando o `CREATE OR REPLACE FUNCTION` é usado para substituir uma função existente, a propriedade e os permissões da função não mudam. Todos os outros atributos da função recebem os valores especificados ou implícitos no comando. Você deve possuir a função para substituí-la (isso inclui ser membro do papel de propriedade).

Se você excluir e, em seguida, recriar uma função, a nova função não será a mesma entidade da antiga; você terá que excluir as regras, visualizações, gatilhos, etc., existentes que se referem à função antiga. Use `CREATE OR REPLACE FUNCTION` para alterar a definição de uma função sem quebrar objetos que se referem à função. Além disso, `ALTER FUNCTION` pode ser usado para alterar a maioria das propriedades auxiliares de uma função existente.

O usuário que cria a função se torna o proprietário da função.

Para poder criar uma função, você deve ter o privilégio `USAGE` nos tipos de argumentos e no tipo de retorno.

Consulte a [Seção 36.3][(xfunc.md "36.3. User-Defined Functions")] para obter mais informações sobre a escrita de funções.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) da função a ser criada.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Apenas argumentos `OUT` podem seguir um argumento `VARIADIC`. Além disso, os argumentos `OUT` e `INOUT` não podem ser usados juntos com a notação `RETURNS TABLE`.

*`argname`*: O nome de um argumento. Algumas linguagens (incluindo SQL e PL/pgSQL) permitem que você use o nome no corpo da função. Para outras linguagens, o nome de um argumento de entrada é apenas documentação adicional, no que diz respeito à própria função; mas você pode usar os nomes dos argumentos de entrada ao chamar uma função para melhorar a legibilidade (consulte [Seção 4.3][(sql-syntax-calling-funcs.md "4.3. Calling Functions")]). Em qualquer caso, o nome de um argumento de saída é significativo, porque ele define o nome da coluna no tipo da linha de resultado. (Se você omitir o nome de um argumento de saída, o sistema escolherá um nome de coluna padrão.)

*`argtype`*: O(s) tipo(s) de dados dos argumentos da função (opcionalmente qualificados por esquema), se houver. Os tipos de argumento podem ser de base, compostos ou tipos de domínio, ou podem referenciar o tipo de uma coluna de tabela.

Dependendo do idioma de implementação, também pode ser permitido especificar “pseudo-tipos”, como `cstring`. Pseudo-tipos indicam que o tipo de argumento real é incompletamente especificado ou está fora do conjunto de tipos de dados SQL comuns.

O tipo de uma coluna é referenciado escrevendo `table_name.column_name%TYPE`. O uso desse recurso pode, às vezes, ajudar a tornar uma função independente das mudanças na definição de uma tabela.

*`default_expr`*: Uma expressão que deve ser usada como valor padrão se o parâmetro não for especificado. A expressão deve ser coerível com o tipo de argumento do parâmetro. Apenas os parâmetros de entrada (incluindo `INOUT`) podem ter um valor padrão. Todos os parâmetros de entrada que seguem um parâmetro com um valor padrão devem ter valores padrão também.

*`rettype`*: O tipo de dados de retorno (opcionalmente qualificado por esquema). O tipo de retorno pode ser um tipo de base, composto ou domínio, ou pode referenciar o tipo de uma coluna de tabela. Dependendo do idioma de implementação, também pode ser permitido especificar "pseudo-tipos", como `cstring`. Se a função não deve retornar um valor, especifique `void` como o tipo de retorno.

Quando houver os parâmetros `OUT` ou `INOUT`, a cláusula `RETURNS` pode ser omitida. Se estiver presente, ela deve concordar com o tipo de resultado implícito pelos parâmetros de saída: `RECORD` se houver vários parâmetros de saída, ou o mesmo tipo que o único parâmetro de saída.

O modificador `SETOF` indica que a função retornará um conjunto de itens, em vez de um único item.

O tipo de uma coluna é referenciado escrevendo `table_name.column_name%TYPE`.

*`column_name`*: O nome de uma coluna de saída na sintaxe `RETURNS TABLE`. Isso é, efetivamente, outra maneira de declarar um parâmetro `OUT` nomeado, exceto que `RETURNS TABLE` também implica em `RETURNS SETOF`.

*`column_type`*: O tipo de dados de uma coluna de saída na sintaxe `RETURNS TABLE`.

*`lang_name`*: O nome da linguagem na qual a função é implementada. Pode ser `sql`, `c`, `internal`, ou o nome de uma linguagem procedural definida pelo usuário, por exemplo, `plpgsql`. O padrão é `sql` se *`sql_body`* for especificado. Enquadrar o nome em aspas é desaconselhável e requer correspondência de caso.

`TRANSFORM { FOR TYPE type_name } [, ... ] }`: Lista as transformações que uma chamada à função deve aplicar. As transformações convertem entre tipos SQL e tipos de dados específicos do idioma; veja [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM"). As implementações em linguagem procedural geralmente têm conhecimento pré-codificado dos tipos embutidos, portanto, esses não precisam ser listados aqui. Se uma implementação em linguagem procedural não souber como lidar com um tipo e nenhum transformação for fornecida, ela retornará um comportamento padrão para a conversão de tipos de dados, mas isso depende da implementação.

`WINDOW`: `WINDOW` indica que a função é uma *função de janela* e não uma função simples. Isso atualmente é útil apenas para funções escritas em C. O atributo `WINDOW` não pode ser alterado ao substituir uma definição de função existente.

`IMMUTABLE` `STABLE` `VOLATILE`: Esses atributos informam o otimizador de consulta sobre o comportamento da função. No máximo, uma escolha pode ser especificada. Se nenhuma dessas opções aparecer, `VOLATILE` é a suposição padrão.

`IMMUTABLE` indica que a função não pode modificar o banco de dados e sempre retorna o mesmo resultado quando recebe os mesmos valores de argumento; ou seja, não faz pesquisas no banco de dados ou não usa informações que não estejam diretamente presentes em sua lista de argumentos. Se esta opção for dada, qualquer chamada da função com argumentos constantes pode ser imediatamente substituída pelo valor da função.

`STABLE` indica que a função não pode modificar o banco de dados, e que, dentro de uma única varredura da tabela, ela retornará consistentemente o mesmo resultado para os mesmos valores de argumento, mas que seu resultado pode mudar em declarações SQL. Esta é a seleção apropriada para funções cujos resultados dependem de consultas no banco de dados, variáveis de parâmetro (como a fusão de hora atual) etc. (É inadequado para `AFTER` gatilhos que desejam consultar linhas modificadas pelo comando atual.) Além disso, note que a família de funções `current_timestamp` se qualifica como estável, uma vez que seus valores não mudam dentro de uma transação.

`VOLATILE` indica que o valor da função pode mudar mesmo dentro de uma única varredura na tabela, portanto, não é possível fazer otimizações. Relativamente poucas funções de banco de dados são voláteis nesse sentido; alguns exemplos são `random()`, `currval()`, `timeofday()`. Mas observe que qualquer função que tenha efeitos colaterais deve ser classificada como volátil, mesmo que seu resultado seja bastante previsível, para evitar que as chamadas sejam otimizadas; um exemplo é `setval()`.

Para obter informações adicionais, consulte a [Seção 36.7][(xfunc-volatility.md "36.7. Function Volatility Categories")].

`LEAKPROOF`: `LEAKPROOF` indica que a função não tem efeitos colaterais. Não revela nenhuma informação sobre seus argumentos, exceto pelo seu valor de retorno. Por exemplo, uma função que lança uma mensagem de erro para alguns valores de argumento, mas não para outros, ou que inclui os valores de argumento em qualquer mensagem de erro, não é à prova de vazamento. Isso afeta a forma como o sistema executa consultas contra visualizações criadas com a opção `security_barrier` ou tabelas com segurança de nível de linha habilitada. O sistema aplicará condições de políticas de segurança e visualizações de barreira de segurança antes de quaisquer condições fornecidas pelo usuário da própria consulta que contenham funções não à prova de vazamento, a fim de prevenir a exposição inadvertida de dados. Funções e operadores marcados como à prova de vazamento são considerados confiáveis e podem ser executados antes das condições de políticas de segurança e visualizações de barreira de segurança. Além disso, funções que não aceitam argumentos ou que não recebem quaisquer argumentos da visualização ou tabela de barreira de segurança não precisam ser marcadas como à prova de vazamento para serem executadas antes das condições de segurança. Consulte [CREATE VIEW](sql-createview.md "CREATE VIEW") e [Seção 39.5](rules-privileges.md "39.5. Rules and Privileges"). Esta opção só pode ser definida pelo superusuário.

`CALLED ON NULL INPUT` `RETURNS NULL ON NULL INPUT` `STRICT`: `CALLED ON NULL INPUT` (padrão) indica que a função será chamada normalmente quando alguns de seus argumentos forem nulos. É, então, responsabilidade do autor da função verificar, se necessário, os valores nulos e responder adequadamente.

`RETURNS NULL ON NULL INPUT` ou `STRICT` indica que a função sempre retorna nulo sempre que qualquer um de seus argumentos for nulo. Se este parâmetro for especificado, a função não é executada quando há argumentos nulos; em vez disso, um resultado nulo é assumido automaticamente.

`[EXTERNAL] SECURITY INVOKER` `[EXTERNAL] SECURITY DEFINER`: `SECURITY INVOKER` indica que a função deve ser executada com os privilégios do usuário que a chama. Isso é o padrão. `SECURITY DEFINER` especifica que a função deve ser executada com os privilégios do usuário que a possui. Para informações sobre como escrever funções `SECURITY DEFINER` de forma segura, [veja abaixo](sql-createfunction.md#SQL-CREATEFUNCTION-SECURITY "Writing SECURITY DEFINER Functions Safely").

A palavra-chave `EXTERNAL` é permitida para conformidade com SQL, mas é opcional, pois, ao contrário do que acontece com o SQL, essa funcionalidade se aplica a todas as funções, não apenas às externas.

`PARALLEL`: `PARALLEL UNSAFE` indica que a função não pode ser executada em modo paralelo; a presença de tal função em uma declaração SQL força um plano de execução serial. Este é o padrão. `PARALLEL RESTRICTED` indica que a função pode ser executada em modo paralelo, mas apenas no processo do líder do grupo paralelo. `PARALLEL SAFE` indica que a função é segura para ser executada em modo paralelo sem restrições, incluindo em processos de trabalhador paralelo.

As funções devem ser rotuladas como inseguras em paralelo se elas modificarem qualquer estado do banco de dados, alterarem o estado da transação (exceto usando uma subtransação para recuperação de erros), acessem sequências (por exemplo, chamando `currval`) ou façam alterações persistentes nos ajustes. Elas devem ser rotuladas como restritas em paralelo se elas acessarem tabelas temporárias, estado da conexão do cliente, cursors, declarações preparadas ou estado variável local do backend que o sistema não possa sincronizar em modo paralelo (por exemplo, `setseed` não pode ser executado senão pelo líder do grupo, pois uma mudança feita por outro processo não seria refletida no líder). Em geral, se uma função é rotulada como segura quando restrita ou insegura, ou se é rotulada como restrita quando na verdade é insegura, ela pode lançar erros ou produzir respostas erradas quando usada em uma consulta paralela. As funções em linguagem C poderiam, teoricamente, exibir comportamento totalmente indefinido se mal rotuladas, uma vez que não há maneira para o sistema se proteger contra código C arbitrário, mas, na maioria dos casos, o resultado não será pior do que para qualquer outra função. Se houver dúvida, as funções devem ser rotuladas como `UNSAFE`, que é o padrão.

`COST` *`execution_cost`*: Um número positivo que fornece o custo estimado de execução da função, em unidades de [cpu_operator_cost](runtime-config-query.md#GUC-CPU-OPERATOR-COST). Se a função retornar um conjunto, este é o custo por linha devolvida. Se o custo não for especificado, 1 unidade é assumida para funções em linguagem C e funções internas, e 100 unidades para funções em todos os outros idiomas. Valores maiores fazem com que o planejador tente evitar avaliar a função com mais frequência do que o necessário.

`ROWS` *`result_rows`*: Um número positivo que indica o número estimado de linhas que o planejador deve esperar que a função retorne. Isso só é permitido quando a função é declarada para retornar um conjunto. A suposição padrão é de 1000 linhas.

`SUPPORT` *`support_function`*: O nome (opcionalmente qualificado por esquema) de uma *função de suporte de planejador* a ser usada para esta função. Consulte [Seção 36.11][(xfunc-optimization.md "36.11. Function Optimization Information")] para detalhes. Você deve ser um superusuário para usar esta opção.

*`configuration_parameter`* *`value`*: A cláusula `SET` faz com que o parâmetro de configuração especificado seja definido pelo valor especificado quando a função é executada, e então restaurado ao seu valor anterior quando a função é encerrada. `SET FROM CURRENT` salva o valor do parâmetro que é atual quando `CREATE FUNCTION` é executado como o valor a ser aplicado quando a função é executada.

Se uma cláusula `SET` estiver anexada a uma função, os efeitos de um comando `SET LOCAL` executado dentro da função para a mesma variável são restritos à função: o valor anterior do parâmetro de configuração ainda é restaurado na saída da função. No entanto, um comando `SET` comum (sem `LOCAL`) substitui a cláusula `SET`, assim como faria para um comando anterior `SET LOCAL`: os efeitos de tal comando persistirão após a saída da função, a menos que a transação atual seja revertida.

Veja [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações sobre os nomes e valores permitidos dos parâmetros.

*`definition`*: Uma constante de cadeia que define a função; o significado depende do idioma. Pode ser um nome de função interna, o caminho para um arquivo de objeto, um comando SQL ou texto em uma linguagem procedural.

É frequentemente útil usar citação em dólares (consulte [Seção 4.1.2.4][(sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING "4.1.2.4. Dollar-Quoted String Constants")]) para escrever a string de definição da função, em vez da sintaxe normal de citação simples. Sem citação em dólares, quaisquer citações simples ou barras invertidas na definição da função devem ser escapadas duplicando-as.

`obj_file, link_symbol`: Esta forma da cláusula `AS` é usada para funções dinamicamente carregáveis em linguagem C, quando o nome da função no código-fonte da linguagem C não é o mesmo que o nome da função SQL. A string *`obj_file`* é o nome do arquivo da biblioteca compartilhada que contém a função C compilada, e é interpretada como para o comando [`LOAD`(sql-load.md "LOAD")]. A string *`link_symbol`* é o símbolo de ligação da função, ou seja, o nome da função no código-fonte da linguagem C. Se o símbolo de ligação for omitido, presume-se que seja o mesmo que o nome da função SQL sendo definida. Os nomes em C de todas as funções devem ser diferentes, então você deve dar funções sobrecarregadas em C nomes diferentes (por exemplo, use os tipos de argumentos como parte dos nomes em C).

Quando chamadas repetidas `CREATE FUNCTION` se referirem ao mesmo arquivo de objeto, o arquivo só será carregado uma vez por sessão. Para descarregar e recarregar o arquivo (talvez durante o desenvolvimento), inicie uma nova sessão.

*`sql_body`*: O corpo de uma função `LANGUAGE SQL`. Isso pode ser uma única declaração

``` RETURN expression
    ```

ou um bloco

    ```
    BEGIN ATOMIC statement; statement; ... statement; END
    ```

Isso é semelhante a escrever o texto do corpo da função como uma constante de string (ver *`definition`* acima), mas há algumas diferenças: Esta forma só funciona para `LANGUAGE SQL`, a forma de constante de string funciona para todos os idiomas. Esta forma é analisada no momento da definição da função, a forma de constante de string é analisada no momento da execução; portanto, esta forma não pode suportar tipos de argumentos polimórficos e outras construções que não sejam resolvíveis no momento da definição da função. Esta forma rastreia as dependências entre a função e os objetos usados no corpo da função, então `DROP ... CASCADE` funcionará corretamente, enquanto a forma que usa literais de string pode deixar funções pendentes. Finalmente, esta forma é mais compatível com o padrão SQL e outras implementações SQL.

## Sobrecarga

O PostgreSQL permite a *sobrecarga de funções*; ou seja, o mesmo nome pode ser usado para várias funções diferentes, desde que elas tenham tipos de argumentos de entrada distintos. Se você o usa ou não, essa capacidade implica precauções de segurança ao chamar funções em bancos de dados onde alguns usuários desconfiam dos outros; veja [Seção 10.3][(typeconv-func.md "10.3. Functions")].

Duas funções são consideradas iguais se tiverem os mesmos nomes e tipos de argumentos de entrada, ignorando quaisquer parâmetros `OUT`. Assim, por exemplo, essas declarações entram em conflito:

```
CREATE FUNCTION foo(int) ... CREATE FUNCTION foo(int, out text) ...
```

Funções que têm diferentes listas de tipos de argumento não serão consideradas conflitantes no momento da criação, mas se forem fornecidas opções padrão, elas podem entrar em conflito no uso. Por exemplo, considere

```
CREATE FUNCTION foo(int) ... CREATE FUNCTION foo(int, int default 42) ...
```

Uma chamada `foo(10)` falhará devido à ambiguidade sobre qual função deve ser chamada.

## Notas

O tipo de sintaxe SQL completo é permitido para declarar os argumentos e o valor de retorno de uma função. No entanto, os modificadores de tipo entre parênteses (por exemplo, o campo de precisão para o tipo `numeric`) são descartados pelo `CREATE FUNCTION`. Assim, por exemplo, `CREATE FUNCTION foo (varchar(10)) ...` é exatamente o mesmo que `CREATE FUNCTION foo (varchar) ...`.

Ao substituir uma função existente por `CREATE OR REPLACE FUNCTION`, há restrições para alterar os nomes dos parâmetros. Não é possível alterar o nome já atribuído a qualquer parâmetro de entrada (embora você possa adicionar nomes a parâmetros que não tinham antes). Se houver mais de um parâmetro de saída, não é possível alterar os nomes dos parâmetros de saída, porque isso mudaria os nomes das colunas do tipo composto anônimo que descreve o resultado da função. Essas restrições são feitas para garantir que as chamadas existentes da função não parem de funcionar quando ela é substituída.

Se uma função for declarada `STRICT` com um argumento `VARIADIC`, a verificação de estrito teste que o array variadic *como um todo* não é nulo. A função ainda será chamada se o array tiver elementos nulos.

## Exemplos

Adicione dois inteiros usando uma função SQL:

```
CREATE FUNCTION add(integer, integer) RETURNS integer AS 'select $1 + $2;' LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT;
```

A mesma função escrita em um estilo mais conforme ao SQL, usando nomes de argumentos e um corpo não citado:

```
CREATE FUNCTION add(a integer, b integer) RETURNS integer LANGUAGE SQL IMMUTABLE RETURNS NULL ON NULL INPUT RETURN a + b;
```

Incremente um inteiro, utilizando o nome de um argumento, em PL/pgSQL:

```
CREATE OR REPLACE FUNCTION increment(i integer) RETURNS integer AS $$ BEGIN RETURN i + 1; END; $$ LANGUAGE plpgsql;
```

Retorne um registro contendo vários parâmetros de saída:

```
CREATE FUNCTION dup(in int, out f1 int, out f2 text) AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$ LANGUAGE SQL;

SELECT * FROM dup(42);
```

Você pode fazer a mesma coisa de forma mais detalhada com um tipo composto explicitamente nomeado:

```
CREATE TYPE dup_result AS (f1 int, f2 text);

CREATE FUNCTION dup(int) RETURNS dup_result AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$ LANGUAGE SQL;

SELECT * FROM dup(42);
```

Outra maneira de retornar várias colunas é usar uma função `TABLE`:

```
CREATE FUNCTION dup(int) RETURNS TABLE(f1 int, f2 text) AS $$ SELECT $1, CAST($1 AS text) || ' is text' $$ LANGUAGE SQL;

SELECT * FROM dup(42);
```

No entanto, uma função `TABLE` é diferente dos exemplos anteriores, porque ela realmente retorna um *conjunto* de registros, não apenas um registro.

## Escrever funções `SECURITY DEFINER` com segurança

Como uma função `SECURITY DEFINER` é executada com os privilégios do usuário que a possui, é necessário ter cuidado para garantir que a função não seja mal utilizada. Por segurança, [search_path][(runtime-config-client.md#GUC-SEARCH-PATH)] deve ser configurada para excluir quaisquer esquemas que possam ser escritos por usuários não confiáveis. Isso impede que usuários maliciosos criem objetos (por exemplo, tabelas, funções e operadores) que ocultem objetos destinados a serem usados pela função. Particularmente importante a esse respeito é o esquema de tabela temporária, que é pesquisado como padrão, e normalmente pode ser escrito por qualquer pessoa. Uma disposição segura pode ser obtida forçando o esquema temporário a ser pesquisado por último. Para fazer isso, escreva `pg_temp` como a última entrada em `search_path`. Esta função ilustra o uso seguro:

```
CREATE FUNCTION check_password(uname TEXT, pass TEXT) RETURNS BOOLEAN AS $$ DECLARE passed BOOLEAN; BEGIN SELECT  (pwd = $2) INTO passed FROM    pwds WHERE   username = $1;

        RETURN passed; END; $$  LANGUAGE plpgsql SECURITY DEFINER -- Set a secure search_path: trusted schema(s), then 'pg_temp'. SET search_path = admin, pg_temp;
```

A intenção desta função é acessar uma tabela `admin.pwds`. Mas sem a cláusula `SET`, ou com uma cláusula `SET` que mencione apenas `admin`, a função pode ser subvertida ao criar uma tabela temporária chamada `pwds`.

Se a função de definição de segurança pretender criar papéis e se estiver sendo executada como um usuário não de nível de administrador, `createrole_self_grant` também deve ser definido com um valor conhecido usando a cláusula `SET`.

Outro ponto a ter em mente é que, por padrão, o privilégio de execução é concedido a `PUBLIC` para funções recém-criadas (consulte [Seção 5.8][(ddl-priv.md "5.8. Privileges")] para mais informações). Frequentemente, você deseja restringir o uso de uma função de definição de segurança apenas para alguns usuários. Para fazer isso, você deve revogar os privilégios padrão de `PUBLIC` e, em seguida, conceder o privilégio de execução seletivamente. Para evitar ter uma janela onde a nova função é acessível a todos, crie-a e defina os privilégios dentro de uma única transação. Por exemplo:

```
BEGIN; CREATE FUNCTION check_password(uname TEXT, pass TEXT) ... SECURITY DEFINER; REVOKE ALL ON FUNCTION check_password(uname TEXT, pass TEXT) FROM PUBLIC; GRANT EXECUTE ON FUNCTION check_password(uname TEXT, pass TEXT) TO admins; COMMIT;
```

## Compatibilidade

Um comando `CREATE FUNCTION` é definido no padrão SQL. A implementação do PostgreSQL pode ser usada de maneira compatível, mas possui muitas extensões. Por outro lado, o padrão SQL especifica uma série de recursos opcionais que não são implementados no PostgreSQL.

Os seguintes são problemas importantes de compatibilidade:

* `OR REPLACE` é uma extensão do PostgreSQL.
* Para compatibilidade com outros sistemas de banco de dados, *`argmode`* pode ser escrito antes ou depois de *`argname`*. Mas apenas a primeira maneira é compatível com o padrão.
* Para os padrões de parâmetros, o padrão SQL especifica apenas a sintaxe com a palavra-chave `DEFAULT`. A sintaxe com `=` é usada em T-SQL e Firebird.
* O modificador `SETOF` é uma extensão do PostgreSQL.
* Apenas `SQL` é padronizado como uma linguagem.
* Todos os outros atributos, exceto `CALLED ON NULL INPUT` e `RETURNS NULL ON NULL INPUT`, não são padronizados.
* Para o corpo das funções de `LANGUAGE SQL`, o padrão SQL especifica apenas a forma *`sql_body`*.

Funções simples `LANGUAGE SQL` podem ser escritas de uma maneira que seja conforme padrão e portátil para outras implementações. Funções mais complexas que utilizam recursos avançados, atributos de otimização ou outros idiomas serão necessariamente específicas para o PostgreSQL de uma maneira significativa.

## Veja também

[ALTERAR FUNÇÃO](sql-alterfunction.md "ALTER FUNCTION"), [DROP FUNÇÃO](sql-dropfunction.md "DROP FUNCTION"), [CONCEDA](sql-grant.md "GRANT"), [CARREGAR](sql-load.md "LOAD"), [RETIRO](sql-revoke.md "REVOKE")