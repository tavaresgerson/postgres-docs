## 52.21. `pg_event_trigger` [#](#CATALOG-PG-EVENT-TRIGGER)

O catálogo `pg_event_trigger` armazena gatilhos de eventos. Consulte o [Capítulo 38](event-triggers.md) para obter mais informações.

**Tabela 52.21. Colunas `pg_event_trigger`**



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
      evtname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome do gatilho (deve ser único)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      evtevent
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Identifica o evento para o qual este gatilho é acionado
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      evtowner
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
     Proprietário do gatilho do evento
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      evtfoid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-proc.md" title="52.39. pg_proc">
      <code>
       pg_proc
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     A função a ser chamada
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      evtenabled
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Controles em que
     <a class="xref" href="runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE">
      session_replication_role
     </a>
     os modos que o gatilho do evento aciona os fogos.
     <code>
      O
     </code>
     = desencadeia incêndios
     <span class="quote">
      “
      <span class="quote">
       origem
      </span>
      ”
     </span>
     e
     <span class="quote">
      “
      <span class="quote">
       local
      </span>
      ”
     </span>
     modos,
     <code>
      D
     </code>
     = o gatilho está desativado,
     <code>
      R
     </code>
     = desencadeia incêndios
     <span class="quote">
      “
      <span class="quote">
       replica
      </span>
      ”
     </span>
     modo,
     <code>
      A
     </code>
     = acionam incêndios sempre.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      evttags
     </code>
     <code>
      text[]
     </code>
    </p>
    <p>
     Etiquetas de comando para as quais este gatilho será disparado. Se NULL, o disparo deste gatilho não é restrito com base na etiqueta de comando.
    </p>
   </td>
  </tr>
 </tbody>
</table>





