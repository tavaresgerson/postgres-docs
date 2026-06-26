## F.40. sepgsql — Módulo de segurança de controle de acesso obrigatório (MAC) baseado em rótulos SELinux [#](#SEPGSQL)

* [F.40.1. Visão geral](sepgsql.md#SEPGSQL-OVERVIEW)
* [F.40.2. Instalação](sepgsql.md#SEPGSQL-INSTALLATION)
* [F.40.3. Testes de regressão](sepgsql.md#SEPGSQL-REGRESSION)
* [F.40.4. Parâmetros do GUC](sepgsql.md#SEPGSQL-PARAMETERS)
* [F.40.5. Recursos](sepgsql.md#SEPGSQL-FEATURES)
* [F.40.6. Funções Sepgsql](sepgsql.md#SEPGSQL-FUNCTIONS)
* [F.40.7. Limitações](sepgsql.md#SEPGSQL-LIMITATIONS)
* [F.40.8. Recursos externos](sepgsql.md#SEPGSQL-RESOURCES)
* [F.40.9. Autor](sepgsql.md#SEPGSQL-AUTHOR)

`sepgsql` é um módulo carregável que suporta controle de acesso obrigatório baseado em rótulos (MAC) baseado na política de segurança SELinux.

### Aviso

A implementação atual tem limitações significativas e não aplica o controle de acesso obrigatório para todas as ações. Veja [Seção F.40.7](sepgsql.md#SEPGSQL-LIMITATIONS).

### F.40.1. Visão geral [#](#SEPGSQL-OVERVIEW)

Este módulo se integra ao SELinux para fornecer uma camada adicional de verificação de segurança acima do que normalmente é fornecido pelo PostgreSQL. Do ponto de vista do SELinux, este módulo permite que o PostgreSQL funcione como um gerenciador de objetos de espaço de usuário. Cada acesso a tabela ou função iniciado por uma consulta DML será verificado em relação à política de segurança do sistema. Esta verificação é adicional à verificação usual de permissões SQL realizada pelo PostgreSQL.

As decisões de controle de acesso do SELinux são feitas usando rótulos de segurança, que são representados por cadeias de caracteres, como `system_u:object_r:sepgsql_table_t:s0`. Cada decisão de controle de acesso envolve dois rótulos: o rótulo do sujeito que está tentando realizar a ação e o rótulo do objeto sobre o qual a operação deve ser realizada. Como esses rótulos podem ser aplicados a qualquer tipo de objeto, as decisões de controle de acesso para objetos armazenados no banco de dados podem ser (e, com este módulo, são) sujeitas aos mesmos critérios gerais usados para objetos de qualquer outro tipo, como arquivos. Esse projeto visa permitir uma política de segurança centralizada para proteger ativos de informações independentemente dos detalhes de como esses ativos são armazenados.

A declaração `SECURITY LABEL` permite a atribuição de uma etiqueta de segurança a um objeto de banco de dados.

### F.40.2. Instalação [#](#SEPGSQL-INSTALLATION)

`sepgsql` só pode ser usado em Linux 2.6.28 ou superior com SELinux habilitado. Não está disponível em nenhuma outra plataforma. Você também precisará do libselinux 2.1.10 ou superior e selinux-policy 3.9.13 ou superior (embora algumas distribuições possam retroceder as regras necessárias para versões de políticas mais antigas).

O comando `sestatus` permite que você verifique o status do SELinux. Um exemplo típico é:

```
$ sestatus
SELinux status:                 enabled
SELinuxfs mount:                /selinux
Current mode:                   enforcing
Mode from config file:          enforcing
Policy version:                 24
Policy from config file:        targeted
```

Se o SELinux estiver desativado ou não instalado, você deve configurá-lo primeiro antes de instalar este módulo.

Para construir este módulo, especifique `--with-selinux` (install-make.md#CONFIGURE-OPTION-WITH-SEPGSQL) (ao usar [make e autoconf](install-make.md "17.3. Building and Installation with Autoconf and Make")) ou `-Dselinux={ auto | enabled | disabled }` (install-meson.md#CONFIGURE-WITH-SEPGSQL-MESON) (ao usar [meson](install-meson.md "17.4. Building and Installation with Meson")). Certifique-se de que o RPM `libselinux-devel` esteja instalado no momento da construção.

Para usar este módulo, você deve incluir `sepgsql` no parâmetro [shared_preload_libraries](runtime-config-client.md#GUC-SHARED-PRELOAD-LIBRARIES) em `postgresql.conf`. O módulo não funcionará corretamente se carregado de qualquer outra maneira. Uma vez que o módulo seja carregado, você deve executar `sepgsql.sql` em cada banco de dados. Isso instalará as funções necessárias para a gestão de etiquetas de segurança e atribuirá etiquetas de segurança iniciais.

Aqui está um exemplo que mostra como inicializar um novo cluster de banco de dados com funções `sepgsql` e rótulos de segurança instalados. Ajuste as permissões mostradas conforme necessário para sua instalação:

```
$ export PGDATA=/path/to/data/directory
$ initdb
$ vi $PGDATA/postgresql.conf
  change
    #shared_preload_libraries = ''                # (change requires restart)
  to
    shared_preload_libraries = 'sepgsql'          # (change requires restart)
$ for DBNAME in template0 template1 postgres; do
    postgres --single -F -c exit_on_error=true $DBNAME \
      </usr/local/pgsql/share/contrib/sepgsql.sql >/dev/null
  done
```

Por favor, note que você pode ver algumas ou todas as seguintes notificações, dependendo das versões específicas que você tem do libselinux e do selinux-policy:

```
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 33 has invalid object type db_blobs
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 36 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 37 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 38 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 39 has invalid object type db_language
/etc/selinux/targeted/contexts/sepgsql_contexts:  line 40 has invalid object type db_language
```

Essas mensagens são inofensivas e devem ser ignoradas.

Se o processo de instalação for concluído sem erros, você pode começar a usar o servidor normalmente.

### F.40.3. Testes de Regressão [#](#SEPGSQL-REGRESSION)

A `sepgsql` é executada se `PG_TEST_EXTRA` contém `sepgsql` (consulte [Seção 31.1.3](regress-run.md#REGRESS-ADDITIONAL)). Este método é adequado durante o desenvolvimento do PostgreSQL. Alternativamente, há uma maneira de executar os testes para verificar se uma instância do banco de dados foi configurada corretamente para `sepgsql`.

Devido à natureza do SELinux, a execução dos testes de regressão para `sepgsql` requer várias etapas de configuração adicionais, algumas das quais devem ser feitas como root.

Os testes manuais devem ser executados no diretório `contrib/sepgsql` de uma árvore de construção configurada do PostgreSQL. Embora eles exijam uma árvore de construção, os testes são projetados para serem executados contra um servidor instalado, ou seja, são comparáveis a `make installcheck` e não a `make check`.

Primeiro, configure o `sepgsql` em um banco de dados funcional de acordo com as instruções na [Seção F.40.2](sepgsql.md#SEPGSQL-INSTALLATION). Observe que o usuário do sistema operacional atual deve ser capaz de se conectar ao banco de dados como superusuário sem autenticação por senha.

Em segundo lugar, construa e instale o pacote de políticas para o teste de regressão. O pacote de políticas `sepgsql-regtest` é um pacote de políticas com finalidade específica que fornece um conjunto de regras que devem ser permitidas durante os testes de regressão. Ele deve ser construído a partir do arquivo de fonte de políticas `sepgsql-regtest.te`, que é feito usando `make` com um Makefile fornecido pelo SELinux. Você precisará localizar o Makefile apropriado em seu sistema; o caminho mostrado abaixo é apenas um exemplo. (Este Makefile é geralmente fornecido pelo `selinux-policy-devel` ou `selinux-policy` RPM.) Uma vez construído, instale este pacote de políticas usando o comando `semodule`, que carrega os pacotes de políticas fornecidos no kernel. Se o pacote for instalado corretamente, `semodule -l` deve listar `sepgsql-regtest` como um pacote de políticas disponível:

```
$ cd .../contrib/sepgsql
$ make -f /usr/share/selinux/devel/Makefile
$ sudo semodule -u sepgsql-regtest.pp
$ sudo semodule -l | grep sepgsql
sepgsql-regtest 1.07
```

Em terceiro lugar, ative `sepgsql_regression_test_mode`. Por razões de segurança, as regras em `sepgsql-regtest` não são ativadas por padrão; o parâmetro `sepgsql_regression_test_mode` habilita as regras necessárias para iniciar os testes de regressão. Pode ser ativado usando o comando `setsebool`:

```
$ sudo setsebool sepgsql_regression_test_mode on
$ getsebool sepgsql_regression_test_mode
sepgsql_regression_test_mode --> on
```

Em quarto lugar, verifique se sua concha está operando no domínio `unconfined_t`:

```
$ id -Z
unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
```

Consulte [Seção F.40.8](sepgsql.md#SEPGSQL-RESOURCES) para obter detalhes sobre a configuração do seu domínio de trabalho, se necessário.

Por fim, execute o script de teste de regressão:

```
$ ./test_sepgsql
```

Este script tentará verificar se você realizou todos os passos de configuração corretamente, e, em seguida, executará os testes de regressão para o módulo `sepgsql`.

Após completar os testes, é recomendável desabilitar o parâmetro `sepgsql_regression_test_mode`:

```
$ sudo setsebool sepgsql_regression_test_mode off
```

Você pode preferir remover completamente a política `sepgsql-regtest`:

```
$ sudo semodule -r sepgsql-regtest
```

### F.40.4. Parâmetros do GUC [#](#SEPGSQL-PARAMETERS)

`sepgsql.permissive` (`boolean`) [#](#GUC-SEPGSQL-PERMISSIVE): Este parâmetro permite que o `sepgsql` funcione no modo permissivo, independentemente da configuração do sistema. O padrão é desligado. Este parâmetro só pode ser definido no arquivo `postgresql.conf` ou na linha de comando do servidor.

Quando este parâmetro está ativado, o `sepgsql` funciona no modo permissivo, mesmo que o SELinux, em geral, esteja funcionando no modo de aplicação. Este parâmetro é principalmente útil para fins de teste.

`sepgsql.debug_audit` (`boolean`) [#](#GUC-SEPGSQL-DEBUG-AUDIT): Este parâmetro permite a impressão de mensagens de auditoria, independentemente das configurações da política do sistema. O padrão é desligado, o que significa que as mensagens serão impressas de acordo com as configurações do sistema.

A política de segurança do SELinux também tem regras para controlar se certos acessos são registrados ou não. Por padrão, as violações de acesso são registradas, mas os acessos permitidos não são.

Este parâmetro força a ativação de todas as possíveis registos, independentemente da política do sistema.

### F.40.5. Características [#](#SEPGSQL-FEATURES)

#### F.40.5.1. Classes de Objetos Controlados [#](#SEPGSQL-FEATURES-CONTROLLED-OBJ-CLASSES)

O modelo de segurança do SELinux descreve todas as regras de controle de acesso como relações entre uma entidade de sujeito (tipicamente, um cliente do banco de dados) e uma entidade de objeto (como um objeto do banco de dados), cada uma das quais é identificada por uma etiqueta de segurança. Se o acesso a um objeto não rotulado for tentado, o objeto é tratado como se tivesse sido atribuído a etiqueta `unlabeled_t`.

Atualmente, `sepgsql` permite que rótulos de segurança sejam atribuídos a esquemas, tabelas, colunas, sequências, visualizações e funções. Quando o `sepgsql` está em uso, os rótulos de segurança são automaticamente atribuídos aos objetos de banco de dados suportados no momento da criação. Esse rótulo é chamado de rótulo de segurança padrão e é decidido de acordo com a política de segurança do sistema, que leva como entrada a etiqueta do criador, a etiqueta atribuída ao objeto pai do novo objeto e, opcionalmente, o nome do objeto construído.

Um novo objeto de banco de dados basicamente herda a etiqueta de segurança do objeto pai, exceto quando a política de segurança tem regras especiais conhecidas como regras de transição de tipo, caso em que uma etiqueta diferente pode ser aplicada. Para esquemas, o objeto pai é o banco de dados atual; para tabelas, sequências, visualizações e funções, é o esquema contendo; para colunas, é a tabela contendo.

#### F.40.5.2. Permissões de DML [#](#SEPGSQL-FEATURES-DML-PERMISSIONS)

Para tabelas, `db_table:select`, `db_table:insert`, `db_table:update` ou `db_table:delete` são verificados para todas as tabelas-alvo referenciadas, dependendo do tipo de declaração; além disso, `db_table:select` também é verificado para todas as tabelas que contêm colunas referenciadas na cláusula `WHERE` ou `RETURNING`, como fonte de dados para `UPDATE`, e assim por diante.

As permissões de nível de coluna também serão verificadas para cada coluna referenciada. `db_column:select` é verificado não apenas nas colunas que estão sendo lidas usando `SELECT`, mas também nas que estão sendo referenciadas em outras declarações DML; `db_column:update` ou `db_column:insert` também serão verificados para colunas que estão sendo modificadas por `UPDATE` ou `INSERT`.

Por exemplo, considere:

```
UPDATE t1 SET x = 2, y = func1(y) WHERE z = 100;
```

Aqui, `db_column:update` será verificado em `t1.x`, uma vez que está sendo atualizado, `db_column:{select update}` será verificado em `t1.y`, uma vez que está tanto atualizado quanto referenciado, e `db_column:select` será verificado em `t1.z`, uma vez que está apenas referenciado. `db_table:{select update}` também será verificado no nível da tabela.

Para sequências, `db_sequence:get_value` é verificado quando referenciamos um objeto de sequência usando `SELECT`; no entanto, observe que, atualmente, não verificamos permissões na execução de funções correspondentes, como `lastval()`.

Para visualizações, `db_view:expand` será verificado, e, em seguida, quaisquer outras permissões necessárias serão verificadas nos objetos que estão sendo expandidos a partir da visualização, individualmente.

Para funções, `db_procedure:{execute}` será verificado quando o usuário tenta executar uma função como parte de uma consulta ou usando invocação de caminho rápido. Se essa função for um procedimento confiável, também verificará a permissão `db_procedure:{entrypoint}` para verificar se pode ser o ponto de entrada de um procedimento confiável.

Para acessar qualquer objeto do esquema, é necessária a permissão `db_schema:search` no esquema contendo. Quando um objeto é referenciado sem qualificação de esquema, os esquemas nos quais essa permissão não está presente não serão pesquisados (assim como se o usuário não tivesse privilégio `USAGE` no esquema). Se uma qualificação explícita de esquema estiver presente, ocorrerá um erro se o usuário não tiver a permissão necessária no esquema nomeado.

O cliente deve ter acesso a todas as tabelas e colunas referenciadas, mesmo que elas tenham origem em visualizações que foram posteriormente expandidas, para que possamos aplicar regras de controle de acesso consistentes, independentemente da maneira como o conteúdo da tabela é referenciado.

O sistema de privilégios padrão do banco de dados permite que os superusuários do banco de dados modifiquem catálogos do sistema usando comandos DML e refiram ou modifiquem tabelas de toast. Essas operações são proibidas quando o `sepgsql` está habilitado.

#### F.40.5.3. Permissões de DDL [#](#SEPGSQL-FEATURES-DDL-PERMISSIONS)

O SELinux define várias permissões para controlar operações comuns para cada tipo de objeto; como criação, alteração, eliminação e rerotulagem de rótulos de segurança. Além disso, vários tipos de objetos têm permissões especiais para controlar suas operações características; como adição ou eliminação de entradas de nome dentro de um esquema específico.

Para criar um novo objeto de banco de dados, é necessário o `create` permissão. O SELinux concederá ou negará essa permissão com base na etiqueta de segurança do cliente e na etiqueta de segurança proposta para o novo objeto. Em alguns casos, são necessários privilégios adicionais:

* `CREATE DATABASE` (sql-createdatabase.md "CREATE DATABASE") também requer permissão `getattr` para o banco de dados de origem ou modelo.
* A criação de um objeto de esquema também requer `add_name` permissão no esquema pai.
* A criação de uma tabela também requer permissão para criar cada coluna de tabela individualmente, assim como se cada coluna de tabela fosse um objeto separado de nível superior.
* A criação de uma função marcada como `LEAKPROOF` também requer `install` permissão. (Esta permissão também é verificada quando `LEAKPROOF` é definida para uma função existente.)

Quando o comando `DROP` é executado, `drop` será verificado no objeto que está sendo removido. As permissões também serão verificadas para objetos que foram descartados indiretamente por meio de `CASCADE`. A exclusão de objetos contidos em um esquema específico (tabelas, visualizações, sequências e procedimentos) requer adicionalmente `remove_name` no esquema.

Quando o comando `ALTER` é executado, `setattr` será verificado no objeto que está sendo modificado para cada tipo de objeto, exceto para objetos subsidiários, como índices ou gatilhos de uma tabela, onde as permissões são verificadas, em vez disso, no objeto pai. Em alguns casos, são necessárias permissões adicionais:

* Para mover um objeto para um novo esquema, é necessário também o `remove_name` de permissão no esquema antigo e o `add_name` de permissão no novo.
* Para definir o atributo `LEAKPROOF` em uma função, é necessário o `install` de permissão.
* Usar `SECURITY LABEL`(sql-security-label.md "SECURITY LABEL") em um objeto também requer o `relabelfrom` de permissão para o objeto em conjunto com sua antiga etiqueta de segurança e o `relabelto` de permissão para o objeto em conjunto com sua nova etiqueta de segurança. (Nos casos em que vários provedores de etiquetas são instalados e o usuário tenta definir uma etiqueta de segurança, mas não é gerenciada pelo SELinux, apenas o `setattr` deve ser verificado aqui. Isso atualmente não é feito devido a restrições de implementação.)

#### F.40.5.4. Procedimentos confiáveis [#](#SEPGSQL-FEATURES-TRUSTED-PROCEDURES)

Procedimentos confiáveis são semelhantes a funções de definição de segurança ou comandos setuid. O SELinux oferece uma característica que permite que códigos confiáveis sejam executados usando uma etiqueta de segurança diferente da do cliente, geralmente para o propósito de fornecer acesso altamente controlado a dados sensíveis (por exemplo, as linhas podem ser omitidas ou a precisão dos valores armazenados pode ser reduzida). Se uma função atua ou não como um procedimento confiável é controlado por sua etiqueta de segurança e a política de segurança do sistema operacional. Por exemplo:

```
postgres=# CREATE TABLE customer (
               cid     int primary key,
               cname   text,
               credit  text
           );
CREATE TABLE
postgres=# SECURITY LABEL ON COLUMN customer.credit
               IS 'system_u:object_r:sepgsql_secret_table_t:s0';
SECURITY LABEL
postgres=# CREATE FUNCTION show_credit(int) RETURNS text
             AS 'SELECT regexp_replace(credit, ''-[0-9]+$'', ''-xxxx'', ''g'')
                        FROM customer WHERE cid = $1'
           LANGUAGE sql;
CREATE FUNCTION
postgres=# SECURITY LABEL ON FUNCTION show_credit(int)
               IS 'system_u:object_r:sepgsql_trusted_proc_exec_t:s0';
SECURITY LABEL
```

As operações acima devem ser realizadas por um usuário administrativo.

```
postgres=# SELECT * FROM customer;
ERROR:  SELinux: security policy violation
postgres=# SELECT cid, cname, show_credit(cid) FROM customer;
 cid | cname  |     show_credit
-----+--------+---------------------
   1 | taro   | 1111-2222-3333-xxxx
   2 | hanako | 5555-6666-7777-xxxx
(2 rows)
```

Neste caso, um usuário comum não pode fazer referência diretamente a `customer.credit`, mas um procedimento confiável `show_credit` permite que o usuário imprima os números dos cartões de crédito dos clientes, com alguns dos dígitos mascarados.

#### F.40.5.5. Transformações dinâmicas de domínio [#](#SEPGSQL-FEATURES-DYNAMIC-DOMAIN-TRANSITIONS)

É possível usar o recurso de transição dinâmica de domínio do SELinux para mudar o rótulo de segurança do processo do cliente, o domínio do cliente, para um novo contexto, se isso for permitido pela política de segurança. O domínio do cliente precisa da permissão `setcurrent` e também `dyntransition` do antigo para o novo domínio.

As transições dinâmicas de domínio devem ser consideradas com cuidado, pois permitem que os usuários mudem sua etiqueta e, portanto, seus privilégios, a seu critério, e não (como no caso de um procedimento confiável) conforme exigido pelo sistema. Assim, a permissão `dyntransition` é considerada segura apenas quando usada para mudar para um domínio com um conjunto menor de privilégios do que o original. Por exemplo:

```
regression=# select sepgsql_getcon();
                    sepgsql_getcon
-------------------------------------------------------
 unconfined_u:unconfined_r:unconfined_t:s0-s0:c0.c1023
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c4');
 sepgsql_setcon
----------------
 t
(1 row)

regression=# SELECT sepgsql_setcon('unconfined_u:unconfined_r:unconfined_t:s0-s0:c1.c1023');
ERROR:  SELinux: security policy violation
```

Neste exemplo acima, fomos autorizados a mudar da faixa maior do MCS `c1.c1023` para a faixa menor `c1.c4`, mas a mudança de volta foi negada.

Uma combinação de transição dinâmica de domínio e procedimento confiável permite um caso de uso interessante que se encaixa no ciclo de vida típico do software de pool de conexões. Mesmo que seu software de pool de conexões não seja autorizado a executar a maioria dos comandos SQL, você pode permitir que ele mude o rótulo de segurança do cliente usando a função `sepgsql_setcon()` dentro de um procedimento confiável; isso deve exigir algumas credenciais para autorizar a solicitação de mudança do rótulo do cliente. Depois disso, essa sessão terá os privilégios do usuário alvo, em vez do pool de conexões. O pool de conexões pode, posteriormente, reverter a mudança do rótulo de segurança usando novamente a `sepgsql_setcon()` com o argumento `NULL`, novamente invocado dentro de um procedimento confiável com verificações de permissões apropriadas. O ponto aqui é que apenas o procedimento confiável tem permissão para mudar o rótulo de segurança efetivo e só faz isso quando recebe as credenciais apropriadas. Claro, para operação segura, o armazenamento de credenciais (tabela, definição de procedimento ou o que for) deve ser protegido contra acesso não autorizado.

#### F.40.5.6. Diversos [#](#SEPGSQL-FEATURES-MISC)

Recusamos o comando `LOAD`(sql-load.md "LOAD") em todos os casos, porque qualquer módulo carregado poderia facilmente contornar a aplicação da política de segurança.

### F.40.6. Funções Sepgsql [#](#SEPGSQL-FUNCTIONS)

[Tabela F.32](sepgsql.md#SEPGSQL-FUNCTIONS-TABLE "Table F.32. Sepgsql Functions") mostra as funções disponíveis.

**Tabela F.32. Funções Sepgsql**



<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sepgsql_getcon
     </code>
     () →
     <code>
      text
     </code>
    </p>
    <p>
     Returns the client domain, the current security label of the client.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sepgsql_setcon
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Switches the client domain of the current session to the new domain, if allowed by the security policy. It also accepts
     <code>
      NULL
     </code>
     input as a request to transition to the client's original domain.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sepgsql_mcstrans_in
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Translates the given qualified MLS/MCS range into raw format if the mcstrans daemon is running.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sepgsql_mcstrans_out
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      text
     </code>
    </p>
    <p>
     Translates the given raw MLS/MCS range into qualified format if the mcstrans daemon is running.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      sepgsql_restorecon
     </code>
     (
     <code>
      text
     </code>
     ) →
     <code>
      boolean
     </code>
    </p>
    <p>
     Sets up initial security labels for all objects within the current database. The argument may be
     <code>
      NULL
     </code>
     , or the name of a specfile to be used as alternative of the system default.
    </p>
   </td>
  </tr>
 </tbody>
</table>







### F.40.7. Limitações [#](#SEPGSQL-LIMITATIONS)

Permissões de Linguagem de Definição de Dados (DDL): Devido a restrições de implementação, algumas operações de DDL não verificam permissões.

Permissões do Data Control Language (DCL): Devido às restrições de implementação, as operações do DCL não verificam permissões.

Controle de acesso em nível de linha: o PostgreSQL suporta acesso em nível de linha, mas o `sepgsql`

Canais ocultos: `sepgsql` não tenta esconder a existência de um determinado objeto, mesmo que o usuário não tenha permissão para referenciá-lo. Por exemplo, podemos inferir a existência de um objeto invisível como resultado de conflitos de chave primária, violações de chave estrangeira, e assim por diante, mesmo que não possamos obter o conteúdo do objeto. A existência de uma tabela de sigilo máximo não pode ser escondida; apenas esperamos ocultar seu conteúdo.

### F.40.8. Recursos externos [#](#SEPGSQL-RESOURCES)

[Introdução ao PostgreSQL](https://wiki.postgresql.org/wiki/SEPostgreSQL_Introduction): Esta página do wiki fornece uma breve visão geral, projeto de segurança, arquitetura, administração e recursos futuros.

[Guia do Usuário e do Administrador do SELinux](https://access.redhat.com/documentation/en-us/red_hat_enterprise_linux/7/html/selinux_users_and_administrators_guide/index): Este documento fornece um amplo espectro de conhecimento para administrar o SELinux em seus sistemas. Ele se concentra principalmente em sistemas operacionais Red Hat, mas não se limita a eles.

[FAQ do SELinux do Fedora](https://fedoraproject.org/wiki/SELinux_FAQ): Este documento responde a perguntas frequentes sobre o SELinux. Ele se concentra principalmente no Fedora, mas não se limita ao Fedora.

### F.40.9. Autor [#](#SEPGSQL-AUTHOR)

KaiGai Kohei `<kaigai@ak.jp.nec.com>`