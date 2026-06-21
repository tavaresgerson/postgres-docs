## 52.48. `pg_shdepend` [#](#CATALOG-PG-SHDEPEND)

O catálogo `pg_shdepend` registra as relações de dependência entre objetos do banco de dados e objetos compartilhados, como papéis. Essas informações permitem que o PostgreSQL garanta que esses objetos não estejam referenciados antes de tentar excluí-los.

Veja também `pg_depend`(catalog-pg-depend.md "52.18. pg_depend"), que realiza uma função semelhante para dependências que envolvem objetos dentro de um único banco de dados.

Ao contrário da maioria dos catálogos de sistema, o `pg_shdepend` é compartilhado em todos os bancos de dados de um clúster: há apenas uma cópia do `pg_shdepend` por clúster, não uma por banco de dados.

**Tabela 52.48. Colunas `pg_shdepend`**



<table border="1" class="table" summary="pg_shdepend Columns">
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
      dbid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-database.md" title="52.15. pg_database">
      <code class="structname">
       pg_database
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do banco de dados no qual o objeto dependente está, ou zero para um objeto compartilhado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      classid
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
     O OID do catálogo do sistema que o objeto dependente está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto dependente específico
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
      objid
     </code>
     e
     <code class="structfield">
      classid
     </code>
     refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      refclassid
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
     O OID do catálogo do sistema que o objeto referenciado está em (deve ser um catálogo compartilhado)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      refobjid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto específico referido
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      deptype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Um código que defina a semântica específica dessa relação de dependência; veja o texto
    </p>
   </td>
  </tr>
 </tbody>
</table>









Em todos os casos, uma entrada `pg_shdepend` indica que o objeto referenciado não pode ser descartado sem também descartar o objeto dependente. No entanto, existem vários subsabores identificados por `deptype`:

`SHARED_DEPENDENCY_OWNER` (`o`): O objeto referenciado (que deve ser um papel) é o proprietário do objeto dependente.

`SHARED_DEPENDENCY_ACL` (`a`): O objeto referido (que deve ser um papel) é mencionado na ACL do objeto dependente. (Uma entrada `SHARED_DEPENDENCY_ACL` não é feita para o proprietário do objeto, uma vez que o proprietário terá uma entrada `SHARED_DEPENDENCY_OWNER` de qualquer forma.)

`SHARED_DEPENDENCY_INITACL` (`i`): O objeto referido (que deve ser um papel) é mencionado em uma entrada [`pg_init_privs`](catalog-pg-init-privs.md "52.28. pg_init_privs") para o objeto dependente.

`SHARED_DEPENDENCY_POLICY` (`r`): O objeto referido (que deve ser um papel) é mencionado como o alvo de um objeto de política dependente.

`SHARED_DEPENDENCY_TABLESPACE` (`t`): O objeto mencionado (que deve ser um tablespace) é mencionado como o tablespace para uma relação que não tem armazenamento.

Outros sabores de dependência podem ser necessários no futuro. Note, em particular, que a definição atual só suporta papéis e espaços de tabela como objetos referenciados.

Assim como no catálogo `pg_depend`, a maioria dos objetos criados durante o initdb são considerados “fixados”. Não são feitas entradas no `pg_shdepend` que tenham um objeto fixado como objeto referenciado ou dependente.