## 52.28. `pg_init_privs` [#](#CATALOG-PG-INIT-PRIVS)

O catálogo `pg_init_privs` registra informações sobre os privilégios iniciais dos objetos no sistema. Há uma entrada para cada objeto no banco de dados que possui um conjunto inicial de privilégios não padrão (não nulo).

Os objetos podem ter privilégios iniciais, seja por terem esses privilégios definidos quando o sistema é inicializado (pelo initdb) ou quando o objeto é criado durante um `CREATE EXTENSION` e o script de extensão define os privilégios iniciais usando o sistema `GRANT` e (sql-grant.md "GRANT"). Note que o sistema irá registrar automaticamente os privilégios durante o script de extensão e que os autores de extensão precisam apenas usar as declarações `GRANT` e `REVOKE` em seu script para que os privilégios sejam registrados. A coluna `privtype` indica se o privilégio inicial foi definido pelo initdb ou durante um comando `CREATE EXTENSION`.

Os objetos que possuem privilégios iniciais definidos por initdb terão entradas onde `privtype` é `'i'`, enquanto os objetos que possuem privilégios iniciais definidos por `CREATE EXTENSION` terão entradas onde `privtype` é `'e'`.

**Tabela 52.28. Colunas `pg_init_privs`**



<table border="1" class="table" summary="pg_init_privs Columns">
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
      objoid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto específico
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      classoid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do catálogo do sistema que o objeto está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objsubid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Para uma coluna de tabela, este é o número da coluna (o
     <code class="structfield">
      objoid
     </code>
     e
     <code class="structfield">
      classoid
     </code>
     refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      privtype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Um código que define o tipo de privilégio inicial deste objeto; veja o texto
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      initprivs
     </code>
     <code class="type">
      aclitem[]
     </code>
    </p>
    <p>
     Os privilégios de acesso inicial; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
 </tbody>
</table>




