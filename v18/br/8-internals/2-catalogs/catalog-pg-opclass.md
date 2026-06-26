## 52.33. `pg_opclass` [#](#CATALOG-PG-OPCLASS)

O catálogo `pg_opclass` define as classes de operadores de método de acesso a índice. Cada classe de operador define a semântica para as colunas de índice de um tipo de dados particular e um método de acesso a índice particular. Uma classe de operador especifica essencialmente que uma família particular de operadores é aplicável a um tipo de dados de coluna indexável particular. O conjunto de operadores da família que são realmente utilizáveis com o tipo de dados de coluna indexável são aqueles que aceitam o tipo de dados da coluna como sua entrada à esquerda.

As classes de operador são descritas em detalhes na [Seção 36.16](xindex.md).

**Tabela 52.33. Colunas `pg_opclass`**



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
      opcmethod
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
     Classe do operador do método de acesso ao índice é para
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome desta classe de operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcnamespace
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
     Nomes de espaço deste operador de classe
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcowner
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
     Proprietário da classe de operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcfamily
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-opfamily.md" title="52.35. pg_opfamily">
      <code>
       pg_opfamily
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Família de operadores que contém a classe de operador
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcintype
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados que o operador de classe indexa
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opcdefault
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se esta classe de operador é a padrão para
     <code>
      opcintype
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      opckeytype
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados armazenados no índice, ou zero se for igual a
     <code>
      opcintype
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>










O `opcmethod` de uma classe de operador deve corresponder ao `opfmethod` da sua família de operadores contida. Além disso, não deve haver mais de uma linha `pg_opclass` com `opcdefault` verdadeiro para qualquer combinação dada de `opcmethod` e `opcintype`.