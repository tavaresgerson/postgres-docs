### 5.8. Privilegios [#](#DDL-PRIV)

Quando um objeto é criado, ele é atribuído a um proprietário. O proprietário é normalmente o papel que executou a declaração de criação. Para a maioria dos tipos de objetos, o estado inicial é que apenas o proprietário (ou um superusuário) pode fazer qualquer coisa com o objeto. Para permitir que outros papéis o usem, *privilegios* devem ser concedidos.

Existem diferentes tipos de privilégios: `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE`, `REFERENCES`, `TRIGGER`, `CREATE`, `CONNECT`, `TEMPORARY`, `EXECUTE`, `USAGE`, `SET`, `ALTER SYSTEM` e `MAINTAIN`. Os privilégios aplicáveis a um objeto específico variam dependendo do tipo do objeto (tabela, função, etc.). Mais detalhes sobre os significados desses privilégios aparecem abaixo. As seções e capítulos seguintes também mostrarão como esses privilégios são usados.

O direito de modificar ou destruir um objeto é inerente ao fato de ser o proprietário do objeto e não pode ser concedido ou revogado por si só. (No entanto, como todos os privilégios, esse direito pode ser herdado por membros do papel de proprietário; veja [Seção 21.3](role-membership.md).

Um objeto pode ser atribuído a um novo proprietário com um comando `ALTER` do tipo apropriado para o objeto, por exemplo

```
ALTER TABLE table_name OWNER TO new_owner;
```

Os superusuários sempre podem fazer isso; os papéis comuns só podem fazer isso se forem ambos os proprietários atuais do objeto (ou herdar os privilégios do papel proprietário) e capazes de `SET ROLE` para o novo papel proprietário. Todos os privilégios do objeto do antigo proprietário são transferidos para o novo proprietário juntamente com a propriedade.

Para atribuir privilégios, o comando [GRANT](sql-grant.md) é utilizado. Por exemplo, se `joe` é um papel existente e `accounts` é uma tabela existente, o privilégio de atualizar a tabela pode ser concedido com:

```
GRANT UPDATE ON accounts TO joe;
```

Escrever `ALL` no lugar de um privilégio específico concede todos os privilégios que são relevantes para o tipo de objeto.

O nome especial “role” `PUBLIC` pode ser usado para conceder privilégios a todos os roles do sistema. Além disso, os roles de “grupo” podem ser configurados para ajudar a gerenciar privilégios quando há muitos usuários de um banco de dados — para detalhes, consulte [Capítulo 21](user-manag.md).

Para revogar um privilégio concedido anteriormente, use o comando apropriadamente chamado [REVOKE](sql-revoke.md):

```
REVOKE ALL ON accounts FROM PUBLIC;
```

Normalmente, apenas o proprietário do objeto (ou um usuário super) pode conceder ou revogar privilégios em um objeto. No entanto, é possível conceder um privilégio “com opção de concessão”, que dá ao destinatário o direito de concedê-lo por sua vez a outros. Se a opção de concessão for subsequentemente revogada, todos os que receberam o privilégio desse destinatário (diretamente ou através de uma cadeia de concessões) perderão o privilégio. Para detalhes, consulte as páginas de referência [GRANT](sql-grant.md "GRANT") e [REVOKE](sql-revoke.md "REVOKE").

O proprietário de um objeto pode optar por revogar seus próprios privilégios comuns, por exemplo, tornar uma tabela somente de leitura para si mesmo e para outros. Mas os proprietários são sempre tratados como tendo todas as opções de concessão, então eles sempre podem re conceder seus próprios privilégios.

Os privilégios disponíveis são:

`SELECT` [#](#DDL-PRIV-SELECT): Permite `SELECT` de qualquer coluna, ou colunas específicas, de uma tabela, visual, visual materializada ou outro objeto semelhante a uma tabela. Também permite o uso de `COPY TO`. Este privilégio também é necessário para referenciar valores de coluna existentes em `UPDATE`, `DELETE` ou `MERGE`. Para sequências, este privilégio também permite o uso da função `currval`. Para objetos grandes, este privilégio permite que o objeto seja lido.

`INSERT` [#](#DDL-PRIV-INSERT): Permite `INSERT` de uma nova linha em uma tabela, visualização, etc. Pode ser concedida em uma coluna específica, no caso, apenas essas colunas podem ser atribuídas no comando `INSERT` (os outros colunas, portanto, receberão valores padrão). Também permite o uso de `COPY FROM`.

`UPDATE` [#](#DDL-PRIV-UPDATE): Permite `UPDATE` de qualquer coluna, ou colunas específicas, de uma tabela, visualização, etc. (Na prática, qualquer comando `UPDATE` não trivial exigirá também o privilégio `SELECT`, uma vez que deve referenciar colunas da tabela para determinar quais linhas devem ser atualizadas e/ou para calcular novos valores para colunas.) Os privilégios `SELECT ... FOR UPDATE` e `SELECT ... FOR SHARE` também exigem este privilégio em pelo menos uma coluna, além do privilégio `SELECT`. Para sequências, este privilégio permite o uso das funções `nextval` e `setval`. Para objetos grandes, este privilégio permite a escrita ou truncar o objeto.

`DELETE` [#](#DDL-PRIV-DELETE): Permite `DELETE` de uma linha de uma tabela, visão, etc. (Na prática, qualquer comando `DELETE` não trivial exigirá também `SELECT` privilégio, uma vez que deve referenciar colunas da tabela para determinar quais linhas devem ser excluídas.)

`TRUNCATE` [#](#DDL-PRIV-TRUNCATE): Permite `TRUNCATE` em uma tabela.

`REFERENCES` [#](#DDL-PRIV-REFERENCES): Permite a criação de uma restrição de chave estrangeira que faz referência a uma tabela ou a uma coluna específica de uma tabela.

`TRIGGER` [#](#DDL-PRIV-TRIGGER): Permite a criação de um gatilho em uma tabela, visualização, etc.

`CREATE` [#](#DDL-PRIV-CREATE): Para bancos de dados, permite que novos esquemas e publicações sejam criados dentro do banco de dados e permite que extensões confiáveis sejam instaladas dentro do banco de dados.

Para esquemas, permite que novos objetos sejam criados dentro do esquema. Para renomear um objeto existente, você deve possuir o objeto *e* ter esse privilégio para o esquema contendo.

Para tablespaces, permite que tabelas, índices e arquivos temporários sejam criados dentro do tablespace e permite que sejam criados bancos de dados que tenham o tablespace como seu tablespace padrão.

Observe que a revogação deste privilégio não alterará a existência ou localização dos objetos existentes.

`CONNECT` [#](#DDL-PRIV-CONNECT): Permite que o beneficiário se conecte ao banco de dados. Este privilégio é verificado na inicialização da conexão (ainda que verifique quaisquer restrições impostas por `pg_hba.conf`).

`TEMPORARY` [#](#DDL-PRIV-TEMPORARY): Permite a criação de tabelas temporárias durante o uso do banco de dados.

`EXECUTE` [#](#DDL-PRIV-EXECUTE): Permite chamar uma função ou procedimento, incluindo o uso de quaisquer operadores que sejam implementados em cima da função. Este é o único tipo de privilégio que é aplicável a funções e procedimentos.

`USAGE` [#](#DDL-PRIV-USAGE): Para linguagens procedurais, permite o uso da linguagem para a criação de funções nessa linguagem. Esse é o único tipo de privilégio aplicável a linguagens procedurais.

Para esquemas, permite o acesso a objetos contidos no esquema (assumindo que os requisitos de privilégio próprios dos objetos também sejam atendidos). Essencialmente, isso permite que o beneficiário "pesquise" objetos dentro do esquema. Sem essa permissão, ainda é possível ver os nomes dos objetos, por exemplo, realizando consultas em catálogos do sistema. Além disso, após revogar essa permissão, as sessões existentes podem ter declarações que realizaram essa pesquisa anteriormente, portanto, essa não é uma maneira completamente segura de impedir o acesso a objetos.

Para sequências, permite o uso das funções `currval` e `nextval`.

Para tipos e domínios, permite o uso do tipo ou domínio na criação de tabelas, funções e outros objetos do esquema. (Observe que este privilégio não controla todo o "uso" do tipo, como os valores do tipo que aparecem em consultas. Ele apenas impede que objetos sejam criados que dependem do tipo. O principal propósito deste privilégio é controlar quais usuários podem criar dependências em um tipo, o que poderia impedir que o proprietário altere o tipo posteriormente.)

Para os wrappers de dados estrangeiros, permite a criação de novos servidores usando o wrapper de dados estrangeiros.

Para servidores estrangeiros, permite a criação de tabelas estrangeiras usando o servidor. Os beneficiários também podem criar, alterar ou descartar seus próprios mapeamentos de usuário associados a esse servidor.

`SET` [#](#DDL-PRIV-SET): Permite que um parâmetro de configuração do servidor seja definido com um novo valor dentro da sessão atual. (Embora este privilégio possa ser concedido em qualquer parâmetro, ele não tem significado, exceto para os parâmetros que normalmente requerem privilégio de superusuário para ser definido.)

`ALTER SYSTEM` [#](#DDL-PRIV-ALTER-SYSTEM): Permite que um parâmetro de configuração do servidor seja configurado para um novo valor usando o comando [ALTER SYSTEM](sql-altersystem.md "ALTER SYSTEM").

`MAINTAIN` [#](#DDL-PRIV-MAINTAIN): Permite a manipulação de estatísticas de objetos de banco de dados `VACUUM`, `ANALYZE`, `CLUSTER`, `REFRESH MATERIALIZED VIEW`, `REINDEX`, `LOCK TABLE` e funções de manipulação de estatísticas de objetos de banco de dados (consulte [Tabela 9.105](functions-admin.md#FUNCTIONS-ADMIN-STATSMOD "Table 9.105. Database Object Statistics Manipulation Functions")) em uma relação.

Os privilégios necessários para outros comandos estão listados na página de referência do respectivo comando.

O PostgreSQL concede privilégios em alguns tipos de objetos ao `PUBLIC` por padrão quando os objetos são criados. Não são concedidos privilégios ao `PUBLIC` por padrão em tabelas, colunas de tabela, sequências, wrappers de dados externos, servidores externos, objetos grandes, esquemas, espaços de tabela ou parâmetros de configuração. Para outros tipos de objetos, os privilégios concedidos por padrão ao `PUBLIC` são os seguintes: privilégios de `CONNECT` e `TEMPORARY` (criar tabelas temporárias) para bancos de dados; privilégio de `EXECUTE` para funções e procedimentos; e privilégio de `USAGE` para linguagens e tipos de dados (incluindo domínios). O proprietário do objeto, é claro, pode `REVOKE` tanto os privilégios concedidos por padrão quanto os expressamente concedidos. (Para máxima segurança, emita o `REVOKE` na mesma transação que cria o objeto; então não há janela em que outro usuário pode usar o objeto.) Além disso, esses ajustes de privilégios padrão podem ser ignorados usando o comando [ALTER DEFAULT PRIVILEGES](sql-alterdefaultprivileges.md "ALTER DEFAULT PRIVILEGES").

[Tabela 5.1](ddl-priv.md#PRIVILEGE-ABBREVS-TABLE) mostra as abreviações de uma letra que são usadas para esses tipos de privilégio nos valores de *ACL*. Você verá essas letras na saída dos comandos [psql](app-psql.md) listados abaixo, ou ao olhar nas colunas ACL dos catálogos do sistema.

**Tabela 5.1. Abreviações de privilégios do ACL**

<table border="1" class="table" summary="ACL Privilege Abbreviations">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Privilege
   </th>
   <th>
    Abbreviation
   </th>
   <th>
    Tipos de Objeto Aplicáveis
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     SELECT
    </code>
   </td>
   <td>
    <code class="literal">
     r
    </code>
    (
    <span class="quote">
     “
     <span class="quote">
      read
     </span>
     ”
    </span>
    )
   </td>
   <td>
    <code class="literal">
     LARGE OBJECT
    </code>
    ,
    <code class="literal">
     SEQUENCE
    </code>
    ,
    <code class="literal">
     TABLE
    </code>
    (e objetos semelhantes a uma mesa), coluna de tabela
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     INSERT
    </code>
   </td>
   <td>
    <code class="literal">
     a
    </code>
    (
    <span class="quote">
     “
     <span class="quote">
      append
     </span>
     ”
    </span>
    )
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
    , coluna de tabela
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     UPDATE
    </code>
   </td>
   <td>
    <code class="literal">
     w
    </code>
    (
    <span class="quote">
     “
     <span class="quote">
      write
     </span>
     ”
    </span>
    )
   </td>
   <td>
    <code class="literal">
     LARGE OBJECT
    </code>
    ,
    <code class="literal">
     SEQUENCE
    </code>
    ,
    <code class="literal">
     TABLE
    </code>
    , , coluna de tabela
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DELETE
    </code>
   </td>
   <td>
    <code class="literal">
     d
    </code>
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TRUNCATE
    </code>
   </td>
   <td>
    <code class="literal">
     D
    </code>
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     REFERENCES
    </code>
   </td>
   <td>
    <code class="literal">
     x
    </code>
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
    , coluna de tabela
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TRIGGER
    </code>
   </td>
   <td>
    <code class="literal">
     t
    </code>
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CREATE
    </code>
   </td>
   <td>
    <code class="literal">
     C
    </code>
   </td>
   <td>
    <code class="literal">
     DATABASE
    </code>
    ,
    <code class="literal">
     SCHEMA
    </code>
    ,
    <code class="literal">
     TABLESPACE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     CONNECT
    </code>
   </td>
   <td>
    <code class="literal">
     c
    </code>
   </td>
   <td>
    <code class="literal">
     DATABASE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TEMPORARY
    </code>
   </td>
   <td>
    <code class="literal">
     T
    </code>
   </td>
   <td>
    <code class="literal">
     DATABASE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     EXECUTE
    </code>
   </td>
   <td>
    <code class="literal">
     X
    </code>
   </td>
   <td>
    <code class="literal">
     FUNCTION
    </code>
    ,
    <code class="literal">
     PROCEDURE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     USAGE
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     DOMAIN
    </code>
    ,
    <code class="literal">
     FOREIGN DATA WRAPPER
    </code>
    ,
    <code class="literal">
     FOREIGN SERVER
    </code>
    ,
    <code class="literal">
     LANGUAGE
    </code>
    ,
    <code class="literal">
     SCHEMA
    </code>
    ,
    <code class="literal">
     SEQUENCE
    </code>
    ,
    <code class="literal">
     TYPE
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SET
    </code>
   </td>
   <td>
    <code class="literal">
     s
    </code>
   </td>
   <td>
    <code class="literal">
     PARAMETER
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     ALTER SYSTEM
    </code>
   </td>
   <td>
    <code class="literal">
     A
    </code>
   </td>
   <td>
    <code class="literal">
     PARAMETER
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     MAINTAIN
    </code>
   </td>
   <td>
    <code class="literal">
     m
    </code>
   </td>
   <td>
    <code class="literal">
     TABLE
    </code>
   </td>
  </tr>
 </tbody>
</table>

[Tabela 5.2](ddl-priv.md#PRIVILEGES-SUMMARY-TABLE) resume os privilégios disponíveis para cada tipo de objeto SQL, usando as abreviações mostradas acima. Também mostra o comando psql que pode ser usado para examinar as configurações de privilégios para cada tipo de objeto.

**Tabela 5.2. Resumo dos privilégios de acesso**

<table border="1" class="table" summary="Summary of Access Privileges">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
  <col class="col3"/>
  <col class="col4"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Object Type
   </th>
   <th>
    All Privileges
   </th>
   <th>
    Default
    <code class="literal">
     PUBLIC
    </code>
    Privileges
   </th>
   <th>
    <span class="application">
     psql
    </span>
    Command
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     DATABASE
    </code>
   </td>
   <td>
    <code class="literal">
     CTc
    </code>
   </td>
   <td>
    <code class="literal">
     Tc
    </code>
   </td>
   <td>
    <code class="literal">
     \l
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     DOMAIN
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     \dD+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     FUNCTION
    </code>
    or
    <code class="literal">
     PROCEDURE
    </code>
   </td>
   <td>
    <code class="literal">
     X
    </code>
   </td>
   <td>
    <code class="literal">
     X
    </code>
   </td>
   <td>
    <code class="literal">
     \df+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     FOREIGN DATA WRAPPER
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dew+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     FOREIGN SERVER
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \des+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LANGUAGE
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     \dL+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     LARGE OBJECT
    </code>
   </td>
   <td>
    <code class="literal">
     rw
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dl+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     PARAMETER
    </code>
   </td>
   <td>
    <code class="literal">
     sA
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dconfig+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SCHEMA
    </code>
   </td>
   <td>
    <code class="literal">
     UC
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dn+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     SEQUENCE
    </code>
   </td>
   <td>
    <code class="literal">
     rwU
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dp
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TABLE
    </code>
    (and table-like objects)
   </td>
   <td>
    <code class="literal">
     arwdDxtm
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dp
    </code>
   </td>
  </tr>
  <tr>
   <td>
    Table column
   </td>
   <td>
    <code class="literal">
     arwx
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \dp
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TABLESPACE
    </code>
   </td>
   <td>
    <code class="literal">
     C
    </code>
   </td>
   <td>
    none
   </td>
   <td>
    <code class="literal">
     \db+
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     TYPE
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     U
    </code>
   </td>
   <td>
    <code class="literal">
     \dT+
    </code>
   </td>
  </tr>
 </tbody>
</table>

Os privilégios que foram concedidos para um objeto específico são exibidos como uma lista de entradas `aclitem`, cada uma com o formato:

```
grantee=privilege-abbreviation[*].../grantor
```

Cada `aclitem` lista todos os permissões de um beneficiário que foram concedidas por um concedente específico. Privilegios específicos são representados por abreviações de uma letra da [Tabela 5.1](ddl-priv.md#PRIVILEGE-ABBREVS-TABLE "Table 5.1. ACL Privilege Abbreviations"), com `*` anexado se o privilégio foi concedido com opção de concessão. Por exemplo, `calvin=r*w/hobbes` especifica que o papel `calvin` tem o privilégio `SELECT` (`r`) com opção de concessão (`*`) e também o privilégio não concedível `UPDATE` (`w`), ambos concedidos pelo papel `hobbes`. Se `calvin` também tem alguns privilégios no mesmo objeto concedidos por um concedente diferente, esses aparecem como uma entrada `aclitem` separada. Um campo de beneficiário vazio em um `aclitem` representa `PUBLIC`.

Como exemplo, suponha que o usuário `miriam` crie a tabela `mytable` e faça:

```
GRANT SELECT ON mytable TO PUBLIC;
GRANT SELECT, UPDATE, INSERT ON mytable TO admin;
GRANT SELECT (col1), UPDATE (col1) ON mytable TO miriam_rw;
```

Então o comando `\dp` do psql mostraria:

```
=> \dp mytable
                                  Access privileges
 Schema |  Name   | Type  |   Access privileges    |   Column privileges   | Policies
--------+---------+-------+------------------------+-----------------------+----------
 public | mytable | table | miriam=arwdDxtm/miriam+| col1:                +|
        |         |       | =r/miriam             +|   miriam_rw=rw/miriam |
        |         |       | admin=arw/miriam       |                       |
(1 row)
```

Se a coluna “Privilegios de acesso” estiver vazia para um objeto específico, isso significa que o objeto tem privilégios padrão (ou seja, sua entrada de privilégios no catálogo do sistema relevante é nula). Os privilégios padrão sempre incluem todos os privilégios do proprietário e podem incluir alguns privilégios para `PUBLIC` dependendo do tipo do objeto, conforme explicado acima. O primeiro `GRANT` ou `REVOKE` em um objeto instanciará os privilégios padrão (produzindo, por exemplo, `miriam=arwdDxt/miriam`) e, em seguida, os modificará de acordo com a solicitação especificada. Da mesma forma, as entradas são mostradas na “Colunas de privilégios” apenas para colunas com privilégios não padrão. (Nota: para este propósito, “privilégios padrão” sempre significa os privilégios padrão embutidos para o tipo do objeto. Um objeto cujos privilégios foram afetados por um comando `ALTER DEFAULT PRIVILEGES` será sempre mostrado com uma entrada de privilégio explícita que inclui os efeitos do `ALTER`.)

Observe que as opções de concessão implícita do proprietário não são marcadas na exibição de privilégios de acesso. Um `*` aparecerá apenas quando as opções de concessão foram explicitamente concedidas a alguém.

A coluna “Privilegios de acesso” exibe `(none)` quando a entrada de privilégios do objeto não é nula, mas está vazia. Isso significa que não são concedidos privilégios, mesmo para o proprietário do objeto — uma situação rara. (O proprietário ainda tem opções de concessão implícita neste caso, e pode, portanto, reconceder seus próprios privilégios; mas não tem nenhum no momento.)