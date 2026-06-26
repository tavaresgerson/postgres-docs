## 52.35. `pg_opfamily` [#](#CATALOG-PG-OPFAMILY)

O catálogo `pg_opfamily` define as famílias de operadores. Cada família de operadores é uma coleção de operadores e rotinas de suporte associadas que implementam a semântica especificada para um método de acesso a índice particular. Além disso, os operadores em uma família são todos “compatíveis”, de uma maneira especificada pelo método de acesso. O conceito de família de operadores permite que operadores de diferentes tipos de dados sejam usados com índices e que seja razoável usar o conhecimento da semântica do método de acesso.

As famílias de operadores são descritas em detalhes na [Seção 36.16](xindex.md).

**Tabela 52.35. Colunas `pg_opfamily`**



<table>
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
     <code>
      oid
     </code>
     <code>
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
     <code>
      opfmethod
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-am.md" title="52.3. pg_am">
      <code>
       pg_am
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O método de acesso ao índice é para a família de operadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opfname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome desta família de operadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opfnamespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Nomes de domínio desta família de operadores
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opfowner
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
      <code>
       pg_authid
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Proprietário da família operadora
    </p>
   </td>
  </tr>
 </tbody>
</table>










A maioria das informações que definem uma família de operadores não está na sua linha `pg_opfamily`, mas nas linhas associadas em [`pg_amop`](catalog-pg-amop.md "52.4. pg_amop"), [`pg_amproc`](catalog-pg-amproc.md "52.5. pg_amproc") e [`pg_opclass`](catalog-pg-opclass.md "52.33. pg_opclass").