## Crie a política

Crie a política — defina uma nova política de segurança de nível de linha para uma tabela

## Sinopse

```
CREATE POLICY name ON table_name
    [ AS { PERMISSIVE | RESTRICTIVE } ]
    [ FOR { ALL | SELECT | INSERT | UPDATE | DELETE } ]
    [ TO { role_name | PUBLIC | CURRENT_ROLE | CURRENT_USER | SESSION_USER } [, ...] ]
    [ USING ( using_expression ) ]
    [ WITH CHECK ( check_expression ) ]
```

## Descrição

O comando `CREATE POLICY` define uma nova política de segurança de nível de linha para uma tabela. Observe que a segurança de nível de linha deve ser habilitada na tabela (usando `ALTER TABLE ... ENABLE ROW LEVEL SECURITY`) para que as políticas criadas sejam aplicadas.

Uma política concede permissão para selecionar, inserir, atualizar ou excluir linhas que correspondem à expressão relevante da política. As linhas de tabela existentes são verificadas contra a expressão especificada em `USING`, enquanto as novas linhas que seriam criadas via `INSERT` ou `UPDATE` são verificadas contra a expressão especificada em `WITH CHECK`. Quando uma expressão de `USING` retorna verdadeira para uma linha específica, então essa linha é visível para o usuário, enquanto se false ou null for retornado, então a linha não é visível. Normalmente, não ocorre erro quando uma linha não é visível, mas veja [Tabela 300](sql-createpolicy.md#SQL-CREATEPOLICY-SUMMARY "Table 300. Policies Applied by Command Type") para exceções. Quando uma expressão de `WITH CHECK` retorna verdadeira para uma linha, então essa linha é inserida ou atualizada, enquanto se false ou null for retornado, então ocorre um erro.

Para as declarações `INSERT`, `UPDATE` e `MERGE`, as expressões `WITH CHECK` são aplicadas após os gatilhos `BEFORE` serem acionados e antes de quaisquer modificações de dados reais serem feitas. Assim, um gatilho `BEFORE ROW` pode modificar os dados a serem inseridos, afetando o resultado da verificação da política de segurança. As expressões `WITH CHECK` são aplicadas antes de quaisquer outras restrições.

Os nomes de políticas são por tabela. Portanto, um nome de política pode ser usado para muitas tabelas diferentes e ter uma definição para cada tabela que seja apropriada para essa tabela.

As políticas podem ser aplicadas para comandos específicos ou para papéis específicos. O padrão para políticas recém-criadas é que elas se apliquem a todos os comandos e papéis, a menos que especificado de outra forma. Múltiplas políticas podem ser aplicadas a um único comando; consulte abaixo para mais detalhes. [Tabela 300][(sql-createpolicy.md#SQL-CREATEPOLICY-SUMMARY "Table 300. Policies Applied by Command Type")] resume como os diferentes tipos de política se aplicam a comandos específicos.

Para políticas que podem ter tanto expressões `USING` quanto `WITH CHECK` (`ALL` e `UPDATE`), se nenhuma expressão `WITH CHECK` for definida, então a expressão `USING` será usada tanto para determinar quais linhas são visíveis (caso normal `USING`) quanto para determinar quais novas linhas serão permitidas para serem adicionadas (caso `WITH CHECK`).

Se a segurança de nível de linha estiver habilitada para uma tabela, mas não houver políticas aplicáveis, uma política de “rejeitar padrão” é assumida, de modo que nenhuma linha será visível ou atualizável.

## Parâmetros

*`name`*: O nome da política a ser criada. Isso deve ser distinto do nome de qualquer outra política para a tabela.

*`table_name`*: O nome (opcionalmente qualificado por esquema) da tabela à qual a política se aplica.

`PERMISSIVE`: Especifique que a política deve ser criada como uma política permissiva. Todas as políticas permissivas que são aplicáveis a uma consulta específica serão combinadas usando o operador booleano “OU”. Ao criar políticas permissivas, os administradores podem adicionar ao conjunto de registros que podem ser acessados. As políticas são permissivas por padrão.

`RESTRICTIVE`: Especifique que a política deve ser criada como uma política restritiva. Todas as políticas restritivas que são aplicáveis a uma consulta específica serão combinadas usando o operador booleano “E”. Ao criar políticas restritivas, os administradores podem reduzir o conjunto de registros que podem ser acessados, pois todas as políticas restritivas devem ser passadas para cada registro.

Observe que é necessário haver pelo menos uma política permissiva para conceder acesso aos registros antes que políticas restritivas possam ser usadas de forma útil para reduzir esse acesso. Se apenas políticas restritivas existirem, então nenhum registro será acessível. Quando uma mistura de políticas permissivas e restritivas está presente, um registro só é acessível se pelo menos uma das políticas permissivas passar, além de todas as políticas restritivas.

*`command`*: O comando ao qual a política se aplica. As opções válidas são `ALL`, `SELECT`, `INSERT`, `UPDATE` e `DELETE`. `ALL` é o padrão. Veja abaixo para detalhes sobre como esses são aplicados.

*`role_name`*: O(s) papel(es) ao qual a política deve ser aplicada. O padrão é `PUBLIC`, que aplicará a política a todos os papéis.

*`using_expression`*: Qualquer expressão condicional SQL (retornando `boolean`). A expressão condicional não pode conter nenhuma função agregada ou de janela. Essa expressão será adicionada às consultas que fazem referência à tabela se a segurança de nível de linha estiver habilitada. As linhas para as quais a expressão retorna verdadeiro serão visíveis. Quaisquer linhas para as quais a expressão retorna falso ou nulo não serão visíveis para o usuário (em um `SELECT`), e não estarão disponíveis para modificação (em um `UPDATE` ou `DELETE`). Tipicamente, essas linhas são suprimidas silenciosamente; nenhum erro é relatado (mas veja [Tabela 300](sql-createpolicy.md#SQL-CREATEPOLICY-SUMMARY "Table 300. Policies Applied by Command Type") para exceções).

*`check_expression`*: Qualquer expressão condicional SQL (retornando `boolean`). A expressão condicional não pode conter nenhuma função agregada ou de janela. Esta expressão será usada em consultas de `INSERT` e `UPDATE` contra a tabela se a segurança de nível de linha estiver habilitada. Apenas as linhas para as quais a expressão avalia como verdadeira serão permitidas. Será lançada uma exceção se a expressão avaliar como falsa ou nulo para qualquer um dos registros inseridos ou para qualquer um dos registros que resultam da atualização. Note que o *`check_expression`* é avaliado contra os novos conteúdos propostos da linha, não os conteúdos originais.

### Políticas por comando

`ALL` [#](#SQL-CREATEPOLICY-ALL): Utilizar `ALL` para uma política significa que ela se aplicará a todos os comandos, independentemente do tipo de comando. Se existir uma política `ALL` e existir políticas mais específicas, então tanto a política `ALL` quanto a política mais específica (ou políticas) serão aplicadas. Além disso, as políticas `ALL` serão aplicadas tanto ao lado de seleção de uma consulta quanto ao lado de modificação, usando a expressão `USING` para ambos os casos, se apenas uma expressão `USING` tiver sido definida.

Como exemplo, se um `UPDATE` for emitido, então a política `ALL` será aplicável tanto ao que o `UPDATE` poderá selecionar como linhas a serem atualizadas (aplicando a expressão `USING`), quanto às linhas atualizadas resultantes, para verificar se elas são permitidas para serem adicionadas à tabela (aplicando a expressão `WITH CHECK`, se definida, e a expressão `USING`, caso contrário). Se um comando `INSERT` ou `UPDATE` tentar adicionar linhas à tabela que não passam pela expressão `ALL` da política `WITH CHECK` (ou sua expressão `USING`, se não tiver uma expressão `WITH CHECK`), o comando inteiro será abortado.

`SELECT` [#](#SQL-CREATEPOLICY-SELECT): O uso de `SELECT` para uma política significa que ela se aplicará a consultas de `SELECT` e sempre que permissões de `SELECT` sejam necessárias na relação para a qual a política é definida. O resultado é que apenas os registros da relação que passam pela política de `SELECT` serão retornados durante uma consulta de `SELECT`, e que as consultas que exigem permissões de `SELECT`, como `UPDATE`, `DELETE` e `MERGE`, também verão apenas aqueles registros que são permitidos pela política de `SELECT`. Uma política de `SELECT` não pode ter uma expressão de `WITH CHECK`, pois ela se aplica apenas nos casos em que registros estão sendo recuperados da relação, exceto conforme descrito abaixo.

Se uma consulta que modifica dados tiver uma cláusula `RETURNING`, são necessárias permissões `SELECT` na relação, e quaisquer linhas recém-inseridas ou atualizadas da relação devem satisfazer as políticas `SELECT` da relação para serem disponibilizadas à cláusula `RETURNING`. Se uma linha recém-inserida ou atualizada não satisfazer as políticas `SELECT` da relação, um erro será lançado (as linhas inseridas ou atualizadas a serem devolvidas *nunca* são ignoradas silenciosamente).

Se um `INSERT` tiver uma cláusula `ON CONFLICT DO UPDATE`, ou uma cláusula `ON CONFLICT DO NOTHING` com uma especificação de índice ou restrição arbítrizável, então as permissões `SELECT` são necessárias na relação, e as linhas propostas para inserção são verificadas usando as políticas `SELECT` da relação. Se uma linha proposta para inserção não satisfazer as políticas `SELECT` da relação, um erro é lançado (o `INSERT` é *nunca* evitado silenciosamente). Além disso, se o caminho `UPDATE` for seguido, a linha a ser atualizada e a nova linha atualizada são verificadas contra as políticas `SELECT` da relação, e um erro é lançado se não forem satisfeitas (um `UPDATE` auxiliar *nunca* é evitado silenciosamente).

Um comando `MERGE` requer permissões `SELECT` tanto nas relações de origem quanto de destino, portanto, as políticas `SELECT` de cada relação são aplicadas antes de serem unidas, e as ações `MERGE` verão apenas os registros permitidos por essas políticas. Além disso, se uma ação `UPDATE` for executada, as políticas `SELECT` da relação de destino são aplicadas à linha atualizada, assim como em um `UPDATE` autônomo, exceto que um erro é lançado se elas não forem satisfeitas.

`INSERT` [#](#SQL-CREATEPOLICY-INSERT): Usar `INSERT` para uma política significa que ela se aplicará a comandos `INSERT` e comandos `MERGE` que contenham ações `INSERT`. As linhas que forem inseridas e não passarem por essa política resultará em um erro de violação de política, e todo o comando `INSERT` será abortado. Uma política `INSERT` não pode ter uma expressão `USING`, pois ela só se aplica em casos em que registros estão sendo adicionados à relação.

Observe que um `INSERT` com uma cláusula `ON CONFLICT DO NOTHING/UPDATE` verificará as expressões de `INSERT` das políticas para todas as linhas propostas para inserção, independentemente de elas serem ou não inseridas.

`UPDATE` [#](#SQL-CREATEPOLICY-UPDATE): Usar `UPDATE` para uma política significa que ela se aplicará aos comandos `UPDATE`, `SELECT FOR UPDATE` e `SELECT FOR SHARE`, bem como às cláusulas auxiliares `ON CONFLICT DO UPDATE` dos comandos `INSERT`, e comandos `MERGE` que contenham ações `UPDATE`. Como um comando `UPDATE` envolve a extração de um registro existente e a substituição por um novo registro modificado, as políticas `UPDATE` aceitam tanto uma expressão `USING` quanto uma expressão `WITH CHECK`. A expressão `USING` determina quais registros o comando `UPDATE` verá para operar, enquanto a expressão `WITH CHECK` define quais linhas modificadas são permitidas para serem armazenadas de volta na relação.

Quaisquer linhas cujos valores atualizados não passam pela expressão `WITH CHECK` causarão um erro, e o comando inteiro será abortado. Se apenas uma cláusula `USING` for especificada, então essa cláusula será usada para os casos de `USING` e `WITH CHECK`.

Tipicamente, um comando `UPDATE` também precisa ler dados de colunas na relação que está sendo atualizada (por exemplo, em uma cláusula `WHERE` ou em uma cláusula `RETURNING`, ou em uma expressão no lado direito da cláusula `SET`). Neste caso, os direitos `SELECT` também são necessários na relação que está sendo atualizada, e as políticas apropriadas `SELECT` ou `ALL` serão aplicadas além das políticas `UPDATE`. Assim, o usuário deve ter acesso às(s) linha(s) que está(m) sendo atualizada através de uma política `SELECT` ou `ALL`, além de ter permissão para atualizar a(s) linha(s) através de uma política `UPDATE` ou `ALL`.

Quando um comando `INSERT` tem uma cláusula auxiliar `ON CONFLICT DO UPDATE`, se o caminho `UPDATE` for seguido, a linha a ser atualizada é verificada primeiro contra as expressões `USING` de quaisquer políticas `UPDATE`, e então a nova linha atualizada é verificada contra as expressões `WITH CHECK`. No entanto, note que, ao contrário de um comando `UPDATE` autônomo, se a linha existente não passar pelas expressões `USING`, um erro será lançado (o caminho `UPDATE` *nunca* será ignorado silenciosamente). O mesmo se aplica a uma ação `UPDATE` de um comando `MERGE`.

`DELETE` [#](#SQL-CREATEPOLICY-DELETE): Usar `DELETE` para uma política significa que ela se aplicará a comandos `DELETE` e comandos `MERGE` que contenham ações `DELETE`. Para um comando `DELETE`, apenas as linhas que passam por essa política serão vistas pelo comando `DELETE`. Pode haver linhas que são visíveis por meio de uma política `SELECT`, mas não estão disponíveis para exclusão, se não passarem pela expressão `USING` para a política `DELETE`. No entanto, observe que uma ação `DELETE` em um comando `MERGE` verá linhas que são visíveis por meio de políticas `SELECT`, e se a política `DELETE` não passar para tal linha, um erro será lançado.

Na maioria dos casos, um comando `DELETE` também precisa ler dados de colunas na relação da qual está excluindo (por exemplo, em uma cláusula `WHERE` ou uma cláusula `RETURNING`). Nesse caso, os direitos `SELECT` também são necessários na relação, e as políticas apropriadas `SELECT` ou `ALL` serão aplicadas além das políticas `DELETE`. Assim, o usuário deve ter acesso às(s) linha(s) sendo excluída(s) através de uma política `SELECT` ou `ALL`, além de ter permissão para excluir as(s) linha(s) via uma política `DELETE` ou `ALL`.

Uma política `DELETE` não pode ter uma expressão `WITH CHECK`, pois ela só se aplica em casos em que os registros estão sendo excluídos da relação, de modo que não há uma nova linha a ser verificada.

[Tabela 300][(sql-createpolicy.md#SQL-CREATEPOLICY-SUMMARY "Table 300. Policies Applied by Command Type")] resume como os diferentes tipos de política se aplicam a comandos específicos. Na tabela, “check” significa que a expressão de política é verificada e um erro é lançado se ela retornar falso ou nulo, enquanto “filter” significa que a linha é ignorada silenciosamente se a expressão de política retornar falso ou nulo.

**Tabela 300. Políticas Aplicadas por Tipo de Comando**



<table border="1" class="table" summary="Policies Applied by Command Type">
<colgroup>
<col/>
<col/>
<col/>
<col class="update-using"/>
<col class="update-check"/>
<col/>
</colgroup>
<thead>
<tr>
<th rowspan="2">Comando</th>
<th>
<code class="literal">
     SELECT/ALL policy
    </code>
</th>
<th>
<code class="literal">
     INSERT/ALL policy
    </code>
</th>
<th colspan="2">
<code class="literal">
     UPDATE/ALL policy
    </code>
</th>
<th>
<code class="literal">
     DELETE/ALL policy
    </code>
</th>
</tr>
<tr>
<th>
<code class="literal">
     USING expression
    </code>
</th>
<th>
<code class="literal">
     WITH CHECK expression
    </code>
</th>
<th>
<code class="literal">
     USING expression
    </code>
</th>
<th>
<code class="literal">
     WITH CHECK expression
    </code>
</th>
<th>
<code class="literal">
     USING expression
    </code>
</th>
</tr>
</thead>
<tbody>
<tr>
<td>
<code class="command">
     SELECT
    </code>/<code class="command">
     COPY ... TO
    </code>
</td>
<td>Filtrar linha existente</td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     SELECT FOR UPDATE/SHARE
    </code>
</td>
<td>Filtrar linha existente</td>
<td>
    —
   </td>
<td>
    Filter existing row
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     INSERT
    </code>
</td>
<td>Ver nova linha<a class="footnote" href="#ftn.RLS-SELECT-PRIV">
<sup class="footnote" id="RLS-SELECT-PRIV">[a]</sup>
</a>
</td>
<td>
    Check new row
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     UPDATE
    </code>
</td>
<td>Filtrar linha existente<a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-SELECT-PRIV">
<sup class="footnoteref">[a]</sup>
</a>&amp; verificar nova linha<a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-SELECT-PRIV">
<sup class="footnoteref">[a]</sup>
</a>
</td>
<td>
    —
   </td>
<td>
    Filter existing row
   </td>
<td>
    Check new row
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     DELETE
    </code>
</td>
<td>Filtrar linha existente<a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-SELECT-PRIV">
<sup class="footnoteref">[a]</sup>
</a>
</td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    Filter existing row
   </td>
</tr>
<tr>
<td>
<code class="command">
     INSERT ... ON CONFLICT
    </code>
</td>
<td>Ver nova linha<a class="footnote" href="#ftn.id-1.9.3.75.6.3.4.2.5.6.2.1">
<sup class="footnote" id="id-1.9.3.75.6.3.4.2.5.6.2.1">[b]</sup>
</a>
<a class="footnote" href="#ftn.RLS-ON-CONFLICT-PRIV">
<sup class="footnote" id="RLS-ON-CONFLICT-PRIV">[c]</sup>
</a>
</td>
<td>
    Check new row
    <a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-ON-CONFLICT-PRIV">
<sup class="footnoteref">
      [c]
     </sup>
</a>
</td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     ON CONFLICT DO UPDATE
    </code>
</td>
<td>Verifique as linhas existentes e novas<a class="footnote" href="#ftn.RLS-ON-CONFLICT-UPDATE-PRIV">
<sup class="footnote" id="RLS-ON-CONFLICT-UPDATE-PRIV">[d]</sup>
</a>
</td>
<td>
    —
   </td>
<td>
    Check existing row
   </td>
<td>
    Check new row
    <a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-ON-CONFLICT-UPDATE-PRIV">
<sup class="footnoteref">
      [d]
     </sup>
</a>
</td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     MERGE
    </code>
</td>
<td>Filtrar linhas de origem e destino</td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     MERGE ... THEN INSERT
    </code>
</td>
<td>Ver nova linha<a class="footnoteref" href="sql-createpolicy.md#ftn.RLS-SELECT-PRIV">
<sup class="footnoteref">[a]</sup>
</a>
</td>
<td>
    Check new row
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     MERGE ... THEN UPDATE
    </code>
</td>
<td>Ver nova linha</td>
<td>
    —
   </td>
<td>
    Check existing row
   </td>
<td>
    Check new row
   </td>
<td>
    —
   </td>
</tr>
<tr>
<td>
<code class="command">
     MERGE ... THEN DELETE
    </code>
</td>
<td>—</td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    —
   </td>
<td>
    Check existing row
   </td>
</tr>
</tbody>
<tbody class="footnotes">
<tr>
<td colspan="6">
<div class="footnote" id="ftn.RLS-SELECT-PRIV">
<p>
<a class="para" href="#RLS-SELECT-PRIV">
<sup class="para">[a]</sup>
</a>Se for necessário acesso de leitura para a linha existente ou nova (por exemplo, uma<code class="literal">
       WHERE
      </code>ou<code class="literal">
       RETURNING
      </code>cláusula que se refere a colunas da relação).</p>
</div>
<div class="footnote" id="ftn.id-1.9.3.75.6.3.4.2.5.6.2.1">
<p>
<a class="para" href="#id-1.9.3.75.6.3.4.2.5.6.2.1">
<sup class="para">[b]</sup>
</a>Se um índice ou restrição de árbitro for especificado.</p>
</div>
<div class="footnote" id="ftn.RLS-ON-CONFLICT-PRIV">
<p>
<a class="para" href="#RLS-ON-CONFLICT-PRIV">
<sup class="para">[c]</sup>
</a>A linha proposta para inserção é verificada, independentemente de ocorrer ou não um conflito.</p>
</div>
<div class="footnote" id="ftn.RLS-ON-CONFLICT-UPDATE-PRIV">
<p>
<a class="para" href="#RLS-ON-CONFLICT-UPDATE-PRIV">
<sup class="para">[d]</sup>
</a>Nova linha do auxiliar<code class="command">
       UPDATE
      </code>comando, que pode ser diferente da nova linha do original<code class="command">
       INSERT
      </code>
      command.
     </p>
</div>
</td>
</tr>
</tbody>
</table>



### Aplicação de Políticas Múltiplas

Quando várias políticas de diferentes tipos de comando se aplicam ao mesmo comando (por exemplo, as políticas `SELECT` e `UPDATE` aplicadas a um comando `UPDATE`, o usuário deve ter ambos os tipos de permissão (por exemplo, permissão para selecionar linhas da relação, bem como permissão para atualizá-las). Assim, as expressões para um tipo de política são combinadas com as expressões para o outro tipo de política usando o operador `AND`.

Quando várias políticas do mesmo tipo de comando se aplicam ao mesmo comando, então deve haver pelo menos uma política `PERMISSIVE` que conceda acesso à relação, e todas as políticas `RESTRICTIVE` devem ser aprovadas. Assim, todas as expressões de políticas `PERMISSIVE` são combinadas usando `OR`, todas as expressões de políticas `RESTRICTIVE` são combinadas usando `AND`, e os resultados são combinados usando `AND`. Se não houver políticas `PERMISSIVE`, então o acesso é negado.

Observe que, para fins de combinação de várias políticas, as políticas `ALL` são tratadas como tendo o mesmo tipo que qualquer outro tipo de política que esteja sendo aplicada.

Por exemplo, em um comando `UPDATE` que exige as permissões `SELECT` e `UPDATE`, se houver várias políticas aplicáveis de cada tipo, elas serão combinadas da seguinte forma:

```
expression from RESTRICTIVE SELECT/ALL policy 1
AND
expression from RESTRICTIVE SELECT/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE SELECT/ALL policy 1
  OR
  expression from PERMISSIVE SELECT/ALL policy 2
  OR
  ...
)
AND
expression from RESTRICTIVE UPDATE/ALL policy 1
AND
expression from RESTRICTIVE UPDATE/ALL policy 2
AND
...
AND
(
  expression from PERMISSIVE UPDATE/ALL policy 1
  OR
  expression from PERMISSIVE UPDATE/ALL policy 2
  OR
  ...
)
```

## Notas

Você deve ser o proprietário de uma tabela para criar ou alterar políticas para ela.

Embora as políticas sejam aplicadas para consultas explícitas contra tabelas no banco de dados, elas não são aplicadas quando o sistema está realizando verificações internas de integridade referencial ou validando restrições. Isso significa que existem maneiras indiretas de determinar que um valor dado existe. Um exemplo disso é tentar inserir um valor duplicado em uma coluna que é uma chave primária ou tem uma restrição única. Se a inserção falhar, o usuário pode inferir que o valor já existe. (Este exemplo assume que o usuário é autorizado pela política a inserir registros que não é permitido ver.) Outro exemplo é quando um usuário é autorizado a inserir em uma tabela que faz referência a outra, de outra forma, tabela oculta. A existência pode ser determinada pelo usuário inserindo valores na tabela de referência, onde o sucesso indicaria que o valor existe na tabela referenciada. Esses problemas podem ser abordados elaborando cuidadosamente as políticas para impedir que os usuários possam inserir, excluir ou atualizar registros, o que poderia possivelmente indicar um valor que eles não são capazes de ver, ou usando valores gerados (por exemplo, chaves surogadas) em vez de chaves com significados externos.

Geralmente, o sistema aplicará as condições de filtro impostas por meio de políticas de segurança antes das qualificações que aparecem nas consultas dos usuários, a fim de evitar a exposição acidental dos dados protegidos a funções definidas pelo usuário que podem não ser confiáveis. No entanto, as funções e operadores marcados pelo sistema (ou pelo administrador do sistema) como `LEAKPROOF` podem ser avaliados antes das expressões de políticas, pois são assumidos como confiáveis.

Como as expressões de política são adicionadas diretamente à consulta do usuário, elas serão executadas com os direitos do usuário que está executando a consulta geral. Portanto, os usuários que estão usando uma política específica devem ser capazes de acessar quaisquer tabelas ou funções referenciadas na expressão, ou eles simplesmente receberão um erro de permissão negada ao tentar consultar a tabela que tem segurança de nível de linha habilitada. Isso, no entanto, não altera como as visualizações funcionam. Assim como em consultas e visualizações normais, as verificações de permissão e as políticas para as tabelas que são referenciadas por uma visualização usarão os direitos do proprietário da visualização e quaisquer políticas que se apliquem ao proprietário da visualização, exceto se a visualização for definida usando a opção `security_invoker` (consulte `CREATE VIEW` (sql-createview.md "CREATE VIEW")).

Não existe uma política separada para `MERGE`. Em vez disso, as políticas definidas para `SELECT`, `INSERT`, `UPDATE` e `DELETE` são aplicadas durante a execução de `MERGE`, dependendo das ações que são realizadas.

Discussões adicionais e exemplos práticos podem ser encontrados em [Seção 5.9][(ddl-rowsecurity.md "5.9. Row Security Policies")].

## Compatibilidade

`CREATE POLICY` é uma extensão do PostgreSQL.

## Veja também

[ALTERAR POLÍTICA](sql-alterpolicy.md "ALTER POLICY"), [DROP POLÍTICA](sql-droppolicy.md "DROP POLICY"), [ALTERAR TABELA](sql-altertable.md "ALTER TABLE")