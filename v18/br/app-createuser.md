## criarusuário

createuser — definir uma nova conta de usuário do PostgreSQL

## Sinopse

`createuser` [*`connection-option`*...] [*`option`*...] [*`username`*]

## Descrição

createuser cria um novo usuário do PostgreSQL (ou, mais precisamente, um papel). Apenas usuários superusuários e usuários com privilégio `CREATEROLE` podem criar novos usuários, portanto, o createuser deve ser invocado por alguém que possa se conectar como um superusuário ou um usuário com privilégio `CREATEROLE`.

Se você deseja criar um papel com o privilégio `SUPERUSER`, `REPLICATION` ou `BYPASSRLS`, você deve se conectar como um superusuário, não apenas com o privilégio `CREATEROLE`. Ser um superusuário implica a capacidade de contornar todas as verificações de permissão de acesso dentro do banco de dados, portanto, o acesso de superusuário não deve ser concedido levemente. `CREATEROLE` também transmite [prédios muito extensos](role-attributes.md#ROLE-CREATION).

createuser é um wrapper em torno do comando SQL `CREATE ROLE`(sql-createrole.md "CREATE ROLE"). Não há diferença efetiva entre criar usuários por meio deste utilitário e por meio de outros métodos para acessar o servidor.

## Opções

createuser aceita os seguintes argumentos de linha de comando:

*`username`*: Especifica o nome do usuário do PostgreSQL a ser criado. Esse nome deve ser diferente de todos os papéis existentes nesta instalação do PostgreSQL.

`-a role` `--with-admin=role`: Especifica um papel existente que será adicionado automaticamente como membro do novo papel com opção de administrador, dando-lhe o direito de conceder membros no novo papel a outros. Múltiplos papéis existentes podem ser especificados escrevendo múltiplos interruptores `-a`.

`-c number` `--connection-limit=number`: Defina um número máximo de conexões para o novo usuário. O padrão é não definir limite.

`-d` `--createdb`: O novo usuário poderá criar bancos de dados.

`-D` `--no-createdb`: O novo usuário não será permitido criar bancos de dados. Esse é o padrão.

`-e` `--echo`: Repita os comandos que o createuser gera e envia ao servidor.

`-E` `--encrypted`: Esta opção é obsoleta, mas ainda é aceita para compatibilidade reversa.

`-g role` `--member-of=role` `--role=role` (desatualizado): Especifica que o novo papel deve ser adicionado automaticamente como membro do papel existente especificado. Múltiplos papéis existentes podem ser especificados escrevendo múltiplos interruptores `-g`.

`-i` `--inherit`: O novo papel herda automaticamente os privilégios dos papéis dos quais é membro. Esse é o padrão.

`-I` `--no-inherit`: O novo papel não herda automaticamente os privilégios dos papéis dos quais é membro.

`--interactive`: Solicitar o nome do usuário se nenhum for especificado na linha de comando, e também solicitar qual das opções `-d`/`-D`, `-r`/`-R`, `-s`/`-S` não for especificado na linha de comando. (Esse era o comportamento padrão até o PostgreSQL 9.1.)

`-l` `--login`: O novo usuário será autorizado a fazer login (ou seja, o nome do usuário pode ser usado como identificador de usuário da sessão inicial). Isso é o padrão.

`-L` `--no-login`: O novo usuário não será autorizado a fazer login. (Um papel sem privilégio de login ainda é útil como meio de gerenciar permissões de banco de dados.)

`-m role` `--with-member=role`: Especifica um papel existente que será adicionado automaticamente como membro do novo papel. Múltiplos papéis existentes podem ser especificados escrevendo múltiplos interruptores `-m`.

`-P` `--pwprompt`: Se fornecida, o createuser exibirá uma solicitação para a senha do novo usuário. Isso não é necessário se você não planeja usar autenticação por senha.

`-r` `--createrole`: O novo usuário poderá criar, alterar, excluir, comentar e alterar a etiqueta de segurança para outros papéis; ou seja, esse usuário terá o privilégio `CREATEROLE`. Consulte [criação de papel](role-attributes.md#ROLE-CREATION) para obter mais detalhes sobre quais capacidades são conferidas por esse privilégio.

`-R` `--no-createrole`: O novo usuário não poderá criar novos papéis. Esse é o padrão.

`-s` `--superuser`: O novo usuário será um superusuário.

`-S` `--no-superuser`: O novo usuário não será um superusuário. Esse é o padrão.

`-v timestamp` `--valid-until=timestamp`: Defina uma data e uma hora após a qual a senha do papel não será mais válida. O padrão é definir uma data de expiração sem senha.

`-V` `--version`: Imprimir a versão createuser e sair.

`--bypassrls`: O novo usuário ignorará todas as políticas de segurança em nível de linha (RLS).

`--no-bypassrls`: O novo usuário não contornará as políticas de segurança em nível de linha (RLS). Isso é o padrão.

`--replication`: O novo usuário terá o privilégio `REPLICATION`, que é descrito mais detalhadamente na documentação para [CREATE ROLE](sql-createrole.md "CREATE ROLE").

`--no-replication`: O novo usuário não terá o privilégio `REPLICATION`, que é descrito mais detalhadamente na documentação para [CREATE ROLE](sql-createrole.md "CREATE ROLE"). Esse é o padrão.

`-?` `--help`: Mostrar ajuda sobre os argumentos da linha de comando do comando createuser e sair.

createuser também aceita os seguintes argumentos de linha de comando para parâmetros de conexão:

`-h host` `--host=host`: Especifica o nome do host da máquina em que o servidor está sendo executado. Se o valor começar com uma barra, ele é usado como o diretório para o socket de domínio Unix.

`-p port` `--port=port`: Especifica a porta TCP ou a extensão de arquivo de soquete de domínio Unix local em que o servidor está ouvindo conexões.

`-U username` `--username=username`: Nome do usuário para se conectar como (não o nome do usuário para criar).

`-w` `--no-password`: Nunca emita um prompt de senha. Se o servidor exigir autenticação por senha e uma senha não estiver disponível por outros meios, como um arquivo `.pgpass`, a tentativa de conexão falhará. Esta opção pode ser útil em trabalhos em lote e scripts onde nenhum usuário está presente para inserir uma senha.

`-W` `--password`: Força a criação de um usuário para solicitar uma senha (para se conectar ao servidor, não para a senha do novo usuário).

Essa opção nunca é essencial, pois o createuser solicitará automaticamente uma senha se o servidor exigir autenticação por senha. No entanto, o createuser desperdiçará uma tentativa de conexão descobrindo que o servidor deseja uma senha. Em alguns casos, vale a pena digitar `-W` para evitar a tentativa extra de conexão.

## Meio Ambiente

`PGHOST` `PGPORT` `PGUSER`: Parâmetros de conexão padrão

`PG_COLOR`: Especifica se a cor deve ser usada nas mensagens de diagnóstico. Os valores possíveis são `always`, `auto` e `never`.

Esse utilitário, como a maioria dos outros utilitários do PostgreSQL, também utiliza as variáveis de ambiente suportadas pelo libpq (consulte a [Seção 32.15](libpq-envars.md)).

## Diagnósticos

Em caso de dificuldade, consulte [CREATE ROLE](sql-createrole.md "CREATE ROLE") e [psql](app-psql.md "psql") para discussões sobre problemas potenciais e mensagens de erro. O servidor de banco de dados deve estar em execução no host alvo. Além disso, quaisquer configurações de conexão padrão e variáveis de ambiente usadas pela biblioteca de interface libpq serão aplicadas.

## Exemplos

Para criar um usuário `joe` no servidor de banco de dados padrão:

```
$ createuser joe
```

Para criar um usuário `joe` no servidor de banco de dados padrão, solicitando alguns atributos adicionais:

```
$ createuser --interactive joe
Shall the new role be a superuser? (y/n) n
Shall the new role be allowed to create databases? (y/n) n
Shall the new role be allowed to create more new roles? (y/n) n
```

Para criar o mesmo usuário `joe` usando o servidor no host `eden`, porta 5000, com atributos especificamente definidos, dê uma olhada no comando subjacente:

```
$ createuser -h eden -p 5000 -S -D -R -e joe
CREATE ROLE joe NOSUPERUSER NOCREATEDB NOCREATEROLE INHERIT LOGIN;
```

Para criar o usuário `joe` como um superusuário e atribuir uma senha imediatamente:

```
$ createuser -P -s -e joe
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE joe PASSWORD 'SCRAM-SHA-256$4096:44560wPMLfjqiAzyPDZ/eQ==$4CA054rZlSFEq8Z3FEhToBTa2X6KnWFxFkPwIbKoDe0=:L/nbSZRCjp6RhOhKK56GoR1zibCCSePKshCJ9lnl3yw=' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN NOREPLICATION NOBYPASSRLS;
```

No exemplo acima, a nova senha não é exibida na tela quando digitada, mas mostramos o que foi digitado para maior clareza. Como você pode ver, a senha é criptografada antes de ser enviada ao cliente.

## Veja também

[dropuser](app-dropuser.md "dropuser"), [CREATE ROLE](sql-createrole.md "CREATE ROLE"), [createrole_self_grant](runtime-config-client.md#GUC-CREATEROLE-SELF-GRANT)