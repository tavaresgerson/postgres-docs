## Crie TRIGGER

CREATE TRIGGER — definir um novo gatilho

## Sinopse

```
CREATE [ OR REPLACE ] [ CONSTRAINT ] TRIGGER name { BEFORE | AFTER | INSTEAD OF } { event [ OR ... ] }
    ON table_name
    [ FROM referenced_table_name ]
    [ NOT DEFERRABLE | [ DEFERRABLE ] [ INITIALLY IMMEDIATE | INITIALLY DEFERRED ] ]
    [ REFERENCING { { OLD | NEW } TABLE [ AS ] transition_relation_name } [ ... ] ]
    [ FOR [ EACH ] { ROW | STATEMENT } ]
    [ WHEN ( condition ) ]
    EXECUTE { FUNCTION | PROCEDURE } function_name ( arguments )

where event can be one of:

    INSERT
    UPDATE [ OF column_name [, ... ] ]
    DELETE
    TRUNCATE
```

## Descrição

`CREATE TRIGGER` cria um novo gatilho. `CREATE OR REPLACE TRIGGER` irá criar um novo gatilho ou substituir um gatilho existente. O gatilho será associado à tabela, visão ou tabela estrangeira especificada e executará a função especificada *`function_name`* quando certas operações forem realizadas naquela tabela.

Para substituir a definição atual de um gatilho existente, use `CREATE OR REPLACE TRIGGER`, especificando o nome do gatilho existente e a tabela pai. Todas as outras propriedades são substituídas.

O gatilho pode ser especificado para ser disparado antes da operação ser realizada em uma linha (antes que as restrições sejam verificadas e o `INSERT`, `UPDATE` ou `DELETE` seja realizado); ou após a operação ter sido concluída (após que as restrições tenham sido verificadas e o `INSERT`, `UPDATE` ou `DELETE` tenha sido concluído); ou em vez da operação (no caso de inserções, atualizações ou exclusões em uma visão). Se o gatilho for disparado antes ou em vez do evento, o gatilho pode ignorar a operação para a linha atual, ou alterar a linha que está sendo inserida (apenas para as operações `INSERT` e `UPDATE`). Se o gatilho for disparado após o evento, todas as alterações, incluindo os efeitos de outros gatilhos, são “visíveis” para o gatilho.

Um gatilho marcado `FOR EACH ROW` é acionado uma vez para cada linha que a operação modifica. Por exemplo, um `DELETE` que afeta 10 linhas fará com que quaisquer gatilhos `ON DELETE` na relação alvo sejam acionados 10 vezes separadamente, uma vez para cada linha excluída. Em contraste, um gatilho marcado `FOR EACH STATEMENT` só é executado uma vez para qualquer operação dada, independentemente de quantas linhas ele modifique (em particular, uma operação que modifique zero linhas ainda resultará na execução de quaisquer gatilhos `FOR EACH STATEMENT` aplicáveis).

Os gatilhos especificados para disparar o evento de gatilho `INSTEAD OF` devem ser marcados como `FOR EACH ROW`, e só podem ser definidos em visualizações. Os gatilhos `BEFORE` e `AFTER` em uma visualização devem ser marcados como `FOR EACH STATEMENT`.

Além disso, os gatilhos podem ser definidos para disparar para `TRUNCATE`, embora apenas para `FOR EACH STATEMENT`.

O quadro a seguir resume os tipos de gatilho que podem ser usados em tabelas, visualizações e tabelas externas:



