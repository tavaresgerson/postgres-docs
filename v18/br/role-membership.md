## 21.3. Membros do papel [#](#ROLE-MEMBERSHIP)

É frequentemente conveniente agrupar os usuários para facilitar a gestão de privilégios: dessa forma, os privilégios podem ser concedidos a, ou revogados de, um grupo como um todo. No PostgreSQL, isso é feito criando um papel que representa o grupo e, em seguida, concedendo *membriado* no papel do grupo a papéis de usuário individuais.

Para configurar um papel de grupo, primeiro crie o papel:

```
CREATE ROLE name;
```

Normalmente, um papel que é usado como um grupo não teria o atributo `LOGIN`, embora você possa defini-lo se desejar.

Uma vez que o papel do grupo exista, você pode adicionar e remover membros usando os comandos `GRANT` (sql-grant.md "GRANT") e `REVOKE` (sql-revoke.md "REVOKE"):

```
GRANT group_role TO role1, ... ;
REVOKE group_role FROM role1, ... ;
```

Você também pode conceder membros a outros papéis do grupo (já que não há realmente nenhuma distinção entre papéis de grupo e papéis não de grupo). O banco de dados não permitirá que você configure loops de membros circulares. Além disso, não é permitido conceder membros a um papel para `PUBLIC`.

Os membros de um grupo podem usar os privilégios do papel de duas maneiras. Primeiro, os papéis de membro que receberam a opção `SET` podem fazer [`SET ROLE`](sql-set-role.md "SET ROLE") para se tornar temporariamente o papel do grupo. Neste estado, a sessão do banco de dados tem acesso aos privilégios do papel do grupo, em vez do papel de login original, e quaisquer objetos do banco de dados criados são considerados de propriedade do papel do grupo, não do papel de login. Em segundo lugar, os papéis de membro que receberam a opção `INHERIT` têm automaticamente o uso dos privilégios daqueles que são membros diretamente ou indiretamente, embora a cadeia pareça em membros que não possuem a opção herdar. Como exemplo, suponha que fizemos:

```
CREATE ROLE joe LOGIN;
CREATE ROLE admin;
CREATE ROLE wheel;
CREATE ROLE island;
GRANT admin TO joe WITH INHERIT TRUE;
GRANT wheel TO admin WITH INHERIT FALSE;
GRANT island TO joe WITH INHERIT TRUE, SET FALSE;
```

Imediatamente após a conexão como papel `joe`, uma sessão no banco de dados terá o uso de privilégios concedidos diretamente a `joe` mais quaisquer privilégios concedidos a `admin` e `island`, porque `joe` “herda” esses privilégios. No entanto, os privilégios concedidos a `wheel` não estão disponíveis, porque, embora `joe` seja indiretamente um membro de `wheel`, a filiação é por meio de `admin`, que foi concedida usando `WITH INHERIT FALSE`. Após:

```
SET ROLE admin;
```

a sessão teria o uso apenas dos privilégios concedidos a `admin`, e não aqueles concedidos a `joe` ou `island`. Após:

```
SET ROLE wheel;
```

a sessão terá o uso apenas dos privilégios concedidos a `wheel`, e não aqueles concedidos a `joe` ou `admin`. O estado original do privilégio pode ser restaurado com qualquer um dos seguintes:

```
SET ROLE joe;
SET ROLE NONE;
RESET ROLE;
```

### Nota

O comando `SET ROLE` sempre permite selecionar qualquer papel que o papel de login original seja diretamente ou indiretamente um membro, desde que haja uma cadeia de concessões de membros, cada uma das quais tenha `SET TRUE` (que é o padrão). Assim, no exemplo acima, não é necessário se tornar `admin` antes de se tornar `wheel`. Por outro lado, não é possível se tornar `island` de forma alguma; `joe` pode acessar esses privilégios apenas por herança.

### Nota

No padrão SQL, há uma distinção clara entre usuários e papéis, e os usuários não herdam automaticamente privilégios enquanto os papéis o fazem. Esse comportamento pode ser obtido no PostgreSQL ao atribuir aos papéis usados como papéis SQL o atributo `INHERIT`, enquanto atribui aos papéis usados como usuários SQL o atributo `NOINHERIT`. No entanto, o PostgreSQL, por padrão, atribui a todos os papéis o atributo `INHERIT`, para compatibilidade reversa com versões anteriores à versão 8.1, nas quais os usuários sempre tinham acesso a permissões concedidas aos grupos dos quais eram membros.

Os atributos de papel `LOGIN`, `SUPERUSER`, `CREATEDB` e `CREATEROLE` podem ser considerados privilégios especiais, mas nunca são herdados como privilégios comuns nos objetos de banco de dados. Você deve, na verdade, `SET ROLE` para um papel específico que tenha um desses atributos para poder utilizar o atributo. Continuando o exemplo acima, podemos optar por conceder `CREATEDB` e `CREATEROLE` ao papel `admin`. Então, uma sessão que se conecta como papel `joe` não teria esses privilégios imediatamente, apenas após fazer `SET ROLE admin`.

Para destruir um papel de grupo, use `DROP ROLE`(sql-droprole.md "DROP ROLE"):

```
DROP ROLE name;
```

Qualquer associação no papel do grupo é automaticamente revogada (mas os papéis dos membros não são afetados de outra forma).