## Crie o papel

Crie o papel — defina um novo papel de banco de dados

## Sinopse

```
CREATE ROLE name [ [ WITH ] option [ ... ] ]

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
    | IN ROLE role_name [, ...]
    | ROLE role_name [, ...]
    | ADMIN role_name [, ...]
    | SYSID uid
```

## Descrição

`CREATE ROLE` adiciona um novo papel a um clúster de banco de dados PostgreSQL. Um papel é uma entidade que pode possuir objetos de banco de dados e ter privilégios de banco de dados; um papel pode ser considerado um “usuário”, um “grupo” ou ambos, dependendo de como é usado. Consulte [Capítulo 21][(user-manag.md "Chapter 21. Database Roles")] e [Capítulo 20][(client-authentication.md "Chapter 20. Client Authentication")] para obter informações sobre a gestão de usuários e autenticação. Você deve ter privilégio `CREATEROLE` ou ser um superusuário do banco de dados para usar este comando.

Observe que os papéis são definidos no nível do clúster do banco de dados e, portanto, são válidos em todos os bancos de dados do clúster.

Durante a criação de um papel, é possível atribuir imediatamente o papel recém-criado a ser membro de um papel existente, e também atribuir papéis existentes a serem membros do papel recém-criado. As regras para as quais as opções de inicial membership de papel são habilitadas são descritas abaixo nas cláusulas `IN ROLE`, `ROLE` e `ADMIN`. O comando [GRANT](sql-grant.md "GRANT") tem controle de opção de nível granular durante a criação de membership, e a capacidade de modificar essas opções após o novo papel ser criado.

## Parâmetros

*`name`*: O nome do novo papel.

`SUPERUSER` `NOSUPERUSER`: Essas cláusulas determinam se o novo papel é um "superusuário", que pode anular todas as restrições de acesso dentro do banco de dados. O status de superusuário é perigoso e deve ser usado apenas quando realmente necessário. Você deve ser um superusuário para criar um novo superusuário. Se não for especificado, `NOSUPERUSER` é o padrão.

`CREATEDB` `NOCREATEDB`: Essas cláusulas definem a capacidade de um papel criar bancos de dados. Se `CREATEDB` for especificado, o papel que está sendo definido será permitido criar novos bancos de dados. Especificar `NOCREATEDB` negará a um papel a capacidade de criar bancos de dados. Se não for especificado, `NOCREATEDB` é o padrão. Apenas papéis de superusuário ou papéis com `CREATEDB` podem especificar `CREATEDB`.

