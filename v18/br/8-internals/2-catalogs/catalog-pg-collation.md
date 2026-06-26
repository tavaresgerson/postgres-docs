## 52.12. `pg_collation` [#](#CATALOG-PG-COLLATION)

O catálogo `pg_collation` descreve as colatões disponíveis, que são essencialmente mapeamentos de um nome SQL para categorias de localização do sistema operacional. Consulte [Seção 23.2](collation.md) para obter mais informações.

**Tabela 52.12. Colunas `pg_collation`**



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
      collname
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     Nome de cotação (único por espaço de nomes e codificação)
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collnamespace
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-namespace.md" title="52.32. pg_namespace">
      <code>
       pg_namespace
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O OID do espaço de nome que contém esta correção
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collowner
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
     Proprietário da coletânea
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collprovider
     </code>
     <code>
      char
     </code>
    </p>
    <p>
     Fornecedora da coleta:
     <code>
      d
     </code>
     = banco de dados padrão,
     <code>
      b
     </code>
     = embutido,
     <code>
      c
     </code>
     = libc,
     <code>
      i
     </code>
     = icu
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collisdeterministic
     </code>
     <code>
      bool
     </code>
    </p>
    <p>
     A correção é determinística?
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collencoding
     </code>
     <code>
      int4
     </code>
    </p>
    <p>
     Codificação na qual a collation é aplicável, ou -1 se funcionar para qualquer codificação
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collcollate
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     <code>
      LC_COLLATE
     </code>
     para este objeto de agregação. Se o provedor não
     <code>
      libc
     </code>
     ,
     <code>
      collcollate
     </code>
     é
     <code>
      NULL
     </code>
     e
     <code>
      colllocale
     </code>
     é usado em vez disso.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collctype
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     <code>
      LC_CTYPE
     </code>
     para este objeto de agregação. Se o provedor não
     <code>
      libc
     </code>
     ,
     <code>
      collctype
     </code>
     é
     <code>
      NULL
     </code>
     e
     <code>
      colllocale
     </code>
     é usado em vez disso.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      colllocale
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Nome do local do fornecedor de collation para este objeto de collation. Se o fornecedor for
     <code>
      libc
     </code>
     ,
     <code>
      colllocale
     </code>
     é
     <code>
      NULL
     </code>
     ;
     <code>
      collcollate
     </code>
     e
     <code>
      collctype
     </code>
     são utilizados em vez disso.
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collicurules
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Regras de colagem de ICU para este objeto de colagem
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      collversion
     </code>
     <code>
      text
     </code>
    </p>
    <p>
     Versão específica do fornecedor da ordenação. Isso é registrado quando a ordenação é criada e, em seguida, verificado quando é usada, para detectar alterações na definição da ordenação que possam levar à corrupção dos dados.
    </p>
   </td>
  </tr>
 </tbody>
</table>










Observe que a chave única neste catálogo é (`collname`, `collencoding`, `collnamespace`) e não apenas (`collname`, `collnamespace`). O PostgreSQL geralmente ignora todas as codificações que não têm `collencoding` igual à codificação do banco de dados atual ou -1, e a criação de novas entradas com o mesmo nome que uma entrada com `collencoding` = -1 é proibida. Portanto, é suficiente usar um nome SQL qualificado (*`schema`*.*`name`*) para identificar uma codificação, embora isso não seja único de acordo com a definição do catálogo. A razão para definir o catálogo dessa maneira é que o initdb o preenche no momento da inicialização do clúster com entradas para todos os locais disponíveis no sistema, então ele deve ser capaz de conter entradas para todas as codificações que possam ser usadas no clúster.

No banco de dados `template0`, poderia ser útil criar colatinas cujas codificações não correspondem à codificação do banco de dados, uma vez que elas poderiam corresponder às codificações dos bancos de dados que posteriormente seriam clonados a partir de `template0`. Isso atualmente teria que ser feito manualmente.