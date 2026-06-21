## 9.31. Funções de Informações Estatísticas [#](#FUNCTIONS-STATISTICS)

* [9.31.1. Inspeção de listas de MCV](functions-statistics.md#FUNCTIONS-STATISTICS-MCV)

O PostgreSQL oferece uma função para inspecionar estatísticas complexas definidas usando o comando `CREATE STATISTICS`.

### 9.31.1. Inspeção de listas de MCV [#](#FUNCTIONS-STATISTICS-MCV)

```
pg_mcv_list_items ( pg_mcv_list ) → setof record
```

`pg_mcv_list_items` retorna um conjunto de registros que descrevem todos os itens armazenados em uma lista MCV de várias colunas. Ele retorna as seguintes colunas:



<table border="1" class="informaltable">
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
<th>Descrição</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="literal">
     index
    </code>
</td>
<td>
<code class="type">
     integer
    </code>
</td>
<td>índice do item no<acronym class="acronym">MCV</acronym>lista</td>
</tr>
<tr>
<td>
<code class="literal">
     values
    </code>
</td>
<td>
<code class="type">
     text[]
    </code>
</td>
<td>valores armazenados no item MCV</td>
</tr>
<tr>
<td>
<code class="literal">
     nulls
    </code>
</td>
<td>
<code class="type">
     boolean[]
    </code>
</td>
<td>bandeiras identificadoras<code class="literal">
     NULL
    </code>valores</td>
</tr>
<tr>
<td>
<code class="literal">
     frequency
    </code>
</td>
<td>
<code class="type">
     double precision
    </code>
</td>
<td>frequência desta<acronym class="acronym">MCV</acronym>item</td>
</tr>
<tr>
<td>
<code class="literal">
     base_frequency
    </code>
</td>
<td>
<code class="type">
     double precision
    </code>
</td>
<td>frequência base desta<acronym class="acronym">MCV</acronym>item</td>
</tr>
</tbody>
</table>



A função `pg_mcv_list_items` pode ser usada da seguinte forma:

```
SELECT m.* FROM pg_statistic_ext join pg_statistic_ext_data on (oid = stxoid),
                pg_mcv_list_items(stxdmcv) m WHERE stxname = 'stts';
```

Os valores do tipo `pg_mcv_list` podem ser obtidos apenas a partir da coluna `pg_statistic_ext_data`.`stxdmcv`.