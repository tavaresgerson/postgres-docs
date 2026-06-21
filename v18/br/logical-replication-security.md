## 29.11. Segurança [#](#LOGICAL-REPLICATION-SECURITY)

O papel usado para a conexão de replicação deve ter o atributo `REPLICATION` (ou ser um superusuário). Se o papel não tiver `SUPERUSER` e `BYPASSRLS`, as políticas de segurança de linha do editor podem ser executadas. Se o papel não confiar em todos os proprietários da tabela, inclua `options=-crow_security=off` na string de conexão; se um proprietário da tabela adicionar uma política de segurança de linha, essa configuração fará com que a replicação seja interrompida em vez de executar a política. O acesso para o papel deve ser configurado em `pg_hba.conf` e deve ter o atributo `LOGIN`.

Para poder copiar os dados iniciais da tabela, o papel usado para a conexão de replicação deve ter o privilégio `SELECT` em uma tabela publicada (ou ser um superusuário).

Para criar uma publicação, o usuário deve ter o privilégio `CREATE` no banco de dados.

Para adicionar tabelas a uma publicação, o usuário deve ter direitos de propriedade na tabela. Para adicionar todas as tabelas do esquema a uma publicação, o usuário deve ser um superusuário. Para criar uma publicação que publique todas as tabelas ou todas as tabelas do esquema automaticamente, o usuário deve ser um superusuário.

Atualmente, não há privilégios em publicações. Qualquer assinatura (que seja capaz de se conectar) pode acessar qualquer publicação. Portanto, se você pretende ocultar alguma informação de assinantes específicos, como usando filtros de linha ou listas de colunas, ou não adicionando toda a tabela à publicação, esteja ciente de que outras publicações no mesmo banco de dados podem expor as mesmas informações. Privilegios de publicação podem ser adicionados ao PostgreSQL no futuro para permitir um controle de acesso mais detalhado.

Para criar uma assinatura, o usuário deve ter os privilégios do papel `pg_create_subscription`, bem como os privilégios `CREATE` no banco de dados.

O processo de aplicação da assinatura aplicará, em nível de sessão, os privilégios do proprietário da assinatura. No entanto, ao realizar uma operação de inserção, atualização, exclusão ou truncar em uma tabela específica, ele mudará para o papel do proprietário da tabela e realizará a operação com os privilégios do proprietário da tabela. Isso significa que o proprietário da assinatura precisa ser capaz de `SET ROLE` para cada papel que possui uma tabela replicada.

Se a assinatura tiver sido configurada com `run_as_owner = true`, então não ocorrerá troca de usuário. Em vez disso, todas as operações serão realizadas com as permissões do proprietário da assinatura. Neste caso, o proprietário da assinatura só precisa de privilégios para `SELECT`, `INSERT`, `UPDATE` e `DELETE` da tabela de destino, e não precisa de privilégios para `SET ROLE` para o proprietário da tabela. No entanto, isso também significa que qualquer usuário que possua uma tabela na qual a replicação está acontecendo pode executar código arbitrário com os privilégios do proprietário da assinatura. Por exemplo, eles poderiam fazer isso simplesmente anexando um gatilho a uma das tabelas que eles possuem. Como geralmente é indesejável permitir que um papel assuma livremente os privilégios de outro, essa opção deve ser evitada, a menos que a segurança do usuário dentro do banco de dados não seja de importância.

Quanto ao editor, os privilégios são verificados apenas uma vez no início de uma conexão de replicação e não são verificados novamente à medida que cada registro de alteração é lido.

No assinante, os privilégios do proprietário da assinatura são verificados novamente para cada transação quando aplicada. Se um trabalhador estiver em processo de aplicação de uma transação quando a propriedade da assinatura é alterada por uma transação concorrente, a aplicação da transação atual continuará sob os privilégios do antigo proprietário.