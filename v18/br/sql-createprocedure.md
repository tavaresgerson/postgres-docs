## Crie o procedimento

Crie procedimento — defina um novo procedimento

## Sinopse

```
CREATE [ OR REPLACE ] PROCEDURE
    name ( [ [ argmode ] [ argname ] argtype [ { DEFAULT | = } default_expr ] [, ...] ] )
  { LANGUAGE lang_name
    | TRANSFORM { FOR TYPE type_name } [, ... ]
    | [ EXTERNAL ] SECURITY INVOKER | [ EXTERNAL ] SECURITY DEFINER
    | SET configuration_parameter { TO value | = value | FROM CURRENT }
    | AS 'definition'
    | AS 'obj_file', 'link_symbol'
    | sql_body
  } ...
```

## Descrição

`CREATE PROCEDURE` define um novo procedimento. `CREATE OR REPLACE PROCEDURE` irá criar um novo procedimento ou substituir uma definição existente. Para poder definir um procedimento, o usuário deve ter o privilégio `USAGE` na língua.

Se um nome de esquema for incluído, o procedimento será criado no esquema especificado. Caso contrário, será criado no esquema atual. O nome do novo procedimento não deve corresponder a nenhum procedimento ou função existente com os mesmos tipos de argumentos de entrada no mesmo esquema. No entanto, procedimentos e funções de diferentes tipos de argumentos podem compartilhar um nome (isso é chamado de *sobrecarga*).

Para substituir a definição atual de um procedimento existente, use `CREATE OR REPLACE PROCEDURE`. Não é possível alterar o nome ou os tipos de argumentos de um procedimento dessa forma (se você tentasse, na verdade, você criaria um procedimento novo e distinto).

Quando o `CREATE OR REPLACE PROCEDURE` é usado para substituir um procedimento existente, a propriedade e as permissões do procedimento não mudam. Todas as outras propriedades do procedimento recebem os valores especificados ou implícitos no comando. Você deve possuir o procedimento para substituí-lo (isso inclui ser membro do papel de proprietário).

O usuário que cria o procedimento se torna o proprietário do procedimento.

Para criar um procedimento, você deve ter o privilégio `USAGE` nos tipos de argumentos.

Consulte [Seção 36.4][(xproc.md "36.4. User-Defined Procedures")] para obter informações adicionais sobre os procedimentos de escrita.

## Parâmetros

*`name`*: O nome (opcionalmente qualificado por esquema) do procedimento a ser criado.

