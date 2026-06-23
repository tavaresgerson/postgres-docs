## 5.9. Políticas de Segurança de Linha [#](#DDL-ROWSECURITY)

Além do sistema de privilégios padrão SQL [(ddl-priv.md "5.8. Privileges")], disponível através de [GRANT][(sql-grant.md "GRANT"), as tabelas podem ter *políticas de segurança de linha* que restringem, em uma base por usuário, quais linhas podem ser devolvidas por consultas normais ou inseridas, atualizadas ou excluídas por comandos de modificação de dados. Esse recurso também é conhecido como *Segurança de Nível de Linha*. Por padrão, as tabelas não têm nenhuma política, de modo que, se um usuário tiver privilégios de acesso a uma tabela de acordo com o sistema de privilégios SQL, todas as linhas dentro dela estarão igualmente disponíveis para consulta ou atualização.

Quando a segurança de linha é habilitada em uma tabela (com [ALTER TABLE ... ENABLE ROW LEVEL SECURITY](sql-altertable.md "ALTER TABLE")), todo acesso normal à tabela para seleção de linhas ou modificação de linhas deve ser permitido por uma política de segurança de linha. (No entanto, o proprietário da tabela normalmente não está sujeito a políticas de segurança de linha.) Se não existir nenhuma política para a tabela, uma política de negação padrão é usada, o que significa que nenhuma linha é visível ou pode ser modificada. Operações que se aplicam a toda a tabela, como `TRUNCATE` e `REFERENCES`, não estão sujeitas à segurança de linha.

As políticas de segurança de linha podem ser específicas para comandos, ou para papéis, ou para ambos. Uma política pode ser especificada para aplicar a comandos `ALL`, ou para `SELECT`, `INSERT`, `UPDATE` ou `DELETE`. Múltiplos papéis podem ser atribuídos a uma política dada, e as regras normais de associação e herança de papel se aplicam.

Para especificar quais linhas são visíveis ou modificáveis de acordo com uma política, é necessária uma expressão que retorne um resultado booleano. Essa expressão será avaliada para cada linha antes de quaisquer condições ou funções provenientes da consulta do usuário. (As únicas exceções a essa regra são as funções `leakproof`, que são garantidas para não vazarem informações; o otimizador pode optar por aplicar tais funções antes da verificação de segurança da linha.) As linhas para as quais a expressão não retorne `true` não serão processadas. Expressões separadas podem ser especificadas para fornecer controle independente sobre as linhas que são visíveis e as linhas que são permitidas para serem modificadas. As expressões de política são executadas como parte da consulta e com os privilégios do usuário que executa a consulta, embora funções definidoras de segurança possam ser usadas para acessar dados não disponíveis para o usuário que realiza a chamada.

Superusuários e papéis com o atributo `BYPASSRLS` sempre ignoram o sistema de segurança de linha ao acessar uma tabela. Os proprietários da tabela normalmente ignoram a segurança de linha também, embora um proprietário de tabela possa optar por estar sujeito à segurança de nível de linha com [ALTER TABLE ... FORÇA SEGURANÇA EM NÍVEL DE LINHA](sql-altertable.md "ALTER TABLE").

Ativar e desativar a segurança de linha, bem como adicionar políticas a uma tabela, é sempre o privilégio exclusivo do proprietário da tabela.

As políticas são criadas usando o comando [CREATE POLICY](sql-createpolicy.md "CREATE POLICY") e alteradas usando o comando [ALTER POLICY](sql-alterpolicy.md "ALTER POLICY"). E removidas usando o comando [DROP POLICY](sql-droppolicy.md "DROP POLICY"). Para habilitar e desabilitar a segurança de linha para uma tabela específica, use o comando [ALTER TABLE](sql-altertable.md "ALTER TABLE").

Cada política tem um nome e várias políticas podem ser definidas para uma tabela. Como as políticas são específicas para a tabela, cada política para uma tabela deve ter um nome único. Tabelas diferentes podem ter políticas com o mesmo nome.

Quando várias políticas se aplicam a uma consulta específica, elas são combinadas usando `OR` (para políticas permissivas, que são a opção padrão) ou usando `AND` (para políticas restritivas). O comportamento do `OR` é semelhante à regra de que um determinado papel tem os privilégios de todos os papéis dos quais é membro. Políticas permissivas vs. restritivas são discutidas mais abaixo.

Como exemplo simples, veja como criar uma política na relação `account` para permitir que apenas membros do papel `managers` acessem as linhas e apenas as linhas de suas contas:

```
CREATE TABLE accounts (manager text, company text, contact_email text);

ALTER TABLE accounts ENABLE ROW LEVEL SECURITY;

CREATE POLICY account_managers ON accounts TO managers
    USING (manager = current_user);
```

A política acima implícita fornece uma cláusula `WITH CHECK` idêntica à sua cláusula `USING`, de modo que a restrição se aplique tanto a linhas selecionadas por um comando (para que um gerente não possa `SELECT`, `UPDATE` ou `DELETE`, existindo linhas pertencentes a um gerente diferente) quanto a linhas modificadas por um comando (para que linhas pertencentes a um gerente diferente não possam ser criadas por meio de `INSERT` ou `UPDATE`).

Se não for especificado um papel, ou o nome especial do usuário `PUBLIC` for usado, então a política se aplica a todos os usuários do sistema. Para permitir que todos os usuários acessem apenas sua própria linha em uma tabela `users`, uma política simples pode ser usada:

```
CREATE POLICY user_policy ON users
    USING (user_name = current_user);
```

Isso funciona de maneira semelhante ao exemplo anterior.

Para usar uma política diferente para as linhas que estão sendo adicionadas à tabela em comparação com as linhas visíveis, várias políticas podem ser combinadas. Este par de políticas permitiria que todos os usuários visualizassem todas as linhas da tabela `users`, mas apenas modificassem as suas próprias:

```
CREATE POLICY user_sel_policy ON users
    FOR SELECT
    USING (true);
CREATE POLICY user_mod_policy ON users
    USING (user_name = current_user);
```

Em um comando `SELECT`, essas duas políticas são combinadas usando `OR`, com o efeito líquido sendo que todas as linhas podem ser selecionadas. Em outros tipos de comando, apenas a segunda política se aplica, de modo que os efeitos são os mesmos que antes.

A segurança de linha também pode ser desativada com o comando `ALTER TABLE`. Desativar a segurança de linha não remove quaisquer políticas que estejam definidas na tabela; elas são simplesmente ignoradas. Em seguida, todas as linhas da tabela são visíveis e modificáveis, sujeitas ao sistema padrão de privilégios SQL.

Abaixo, há um exemplo maior de como esse recurso pode ser usado em ambientes de produção. A tabela `passwd` emula um arquivo de senha Unix:

```
-- Simple passwd-file based example
CREATE TABLE passwd (
  user_name             text UNIQUE NOT NULL,
  pwhash                text,
  uid                   int  PRIMARY KEY,
  gid                   int  NOT NULL,
  real_name             text NOT NULL,
  home_phone            text,
  extra_info            text,
  home_dir              text NOT NULL,
  shell                 text NOT NULL
);

CREATE ROLE admin;  -- Administrator
CREATE ROLE bob;    -- Normal user
CREATE ROLE alice;  -- Normal user

-- Populate the table
INSERT INTO passwd VALUES
  ('admin','xxx',0,0,'Admin','111-222-3333',null,'/root','/bin/dash');
INSERT INTO passwd VALUES
  ('bob','xxx',1,1,'Bob','123-456-7890',null,'/home/bob','/bin/zsh');
INSERT INTO passwd VALUES
  ('alice','xxx',2,1,'Alice','098-765-4321',null,'/home/alice','/bin/zsh');

-- Be sure to enable row-level security on the table
ALTER TABLE passwd ENABLE ROW LEVEL SECURITY;

-- Create policies
-- Administrator can see all rows and add any rows
CREATE POLICY admin_all ON passwd TO admin USING (true) WITH CHECK (true);
-- Normal users can view all rows
CREATE POLICY all_view ON passwd FOR SELECT USING (true);
-- Normal users can update their own records, but
-- limit which shells a normal user is allowed to set
CREATE POLICY user_mod ON passwd FOR UPDATE
  USING (current_user = user_name)
  WITH CHECK (
    current_user = user_name AND
    shell IN ('/bin/bash','/bin/sh','/bin/dash','/bin/zsh','/bin/tcsh')
  );

-- Allow admin all normal rights
GRANT SELECT, INSERT, UPDATE, DELETE ON passwd TO admin;
-- Users only get select access on public columns
GRANT SELECT
  (user_name, uid, gid, real_name, home_phone, extra_info, home_dir, shell)
  ON passwd TO public;
-- Allow users to update certain columns
GRANT UPDATE
  (pwhash, real_name, home_phone, extra_info, shell)
  ON passwd TO public;
```

Como em qualquer configuração de segurança, é importante testar e garantir que o sistema esteja funcionando conforme o esperado. Usando o exemplo acima, isso demonstra que o sistema de permissão está funcionando corretamente.

```
-- admin can view all rows and fields
postgres=> set role admin;
SET
postgres=> table passwd;
 user_name | pwhash | uid | gid | real_name |  home_phone  | extra_info | home_dir    |   shell
-----------+--------+-----+-----+-----------+--------------+------------+-------------+-----------
 admin     | xxx    |   0 |   0 | Admin     | 111-222-3333 |            | /root       | /bin/dash
 bob       | xxx    |   1 |   1 | Bob       | 123-456-7890 |            | /home/bob   | /bin/zsh
 alice     | xxx    |   2 |   1 | Alice     | 098-765-4321 |            | /home/alice | /bin/zsh
(3 rows)

-- Test what Alice is able to do
postgres=> set role alice;
SET
postgres=> table passwd;
ERROR:  permission denied for table passwd
postgres=> select user_name,real_name,home_phone,extra_info,home_dir,shell from passwd;
 user_name | real_name |  home_phone  | extra_info | home_dir    |   shell
-----------+-----------+--------------+------------+-------------+-----------
 admin     | Admin     | 111-222-3333 |            | /root       | /bin/dash
 bob       | Bob       | 123-456-7890 |            | /home/bob   | /bin/zsh
 alice     | Alice     | 098-765-4321 |            | /home/alice | /bin/zsh
(3 rows)

postgres=> update passwd set user_name = 'joe';
ERROR:  permission denied for table passwd
-- Alice is allowed to change her own real_name, but no others
postgres=> update passwd set real_name = 'Alice Doe';
UPDATE 1
postgres=> update passwd set real_name = 'John Doe' where user_name = 'admin';
UPDATE 0
postgres=> update passwd set shell = '/bin/xx';
ERROR:  new row violates WITH CHECK OPTION for "passwd"
postgres=> delete from passwd;
ERROR:  permission denied for table passwd
postgres=> insert into passwd (user_name) values ('xxx');
ERROR:  permission denied for table passwd
-- Alice can change her own password; RLS silently prevents updating other rows
postgres=> update passwd set pwhash = 'abc';
UPDATE 1
```

Todas as políticas construídas até agora foram políticas permissivas, o que significa que, quando várias políticas são aplicadas, elas são combinadas usando o operador booleano "OU". Embora políticas permissivas possam ser construídas para permitir apenas o acesso a linhas nos casos pretendidos, pode ser mais simples combinar políticas permissivas com políticas restritivas (que os registros devem passar e que são combinadas usando o operador booleano "E"). Baseando-se no exemplo acima, adicionamos uma política restritiva para exigir que o administrador esteja conectado através de um socket Unix local para acessar os registros da tabela `passwd`:

```
CREATE POLICY admin_local_only ON passwd AS RESTRICTIVE TO admin
    USING (pg_catalog.inet_client_addr() IS NULL);
```

Podemos então perceber que um administrador que se conecta através de uma rede não verá nenhum registro, devido à política restritiva:

```
=> SELECT current_user;
 current_user
--------------
 admin
(1 row)

=> select inet_client_addr();
 inet_client_addr
------------------
 127.0.0.1
(1 row)

=> TABLE passwd;
 user_name | pwhash | uid | gid | real_name | home_phone | extra_info | home_dir | shell
-----------+--------+-----+-----+-----------+------------+------------+----------+-------
(0 rows)

=> UPDATE passwd set pwhash = NULL;
UPDATE 0
```

Os controles de integridade referencial, como restrições de chave primária única ou de chave estrangeira, sempre ignoram a segurança de linha para garantir que a integridade dos dados seja mantida. É necessário ter cuidado ao desenvolver esquemas e políticas de nível de linha para evitar vazamentos de "canal oculto" de informações por meio desses controles de integridade referencial.

Em alguns contextos, é importante garantir que a segurança de linha não esteja sendo aplicada. Por exemplo, ao fazer um backup, poderia ser desastroso se a segurança de linha silencialmente causar a omissão de algumas linhas do backup. Nessa situação, você pode definir o parâmetro de configuração [row_security](runtime-config-client.md#GUC-ROW-SECURITY) para `off`. Isso não elimina a segurança de linha por si só; o que ele faz é lançar um erro se os resultados de qualquer consulta forem filtrados por uma política. O motivo do erro pode então ser investigado e corrigido.

Nos exemplos acima, as expressões de política consideram apenas os valores atuais na linha a ser acessada ou atualizada. Este é o caso mais simples e de melhor desempenho; quando possível, é melhor projetar aplicativos de segurança de linha para funcionar dessa maneira. Se for necessário consultar outras linhas ou outras tabelas para tomar uma decisão de política, isso pode ser realizado usando sub`SELECT`s ou funções que contenham `SELECT`s, nas expressões de política. No entanto, esteja ciente de que tais acessos podem criar condições de corrida que poderiam permitir vazamento de informações se não for tomado cuidado. Como exemplo, considere o seguinte desenho de tabela:

```
-- definition of privilege groups
CREATE TABLE groups (group_id int PRIMARY KEY,
                     group_name text NOT NULL);

INSERT INTO groups VALUES
  (1, 'low'),
  (2, 'medium'),
  (5, 'high');

GRANT ALL ON groups TO alice;  -- alice is the administrator
GRANT SELECT ON groups TO public;

-- definition of users' privilege levels
CREATE TABLE users (user_name text PRIMARY KEY,
                    group_id int NOT NULL REFERENCES groups);

INSERT INTO users VALUES
  ('alice', 5),
  ('bob', 2),
  ('mallory', 2);

GRANT ALL ON users TO alice;
GRANT SELECT ON users TO public;

-- table holding the information to be protected
CREATE TABLE information (info text,
                          group_id int NOT NULL REFERENCES groups);

INSERT INTO information VALUES
  ('barely secret', 1),
  ('slightly secret', 2),
  ('very secret', 5);

ALTER TABLE information ENABLE ROW LEVEL SECURITY;

-- a row should be visible to/updatable by users whose security group_id is
-- greater than or equal to the row's group_id
CREATE POLICY fp_s ON information FOR SELECT
  USING (group_id <= (SELECT group_id FROM users WHERE user_name = current_user));
CREATE POLICY fp_u ON information FOR UPDATE
  USING (group_id <= (SELECT group_id FROM users WHERE user_name = current_user));

-- we rely only on RLS to protect the information table
GRANT ALL ON information TO public;
```

Agora, suponha que `alice` queira alterar as informações “pouco secretas”, mas decida que `mallory` não deve ser confiada com o novo conteúdo daquela linha, então ela faz isso:

```
BEGIN;
UPDATE users SET group_id = 1 WHERE user_name = 'mallory';
UPDATE information SET info = 'secret from mallory' WHERE group_id = 2;
COMMIT;
```

Isso parece seguro; não há uma janela na qual `mallory` deveria ser capaz de ver a string "segredo de mallory". No entanto, há uma condição de corrida aqui. Se `mallory` estiver fazendo, por exemplo,

```
SELECT * FROM information WHERE group_id = 2 FOR UPDATE;
```

e sua transação está no modo `READ COMMITTED`, é possível para ela ver “segredo de Mallory”. Isso acontece se sua transação atingir a linha `information` logo após a de `alice`. Isso bloqueia a espera pela transação de `alice`, e depois recupera os conteúdos atualizados da linha graças à cláusula `FOR UPDATE`. No entanto, ela *não* recupera uma linha atualizada para o `SELECT` implícito de `users`, porque esse sub-`SELECT` não tinha `FOR UPDATE`; em vez disso, a linha `users` é lida com o instantâneo tomado no início da consulta. Portanto, a expressão de política testa o valor antigo do nível de privilégio de `mallory` e permite que ela veja a linha atualizada.

Existem várias maneiras de contornar esse problema. Uma resposta simples é usar `SELECT ... FOR SHARE` em sub`SELECT`s em políticas de segurança de linha. No entanto, isso exige conceder o privilégio `UPDATE` na tabela referenciada (aqui `users`) aos usuários afetados, o que pode ser indesejável. (Mas outra política de segurança de linha pode ser aplicada para impedir que eles realmente exerçam esse privilégio; ou o sub`SELECT` pode ser incorporado em uma função de definidor de segurança.) Além disso, o uso pesado de bloqueios de compartilhamento de linha na tabela referenciada pode representar um problema de desempenho, especialmente se as atualizações forem frequentes. Outra solução, prática se as atualizações da tabela referenciada forem infrequentes, é tomar um bloqueio `ACCESS EXCLUSIVE` na tabela referenciada ao atualizá-la, para que nenhuma transação concorrente possa examinar os valores antigos da linha. Ou pode-se simplesmente esperar que todas as transações concorrentes terminem após o compromisso de uma atualização da tabela referenciada e antes de fazer alterações que dependem da nova situação de segurança.

Para obter informações adicionais, consulte [CREATE POLICY](sql-createpolicy.md "CREATE POLICY") e [ALTER TABLE](sql-altertable.md "ALTER TABLE").