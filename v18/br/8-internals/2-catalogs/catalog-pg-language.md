## 52.29. `pg_language` [#](#CATALOG-PG-LANGUAGE)

O catálogo `pg_language` registra os idiomas nos quais você pode escrever funções ou procedimentos armazenados. Consulte [CREATE LANGUAGE](sql-createlanguage.md "CREATE LANGUAGE") e [Capítulo 40](xplang.md "Chapter 40. Procedural Languages") para obter mais informações sobre manipuladores de idioma.

**Tabela 52.29. Colunas `pg_language`**



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
      lanname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome da língua
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanowner
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
     Proprietário da língua
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanispl
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Isso é falso para as línguas internas (como
     <acronym class="acronym">
      SQL
     </acronym>
     ) e verdadeiro para idiomas definidos pelo usuário.
     <span class="application">
      pg_dump
     </span>
     Ainda usa isso para determinar quais idiomas precisam ser descartados, mas isso pode ser substituído por um mecanismo diferente no futuro.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanpltrusted
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     Verdadeiro se este for um idioma de confiança, o que significa que não se acredita que ele conceda acesso a nada fora do ambiente normal de execução do SQL. Apenas usuários super podem criar funções em idiomas não confiáveis.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanplcallfoid
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
     Para idiomas não internos, isso se refere ao manipulador de linguagem, que é uma função especial responsável por executar todas as funções escritas na língua específica. Zero para idiomas internos.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      laninline
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
     Isso se refere a uma função que é responsável por executar
     <span class="quote">
      “
      <span class="quote">
       em linha
      </span>
      ”
     </span>
     blocos de código anônimos
     <a class="xref" href="sql-do.md" title="DO">
      <span class="refentrytitle">
       DO
      </span>
     </a>
     blocos). Zero se os blocos inline não forem suportados.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanvalidator
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
     Isso se refere a uma função de validação de linguagem que é responsável por verificar a sintaxe e a validade de novas funções quando elas são criadas. Zero se nenhum validador for fornecido.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      lanacl
     </code>
     <code>
      aclitem[]
     </code>
    </p>
    <p>
     Privilegios de acesso; veja
     <a class="xref" href="ddl-priv.md" title="5.8. Privileges">
      Seção 5.8
     </a>
     para detalhes
    </p>
   </td>
  </tr>
 </tbody>
</table>





