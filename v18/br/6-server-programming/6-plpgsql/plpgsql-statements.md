## 41.5. Declarações Básicas [#](#PLPGSQL-STATEMENTS)

* [41.5.1. Atribuição](plpgsql-statements.md#PLPGSQL-STATEMENTS-ASSIGNMENT)
* [41.5.2. Executar comandos SQL](plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL)
* [41.5.3. Executar um comando com um resultado de uma única linha](plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW)
* [41.5.4. Executar comandos dinâmicos](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN)
* [41.5.5. Obter o status do resultado](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)
* [41.5.6. Não fazer nada](plpgsql-statements.md#PLPGSQL-STATEMENTS-NULL)

Nesta seção e nas seguintes, descrevemos todos os tipos de declaração que são explicitamente compreendidos pelo PL/pgSQL. Qualquer coisa que não seja reconhecida como um desses tipos de declaração é presumida ser um comando SQL e é enviada ao motor principal do banco de dados para execução, conforme descrito em [Seção 41.5.2](plpgsql-statements.md#PLPGSQL-STATEMENTS-GENERAL-SQL).

### 41.5.1. Atribuição [#](#PLPGSQL-STATEMENTS-ASSIGNMENT)

Uma atribuição de um valor a uma variável PL/pgSQL é escrita da seguinte forma:

```
variable { := | = } expression;
```

Como explicado anteriormente, a expressão em tal declaração é avaliada por meio de um comando SQL `SELECT` enviado ao motor principal do banco de dados. A expressão deve produzir um único valor (possivelmente um valor de linha, se a variável for uma variável de linha ou registro). A variável alvo pode ser uma variável simples (opcionalmente qualificada com um nome de bloco), um campo de um alvo de linha ou registro, ou um elemento ou fatias de um alvo de matriz. Igual (`=`) pode ser usado em vez de `:=` compatível com PL/SQL.

Se o tipo de dados do resultado da expressão não corresponder ao tipo de dados da variável, o valor será convertido como se fosse um cast de atribuição (consulte [Seção 10.4](typeconv-query.md)). Se não for conhecido nenhum cast de atribuição para o par de tipos de dados envolvidos, o interpretador PL/pgSQL tentará converter o valor do resultado textualmente, ou seja, aplicando a função de saída do tipo de resultado seguida pela função de entrada do tipo de variável. Observe que isso pode resultar em erros de execução gerados pela função de entrada, se a forma de string do valor do resultado não for aceitável para a função de entrada.

Exemplos:

```
tax := subtotal * 0.06;
my_record.user_id := 20;
my_array[j] := 20;
my_array[1:3] := array[1,2,3];
complex_array[n].realpart = 12.3;
```

### 41.5.2. Executando comandos SQL [#](#PLPGSQL-STATEMENTS-GENERAL-SQL)

Em geral, qualquer comando SQL que não retorne linhas pode ser executado dentro de uma função PL/pgSQL, simplesmente escrevendo o comando. Por exemplo, você pode criar e preencher uma tabela escrevendo

```
CREATE TABLE mytable (id int primary key, data text);
INSERT INTO mytable VALUES (1,'one'), (2,'two');
```

Se o comando retornar linhas (por exemplo, `SELECT`, ou `INSERT`/`UPDATE`/`DELETE`/`MERGE` com `RETURNING`), há duas maneiras de proceder. Quando o comando retornará, no máximo, uma linha, ou você só se importa com a primeira linha de saída, escreva o comando como de costume, mas adicione uma cláusula `INTO` para capturar a saída, conforme descrito em [Seção 41.5.3](plpgsql-statements.md#PLPGSQL-STATEMENTS-SQL-ONEROW). Para processar todas as linhas de saída, escreva o comando como fonte de dados para um loop `FOR`, conforme descrito em [Seção 41.6.6](plpgsql-control-structures.md#PLPGSQL-RECORDS-ITERATING).

Geralmente, não é suficiente apenas executar comandos SQL definidos estaticamente. Normalmente, você deseja um comando que utilize valores de dados variáveis ou até mesmo que varie de maneiras mais fundamentais, como usar diferentes nomes de tabela em diferentes momentos. Novamente, há duas maneiras de proceder, dependendo da situação.

Os valores das variáveis PL/pgSQL podem ser inseridos automaticamente em comandos SQL otimizáveis, que são `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` e certos comandos utilitários que incorporam um desses, como `EXPLAIN` e `CREATE TABLE ... AS SELECT`. Nesses comandos, qualquer nome de variável PL/pgSQL que apareça no texto do comando é substituído por um parâmetro de consulta, e então o valor atual da variável é fornecido como o valor do parâmetro no momento da execução. Isso é exatamente como o processamento descrito anteriormente para expressões; para detalhes, consulte [Seção 41.11.1](plpgsql-implementation.md#PLPGSQL-VAR-SUBST).

Ao executar um comando SQL otimizável dessa forma, o PL/pgSQL pode armazenar e reutilizar o plano de execução do comando, conforme discutido em [Seção 41.11.2](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING).

Os comandos SQL não otimizáveis (também chamados de comandos utilitários) não são capazes de aceitar parâmetros de consulta. Portanto, a substituição automática de variáveis PL/pgSQL não funciona em tais comandos. Para incluir texto não constante em um comando utilitário executado a partir de PL/pgSQL, você deve construir o comando utilitário como uma string e, em seguida, `EXECUTE`-lo, conforme discutido em [Seção 41.5.4](plpgsql-statements.md#PLPGSQL-STATEMENTS-EXECUTING-DYN).

`EXECUTE` também deve ser usado se você quiser modificar o comando de alguma outra maneira que não seja fornecer um valor de dados, por exemplo, alterando o nome de uma tabela.

Às vezes, é útil avaliar uma expressão ou consulta `SELECT`, mas descartar o resultado, por exemplo, ao chamar uma função que tem efeitos colaterais, mas sem um valor de resultado útil. Para fazer isso no PL/pgSQL, use a declaração `PERFORM`:

```
PERFORM query;
```

Isso executa *`query`* e descarta o resultado. Escreva *`query`* da mesma maneira que você escreveria um comando SQL `SELECT`, mas substitua a palavra-chave inicial `SELECT` por `PERFORM`. Para consultas `WITH`, use `PERFORM` e, em seguida, coloque a consulta entre parênteses. (Neste caso, a consulta só pode retornar uma linha.) As variáveis PL/pgSQL serão substituídas na consulta da mesma maneira descrita acima, e o plano é armazenado em cache da mesma maneira. Além disso, a variável especial `FOUND` é definida como verdadeira se a consulta produziu pelo menos uma linha, ou falsa se não produziu nenhuma linha (consulte [Seção 41.5.5](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS "41.5.5. Obtaining the Result Status")).

Nota

Pode-se esperar que escrever `SELECT` diretamente consiga alcançar esse resultado, mas, atualmente, a única maneira aceita de fazer isso é `PERFORM`. Um comando SQL que pode retornar linhas, como `SELECT`, será rejeitado como um erro, a menos que tenha uma cláusula `INTO`, conforme discutido na próxima seção.

Um exemplo:

```
PERFORM create_mv('cs_session_page_requests_mv', my_query);
```

### 41.5.3. Executar um comando com um resultado de uma única linha [#](#PLPGSQL-STATEMENTS-SQL-ONEROW)

O resultado de um comando SQL que produz uma única linha (possível de várias colunas) pode ser atribuído a uma variável de registro, variável de tipo de linha ou lista de variáveis escalares. Isso é feito escrevendo o comando SQL básico e adicionando uma cláusula `INTO`. Por exemplo,

```
SELECT select_expressions INTO [STRICT] target FROM ...;
INSERT ... RETURNING expressions INTO [STRICT] target;
UPDATE ... RETURNING expressions INTO [STRICT] target;
DELETE ... RETURNING expressions INTO [STRICT] target;
MERGE ... RETURNING expressions INTO [STRICT] target;
```

onde *`target`* pode ser uma variável de registro, uma variável de linha ou uma lista de variáveis simples e campos de registro/linha separados por vírgula. As variáveis PL/pgSQL serão substituídas no resto do comando (ou seja, tudo, exceto a cláusula `INTO`) da mesma forma descrita acima, e o plano será armazenado na cache da mesma maneira. Isso funciona para `SELECT`, `INSERT`/`UPDATE`/`DELETE`/`MERGE` com `RETURNING`, e certos comandos utilitários que retornam conjuntos de linhas, como `EXPLAIN`. Exceto pela cláusula `INTO`, o comando SQL é o mesmo que seria escrito fora do PL/pgSQL.

### DICA

Observe que essa interpretação de `SELECT` com `INTO` é bastante diferente do comando regular `SELECT INTO` do PostgreSQL, no qual o alvo `INTO` é uma tabela recém-criada. Se você deseja criar uma tabela a partir de um resultado de `SELECT` dentro de uma função PL/pgSQL, use a sintaxe `CREATE TABLE ... AS SELECT`.

Se uma variável de linha ou uma lista de variáveis for usada como alvo, as colunas dos resultados do comando devem corresponder exatamente à estrutura do alvo em termos de número e tipos de dados, caso contrário, ocorrerá um erro de execução. Quando uma variável de registro é o alvo, ela se configura automaticamente ao tipo de linha das colunas dos resultados do comando.

A cláusula `INTO` pode aparecer quase em qualquer lugar no comando SQL. Costuma ser escrita antes ou depois da lista de *`select_expressions`* em um comando `SELECT`, ou no final do comando para outros tipos de comandos. É recomendável que você siga essa convenção, caso o analisador PL/pgSQL se torne mais rigoroso em versões futuras.

Se `STRICT` não for especificado na cláusula `INTO`, então *`target`* será definido na primeira linha retornada pelo comando, ou em nulos se o comando não retornar nenhuma linha. (Observe que “a primeira linha” não é bem definida a menos que você tenha usado `ORDER BY`.) Quaisquer linhas de resultado após a primeira linha são descartadas. Você pode verificar a variável especial `FOUND` (consulte [Seção 41.5.5](plpgsql-statements.md#PLPGSQL-STATEMENTS-DIAGNOSTICS)) para determinar se uma linha foi retornada:

```
SELECT * INTO myrec FROM emp WHERE empname = myname;
IF NOT FOUND THEN
    RAISE EXCEPTION 'employee % not found', myname;
END IF;
```

Se a opção `STRICT` for especificada, o comando deve retornar exatamente uma linha, ou será relatado um erro de execução, seja `NO_DATA_FOUND` (sem linhas) ou `TOO_MANY_ROWS` (mais de uma linha). Você pode usar um bloco de exceção se desejar capturar o erro, por exemplo:

```
BEGIN
    SELECT * INTO STRICT myrec FROM emp WHERE empname = myname;
    EXCEPTION
        WHEN NO_DATA_FOUND THEN
            RAISE EXCEPTION 'employee % not found', myname;
        WHEN TOO_MANY_ROWS THEN
            RAISE EXCEPTION 'employee % not unique', myname;
END;
```

A execução bem-sucedida de um comando com `STRICT` sempre define `FOUND` como verdadeiro.

Para [[`INSERT`]/[`UPDATE`]/[`DELETE`]/[`MERGE`]] com `RETURNING`, o PL/pgSQL reporta um erro para mais de uma linha retornada, mesmo quando `STRICT` não é especificado. Isso ocorre porque não há uma opção como `ORDER BY` com a qual se possa determinar qual linha afetada deve ser retornada.

Se `print_strict_params` estiver habilitado para a função, quando um erro for lançado porque os requisitos de `STRICT` não são atendidos, a parte `DETAIL` da mensagem de erro incluirá informações sobre os parâmetros passados ao comando. Você pode alterar o ajuste `print_strict_params` para todas as funções definindo `plpgsql.print_strict_params`, embora apenas as compilações subsequentes de funções sejam afetadas. Você também pode habilitá-lo em uma base por função usando uma opção do compilador, por exemplo:

```
CREATE FUNCTION get_userid(username text) RETURNS int
AS $$
#print_strict_params on
DECLARE
userid int;
BEGIN
    SELECT users.userid INTO STRICT userid
        FROM users WHERE users.username = get_userid.username;
    RETURN userid;
END;
$$ LANGUAGE plpgsql;
```

Em caso de falha, essa função pode produzir uma mensagem de erro, como:

```
ERROR:  query returned no rows
DETAIL:  parameters: username = 'nosuchuser'
CONTEXT:  PL/pgSQL function get_userid(text) line 6 at SQL statement
```

Nota

A opção `STRICT` corresponde ao comportamento do `SELECT INTO` do Oracle PL/SQL e das declarações relacionadas.

### 41.5.4. Executando comandos dinâmicos [#](#PLPGSQL-STATEMENTS-EXECUTING-DYN)

Muitas vezes, você vai querer gerar comandos dinâmicos dentro de suas funções PL/pgSQL, ou seja, comandos que envolverão diferentes tabelas ou diferentes tipos de dados cada vez que forem executados. As tentativas normais do PL/pgSQL de cachear planos para comandos (como discutido em [Seção 41.11.2](plpgsql-implementation.md#PLPGSQL-PLAN-CACHING)) não funcionarão em tais cenários. Para lidar com esse tipo de problema, a declaração `EXECUTE` é fornecida:

```
EXECUTE command-string [ INTO [STRICT] target ] [ USING expression [, ... ] ];
```

onde *`command-string`* é uma expressão que produz uma cadeia de caracteres (do tipo `text`) contendo o comando a ser executado. A expressão opcional *`target`* é uma variável de registro, uma variável de linha ou uma lista de separação por vírgula de variáveis simples e campos de registro/linha, na qual os resultados do comando serão armazenados. As expressões opcionais `USING` fornecem valores a serem inseridos no comando.

Nenhuma substituição de variáveis PL/pgSQL é feita na string de comando calculada. Quaisquer valores de variáveis necessários devem ser inseridos na string de comando conforme ela é construída; ou você pode usar parâmetros conforme descrito abaixo.

Além disso, não há cache para comandos executados via `EXECUTE`. Em vez disso, o comando é sempre planejado cada vez que a declaração é executada. Assim, a string de comando pode ser criada dinamicamente dentro da função para realizar ações em diferentes tabelas e colunas.

A cláusula `INTO` especifica onde os resultados de um comando SQL que retorna linhas devem ser atribuídos. Se uma variável de linha ou uma lista de variáveis for fornecida, ela deve corresponder exatamente à estrutura dos resultados do comando; se uma variável de registro for fornecida, ela se configurará para corresponder à estrutura do resultado automaticamente. Se várias linhas forem retornadas, apenas a primeira será atribuída à(s) variável(es) `INTO`. Se nenhuma linha for retornada, NULL é atribuído à(s) variável(es) `INTO`. Se não for especificada nenhuma cláusula `INTO`, os resultados do comando são descartados.

Se a opção `STRICT` for fornecida, um erro será relatado, a menos que o comando produza exatamente uma linha.

A string de comando pode usar valores de parâmetro, que são referenciados no comando como `$1`, `$2`, etc. Esses símbolos referem-se a valores fornecidos na cláusula `USING`. Esse método é frequentemente preferível a inserir valores de dados na string de comando como texto: evita o overhead de tempo de execução de conversão dos valores para texto e de volta, e é muito menos propenso a ataques de injetão SQL, uma vez que não há necessidade de citação ou escapagem. Um exemplo é:

```
EXECUTE 'SELECT count(*) FROM mytable WHERE inserted_by = $1 AND inserted <= $2'
   INTO c
   USING checked_user, checked_date;
```

Observe que os símbolos de parâmetro só podem ser usados para valores de dados — se você quiser usar nomes de tabela ou coluna determinados dinamicamente, você deve inseri-los no texto da string de comando. Por exemplo, se a consulta anterior precisasse ser feita contra uma tabela selecionada dinamicamente, você poderia fazer isso:

```
EXECUTE 'SELECT count(*) FROM '
    || quote_ident(tabname)
    || ' WHERE inserted_by = $1 AND inserted <= $2'
   INTO c
   USING checked_user, checked_date;
```

Uma abordagem mais limpa é usar a especificação `format()` de `%I` para inserir nomes de tabela ou coluna com citação automática:

```
EXECUTE format('SELECT count(*) FROM %I '
   'WHERE inserted_by = $1 AND inserted <= $2', tabname)
   INTO c
   USING checked_user, checked_date;
```

(Este exemplo depende da regra SQL de que as literais de string separadas por uma nova linha são concatenadas implicitamente.)

Outra restrição sobre os símbolos de parâmetros é que eles só funcionam em comandos SQL otimizáveis (`SELECT`, `INSERT`, `UPDATE`, `DELETE`, `MERGE` e certos comandos que contêm um desses). Em outros tipos de declarações (geralmente chamados de declarações de utilitário), você deve inserir os valores textualmente, mesmo que sejam apenas valores de dados.

Um `EXECUTE` com uma string de comando constante simples e alguns parâmetros `USING`, como no primeiro exemplo acima, é funcionalmente equivalente a escrever o comando diretamente no PL/pgSQL e permitir que a substituição de variáveis PL/pgSQL aconteça automaticamente. A diferença importante é que o `EXECUTE` replaneará o comando em cada execução, gerando um plano que é específico aos valores atuais dos parâmetros; enquanto o PL/pgSQL pode, de outra forma, criar um plano genérico e cacheá-lo para reutilização. Em situações em que o melhor plano depende fortemente dos valores dos parâmetros, pode ser útil usar o `EXECUTE` para garantir positivamente que um plano genérico não seja selecionado.

`SELECT INTO` não é atualmente suportado dentro de `EXECUTE`; em vez disso, execute um comando simples `SELECT` e especifique `INTO` como parte do próprio `EXECUTE`.

Nota

A declaração PL/pgSQL `EXECUTE` não está relacionada à declaração SQL `EXECUTE`(sql-execute.md "EXECUTE") suportada pelo servidor PostgreSQL. A declaração do servidor `EXECUTE` não pode ser usada diretamente dentro das funções PL/pgSQL (e não é necessária).

**Exemplo 41.1. Citando valores em consultas dinâmicas**

Ao trabalhar com comandos dinâmicos, você geralmente terá que lidar com a escapagem de aspas simples. O método recomendado para citar texto fixo no corpo da função é a citação em dólar. (Se você tiver código antigo que não usa citação em dólar, consulte a visão geral em [Seção 41.12.1] (https://www.postgresql.org/docs/13/sql-quote.html), que pode lhe poupar algum esforço ao traduzir o código para um esquema mais razoável.)

Os valores dinâmicos exigem um manuseio cuidadoso, pois podem conter caracteres de citação. Um exemplo usando `format()` (essa suposição assume que você está citando o corpo da função com dólar, portanto, as aspas não precisam ser duplicadas):

```
EXECUTE format('UPDATE tbl SET %I = $1 '
   'WHERE key = $2', colname) USING newvalue, keyvalue;
```

Também é possível chamar as funções de citação diretamente:

```
EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = '
        || quote_literal(newvalue)
        || ' WHERE key = '
        || quote_literal(keyvalue);
```

Este exemplo demonstra o uso das funções `quote_ident` e `quote_literal` (ver [Seção 9.4](functions-string.md)). Por segurança, as expressões que contêm identificadores de coluna ou tabela devem ser passadas através de `quote_ident` antes da inserção em uma consulta dinâmica. As expressões que contêm valores que devem ser strings literais no comando construído devem ser passadas através de `quote_literal`. Essas funções tomam as medidas apropriadas para retornar o texto de entrada fechado em aspas duplas ou simples, respectivamente, com quaisquer caracteres especiais incorporados adequadamente escapados.

Como `quote_literal` é rotulado como `STRICT`, ele sempre retornará nulo quando chamado com um argumento nulo. No exemplo acima, se `newvalue` ou `keyvalue` fossem nulos, toda a string dinâmica da consulta se tornaria nulo, levando a um erro de `EXECUTE`. Você pode evitar esse problema usando a função `quote_nullable`, que funciona da mesma forma que `quote_literal`, exceto que, quando chamada com um argumento nulo, ela retorna a string `NULL`. Por exemplo,

```
EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = '
        || quote_nullable(newvalue)
        || ' WHERE key = '
        || quote_nullable(keyvalue);
```

Se você está lidando com valores que podem ser nulos, geralmente deve usar `quote_nullable` em vez de `quote_literal`.

Como sempre, é preciso ter cuidado para garantir que os valores nulos em uma consulta não gerem resultados não intencionais. Por exemplo, a cláusula `WHERE`

```
'WHERE key = ' || quote_nullable(keyvalue)
```

não terá sucesso se `keyvalue` for nulo, porque o resultado de usar o operador de igualdade `=` com um operando nulo é sempre nulo. Se você deseja que nulo funcione como um valor de chave comum, você precisaria reescrever o acima como

```
'WHERE key IS NOT DISTINCT FROM ' || quote_nullable(keyvalue)
```

(Atualmente, `IS NOT DISTINCT FROM` é tratado muito menos eficientemente do que `=`, então não faça isso a menos que seja necessário. Consulte [Seção 9.2](functions-comparison.md "9.2. Comparison Functions and Operators") para mais informações sobre nulos e `IS DISTINCT`.])

Observe que a citação em dólares é útil apenas para citar texto fixo. Seria uma ideia muito ruim tentar escrever este exemplo como:

```
EXECUTE 'UPDATE tbl SET '
        || quote_ident(colname)
        || ' = $$'
        || newvalue
        || '$$ WHERE key = '
        || quote_literal(keyvalue);
```

porque ele quebraria se o conteúdo do `newvalue` por acaso contivesse `$$`. A mesma objeção se aplicaria a qualquer outro delimitador que citasse dólares que você pudesse escolher. Portanto, para citar com segurança um texto que não é conhecido antecipadamente, você *deve* usar `quote_literal`, `quote_nullable` ou `quote_ident`, conforme apropriado.

As instruções SQL dinâmicas também podem ser construídas com segurança usando a função `format` (consulte [Seção 9.4.1](functions-string.md#FUNCTIONS-STRING-FORMAT)). Por exemplo:

```
EXECUTE format('UPDATE tbl SET %I = %L '
   'WHERE key = %L', colname, newvalue, keyvalue);
```

`%I` é equivalente a `quote_ident`, e `%L` é equivalente a `quote_nullable`. A função `format` pode ser usada em conjunto com a cláusula `USING`:

```
EXECUTE format('UPDATE tbl SET %I = $1 WHERE key = $2', colname)
   USING newvalue, keyvalue;
```

Essa forma é melhor porque as variáveis são manipuladas em seu formato de tipo de dados nativo, em vez de convertê-las incondicionalmente para texto e cita-las via `%L`. Também é mais eficiente.



Um exemplo muito maior de um comando dinâmico e `EXECUTE` pode ser visto em [Exemplo 41.10](plpgsql-porting.md#PLPGSQL-PORTING-EX2), que constrói e executa um comando `CREATE FUNCTION` para definir uma nova função.

### 41.5.5. Obter o status do resultado [#](#PLPGSQL-STATEMENTS-DIAGNOSTICS)

Existem várias maneiras de determinar o efeito de um comando. O primeiro método é usar o comando `GET DIAGNOSTICS`, que tem a seguinte forma:

```
GET [ CURRENT ] DIAGNOSTICS variable { = | := } item [ , ... ];
```

Este comando permite a recuperação dos indicadores de status do sistema. `CURRENT` é uma palavra de ruído (mas veja também `GET STACKED DIAGNOSTICS` em [Seção 41.6.8.1](plpgsql-control-structures.md#PLPGSQL-EXCEPTION-DIAGNOSTICS "41.6.8.1. Obtaining Information about an Error")). Cada *`item`* é uma palavra-chave que identifica um valor de status a ser atribuído ao *`variable`* especificado (que deve ser do tipo de dados correto para recebê-lo). Os itens de status atualmente disponíveis são mostrados em [Tabela 41.1](plpgsql-statements.md#PLPGSQL-CURRENT-DIAGNOSTICS-VALUES "Table 41.1. Available Diagnostics Items"). O colon-igual (`:=`) pode ser usado em vez do token padrão do SQL `=`. Um exemplo:

```
GET DIAGNOSTICS integer_var = ROW_COUNT;
```

**Tabela 41.1. Itens de Diagnóstico Disponíveis**



<table border="1" class="table" summary="Available Diagnostics Items">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="varname">
     ROW_COUNT
    </code>
   </td>
   <td>
    <code class="type">
     bigint
    </code>
   </td>
   <td>
    o número de linhas processadas pelo mais recente
    <acronym class="acronym">
     SQL
    </acronym>
    comando
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PG_CONTEXT
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    linha(s) de texto descrevendo a pilha de chamadas atual (consulte
    <a class="xref" href="plpgsql-control-structures.md#PLPGSQL-CALL-STACK" title="41.6.9. Obtaining Execution Location Information">
     Seção 41.6.9
    </a>
    )
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PG_ROUTINE_OID
    </code>
   </td>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    OID da função atual
   </td>
  </tr>
 </tbody>
</table>










O segundo método para determinar os efeitos de um comando é verificar a variável especial denominada `FOUND`, que é do tipo `boolean`. `FOUND` começa como falso em cada chamada de função PL/pgSQL. É definido por cada um dos seguintes tipos de declarações:

A declaração `SELECT INTO` define `FOUND` como verdadeiro se uma linha for atribuída, falsa se nenhuma linha for retornada. A declaração `PERFORM` define `FOUND` como verdadeiro se ela produz (e descarta) uma ou mais linhas, falsa se nenhuma linha for produzida. As declarações `UPDATE`, `INSERT`, `DELETE` e `MERGE` definem `FOUND` como verdadeiro se pelo menos uma linha é afetada, falsa se nenhuma linha é afetada. A declaração `FETCH` define `FOUND` como verdadeiro se ela retorna uma linha, falsa se nenhuma linha for retornada. A declaração `MOVE` define `FOUND` como verdadeiro se ela reposiciona o cursor com sucesso, falsa de outra forma. As declarações `FOR` ou `FOREACH` definem `FOUND` como verdadeiro se ela se itera uma ou mais vezes, caso contrário falsa. `FOUND` é definido dessa forma quando o loop sai; dentro da execução do loop, `FOUND` não é modificado pela declaração do loop, embora possa ser alterado pela execução de outras declarações dentro do corpo do loop. As declarações `RETURN QUERY` e `RETURN QUERY EXECUTE` definem `FOUND` como verdadeiro se a consulta retorna pelo menos uma linha, falsa se nenhuma linha for retornada.

Outras declarações do PL/pgSQL não alteram o estado de `FOUND`. Note, em particular, que `EXECUTE` altera a saída de `GET DIAGNOSTICS`, mas não altera `FOUND`.

`FOUND` é uma variável local dentro de cada função PL/pgSQL; quaisquer alterações nela afetam apenas a função atual.

### 41.5.6. Não fazer absolutamente nada [#](#PLPGSQL-STATEMENTS-NULL)

Às vezes, uma declaração de marcador que não faz nada é útil. Por exemplo, pode indicar que um braço de uma cadeia if/then/else está deliberadamente vazio. Para esse propósito, use a declaração `NULL`:

```
NULL;
```

Por exemplo, os seguintes dois fragmentos de código são equivalentes:

```
BEGIN
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN
        NULL;  -- ignore the error
END;
```

```
BEGIN
    y := x / 0;
EXCEPTION
    WHEN division_by_zero THEN  -- ignore the error
END;
```

O que é preferível é uma questão de gosto.

Nota

No PL/SQL da Oracle, listas de declarações vazias não são permitidas, e, portanto, as declarações `NULL` são *requeridas* para situações como essa. O PL/pgSQL permite que você simplesmente não escreva nada, em vez disso.