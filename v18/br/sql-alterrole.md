## ALTER ROLE

ALTER ROLE — alterar um papel de banco de dados

## Sinopse

```
ALTER ROLE role_specification [ WITH ] option [ ... ]

where option can be:

      SUPERUSER | NOSUPERUSER
    | CREATEDB | NOCREATEDB
    | CREATEROLE | NOCREATEROLE
    | INHERIT | NOINHERIT
    | LOGIN | NOLOGIN
    | REPLICATION | NOREPLICATION
    | BYPASSRLS | NOBYPASSRLS
    | CONNECTION LIMIT connlimit
    | [ ENCRYPTED ] PASSWORD 'password' | PASSWORD NULL
    | VALID UNTIL 'timestamp'

ALTER ROLE name RENAME TO new_name

ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter { TO | = } { value | DEFAULT }
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] SET configuration_parameter FROM CURRENT
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] RESET configuration_parameter
ALTER ROLE { role_specification | ALL } [ IN DATABASE database_name ] RESET ALL

where role_specification can be:

    role_name
  | CURRENT_ROLE
  | CURRENT_USER
  | SESSION_USER
```

## Descrição

`ALTER ROLE` altera os atributos de um papel do PostgreSQL.

A primeira variante deste comando listado no sinopse pode alterar muitos dos atributos de papel que podem ser especificados em [`CREATE ROLE`](sql-createrole.md "CREATE ROLE"). (Todos os atributos possíveis são cobertos, exceto que não há opções para adicionar ou remover membros; use [`GRANT`](sql-grant.md "GRANT") e [`REVOKE`](sql-revoke.md "REVOKE") para isso.) Os atributos não mencionados no comando retêm suas configurações anteriores. Superusuários de banco de dados podem alterar qualquer uma dessas configurações para qualquer papel, exceto para alterar a propriedade [`SUPERUSER` para o [*[bootstrap superuser](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER "Bootstrap superuser")*](glossary.md#GLOSSARY-BOOTSTRAP-SUPERUSER). Os papéis que não são superusuários com privilégio `CREATEROLE` podem alterar a maioria dessas propriedades, mas apenas para papéis que não são superusuários e não de replicação para os quais eles foram concedidos `ADMIN OPTION`. Os não superusuários não podem alterar a propriedade `SUPERUSER` e podem alterar as propriedades `CREATEDB`, `REPLICATION` e `BYPASSRLS` apenas se elas possuírem a propriedade correspondente. Papéis comuns podem apenas alterar sua própria senha.

A segunda variante altera o nome do papel. Os superusuários do banco de dados podem renomear qualquer papel. Os papéis com privilégio `CREATEROLE` podem renomear papéis que não são superusuários para os quais eles tenham sido concedidos `ADMIN OPTION`. O usuário da sessão atual não pode ser renomeado. (Conecte-se como um usuário diferente se precisar fazer isso.) Como as senhas criptografadas `MD5` usam o nome do papel como sal criptográfico, renomear um papel limpa sua senha se a senha for criptografada `MD5`.

As variantes restantes alteram a sessão padrão de um papel para uma variável de configuração, para todas as bases de dados ou, quando a cláusula `IN DATABASE` é especificada, apenas para sessões no banco de dados nomeado. Se `ALL` for especificado em vez de um nome de papel, isso altera o ajuste para todos os papéis. Usar `ALL` com `IN DATABASE` é efetivamente o mesmo que usar o comando `ALTER DATABASE ... SET ...`.

Sempre que o papel subsequentemente iniciar uma nova sessão, o valor especificado se torna o padrão da sessão, substituindo qualquer configuração presente em `postgresql.conf` ou que tenha sido recebida a partir da linha de comando `postgres`. Isso acontece apenas no momento do login; a execução de [`SET ROLE`](sql-set-role.md "SET ROLE") ou [`SET SESSION AUTHORIZATION`](sql-set-session-authorization.md "SET SESSION AUTHORIZATION") não faz com que novos valores de configuração sejam definidos. As configurações definidas para todas as bases de dados são substituídas por configurações específicas da base de dados anexadas a um papel. As configurações para bases de dados específicas ou para papéis específicos substituem as configurações para todos os papéis.

Os superusuários podem alterar as configurações padrão de qualquer sessão. Os papéis que possuem o privilégio `CREATEROLE` podem alterar as configurações padrão dos papéis que não são superusuários para os quais eles foram concedidos `ADMIN OPTION`. Os papéis comuns só podem definir configurações para si mesmos. Algumas variáveis de configuração não podem ser definidas dessa maneira, ou só podem ser definidas se um superusuário emitir o comando. Apenas os superusuários podem alterar uma configuração para todos os papéis em todos os bancos de dados.

## Parâmetros

*`name`* [#](#SQL-ALTERROLE-PARAMS-NAME): O nome do papel cujos atributos devem ser alterados.

`CURRENT_ROLE` `CURRENT_USER` [#](#SQL-ALTERROLE-PARAMS-CURRENT-ROLE): Alterar o usuário atual em vez de um papel explicitamente identificado.

`SESSION_USER` [#](#SQL-ALTERROLE-PARAMS-SESSION-USER): Alterar o usuário da sessão atual em vez de um papel explicitamente identificado.

`SUPERUSER` `NOSUPERUSER` `CREATEDB` `NOCREATEDB` `CREATEROLE` `NOCREATEROLE` `INHERIT` `NOINHERIT` `LOGIN` `NOLOGIN` `REPLICATION` `NOREPLICATION` `BYPASSRLS` `NOBYPASSRLS` `CONNECTION LIMIT` *`connlimit`* [ `ENCRYPTED` ] `PASSWORD` '*`password`*' `PASSWORD NULL` `VALID UNTIL` '*`timestamp`*' [#](#SQL-ALTERROLE-PARAMS-SUPERUSER): Essas cláusulas alteram atributos originalmente definidos por [`CREATE ROLE`](sql-createrole.md). Para mais informações, consulte a página de referência `CREATE ROLE`.

*`new_name`* [#](#SQL-ALTERROLE-PARAMS-NEW-NAME): O novo nome do papel.

*`database_name`* [#](#SQL-ALTERROLE-PARAMS-DATABASE-NAME): O nome do banco de dados no qual a variável de configuração deve ser definida.

*`configuration_parameter`* *`value`* [#](#SQL-ALTERROLE-PARAMS-CONFIGURATION-PARAMETER): Defina o valor padrão da sessão do papel para o parâmetro de configuração especificado no valor dado. Se *`value`* for `DEFAULT` ou, de forma equivalente, `RESET` for usado, o ajuste da variável específica do papel é removido, de modo que o papel herde o ajuste padrão de nível de sistema em novas sessões. Use `RESET ALL` para limpar todos os ajustes específicos do papel. `SET FROM CURRENT` salva o valor atual da sessão do parâmetro como o valor específico do papel. Se `IN DATABASE` for especificado, o parâmetro de configuração é definido ou removido apenas para o papel e o banco de dados.

As configurações variáveis específicas para o papel só entram em vigor no momento do login; `SET ROLE` (sql-set-role.md "SET ROLE") e [`SET SESSION AUTHORIZATION` ](sql-set-session-authorization.md) não processam configurações variáveis específicas para o papel.

Consulte [SET](sql-set.md "SET") e [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para obter mais informações sobre os nomes e valores permitidos dos parâmetros.

## Notas

Use `CREATE ROLE` para adicionar novos papéis e `DROP ROLE` para remover um papel.

`ALTER ROLE` não pode alterar as associações de um papel. Use [`GRANT`](sql-grant.md "GRANT") e [`REVOKE`](sql-revoke.md "REVOKE") para fazer isso.

É necessário ter cautela ao especificar uma senha não criptografada com este comando. A senha será transmitida ao servidor em texto claro e também pode ser registrada no histórico de comandos do cliente ou no log do servidor. [psql](app-psql.md "psql") contém um comando `\password` que pode ser usado para alterar a senha de um papel sem expor a senha em texto claro.

Também é possível vincular um padrão de sessão a um banco de dados específico, em vez de a um papel; veja [ALTER DATABASE](sql-alterdatabase.md "ALTER DATABASE"). Se houver um conflito, as configurações específicas do banco de dados substituem as específicas do papel, que por sua vez substituem as específicas do banco de dados.

## Exemplos

Alterar a senha de um papel:

```
ALTER ROLE davide WITH PASSWORD 'hu8jmn3';
```

Remova a senha de um papel:

```
ALTER ROLE davide WITH PASSWORD NULL;
```

Altere a data de expiração da senha, especificando que a senha deve expirar ao meio-dia em 4 de maio de 2015, usando o fuso horário que está uma hora à frente do UTC:

```
ALTER ROLE chris VALID UNTIL 'May 4 12:00:00 2015 +1';
```

Faça uma senha válida para sempre:

```
ALTER ROLE fred VALID UNTIL 'infinity';
```

Dê a uma função a capacidade de gerenciar outras funções e criar novos bancos de dados:

```
ALTER ROLE miriam CREATEROLE CREATEDB;
```

Dê um valor padrão diferente para o parâmetro [maintenance_work_mem](runtime-config-resource.md#GUC-MAINTENANCE-WORK-MEM) de um recurso:

```
ALTER ROLE worker_bee SET maintenance_work_mem = 100000;
```

Dê a um papel uma configuração específica do parâmetro [client_min_messages](runtime-config-client.md#GUC-CLIENT-MIN-MESSAGES) que não seja padrão e específica do banco de dados:

```
ALTER ROLE fred IN DATABASE devel SET client_min_messages = DEBUG;
```

## Compatibilidade

A declaração `ALTER ROLE` é uma extensão do PostgreSQL.

## Veja também

[Crie papel](sql-createrole.md "CREATE ROLE"), [Retire papel](sql-droprole.md "DROP ROLE"), [Alterar banco de dados](sql-alterdatabase.md "ALTER DATABASE"), [Definir](sql-set.md "SET")