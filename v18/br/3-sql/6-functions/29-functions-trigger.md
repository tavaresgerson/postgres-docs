### 9.29. Funções de disparo [#](#FUNCTIONS-TRIGGER)

Embora muitos usos de gatilhos envolvam funções de gatilho escritas pelo usuário, o PostgreSQL fornece algumas funções de gatilho pré-definidas que podem ser usadas diretamente em gatilhos definidos pelo usuário. Essas são resumidas em [Tabela 9.110](functions-trigger.md#BUILTIN-TRIGGERS-TABLE). (Existem outras funções de gatilho pré-definidas, que implementam restrições de chave estrangeira e restrições de índice diferido. Essas não são documentadas aqui, pois os usuários não precisam usá-las diretamente.)

Para mais informações sobre como criar gatilhos, consulte [CREATE TRIGGER](sql-createtrigger.md "CREATE TRIGGER").

**Tabela 9.110. Funções de gatilho integradas**

<table>
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
     Example Usage
    </p>
   </th>
  </tr>
 </thead>
 <tbody>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      suppress_redundant_updates_trigger
     </code>
     ( ) →
     <code>
      trigger
     </code>
    </p>
    <p>
     Suppresses do-nothing update operations.  See below for details.
    </p>
    <p>
     <code>
      CREATE TRIGGER ... suppress_redundant_updates_trigger()
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsvector_update_trigger
     </code>
     ( ) →
     <code>
      trigger
     </code>
    </p>
    <p>
     Automatically updates a
     <code>
      tsvector
     </code>
     column from associated plain-text document column(s).  The text search configuration to use is specified by name as a trigger argument.  See
     <a class="xref" href="textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS" title="12.4.3. Triggers for Automatic Updates">
      Section 12.4.3
     </a>
     for details.
    </p>
    <p>
     <code>
      CREATE TRIGGER ... tsvector_update_trigger(tsvcol, 'pg_catalog.swedish', title, body)
     </code>
    </p>
   </td>
  </tr>
  <tr>
   <td class="func_table_entry">
    <p class="func_signature">
     <code>
      tsvector_update_trigger_column
     </code>
     ( ) →
     <code>
      trigger
     </code>
    </p>
    <p>
     Automatically updates a
     <code>
      tsvector
     </code>
     column from associated plain-text document column(s).  The text search configuration to use is taken from a
     <code>
      regconfig
     </code>
     column of the table.  See
     <a class="xref" href="textsearch-features.md#TEXTSEARCH-UPDATE-TRIGGERS" title="12.4.3. Triggers for Automatic Updates">
      Section 12.4.3
     </a>
     for details.
    </p>
    <p>
     <code>
      CREATE TRIGGER ... tsvector_update_trigger_column(tsvcol, tsconfigcol, title, body)
     </code>
    </p>
   </td>
  </tr>
 </tbody>
</table>

A função `suppress_redundant_updates_trigger`, quando aplicada como um gatilho de nível de linha `BEFORE UPDATE`, impedirá que qualquer atualização que não mude efetivamente os dados da linha ocorra. Isso substitui o comportamento normal, que sempre realiza uma atualização física da linha, independentemente de os dados terem sido alterados ou não. (Esse comportamento normal faz com que as atualizações sejam executadas mais rapidamente, uma vez que não é necessária nenhuma verificação, e também é útil em certos casos.)

Idealmente, você deve evitar executar atualizações que não alteram realmente os dados no registro. As atualizações redundantes podem custar um tempo considerável e desnecessário, especialmente se houver muitos índices a serem alterados e espaço em linhas mortas que, eventualmente, terão que ser varridos. No entanto, detectar tais situações no código do cliente nem sempre é fácil, ou até mesmo possível, e escrever expressões para detectá-las pode ser propenso a erros. Uma alternativa é usar `suppress_redundant_updates_trigger`, que ignorará as atualizações que não alteram os dados. No entanto, você deve usar isso com cuidado. O gatilho leva um tempo pequeno, mas não trivial, para cada registro, então, se a maioria dos registros afetados pelas atualizações realmente mudar, o uso deste gatilho fará com que as atualizações sejam executadas mais lentamente em média.

A função `suppress_redundant_updates_trigger` pode ser adicionada a uma tabela assim:

```sql
CREATE TRIGGER z_min_update
BEFORE UPDATE ON tablename
FOR EACH ROW EXECUTE FUNCTION suppress_redundant_updates_trigger();
```

Na maioria dos casos, você precisa disparar este gatilho por último para cada linha, para que ele não sobrecarregue outros gatilhos que possam querer alterar a linha. Tendo em mente que os gatilhos são disparados em ordem de nome, você escolheria, portanto, um nome de gatilho que vem após o nome de qualquer outro gatilho que você possa ter na tabela. (Daí o prefixo “z” no exemplo.)