`CREATEROLE` `NOCREATEROLE`: Essas cláusulas determinam se um papel será permitido criar, alterar, descartar, comentar e alterar a etiqueta de segurança para outros papéis. Consulte [criação de papel](role-attributes.md#ROLE-CREATION) para obter mais detalhes sobre quais capacidades são conferidas por este privilégio. Se não especificado, `NOCREATEROLE` é o padrão.

`INHERIT` `NOINHERIT`: Isso afeta o status de herança de membros quando este papel é adicionado como membro de outro papel, tanto neste quanto em comandos futuros. Especificamente, ele controla o status de herança de membros adicionados com este comando usando a cláusula `IN ROLE`, e em comandos posteriores usando a cláusula `ROLE`. Também é usado como o status de herança padrão ao adicionar este papel como membro usando o comando `GRANT`. Se não especificado, `INHERIT` é o padrão.

Nas versões do PostgreSQL anteriores à 16, a herança era um atributo de nível de papel que controlava todas as verificações de associação em tempo de execução para esse papel.

`LOGIN`: Essas cláusulas determinam se um papel pode fazer login, ou seja, se o papel pode ser especificado como o nome da autorização inicial durante a conexão do cliente. Um papel que possui o atributo `NOLOGIN` pode ser considerado um usuário. Os papéis sem esse atributo são úteis para gerenciar privilégios de banco de dados, mas não são usuários no sentido usual da palavra. Se não especificado, `LOGIN` é o padrão, exceto quando `NOLOGIN` é invocado através de sua grafia alternativa [`CREATE ROLE`](sql-createuser.md "CREATE USER").

`REPLICATION` `NOREPLICATION`: Essas cláusulas determinam se um papel é um papel de replicação. Um papel deve ter esse atributo (ou ser um superusuário) para poder se conectar ao servidor no modo de replicação (replicação física ou lógica) e para poder criar ou descartar slots de replicação. Um papel que possui o atributo `REPLICATION` é um papel muito altamente privilegiado e deve ser usado apenas em papéis que são realmente usados para replicação. Se não for especificado, `NOREPLICATION` é o padrão. Apenas papéis de superusuário ou papéis com `REPLICATION` podem especificar `REPLICATION`.

`BYPASSRLS` `NOBYPASSRLS`: Essas cláusulas determinam se um papel ignora toda a política de segurança em nível de linha (RLS). `NOBYPASSRLS` é o padrão. Apenas papéis de superusuário ou papéis com `BYPASSRLS` podem especificar `BYPASSRLS`.

Observe que o pg_dump configurará `row_security` para `OFF` por padrão, para garantir que todos os conteúdos de uma tabela sejam descarregados. Se o usuário que executa o pg_dump não tiver permissões apropriadas, um erro será retornado. No entanto, superusuários e o proprietário da tabela que está sendo descarregada sempre ignoram o RLS.

`CONNECTION LIMIT` *`connlimit`*: Se o papel puder fazer login, isso especifica quantas conexões concorrentes o papel pode fazer. -1 (o padrão) significa sem limite. Note que apenas conexões normais são contadas para este limite. Nem as transações preparadas nem as conexões do trabalhador de fundo são contadas para este limite.

[[`ENCRYPTED`]] `PASSWORD` '*`password`*' `PASSWORD NULL`: Define a senha do papel. (Uma senha só é útil para papéis que possuem o atributo `LOGIN`, mas você pode definir uma para papéis sem esse atributo.) Se você não planeja usar autenticação por senha, pode omitir essa opção. Se não for especificado nenhuma senha, a senha será definida como nulo e a autenticação por senha sempre falhará para esse usuário. Uma senha nula pode ser escrita explicitamente como `PASSWORD NULL`, opcionalmente.

### Nota

Especificar uma string vazia também definirá a senha como nulo, mas isso não era o caso antes da versão 10 do PostgreSQL. Em versões anteriores, uma string vazia poderia ser usada, ou não, dependendo do método de autenticação e da versão exata, e o libpq se recusaria a usá-la em qualquer caso. Para evitar a ambiguidade, a especificação de uma string vazia deve ser evitada.

A senha é sempre armazenada criptografada nos catálogos do sistema. A palavra-chave `ENCRYPTED` não tem efeito, mas é aceita para compatibilidade reversa. O método de criptografia é determinado pelo parâmetro de configuração [password_encryption](runtime-config-connection.md#GUC-PASSWORD-ENCRYPTION). Se a string de senha apresentada já estiver em formato criptografado MD5 ou SCRAM, ela é armazenada como está, independentemente de `password_encryption` (já que o sistema não pode descriptografar a string de senha criptografada especificada, para criptografá-la em um formato diferente). Isso permite a recarga de senhas criptografadas durante o dump/restauração.

### Aviso

O suporte para senhas criptografadas com MD5 é desatualizado e será removido em uma versão futura do PostgreSQL. Consulte [Seção 20.5][(auth-password.md "20.5. Password Authentication")] para obter detalhes sobre a migração para outro tipo de senha.

`VALID UNTIL` '*`timestamp`*: A cláusula `VALID UNTIL` define uma data e uma hora após a qual a senha do papel não será mais válida. Se esta cláusula for omitida, a senha será válida por todo o tempo.

`IN ROLE` *`role_name`*: A cláusula `IN ROLE` faz com que o novo papel seja adicionado automaticamente como membro dos papéis existentes especificados. A nova associação terá a opção `SET` habilitada e a opção `ADMIN` desabilitada. A opção `INHERIT` será habilitada, a menos que a opção `NOINHERIT` seja especificada.

`ROLE` *`role_name`*: A cláusula `ROLE` faz com que um ou mais papéis existentes especificados sejam adicionados automaticamente como membros, com a opção `SET` habilitada. Isso, na verdade, torna o novo papel um “grupo”. Os papéis nomeados nesta cláusula com o atributo de nível de papel `INHERIT` terão a opção `INHERIT` habilitada na nova associação. Novas associações terão a opção `ADMIN` desabilitada.

`ADMIN` *`role_name`*: A cláusula `ADMIN` tem o mesmo efeito que `ROLE`, mas os papéis nomeados são adicionados como membros do novo papel com `ADMIN` habilitado, dando-lhes o direito de conceder a adesão ao novo papel a outros.

`SYSID` *`uid`*: A cláusula `SYSID` é ignorada, mas é aceita para compatibilidade reversa.

## Notas

Use `ALTER ROLE` para alterar os atributos de um papel e (sql-alterrole.md "ALTER ROLE") para remover um papel. Todos os atributos especificados por `DROP ROLE` podem ser modificados por comandos posteriores `ALTER ROLE`.

A maneira preferida de adicionar e remover membros de papéis que estão sendo usados como grupos é usar `GRANT` (sql-grant.md "GRANT") e `REVOKE` (sql-revoke.md "REVOKE").

A cláusula `VALID UNTIL` define um tempo de expiração apenas para uma senha, não para o papel em si. Em particular, o tempo de expiração não é aplicado ao acesso usando um método de autenticação que não é baseado em senha.

Os atributos de papel definidos aqui não são hereditários, ou seja, sendo membro de um papel com, por exemplo, `CREATEDB`, o membro não poderá criar novos bancos de dados, mesmo que a concessão de acesso tenha a opção `INHERIT`. Claro que, se a concessão de acesso tiver a opção `SET`, o papel do membro poderá [`SET ROLE`(sql-set-role.md "SET ROLE") para o papel criado_db e, em seguida, criar um novo banco de dados.

As concessões de filiação criadas pelas cláusulas `IN ROLE`, `ROLE` e `ADMIN` têm o papel de executar este comando como concedente.

O atributo `INHERIT` é o padrão por razões de compatibilidade reversa: em versões anteriores do PostgreSQL, os usuários sempre tinham acesso a todos os privilégios dos grupos dos quais eram membros. No entanto, `NOINHERIT` fornece uma correspondência mais próxima às semânticas especificadas no padrão SQL.

O PostgreSQL inclui um programa [createuser][(app-createuser.md "createuser")] que tem a mesma funcionalidade que `CREATE ROLE` (de fato, ele chama esse comando) mas pode ser executado a partir do shell de comando.

A opção `CONNECTION LIMIT` é apenas aplicada aproximadamente; se duas novas sessões começarem aproximadamente ao mesmo tempo, quando apenas um "caixote" de conexão permanece para o papel, é possível que ambas falhem. Além disso, o limite nunca é aplicado para superusuários.

É necessário ter cautela ao especificar uma senha não criptografada com este comando. A senha será transmitida ao servidor em texto claro e também pode ser registrada no histórico de comandos do cliente ou no log do servidor. O comando [createuser](app-createuser.md "createuser"), no entanto, transmite a senha criptografada. Além disso, [psql](app-psql.md "psql") contém um comando `\password` que pode ser usado para alterar a senha com segurança posteriormente.

## Exemplos

Crie um papel que possa fazer login, mas não dê uma senha:

```
CREATE ROLE jonathan LOGIN;
```

Crie um papel com uma senha:

```
CREATE USER davide WITH PASSWORD 'jw8s0F4';
```

(`CREATE USER` é o mesmo que `CREATE ROLE`, exceto que ele implica em `LOGIN`.])

Crie um papel com uma senha válida até o final de 2004. Após um segundo ter passado em 2005, a senha deixa de ser válida.

```
CREATE ROLE miriam WITH LOGIN PASSWORD 'jw8s0F4' VALID UNTIL '2005-01-01';
```

Crie um papel que possa criar bancos de dados e gerenciar papéis:

```
CREATE ROLE admin WITH CREATEDB CREATEROLE;
```

## Compatibilidade

A declaração `CREATE ROLE` está no padrão SQL, mas o padrão apenas exige a sintaxe

```
CREATE ROLE name [ WITH ADMIN role_name ]
```

Múltiplos administradores iniciais e todas as outras opções de `CREATE ROLE` são extensões do PostgreSQL.

O padrão SQL define os conceitos de usuários e papéis, mas considera-os como conceitos distintos e deixa todos os comandos que definem usuários especificados por cada implementação do banco de dados. No PostgreSQL, escolhemos unificar usuários e papéis em um único tipo de entidade. Portanto, os papéis têm muitos mais atributos opcionais do que eles têm no padrão.

O comportamento especificado pelo padrão SQL é mais bem aproximado ao criar usuários padrão SQL como papéis do PostgreSQL com a opção `NOINHERIT`, e papéis padrão SQL como papéis do PostgreSQL com a opção `INHERIT`.

A cláusula `USER` tem o mesmo comportamento que `ROLE`, mas foi descontinuada:

```
USER role_name [, ...]
```

A cláusula `IN GROUP` tem o mesmo comportamento que a `IN ROLE`, mas foi descontinuada:

```
IN GROUP role_name [, ...]
```

## Veja também

[SET ROLE](sql-set-role.md "SET ROLE"), [ALTER ROLE](sql-alterrole.md "ALTER ROLE"), [DROP ROLE](sql-droprole.md "DROP ROLE"), [GRANT](sql-grant.md "GRANT"), [REVOKE](sql-revoke.md "REVOKE"), [createuser](app-createuser.md "createuser"), [createrole_self_grant](runtime-config-client.md#GUC-CREATEROLE-SELF-GRANT)