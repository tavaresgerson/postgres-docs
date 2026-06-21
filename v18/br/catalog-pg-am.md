## 52.3. `pg_am` [#](#CATALOG-PG-AM)

O catálogo `pg_am` armazena informações sobre os métodos de acesso à relação. Há uma linha para cada método de acesso suportado pelo sistema. Atualmente, apenas tabelas e índices têm métodos de acesso. Os requisitos para os métodos de acesso a tabelas e índices são discutidos em detalhes nos capítulos 62 e 63, respectivamente.

**Tabela 52.3. Colunas `pg_am`**



<table border="1" class="table" summary="pg_am Columns">
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
      amname
     </code>
     <code class="type">
      name
     </code>
    </p>
    <p>
     Nome do método de acesso
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amhandler
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
     OID de uma função de manipulador que é responsável por fornecer informações sobre o método de acesso
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      amtype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     <code class="literal">
      t
     </code>
     = tabela (incluindo visualizações materializadas),
     <code class="literal">
      i
     </code>
     = índice.
    </p>
   </td>
  </tr>
 </tbody>
</table>










### Nota

Antes do PostgreSQL 9.6, `pg_am` continha muitas colunas adicionais que representavam propriedades dos métodos de acesso ao índice. Esses dados agora são visíveis apenas diretamente no nível do código C. No entanto, `pg_index_column_has_property()` e as funções relacionadas foram adicionadas para permitir que consultas SQL inspecionem as propriedades dos métodos de acesso ao índice; veja [Tabela 9.76](functions-info.md#FUNCTIONS-INFO-CATALOG-TABLE).