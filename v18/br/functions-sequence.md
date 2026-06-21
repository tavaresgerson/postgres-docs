## 9.17. Funções de manipulação de sequência [#](#FUNCTIONS-SEQUENCE)

Esta seção descreve funções para operar em objetos de sequência, também chamados de geradores de sequência ou simplesmente sequências. Os objetos de sequência são tabelas especiais de uma única linha criadas com [CREATE SEQUENCE](sql-createsequence.md "CREATE SEQUENCE"). Os objetos de sequência são comumente usados para gerar identificadores únicos para as linhas de uma tabela. As funções de sequência, listadas em [Tabela 9.55](functions-sequence.md#FUNCTIONS-SEQUENCE-TABLE "Table 9.55. Sequence Functions"), fornecem métodos simples e seguros para múltiplos usuários para obter valores de sequência consecutivos a partir de objetos de sequência.

**Tabela 9.55. Funções de sequência**



<table border="1" class="table" summary="Sequence Functions">
<colgroup>
<col/>
</colgroup>
<thead>
<tr>
<th class="func_table_entry">
<p class="func_signature">Função</p>
<p>Descrição</p>
</th>
</tr>
</thead>
<tbody>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      nextval
     </code>(<code class="type">
      regclass
     </code>)<code class="returnvalue">
      bigint
     </code>
</p>
<p>Avança o objeto de sequência para seu próximo valor e retorna esse valor. Isso é feito de forma atômica: mesmo que várias sessões executem<code class="function">
      nextval
     </code>concomitantemente, cada um receberá, de forma segura, um valor de sequência distinto. Se o objeto de sequência tiver sido criado com parâmetros padrão, sucessivos<code class="function">
      nextval
     </code>As chamadas retornarão valores sucessivos que começam com 1. Outros comportamentos podem ser obtidos usando parâmetros apropriados no<a class="xref" href="sql-createsequence.md" title="CREATE SEQUENCE">
<span class="refentrytitle">Crie Sequência</span>
</a>
     command.
    </p>
<p>Esta função requer<code class="literal">
      USAGE
     </code>ou<code class="literal">
      UPDATE
     </code>privilégio na sequência.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      setval
     </code>(<code class="type">
      regclass
     </code>,<code class="type">
      bigint
     </code>[<span class="optional">,<code class="type">
       boolean
      </code>
</span>] )<code class="returnvalue">
      bigint
     </code>
</p>
<p>Define o valor atual do objeto de sequência e, opcionalmente, sua<code class="literal">
      is_called
     </code>flag. A forma de dois parâmetros define a sequência<code class="literal">
      last_value
     </code>campo para o valor especificado e define seu<code class="literal">
      is_called
     </code>campo para<code class="literal">
      true
     </code>, ou seja, a próxima<code class="function">
      nextval
     </code>avançar a sequência antes de
        retornar um valor. O valor que será relatado por<code class="function">
      currval
     </code>também é definido para o valor especificado. Na forma de três parâmetros,<code class="literal">
      is_called
     </code>pode ser configurada para qualquer uma das opções<code class="literal">
      true
     </code>ou<code class="literal">
      false
     </code>
     .
     <code class="literal">
      true
     </code>tem o mesmo efeito que a forma de dois parâmetros. Se estiver definido como<code class="literal">
      false
     </code>, a próxima<code class="function">
      nextval
     </code>retornará exatamente o valor especificado, e o avanço da sequência começa com o seguinte<code class="function">
      nextval
     </code>Além disso, o valor relatado por<code class="function">
      currval
     </code>não é alterado neste caso. Por exemplo,</p>
<pre class="programlisting">
SELECT setval('myseq', 42);           <em class="lineannotation"><span class="lineannotation">Próximo<code class="function">nextval</code>retornará 43</span></em> SELECT setval('myseq', 42, true);     <em class="lineannotation"><span class="lineannotation">O mesmo que acima</span></em> SELECT setval('myseq', 42, false);    <em class="lineannotation"><span class="lineannotation">Próximo<code class="function">nextval</code>retornará 42</span></em>
</pre>
<p>O resultado retornado por<code class="function">
      setval
     </code>é apenas o valor do seu segundo argumento.</p>
<p>Esta função requer<code class="literal">
      UPDATE
     </code>privilégio na sequência.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      currval
     </code>(<code class="type">
      regclass
     </code>)<code class="returnvalue">
      bigint
     </code>
</p>
<p>Retorna o valor obtido mais recentemente por<code class="function">
      nextval
     </code>para esta sequência na sessão atual. (Um erro é relatado se<code class="function">
      nextval
     </code>nunca foi chamada para essa sequência nesta sessão.) Como isso está retornando um valor local da sessão, ele dá uma resposta previsível, independentemente de outras sessões terem executado ou<code class="function">
      nextval
     </code>como a sessão atual já fez.</p>
<p>Esta função requer<code class="literal">
      USAGE
     </code>ou<code class="literal">
      SELECT
     </code>privilégio na sequência.</p>
</td>
</tr>
<tr>
<td class="func_table_entry">
<p class="func_signature">
<code class="function">
      lastval
     </code>()<code class="returnvalue">
      bigint
     </code>
</p>
<p>Retorna o valor mais recentemente retornado por<code class="function">
      nextval
     </code>na sessão atual. Esta função é
        identicamente igual a<code class="function">
      currval
     </code>, exceto que, em vez de tomar o nome da sequência como argumento, ele se refere a qualquer sequência<code class="function">
      nextval
     </code>foi mais recentemente aplicado na sessão atual. É um erro chamar<code class="function">
      lastval
     </code>se<code class="function">
      nextval
     </code>não foi convocada ainda na sessão atual.</p>
<p>Esta função requer<code class="literal">
      USAGE
     </code>ou<code class="literal">
      SELECT
     </code>privilegio na última sequência usada.</p>
</td>
</tr>
</tbody>
</table>




  

### Atenção

Para evitar bloquear transações concorrentes que obtêm números da mesma sequência, o valor obtido por `nextval` não é recuperado para uso novamente se a transação solicitante for cancelada posteriormente. Isso significa que abortos de transações ou falhas no banco de dados podem resultar em lacunas na sequência de valores atribuídos. Isso também pode acontecer sem um aborto de transação. Por exemplo, um `INSERT` com uma cláusula `ON CONFLICT` calculará o tuplo a ser inserido, incluindo a realização de quaisquer chamadas necessárias `nextval`, antes de detectar qualquer conflito que o faça seguir a regra `ON CONFLICT` em vez disso. Assim, os objetos de sequência do PostgreSQL *não podem ser usados para obter sequências sem lacunas*.

Da mesma forma, as mudanças de estado de sequência feitas por `setval` são imediatamente visíveis para outras transações e não são desfeitas se a transação que as fez retornar.

Se o grupo de bancos de dados falhar antes de comprometer uma transação que contém uma chamada de `nextval` ou `setval`, a mudança do estado da sequência pode não ter sido armazenada no armazenamento persistente, de modo que é incerto se a sequência terá seu estado original ou atualizado após o restabelecimento do grupo. Isso é inócuo para o uso da sequência dentro do banco de dados, uma vez que outros efeitos das transações não comprometidas também não serão visíveis. No entanto, se você deseja usar um valor de sequência para fins persistentes fora do banco de dados, certifique-se de que a chamada de `nextval` tenha sido comprometida antes de fazer isso.

A sequência que será operada por uma função de sequência é especificada por um argumento `regclass`, que é simplesmente o OID da sequência no catálogo de sistema `pg_class`. No entanto, você não precisa procurar o OID manualmente, pois o conversor de entrada do tipo de dados `regclass` fará o trabalho por você. Veja [Seção 8.19][(datatype-oid.md "8.19. Object Identifier Types")] para detalhes.