## F.31. pgrowlocks — mostre as informações de bloqueio de linha de uma tabela [#](#PGROWLOCKS)

* [F.31.1. Visão geral](pgrowlocks.md#PGROWLOCKS-OVERVIEW)
* [F.31.2. Saída de amostra](pgrowlocks.md#PGROWLOCKS-SAMPLE-OUTPUT)
* [F.31.3. Autor](pgrowlocks.md#PGROWLOCKS-AUTHOR)

O módulo `pgrowlocks` fornece uma função para mostrar informações de bloqueio de linha para uma tabela especificada.

Por padrão, o uso é restrito a superusuários, papéis com privilégios do papel `pg_stat_scan_tables` e usuários com permissões `SELECT` na tabela.

### F.31.1. Visão geral [#](#PGROWLOCKS-OVERVIEW)

```
pgrowlocks(text) returns setof record
```

O parâmetro é o nome de uma tabela. O resultado é um conjunto de registros, com uma linha para cada linha bloqueada na tabela. As colunas de saída são mostradas em [Tabela F.21](pgrowlocks.md#PGROWLOCKS-COLUMNS).

**Tabela F.21. Colunas de Saída `pgrowlocks`**



<table border="1" class="table" summary="pgrowlocks Output Columns">
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
    <code class="structfield">
     locked_row
    </code>
   </td>
   <td>
    <code class="type">
     tid
    </code>
   </td>
   <td>
    ID do par (TID) da linha bloqueada
   </td>
  </tr>
  <tr>
   <td>
    <code class="structfield">
     locker
    </code>
   </td>
   <td>
    <code class="type">
     xid
    </code>
   </td>
   <td>
    ID de transação do armário, ou ID multixact se for multitransação; veja
    <a class="xref" href="transaction-id.md" title="67.1. Transactions and Identifiers">
     Seção 67.1
    </a>
   </td>
  </tr>
  <tr>
   <td>
    <code class="structfield">
     multi
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se o armário é uma multitransação
   </td>
  </tr>
  <tr>
   <td>
    <code class="structfield">
     xids
    </code>
   </td>
   <td>
    <code class="type">
     xid[]
    </code>
   </td>
   <td>
    ID de transação dos armários (mais de um, se for multitransação)
   </td>
  </tr>
  <tr>
   <td>
    <code class="structfield">
     modes
    </code>
   </td>
   <td>
    <code class="type">
     text[]
    </code>
   </td>
   <td>
    Modo de bloqueio dos armários (mais de um, se for multitransação), uma matriz de
    <code class="literal">
     For Key Share
    </code>
    ,
    <code class="literal">
     For Share
    </code>
    ,
    <code class="literal">
     For No Key Update
    </code>
    ,
    <code class="literal">
     No Key Update
    </code>
    ,
    <code class="literal">
     For Update
    </code>
    ,
    <code class="literal">
     Update
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="structfield">
     pids
    </code>
   </td>
   <td>
    <code class="type">
     integer[]
    </code>
   </td>
   <td>
    IDs de processo de backends de bloqueio (mais de um, se for multitransação)
   </td>
  </tr>
 </tbody>
</table>









`pgrowlocks` assume `AccessShareLock` para a tabela alvo e lê cada linha uma a uma para coletar as informações de bloqueio da linha. Isso não é muito rápido para uma tabela grande. Observe que:

1. Se um bloqueio `ACCESS EXCLUSIVE` for realizado na tabela, o `pgrowlocks` será bloqueado.
2. Não é garantido que `pgrowlocks` produza um instantâneo autoconsistente. É possível que um novo bloqueio de linha seja realizado ou um bloqueio antigo seja liberado durante sua execução.

`pgrowlocks` não exibe o conteúdo das linhas bloqueadas. Se você quiser dar uma olhada no conteúdo da linha ao mesmo tempo, pode fazer algo assim:

```
SELECT * FROM accounts AS a, pgrowlocks('accounts') AS p
  WHERE p.locked_row = a.ctid;
```

No entanto, esteja ciente de que essa consulta será muito ineficiente.

### F.31.2. Saída de amostra [#](#PGROWLOCKS-SAMPLE-OUTPUT)

```
=# SELECT * FROM pgrowlocks('t1');
 locked_row | locker | multi | xids  |     modes      |  pids
------------+--------+-------+-------+----------------+--------
 (0,1)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,2)      |    609 | f     | {609} | {"For Share"}  | {3161}
 (0,3)      |    607 | f     | {607} | {"For Update"} | {3107}
 (0,4)      |    607 | f     | {607} | {"For Update"} | {3107}
(4 rows)
```

### F.31.3. Autor [#](#PGROWLOCKS-AUTHOR)

Tatsuo Ishii