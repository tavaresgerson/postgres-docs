## 53.7. `pg_cursors` [#](#VIEW-PG-CURSORS)

A vista `pg_cursors` lista os cursors que estão disponíveis atualmente. Os cursors podem ser definidos de várias maneiras:

* via a declaração `DECLARE` no SQL
* via a mensagem Bind no protocolo frontend/backend, conforme descrito em [Seção 54.2.3](protocol-flow.md#PROTOCOL-FLOW-EXT-QUERY)
* via a Interface de Programação do Servidor (SPI), conforme descrito em [Seção 45.1](spi-interface.md)

A vista `pg_cursors` exibe os cursors criados por qualquer um desses meios. Os cursors existem apenas durante a transação que os define, a menos que tenham sido declarados `WITH HOLD`. Portanto, os cursors não mantidos estão presentes apenas na vista até o final da transação que os criou.

Nota

Os cursors são usados internamente para implementar alguns dos componentes do PostgreSQL, como linguagens procedimentais. Portanto, a vista `pg_cursors` pode incluir cursors que não foram explicitamente criados pelo usuário.

**Tabela 53.7. Colunas `pg_cursors`**



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
      name
     </code>
     <code>
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
     <code>
      statement
     </code>
     <code>
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
     <code>
      is_holdable
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     se o cursor for mantido (ou seja, pode ser acessado após a transação que declarou que o cursor foi comprometido);
     <code>
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_binary
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     se o cursor foi declarado
     <code>
      BINARY
     </code>
     ;
     <code>
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      is_scrollable
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     <code>
      true
     </code>
     se o cursor for rolável (ou seja, permite que as linhas sejam recuperadas de maneira não sequencial);
     <code>
      false
     </code>
     caso contrário
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      creation_time
     </code>
     <code>
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