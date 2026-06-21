## 35.25. `enabled_roles` [#](#INFOSCHEMA-ENABLED-ROLES)

A visão `enabled_roles` identifica os papéis atualmente “ativados”. Os papéis ativados são definidos recursivamente como o usuário atual, juntamente com todos os papéis que foram concedidos aos papéis ativados com herança automática. Em outras palavras, são todos os papéis que o usuário atual tem, direta ou indiretamente, herdando automaticamente a filiação.

Para a verificação de permissão, o conjunto de “rolos aplicáveis” é aplicado, que pode ser mais amplo do que o conjunto de rolos habilitados. Portanto, geralmente é melhor usar a visão `applicable_roles` em vez desta; Veja [Seção 35.5][(infoschema-applicable-roles.md "35.5. applicable_roles")] para detalhes sobre a visão `applicable_roles`.

**Tabela 35.23. Colunas `enabled_roles`**



<table border="1" class="table" summary="enabled_roles Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">Tipo de coluna</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      role_name
     </code>
<code class="type">
      sql_identifier
     </code>
</p>
<p>Nome de um papel</p>
</td>
</tr>
</tbody>
</table>

