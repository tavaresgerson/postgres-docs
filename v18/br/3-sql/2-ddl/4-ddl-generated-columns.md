## 5.4. Colunas Geradas [#](#DDL-GENERATED-COLUMNS)

Uma coluna gerada é uma coluna especial que é sempre calculada a partir de outras colunas. Assim, é o que uma visão é para tabelas. Existem dois tipos de colunas geradas: armazenadas e virtuais. Uma coluna gerada armazenada é calculada quando é escrita (inserida ou atualizada) e ocupa armazenamento como se fosse uma coluna normal. Uma coluna gerada virtual não ocupa armazenamento e é calculada quando é lida. Assim, uma coluna gerada virtual é semelhante a uma visão e uma coluna gerada armazenada é semelhante a uma visão materializada (exceto que é sempre atualizada automaticamente).

Para criar uma coluna gerada, use a cláusula `GENERATED ALWAYS AS` em `CREATE TABLE`, por exemplo:

```
CREATE TABLE people (
    ...,
    height_cm numeric,
    height_in numeric GENERATED ALWAYS AS (height_cm / 2.54)
);
```

Uma coluna gerada é, por padrão, do tipo virtual. Use as palavras-chave `VIRTUAL` ou `STORED` para tornar a escolha explícita. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para obter mais detalhes.

Uma coluna gerada não pode ser escrita diretamente. Nos comandos `INSERT` ou `UPDATE`, não é possível especificar um valor para uma coluna gerada, mas o termo-chave `DEFAULT` pode ser especificado.

Considere as diferenças entre uma coluna com um valor padrão e uma coluna gerada. O valor padrão da coluna é avaliado uma vez quando a linha é inserida pela primeira vez, se nenhum outro valor for fornecido; uma coluna gerada é atualizada sempre que a linha muda e não pode ser sobrescrita. Um valor padrão de coluna não pode se referir a outras colunas da tabela; uma expressão de geração normalmente o faz. Um valor padrão de coluna pode usar funções voláteis, por exemplo, `random()` ou funções que se referem ao horário atual; isso não é permitido para colunas geradas.

Várias restrições se aplicam à definição de colunas e tabelas geradas que envolvem colunas geradas:

* A expressão de geração só pode usar funções imutáveis e não pode usar subconsultas ou referenciar qualquer coisa que não seja a linha atual de qualquer maneira.
* A expressão de geração não pode referenciar outra coluna gerada.
* A expressão de geração não pode referenciar uma coluna do sistema, exceto `tableoid`.
* Uma coluna gerada virtual não pode ter um tipo definido pelo usuário e a expressão de geração de uma coluna gerada virtual não deve referenciar funções ou tipos definidos pelo usuário, ou seja, só pode usar funções ou tipos embutidos. Isso também se aplica indiretamente, como para funções ou tipos que subjazem a operadores ou casts. (Essa restrição não existe para colunas geradas armazenadas.)
* Uma coluna gerada não pode ter um padrão de coluna ou uma definição de identidade.
* Uma coluna gerada não pode fazer parte de uma chave de partição.
* Tabelas estrangeiras podem ter colunas geradas. Veja [CREATE FOREIGN TABLE](sql-createforeigntable.md) para detalhes.
* Para herança e particionamento:

+ Se uma coluna pai for uma coluna gerada, sua coluna filho também deve ser uma coluna gerada do mesmo tipo (armazenada ou virtual); no entanto, a coluna filho pode ter uma expressão de geração diferente.

Para colunas geradas armazenadas, a expressão de geração que é realmente aplicada durante a inserção ou atualização de uma linha é a associada à tabela na qual a linha está fisicamente. (Isso é diferente do comportamento para os padrões de coluna: para esses, o valor padrão associado à tabela mencionada na consulta se aplica.) Para colunas geradas virtuais, a expressão de geração da tabela mencionada na consulta se aplica quando uma tabela é lida.
+ Se uma coluna pai não for uma coluna gerada, sua coluna filho também não deve ser gerada.
+ Para tabelas herdadas, se você escrever uma definição de coluna filho sem qualquer cláusula `GENERATED` em `CREATE TABLE ... INHERITS`, então sua cláusula `GENERATED` será automaticamente copiada do pai. `ALTER TABLE ... INHERIT` insistirá que as colunas pai e filho já correspondam quanto ao status de geração, mas não exigirá que suas expressões de geração correspondam.
+ Da mesma forma para tabelas particionadas, se você escrever uma definição de coluna filho sem qualquer cláusula `GENERATED` em `CREATE TABLE ... PARTITION OF`, então sua cláusula `GENERATED` será automaticamente copiada do pai. `ALTER TABLE ... ATTACH PARTITION` insistirá que as colunas pai e filho já correspondam quanto ao status de geração, mas não exigirá que suas expressões de geração correspondam.
+ Em caso de múltiplos herdeiros, se uma coluna pai for uma coluna gerada, então todas as colunas pai devem ser colunas geradas. Se elas não tiverem todas a mesma expressão de geração, então a expressão desejada para a criança deve ser especificada explicitamente.

Considerações adicionais se aplicam ao uso de colunas geradas.

* As colunas geradas mantêm privilégios de acesso separadamente de suas colunas de base subjacentes. Portanto, é possível configurá-las de modo que um determinado papel possa ler de uma coluna gerada, mas não das colunas de base subjacentes.

Para colunas geradas virtualmente, isso é totalmente seguro apenas se a expressão de geração usar apenas funções à prova de vazamento (consulte [CREATE FUNCTION](sql-createfunction.md)), mas isso não é exigido pelo sistema.
* Os privilégios das funções usadas nas expressões de geração são verificados quando a expressão é executada, na escrita ou leitura, respectivamente, como se a expressão de geração tivesse sido chamada diretamente da consulta usando a coluna gerada. O usuário de uma coluna gerada deve ter permissões para chamar todas as funções usadas pela expressão de geração. As funções na expressão de geração são executadas com os privilégios do usuário que executa a consulta ou do proprietário da função, dependendo se as funções são definidas como `SECURITY INVOKER` ou `SECURITY DEFINER`.
* As colunas geradas são, conceitualmente, atualizadas após os gatilhos `BEFORE` terem sido executados. Portanto, as alterações feitas nas colunas base em um gatilho `BEFORE` serão refletidas nas colunas geradas. Mas, reciprocamente, não é permitido acessar colunas geradas em gatilhos `BEFORE`.
* As colunas geradas podem ser replicadas durante a replicação lógica de acordo com o parâmetro `CREATE PUBLICATION` [`publish_generated_columns`](sql-createpublication.md#SQL-CREATEPUBLICATION-PARAMS-WITH-PUBLISH-GENERATED-COLUMNS) ou incluindo-as na lista de colunas do comando `CREATE PUBLICATION`. Isso atualmente é suportado apenas para colunas geradas armazenadas. Consulte [Seção 29.6](logical-replication-gencols.md) para detalhes.