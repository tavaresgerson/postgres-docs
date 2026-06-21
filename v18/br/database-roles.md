## 21.1. Papéis de banco de dados [#](#DATABASE-ROLES)

Os papéis de banco de dados são conceitualmente completamente separados dos usuários do sistema operacional. Na prática, pode ser conveniente manter uma correspondência, mas isso não é necessário. Os papéis de banco de dados são globais em uma instalação de cluster de banco de dados (e não por banco de dados individual). Para criar um papel, use o comando SQL `CREATE ROLE`(sql-createrole.md "CREATE ROLE"):

```
CREATE ROLE name;
```

*`name`* segue as regras para identificadores SQL: sem caracteres especiais ou com aspas duplas. (Na prática, você geralmente vai querer adicionar opções adicionais, como `LOGIN`, ao comando. Mais detalhes aparecem abaixo.) Para remover um papel existente, use o comando análogo [`DROP ROLE`](sql-droprole.md)]:

```
DROP ROLE name;
```

Para conveniência, os programas [createuser](app-createuser.md "createuser") e [dropuser](app-dropuser.md "dropuser") são fornecidos como wrappers em torno desses comandos SQL que podem ser chamados a partir da linha de comando do shell:

```
createuser name
dropuser name
```

Para determinar o conjunto de papéis existentes, examine o catálogo do sistema `pg_roles`, por exemplo:

```
SELECT rolname FROM pg_roles;
```

ou para ver apenas aqueles capazes de fazer login:

```
SELECT rolname FROM pg_roles WHERE rolcanlogin;
```

O comando meta (app-psql.md "psql") do programa [psql](app-psql.md) também é útil para listar os papéis existentes.

Para inicializar o sistema de banco de dados, um sistema recém-inicializado sempre contém um papel pré-definido capaz de fazer login. Esse papel é sempre um “superusuário” e terá o mesmo nome do usuário do sistema operacional que inicializou o clúster de banco de dados com `initdb`, a menos que um nome diferente seja especificado. Esse papel é frequentemente denominado `postgres`. Para criar mais papéis, você primeiro deve se conectar como esse papel inicial.

Cada conexão com o servidor de banco de dados é feita usando o nome de algum papel específico, e esse papel determina os privilégios de acesso inicial para comandos emitidos nessa conexão. O nome do papel a ser usado para uma conexão específica com um banco de dados é indicado pelo cliente que está iniciando a solicitação de conexão de uma maneira específica para a aplicação. Por exemplo, o programa `psql` usa a opção de linha de comando `-U` para indicar o papel para se conectar. Muitas aplicações assumem o nome do usuário do sistema operacional padrão por padrão (incluindo `createuser` e `psql`). Portanto, é frequentemente conveniente manter uma correspondência de nomeação entre papéis e usuários do sistema operacional.

O conjunto de papéis de banco de dados que uma conexão de cliente específica pode se conectar é determinado pelo conjunto de configuração de autenticação do cliente, conforme explicado em [Capítulo 20](client-authentication.md). (Assim, um cliente não é limitado a se conectar como o papel que corresponde ao usuário do seu sistema operacional, assim como o nome de login de uma pessoa não precisa corresponder ao seu nome real.) Como a identidade do papel determina o conjunto de privilégios disponíveis para um cliente conectado, é importante configurar cuidadosamente os privilégios ao configurar um ambiente multiusuário.