<table border="1" class="informaltable">
 <colgroup>
  <col/>
  <col/>
  <col/>
  <col/>
 </colgroup>
 <thead>
  <tr>
   <th>
    When
   </th>
   <th>
    Event
   </th>
   <th>
    Nível de linha
   </th>
   <th>
    Nível de declaração
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td align="center" rowspan="2">
    <code class="literal">
     BEFORE
    </code>
   </td>
   <td align="center">
    <code class="command">
     INSERT
    </code>
    /
    <code class="command">
     UPDATE
    </code>
    /
    <code class="command">
     DELETE
    </code>
   </td>
   <td align="center">
    Tabelas e tabelas estrangeiras
   </td>
   <td align="center">
    Tabelas, visualizações e tabelas externas
   </td>
  </tr>
  <tr>
   <td align="center">
    <code class="command">
     TRUNCATE
    </code>
   </td>
   <td align="center">
    —
   </td>
   <td align="center">
    Tabelas e tabelas estrangeiras
   </td>
  </tr>
  <tr>
   <td align="center" rowspan="2">
    <code class="literal">
     AFTER
    </code>
   </td>
   <td align="center">
    <code class="command">
     INSERT
    </code>
    /
    <code class="command">
     UPDATE
    </code>
    /
    <code class="command">
     DELETE
    </code>
   </td>
   <td align="center">
    Tabelas e tabelas estrangeiras
   </td>
   <td align="center">
    Tabelas, visualizações e tabelas externas
   </td>
  </tr>
  <tr>
   <td align="center">
    <code class="command">
     TRUNCATE
    </code>
   </td>
   <td align="center">
    —
   </td>
   <td align="center">
    Tabelas e tabelas estrangeiras
   </td>
  </tr>
  <tr>
   <td align="center" rowspan="2">
    <code class="literal">
     INSTEAD OF
    </code>
   </td>
   <td align="center">
    <code class="command">
     INSERT
    </code>
    /
    <code class="command">
     UPDATE
    </code>
    /
    <code class="command">
     DELETE
    </code>
   </td>
   <td align="center">
    Visões
   </td>
   <td align="center">
    —
   </td>
  </tr>
  <tr>
   <td align="center">
    <code class="command">
     TRUNCATE
    </code>
   </td>
   <td align="center">
    —
   </td>
   <td align="center">
    —
   </td>
  </tr>
 </tbody>
</table>







Além disso, uma definição de gatilho pode especificar uma condição booleana `WHEN`, que será testada para determinar se o gatilho deve ser disparado. Em gatilhos de nível de linha, a condição `WHEN` pode examinar os valores antigos e/ou novos das colunas da linha. Gatilhos de nível de declaração também podem ter condições `WHEN`, embora o recurso não seja tão útil para eles, uma vez que a condição não pode se referir a quaisquer valores na tabela.

Se vários gatilhos do mesmo tipo forem definidos para o mesmo evento, eles serão disparados em ordem alfabética por nome.

Quando a opção `CONSTRAINT` é especificada, este comando cria um *trigger de restrição*. Isso é o mesmo que um trigger regular, exceto que o momento em que o disparo do trigger pode ser ajustado usando [`SET CONSTRAINTS`](sql-set-constraints.md)]. Os triggers de restrição devem ser triggers `AFTER ROW` em tabelas simples (não em tabelas estrangeiras). Eles podem ser disparados no final da declaração que causa o evento de disparo, ou no final da transação contendo; neste último caso, eles são ditos como *diferidos*. Um disparo de trigger diferido pendente também pode ser forçado a acontecer imediatamente usando `SET CONSTRAINTS`. Espera-se que os triggers de restrição levantem uma exceção quando as restrições que implementam são violadas.

A opção `REFERENCING` permite a coleta de *relações de transição*, que são conjuntos de linhas que incluem todas as linhas inseridas, excluídas ou modificadas pelo atual enunciado SQL. Esse recurso permite que o gatilho veja uma visão global do que o enunciado fez, não apenas uma linha de cada vez. Esta opção só é permitida para um gatilho `AFTER` em uma tabela simples (não em uma tabela estrangeira). O gatilho não deve ser um gatilho de restrição. Além disso, se o gatilho for um gatilho `UPDATE`, ele não deve especificar uma lista *`column_name`* ao usar esta opção. `OLD TABLE` só pode ser especificado uma vez e apenas para um gatilho que pode ser disparado em `UPDATE` ou `DELETE`; ele cria uma relação de transição contendo as *imagens anteriores* de todas as linhas atualizadas ou excluídas pelo enunciado. Da mesma forma, `NEW TABLE` só pode ser especificado uma vez e apenas para um gatilho que pode ser disparado em `UPDATE` ou `INSERT`; ele cria uma relação de transição contendo as *imagens posteriores* de todas as linhas atualizadas ou inseridas pelo enunciado.

