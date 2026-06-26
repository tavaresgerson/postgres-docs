### 9.1. Operadores Lógicos [#](#FUNCTIONS-LOGICAL)

Os operadores lógicos usuais estão disponíveis:

```sql
boolean AND boolean → boolean
boolean OR boolean → boolean
NOT boolean → boolean
```

O SQL utiliza um sistema lógico de três valores com verdadeiro, falso e `null`, que representa “desconhecido”. Observe as seguintes tabelas de verdade:

<table>
 <thead>
  <tr>
   <th>
    <em class="replaceable">
     <code>
      a
     </code>
    </em>
   </th>
   <th>
    <em class="replaceable">
     <code>
      b
     </code>
    </em>
   </th>
   <th>
    <em class="replaceable">
     <code>
      a
     </code>
    </em>
    AND
    <em class="replaceable">
     <code>
      b
     </code>
    </em>
   </th>
   <th>
     <code>a</code>
    OR
     <code>
      b
     </code>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    TRUE
   </td>
   <td>
    TRUE
   </td>
   <td>
    TRUE
   </td>
   <td>
    TRUE
   </td>
  </tr>
  <tr>
   <td>
    TRUE
   </td>
   <td>
    FALSE
   </td>
   <td>
    FALSE
   </td>
   <td>
    TRUE
   </td>
  </tr>
  <tr>
   <td>
    TRUE
   </td>
   <td>
    NULL
   </td>
   <td>
    NULL
   </td>
   <td>
    TRUE
   </td>
  </tr>
  <tr>
   <td>
    FALSE
   </td>
   <td>
    FALSE
   </td>
   <td>
    FALSE
   </td>
   <td>
    FALSE
   </td>
  </tr>
  <tr>
   <td>
    FALSE
   </td>
   <td>
    NULL
   </td>
   <td>
    FALSE
   </td>
   <td>
    NULL
   </td>
  </tr>
  <tr>
   <td>
    NULL
   </td>
   <td>
    NULL
   </td>
   <td>
    NULL
   </td>
   <td>
    NULL
   </td>
  </tr>
 </tbody>
</table>

<table>
 <thead>
  <tr>
   <th>
    <code>a</code>
   </th>
   <th>
    NOT <code>a</code>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    TRUE
   </td>
   <td>
    FALSE
   </td>
  </tr>
  <tr>
   <td>
    FALSE
   </td>
   <td>
    TRUE
   </td>
  </tr>
  <tr>
   <td>
    NULL
   </td>
   <td>
    NULL
   </td>
  </tr>
 </tbody>
</table>

Os operadores `AND` e `OR` são compostos, ou seja, você pode trocar os operandos esquerdo e direito sem afetar o resultado. (No entanto, não é garantido que o operando esquerdo seja avaliado antes do operando direito. Consulte [Seção 4.2.14](sql-expressions.md#SYNTAX-EXPRESS-EVAL) para obter mais informações sobre a ordem de avaliação das subexpressões.)