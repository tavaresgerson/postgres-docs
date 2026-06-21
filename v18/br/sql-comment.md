## COMENTÁRIO

COMENTÁRIO — definir ou alterar o comentário de um objeto

## Sinopse

```
COMMENT ON
{
  ACCESS METHOD object_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  CAST (source_type AS target_type) |
  COLLATION object_name |
  COLUMN relation_name.column_name |
  CONSTRAINT constraint_name ON table_name |
  CONSTRAINT constraint_name ON DOMAIN domain_name |
  CONVERSION object_name |
  DATABASE object_name |
  DOMAIN object_name |
  EXTENSION object_name |
  EVENT TRIGGER object_name |
  FOREIGN DATA WRAPPER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  INDEX object_name |
  LARGE OBJECT large_object_oid |
  MATERIALIZED VIEW object_name |
  OPERATOR operator_name (left_type, right_type) |
  OPERATOR CLASS object_name USING index_method |
  OPERATOR FAMILY object_name USING index_method |
  POLICY policy_name ON table_name |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  PUBLICATION object_name |
  ROLE object_name |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  RULE rule_name ON table_name |
  SCHEMA object_name |
  SEQUENCE object_name |
  SERVER object_name |
  STATISTICS object_name |
  SUBSCRIPTION object_name |
  TABLE object_name |
  TABLESPACE object_name |
  TEXT SEARCH CONFIGURATION object_name |
  TEXT SEARCH DICTIONARY object_name |
  TEXT SEARCH PARSER object_name |
  TEXT SEARCH TEMPLATE object_name |
  TRANSFORM FOR type_name LANGUAGE lang_name |
  TRIGGER trigger_name ON table_name |
  TYPE object_name |
  VIEW object_name
} IS { string_literal | NULL }

where aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## Descrição

`COMMENT` armazena, substitui ou remove o comentário de um objeto de banco de dados.

Apenas uma cadeia de comentário é armazenada para cada objeto. Emitir um novo comando `COMMENT` para o mesmo objeto substitui o comentário existente. Especificar `NULL` ou uma cadeia vazia (`''`) remove o comentário. Os comentários são automaticamente descartados quando seu objeto é descartado.

Um bloqueio `SHARE UPDATE EXCLUSIVE` é adquirido no objeto que será comentado.

Para a maioria dos tipos de objeto, apenas o proprietário do objeto pode definir o comentário. Os papéis não têm proprietários, portanto, a regra para `COMMENT ON ROLE` é que você deve ser um superusuário para comentar em um papel de superusuário, ou ter o privilégio `CREATEROLE` e ter sido concedido `ADMIN OPTION` no papel alvo. Da mesma forma, os métodos de acesso também não têm proprietários; você deve ser um superusuário para comentar em um método de acesso. Claro, um superusuário pode comentar sobre qualquer coisa.

Os comentários podem ser visualizados usando a família de comandos `\d` do psql. Outras interfaces de usuário para recuperar comentários podem ser construídas sobre as mesmas funções embutidas que o psql usa, ou seja, `obj_description`, `col_description` e `shobj_description` (consulte [Tabela 9.82](functions-info.md#FUNCTIONS-INFO-COMMENT-TABLE)).

## Parâmetros

*`object_name`* *`relation_name`*.*`column_name`* *`aggregate_name`* *`constraint_name`* *`function_name`* *`operator_name`* *`policy_name`* *`procedure_name`* *`routine_name`* *`rule_name`* *`trigger_name`*: O nome do objeto a ser comentado. Os nomes dos objetos que residem em esquemas (tabelas, funções, etc.) podem ser qualificados por esquema. Ao comentar sobre uma coluna, *`relation_name`* deve se referir a uma tabela, visão, tipo composto ou tabela externa.

*`table_name`* *`domain_name`*: Ao criar um comentário sobre uma restrição, um gatilho, uma regra ou uma política, esses parâmetros especificam o nome da tabela ou domínio sobre o qual esse objeto é definido.

*`source_type`*: O nome do tipo de dados fonte do cast.

*`target_type`*: O nome do tipo de dados de destino do cast.

*`argmode`*: O modo de uma função, procedimento ou argumento agregado: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Note que `COMMENT` não presta atenção na verdade em argumentos `OUT`, uma vez que apenas os argumentos de entrada são necessários para determinar a identidade da função. Portanto, é suficiente listar os argumentos `IN`, `INOUT` e `VARIADIC`.

*`argname`*: O nome de uma função, procedimento ou argumento agregado. Observe que `COMMENT` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função.

*`argtype`*: O tipo de dados de uma função, procedimento ou argumento agregado.

*`large_object_oid`*: O OID do grande objeto.

*`left_type`* *`right_type`*: O(s) tipo(s) de dados dos argumentos do operador (opcionalmente qualificados por esquema). Escreva `NONE` para o argumento ausente de um operador prefixo.

`PROCEDURAL`: Esta é uma palavra de ruído.

*`type_name`*: O nome do tipo de dados do transformador.

*`lang_name`*: O nome da língua do transformador.

*`string_literal`*: O novo conteúdo do comentário, escrito como uma literal de string. Uma string vazia (`''`) remove o comentário.

`NULL`: Escreva `NULL` para remover o comentário.

## Notas

Atualmente, não há mecanismo de segurança para visualizar comentários: qualquer usuário conectado a um banco de dados pode ver todos os comentários dos objetos nesse banco de dados. Para objetos compartilhados, como bancos de dados, papéis e espaços de tabela, os comentários são armazenados globalmente, de modo que qualquer usuário conectado a qualquer banco de dados do clúster pode ver todos os comentários dos objetos compartilhados. Portanto, não coloque informações críticas à segurança em comentários.

## Exemplos

Adicione um comentário à tabela `mytable`:

```
COMMENT ON TABLE mytable IS 'This is my table.';
```

Remova-o novamente:

```
COMMENT ON TABLE mytable IS NULL;
```

Alguns exemplos mais:

```
COMMENT ON ACCESS METHOD gin IS 'GIN index access method';
COMMENT ON AGGREGATE my_aggregate (double precision) IS 'Computes sample variance';
COMMENT ON CAST (text AS int4) IS 'Allow casts from text to int4';
COMMENT ON COLLATION "fr_CA" IS 'Canadian French';
COMMENT ON COLUMN my_table.my_column IS 'Employee ID number';
COMMENT ON CONVERSION my_conv IS 'Conversion to UTF8';
COMMENT ON CONSTRAINT bar_col_cons ON bar IS 'Constrains column col';
COMMENT ON CONSTRAINT dom_col_constr ON DOMAIN dom IS 'Constrains col of domain';
COMMENT ON DATABASE my_database IS 'Development Database';
COMMENT ON DOMAIN my_domain IS 'Email Address Domain';
COMMENT ON EVENT TRIGGER abort_ddl IS 'Aborts all DDL commands';
COMMENT ON EXTENSION hstore IS 'implements the hstore data type';
COMMENT ON FOREIGN DATA WRAPPER mywrapper IS 'my foreign data wrapper';
COMMENT ON FOREIGN TABLE my_foreign_table IS 'Employee Information in other database';
COMMENT ON FUNCTION my_function (timestamp) IS 'Returns Roman Numeral';
COMMENT ON INDEX my_index IS 'Enforces uniqueness on employee ID';
COMMENT ON LANGUAGE plpython IS 'Python support for stored procedures';
COMMENT ON LARGE OBJECT 346344 IS 'Planning document';
COMMENT ON MATERIALIZED VIEW my_matview IS 'Summary of order history';
COMMENT ON OPERATOR ^ (text, text) IS 'Performs intersection of two texts';
COMMENT ON OPERATOR - (NONE, integer) IS 'Unary minus';
COMMENT ON OPERATOR CLASS int4ops USING btree IS '4 byte integer operators for btrees';
COMMENT ON OPERATOR FAMILY integer_ops USING btree IS 'all integer operators for btrees';
COMMENT ON POLICY my_policy ON mytable IS 'Filter rows by users';
COMMENT ON PROCEDURE my_proc (integer, integer) IS 'Runs a report';
COMMENT ON PUBLICATION alltables IS 'Publishes all operations on all tables';
COMMENT ON ROLE my_role IS 'Administration group for finance tables';
COMMENT ON ROUTINE my_routine (integer, integer) IS 'Runs a routine (which is a function or procedure)';
COMMENT ON RULE my_rule ON my_table IS 'Logs updates of employee records';
COMMENT ON SCHEMA my_schema IS 'Departmental data';
COMMENT ON SEQUENCE my_sequence IS 'Used to generate primary keys';
COMMENT ON SERVER myserver IS 'my foreign server';
COMMENT ON STATISTICS my_statistics IS 'Improves planner row estimations';
COMMENT ON SUBSCRIPTION alltables IS 'Subscription for all operations on all tables';
COMMENT ON TABLE my_schema.my_table IS 'Employee Information';
COMMENT ON TABLESPACE my_tablespace IS 'Tablespace for indexes';
COMMENT ON TEXT SEARCH CONFIGURATION my_config IS 'Special word filtering';
COMMENT ON TEXT SEARCH DICTIONARY swedish IS 'Snowball stemmer for Swedish language';
COMMENT ON TEXT SEARCH PARSER my_parser IS 'Splits text into words';
COMMENT ON TEXT SEARCH TEMPLATE snowball IS 'Snowball stemmer';
COMMENT ON TRANSFORM FOR hstore LANGUAGE plpython3u IS 'Transform between hstore and Python dict';
COMMENT ON TRIGGER my_trigger ON my_table IS 'Used for RI';
COMMENT ON TYPE complex IS 'Complex number data type';
COMMENT ON VIEW my_view IS 'View of departmental costs';
COMMENT ON VIEW my_view IS NULL;
```

## Compatibilidade

Não existe comando `COMMENT` no padrão SQL.