`SELECT` não modifica nenhuma linha, portanto, você não pode criar gatilhos `SELECT`. Regras e visualizações podem fornecer soluções viáveis para problemas que parecem precisar de gatilhos `SELECT`.

Consulte o [Capítulo 37](triggers.md) para obter mais informações sobre gatilhos.

## Parâmetros

*`name`*: O nome a ser dado ao novo gatilho. Este deve ser distinto do nome de qualquer outro gatilho para a mesma tabela. O nome não pode ser qualificado pelo esquema — o gatilho herda o esquema de sua tabela. Para um gatilho de restrição, este é também o nome a ser usado ao modificar o comportamento do gatilho usando `SET CONSTRAINTS`.

`BEFORE` `AFTER` `INSTEAD OF`: Determina se a função é chamada antes, depois ou em vez do evento. Um gatilho de restrição só pode ser especificado como `AFTER`.

*`event`*: Um dos `INSERT`, `UPDATE`, `DELETE` ou `TRUNCATE`; este especifica o evento que acionará o gatilho. Múltiplos eventos podem ser especificados usando `OR`, exceto quando relações de transição são solicitadas.

Para eventos de `UPDATE`, é possível especificar uma lista de colunas usando essa sintaxe:

```
UPDATE OF column_name1 [, column_name2 ... ]
```

O gatilho só será disparado se pelo menos uma das colunas listadas for mencionada como alvo do comando `UPDATE` ou se uma das colunas listadas for uma coluna gerada que depende de uma coluna que é alvo do `UPDATE`.

Os eventos `INSTEAD OF UPDATE` não permitem uma lista de colunas. Uma lista de colunas também não pode ser especificada ao solicitar relações de transição.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela, visão ou tabela externa para a qual o gatilho está configurado.

*`referenced_table_name`*: O nome (possivelmente qualificado por esquema) de outra tabela referenciada pela restrição. Esta opção é usada para restrições de chave estrangeira e não é recomendada para uso geral. Isso só pode ser especificado para gatilhos de restrição.