*`argmode`*: O modo de um argumento: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`.

*`argname`*: O nome de um argumento.

*`argtype`*: O(s) tipo(s) de dados dos argumentos do procedimento (opcionalmente qualificados por esquema), se houver. Os tipos de argumento podem ser base, composto ou tipos de domínio, ou podem referenciar o tipo de uma coluna de tabela.

Dependendo do idioma de implementação, também pode ser permitido especificar “pseudo-tipos”, como `cstring`. Pseudo-tipos indicam que o tipo de argumento real é incompletamente especificado ou está fora do conjunto de tipos de dados SQL comuns.

O tipo de uma coluna é referenciado escrevendo `table_name.column_name%TYPE`. O uso desse recurso pode, às vezes, ajudar a tornar um procedimento independente das mudanças na definição de uma tabela.

*`default_expr`*: Uma expressão que deve ser usada como valor padrão se o parâmetro não for especificado. A expressão deve ser coerente com o tipo de argumento do parâmetro. Todos os parâmetros de entrada que seguem um parâmetro com um valor padrão devem ter valores padrão também.

*`lang_name`*: O nome da linguagem na qual o procedimento é implementado. Pode ser `sql`, `c`, `internal`, ou o nome de uma linguagem procedural definida pelo usuário, por exemplo, `plpgsql`. O padrão é `sql` se *`sql_body`* for especificado. Enquadrar o nome em aspas é desaconselhável e requer correspondência de caso.

`TRANSFORM { FOR TYPE type_name } [, ... ] }`: Lista as transformações que devem ser aplicadas a uma chamada ao procedimento. As transformações convertem entre tipos SQL e tipos de dados específicos do idioma; consulte [CREATE TRANSFORM](sql-createtransform.md "CREATE TRANSFORM"). As implementações de linguagens procedimentais geralmente têm conhecimento pré-codificado dos tipos embutidos, portanto, esses não precisam ser listados aqui. Se uma implementação de linguagem procedural não souber como lidar com um tipo e nenhum transformação for fornecida, ela retornará um comportamento padrão para a conversão de tipos de dados, mas isso depende da implementação.

`[EXTERNAL] SECURITY INVOKER` `[EXTERNAL] SECURITY DEFINER`: `SECURITY INVOKER` indica que o procedimento deve ser executado com os privilégios do usuário que o chama. Isso é o padrão. `SECURITY DEFINER` especifica que o procedimento deve ser executado com os privilégios do usuário que o possui.

A palavra-chave `EXTERNAL` é permitida para conformidade com SQL, mas é opcional, pois, ao contrário do que acontece com o SQL, essa funcionalidade se aplica a todos os procedimentos, não apenas aos externos.

Um procedimento `SECURITY DEFINER` não pode executar instruções de controle de transação (por exemplo, `COMMIT` e `ROLLBACK`, dependendo do idioma).

*`configuration_parameter`* *`value`*: A cláusula `SET` faz com que o parâmetro de configuração especificado seja definido pelo valor especificado quando o procedimento é iniciado e, em seguida, restaurado ao seu valor anterior quando o procedimento é encerrado. `SET FROM CURRENT` salva o valor do parâmetro que é atual quando `CREATE PROCEDURE` é executado como o valor a ser aplicado quando o procedimento é iniciado.

Se uma cláusula `SET` estiver anexada a um procedimento, os efeitos de um comando `SET LOCAL` executado dentro do procedimento para a mesma variável são restritos ao procedimento: o valor anterior do parâmetro de configuração ainda é restaurado na saída do procedimento. No entanto, um comando `SET` comum (sem `LOCAL`) substitui a cláusula `SET`, assim como faria para um comando anterior `SET LOCAL`: os efeitos de tal comando persistirão após a saída do procedimento, a menos que a transação atual seja revertida.

Se uma cláusula `SET` estiver anexada a um procedimento, então esse procedimento não pode executar declarações de controle de transação (por exemplo, `COMMIT` e `ROLLBACK`, dependendo do idioma).

Consulte [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para obter mais informações sobre os nomes e valores permitidos dos parâmetros.

*`definition`*: Uma constante de cadeia que define o procedimento; o significado depende do idioma. Pode ser o nome de um procedimento interno, o caminho de um arquivo de objeto, um comando SQL ou texto em uma linguagem procedural.

É frequentemente útil usar citação em dólares (consulte [Seção 4.1.2.4][(sql-syntax-lexical.md#SQL-SYNTAX-DOLLAR-QUOTING "4.1.2.4. Dollar-Quoted String Constants")]) para escrever a string de definição do procedimento, em vez da sintaxe normal de citação simples. Sem citação em dólares, quaisquer citações simples ou barras invertidas na definição do procedimento devem ser escapadas duplicando-as.

`obj_file, link_symbol`: Esta forma da cláusula `AS` é usada para procedimentos dinamicamente carregáveis em linguagem C, quando o nome do procedimento no código-fonte da linguagem C não é o mesmo que o nome do procedimento SQL. A string *`obj_file`* é o nome do arquivo da biblioteca compartilhada que contém o procedimento C compilado, e é interpretada como para o comando [`LOAD`(sql-load.md "LOAD")]. A string *`link_symbol`* é o símbolo de ligação do procedimento, ou seja, o nome do procedimento no código-fonte da linguagem C. Se o símbolo de ligação for omitido, presume-se que seja o mesmo que o nome do procedimento SQL sendo definido.

Quando chamadas `CREATE PROCEDURE` repetidas referem-se ao mesmo arquivo de objeto, o arquivo é carregado apenas uma vez por sessão. Para descarregar e recarregar o arquivo (talvez durante o desenvolvimento), inicie uma nova sessão.

*`sql_body`*: O corpo de um procedimento `LANGUAGE SQL`. Isso deve ser um bloco

``` BEGIN ATOMIC statement; statement; ... statement; END
    ```

Isso é semelhante a escrever o texto do corpo do procedimento como uma constante de string (veja *`definition`* acima), mas há algumas diferenças: Este formulário só funciona para `LANGUAGE SQL`, a forma de constante de string funciona para todos os idiomas. Este formulário é analisado no momento da definição do procedimento, a forma de constante de string é analisada no momento da execução; portanto, este formulário não pode suportar tipos de argumentos polimórficos e outras construções que não sejam resolvíveis no momento da definição do procedimento. Este formulário rastreia as dependências entre o procedimento e os objetos usados no corpo do procedimento, então `DROP ... CASCADE` funcionará corretamente, enquanto o formulário que usa literais de string pode deixar procedimentos pendentes. Finalmente, este formulário é mais compatível com o padrão SQL e outras implementações SQL.

## Notas

Veja [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION") para mais detalhes sobre a criação de funções que também se aplicam a procedimentos.

Use [CALL](sql-call.md "CALL") para executar um procedimento.

## Exemplos

```
CREATE PROCEDURE insert_data(a integer, b integer) LANGUAGE SQL AS $$ INSERT INTO tbl VALUES (a); INSERT INTO tbl VALUES (b); $$;
```

ou

```
CREATE PROCEDURE insert_data(a integer, b integer) LANGUAGE SQL BEGIN ATOMIC INSERT INTO tbl VALUES (a); INSERT INTO tbl VALUES (b); END;
```

e ligue assim:

```
CALL insert_data(1, 2);
```

## Compatibilidade

Um comando `CREATE PROCEDURE` é definido no padrão SQL. A implementação do PostgreSQL pode ser usada de maneira compatível, mas possui muitas extensões. Para detalhes, consulte também [CREATE FUNCTION][(sql-createfunction.md "CREATE FUNCTION")].

## Veja também

[ALTER PROCEDURE](sql-alterprocedure.md "ALTER PROCEDURE"), [DROP PROCEDURE](sql-dropprocedure.md "DROP PROCEDURE"), [CALL](sql-call.md "CALL"), [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION")