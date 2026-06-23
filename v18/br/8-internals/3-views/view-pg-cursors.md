## 53.7. `pg_cursors` [#](#VIEW-PG-CURSORS)

A vista `pg_cursors` lista os cursors que estão disponíveis atualmente. Os cursors podem ser definidos de várias maneiras:

* via a declaração `DECLARE` no SQL
* via a mensagem Bind no protocolo frontend/backend, conforme descrito em [Seção 54.2.3](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)
* via a Interface de Programação do Servidor (SPI), conforme descrito em [Seção 45.1](spi-interface.md)

A vista `pg_cursors` exibe os cursors criados por qualquer um desses meios. Os cursors existem apenas durante a transação que os define, a menos que tenham sido declarados `WITH HOLD`. Portanto, os cursors não mantidos estão presentes apenas na vista até o final da transação que os criou.

Nota

Os cursors são usados internamente para implementar alguns dos componentes do PostgreSQL, como linguagens procedimentais. Portanto, a vista `pg_cursors` pode incluir cursors que não foram explicitamente criados pelo usuário.

**Tabela 53.7. Colunas `pg_cursors`**



<table border="1" class="table" summary="pg_cursors Columns">
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
      name
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     O nome do cursor
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      statement
     </code>
     <code class="type">
      text
     </code>
    </p>
    <p>
     A string de consulta literal enviada para declarar este cursor
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_holdable
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="literal">
      true
     </code>
     se o cursor for mantido (ou seja, pode ser acessado após a transação que declarou que o cursor foi comprometido);
     <code class="literal">
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_binary
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="literal">
      true
     </code>
     se o cursor foi declarado
     <code class="literal">
      BINARY
     </code>
     ;
     <code class="literal">
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      is_scrollable
     </code>
     <code class="type">
      bool
     </code>
    </p>
    <p>
     <code class="literal">
      true
     </code>
     se o cursor for rolável (ou seja, permite que as linhas sejam recuperadas de maneira não sequencial);
     <code class="literal">
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      creation_time
     </code>
     <code class="type">
      timestamptz
     </code>
    </p>
    <p>
     O momento em que o cursor foi declarado
    </p>
   </td>
  </tr>
 </tbody>
</table>










A visualização `pg_cursors` é somente de leitura.