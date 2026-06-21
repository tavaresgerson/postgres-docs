## 29.1. Publicação [#](#LOGICAL-REPLICATION-PUBLICATION)

* [29.1.1. Identidade Replicável](logical-replication-publication.md#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

Uma *publicação* pode ser definida em qualquer replicação primária física. O nó onde uma publicação é definida é referido como *editor*. Uma publicação é um conjunto de alterações geradas a partir de uma tabela ou um grupo de tabelas, e também pode ser descrita como um conjunto de alterações ou conjunto de replicação. Cada publicação existe em apenas um banco de dados.

As publicações são diferentes dos esquemas e não afetam a forma como a tabela é acessada. Cada tabela pode ser adicionada a várias publicações, se necessário. As publicações podem atualmente conter apenas tabelas e todas as tabelas do esquema. Os objetos devem ser adicionados explicitamente, exceto quando uma publicação é criada para `ALL TABLES`.

As publicações podem optar por limitar as alterações que produzem a qualquer combinação de `INSERT`, `UPDATE`, `DELETE` e `TRUNCATE`, de forma semelhante à maneira como os gatilhos são disparados por tipos de eventos específicos. Por padrão, todos os tipos de operação são replicados. Essas especificações de publicação aplicam-se apenas para operações DML; elas não afetam a cópia inicial de sincronização de dados. (Os filtros de linha não têm efeito para `TRUNCATE`. Veja [Seção 29.4][(logical-replication-row-filter.md "29.4. Row Filters")]).

Cada publicação pode ter vários assinantes.

Uma publicação é criada usando o comando `CREATE PUBLICATION`(sql-createpublication.md "CREATE PUBLICATION") e pode ser alterada ou removida posteriormente usando comandos correspondentes.

As tabelas individuais podem ser adicionadas e removidas dinamicamente usando `ALTER PUBLICATION` e (sql-alterpublication.md "ALTER PUBLICATION"). As operações `ADD TABLE` e `DROP TABLE` são transacionais, portanto, a tabela começará ou parará a replicação no momento correto do instantâneo assim que a transação tiver sido confirmada.

### 29.1.1. Identidade Replicável [#](#LOGICAL-REPLICATION-PUBLICATION-REPLICA-IDENTITY)

Uma tabela publicada deve ter uma *identidade de replicação* configurada para poder replicar as operações `UPDATE` e `DELETE`, de modo que as linhas apropriadas para atualização ou exclusão possam ser identificadas no lado do assinante.

Por padrão, esta é a chave primária, se houver uma. Outro índice único (com certos requisitos adicionais) também pode ser definido como a identidade da replica. Se a tabela não tiver nenhuma chave adequada, então ela pode ser definida como identidade de replica `FULL`, o que significa que toda a linha se torna a chave. Quando a identidade de replica `FULL` é especificada, índices podem ser usados no lado do assinante para pesquisar as linhas. Os índices candidatos devem ser btree ou hash, não parciais, e o campo do índice mais à esquerda deve ser uma coluna (não uma expressão) que faça referência à coluna da tabela publicada. Essas restrições sobre as propriedades do índice não único aderem a algumas das restrições que são aplicadas para chaves primárias. Se não houver tais índices adequados, a pesquisa no lado do assinante pode ser muito ineficiente, portanto, a identidade de replica `FULL` só deve ser usada como uma solução de fallback se nenhuma outra solução for possível.

Se uma identidade de replicação diferente de `FULL` for definida no lado do editor, uma identidade de replicação que compreenda as mesmas colunas ou menos também deve ser definida no lado do assinante.

Tabelas com uma identidade replica definida como `NOTHING`, `DEFAULT` sem uma chave primária, ou `USING INDEX` com um índice excluído, não podem suportar operações `UPDATE` ou `DELETE` quando incluídas em uma publicação que replica essas ações. Tentar realizar tais operações resultará em um erro no editor.

As operações `INSERT` podem prosseguir independentemente de qualquer identidade de replicação.

Veja `ALTER TABLE...REPLICA IDENTITY`(sql-altertable.md#SQL-ALTERTABLE-REPLICA-IDENTITY) para obter detalhes sobre como definir a identidade da replica.