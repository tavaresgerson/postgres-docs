### 9.31. Funções de Informações Estatísticas [#](#FUNCTIONS-STATISTICS)

* [9.31.1. Inspeção de listas de MCV](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

O PostgreSQL oferece uma função para inspecionar estatísticas complexas definidas usando o comando `CREATE STATISTICS`.

#### 9.31.1. Inspeção de listas de MCV [#](#FUNCTIONS-STATISTICS-MCV)

```sql
pg_mcv_list_items ( pg_mcv_list ) → setof record
```

`pg_mcv_list_items` retorna um conjunto de registros que descrevem todos os itens armazenados em uma lista MCV de várias colunas. Ele retorna as seguintes colunas:

<table>
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
    Type
   </th>
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code>
     index
    </code>
   </td>
   <td>
    <code>
     integer
    </code>
   </td>
   <td>
    índice do item no
    <acronym class="acronym">
     MCV
    </acronym>
    lista
   </td>
  </tr>
  <tr>
   <td>
    <code>
     values
    </code>
   </td>
   <td>
    <code>
     text[]
    </code>
   </td>
   <td>
    valores armazenados no item MCV
   </td>
  </tr>
  <tr>
   <td>
    <code>
     nulls
    </code>
   </td>
   <td>
    <code>
     boolean[]
    </code>
   </td>
   <td>
    bandeiras identificadoras
    <code>
     NULL
    </code>
    valores
   </td>
  </tr>
  <tr>
   <td>
    <code>
     frequency
    </code>
   </td>
   <td>
    <code>
     double precision
    </code>
   </td>
   <td>
    frequência desta
    <acronym class="acronym">
     MCV
    </acronym>
    item
   </td>
  </tr>
  <tr>
   <td>
    <code>
     base_frequency
    </code>
   </td>
   <td>
    <code>
     double precision
    </code>
   </td>
   <td>
    frequência base desta
    <acronym class="acronym">
     MCV
    </acronym>
    item
   </td>
  </tr>
 </tbody>
</table>

A função `pg_mcv_list_items` pode ser usada da seguinte forma:

```sql
SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';
```

Os valores do tipo `pg_mcv_list` podem ser obtidos apenas a partir da coluna `pg_statistic_ext_data`.`stxdmcv`.