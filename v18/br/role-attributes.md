## 21.2. Atributos do papel [#](#ROLE-ATTRIBUTES)

Um papel de banco de dados pode ter vários atributos que definem seus privilégios e interagem com o sistema de autenticação do cliente.

privilégio de login: Apenas os papéis que possuem o atributo `LOGIN` podem ser usados como o nome inicial do papel para uma conexão de banco de dados. Um papel com o atributo `LOGIN` pode ser considerado o mesmo que um “usuário do banco de dados”. Para criar um papel com privilégio de login, use:

``` CREATE ROLE name LOGIN; CREATE USER name;
    ```

(`CREATE USER` é equivalente a `CREATE ROLE`, exceto que `CREATE USER` inclui `LOGIN` por padrão, enquanto `CREATE ROLE` não o faz.)

status de superusuário: um superusuário de banco de dados contorna todas as verificações de permissão, exceto o direito de fazer login. Este é um privilégio perigoso e não deve ser usado descuidadamente; é melhor fazer a maior parte do seu trabalho como um papel que não é um superusuário. Para criar um novo superusuário de banco de dados, use `CREATE ROLE name SUPERUSER`. Você deve fazer isso como um papel que já é um superusuário.

criação de banco de dados: Um papel deve ter explicitamente a permissão para criar bancos de dados (exceto para superusuários, pois esses contornam todas as verificações de permissão). Para criar tal papel, use `CREATE ROLE name CREATEDB`.

criação de funções: uma função deve ter explicitamente permissão para criar mais funções (exceto para superusuários, pois esses contornam todas as verificações de permissão). Para criar tal função, use `CREATE ROLE name CREATEROLE`. Uma função com privilégio `CREATEROLE` pode alterar e descartar funções que tenham sido concedidas ao usuário `CREATEROLE` com a opção `ADMIN`. Tal concessão ocorre automaticamente quando um usuário `CREATEROLE` que não é um superusuário cria uma nova função, de modo que, por padrão, um usuário `CREATEROLE` pode alterar e descartar as funções que ele criou. Alterar uma função inclui a maioria das alterações que podem ser feitas usando `ALTER ROLE`, incluindo, por exemplo, alterar senhas. Também inclui modificações em uma função que podem ser feitas usando os comandos `COMMENT` e `SECURITY LABEL`.

No entanto, `CREATEROLE` não transmite a capacidade de criar papéis `SUPERUSER`, nem transmite qualquer poder sobre papéis `SUPERUSER` que já existam. Além disso, `CREATEROLE` não transmite o poder de criar usuários `REPLICATION`, nem a capacidade de conceder ou revogar o privilégio `REPLICATION`, nem a capacidade de modificar as propriedades dos papéis desses usuários. No entanto, permite que `ALTER ROLE ... SET` e `ALTER ROLE ... RENAME` sejam usados em papéis `REPLICATION`, bem como o uso de `COMMENT ON ROLE`, `SECURITY LABEL ON ROLE` e `DROP ROLE`. Finalmente, `CREATEROLE` não confere a capacidade de conceder ou revogar o privilégio `BYPASSRLS`.

iniciando a replicação: Um papel deve ter explicitamente a permissão para iniciar a replicação em streaming (exceto para superusuários, pois esses contornam todas as verificações de permissão). Um papel usado para replicação em streaming também deve ter a permissão `LOGIN`. Para criar um papel desse tipo, use `CREATE ROLE name REPLICATION LOGIN`.

senha: Uma senha é significativa apenas se o método de autenticação do cliente exigir que o usuário forneça uma senha ao se conectar ao banco de dados. Os métodos de autenticação `password` e `md5` utilizam senhas. As senhas do banco de dados são separadas das senhas do sistema operacional. Especifique uma senha na criação do papel com `CREATE ROLE name PASSWORD 'string'`.

herança de privilégios: Por padrão, um papel herda os privilégios dos papéis dos quais é membro. No entanto, para criar um papel que não herde privilégios por padrão, use `CREATE ROLE name NOINHERIT`. Alternativamente, a herança pode ser ignorada para concessões individuais usando `WITH INHERIT TRUE` ou `WITH INHERIT FALSE`.

bypassar a segurança de nível de linha: Uma função deve ter explicitamente concedido permissão para ignorar todas as políticas de segurança de nível de linha (RLS) (exceto para superusuários, uma vez que esses ignoram todas as verificações de permissão). Para criar tal função, use `CREATE ROLE name BYPASSRLS` como um superusuário.

limite de conexão: O limite de conexão pode especificar quantas conexões concorrentes um papel pode fazer. -1 (o padrão) significa sem limite. Especifique o limite de conexão na criação do papel com `CREATE ROLE name CONNECTION LIMIT 'integer'`.

Os atributos de um papel podem ser modificados após a criação com `ALTER ROLE`. Consulte as páginas de referência para os comandos [CREATE ROLE](sql-createrole.md "CREATE ROLE") e [ALTER ROLE](sql-alterrole.md "ALTER ROLE") para obter detalhes.

Um papel também pode ter configurações específicas para o papel para muitas das configurações de configuração de tempo de execução descritas em [Capítulo 19][(runtime-config.md "Chapter 19. Server Configuration")]. Por exemplo, se, por algum motivo, você quiser desabilitar varreduras de índice (dica: não é uma boa ideia) a qualquer momento que você se conectar, você pode usar:

```
ALTER ROLE myname SET enable_indexscan TO off;
```

Isso salvará o ajuste (mas não o configurará imediatamente). Em conexões subsequentes por este papel, parecerá como se `SET enable_indexscan TO off` tivesse sido executado pouco antes do início da sessão. Você ainda pode alterar este ajuste durante a sessão; ele será apenas o padrão. Para remover um ajuste padrão específico do papel, use `ALTER ROLE rolename RESET varname`. Note que os ajustes padrão específicos do papel anexados a papéis sem privilégio `LOGIN` são bastante inúteis, uma vez que nunca serão invocados.

Quando um usuário não superusuário cria um papel usando o privilégio `CREATEROLE`, o papel criado é automaticamente concedido de volta ao usuário criador, assim como se o superusuário de bootstrap tivesse executado o comando `GRANT created_user TO creating_user WITH ADMIN TRUE, SET FALSE, INHERIT FALSE`. Como um usuário `CREATEROLE` só pode exercer privilégios especiais em relação a um papel existente se tiver `ADMIN OPTION` nele, essa concessão é apenas suficiente para permitir que um usuário `CREATEROLE` administre os papéis que criou. No entanto, como é criado com `INHERIT FALSE, SET FALSE`, o usuário `CREATEROLE` não herda os privilégios do papel criado, nem pode acessar os privilégios desse papel usando `SET ROLE`. No entanto, como qualquer usuário que tenha `ADMIN OPTION` em um papel pode conceder filiação a esse papel a qualquer outro usuário, o usuário `CREATEROLE` pode obter acesso ao papel criado, simplesmente concedendo esse papel de volta a si mesmo com as opções `INHERIT` e/ou `SET`. Assim, o fato de que os privilégios não são herdados por padrão e o `SET ROLE` não é concedido por padrão é uma proteção contra acidentes, não uma característica de segurança. Além disso, note que, como essa concessão automática é concedida pelo superusuário de bootstrap, não pode ser removida ou alterada pelo usuário `CREATEROLE`; no entanto, qualquer superusuário pode revogá-la, modificá-la e/ou emitir concessões adicionais a outros usuários `CREATEROLE`. Quaisquer usuários `CREATEROLE` que tenham `ADMIN OPTION` em um papel em qualquer momento podem administrá-lo.