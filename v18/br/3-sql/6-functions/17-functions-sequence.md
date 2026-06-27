### 9.17. Funções de manipulação de sequência [#](#FUNCTIONS-SEQUENCE)

Esta seção descreve funções para operar em objetos de sequência, também chamados de geradores de sequência ou simplesmente sequências. Os objetos de sequência são tabelas especiais de uma única linha criadas com [CREATE SEQUENCE](sql-createsequence.md "CREATE SEQUENCE"). Os objetos de sequência são comumente usados para gerar identificadores únicos para as linhas de uma tabela. As funções de sequência, listadas em [Tabela 9.55](functions-sequence.md#FUNCTIONS-SEQUENCE-TABLE "Table 9.55. Sequence Functions"), fornecem métodos simples e seguros para múltiplos usuários para obter valores de sequência consecutivos a partir de objetos de sequência.

**Tabela 9.55. Funções de sequência**

<table>
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
     <code>
      nextval
     </code>
     (
     <code>
      regclass
     </code>
     )
     <code>
      bigint
     </code>
    </p>
    <p>
     Avança o objeto de sequência para seu próximo valor e retorna esse valor. Isso é feito de forma atômica: mesmo que várias sessões executem
     <code>
      nextval
     </code>
     concomitantemente, cada um receberá, de forma segura, um valor de sequência distinto. Se o objeto de sequência tiver sido criado com parâmetros padrão, sucessivos
     <code>
      nextval
     </code>
     As chamadas retornarão valores sucessivos que começam com 1. Outros comportamentos podem ser obtidos usando parâmetros apropriados no
     <a class="xref" href="sql-createsequence.md" title="CREATE SEQUENCE">
      <span class="refentrytitle">
       Crie Sequência
      </span>
     </a>
     command.
    </p>
    <p>
     Esta função requer
     <code>
      USAGE
     </code>
     ou
     <code>
      UPDATE
     </code>
     privilégio na sequência.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      setval
     </code>
     (
     <code>
      regclass
     </code>
     ,
     <code>
      bigint
     </code>
     [
     <span class="optional">
      ,
      <code>
       boolean
      </code>
     </span>
     ] )
     <code>
      bigint
     </code>
    </p>
    <p>
     Define o valor atual do objeto de sequência e, opcionalmente, sua
     <code>
      is_called
     </code>
     flag. A forma de dois parâmetros define a sequência
     <code>
      last_value
     </code>
     campo para o valor especificado e define seu
     <code>
      is_called
     </code>
     campo para
     <code>
      true
     </code>
     , ou seja, a próxima
     <code>
      nextval
     </code>
     avançar a sequência antes de retornar um valor. O valor que será relatado por
     <code>
      currval
     </code>
     também é definido para o valor especificado. Na forma de três parâmetros,
     <code>
      is_called
     </code>
     pode ser configurada para qualquer uma das opções
     <code>
      true
     </code>
     ou
     <code>
      false
     </code>
     .
     <code>
      true
     </code>
     tem o mesmo efeito que a forma de dois parâmetros. Se estiver definido como
     <code>
      false
     </code>
     , a próxima
     <code>
      nextval
     </code>
     retornará exatamente o valor especificado, e o avanço da sequência começa com o seguinte
     <code>
      nextval
     </code>
     Além disso, o valor relatado por
     <code>
      currval
     </code>
     não é alterado neste caso. Por exemplo,
    </p>
    <pre class="programlisting">
SELECT setval('myseq', 42);           Próximo<code>nextval</code>retornará 43 SELECT setval('myseq', 42, true);     O mesmo que acima SELECT setval('myseq', 42, false);    Próximo<code>nextval</code>retornará 42
</pre>
    <p>
     O resultado retornado por
     <code>
      setval
     </code>
     é apenas o valor do seu segundo argumento.
    </p>
    <p>
     Esta função requer
     <code>
      UPDATE
     </code>
     privilégio na sequência.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      currval
     </code>
     (
     <code>
      regclass
     </code>
     )
     <code>
      bigint
     </code>
    </p>
    <p>
     Retorna o valor obtido mais recentemente por
     <code>
      nextval
     </code>
     para esta sequência na sessão atual. (Um erro é relatado se
     <code>
      nextval
     </code>
     nunca foi chamada para essa sequência nesta sessão.) Como isso está retornando um valor local da sessão, ele dá uma resposta previsível, independentemente de outras sessões terem executado ou
     <code>
      nextval
     </code>
     como a sessão atual já fez.
    </p>
    <p>
     Esta função requer
     <code>
      USAGE
     </code>
     ou
     <code>
      SELECT
     </code>
     privilégio na sequência.
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      lastval
     </code>
     ()
     <code>
      bigint
     </code>
    </p>
    <p>
     Retorna o valor mais recentemente retornado por
     <code>
      nextval
     </code>
     na sessão atual. Esta função é identicamente igual a
     <code>
      currval
     </code>
     , exceto que, em vez de tomar o nome da sequência como argumento, ele se refere a qualquer sequência
     <code>
      nextval
     </code>
     foi mais recentemente aplicado na sessão atual. É um erro chamar
     <code>
      lastval
     </code>
     se
     <code>
      nextval
     </code>
     não foi convocada ainda na sessão atual.
    </p>
    <p>
     Esta função requer
     <code>
      USAGE
     </code>
     ou
     <code>
      SELECT
     </code>
     privilegio na última sequência usada.
    </p>
   </td>
  </tr>
 </tbody>
</table>

Atenção

Para evitar bloquear transações concorrentes que obtêm números da mesma sequência, o valor obtido por `nextval` não é recuperado para uso novamente se a transação solicitante for cancelada posteriormente. Isso significa que abortos de transações ou falhas no banco de dados podem resultar em lacunas na sequência de valores atribuídos. Isso também pode acontecer sem um aborto de transação. Por exemplo, um `INSERT` com uma cláusula `ON CONFLICT` calculará o tuplo a ser inserido, incluindo a realização de quaisquer chamadas necessárias `nextval`, antes de detectar qualquer conflito que o faça seguir a regra `ON CONFLICT` em vez disso. Assim, os objetos de sequência do PostgreSQL *não podem ser usados para obter sequências sem lacunas*.

Da mesma forma, as mudanças de estado de sequência feitas por `setval` são imediatamente visíveis para outras transações e não são desfeitas se a transação que as fez retornar.

Se o grupo de bancos de dados falhar antes de comprometer uma transação que contém uma chamada de `nextval` ou `setval`, a mudança do estado da sequência pode não ter sido armazenada no armazenamento persistente, de modo que é incerto se a sequência terá seu estado original ou atualizado após o restabelecimento do grupo. Isso é inócuo para o uso da sequência dentro do banco de dados, uma vez que outros efeitos das transações não comprometidas também não serão visíveis. No entanto, se você deseja usar um valor de sequência para fins persistentes fora do banco de dados, certifique-se de que a chamada de `nextval` tenha sido comprometida antes de fazer isso.

A sequência que será operada por uma função de sequência é especificada por um argumento `regclass`, que é simplesmente o OID da sequência no catálogo de sistema `pg_class`. No entanto, você não precisa procurar o OID manualmente, pois o conversor de entrada do tipo de dados `regclass` fará o trabalho por você. Veja [Seção 8.19](datatype-oid.md) para detalhes.