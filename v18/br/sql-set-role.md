## DEFINA O PAPEL

SET ROLE — define o identificador atual do usuário da sessão atual

## Sinopse

```
SET [ SESSION | LOCAL ] ROLE role_name
SET [ SESSION | LOCAL ] ROLE NONE
RESET ROLE
```

## Descrição

Este comando define o identificador de usuário atual da sessão SQL atual como *`role_name`*. O nome do papel pode ser escrito como um identificador ou uma literal de string. Após `SET ROLE`, a verificação de permissões para comandos SQL é realizada como se o papel nomeado fosse o que havia iniciado sessão originalmente. Note que `SET ROLE` e `SET SESSION AUTHORIZATION` são exceções; as verificações de permissões para essas exceções continuam a usar o usuário da sessão atual e o usuário da sessão inicial (o usuário *autenticado*), respectivamente.

O usuário atual da sessão deve ter a opção `SET` para o *`role_name` especificado, diretamente ou indiretamente por meio de uma cadeia de associações com a opção `SET`. (Se o usuário da sessão for um superusuário, qualquer papel pode ser selecionado.)

Os modificadores `SESSION` e `LOCAL` atuam da mesma forma que o comando regular [`SET`(sql-set.md "SET")].

`SET ROLE NONE` define o identificador do usuário atual como o identificador do usuário da sessão atual, conforme retornado por `session_user`. `RESET ROLE` define o identificador do usuário atual como o ajuste do tempo de conexão especificado pelas opções de linha de comando [(libpq-connect.md#LIBPQ-CONNECT-OPTIONS), [`ALTER ROLE`](sql-alterrole.md "ALTER ROLE"), ou [`ALTER DATABASE`](sql-alterdatabase.md "ALTER DATABASE"), se houver tais configurações. Caso contrário, `RESET ROLE` define o identificador do usuário atual como o identificador do usuário da sessão atual. Esses formulários podem ser executados por qualquer usuário.

## Notas

Usando este comando, é possível adicionar privilégios ou restringir os privilégios de alguém. Se o papel do usuário da sessão tiver sido concedido a membros `WITH INHERIT TRUE`, ele terá automaticamente todos os privilégios de cada um desses papéis. Neste caso, `SET ROLE` efetivamente elimina todos os privilégios, exceto aqueles que o papel alvo possui diretamente ou herda. Por outro lado, se o papel do usuário da sessão tiver sido concedido a membros `WITH INHERIT FALSE`, os privilégios dos papéis concedidos não podem ser acessados por padrão. No entanto, se o papel foi concedido `WITH SET TRUE`, o usuário da sessão pode usar `SET ROLE` para eliminar os privilégios atribuídos diretamente ao usuário da sessão e, em vez disso, adquirir os privilégios disponíveis para o papel nomeado. Se o papel foi concedido `WITH INHERIT FALSE, SET FALSE`, os privilégios desse papel também não podem ser exercidos com ou sem `SET ROLE`.

`SET ROLE` tem efeitos comparáveis a [`SET SESSION AUTHORIZATION`](sql-set-session-authorization.md "SET SESSION AUTHORIZATION"), mas as verificações de privilégio envolvidas são bastante diferentes. Além disso, `SET SESSION AUTHORIZATION` determina quais papéis são permitidos para comandos posteriores de `SET ROLE`, enquanto alterar papéis com `SET ROLE` não altera o conjunto de papéis permitidos para um comando posterior de `SET ROLE`.

`SET ROLE` não processa variáveis de sessão conforme especificado pelas configurações do `ALTER ROLE` do papel; isso acontece apenas durante o login.

`SET ROLE` não pode ser usado dentro de uma função `SECURITY DEFINER`.

## Exemplos

```
SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | peter

SET ROLE 'paul';

SELECT SESSION_USER, CURRENT_USER;

 session_user | current_user
--------------+--------------
 peter        | paul
```

## Compatibilidade

O PostgreSQL permite a sintaxe de identificadores (`"rolename"`), enquanto o padrão SQL exige que o nome do papel seja escrito como uma literal de string. O SQL não permite este comando durante uma transação; o PostgreSQL não faz essa restrição porque não há motivo para isso. Os modificadores `SESSION` e `LOCAL` são uma extensão do PostgreSQL, assim como a sintaxe `RESET`.

## Veja também

[SET SESSION AUTHORIZATION](sql-set-session-authorization.md "SET SESSION AUTHORIZATION")