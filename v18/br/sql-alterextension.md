## ALTER EXTENSION

ALTER EXTENSION — alterar a definição de uma extensão

## Sinopse

```
ALTER EXTENSION name UPDATE [ TO new_version ]
ALTER EXTENSION name SET SCHEMA new_schema
ALTER EXTENSION name ADD member_object
ALTER EXTENSION name DROP member_object

where member_object is:

  ACCESS METHOD object_name |
  AGGREGATE aggregate_name ( aggregate_signature ) |
  CAST (source_type AS target_type) |
  COLLATION object_name |
  CONVERSION object_name |
  DOMAIN object_name |
  EVENT TRIGGER object_name |
  FOREIGN DATA WRAPPER object_name |
  FOREIGN TABLE object_name |
  FUNCTION function_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  MATERIALIZED VIEW object_name |
  OPERATOR operator_name (left_type, right_type) |
  OPERATOR CLASS object_name USING index_method |
  OPERATOR FAMILY object_name USING index_method |
  [ PROCEDURAL ] LANGUAGE object_name |
  PROCEDURE procedure_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  ROUTINE routine_name [ ( [ [ argmode ] [ argname ] argtype [, ...] ] ) ] |
  SCHEMA object_name |
  SEQUENCE object_name |
  SERVER object_name |
  TABLE object_name |
  TEXT SEARCH CONFIGURATION object_name |
  TEXT SEARCH DICTIONARY object_name |
  TEXT SEARCH PARSER object_name |
  TEXT SEARCH TEMPLATE object_name |
  TRANSFORM FOR type_name LANGUAGE lang_name |
  TYPE object_name |
  VIEW object_name

and aggregate_signature is:

* |
[ argmode ] [ argname ] argtype [ , ... ] |
[ [ argmode ] [ argname ] argtype [ , ... ] ] ORDER BY [ argmode ] [ argname ] argtype [ , ... ]
```

## Descrição

`ALTER EXTENSION` altera a definição de uma extensão instalada. Existem vários subformularios:

`UPDATE`: Este formulário atualiza a extensão para uma versão mais recente. A extensão deve fornecer um script de atualização adequado (ou uma série de scripts) que possa modificar a versão instalada atualmente na versão solicitada.

`SET SCHEMA`: Este formulário move os objetos da extensão para outro esquema. A extensão precisa ser *relocável* para que este comando seja bem-sucedido.

`ADD member_object`: Este formulário adiciona um objeto existente à extensão. Isso é principalmente útil em scripts de atualização de extensão. O objeto será posteriormente tratado como um membro da extensão; notavelmente, ele só pode ser descartado ao descarregar a extensão.

`DROP member_object`: Este formulário remove um objeto de extensão do membro. Isso é principalmente útil em scripts de atualização de extensão. O objeto não é descartado, apenas desassociado da extensão.

Consulte a [Seção 36.17][(extend-extensions.md "36.17. Packaging Related Objects into an Extension")] para obter mais informações sobre essas operações.

Você deve possuir a extensão para usar `ALTER EXTENSION`. Os formulários `ADD`/`DROP` também exigem a posse do objeto adicionado/removido.

## Parâmetros

*`name`*: O nome de uma extensão instalada.

*`new_version`*: A nova versão desejada da extensão. Isso pode ser escrito como um identificador ou uma literal de string. Se não especificado, `ALTER EXTENSION UPDATE` tenta atualizar para o que é mostrado como a versão padrão no arquivo de controle da extensão.

*`new_schema`*: O novo esquema para a extensão.

*`object_name`* *`aggregate_name`* *`function_name`* *`operator_name`* *`procedure_name`* *`routine_name`*: O nome de um objeto que será adicionado ou removido da extensão. Os nomes de tabelas, agregados, domínios, tabelas externas, funções, operadores, classes de operadores, famílias de operadores, procedimentos, rotinas, objetos de pesquisa de texto, tipos e visualizações podem ser qualificados pelo esquema.

*`source_type`*: O nome do tipo de dados fonte do cast.

*`target_type`*: O nome do tipo de dados de destino do cast.

*`argmode`*: O modo de uma função, procedimento ou argumento agregado: `IN`, `OUT`, `INOUT` ou `VARIADIC`. Se omitido, o padrão é `IN`. Note que `ALTER EXTENSION` não presta atenção na verdade em argumentos `OUT`, uma vez que apenas os argumentos de entrada são necessários para determinar a identidade da função. Portanto, é suficiente listar os argumentos `IN`, `INOUT` e `VARIADIC`.

*`argname`*: O nome de uma função, procedimento ou argumento agregado. Observe que `ALTER EXTENSION` não presta atenção na verdade aos nomes dos argumentos, uma vez que apenas os tipos de dados dos argumentos são necessários para determinar a identidade da função.

*`argtype`*: O tipo de dados de uma função, procedimento ou argumento agregado.

*`left_type`* *`right_type`*: O(s) tipo(s) de dados dos argumentos do operador (opcionalmente qualificados pelo esquema). Escreva `NONE` para o argumento ausente de um operador prefixo.

`PROCEDURAL`: Esta é uma palavra de ruído.

*`type_name`*: O nome do tipo de dados do transformador.

*`lang_name`*: O nome da língua do transformador.

## Exemplos

Para atualizar a extensão `hstore` para a versão 2.0:

```
ALTER EXTENSION hstore UPDATE TO '2.0';
```

Para alterar o esquema da extensão `hstore` para `utils`:

```
ALTER EXTENSION hstore SET SCHEMA utils;
```

Para adicionar uma função existente à extensão `hstore`:

```
ALTER EXTENSION hstore ADD FUNCTION populate_record(anyelement, hstore);
```

## Compatibilidade

`ALTER EXTENSION` é uma extensão do PostgreSQL.

## Veja também

[CREATE EXTENSION](sql-createextension.md "CREATE EXTENSION"), [DROP EXTENSION](sql-dropextension.md "DROP EXTENSION")