## Crie o esquema

CREATE SCHEMA — definir um novo esquema

## Sinopse

```
CREATE SCHEMA schema_name [ AUTHORIZATION role_specification ] [ schema_element [ ... ] ]
CREATE SCHEMA AUTHORIZATION role_specification [ schema_element [ ... ] ]
CREATE SCHEMA IF NOT EXISTS schema_name [ AUTHORIZATION role_specification ]
CREATE SCHEMA IF NOT EXISTS AUTHORIZATION role_specification

where role_specification can be:

    user_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

## Descrição

`CREATE SCHEMA` insere um novo esquema no banco de dados atual. O nome do esquema deve ser distinto do nome de qualquer esquema existente no banco de dados atual.

Um esquema é essencialmente um espaço de nomes: ele contém objetos nomeados (tabelas, tipos de dados, funções e operadores) cujos nomes podem duplicar os de outros objetos existentes em outros esquemas. Os objetos nomeados são acessados ou qualificando seus nomes com o nome do esquema como prefixo, ou definindo um caminho de busca que inclui o(s) esquema(s) desejado(s). Um comando `CREATE` que especifica um nome de objeto não qualificado cria o objeto no esquema atual (o que está na frente do caminho de busca, que pode ser determinado com a função `current_schema`).

Opcionalmente, `CREATE SCHEMA` pode incluir subcomandos para criar objetos dentro do novo esquema. Os subcomandos são tratados essencialmente da mesma forma que comandos separados emitidos após a criação do esquema, exceto que, se a cláusula `AUTHORIZATION` for usada, todos os objetos criados serão de propriedade desse usuário.

## Parâmetros

*`schema_name`*: O nome do esquema a ser criado. Se isso for omitido, o *`user_name`* é usado como nome do esquema. O nome não pode começar com `pg_`, pois tais nomes são reservados para esquemas do sistema.

*`user_name`*: O nome do papel do usuário que possuirá o novo esquema. Se omitido, o padrão é o usuário que executa o comando. Para criar um esquema possuído por outro papel, você deve ser capaz de `SET ROLE` para esse papel.

*`schema_element`*: Uma declaração SQL que define um objeto a ser criado dentro do esquema. Atualmente, apenas `CREATE TABLE`, `CREATE VIEW`, `CREATE INDEX`, `CREATE SEQUENCE`, `CREATE TRIGGER` e `GRANT` são aceitos como cláusulas dentro de `CREATE SCHEMA`. Outros tipos de objetos podem ser criados em comandos separados após a criação do esquema.

`IF NOT EXISTS`: Não faça nada (exceto emitir um aviso) se um esquema com o mesmo nome já existir. Os subcomandos *`schema_element`* não podem ser incluídos quando esta opção é usada.

## Notas

Para criar um esquema, o usuário que faz a solicitação deve ter o privilégio `CREATE` para o banco de dados atual. (É claro que os superusuários ignoram essa verificação.)

## Exemplos

Crie um esquema:

```
CREATE SCHEMA myschema;
```

Crie um esquema para o usuário `joe`; o esquema também será chamado `joe`:

```
CREATE SCHEMA AUTHORIZATION joe;
```

Crie um esquema chamado `test` que será de propriedade do usuário `joe`, a menos que já exista um esquema chamado `test`. (Não importa se `joe` possui o esquema pré-existente.)

```
CREATE SCHEMA IF NOT EXISTS test AUTHORIZATION joe;
```

Crie um esquema e crie uma tabela e uma visão dentro dele:

```
CREATE SCHEMA hollywood
    CREATE TABLE films (title text, release date, awards text[])
    CREATE VIEW winners AS
        SELECT title, release FROM films WHERE awards IS NOT NULL;
```

Observe que os subcomandos individuais não terminam com pontos e vírgulas.

O que se segue é uma maneira equivalente de obter o mesmo resultado:

```
CREATE SCHEMA hollywood;
CREATE TABLE hollywood.films (title text, release date, awards text[]);
CREATE VIEW hollywood.winners AS
    SELECT title, release FROM hollywood.films WHERE awards IS NOT NULL;
```

## Compatibilidade

O padrão SQL permite uma cláusula `DEFAULT CHARACTER SET` em `CREATE SCHEMA`, bem como mais tipos de subcomando do que os atualmente aceitos pelo PostgreSQL.

O padrão SQL especifica que os subcomandos em `CREATE SCHEMA` podem aparecer em qualquer ordem. A presente implementação do PostgreSQL não lida com todos os casos de referências diretas nos subcomandos; às vezes pode ser necessário reorganizar os subcomandos para evitar referências diretas.

De acordo com o padrão SQL, o proprietário de um esquema sempre possui todos os objetos dentro dele. O PostgreSQL permite que os esquemas contenham objetos de propriedade de usuários que não sejam o proprietário do esquema. Isso só pode acontecer se o proprietário do esquema conceder o privilégio `CREATE` em seu esquema para outra pessoa, ou um superusuário optar por criar objetos nele.

A opção `IF NOT EXISTS` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR SCHEMA](sql-alterschema.md "ALTER SCHEMA"), [DROP SCHEMA](sql-dropschema.md "DROP SCHEMA")