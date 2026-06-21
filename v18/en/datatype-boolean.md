## 8.6. Boolean Type [#](#DATATYPE-BOOLEAN)

PostgreSQL provides the standard SQL type `boolean`; see [Table 8.19](datatype-boolean.md#DATATYPE-BOOLEAN-TABLE "Table 8.19. Boolean Data Type"). The `boolean` type can have several states: “true”, “false”, and a third state, “unknown”, which is represented by the SQL null value.

**Table 8.19. Boolean Data Type**



<table border="1" class="table" summary="Boolean Data Type">
 <colgroup>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
   </th>
   <th>
    Storage Size
   </th>
   <th>
    Description
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    1 byte
   </td>
   <td>
    state of true or false
   </td>
  </tr>
 </tbody>
</table>




  

Boolean constants can be represented in SQL queries by the SQL key words `TRUE`, `FALSE`, and `NULL`.

The datatype input function for type `boolean` accepts these string representations for the “true” state:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="literal">
    true
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    yes
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    on
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    1
   </code>
  </td>
 </tr>
</table>




and these representations for the “false” state:



<table border="0" class="simplelist" summary="Simple list">
 <tr>
  <td>
   <code class="literal">
    false
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    no
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    off
   </code>
  </td>
 </tr>
 <tr>
  <td>
   <code class="literal">
    0
   </code>
  </td>
 </tr>
</table>




Unique prefixes of these strings are also accepted, for example `t` or `n`. Leading or trailing whitespace is ignored, and case does not matter.

The datatype output function for type `boolean` always emits either `t` or `f`, as shown in [Example 8.2](datatype-boolean.md#DATATYPE-BOOLEAN-EXAMPLE "Example 8.2. Using the boolean Type").

**Example 8.2. Using the `boolean` Type**

```
CREATE TABLE test1 (a boolean, b text);
INSERT INTO test1 VALUES (TRUE, 'sic est');
INSERT INTO test1 VALUES (FALSE, 'non est');
SELECT * FROM test1;
 a |    b
---+---------
 t | sic est
 f | non est

SELECT * FROM test1 WHERE a;
 a |    b
---+---------
 t | sic est
```

  

The key words `TRUE` and `FALSE` are the preferred (SQL-compliant) method for writing Boolean constants in SQL queries. But you can also use the string representations by following the generic string-literal constant syntax described in [Section 4.1.2.7](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC "4.1.2.7. Constants of Other Types"), for example `'yes'::boolean`.

Note that the parser automatically understands that `TRUE` and `FALSE` are of type `boolean`, but this is not so for `NULL` because that can have any type. So in some contexts you might have to cast `NULL` to `boolean` explicitly, for example `NULL::boolean`. Conversely, the cast can be omitted from a string-literal Boolean value in contexts where the parser can deduce that the literal must be of type `boolean`.
