### 9.10. Funções de suporte de enumeração [#](#FUNCTIONS-ENUM)

Para os tipos de enumeração (descritos na [Seção 8.7](datatype-enum.md)), existem várias funções que permitem uma programação mais limpa, sem codificar valores específicos de um tipo de enumeração. Essas funções estão listadas na [Tabela 9.35](functions-enum.md#FUNCTIONS-ENUM-TABLE). Os exemplos assumem um tipo de enumeração criado como:

```sql
CREATE TYPE rainbow AS ENUM ('red', 'orange', 'yellow', 'green', 'blue', 'purple');
```

**Tabela 9.35. Funções de suporte de enumeração**

<table>
 <colgroup>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th class="func_table_entry">
    <p class="func_signature">
     Function
    </p>
    <p>
     Description
    </p>
    <p>
     Example(s)
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      enum_first
     </code>
     (
     <code>
      anyenum
     </code>
     ) →
     <code>
      anyenum
     </code>
    </p>
    <p>
     Returns the first value of the input enum type.
    </p>
    <p>
     <code>
      enum_first(null::rainbow)
     </code>
     →
     <code>
      red
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      enum_last
     </code>
     (
     <code>
      anyenum
     </code>
     ) →
     <code>
      anyenum
     </code>
    </p>
    <p>
     Returns the last value of the input enum type.
    </p>
    <p>
     <code>
      enum_last(null::rainbow)
     </code>
     →
     <code>
      purple
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      enum_range
     </code>
     (
     <code>
      anyenum
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Returns all values of the input enum type in an ordered array.
    </p>
    <p>
     <code>
      enum_range(null::rainbow)
     </code>
     →
     <code>
      {red,orange,yellow,​green,blue,purple}
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      enum_range
     </code>
     (
     <code>
      anyenum
     </code>
     ,
     <code>
      anyenum
     </code>
     ) →
     <code>
      anyarray
     </code>
    </p>
    <p>
     Returns the range between the two given enum values, as an ordered array. The values must be from the same enum type. If the first parameter is null, the result will start with the first value of the enum type. If the second parameter is null, the result will end with the last value of the enum type.
    </p>
    <p>
     <code>
      enum_range('orange'::rainbow, 'green'::rainbow)
     </code>
     →
     <code>
      {orange,yellow,green}
     </code>
    </p>
    <p>
     <code>
      enum_range(NULL, 'green'::rainbow)
     </code>
     →
     <code>
      {red,orange,​yellow,green}
     </code>
    </p>
    <p>
     <code>
      enum_range('orange'::rainbow, NULL)
     </code>
     →
     <code>
      {orange,yellow,green,​blue,purple}
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

Observe que, exceto para a forma de dois argumentos de `enum_range`, essas funções ignoram o valor específico passado para elas; elas se importam apenas com seu tipo de dados declarado. Pode ser passado nulo ou um valor específico do tipo, com o mesmo resultado. É mais comum aplicar essas funções a uma coluna de tabela ou argumento de função do que a um nome de tipo hardwired como usado nos exemplos.