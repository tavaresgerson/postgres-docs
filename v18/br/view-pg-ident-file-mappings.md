## 53.11. `pg_ident_file_mappings` [#](#VIEW-PG-IDENT-FILE-MAPPINGS)

A vista `pg_ident_file_mappings` fornece um resumo dos conteúdos do arquivo de configuração de mapeamento de nome de usuário do cliente, `pg_ident.conf`(auth-username-maps.md "20.2. User Name Maps"). Uma linha aparece nesta vista para cada linha não vazia e não comentada no arquivo, com anotações indicando se o mapa pode ser aplicado com sucesso.

Essa visão pode ser útil para verificar se as alterações planejadas no arquivo de configuração de autenticação funcionarão ou para diagnosticar uma falha anterior. Note que essa visão relata os *conteúdos* atuais do arquivo, não sobre o que foi carregado pela última vez pelo servidor.

Por padrão, a visualização `pg_ident_file_mappings` pode ser lida apenas por superusuários.

**Tabela 53.11. Colunas `pg_ident_file_mappings`**



<table border="1" class="table" summary="pg_ident_file_mappings Columns">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="catalog_table_entry">
<p class="column_definition">
     Column Type
    </p>
<p>
     Description
    </p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      map_number
     </code>
<code class="type">
      int4
     </code>
</p>
<p>
     Number of this map, in priority order, if valid, otherwise
     <code class="literal">
      NULL
     </code>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      file_name
     </code>
<code class="type">
      text
     </code>
</p>
<p>
     Name of the file containing this map
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      line_number
     </code>
<code class="type">
      int4
     </code>
</p>
<p>
     Line number of this map in
     <code class="literal">
      file_name
     </code>
</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      map_name
     </code>
<code class="type">
      text
     </code>
</p>
<p>
     Name of the map
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      sys_name
     </code>
<code class="type">
      text
     </code>
</p>
<p>
     Detected user name of the client
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      pg_username
     </code>
<code class="type">
      text
     </code>
</p>
<p>
     Requested PostgreSQL user name
    </p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      error
     </code>
<code class="type">
      text
     </code>
</p>
<p>
     If not
     <code class="literal">
      NULL
     </code>
     , an error message indicating why this line could not be processed
    </p>
</td>
</tr>
</tbody>
</table>




  

Normalmente, uma linha que reflete uma entrada incorreta terá valores apenas nos campos `line_number` e `error`.

Veja [Capítulo 20](client-authentication.md "Chapter 20. Client Authentication") para mais informações sobre a configuração de autenticação do cliente.