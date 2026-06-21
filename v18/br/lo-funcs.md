## 33.4. Funções no lado do servidor [#](#LO-FUNCS)

As funções do lado do servidor, adaptadas para manipular objetos grandes a partir do SQL, estão listadas em [Tabela 33.1](lo-funcs.md#LO-FUNCS-TABLE).

**Tabela 33.1. Funções de Objeto Grande Orientado a SQL**



<table border="1" class="table" summary="SQL-Oriented Large Object Functions">
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
     <code class="function">
      lo_from_bytea
     </code>
     (
     <em class="parameter">
      <code>
       loid
      </code>
     </em>
     <code class="type">
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       data
      </code>
     </em>
     <code class="type">
      bytea
     </code>
     ) →
     <code class="returnvalue">
      oid
     </code>
    </p>
    <p>
     Creates a large object and stores
     <em class="parameter">
      <code>
       data
      </code>
     </em>
     in it. If
     <em class="parameter">
      <code>
       loid
      </code>
     </em>
     is zero then the system will choose a free OID, otherwise that OID is used (with an error if some large object already has that OID).  On success, the large object's OID is returned.
    </p>
    <p>
     <code class="literal">
      lo_from_bytea(0, '\xffffff00')
     </code>
     →
     <code class="returnvalue">
      24528
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lo_put
     </code>
     (
     <em class="parameter">
      <code>
       loid
      </code>
     </em>
     <code class="type">
      oid
     </code>
     ,
     <em class="parameter">
      <code>
       offset
      </code>
     </em>
     <code class="type">
      bigint
     </code>
     ,
     <em class="parameter">
      <code>
       data
      </code>
     </em>
     <code class="type">
      bytea
     </code>
     ) →
     <code class="returnvalue">
      void
     </code>
    </p>
    <p>
     Writes
     <em class="parameter">
      <code>
       data
      </code>
     </em>
     starting at the given offset within the large object; the large object is enlarged if necessary.
    </p>
    <p>
     <code class="literal">
      lo_put(24528, 1, '\xaa')
     </code>
     →
     <code class="returnvalue">
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      lo_get
     </code>
     (
     <em class="parameter">
      <code>
       loid
      </code>
     </em>
     <code class="type">
      oid
     </code>
     [
     <span class="optional">
      ,
      <em class="parameter">
       <code>
        offset
       </code>
      </em>
      <code class="type">
       bigint
      </code>
      ,
      <em class="parameter">
       <code>
        length
       </code>
      </em>
      <code class="type">
       integer
      </code>
     </span>
     ] ) →
     <code class="returnvalue">
      bytea
     </code>
    </p>
    <p>
     Extracts the large object's contents, or a substring thereof.
    </p>
    <p>
     <code class="literal">
      lo_get(24528, 0, 3)
     </code>
     →
     <code class="returnvalue">
      \xffaaff
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>









Existem funções adicionais no lado do servidor correspondentes a cada uma das funções do lado do cliente descritas anteriormente; de fato, na maior parte, as funções do lado do cliente são simplesmente interfaces para as funções equivalentes do lado do servidor. As que são igualmente convenientes para serem chamadas por meio de comandos SQL são `lo_creat`, `lo_create`, `lo_unlink`, `lo_import` e `lo_export`. Aqui estão exemplos de seu uso:

```
CREATE TABLE image (
    name            text,
    raster          oid
);

SELECT lo_creat(-1);       -- returns OID of new, empty large object

SELECT lo_create(43213);   -- attempts to create large object with OID 43213

SELECT lo_unlink(173454);  -- deletes large object with OID 173454

INSERT INTO image (name, raster)
    VALUES ('beautiful image', lo_import('/etc/motd'));

INSERT INTO image (name, raster)  -- same as above, but specify OID to use
    VALUES ('beautiful image', lo_import('/etc/motd', 68583));

SELECT lo_export(image.raster, '/tmp/motd') FROM image
    WHERE name = 'beautiful image';
```

As funções `lo_import` e `lo_export` do lado do servidor se comportam de maneira consideravelmente diferente de suas análogas do lado do cliente. Essas duas funções leem e escrevem arquivos no sistema de arquivos do servidor, usando as permissões do usuário proprietário do banco de dados. Portanto, por padrão, seu uso é restrito a superusuários. Em contraste, as funções de importação e exportação do lado do cliente leem e escrevem arquivos no sistema de arquivos do cliente, usando as permissões do programa do cliente. As funções do lado do cliente não requerem quaisquer privilégios de banco de dados, exceto o privilégio de ler ou escrever o objeto grande em questão.

### Atenção

É possível [[GRANT]] o uso dos (sql-grant.md "GRANT") funções de lado do servidor e `lo_import` e `lo_export` para usuários não superusuários, mas é necessário considerar cuidadosamente as implicações de segurança. Um usuário malicioso desses privilégios poderia facilmente transformá-los em superusuário (por exemplo, reescrevendo arquivos de configuração do servidor) ou poderia atacar o resto do sistema de arquivos do servidor sem se preocupar em obter privilégios de superusuário do banco de dados. *Portanto, o acesso a funções com esses privilégios deve ser protegido com a mesma cautela que o acesso a funções de superusuário.* No entanto, se o uso de `lo_import` ou `lo_export` do lado do servidor for necessário para uma tarefa rotineira, é mais seguro usar um papel com esses privilégios do que um com privilégios de superusuário completos, pois isso ajuda a reduzir o risco de danos por erros acidentais.

A funcionalidade de `lo_read` e `lo_write` também está disponível por meio de chamadas do lado do servidor, mas os nomes das funções do lado do servidor diferem das interfaces do lado do cliente, pois não contêm sublinhados. Você deve chamar essas funções como `loread` e `lowrite`.