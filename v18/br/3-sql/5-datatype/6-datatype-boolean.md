### 8.6. Tipo Booleano [#](#DATATYPE-BOOLEAN)

O PostgreSQL fornece o tipo padrão SQL `boolean`; veja [Tabela 8.19](datatype-boolean.md#DATATYPE-BOOLEAN-TABLE). O tipo `boolean` pode ter vários estados: “verdadeiro”, “falso” e um terceiro estado, “desconhecido”, que é representado pelo valor nulo do SQL.

**Tabela 8.19. Tipo de dados booleano**

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
    Descrição
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
    estado de verdadeiro ou falso
   </td>
  </tr>
 </tbody>
</table>

As constantes booleanas podem ser representadas em consultas SQL pelos termos-chave SQL `TRUE`, `FALSE` e `NULL`.

A função de entrada de tipo de dados do tipo `boolean` aceita essas representações de string para o estado “verdadeiro”:

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

e essas representações para o estado “falso”:

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

Prefixos únicos dessas strings também são aceitos, por exemplo, `t` ou `n`. Espaços em branco no início ou no fim são ignorados e a grafia não importa.

A função de saída de tipo de dados para o tipo `boolean` sempre emite `t` ou `f`, conforme mostrado no [Exemplo 8.2](datatype-boolean.md#DATATYPE-BOOLEAN-EXAMPLE).

**Exemplo 8.2. Usando o Tipo `boolean`**

```sql
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

As palavras-chave `TRUE` e `FALSE` são o método preferido (compatível com SQL) para escrever constantes booleanas em consultas SQL. Mas você também pode usar as representações de string seguindo a sintaxe de constante de literal de string genérica descrita em [Seção 4.1.2.7](sql-syntax-lexical.md#SQL-SYNTAX-CONSTANTS-GENERIC), por exemplo `'yes'::boolean`.

Observe que o analisador entende automaticamente que `TRUE` e `FALSE` são do tipo `boolean`, mas isso não é o caso de `NULL`, pois este pode ter qualquer tipo. Portanto, em alguns contextos, você pode precisar converter `NULL` para `boolean` explicitamente, por exemplo, `NULL::boolean`. Por outro lado, o cast pode ser omitido em um valor booleano literal de string em contextos onde o analisador pode deduzir que o literal deve ser do tipo `boolean`.