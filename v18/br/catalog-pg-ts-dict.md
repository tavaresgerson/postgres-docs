## 52.61. `pg_ts_dict` [#](#CATALOG-PG-TS-DICT)

O catálogo `pg_ts_dict` contém entradas que definem dicionários de busca de texto. Um dicionário depende de um modelo de busca de texto, que especifica todas as funções de implementação necessárias; o próprio dicionário fornece valores para os parâmetros configuráveis pelo usuário suportados pelo modelo. Essa divisão do trabalho permite que dicionários sejam criados por usuários não privilegiados. Os parâmetros são especificados por uma string de texto `dictinitoption`, cujo formato e significado variam dependendo do modelo.

As funcionalidades de busca de texto do PostgreSQL são descritas em detalhes no Capítulo 12 (textsearch.md "Chapter 12. Full Text Search").

**Tabela 52.61. Colunas `pg_ts_dict`**



<table border="1" class="table" summary="pg_ts_dict Columns">
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
      oid
     </code>
<code class="type">
      oid
     </code>
</p>
<p>Identificador da linha</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dictname
     </code>
<code class="type">
      name
     </code>
</p>
<p>Nome do dicionário de pesquisa de texto</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dictnamespace
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
<code class="structname">
       pg_namespace
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do espaço de nomes que contém este dicionário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dictowner
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-authid.md" title="52.8. pg_authid">
<code class="structname">
       pg_authid
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>Proprietário do dicionário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dicttemplate
     </code>
<code class="type">
      oid
     </code>(referências<a class="link" href="catalog-pg-ts-template.md" title="52.63. pg_ts_template">
<code class="structname">
       pg_ts_template
      </code>
</a>
     .
     <code class="structfield">
      oid
     </code>)</p>
<p>O OID do modelo de busca de texto para este dicionário</p>
</td>
</tr>
<tr>
<td class="catalog_table_entry">
<p class="column_definition">
<code class="structfield">
      dictinitoption
     </code>
<code class="type">
      text
     </code>
</p>
<p>Opção de inicialização de string para o modelo</p>
</td>
</tr>
</tbody>
</table>

