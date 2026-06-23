## 52.15. `pg_database` [#](#CATALOG-PG-DATABASE)

O catálogo `pg_database` armazena informações sobre os bancos de dados disponíveis. Os bancos de dados são criados com o comando [`CREATE DATABASE`](sql-createdatabase.md "CREATE DATABASE"). Consulte o [Capítulo 22](managing-databases.md "Chapter 22. Managing Databases") para obter detalhes sobre o significado de alguns dos parâmetros.

Ao contrário da maioria dos catálogos de sistema, o `pg_database` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_database` por clúster, não uma por banco de dados.

**Tabela 52.15. Colunas `pg_database`**



<table border="1" class="table" summary="pg_database Columns">
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="catalog_table_entry">
    <p class="column_definition">
     Tipo de coluna
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      oid
     </code>
     <code class="type">
      oid
     </code>
    </p>
    <p>
     Identificador da linha
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datdba
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code class="structname">
       pg_authid
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Proprietário do banco de dados, geralmente o usuário que o criou
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      encoding
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Codificação de caracteres para este banco de dados (
     <a class="link" href="functions-info.md#PG-ENCODING-TO-CHAR">
      <code class="function">
       pg_encoding_to_char()
      </code>
     </a>
     pode traduzir esse número para o nome do codificação)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datlocprovider
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Fornecedora de localização para este banco de dados:
     <code class="literal">
      b
     </code>
     = embutido,
     <code class="literal">
      c
     </code>
     = libc,
     <code class="literal">
      i
     </code>
     = icu
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datistemplate
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Se for verdade, então esse banco de dados pode ser clonado por qualquer usuário com
     <code class="literal">
      CREATEDB
     </code>
     privilegios; se falso, então apenas superusuários ou o proprietário do banco de dados podem cloná-lo.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datallowconn
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Se falso, então ninguém pode se conectar a este banco de dados. Isso é usado para proteger
     <code class="literal">
      template0
     </code>
     para que o banco de dados não seja alterado.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      dathasloginevt
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     Indica que há gatilhos de eventos de login definidos para este banco de dados. Essa bandeira é usada para evitar pesquisas extras no
     <code class="structname">
      pg_event_trigger
     </code>
     tabela durante cada inicialização do backend. Essa bandeira é usada internamente pelo
     <span class="productname">
      PostgreSQL
     </span>
     e não deve ser alterado manualmente ou lido para fins de monitoramento.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datconnlimit
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Define o número máximo de conexões concorrentes que podem ser feitas com este banco de dados. -1 significa sem limite, -2 indica que o banco de dados é inválido.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datfrozenxid
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     Todos os IDs de transação antes deste foram substituídos por um permanente (
     <span class="quote">
      “
      <span class="quote">
       congelado
      </span>
      ”
     </span>
     ) ID de transação neste banco de dados. Isso é usado para rastrear se o banco de dados precisa ser aspirado para evitar o envolvimento do ID de transação ou para permitir
     <code class="literal">
      pg_xact
     </code>
     para ser reduzido. É o mínimo por tabela
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      relfrozenxid
     </code>
     values.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datminmxid
     </code>
     <code class="type">
      xid
     </code>
    </p>
    <p>
     Todos os IDs multixact anteriores a este foram substituídos por um ID de transação neste banco de dados. Isso é usado para rastrear se o banco de dados precisa ser aspirado para evitar o envolvimento de IDs multixact ou para permitir
     <code class="literal">
      pg_multixact
     </code>
     para ser reduzido. É o mínimo por tabela
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      relminmxid
     </code>
     values.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      dattablespace
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-tablespace.md" title="52.56. pg_tablespace">
      <code class="structname">
       pg_tablespace
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O espaço de tabela padrão para o banco de dados. Dentro deste banco de dados, todas as tabelas para as quais
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      reltablespace
     </code>
     é zero; será armazenado neste espaço de tabela; em particular, todos os catálogos do sistema não compartilhados estarão lá.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datcollate
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     LC_COLLATE para este banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datctype
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     LC_CTYPE para este banco de dados
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datlocale
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Nome do local do provedor de cotação para este banco de dados. Se o provedor for
     <code class="literal">
      libc
     </code>
     ,
     <code class="structfield">
      datlocale
     </code>
     é
     <code class="literal">
      NULL
     </code>
     ;
     <code class="structfield">
      datcollate
     </code>
     e
     <code class="structfield">
      datctype
     </code>
     são utilizados em vez disso.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      daticurules
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Regras de agregação de banco de dados de UTI
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datcollversion
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     Versão específica do fornecedor da codificação. Isso é registrado quando o banco de dados é criado e, em seguida, verificado quando é usado, para detectar alterações na definição da codificação que possam levar à corrupção dos dados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      datacl
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
 </tbody>
</table>





