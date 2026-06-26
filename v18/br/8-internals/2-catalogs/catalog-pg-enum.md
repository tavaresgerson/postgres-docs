## 52.20. `pg_enum` [#](#CATALOG-PG-ENUM)

O catálogo `pg_enum` contém entradas que mostram os valores e rótulos para cada tipo de enumeração. A representação interna de um valor de enumeração dado é, na verdade, o OID de sua linha associada em `pg_enum`.

**Tabela 52.20. Colunas `pg_enum`**

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
      enumtypid
     </code>
     <code>
      oid
     </code>
     (referências
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     .
     <code>
      oid
     </code>
     )
    </p>
    <p>
     O OID do
     <a class="link" href="catalog-pg-type.md" title="52.64. pg_type">
      <code>
       pg_type
      </code>
     </a>
     entrada que possui esse valor do enum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      enumsortorder
     </code>
     <code>
      float4
     </code>
    </p>
    <p>
     A posição de classificação deste valor do enum dentro do seu tipo de enum
    </p>
   </td>
  </tr>
  <tr>
   <td class="catalog_table_entry">
    <p class="column_definition">
     <code>
      enumlabel
     </code>
     <code>
      name
     </code>
    </p>
    <p>
     O rótulo textual para este valor do enum
    </p>
   </td>
  </tr>
 </tbody>
</table>










Os OIDs para as linhas `pg_enum` seguem uma regra especial: os OIDs pares são garantidos para serem ordenados da mesma maneira que o ordenamento de classificação de seu tipo de enum. Isso significa que, se dois OIDs pares pertencem ao mesmo tipo de enum, o OID menor deve ter o menor valor `enumsortorder`. Os valores de OID ímpares não precisam ter relação com o pedido de classificação. Essa regra permite que as rotinas de comparação de enum evitem pesquisas no catálogo em muitos casos comuns. As rotinas que criam e alteram tipos de enum tentam atribuir OIDs pares a valores de enum sempre que possível.

Quando um tipo de enum é criado, seus membros recebem posições de ordem de classificação de 1..`n`*. Mas os membros adicionados posteriormente podem receber valores negativos ou fracionários de `enumsortorder`. O único requisito desses valores é que eles sejam corretamente ordenados e únicos dentro de cada tipo de enum.