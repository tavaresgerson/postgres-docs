## 52.5. `pg_amproc` [#](#CATALOG-PG-AMPROC)

O catálogo `pg_amproc` armazena informações sobre as funções de suporte associadas às famílias de operadores de método de acesso. Há uma linha para cada função de suporte pertencente a uma família de operadores.

**Tabela 52.5. Colunas `pg_amproc`**



<table border="1" class="table" summary="pg_amproc Columns">
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
      amprocfamily
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-opfamily.md" title="52.35. pg_opfamily">
      <code class="structname">
       pg_opfamily
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     A família do operador esta entrada é para
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amproclefttype
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados de entrada à esquerda do operador associado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amprocrighttype
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code class="structname">
       pg_type
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     Tipo de dados de entrada da mão direita do operador associado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amprocnum
     </code>
     <code class="type">
      int2
     </code>
    </p>
    <p>
     Número da função de suporte
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amproc
     </code>
     <code class="type">
      regproc
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code class="structname">
       pg_proc
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     OID da função
    </p>
   </td>
  </tr>
 </tbody>
</table>










A interpretação usual dos campos `amproclefttype` e `amprocrighttype` é que eles identificam os tipos de entrada esquerda e direita dos operadores que uma função de suporte específica suporta. Para alguns métodos de acesso, eles correspondem ao(s) tipo(s) de dados de entrada da própria função de suporte, e para outros, não. Há uma noção de funções de suporte "padrão" para um índice, que são aquelas com `amproclefttype` e `amprocrighttype` iguais à classe de operador de índice `opcintype`.