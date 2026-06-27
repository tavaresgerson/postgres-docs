### 9.23. Fusão de funções de suporte [#](#FUNCTIONS-MERGE-SUPPORT)

O PostgreSQL inclui uma função de suporte a junção que pode ser usada na lista `RETURNING` de um comando [MERGE](sql-merge.md "MERGE") para identificar a ação realizada para cada linha; veja [Tabela 9.68](functions-merge-support.md#FUNCTIONS-MERGE-SUPPORT-TABLE "Table 9.68. Merge Support Functions").

**Tabela 9.68. Funções de suporte de fusão**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Função
    </p>
    <p>
     Descrição
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry" id="MERGE-ACTION">
    <p class="func_signature">
     <code>
      merge_action
     </code>
     ( )
     <code>
      text
     </code>
    </p>
    <p>
     Retorna o comando de ação de junção executado para a linha atual. Isso será
     <code>
      'INSERT'
     </code>
     ,
     <code>
      'UPDATE'
     </code>
     , ou
     <code>
      'DELETE'
     </code>
     .
    </p>
   </td>
  </tr>
 </tbody>
</table>

Exemplo:

```sql
MERGE INTO products p
  USING stock s ON p.product_id = s.product_id
  WHEN MATCHED AND s.quantity > 0 THEN
    UPDATE SET in_stock = true, quantity = s.quantity
  WHEN MATCHED THEN
    UPDATE SET in_stock = false, quantity = 0
  WHEN NOT MATCHED THEN
    INSERT (product_id, in_stock, quantity)
      VALUES (s.product_id, true, s.quantity)
  RETURNING merge_action(), p.*;

 merge_action | product_id | in_stock | quantity
--------------+------------+----------+----------
 UPDATE       |       1001 | t        |       50
 UPDATE       |       1002 | f        |        0
 INSERT       |       1003 | t        |       10
```

Observe que essa função só pode ser usada na lista `RETURNING` de um comando `MERGE`. É um erro usá-la em qualquer outra parte de uma consulta.