## Crie Transformação

Crie TRANSFORM — defina uma nova transformação

## Sinopse

```
CREATE [ OR REPLACE ] TRANSFORM FOR type_name LANGUAGE lang_name (
    FROM SQL WITH FUNCTION from_sql_function_name [ (argument_type [, ...]) ],
    TO SQL WITH FUNCTION to_sql_function_name [ (argument_type [, ...]) ]
);
```

## Descrição

`CREATE TRANSFORM` define uma nova transformação. `CREATE OR REPLACE TRANSFORM` irá criar uma nova transformação ou substituir uma definição existente.

Uma transformação especifica como adaptar um tipo de dados a uma linguagem procedural. Por exemplo, ao escrever uma função em PL/Python usando o tipo `hstore`, o PL/Python não tem conhecimento prévio sobre como apresentar os valores `hstore` no ambiente Python. As implementações de linguagem geralmente optam por usar a representação textual, mas isso é inconveniente quando, por exemplo, um array associativo ou uma lista seria mais apropriado.

Uma transformação especifica duas funções:

* Uma função "de SQL" que converte o tipo do ambiente SQL para a linguagem. Esta função será invocada nos argumentos de uma função escrita na linguagem. * Uma função "para SQL" que converte o tipo da linguagem para o ambiente SQL. Esta função será invocada no valor de retorno de uma função escrita na linguagem.

Não é necessário fornecer ambas essas funções. Se uma delas não for especificada, o comportamento padrão específico para a linguagem será usado, se necessário. (Para evitar que uma transformação em uma certa direção aconteça, você também pode escrever uma função de transformação que sempre falhe.)

Para poder criar uma transformação, você deve possuir e ter privilégio `USAGE` no tipo, ter privilégio `USAGE` na língua e possuir e ter privilégio `EXECUTE` nas funções de from-SQL e to-SQL, se especificadas.

## Parâmetros

*`type_name`*: O nome do tipo de dados do transformador.

*`lang_name`*: O nome da língua do transformador.

`from_sql_function_name[(argument_type [, ...])]`: O nome da função para converter o tipo do ambiente SQL para a linguagem. Deve receber um argumento do tipo `internal` e retornar o tipo `internal`. O argumento real será do tipo para a transformação, e a função deve ser codificada como se fosse. (Mas não é permitido declarar uma função de nível SQL que retorne `internal` sem pelo menos um argumento do tipo `internal`.). O valor de retorno real será algo específico para a implementação da linguagem. Se não for especificada uma lista de argumentos, o nome da função deve ser único em seu esquema.

`to_sql_function_name[(argument_type [, ...])]`: O nome da função para converter o tipo da linguagem para o ambiente SQL. Deve receber um argumento do tipo `internal` e retornar o tipo que é o tipo para a transformação. O valor do argumento real será algo específico para a implementação da linguagem. Se nenhuma lista de argumentos for especificada, o nome da função deve ser único em seu esquema.

## Notas

Use `DROP TRANSFORM`(sql-droptransform.md "DROP TRANSFORM") para remover transformações.

## Exemplos

Para criar uma transformação para o tipo `hstore` e idioma `plpython3u`, configure primeiro o tipo e o idioma:

```
CREATE TYPE hstore ...;

CREATE EXTENSION plpython3u;
```

Em seguida, crie as funções necessárias:

```
CREATE FUNCTION hstore_to_plpython(val internal) RETURNS internal
LANGUAGE C STRICT IMMUTABLE
AS ...;

CREATE FUNCTION plpython_to_hstore(val internal) RETURNS hstore
LANGUAGE C STRICT IMMUTABLE
AS ...;
```

E, por fim, crie a transformação para conectá-los todos juntos:

```
CREATE TRANSFORM FOR hstore LANGUAGE plpython3u (
    FROM SQL WITH FUNCTION hstore_to_plpython(internal),
    TO SQL WITH FUNCTION plpython_to_hstore(internal)
);
```

Na prática, esses comandos seriam encapsulados em uma extensão.

A seção `contrib` contém uma série de extensões que fornecem transformações, que podem servir como exemplos do mundo real.

## Compatibilidade

Essa forma de `CREATE TRANSFORM` é uma extensão do PostgreSQL. Há um comando `CREATE TRANSFORM` no padrão SQL, mas ele é para adaptar tipos de dados aos idiomas do cliente. Esse uso não é suportado pelo PostgreSQL.

## Veja também

[Crie função](sql-createfunction.md "CREATE FUNCTION"), [Crie linguagem](sql-createlanguage.md "CREATE LANGUAGE"), [Crie tipo](sql-createtype.md "CREATE TYPE"), [Exclua transformação](sql-droptransform.md "DROP TRANSFORM")