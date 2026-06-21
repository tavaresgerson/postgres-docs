## 52.18. `pg_depend` [#](#CATALOG-PG-DEPEND)

O catálogo `pg_depend` registra as relações de dependência entre os objetos do banco de dados. Essas informações permitem que os comandos `DROP` encontrem quais outros objetos devem ser descartados pelo `DROP CASCADE` ou impedir a descartagem no caso do `DROP RESTRICT`.

Veja também `pg_shdepend` (catalog-pg-shdepend.md "52.48. pg_shdepend"), que realiza uma função semelhante para dependências que envolvem objetos que são compartilhados em um clúster de banco de dados.

**Tabela 52.18. Colunas `pg_depend`**



<table border="1" class="table" summary="pg_depend Columns">
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
      classid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do catálogo do sistema que o objeto dependente está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto dependente específico
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      objsubid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Para uma coluna de tabela, este é o número da coluna (o
     <code class="structfield">
      objid
     </code>
     e
     <code class="structfield">
      classid
     </code>
     refere-se à própria tabela). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      refclassid
     </code>
     <code class="type">
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-class.md" title="52.11. pg_class">
      <code class="structname">
       pg_class
      </code>
     </a>
     .
     <code class="structfield">
      oid
     </code>
     )
    </p>
    <p>
     O OID do catálogo do sistema que o objeto referenciado está em
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      refobjid
     </code>
     <code class="type">
      oid
     </code>
     (referência a qualquer coluna OID)
    </p>
    <p>
     O OID do objeto específico referido
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      refobjsubid
     </code>
     <code class="type">
      int4
     </code>
    </p>
    <p>
     Para uma coluna de tabela, este é o número da coluna (o
     <code class="structfield">
      refobjid
     </code>
     e
     <code class="structfield">
      refclassid
     </code>
     refere-se à tabela em si). Para todos os outros tipos de objeto, essa coluna é zero.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code class="structfield">
      deptype
     </code>
     <code class="type">
      char
     </code>
    </p>
    <p>
     Um código que defina a semântica específica dessa relação de dependência; veja o texto
    </p>
   </td>
  </tr>
 </tbody>
</table>










Em todos os casos, uma entrada `pg_depend` indica que o objeto referenciado não pode ser descartado sem também descartar o objeto dependente. No entanto, existem vários subsabores identificados por `deptype`:

`DEPENDENCY_NORMAL` (`n`): Uma relação normal entre objetos criados separadamente. O objeto dependente pode ser descartado sem afetar o objeto referenciado. O objeto referenciado só pode ser descartado especificando `CASCADE`, no caso, o objeto dependente também é descartado. Exemplo: uma coluna de tabela tem uma dependência normal em seu tipo de dados.

`DEPENDENCY_AUTO` (`a`): O objeto dependente pode ser descartado separadamente do objeto referenciado, e deve ser descartado automaticamente (independentemente do modo `RESTRICT` ou `CASCADE`) se o objeto referenciado for descartado. Exemplo: uma restrição nomeada em uma tabela é feita automaticamente dependente da tabela, de modo que ela desaparecerá se a tabela for descartada.

`DEPENDENCY_INTERNAL` (`i`): O objeto dependente foi criado como parte da criação do objeto referenciado e, na verdade, é apenas uma parte de sua implementação interna. Um `DROP` direto do objeto dependente será totalmente desconsiderado (diremos ao usuário que emita um `DROP` contra o objeto referenciado, em vez disso). Um `DROP` do objeto referenciado resultará na eliminação automática do objeto dependente, independentemente de `CASCADE` ser especificado ou não. Se o objeto dependente tiver que ser eliminado devido a uma dependência de algum outro objeto ser removida, sua eliminação é convertida em uma eliminação do objeto referenciado, de modo que as dependências `NORMAL` e `AUTO` do objeto dependente se comportam muito como se fossem dependências do objeto referenciado. Exemplo: a regra `ON SELECT` de uma visão é feita internamente dependente da visão, impedindo que seja eliminada enquanto a visão permanecer. As dependências da regra (como as tabelas a que se refere) atuam como se fossem dependências da visão.

