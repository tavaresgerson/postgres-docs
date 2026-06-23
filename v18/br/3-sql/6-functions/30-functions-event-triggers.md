## 9.30. Funções de Desempenho de Eventos [#](#FUNCTIONS-EVENT-TRIGGERS)

* [9.30.1. Captura de alterações no final do comando](functions-event-triggers.md#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)
* [9.30.2. Processamento de objetos descartados por um comando DDL](functions-event-triggers.md#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)
* [9.30.3. Tratamento de um evento de reescrita de tabela](functions-event-triggers.md#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

O PostgreSQL fornece essas funções auxiliares para recuperar informações de gatilhos de eventos.

Para mais informações sobre gatilhos de eventos, consulte o [Capítulo 38](event-triggers.md).

### 9.30.1. Capturando mudanças no final do comando [#](#PG-EVENT-TRIGGER-DDL-COMMAND-END-FUNCTIONS)

```
pg_event_trigger_ddl_commands () → setof record
```

`pg_event_trigger_ddl_commands` retorna uma lista de comandos DDL executados por cada ação do usuário, quando invocado em uma função anexada a um gatilho de evento `ddl_command_end`. Se chamado em qualquer outro contexto, um erro é exibido. `pg_event_trigger_ddl_commands` retorna uma linha para cada comando de base executado; alguns comandos que são uma única sentença SQL podem retornar mais de uma linha. Esta função retorna as seguintes colunas:



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
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     classid
    </code>
   </td>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    OID do catálogo ao qual o objeto pertence
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     objid
    </code>
   </td>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    OID do próprio objeto
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     objsubid
    </code>
   </td>
   <td>
    <code class="type">
     integer
    </code>
   </td>
   <td>
    ID do subobjeto (por exemplo, número de atributo para uma coluna)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     command_tag
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Tag de comando
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object_type
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Tipo do objeto
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     schema_name
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Nome do esquema ao qual o objeto pertence, se houver; caso contrário
    <code class="literal">
     NULL
    </code>
    . Não há citação aplicada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object_identity
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Renderização textual da identidade do objeto, qualificada por esquema. Cada identificador incluído na identidade é citado, se necessário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     in_extension
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se o comando faz parte de um script de extensão
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     command
    </code>
   </td>
   <td>
    <code class="type">
     pg_ddl_command
    </code>
   </td>
   <td>
    Uma representação completa do comando, em formato interno. Isso não pode ser exibido diretamente, mas pode ser passado para outras funções para obter diferentes informações sobre o comando.
   </td>
  </tr>
 </tbody>
</table>







### 9.30.2. Processamento de Objetos Arrastados por um Comando DDL [#](#PG-EVENT-TRIGGER-SQL-DROP-FUNCTIONS)

```
pg_event_trigger_dropped_objects () → setof record
```

`pg_event_trigger_dropped_objects` retorna uma lista de todos os objetos que foram descartados pelo comando no evento cujo `sql_drop` é chamado. Se chamado em qualquer outro contexto, um erro é gerado. Esta função retorna as seguintes colunas:



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
   <th>
    Descrição
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td>
    <code class="literal">
     classid
    </code>
   </td>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    OID do catálogo ao qual o objeto pertencia
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     objid
    </code>
   </td>
   <td>
    <code class="type">
     oid
    </code>
   </td>
   <td>
    OID do próprio objeto
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     objsubid
    </code>
   </td>
   <td>
    <code class="type">
     integer
    </code>
   </td>
   <td>
    ID do subobjeto (por exemplo, número de atributo para uma coluna)
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     original
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se este fosse um dos objetos raiz(s) da exclusão
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     normal
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se houver uma relação de dependência normal no gráfico de dependência que leva a este objeto
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     is_temporary
    </code>
   </td>
   <td>
    <code class="type">
     boolean
    </code>
   </td>
   <td>
    Verdadeiro se este fosse um objeto temporário
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object_type
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Tipo do objeto
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     schema_name
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Nome do esquema ao qual o objeto pertencia, se houver; caso contrário
    <code class="literal">
     NULL
    </code>
    . Não há citação aplicada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object_name
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Nome do objeto, se a combinação de esquema e nome puder ser usada como um identificador único para o objeto; caso contrário
    <code class="literal">
     NULL
    </code>
    . Não há citação aplicada, e o nome nunca é qualificada por esquema.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     object_identity
    </code>
   </td>
   <td>
    <code class="type">
     text
    </code>
   </td>
   <td>
    Renderização textual da identidade do objeto, qualificada por esquema. Cada identificador incluído na identidade é citado, se necessário.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     address_names
    </code>
   </td>
   <td>
    <code class="type">
     text[]
    </code>
   </td>
   <td>
    Uma série que, juntamente com
    <code class="literal">
     object_type
    </code>
    e
    <code class="literal">
     address_args
    </code>
    , pode ser utilizado por
    <code class="function">
     pg_get_object_address
    </code>
    função para recriar o endereço do objeto em um servidor remoto que contenha um objeto com o mesmo nome e do mesmo tipo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="literal">
     address_args
    </code>
   </td>
   <td>
    <code class="type">
     text[]
    </code>
   </td>
   <td>
    Complemento para
    <code class="literal">
     address_names
    </code>
   </td>
  </tr>
 </tbody>
</table>







A função `pg_event_trigger_dropped_objects` pode ser usada em um gatilho de evento como este:

```
CREATE FUNCTION test_event_trigger_for_drops()
        RETURNS event_trigger LANGUAGE plpgsql AS $$
DECLARE
    obj record;
BEGIN
    FOR obj IN SELECT * FROM pg_event_trigger_dropped_objects()
    LOOP
        RAISE NOTICE '% dropped object: % %.% %',
                     tg_tag,
                     obj.object_type,
                     obj.schema_name,
                     obj.object_name,
                     obj.object_identity;
    END LOOP;
END;
$$;
CREATE EVENT TRIGGER test_event_trigger_for_drops
   ON sql_drop
   EXECUTE FUNCTION test_event_trigger_for_drops();
```

### 9.30.3. Gerenciamento de um Evento de Reescrita de Tabela [#](#PG-EVENT-TRIGGER-TABLE-REWRITE-FUNCTIONS)

As funções mostradas na [Tabela 9.111](functions-event-triggers.md#FUNCTIONS-EVENT-TRIGGER-TABLE-REWRITE) fornecem informações sobre uma tabela para a qual um evento `table_rewrite` foi chamado recentemente. Se chamada em qualquer outro contexto, um erro é exibido.

**Tabela 9.111. Funções de Reescrita de Tabela**



<table border="1" class="table" summary="Table Rewrite Information Functions">
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
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_event_trigger_table_rewrite_oid
     </code>
     ()
     <code class="returnvalue">
      oid
     </code>
    </p>
    <p>
     Retorna o OID da tabela que está prestes a ser reescrita.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code class="function">
      pg_event_trigger_table_rewrite_reason
     </code>
     ()
     <code class="returnvalue">
      integer
     </code>
    </p>
    <p>
     Retorna um código que explica a(s) razão(ões) para a reescrita. O valor é uma bitmap construída a partir dos seguintes valores:
     <code class="literal">
      1
     </code>
     (a tabela mudou sua persistência),
     <code class="literal">
      2
     </code>
     (o valor padrão de uma coluna foi alterado),
     <code class="literal">
      4
     </code>
     (uma coluna tem um novo tipo de dados) e
     <code class="literal">
      8
     </code>
     (o método de acesso à tabela foi alterado).
    </p>
   </td>
  </tr>
 </tbody>
</table>










Essas funções podem ser usadas em um gatilho de evento como este:

```
CREATE FUNCTION test_event_trigger_table_rewrite_oid()
 RETURNS event_trigger
 LANGUAGE plpgsql AS
$$
BEGIN
  RAISE NOTICE 'rewriting table % for reason %',
                pg_event_trigger_table_rewrite_oid()::regclass,
                pg_event_trigger_table_rewrite_reason();
END;
$$;

CREATE EVENT TRIGGER test_table_rewrite_oid
                  ON table_rewrite
   EXECUTE FUNCTION test_event_trigger_table_rewrite_oid();
```