`DEFERRABLE` `NOT DEFERRABLE` `INITIALLY IMMEDIATE` `INITIALLY DEFERRED`: O momento padrão do gatilho. Consulte a documentação do [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter detalhes dessas opções de restrição. Isso só pode ser especificado para gatilhos de restrição.

`REFERENCING`: Esta palavra-chave precede imediatamente a declaração de um ou dois nomes de relação que fornecem acesso às relações de transição da declaração desencadeadora.

`OLD TABLE` `NEW TABLE`: Esta cláusula indica se o nome da relação a seguir é para a relação de transição antes da imagem ou para a relação de transição após a imagem.

*`transition_relation_name`*: O nome (não qualificado) a ser usado dentro do gatilho para essa relação de transição.

`FOR EACH ROW`: `FOR EACH STATEMENT`: Isso especifica se a função de gatilho deve ser acionada uma vez para cada linha afetada pelo evento de gatilho, ou apenas uma vez por declaração SQL. Se nenhuma das opções for especificada, `FOR EACH STATEMENT` é a opção padrão. Gatilhos de restrição só podem ser especificados `FOR EACH ROW`.

*`condition`*: Uma expressão booleana que determina se a função de gatilho será realmente executada. Se `WHEN` for especificado, a função será chamada apenas se o *`condition`* retornar `true`. Nos gatilhos de `FOR EACH ROW`, a condição `WHEN` pode se referir a colunas dos valores da linha antiga e/ou nova, escrevendo `OLD.column_name` ou `NEW.column_name`, respectivamente. Claro, os gatilhos de `INSERT` não podem se referir a `OLD` e os gatilhos de `DELETE` não podem se referir a `NEW`.

Os gatilhos `INSTEAD OF` não suportam condições `WHEN`.

Atualmente, as expressões `WHEN` não podem conter subconsultas.

Observe que, para gatilhos de restrição, a avaliação da condição `WHEN` não é adiada, mas ocorre imediatamente após a operação de atualização da linha ser realizada. Se a condição não for avaliada como verdadeira, o gatilho não será enfileirado para execução diferida.

*`function_name`*: Uma função fornecida pelo usuário que é declarada sem argumentos e retorna o tipo `trigger`, que é executada quando o gatilho é acionado.

Na sintaxe de `CREATE TRIGGER`, as palavras-chave `FUNCTION` e `PROCEDURE` são equivalentes, mas a função referenciada deve, em qualquer caso, ser uma função, não um procedimento. O uso da palavra-chave `PROCEDURE` aqui é histórico e desatualizado.

*`arguments`*: Uma lista opcional de argumentos separados por vírgula que devem ser fornecidos à função quando o gatilho é executado. Os argumentos são constantes de cadeia literal. Nomes simples e constantes numéricas também podem ser escritos aqui, mas todos eles serão convertidos em cadeias de caracteres. Por favor, verifique a descrição do idioma de implementação da função do gatilho para descobrir como esses argumentos podem ser acessados dentro da função; isso pode ser diferente dos argumentos normais da função.

## Notas

Para criar ou substituir um gatilho em uma tabela, o usuário deve ter o privilégio `TRIGGER` na tabela. O usuário também deve ter o privilégio `EXECUTE` na função do gatilho.

Use `DROP TRIGGER`(sql-droptrigger.md "DROP TRIGGER") para remover um gatilho.

Criar um gatilho de nível de linha em uma tabela particionada fará com que um gatilho idêntico seja criado em cada uma de suas particionamentos existentes; e quaisquer particionamentos criados ou anexados posteriormente também terão um gatilho idêntico. Se houver um gatilho com nome conflitante em uma particionamento filho já existente, ocorrerá um erro, a menos que `CREATE OR REPLACE TRIGGER` seja usado, no caso em que esse gatilho é substituído por um gatilho clone. Quando uma particionamento é desconectada de seu pai, seus gatilhos clonados são removidos.

Um gatilho específico para uma coluna (um definido usando a sintaxe `UPDATE OF column_name`) será acionado quando qualquer uma de suas colunas estiver listada como alvo na lista `SET` do comando `UPDATE`. É possível que o valor de uma coluna mude mesmo quando o gatilho não é acionado, porque as alterações feitas no conteúdo da linha por gatilhos `BEFORE UPDATE` não são consideradas. Por outro lado, um comando como `UPDATE ... SET x = x ...` acionará um gatilho na coluna `x`, mesmo que o valor da coluna não tenha mudado.

Em um gatilho `BEFORE`, a condição `WHEN` é avaliada logo antes da função ser ou ser executada, então usar `WHEN` não é materialmente diferente de testar a mesma condição no início da função do gatilho. Note, em particular, que a linha `NEW` vista pela condição é o valor atual, possivelmente modificado por gatilhos anteriores. Além disso, a condição `BEFORE` de um gatilho `WHEN` não é permitida para examinar as colunas do sistema da linha `NEW` (como `ctid`, por exemplo), porque essas colunas ainda não serão definidas.

Em um gatilho `AFTER`, a condição `WHEN` é avaliada logo após a atualização da linha ocorrer, e determina se um evento deve ser enfileirado para acionar o gatilho no final da declaração. Portanto, quando a condição `WHEN` de um gatilho `AFTER` não retorna verdadeira, não é necessário enfileirar um evento nem refazer a linha no final da declaração. Isso pode resultar em melhorias significativas em declarações que modificam muitas linhas, se o gatilho precisar ser acionado apenas para algumas das linhas.

Em alguns casos, é possível que um único comando SQL execute mais de um tipo de gatilho. Por exemplo, um `INSERT` com uma cláusula `ON CONFLICT DO UPDATE` pode causar operações de inserção e atualização, portanto, ele acionará ambos os tipos de gatilhos conforme necessário. As relações de transição fornecidas aos gatilhos são específicas ao seu tipo de evento; assim, um gatilho `INSERT` verá apenas as linhas inseridas, enquanto um gatilho `UPDATE` verá apenas as linhas atualizadas.

As atualizações ou exclusões de linha causadas por ações de enforcement de chave estrangeira, como `ON UPDATE CASCADE` ou `ON DELETE SET NULL`, são tratadas como parte do comando SQL que as causou (observe que tais ações nunca são diferidas). Os gatilhos relevantes na tabela afetada serão acionados, para que isso forneça outra maneira em que um comando SQL pode acionar gatilhos que não correspondem diretamente ao seu tipo. Em casos simples, os gatilhos que solicitam relações de transição verão todas as alterações causadas em sua tabela por um único comando SQL original como uma única relação de transição. No entanto, há casos em que a presença de um gatilho `AFTER ROW` que solicita relações de transição causará as ações de enforcement de chave estrangeira desencadeadas por um único comando SQL serem divididas em múltiplos passos, cada um com sua própria(s) relação(ões) de transição. Nesses casos, quaisquer gatilhos de nível de declaração que estejam presentes serão acionados uma vez por criação de um conjunto de relações de transição, garantindo que os gatilhos vejam cada linha afetada em uma relação de transição uma vez e apenas uma vez.

Os gatilhos de nível de declaração em uma visão são acionados apenas se a ação na visão for tratada por um gatilho `INSTEAD OF` de nível de linha. Se a ação for tratada por uma regra `INSTEAD`, então quaisquer declarações emitidas pela regra são executadas no lugar da declaração original que nomeia a visão, de modo que os gatilhos que serão acionados são aqueles em tabelas nomeadas nas declarações de substituição. Da mesma forma, se a visão for automaticamente atualizável, então a ação é tratada pela reescrita automática da declaração em uma ação na tabela base da visão, de modo que os gatilhos de nível de declaração da tabela base são os que são acionados.

A modificação de uma tabela dividida ou de uma tabela com filhos hereditários aciona gatilhos de nível de declaração vinculados à tabela explicitamente nomeada, mas não gatilhos de nível de declaração para suas partições ou tabelas de filho. Em contraste, os gatilhos de nível de linha são acionados nas linhas das partições afetadas ou nas tabelas de filho, mesmo que não estejam explicitamente nomeadas na consulta. Se um gatilho de nível de declaração tiver sido definido com relações de transição nomeadas por uma cláusula `REFERENCING`, então as imagens antes e depois das linhas são visíveis de todas as partições afetadas ou tabelas de filho. No caso de filhos hereditários, as imagens de linha incluem apenas as colunas presentes na tabela à qual o gatilho está vinculado.

Atualmente, os gatilhos de nível de linha com relações de transição não podem ser definidos em partições ou em tabelas filhas de herança. Além disso, os gatilhos em tabelas particionadas podem não ser `INSTEAD OF`.

Atualmente, a opção `OR REPLACE` não é suportada para gatilhos de restrição.

Não é recomendado substituir um gatilho existente dentro de uma transação que já realizou ações de atualização na tabela do gatilho. As decisões de disparo do gatilho, ou partes das decisões de disparo, que já foram feitas, não serão reconsideradas, portanto, os efeitos podem ser surpreendentes.

Existem algumas funções de gatilho integradas que podem ser usadas para resolver problemas comuns sem precisar escrever seu próprio código de gatilho; veja [Seção 9.29](functions-trigger.md).

## Exemplos

Execute a função `check_account_update` sempre que uma linha da tabela `accounts` estiver prestes a ser atualizada:

```
CREATE TRIGGER check_update BEFORE UPDATE ON accounts FOR EACH ROW EXECUTE FUNCTION check_account_update();
```

Modifique essa definição de gatilho para executar a função apenas se a coluna `balance` for especificada como alvo no comando `UPDATE`:

```
CREATE OR REPLACE TRIGGER check_update BEFORE UPDATE OF balance ON accounts FOR EACH ROW EXECUTE FUNCTION check_account_update();
```

Este formulário só executa a função se a coluna `balance` tiver, de fato, mudado o valor:

```
CREATE TRIGGER check_update BEFORE UPDATE ON accounts FOR EACH ROW WHEN (OLD.balance IS DISTINCT FROM NEW.balance) EXECUTE FUNCTION check_account_update();
```

Chame uma função para registrar as atualizações de `accounts`, mas apenas se algo tiver sido alterado:

```
CREATE TRIGGER log_update AFTER UPDATE ON accounts FOR EACH ROW WHEN (OLD.* IS DISTINCT FROM NEW.*) EXECUTE FUNCTION log_account_update();
```

Execute a função `view_insert_row` para cada linha para inserir linhas nas tabelas que fundamentam uma visão:

```
CREATE TRIGGER view_insert INSTEAD OF INSERT ON my_view FOR EACH ROW EXECUTE FUNCTION view_insert_row();
```

Execute a função `check_transfer_balances_to_zero` para cada declaração para confirmar que o deslocamento das linhas `transfer` para uma rede de zero:

```
CREATE TRIGGER transfer_insert AFTER INSERT ON transfer REFERENCING NEW TABLE AS inserted FOR EACH STATEMENT EXECUTE FUNCTION check_transfer_balances_to_zero();
```

Execute a função `check_matching_pairs` para cada linha para confirmar que as alterações são feitas em pares correspondentes ao mesmo tempo (pelo mesmo enunciado):

```
CREATE TRIGGER paired_items_update AFTER UPDATE ON paired_items REFERENCING NEW TABLE AS newtab OLD TABLE AS oldtab FOR EACH ROW EXECUTE FUNCTION check_matching_pairs();
```

[Seção 37.4] (trigger-example.md "37.4. A Complete Trigger Example") contém um exemplo completo de uma função de gatilho escrita em C.

## Compatibilidade

A declaração `CREATE TRIGGER` no PostgreSQL implementa um subconjunto do padrão SQL. As seguintes funcionalidades estão atualmente ausentes:

* Embora os nomes das tabelas de transição para os gatilhos `AFTER` sejam especificados usando a cláusula `REFERENCING` da maneira padrão, as variáveis de linha usadas nos gatilhos `FOR EACH ROW` podem não ser especificadas em uma cláusula `REFERENCING`. Elas estão disponíveis de uma maneira que depende do idioma em que a função de gatilho é escrita, mas é fixa para qualquer idioma. Algumas linguagens se comportam efetivamente como se houvesse uma cláusula `REFERENCING` contendo `OLD ROW AS OLD NEW ROW AS NEW`.
* O padrão permite que as tabelas de transição sejam usadas com gatilhos `UPDATE` específicos de coluna, mas então o conjunto de linhas que deve ser visível nas tabelas de transição depende da lista de colunas do gatilho. Isso atualmente não é implementado pelo PostgreSQL.
* O PostgreSQL só permite a execução de uma função definida pelo usuário para a ação desencadeada. O padrão permite a execução de vários outros comandos SQL, como `CREATE TABLE`, como ação desencadeada. Essa limitação não é difícil de contornar criando uma função definida pelo usuário que execute os comandos desejados.

O SQL especifica que múltiplos gatilhos devem ser disparados na ordem do momento da criação. O PostgreSQL usa a ordem do nome, que foi julgada mais conveniente.

O SQL especifica que os gatilhos `BEFORE DELETE` em apagamentos em cascata são acionados *após* o `DELETE` em cascata ser concluído. O comportamento do PostgreSQL é que o `BEFORE DELETE` sempre seja acionado antes da ação de apagamento, mesmo em cascata. Isso é considerado mais consistente. Há também um comportamento não padrão se os gatilhos `BEFORE` modificarem linhas ou impedirem atualizações durante uma atualização causada por uma ação referencial. Isso pode levar a violações de restrições ou dados armazenados que não respeitam a restrição referencial.

A capacidade de especificar múltiplas ações para um único gatilho usando `OR` é uma extensão do padrão SQL do PostgreSQL.

A capacidade de disparar gatilhos para `TRUNCATE` é uma extensão do padrão SQL do PostgreSQL, assim como a capacidade de definir gatilhos em nível de declaração em vistas.

`CREATE CONSTRAINT TRIGGER` é uma extensão do PostgreSQL do padrão SQL. Assim como a opção `OR REPLACE`.

## Veja também

[ALTER TRIGGER](sql-altertrigger.md "ALTER TRIGGER"), [DROP TRIGGER](sql-droptrigger.md "DROP TRIGGER"), [CREATE FUNCTION](sql-createfunction.md "CREATE FUNCTION"), [SET CONSTRAINTS](sql-set-constraints.md "SET CONSTRAINTS")