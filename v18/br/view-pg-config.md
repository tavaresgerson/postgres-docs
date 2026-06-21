## 53.6. `pg_config` [#](#VIEW-PG-CONFIG)

A visão `pg_config` descreve os parâmetros de configuração de tempo de compilação da versão atualmente instalada do PostgreSQL. Ela é destinada, por exemplo, a ser usada por pacotes de software que desejam interagir com o PostgreSQL para facilitar a localização dos arquivos de cabeçalho e bibliotecas necessários. Ela fornece as mesmas informações básicas que a aplicação cliente PostgreSQL [pg_config][(app-pgconfig.md "pg_config")].

Por padrão, a visualização `pg_config` pode ser lida apenas por superusuários.

**Tabela 53.6. Colunas `pg_config`**



<table border="1" class="table" summary="pg_config Columns">
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
      name
     </code>
<code class="type">
      text
     </code>
</p>
<p>O nome do parâmetro</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      setting
     </code>
<code class="type">
      text
     </code>
</p>
<p>O valor do parâmetro</p>
</td>
</tr>
</tbody>
</table>

