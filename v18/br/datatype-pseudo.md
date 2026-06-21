## 8.21. Pseudo-tipos [#](#DATATYPE-PSEUDO)

O sistema de tipos do PostgreSQL contém várias entradas de propósito especial que são coletivamente chamadas de *pseudo-tipos*. Um pseudo-tipo não pode ser usado como um tipo de dados de coluna, mas pode ser usado para declarar o tipo de argumento ou resultado de uma função. Cada um dos pseudo-tipos disponíveis é útil em situações em que o comportamento de uma função não corresponde a simplesmente tomar ou retornar um valor de um tipo de dados específico do SQL. [Tabela 8.27](datatype-pseudo.md#DATATYPE-PSEUDOTYPES-TABLE) lista os pseudo-tipos existentes.

**Tabela 8.27. Pseudo-tipos**



<table border="1" class="table" summary="Pseudo-Types">
 <colgroup>
  <col class="col1"/>
  <col class="col2"/>
 </colgroup>
 <thead>
  <tr>
   <th>
    Name
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
     any
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados de entrada.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anyelement
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anyarray
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados de matriz (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anynonarray
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados que não seja um array (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anyenum
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados enum (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    e
    <a class="xref" href="datatype-enum.md" title="8.7. Enumerated Types">
     Seção 8.7
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anyrange
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados de intervalo
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    e
    <a class="xref" href="rangetypes.md" title="8.17. Range Types">
     Seção 8.17
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anymultirange
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados multirange (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    e
    <a class="xref" href="rangetypes.md" title="8.17. Range Types">
     Seção 8.17
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anycompatible
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados, com promoção automática de múltiplos argumentos para um tipo de dados comum (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anycompatiblearray
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados de matriz, com promoção automática de vários argumentos para um tipo de dados comum (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anycompatiblenonarray
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados que não seja um array, com promoção automática de múltiplos argumentos para um tipo de dados comum (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anycompatiblerange
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados de intervalo, com promoção automática de vários argumentos para um tipo de dados comum (consulte
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    e
    <a class="xref" href="rangetypes.md" title="8.17. Range Types">
     Seção 8.17
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     anycompatiblemultirange
    </code>
   </td>
   <td>
    Indica que uma função aceita qualquer tipo de dados multirange, com promoção automática de múltiplos argumentos para um tipo de dados comum (veja
    <a class="xref" href="extend-type-system.md#EXTEND-TYPES-POLYMORPHIC" title="36.2.5. Polymorphic Types">
     Seção 36.2.5
    </a>
    e
    <a class="xref" href="rangetypes.md" title="8.17. Range Types">
     Seção 8.17
    </a>
    ).
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     cstring
    </code>
   </td>
   <td>
    Indica que uma função aceita ou retorna uma cadeia de caracteres C terminada por nulo.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     internal
    </code>
   </td>
   <td>
    Indica que uma função aceita ou retorna um tipo de dados interno do servidor.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     language_handler
    </code>
   </td>
   <td>
    Um controlador de chamada de linguagem procedural é declarado para retornar
    <code class="type">
     language_handler
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     fdw_handler
    </code>
   </td>
   <td>
    Um manipulador de wrapper de dados estrangeiros é declarado para retornar
    <code class="type">
     fdw_handler
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     table_am_handler
    </code>
   </td>
   <td>
    Um manipulador de método de acesso a tabela é declarado para retornar
    <code class="type">
     table_am_handler
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     index_am_handler
    </code>
   </td>
   <td>
    Um manipulador de método de acesso ao índice é declarado para retornar
    <code class="type">
     index_am_handler
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     tsm_handler
    </code>
   </td>
   <td>
    Um manipulador de amostra de tabela é declarado para retornar
    <code class="type">
     tsm_handler
    </code>
    .
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     record
    </code>
   </td>
   <td>
    Identifica uma função que recebe ou retorna um tipo de linha não especificado.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     trigger
    </code>
   </td>
   <td>
    Uma função de gatilho é declarada para retornar
    <code class="type">
     trigger.
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     event_trigger
    </code>
   </td>
   <td>
    Uma função de gatilho de evento é declarada para retornar
    <code class="type">
     event_trigger.
    </code>
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     pg_ddl_command
    </code>
   </td>
   <td>
    Identifica uma representação de comandos DDL que está disponível para gatilhos de evento.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     void
    </code>
   </td>
   <td>
    Indica que uma função não retorna nenhum valor.
   </td>
  </tr>
  <tr>
   <td>
    <code class="type">
     unknown
    </code>
   </td>
   <td>
    Identifica um tipo ainda não resolvido, por exemplo, de uma literal de string não decorada.
   </td>
  </tr>
 </tbody>
</table>









As funções codificadas em C (seja embutidas ou carregadas dinamicamente) podem ser declaradas para aceitar ou retornar qualquer um desses pseudotípicos. Cabe ao autor da função garantir que a função se comporte de forma segura quando um pseudotípico é usado como tipo de argumento.

As funções codificadas em linguagens procedimentais podem usar pseudotipos apenas conforme permitido por suas linguagens de implementação. Atualmente, a maioria das linguagens procedimentais proíbe o uso de um pseudotipo como tipo de argumento e permite apenas `void` e `record` como tipo de resultado (mais `trigger` ou `event_trigger` quando a função é usada como um gatilho ou gatilho de evento). Algumas também suportam funções polimórficas usando os pseudotipos polimórficos, que são mostrados acima e discutidos em detalhes em [Seção 36.2.5](extend-type-system.md#EXTEND-TYPES-POLYMORPHIC).

O pseudo-tipo `internal` é usado para declarar funções que devem ser chamadas apenas internamente pelo sistema de banco de dados, e não por invocação direta em uma consulta SQL. Se uma função tiver pelo menos um argumento do tipo `internal`, ela não pode ser chamada a partir do SQL. Para preservar a segurança do tipo dessa restrição, é importante seguir essa regra de codificação: não criar nenhuma função declarada para retornar `internal`, a menos que tenha pelo menos um argumento do tipo `internal`.