`DEPENDENCY_PARTITION_PRI` (`P`) `DEPENDENCY_PARTITION_SEC` (`S`): O objeto dependente foi criado como parte da criação do objeto referenciado e é realmente apenas uma parte de sua implementação interna; no entanto, ao contrário de `INTERNAL`, há mais de um objeto referenciado desse tipo. O objeto dependente não deve ser descartado a menos que pelo menos um desses objetos referenciados seja descartado; se algum deles for descartado, o objeto dependente deve ser descartado, independentemente de `CASCADE` ser especificado. Além disso, ao contrário de `INTERNAL`, a descarte de algum outro objeto do qual o objeto dependente depende não resulta na exclusão automática de qualquer objeto referenciado por partição. Portanto, se a descarte não se espalhar para pelo menos um desses objetos por algum outro caminho, será recusada. (Na maioria dos casos, o objeto dependente compartilha todas as suas dependências não referenciadas com pelo menos um objeto referenciado por partição, de modo que essa restrição não resulta no bloqueio de qualquer apagamento em cascata). As dependências de partição são feitas em adição, não em substituição, a quaisquer dependências que o objeto normalmente teria. Isso simplifica as operações de `ATTACH/DETACH PARTITION`: as dependências de partição precisam apenas ser adicionadas ou removidas. Exemplo: um índice particionado filho é feito dependente da tabela de partição em que está e do índice particionado pai, de modo que ele desaparece se qualquer um deles for descartado, mas não de outra forma. A dependência do índice pai é primária, de modo que, se o usuário tentar descarte o índice particionado filho, a mensagem de erro sugerirá descarte do índice pai em vez disso (e não da tabela).

`DEPENDENCY_EXTENSION` (`e`): O objeto dependente é um membro da *extensão* que é o objeto referenciado (ver [`pg_extension`](catalog-pg-extension.md "52.22. pg_extension")). O objeto dependente só pode ser descartado através de [`DROP EXTENSION`](sql-dropextension.md "DROP EXTENSION") no objeto referenciado. Funcionalmente, esse tipo de dependência atua da mesma forma que uma dependência `INTERNAL`, mas é mantido separado para clareza e para simplificar o pg_dump.

`DEPENDENCY_AUTO_EXTENSION` (`x`): O objeto dependente não é membro da extensão que é o objeto referenciado (e, portanto, não deve ser ignorado pelo pg_dump), mas não pode funcionar sem a extensão e deve ser automaticamente descartado se a extensão for. O objeto dependente também pode ser descartado por si só. Funcionalmente, esse tipo de dependência atua da mesma forma que uma dependência `AUTO`, mas é mantido separado para clareza e para simplificar o pg_dump.

Outros sabores de dependência podem ser necessários no futuro.

Observe que é perfeitamente possível que dois objetos estejam vinculados por mais de uma entrada `pg_depend`. Por exemplo, um índice particionado teria tanto uma dependência de tipo de partição em sua tabela de partição associada quanto uma dependência automática em cada coluna dessa tabela que ele indexa. Esse tipo de situação expressa a união de múltiplas semânticas de dependência. Um objeto dependente pode ser descartado sem `CASCADE` se qualquer uma de suas dependências satisfaça sua condição para descarte automático. Por outro lado, todas as restrições das dependências sobre quais objetos devem ser descartados juntos devem ser satisfeitas.

A maioria dos objetos criados durante o initdb são considerados “fixos”, o que significa que o próprio sistema depende deles. Portanto, eles nunca são permitidos a serem descartados. Além disso, sabendo que os objetos fixos não serão descartados, o mecanismo de dependência não se preocupa em fazer entradas `pg_depend` que mostrem dependências deles. Assim, por exemplo, uma coluna de tabela do tipo `numeric` nominalmente tem uma `NORMAL` dependência no tipo de dados `numeric`, mas nenhuma entrada desse tipo realmente aparece em `pg_depend`.