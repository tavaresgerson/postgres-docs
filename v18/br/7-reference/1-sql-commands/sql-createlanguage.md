## Crie a linguagem

Crie linguagem — defina uma nova linguagem procedural

## Sinopse

```
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
    HANDLER call_handler [ INLINE inline_handler ] [ VALIDATOR valfunction ]
CREATE [ OR REPLACE ] [ TRUSTED ] [ PROCEDURAL ] LANGUAGE name
```

## Descrição

`CREATE LANGUAGE` registra uma nova linguagem procedural em um banco de dados PostgreSQL. Posteriormente, funções e procedimentos podem ser definidos nessa nova linguagem.

`CREATE LANGUAGE` associa efetivamente o nome da linguagem com a(s) função(ões) de manipulação que são responsáveis por executar funções escritas na linguagem. Consulte o [Capítulo 57](plhandler.md) para obter mais informações sobre manipuladores de linguagem.

`CREATE OR REPLACE LANGUAGE` criará uma nova linguagem ou substituirá uma definição existente. Se a linguagem já existir, seus parâmetros são atualizados de acordo com o comando, mas as configurações de propriedade e permissões da linguagem não são alteradas, e quaisquer funções existentes escritas na linguagem são assumidas como válidas.

É necessário ter o privilégio de superusuário do PostgreSQL para registrar uma nova língua ou alterar os parâmetros de uma língua existente. No entanto, uma vez que a língua é criada, é válido atribuir a propriedade dela a um usuário que não seja um superusuário, que pode, então, descartá-la, alterar suas permissões, renomeá-la ou atribuí-la a um novo proprietário. (No entanto, não atribua a propriedade das funções C subjacentes a um usuário que não seja um superusuário; isso criaria um caminho de escalada de privilégios para esse usuário.)

O formato do `CREATE LANGUAGE` que não fornece nenhuma função de manipulador é obsoleto. Para compatibilidade reversa com arquivos antigos de depuração, ele é interpretado como `CREATE EXTENSION`. Isso funcionará se a linguagem tiver sido embalada em uma extensão com o mesmo nome, que é a maneira convencional de configurar linguagens procedimentais.

## Parâmetros

`TRUSTED`: `TRUSTED` especifica que a linguagem não concede acesso a dados que o usuário não teria de outra forma. Se essa palavra-chave for omitida ao registrar a linguagem, apenas os usuários com privilégio de superusuário do PostgreSQL podem usar essa linguagem para criar novas funções.

`PROCEDURAL`: Esta é uma palavra de ruído.

*`name`*: O nome do novo idioma processual. O nome deve ser único entre os idiomas na base de dados.

`HANDLER` *`call_handler`*: *`call_handler`* é o nome de uma função previamente registrada que será chamada para executar as funções do idioma procedural. O manipulador de chamada para um idioma procedural deve ser escrito em uma linguagem compilada, como C, com convenção de chamada da versão 1 e registrado no PostgreSQL como uma função que não recebe argumentos e retorna o tipo `language_handler`, um tipo de marcador que é simplesmente usado para identificar a função como um manipulador de chamada.

`INLINE` *`inline_handler`*: *`inline_handler`* é o nome de uma função previamente registrada que será chamada para executar um bloco de código anônimo (comando [`DO`](sql-do.md "DO")) neste idioma. Se nenhuma função *`inline_handler`* for especificada, o idioma não suporta blocos de código anônimos. A função de manipulador deve receber um argumento do tipo `internal`, que será a representação interna do comando `DO`, e geralmente retornará `void`. O valor de retorno do manipulador é ignorado.

`VALIDATOR` *`valfunction`*: *`valfunction`* é o nome de uma função previamente registrada que será chamada quando uma nova função no idioma for criada, para validar a nova função. Se nenhuma função validadora for especificada, então uma nova função não será verificada quando for criada. A função validadora deve receber um argumento do tipo `oid`, que será o OID da função a ser criada, e normalmente retornará `void`.

Uma função de validação normalmente inspeciona o corpo da função em busca de correção sintática, mas também pode analisar outras propriedades da função, por exemplo, se a linguagem não pode lidar com certos tipos de argumentos. Para sinalizar um erro, a função de validação deve usar a função `ereport()`. O valor de retorno da função é ignorado.

## Notas

Use `DROP LANGUAGE`(sql-droplanguage.md "DROP LANGUAGE") para descartar linguagens processuais.

O catálogo do sistema `pg_language` (consulte [Seção 52.29](catalog-pg-language.md)) registra informações sobre os idiomas instalados atualmente. Além disso, o comando psql `\dL` lista os idiomas instalados.

Para criar funções em uma linguagem procedural, o usuário deve ter o privilégio `USAGE` para a linguagem. Por padrão, `USAGE` é concedido a `PUBLIC` (ou seja, a todos) para linguagens confiáveis. Isso pode ser revogado, se desejado.

As linguagens processuais são locais para bancos de dados individuais. No entanto, uma linguagem pode ser instalada no banco de dados `template1`, o que fará com que ela esteja disponível automaticamente em todos os bancos de dados posteriormente criados.

## Exemplos

Uma sequência mínima para criar uma nova linguagem procedural é:

```
CREATE FUNCTION plsample_call_handler() RETURNS language_handler
    AS '$libdir/plsample'
    LANGUAGE C;
CREATE LANGUAGE plsample
    HANDLER plsample_call_handler;
```

Normalmente, isso seria escrito em um script de criação de extensão, e os usuários fariam isso para instalar a extensão:

```
CREATE EXTENSION plsample;
```

## Compatibilidade

`CREATE LANGUAGE` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR LINGUAGEM](sql-alterlanguage.md "ALTER LANGUAGE"), [Criação de FUNÇÃO](sql-createfunction.md "CREATE FUNCTION"), [Eliminação de LINGUAGEM](sql-droplanguage.md "DROP LANGUAGE"), [CONCEDIMENTO](sql-grant.md "GRANT"), [RETIRO](sql-revoke.md "REVOKE")