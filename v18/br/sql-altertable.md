## ALTER TABLE

ALTER TABLE — alterar a definição de uma tabela

## Sinopse

```
ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    action [, ... ]
ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME [ COLUMN ] column_name TO new_column_name
ALTER TABLE [ IF EXISTS ] [ ONLY ] name [ * ]
    RENAME CONSTRAINT constraint_name TO new_constraint_name
ALTER TABLE [ IF EXISTS ] name
    RENAME TO new_name
ALTER TABLE [ IF EXISTS ] name
    SET SCHEMA new_schema
ALTER TABLE ALL IN TABLESPACE name [ OWNED BY role_name [, ... ] ]
    SET TABLESPACE new_tablespace [ NOWAIT ]
ALTER TABLE [ IF EXISTS ] name
    ATTACH PARTITION partition_name { FOR VALUES partition_bound_spec | DEFAULT }
ALTER TABLE [ IF EXISTS ] name
    DETACH PARTITION partition_name [ CONCURRENTLY | FINALIZE ]

where action is one of:

    ADD [ COLUMN ] [ IF NOT EXISTS ] column_name data_type [ COLLATE collation ] [ column_constraint [ ... ] ]
    DROP [ COLUMN ] [ IF EXISTS ] column_name [ RESTRICT | CASCADE ]
    ALTER [ COLUMN ] column_name [ SET DATA ] TYPE data_type [ COLLATE collation ] [ USING expression ]
    ALTER [ COLUMN ] column_name SET DEFAULT expression
    ALTER [ COLUMN ] column_name DROP DEFAULT
    ALTER [ COLUMN ] column_name { SET | DROP } NOT NULL
    ALTER [ COLUMN ] column_name SET EXPRESSION AS ( expression )
    ALTER [ COLUMN ] column_name DROP EXPRESSION [ IF EXISTS ]
    ALTER [ COLUMN ] column_name ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ]
    ALTER [ COLUMN ] column_name { SET GENERATED { ALWAYS | BY DEFAULT } | SET sequence_option | RESTART [ [ WITH ] restart ] } [...]
    ALTER [ COLUMN ] column_name DROP IDENTITY [ IF EXISTS ]
    ALTER [ COLUMN ] column_name SET STATISTICS { integer | DEFAULT }
    ALTER [ COLUMN ] column_name SET ( attribute_option = value [, ... ] )
    ALTER [ COLUMN ] column_name RESET ( attribute_option [, ... ] )
    ALTER [ COLUMN ] column_name SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }
    ALTER [ COLUMN ] column_name SET COMPRESSION compression_method
    ADD table_constraint [ NOT VALID ]
    ADD table_constraint_using_index
    ALTER CONSTRAINT constraint_name [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]
    ALTER CONSTRAINT constraint_name [ INHERIT | NO INHERIT ]
    VALIDATE CONSTRAINT constraint_name
    DROP CONSTRAINT [ IF EXISTS ]  constraint_name [ RESTRICT | CASCADE ]
    DISABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE TRIGGER [ trigger_name | ALL | USER ]
    ENABLE REPLICA TRIGGER trigger_name
    ENABLE ALWAYS TRIGGER trigger_name
    DISABLE RULE rewrite_rule_name
    ENABLE RULE rewrite_rule_name
    ENABLE REPLICA RULE rewrite_rule_name
    ENABLE ALWAYS RULE rewrite_rule_name
    DISABLE ROW LEVEL SECURITY
    ENABLE ROW LEVEL SECURITY
    FORCE ROW LEVEL SECURITY
    NO FORCE ROW LEVEL SECURITY
    CLUSTER ON index_name
    SET WITHOUT CLUSTER
    SET WITHOUT OIDS
    SET ACCESS METHOD { new_access_method | DEFAULT }
    SET TABLESPACE new_tablespace
    SET { LOGGED | UNLOGGED }
    SET ( storage_parameter [= value] [, ... ] )
    RESET ( storage_parameter [, ... ] )
    INHERIT parent_table
    NO INHERIT parent_table
    OF type_name
    NOT OF
    OWNER TO { new_owner | CURRENT_ROLE | CURRENT_USER | SESSION_USER }
    REPLICA IDENTITY { DEFAULT | USING INDEX index_name | FULL | NOTHING }

and partition_bound_spec is:

IN ( partition_bound_expr [, ...] ) |
FROM ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] )
  TO ( { partition_bound_expr | MINVALUE | MAXVALUE } [, ...] ) |
WITH ( MODULUS numeric_literal, REMAINDER numeric_literal )

and column_constraint is:

[ CONSTRAINT constraint_name ]
{ NOT NULL [ NO INHERIT ] |
  NULL |
  CHECK ( expression ) [ NO INHERIT ] |
  DEFAULT default_expr |
  GENERATED ALWAYS AS ( generation_expr ) [ STORED | VIRTUAL ] |
  GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY [ ( sequence_options ) ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] index_parameters |
  PRIMARY KEY index_parameters |
  REFERENCES reftable [ ( refcolumn ) ] [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ]
    [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint is:

[ CONSTRAINT constraint_name ]
{ CHECK ( expression ) [ NO INHERIT ] |
  NOT NULL column_name [ NO INHERIT ] |
  UNIQUE [ NULLS [ NOT ] DISTINCT ] ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  PRIMARY KEY ( column_name [, ... ] [, column_name WITHOUT OVERLAPS ] ) index_parameters |
  EXCLUDE [ USING index_method ] ( exclude_element WITH operator [, ... ] ) index_parameters [ WHERE ( predicate ) ] |
  FOREIGN KEY ( column_name [, ... ] [, PERIOD column_name ] ) REFERENCES reftable [ ( refcolumn [, ... ]  [, PERIOD refcolumn ] ) ]
    [ MATCH FULL | MATCH PARTIAL | MATCH SIMPLE ] [ ON DELETE referential_action ] [ ON UPDATE referential_action ] }
[ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ] [ ENFORCED | NOT ENFORCED ]

and table_constraint_using_index is:

    [ CONSTRAINT constraint_name ]
    { UNIQUE | PRIMARY KEY } USING INDEX index_name
    [ DEFERRABLE | NOT DEFERRABLE ] [ INITIALLY DEFERRED | INITIALLY IMMEDIATE ]

index_parameters in UNIQUE, PRIMARY KEY, and EXCLUDE constraints are:

[ INCLUDE ( column_name [, ... ] ) ]
[ WITH ( storage_parameter [= value] [, ... ] ) ]
[ USING INDEX TABLESPACE tablespace_name ]

exclude_element in an EXCLUDE constraint is:

{ column_name | ( expression ) } [ COLLATE collation ] [ opclass [ ( opclass_parameter = value [, ... ] ) ] ] [ ASC | DESC ] [ NULLS { FIRST | LAST } ]

referential_action in a FOREIGN KEY/REFERENCES constraint is:

{ NO ACTION | RESTRICT | CASCADE | SET NULL [ ( column_name [, ... ] ) ] | SET DEFAULT [ ( column_name [, ... ] ) ] }
```

## Descrição

`ALTER TABLE` altera a definição de uma tabela existente. Há vários subformularizados descritos abaixo. Observe que o nível de bloqueio exigido pode diferir para cada subformulário. Um bloqueio `ACCESS EXCLUSIVE` é adquirido, a menos que seja explicitamente indicado. Quando vários subcomandos são fornecidos, o bloqueio adquirido será o mais rigoroso exigido por qualquer subcomando.

`ADD [ COLUMN ] [ IF NOT EXISTS ]` [#](#SQL-ALTERTABLE-DESC-ADD-COLUMN): Este formulário adiciona uma nova coluna à tabela, usando a mesma sintaxe que [`CREATE TABLE`](sql-createtable.md "CREATE TABLE"). Se `IF NOT EXISTS` for especificado e uma coluna já existir com esse nome, não será lançada nenhuma mensagem de erro.

`DROP [ COLUMN ] [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-COLUMN): Este formulário exclui uma coluna de uma tabela. Os índices e as restrições de tabela que envolvem a coluna serão excluídos automaticamente também. As estatísticas multivariáveis que fazem referência à coluna excluída também serão removidas se a remoção da coluna causar que as estatísticas contenham dados para apenas uma única coluna. Você precisará dizer `CASCADE` se algo fora da tabela depende da coluna, por exemplo, referências de chave estrangeira ou visualizações. Se `IF EXISTS` for especificado e a coluna não existir, não será lançada nenhuma exceção. Nesse caso, em vez disso, será emitido um aviso.

`SET DATA TYPE` [#](#SQL-ALTERTABLE-DESC-SET-DATA-TYPE): Este formulário altera o tipo de uma coluna de uma tabela. Índices e restrições simples de tabela que envolvem a coluna serão automaticamente convertidos para usar o novo tipo de coluna, mediante a reestruturação da expressão originalmente fornecida. A cláusula opcional `COLLATE` especifica uma codificação para a nova coluna; se omitida, a codificação é a padrão para o novo tipo de coluna. A cláusula opcional `USING` especifica como calcular o valor da nova coluna a partir da antiga; se omitida, a conversão padrão é a mesma que uma atribuição de tipo de dados antigo para novo. Uma cláusula `USING` deve ser fornecida se não houver uma atribuição ou conversão de tipo antigo para novo.

Quando este formulário é usado, as estatísticas da coluna são removidas, portanto, é recomendável executar `ANALYZE` (sql-analyze.md "ANALYZE") na tabela posteriormente. Para uma coluna gerada virtualmente, `ANALYZE` não é necessário, porque essas colunas nunca têm estatísticas.

`SET`/`DROP DEFAULT` [#](#SQL-ALTERTABLE-DESC-SET-DROP-DEFAULT): Esses formulários definem ou removem o valor padrão para uma coluna (onde a remoção é equivalente a definir o valor padrão como NULL). O novo valor padrão só se aplicará em comandos subsequentes `INSERT` ou `UPDATE`; ele não causa alterações nas linhas já na tabela.

`SET`/`DROP NOT NULL` [#](#SQL-ALTERTABLE-DESC-SET-DROP-NOT-NULL): Esses formulários alteram se uma coluna é marcada para permitir valores nulos ou para rejeitar valores nulos.

`SET NOT NULL` só pode ser aplicado a uma coluna, desde que nenhum dos registros na tabela contenha um valor `NULL` para a coluna. Normalmente, isso é verificado durante o `ALTER TABLE`, ao digitalizar toda a tabela, a menos que `NOT VALID` seja especificado; no entanto, se existir uma restrição válida `CHECK` (e não seja descartada no mesmo comando) que comprove que não pode existir `NULL`, então o varrimento da tabela é ignorado. Se uma coluna tiver uma restrição não-nulo inválida, `SET NOT NULL` a valida.

Se esta tabela for uma partição, não é possível realizar `DROP NOT NULL` em uma coluna se ela estiver marcada `NOT NULL` na tabela principal. Para descartar a restrição `NOT NULL` de todas as partições, realize `DROP NOT NULL` na tabela principal. Mesmo que não haja restrição `NOT NULL` na tabela principal, é possível adicionar essa restrição a partições individuais, se desejado; ou seja, as crianças podem não permitir nulos, mesmo que a principal os permita, mas não o contrário. Também é possível descartar a restrição `NOT NULL` da tabela principal `ONLY`, o que não a remove das crianças.

`SET EXPRESSION AS` [#](#SQL-ALTERTABLE-DESC-SET-EXPRESSION): Este formulário substitui a expressão de uma coluna gerada. Os dados existentes em uma coluna gerada armazenada são reescritos e todas as mudanças futuras aplicarão a nova expressão de geração.

Quando este formulário é usado em uma coluna gerada armazenada, suas estatísticas são removidas, portanto, executar `ANALYZE` (sql-analyze.md "ANALYZE") na tabela posteriormente é recomendado. Para uma coluna gerada virtualmente, `ANALYZE` não é necessário porque tais colunas nunca têm estatísticas.

`DROP EXPRESSION [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-EXPRESSION): Este formulário transforma uma coluna gerada armazenada em uma coluna normal de base. Os dados existentes nas colunas são retidos, mas as mudanças futuras não aplicarão mais a expressão de geração.

Este formulário é atualmente suportado apenas para colunas geradas armazenadas (não virtuais).

Se `DROP EXPRESSION IF EXISTS` for especificado e a coluna não for uma coluna gerada, não será lançada nenhuma mensagem de erro. Nesse caso, é emitida uma notificação em vez disso.

`ADD GENERATED { ALWAYS | BY DEFAULT } AS IDENTITY` `SET GENERATED { ALWAYS | BY DEFAULT }` `DROP IDENTITY [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-GENERATED-IDENTITY): Esses formulários alteram se uma coluna é uma coluna de identidade ou alteram o atributo de geração de uma coluna de identidade existente. Consulte [`CREATE TABLE`](sql-createtable.md "CREATE TABLE") para obter detalhes. Como `SET DEFAULT`, esses formulários afetam apenas o comportamento dos comandos subsequentes `INSERT` e `UPDATE`; eles não causam alterações nas linhas já na tabela.

Se `DROP IDENTITY IF EXISTS` for especificado e a coluna não for uma coluna de identidade, não será lançada nenhuma exceção. Nesse caso, é emitido um aviso em vez disso.

`SET sequence_option` `RESTART` [#](#SQL-ALTERTABLE-DESC-SET-SEQUENCE-OPTION): Esses formulários alteram a sequência que fundamenta uma coluna de identidade existente. *`sequence_option`* é uma opção suportada por [`ALTER SEQUENCE`](sql-altersequence.md "ALTER SEQUENCE") como `INCREMENT BY`.

`SET STATISTICS` [#](#SQL-ALTERTABLE-DESC-SET-STATISTICS): Este formulário define o objetivo de coleta de estatísticas por coluna para operações subsequentes do `ANALYZE`(sql-analyze.md "ANALYZE"). O objetivo pode ser definido na faixa de 0 a 10000. Defina-o em `DEFAULT` para retornar ao uso do objetivo de estatísticas padrão do sistema ([default_statistics_target](runtime-config-query.md#GUC-DEFAULT-STATISTICS-TARGET)). (Definir um valor de -1 é uma maneira obsoleta de obter o mesmo resultado.) Para mais informações sobre o uso de estatísticas pelo planejador de consultas do PostgreSQL, consulte [Seção 14.2](planner-stats.md "14.2. Statistics Used by the Planner").

`SET STATISTICS` adquire um bloqueio `SHARE UPDATE EXCLUSIVE`.

`SET ( attribute_option = value [, ... ] )` `RESET ( attribute_option [, ... ] )` [#](#SQL-ALTERTABLE-DESC-SET-ATTRIBUTE-OPTION): Este formulário define ou redefine opções por atributo. Atualmente, as únicas opções por atributo definidas são `n_distinct` e `n_distinct_inherited`, que substituem as estimativas do número de valores distintos feitas por operações subsequentes [`ANALYZE`](sql-analyze.md "ANALYZE"). `n_distinct` afeta as estatísticas da própria tabela, enquanto `n_distinct_inherited` afeta as estatísticas coletadas para a tabela mais seus filhos de herança e para as estatísticas coletadas para tabelas particionadas. Quando o valor especificado é um valor positivo, o planejador de consulta assumirá que a coluna contém exatamente o número especificado de valores distintos não nulos. Valores fracionários também podem ser especificados usando valores abaixo de 0 e acima ou iguais a -1. Isso instrui o planejador de consulta a estimar o número de valores distintos multiplicando o valor absoluto do número especificado pelo número estimado de linhas na tabela. Por exemplo, um valor de -1 implica que todos os valores na coluna são distintos, enquanto um valor de -0,5 implica que cada valor aparece duas vezes em média. Isso pode ser útil quando o tamanho da tabela muda ao longo do tempo. Para mais informações sobre o uso de estatísticas pelo planejador de consulta do PostgreSQL, consulte [Seção 14.2](planner-stats.md "14.2. Statistics Used by the Planner").

Altere as opções por atributo e adquirirá um bloqueio `SHARE UPDATE EXCLUSIVE`.

`SET STORAGE { PLAIN | EXTERNAL | EXTENDED | MAIN | DEFAULT }` [#](#SQL-ALTERTABLE-DESC-SET-STORAGE): Este formulário define o modo de armazenamento para uma coluna. Isso controla se essa coluna será mantida em linha ou em uma tabela secundária TOAST, e se os dados devem ser comprimidos ou não. `PLAIN` deve ser usado para valores de comprimento fixo, como `integer` e é em linha, não comprimido. `MAIN` é para dados em linha, comprimíveis. `EXTERNAL` é para dados externos, não comprimidos, e `EXTENDED` é para dados externos, comprimidos. Escrever `DEFAULT` define o modo de armazenamento para o modo padrão para o tipo de dados da coluna. `EXTENDED` é o padrão para a maioria dos tipos de dados que suportam armazenamento não `PLAIN`. O uso de `EXTERNAL` fará com que as operações de subcadeia em valores muito grandes `text` e `bytea` sejam executadas mais rápido, com a penalidade de aumento do espaço de armazenamento. Note que `ALTER TABLE ... SET STORAGE` não muda nada na tabela; ele apenas define a estratégia a ser seguida durante futuras atualizações da tabela. Consulte [Seção 66.2](storage-toast.md "66.2. TOAST") para mais informações.

`SET COMPRESSION compression_method` [#](#SQL-ALTERTABLE-DESC-SET-COMPRESSION): Este formulário define o método de compressão para uma coluna, determinando como os valores inseridos no futuro serão comprimidos (se o modo de armazenamento permitir a compressão em qualquer caso). Isso não faz com que a tabela seja reescrita, portanto, os dados existentes ainda podem ser comprimidos com outros métodos de compressão. Se a tabela for restaurada com o pg_restore, então todos os valores serão reescritos com o método de compressão configurado. No entanto, quando os dados são inseridos a partir de outra relação (por exemplo, por `INSERT ... SELECT`, os valores da tabela de origem não são necessariamente descompressados, portanto, qualquer dado previamente comprimido pode manter seu método de compressão existente, em vez de ser recomprimido com o método de compressão da coluna de destino. Os métodos de compressão suportados são `pglz` e `lz4`. (`lz4` está disponível apenas se `--with-lz4` foi usado ao construir o PostgreSQL.) Além disso, *`compression_method`* pode ser `default`, que seleciona o comportamento padrão de consultar a configuração [default_toast_compression](runtime-config-client.md#GUC-DEFAULT-TOAST-COMPRESSION) no momento da inserção de dados para determinar o método a ser usado.

`ADD table_constraint [ NOT VALID ]` [#](#SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT): Este formulário adiciona uma nova restrição a uma tabela usando a mesma sintaxe de restrição que [`CREATE TABLE`](sql-createtable.md "CREATE TABLE"), além da opção `NOT VALID`, que atualmente só é permitida para restrições de chave estrangeira, `CHECK`, e não nulo.

Normalmente, essa forma causará uma varredura da tabela para verificar se todas as linhas existentes na tabela satisfazem a nova restrição. Mas se a opção `NOT VALID` for usada, essa varredura potencialmente demorada é ignorada. A restrição ainda será aplicada em inserções ou atualizações subsequentes (ou seja, elas falharão, a menos que haja uma linha correspondente na tabela referenciada, no caso de chaves estrangeiras, ou elas falharão, a menos que a nova linha corresponda à condição de verificação especificada). Mas o banco de dados não assumirá que a restrição se aplica a todas as linhas da tabela, até que seja validada usando a opção `VALIDATE CONSTRAINT`. Consulte [Notas][(sql-altertable.md#SQL-ALTERTABLE-NOTES "Notes")] abaixo para obter mais informações sobre o uso da opção `NOT VALID`.

Embora a maioria das formas de `ADD table_constraint` exija um bloqueio de `ACCESS EXCLUSIVE`, o `ADD FOREIGN KEY` requer apenas um bloqueio de `SHARE ROW EXCLUSIVE`. Observe que o `ADD FOREIGN KEY` também adquire um bloqueio de `SHARE ROW EXCLUSIVE` na tabela referenciada, além do bloqueio na tabela na qual a restrição é declarada.

Restrições adicionais se aplicam quando restrições de chave única ou primária são adicionadas a tabelas particionadas; consulte `CREATE TABLE`(sql-createtable.md "CREATE TABLE").

`ADD table_constraint_using_index` [#](#SQL-ALTERTABLE-DESC-ADD-TABLE-CONSTRAINT-USING-INDEX): Este formulário adiciona uma nova restrição `PRIMARY KEY` ou `UNIQUE` a uma tabela com base em um índice único existente. Todas as colunas do índice serão incluídas na restrição.

O índice não pode ter colunas de expressão nem ser um índice parcial. Além disso, ele deve ser um índice de árvore b com a ordem de classificação padrão. Essas restrições garantem que o índice seja equivalente ao que seria construído por um comando regular do `ADD PRIMARY KEY` ou `ADD UNIQUE`.

Se `PRIMARY KEY` for especificado e as colunas do índice não estiverem já marcadas `NOT NULL`, então este comando tentará realizar `ALTER COLUMN SET NOT NULL` contra cada uma dessas colunas. Isso requer uma varredura completa da tabela para verificar se as colunas não contêm nulos. Em todos os outros casos, essa é uma operação rápida.

Se um nome de restrição for fornecido, o índice será renomeado para corresponder ao nome da restrição. Caso contrário, a restrição será nomeada da mesma forma que o índice.

Após a execução deste comando, o índice é “devido” à restrição, da mesma forma como se o índice tivesse sido construído por um comando regular do tipo `ADD PRIMARY KEY` ou `ADD UNIQUE`. Em particular, a eliminação da restrição fará com que o índice também desapareça.

Este formulário não é atualmente suportado em tabelas particionadas.

### Nota

Adicionar uma restrição usando um índice existente pode ser útil em situações em que uma nova restrição precisa ser adicionada sem bloquear as atualizações da tabela por um longo período. Para fazer isso, crie o índice usando `CREATE UNIQUE INDEX CONCURRENTLY`, e, em seguida, converta-o em uma restrição usando este sintaxe. Veja o exemplo abaixo.

`ALTER CONSTRAINT` [#](#SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT): Este formulário altera os atributos de uma restrição que foi criada anteriormente. Atualmente, apenas as restrições de chave estrangeira podem ser alteradas dessa maneira, mas veja abaixo.

`ALTER CONSTRAINT ... INHERIT` `ALTER CONSTRAINT ... NO INHERIT` [#](#SQL-ALTERTABLE-DESC-ALTER-CONSTRAINT-INHERIT): Essas formas modificam uma restrição hereditária de modo que ela não se torne hereditária, ou vice-versa. Apenas restrições não nulos podem ser alteradas dessa maneira atualmente. Além de mudar o status de hereditariedade da restrição, no caso em que uma restrição não hereditária está sendo marcada como hereditária, se a tabela tiver filhos, uma restrição equivalente será adicionada a eles. Se marcar uma restrição hereditária como não hereditária em uma tabela com filhos, então a restrição correspondente nos filhos será marcada como não mais herdada, mas não removida.

`VALIDATE CONSTRAINT` [#](#SQL-ALTERTABLE-DESC-VALIDATE-CONSTRAINT): Este formulário valida uma chave estrangeira, uma verificação ou uma restrição não nula que foi criada anteriormente como `NOT VALID`, verificando a tabela para garantir que não haja linhas para as quais a restrição não seja satisfeita. Se a restrição foi definida como `NOT ENFORCED`, um erro é lançado. Não acontece nada se a restrição já estiver marcada como válida. (Veja [Notas](sql-altertable.md#SQL-ALTERTABLE-NOTES "Notes") abaixo para uma explicação sobre a utilidade deste comando.)

Este comando adquire um bloqueio `SHARE UPDATE EXCLUSIVE`.

`DROP CONSTRAINT [ IF EXISTS ]` [#](#SQL-ALTERTABLE-DESC-DROP-CONSTRAINT): Este formulário elimina a restrição especificada em uma tabela, juntamente com qualquer índice que subjaz à restrição. Se `IF EXISTS` for especificado e a restrição não existir, não será lançada nenhuma mensagem de erro. Nesse caso, em vez disso, é emitida uma notificação.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] TRIGGER` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-TRIGGER): Esses formulários configuram o disparo do(s) gatilho(s) pertencente(s) à tabela. É sabido que um gatilho desativado ainda é conhecido pelo sistema, mas não é executado quando seu evento de disparo ocorre. (Para um gatilho diferido, o status de ativação é verificado quando o evento ocorre, não quando a função do gatilho é realmente executada.) É possível desativar ou ativar um único gatilho especificado por nome, ou todos os gatilhos na tabela, ou apenas gatilhos de usuário (esta opção exclui gatilhos de restrição gerados internamente, como aqueles que são usados para implementar restrições de chave estrangeira ou restrições de unicidade e exclusão diferíveis). Desativar ou ativar gatilhos de restrição gerados internamente requer privilégios de superusuário; deve ser feito com cautela, pois, claro, a integridade da restrição não pode ser garantida se os gatilhos não forem executados.

O mecanismo de disparo do gatilho também é afetado pela variável de configuração [session_replication_role][(runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE)]. Gatilhos simplesmente habilitados (o padrão) serão disparados quando o papel de replicação estiver configurado como “origem” (o padrão) ou “local”. Gatilhos configurados como `ENABLE REPLICA` serão disparados apenas se a sessão estiver no modo “replica”, e gatilhos configurados como `ENABLE ALWAYS` serão disparados independentemente do papel de replicação atual.

O efeito desse mecanismo é que, na configuração padrão, os gatilhos não são acionados em réplicas. Isso é útil porque, se um gatilho for usado na origem para propagar dados entre tabelas, o sistema de replicação também replicará os dados propagados; portanto, o gatilho não deve ser acionado novamente na replica, porque isso levaria à duplicação. No entanto, se um gatilho for usado para outro propósito, como criar alertas externos, então pode ser apropriado configurá-lo para `ENABLE ALWAYS` para que ele também seja acionado em réplicas.

Quando este comando é aplicado a uma tabela particionada, os estados dos gatilhos de clone correspondentes nas partições também são atualizados, a menos que `ONLY` seja especificado.

Este comando adquire um bloqueio `SHARE ROW EXCLUSIVE`.

`DISABLE`/`ENABLE [ REPLICA | ALWAYS ] RULE` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-RULE): Essas formas configuram o disparo de regras de reescrita pertencentes à tabela. Uma regra desativada ainda é conhecida pelo sistema, mas não é aplicada durante a reescrita da consulta. A semântica é a mesma para gatilhos ativados/desativados. Esta configuração é ignorada para as regras `ON SELECT`, que são sempre aplicadas para manter as visualizações funcionando mesmo se a sessão atual estiver em um papel de replicação não padrão.

O mecanismo de disparo de regra também é afetado pela variável de configuração [session_replication_role](runtime-config-client.md#GUC-SESSION-REPLICATION-ROLE), análogo aos gatilhos como descrito acima.

`DISABLE`/`ENABLE ROW LEVEL SECURITY` [#](#SQL-ALTERTABLE-DESC-DISABLE-ENABLE-ROW-LEVEL-SECURITY): Esses formulários controlam a aplicação de políticas de segurança de linha pertencentes à tabela. Se habilitado e não houver políticas para a tabela, então uma política de negação padrão é aplicada. Observe que as políticas podem existir para uma tabela mesmo que a segurança de nível de linha seja desativada. Neste caso, as políticas *não* serão aplicadas e as políticas serão ignoradas. Veja também [`CREATE POLICY`](sql-createpolicy.md "CREATE POLICY").

`NO FORCE`/`FORCE ROW LEVEL SECURITY` [#](#SQL-ALTERTABLE-DESC-FORCE-ROW-LEVEL-SECURITY): Esses formulários controlam a aplicação de políticas de segurança de linha pertencentes à tabela quando o usuário é o proprietário da tabela. Se habilitado, as políticas de segurança de nível de linha serão aplicadas quando o usuário é o proprietário da tabela. Se desabilitado (o padrão), a segurança de nível de linha não será aplicada quando o usuário é o proprietário da tabela. Veja também [`CREATE POLICY`](sql-createpolicy.md "CREATE POLICY").

`CLUSTER ON` [#](#SQL-ALTERTABLE-DESC-CLUSTER-ON): Este formulário seleciona o índice padrão para operações futuras de `CLUSTER` [#](sql-cluster.md "CLUSTER"). Na verdade, ele não reclasifica a tabela.

Altere as opções do cluster e obtenha um bloqueio `SHARE UPDATE EXCLUSIVE`.

`SET WITHOUT CLUSTER` [#](#SQL-ALTERTABLE-DESC-SET-WITHOUT-CLUSTER): Este formulário remove a especificação de índice de `CLUSTER` mais recentemente usado da tabela. Isso afeta operações futuras de agrupamento que não especificam um índice.

Altere as opções do cluster e obtenha um bloqueio `SHARE UPDATE EXCLUSIVE`.

`SET WITHOUT OIDS` [#](#SQL-ALTERTABLE-DESC-SET-WITHOUT-OIDS): Sintaxe retrocompatível para remover a coluna do sistema `oid`. Como as colunas do sistema `oid` não podem ser adicionadas mais, isso nunca tem efeito.

`SET ACCESS METHOD` [#](#SQL-ALTERTABLE-DESC-SET-ACCESS-METHOD): Este formulário altera o método de acesso da tabela, reescrevendo-a usando o método de acesso indicado; especificando `DEFAULT` seleciona o método de acesso definido como o parâmetro de configuração [default_table_access_method](runtime-config-client.md#GUC-DEFAULT-TABLE-ACCESS-METHOD). Consulte [Capítulo 62](tableam.md "Chapter 62. Table Access Method Interface Definition") para obter mais informações.

Quando aplicado a uma tabela particionada, não há dados a serem reescritos, mas as partições criadas posteriormente terão o método de acesso padrão, a menos que sejam sobrescritos por uma cláusula `USING`. Especificar `DEFAULT` remove um valor anterior, fazendo com que as partições futuras tenham o padrão `default_table_access_method`.

`SET TABLESPACE` [#](#SQL-ALTERTABLE-DESC-SET-TABLESPACE): Este formulário altera o espaço de tabela para o espaço de tabela especificado e move o(s) arquivo(s) de dados associado(s) à tabela para o novo espaço de tabela. Os índices na tabela, se houver, não são movidos; mas eles podem ser movidos separadamente com comandos adicionais `SET TABLESPACE`. Quando aplicado a uma tabela particionada, nada é movido, mas quaisquer particionamentos criados posteriormente com `CREATE TABLE PARTITION OF` usarão esse espaço de tabela, a menos que seja sobrescrito por uma cláusula `TABLESPACE`.

Todas as tabelas no banco de dados atual em um espaço de tabelas podem ser movidas usando o formulário `ALL IN TABLESPACE`, que irá bloquear todas as tabelas a serem movidas primeiro e, em seguida, mover cada uma delas. Este formulário também suporta `OWNED BY`, que irá mover apenas as tabelas de propriedade dos papéis especificados. Se a opção `NOWAIT` for especificada, o comando falhará se não conseguir adquirir todos os bloqueios necessários imediatamente. Observe que os catálogos do sistema não são movidos por este comando; use `ALTER DATABASE` ou invocções explícitas de `ALTER TABLE` se desejar. As relações `information_schema` não são consideradas parte dos catálogos do sistema e serão movidas. Veja também [`CREATE TABLESPACE`](sql-createtablespace.md "CREATE TABLESPACE").

`SET { LOGGED | UNLOGGED }` [#](#SQL-ALTERTABLE-DESC-SET-LOGGED-UNLOGGED): Este formulário altera a tabela de não registrada para registrada ou vice-versa (consulte [`UNLOGGED`](sql-createtable.md#SQL-CREATETABLE-UNLOGGED)). Não pode ser aplicado a uma tabela temporária.

Isso também altera a persistência de quaisquer sequências vinculadas à tabela (para colunas de identidade ou de série). No entanto, também é possível alterar a persistência dessas sequências separadamente.

Este formulário não é suportado para tabelas particionadas.

`SET ( storage_parameter [= value] [, ... ] )` [#](#SQL-ALTERTABLE-DESC-SET-STORAGE-PARAMETER): Este formulário altera um ou mais parâmetros de armazenamento da tabela. Consulte os detalhes dos parâmetros disponíveis na documentação da tabela [`CREATE TABLE`(sql-createtable.md "CREATE TABLE")]. Observe que o conteúdo da tabela não será modificado imediatamente por este comando; dependendo do parâmetro, você pode precisar reescrever a tabela para obter os efeitos desejados. Isso pode ser feito com [`VACUUM FULL`(sql-vacuum.md "VACUUM"), [`CLUSTER`(sql-cluster.md "CLUSTER")]] ou uma das formas de [`ALTER TABLE`]] que força a reescrita da tabela. Para parâmetros relacionados ao planejador, as alterações terão efeito a partir da próxima vez que a tabela for bloqueada, portanto, as consultas atualmente em execução não serão afetadas.

O bloqueio `SHARE UPDATE EXCLUSIVE` será tomado para os parâmetros de armazenamento de fillfactor, toast e autovacuum, bem como o parâmetro do planejador `parallel_workers`.

`RESET ( storage_parameter [, ... ] )` [#](#SQL-ALTERTABLE-DESC-RESET-STORAGE-PARAMETER): Este formulário redefre o(s) parâmetro(es) de armazenamento para seus valores padrão. Como mencionado em `SET`, pode ser necessário uma reescrita de tabela para atualizar a tabela inteira.

`INHERIT parent_table` [#](#SQL-ALTERTABLE-DESC-INHERIT): Este formulário adiciona a tabela-alvo como uma nova criança da tabela-pai especificada. Posteriormente, as consultas contra o pai incluirão registros da tabela-alvo. Para ser adicionado como uma criança, a tabela-alvo deve conter todos os mesmos campos que o pai (pode ter colunas adicionais também). Os campos devem ter tipos de dados correspondentes.

Além disso, todas as restrições `CHECK` e `NOT NULL` do pai também devem existir na criança, exceto aquelas marcadas como não hereditárias (ou seja, criadas com `ALTER TABLE ... ADD CONSTRAINT ... NO INHERIT`, que são ignoradas). Todas as restrições correspondentes à tabela da criança não devem ser marcadas como não hereditárias. Atualmente, as restrições `UNIQUE`, `PRIMARY KEY` e `FOREIGN KEY` não são consideradas, mas isso pode mudar no futuro.

`NO INHERIT parent_table` [#](#SQL-ALTERTABLE-DESC-NO-INHERIT): Este formulário remove a tabela-alvo da lista de filhos da tabela-padrão especificada. As consultas contra a tabela-padrão não incluirão mais registros retirados da tabela-alvo.

`OF type_name` [#](#SQL-ALTERTABLE-DESC-OF): Este formulário vincula a tabela a um tipo composto como se `CREATE TABLE OF` o tivesse formado. A lista de nomes e tipos de colunas da tabela deve corresponder exatamente àquela do tipo composto. A tabela não deve herdar de nenhuma outra tabela. Essas restrições garantem que `CREATE TABLE OF` permitiria uma definição de tabela equivalente.

`NOT OF` [#](#SQL-ALTERTABLE-DESC-NOT-OF): Este formulário desvincula uma tabela tipificada de seu tipo.

`OWNER TO` [#](#SQL-ALTERTABLE-DESC-OWNER-TO): Este formulário altera o proprietário da tabela, sequência, visualização, visualização materializada ou tabela externa para o usuário especificado.

`REPLICA IDENTITY` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY): Este formulário altera as informações que são escritas no log de pré-escrita para identificar as linhas que são atualizadas ou excluídas. Na maioria dos casos, o valor antigo de cada coluna é apenas registrado se diferir do novo valor; no entanto, se o valor antigo for armazenado externamente, ele é sempre registrado, independentemente de ter sido alterado ou não. Esta opção não tem efeito, exceto quando a replicação lógica está em uso.

`DEFAULT` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-DEFAULT) : Registra os valores antigos das colunas da chave primária. Este é o comportamento padrão para tabelas não-sistemáticas. Quando não há chave primária, o comportamento é o mesmo que `NOTHING`.

`USING INDEX index_name` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-USING-INDEX) :   Registra os valores antigos das colunas cobertas pelo índice nomeado, que devem ser únicos, não parciais, não diferíveis e incluir apenas colunas marcadas `NOT NULL`. Se este índice for descartado, o comportamento é o mesmo que `NOTHING`.

`FULL` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-FULL) : Registra os valores antigos de todas as colunas na linha.

`NOTHING` [#](#SQL-ALTERTABLE-REPLICA-IDENTITY-NOTHING) :   Não contém informações sobre a linha antiga. Esse é o padrão para as tabelas do sistema.

`RENAME` [#](#SQL-ALTERTABLE-DESC-RENAME): As formas dos formulários `RENAME` alteram o nome de uma tabela (ou de um índice, sequência, visão, visão materializada ou tabela externa), o nome de uma coluna individual em uma tabela ou o nome de uma restrição da tabela. Ao renomear uma restrição que tem um índice subjacente, o índice também é renomeado. Não há efeito nos dados armazenados.

`SET SCHEMA` [#](#SQL-ALTERTABLE-DESC-SET-SCHEMA): Este formulário move a tabela para outro esquema. Os índices associados, restrições e sequências de propriedade das colunas da tabela também são movidos.

`ATTACH PARTITION partition_name { FOR VALUES partition_bound_spec | DEFAULT }` [#](#SQL-ALTERTABLE-ATTACH-PARTITION): Este formulário anexa uma tabela existente (que pode ser particionada) como uma partição da tabela de destino. A tabela pode ser anexada como uma partição para valores específicos usando `FOR VALUES` ou como uma partição padrão usando `DEFAULT`. Para cada índice na tabela de destino, um correspondente será criado na tabela anexada; ou, se um índice equivalente já existir, ele será anexado ao índice da tabela de destino, como se `ALTER INDEX ATTACH PARTITION` tivesse sido executado. Note que, se a tabela existente for uma tabela estrangeira, atualmente não é permitido anexar a tabela como uma partição da tabela de destino se houver índices `UNIQUE` na tabela de destino. (Veja também [CREATE FOREIGN TABLE](sql-createforeigntable.md "CREATE FOREIGN TABLE").). Para cada gatilho definido pelo usuário em nível de linha que existe na tabela de destino, um correspondente é criado na tabela anexada.

Uma partição usando `FOR VALUES` utiliza a mesma sintaxe para *`partition_bound_spec`* quanto [(sql-createtable.md "CREATE TABLE")]. A especificação de vinculação da partição deve corresponder à estratégia de particionamento e à chave de particionamento da tabela-alvo. A tabela a ser anexada deve ter todas as mesmas colunas que a tabela-alvo e não mais; além disso, os tipos de coluna também devem corresponder. Além disso, ela deve ter todas as restrições `NOT NULL` e `CHECK` da tabela-alvo, não marcadas `NO INHERIT`. Atualmente, as restrições `FOREIGN KEY` não são consideradas. As restrições `UNIQUE` e `PRIMARY KEY` da tabela-pai serão criadas na partição, se ainda não existirem.

Se a nova partição for uma tabela regular, uma varredura completa da tabela é realizada para verificar se as linhas existentes na tabela não violam o constrangimento da partição. É possível evitar essa varredura adicionando um constrangimento válido `CHECK` à tabela que permite apenas as linhas que satisfazem o constrangimento de partição desejado antes de executar este comando. O constrangimento `CHECK` será usado para determinar que a tabela não precisa ser varrida para validar o constrangimento da partição. Isso, no entanto, não funciona se qualquer uma das chaves de partição for uma expressão e a partição não aceite valores `NULL`. Se estiver anexando uma partição de lista que não aceitará valores `NULL`, adicione também um constrangimento `NOT NULL` à coluna da chave de partição, a menos que seja uma expressão.

Se a nova partição for uma tabela estrangeira, nada é feito para verificar se todas as linhas da tabela estrangeira obedecem ao constrangimento da partição. (Veja a discussão em [CREATE FOREIGN TABLE][(sql-createforeigntable.md "CREATE FOREIGN TABLE")] sobre os constrangimentos na tabela estrangeira.)

Quando uma tabela tem uma partição padrão, definir uma nova partição altera a restrição de partição da partição padrão. A partição padrão não pode conter quaisquer linhas que precisem ser movidas para a nova partição e será verificada para garantir que nenhuma delas esteja presente. Essa verificação, assim como a verificação da nova partição, pode ser evitada se houver uma restrição apropriada `CHECK`. Também, assim como a verificação da nova partição, ela é sempre ignorada quando a partição padrão é uma tabela estrangeira.

Ao anexar uma partição, o `SHARE UPDATE EXCLUSIVE` adquire um bloqueio na tabela pai, além dos bloqueios `ACCESS EXCLUSIVE` na tabela anexada e na partição padrão (se houver).

Outras chaves também devem ser mantidas em todas as subpartições se a tabela que está sendo anexada for ela mesma uma tabela particionada. Da mesma forma, se a partição padrão for ela mesma uma tabela particionada. O bloqueio das subpartições pode ser evitado adicionando uma restrição `CHECK` conforme descrito em [Seção 5.12.2.2][(ddl-partitioning.md#DDL-PARTITIONING-DECLARATIVE-MAINTENANCE "5.12.2.2. Partition Maintenance")].

`DETACH PARTITION partition_name [ CONCURRENTLY | FINALIZE ]` [#](#SQL-ALTERTABLE-DETACH-PARTITION): Este formulário desvincula a partição especificada da tabela de destino. A partição desvinculada continua a existir como uma tabela autônoma, mas não tem mais qualquer vínculo com a tabela da qual foi desvinculada. Quaisquer índices que foram anexados aos índices da tabela de destino são desvinculados. Quaisquer gatilhos que foram criados como clones daqueles na tabela de destino são removidos. O bloqueio `SHARE` é obtido em quaisquer tabelas que façam referência a esta tabela particionada em restrições de chave estrangeira.

Se `CONCURRENTLY` for especificado, ele é executado com um nível de bloqueio reduzido para evitar bloquear outras sessões que possam estar acessando a tabela particionada. Nesse modo, duas transações são usadas internamente. Durante a primeira transação, uma `SHARE UPDATE EXCLUSIVE` é tomada em ambas as tabelas pai e na partição, e a partição é marcada como em processo de desmontagem; nesse ponto, a transação é comprometida e todas as outras transações que usam a tabela particionada são esperadas. Uma vez que todas essas transações tenham sido concluídas, a segunda transação adquire `SHARE UPDATE EXCLUSIVE` na tabela particionada e `ACCESS EXCLUSIVE` na partição, e o processo de desmontagem é concluído. Uma restrição `CHECK` que duplica a restrição da partição é adicionada à partição. `CONCURRENTLY` não pode ser executado em um bloco de transação e não é permitido se a tabela particionada contiver uma partição padrão.

Se `FINALIZE` for especificado, uma invocação anterior `DETACH CONCURRENTLY` que foi cancelada ou interrompida é concluída. No máximo, uma partição em uma tabela particionada pode estar pendente de desvinculação de cada vez.

Todas as formas de `ALTER TABLE` que atuam em uma única tabela, exceto `RENAME`, `SET SCHEMA`, `ATTACH PARTITION` e `DETACH PARTITION`, podem ser combinadas em uma lista de várias alterações a serem aplicadas juntas. Por exemplo, é possível adicionar várias colunas e/ou alterar o tipo de várias colunas em um único comando. Isso é particularmente útil com tabelas grandes, pois apenas uma passagem pela tabela precisa ser feita.

Você deve possuir a tabela para usar `ALTER TABLE`. Para alterar o esquema ou o espaço de tabelas de uma tabela, você também deve ter o privilégio `CREATE` no novo esquema ou espaço de tabelas. Para adicionar a tabela como uma nova subtabela de uma tabela pai, você também deve possuir a tabela pai. Além disso, para anexar uma tabela como uma nova partição da tabela, você deve possuir a tabela sendo anexada. Para alterar o proprietário, você deve ser capaz de `SET ROLE` para o novo papel de proprietário, e esse papel deve ter o privilégio `CREATE` no esquema da tabela. (Essas restrições garantem que alterar o proprietário não faz nada que você não poderia fazer ao descartar e recriar a tabela. No entanto, um superusuário pode alterar a propriedade de qualquer tabela de qualquer maneira.) Para adicionar uma coluna ou alterar o tipo de coluna ou usar a cláusula `OF`, você também deve ter o privilégio `USAGE` no tipo de dados.

## Parâmetros

`IF EXISTS` [#](#SQL-ALTERTABLE-PARMS-IF-EXISTS): Não exija erro se a tabela não existir. Neste caso, é emitido um aviso.

*`name`* [#](#SQL-ALTERTABLE-PARMS-NAME): O nome (opcionalmente qualificado por esquema) de uma tabela existente para alterar. Se `ONLY` é especificado antes do nome da tabela, apenas essa tabela é alterada. Se `ONLY` não é especificado, a tabela e todas as suas tabelas descendentes (se houver) são alteradas. Opcionalmente, `*` pode ser especificado após o nome da tabela para indicar explicitamente que as tabelas descendentes são incluídas.

*`column_name`* [#](#SQL-ALTERTABLE-PARMS-COLUMN-NAME): Nome de uma coluna nova ou existente.

*`new_column_name`* [#](#SQL-ALTERTABLE-PARMS-NEW-COLUMN-NAME): Novo nome para uma coluna existente.

*`new_name`* [#](#SQL-ALTERTABLE-PARMS-NEW-NAME): Novo nome para a tabela.

*`data_type`* [#](#SQL-ALTERTABLE-PARMS-DATA-TYPE): Tipo de dados da nova coluna, ou novo tipo de dados para uma coluna existente.

*`table_constraint`* [#](#SQL-ALTERTABLE-PARMS-TABLE-CONSTRAINT): Nova restrição de tabela para a tabela.

*`constraint_name`* [#](#SQL-ALTERTABLE-PARMS-CONSTRAINT-NAME): Nome de uma restrição nova ou existente.

`CASCADE` [#](#SQL-ALTERTABLE-PARMS-CASCADE): Descarte automaticamente os objetos que dependem da coluna ou restrição descartada (por exemplo, vistas que fazem referência à coluna), e, por sua vez, todos os objetos que dependem desses objetos (consulte [Seção 5.15][(ddl-depend.md "5.15. Dependency Tracking")]).

`RESTRICT` [#](#SQL-ALTERTABLE-PARMS-RESTRICT): Rejeitar a eliminação da coluna ou restrição se houver quaisquer objetos dependentes. Esse é o comportamento padrão.

*`trigger_name`* [#](#SQL-ALTERTABLE-PARMS-TRIGGER-NAME): Nome de um único gatilho para desabilitar ou habilitar.

`ALL` [#](#SQL-ALTERTABLE-PARMS-ALL): Desabilitar ou habilitar todos os gatilhos pertencentes à tabela. (Isso requer privilégio de superusuário, se algum dos gatilhos for um gatilho de restrição gerado internamente, como aqueles que são usados para implementar restrições de chave estrangeira ou restrições de unicidade e exclusão diferíveis.)

`USER` [#](#SQL-ALTERTABLE-PARMS-USER): Desabilitar ou habilitar todos os gatilhos pertencentes à tabela, exceto os gatilhos de restrição gerados internamente, como aqueles que são usados para implementar restrições de chave estrangeira ou restrições de unicidade e exclusão diferíveis.

*`index_name`* [#](#SQL-ALTERTABLE-PARMS-INDEX-NAME): O nome de um índice existente.

*`storage_parameter`* [#](#SQL-ALTERTABLE-PARMS-STORAGE-PARAMETER): O nome de um parâmetro de armazenamento de tabela.

*`value`* [#](#SQL-ALTERTABLE-PARMS-VALUE): O novo valor para um parâmetro de armazenamento de tabela. Isso pode ser um número ou uma palavra, dependendo do parâmetro.

*`parent_table`* [#](#SQL-ALTERTABLE-PARMS-PARENT-TABLE): Uma tabela pai para associar ou desassociar com esta tabela.

*`new_owner`* [#](#SQL-ALTERTABLE-PARMS-NEW-OWNER): O nome do usuário do novo proprietário da tabela.

*`new_access_method`* [#](#SQL-ALTERTABLE-PARMS-NEW-ACCESS-METHOD): O nome do método de acesso ao qual a tabela será convertida.

*`new_tablespace`* [#](#SQL-ALTERTABLE-PARMS-NEW-TABLESPACE): O nome do espaço de tabela para o qual a tabela será movida.

*`new_schema`* [#](#SQL-ALTERTABLE-PARMS-NEW-SCHEMA): O nome do esquema para o qual a tabela será movida.

*`partition_name`* [#](#SQL-ALTERTABLE-PARMS-PARTITION-NAME): O nome da tabela a ser anexada como uma nova partição ou a ser desvinculada desta tabela.

*`partition_bound_spec`* [#](#SQL-ALTERTABLE-PARMS-PARTITION-BOUND-SPEC): A especificação de limite de partição para uma nova partição. Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para mais detalhes sobre a sintaxe da mesma.

## Notas

A palavra-chave `COLUMN` é ruído e pode ser omitida.

Quando uma coluna é adicionada com `ADD COLUMN` e um `DEFAULT` não volátil é especificado, o valor padrão é avaliado no momento da declaração e o resultado é armazenado nos metadados da tabela, onde será retornado quando qualquer linha existente for acessada. O valor será aplicado apenas quando a tabela for reescrita, tornando o `ALTER TABLE` muito rápido, mesmo em tabelas grandes. Se nenhuma restrição de coluna for especificada, NULL é usado como o `DEFAULT`. Em nenhum dos casos, é necessária uma reescrita da tabela.

Adicionar uma coluna com um `DEFAULT` volátil (por exemplo, `clock_timestamp()`), uma coluna gerada armazenada, uma coluna de identidade ou uma coluna com um tipo de dados de domínio que tenha restrições fará com que toda a tabela e seus índices sejam reescritos. Adicionar uma coluna gerada virtual nunca requer uma reescrita.

Mudar o tipo de uma coluna existente normalmente fará com que toda a tabela e seus índices sejam reescritos. Como exceção, quando muda o tipo de uma coluna existente, se a cláusula `USING` não altera o conteúdo da coluna e o tipo antigo é binário coerível com o novo tipo ou um domínio não limitado sobre o novo tipo, não é necessária uma reescrita da tabela. No entanto, os índices ainda serão reconstruídos, a menos que o sistema possa verificar que o novo índice seria logicamente equivalente ao existente. Por exemplo, se a codificação de uma coluna foi alterada, é necessário reconstruir um índice porque o novo ordem de classificação pode ser diferente. No entanto, na ausência de uma alteração na codificação, uma coluna pode ser alterada de `text` para `varchar` (ou vice-versa) sem reconstruir os índices, porque esses tipos de dados são classificados de forma idêntica.

A reconstrução da tabela e/ou do índice pode levar um tempo significativo para uma tabela grande e, temporariamente, exigirá o dobro do espaço em disco.

A adição de uma restrição `CHECK` ou `NOT NULL` requer a digitalização da tabela para verificar se as linhas existentes atendem à restrição, mas não requer uma reescrita da tabela. Se uma restrição `CHECK` for adicionada como `NOT ENFORCED`, nenhuma verificação será realizada.

Da mesma forma, ao anexar uma nova partição, ela pode ser verificada para garantir que as linhas existentes atendam à restrição da partição.

A principal razão para fornecer a opção de especificar várias alterações em um único `ALTER TABLE` é que, dessa forma, várias varreduras ou reescritas de tabela podem ser combinadas em uma única passagem pela tabela.

Digitalizar uma tabela grande para verificar novas restrições de chave estrangeira, verificação ou não nulo pode levar muito tempo, e outras atualizações na tabela são bloqueadas até que o comando `ALTER TABLE ADD CONSTRAINT` seja comprometido. O principal propósito da opção de restrição `NOT VALID` é reduzir o impacto de adicionar uma restrição em atualizações concorrentes. Com `NOT VALID`, o comando `ADD CONSTRAINT` não digitaliza a tabela e pode ser comprometido imediatamente. Depois disso, um comando `VALIDATE CONSTRAINT` pode ser emitido para verificar se as linhas existentes satisfazem a restrição. A etapa de validação não precisa bloquear atualizações concorrentes, uma vez que sabe que outras transações estarão aplicando a restrição para as linhas que inserem ou atualizam; apenas as linhas pré-existentes precisam ser verificadas. Portanto, a validação adquire apenas um `SHARE UPDATE EXCLUSIVE` bloqueio na tabela que está sendo alterada. (Se a restrição for uma chave estrangeira, também é necessário um `ROW SHARE` bloqueio na tabela referenciada pela restrição.) Além de melhorar a concorrência, pode ser útil usar `NOT VALID` e `VALIDATE CONSTRAINT` em casos em que a tabela é conhecida por conter violações pré-existentes. Uma vez que a restrição esteja em vigor, nenhuma nova violação pode ser inserida, e os problemas existentes podem ser corrigidos ao gosto até que `VALIDATE CONSTRAINT` finalmente tenha sucesso.

O formulário `DROP COLUMN` não remove fisicamente a coluna, mas simplesmente a torna invisível para operações SQL. As operações subsequentes de inserção e atualização na tabela armazenarão um valor nulo para a coluna. Assim, descartar uma coluna é rápido, mas não reduzirá imediatamente o tamanho em disco da sua tabela, pois o espaço ocupado pela coluna descartada não é recuperado. O espaço será recuperado ao longo do tempo à medida que as linhas existentes são atualizadas.

Para forçar a recuperação imediata do espaço ocupado por uma coluna descartada, você pode executar uma das formas do `ALTER TABLE` que realiza uma reescrita de toda a tabela. Isso resulta na reconstrução de cada linha com a coluna descartada substituída por um valor nulo.

As formas de reescrita de `ALTER TABLE` não são seguras para MVCC. Após uma reescrita de tabela, a tabela parecerá vazia para transações concorrentes, se elas estiverem usando uma instantânea tirada antes da reescrita ter ocorrido. Veja [Seção 13.6][(mvcc-caveats.md "13.6. Caveats")] para mais detalhes.

A opção `USING` de `SET DATA TYPE` pode, na verdade, especificar qualquer expressão que envolva os valores antigos da linha; ou seja, pode se referir a outras colunas, bem como àquela que está sendo convertida. Isso permite que conversões muito gerais sejam feitas com a sintaxe `SET DATA TYPE`. Devido a essa flexibilidade, a expressão `USING` não é aplicada ao valor padrão da coluna (se houver); o resultado pode não ser uma expressão constante, conforme exigido para um padrão. Isso significa que, quando não há uma atribuição implícita ou de conversão de tipo de antigo para novo, `SET DATA TYPE` pode não converter o padrão, mesmo que uma cláusula `USING` seja fornecida. Nesses casos, descarte o padrão com `DROP DEFAULT`, realize o `ALTER TYPE`, e depois use `SET DEFAULT` para adicionar um novo padrão adequado. Considerações semelhantes se aplicam a índices e restrições que envolvem a coluna.

Se uma tabela tiver quaisquer tabelas descendentes, não é permitido adicionar, renomear ou alterar o tipo de uma coluna na tabela principal sem fazer o mesmo com os descendentes. Isso garante que os descendentes sempre tenham colunas que correspondem à principal. Da mesma forma, uma restrição `CHECK` não pode ser renomeada na principal sem também renomeá-la em todos os descendentes, para que as restrições `CHECK` também correspondam entre a principal e seus descendentes. (Essa restrição, no entanto, não se aplica a restrições baseadas em índice.) Além disso, porque selecionar a partir da principal também seleciona a partir de seus descendentes, uma restrição na principal não pode ser marcada como válida a menos que também seja marcada como válida para esses descendentes. Em todos esses casos, `ALTER TABLE ONLY` será rejeitada.

Uma operação recursiva `DROP COLUMN` removerá a coluna de uma tabela descendente apenas se o descendente não herdar essa coluna de quaisquer outros pais e nunca tiver uma definição independente da coluna. Um comando não recursivo `DROP COLUMN` (ou seja, `ALTER TABLE ONLY ... DROP COLUMN`) nunca remove quaisquer colunas descendentes, mas, em vez disso, as marca como independentemente definidas, em vez de herdadas. Um comando não recursivo `DROP COLUMN` falhará para uma tabela particionada, porque todas as partições de uma tabela devem ter as mesmas colunas que a raiz da partição.

As ações para colunas de identidade (`ADD GENERATED`, `SET` etc., `DROP IDENTITY`), bem como as ações `CLUSTER`, `OWNER` e `TABLESPACE` nunca recorrem a tabelas descendentes; ou seja, sempre agem como se `ONLY` fosse especificado. As ações que afetam os estados de gatilho recorrem a partições de tabelas particionadas (a menos que `ONLY` seja especificado), mas nunca a descendentes de herança tradicional. Adicionar uma restrição recorre apenas para restrições `CHECK` que não são marcadas `NO INHERIT`.

Não é permitido alterar qualquer parte de uma tabela de catálogo de sistema.

Consulte [CREATE TABLE](sql-createtable.md "CREATE TABLE") para uma descrição adicional dos parâmetros válidos. [Capítulo 5](ddl.md "Chapter 5. Data Definition") contém informações adicionais sobre herança.

## Exemplos

Para adicionar uma coluna do tipo `varchar` a uma tabela:

```
ALTER TABLE distributors ADD COLUMN address varchar(30);
```

Isso fará com que todas as linhas existentes na tabela sejam preenchidas com valores nulos para a nova coluna.

Para adicionar uma coluna com um valor padrão não nulo:

```
ALTER TABLE measurements
  ADD COLUMN mtime timestamp with time zone DEFAULT now();
```

As linhas existentes serão preenchidas com a hora atual como o valor da nova coluna, e, em seguida, as novas linhas receberão a hora de sua inserção.

Para adicionar uma coluna e preencher com um valor diferente do padrão que será usado mais tarde:

```
ALTER TABLE transactions
  ADD COLUMN status varchar(30) DEFAULT 'old',
  ALTER COLUMN status SET default 'current';
```

As linhas existentes serão preenchidas com `old`, mas, em seguida, o padrão para comandos subsequentes será `current`. Os efeitos são os mesmos como se os dois subcomandos tivessem sido emitidos em comandos separados `ALTER TABLE`.

Para excluir uma coluna de uma tabela:

```
ALTER TABLE distributors DROP COLUMN address RESTRICT;
```

Para alterar os tipos de duas colunas existentes em uma operação:

```
ALTER TABLE distributors
    ALTER COLUMN address TYPE varchar(80),
    ALTER COLUMN name TYPE varchar(100);
```

Para alterar uma coluna inteira contendo timestamps Unix para `timestamp with time zone` através de uma cláusula `USING`:

```
ALTER TABLE foo
    ALTER COLUMN foo_timestamp SET DATA TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second';
```

O mesmo, quando a coluna tem uma expressão padrão que não será automaticamente convertido para o novo tipo de dados:

```
ALTER TABLE foo
    ALTER COLUMN foo_timestamp DROP DEFAULT,
    ALTER COLUMN foo_timestamp TYPE timestamp with time zone
    USING
        timestamp with time zone 'epoch' + foo_timestamp * interval '1 second',
    ALTER COLUMN foo_timestamp SET DEFAULT now();
```

Para renomear uma coluna existente:

```
ALTER TABLE distributors RENAME COLUMN address TO city;
```

Para renomear uma tabela existente:

```
ALTER TABLE distributors RENAME TO suppliers;
```

Para renomear uma restrição existente:

```
ALTER TABLE distributors RENAME CONSTRAINT zipchk TO zip_check;
```

Para adicionar uma restrição de não nulo a uma coluna:

```
ALTER TABLE distributors ALTER COLUMN street SET NOT NULL;
```

Para remover uma restrição não nula de uma coluna:

```
ALTER TABLE distributors ALTER COLUMN street DROP NOT NULL;
```

Para adicionar uma restrição de verificação a uma tabela e todas as suas crianças:

```
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5);
```

Para adicionar uma restrição de verificação apenas a uma tabela e não às suas crianças:

```
ALTER TABLE distributors ADD CONSTRAINT zipchk CHECK (char_length(zipcode) = 5) NO INHERIT;
```

(A restrição de verificação também não será herdada por filhos futuros.)

Para remover uma restrição de verificação de uma tabela e todas as suas crianças:

```
ALTER TABLE distributors DROP CONSTRAINT zipchk;
```

Para remover uma restrição de verificação de uma única tabela:

```
ALTER TABLE ONLY distributors DROP CONSTRAINT zipchk;
```

(A restrição de verificação permanece em vigor para quaisquer tabelas filhas.)

Para adicionar uma restrição de chave estrangeira a uma tabela:

```
ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address);
```

Para adicionar uma restrição de chave estrangeira a uma tabela com o menor impacto em outros trabalhos:

```
ALTER TABLE distributors ADD CONSTRAINT distfk FOREIGN KEY (address) REFERENCES addresses (address) NOT VALID;
ALTER TABLE distributors VALIDATE CONSTRAINT distfk;
```

Para adicionar uma restrição (multicolumn) única a uma tabela:

```
ALTER TABLE distributors ADD CONSTRAINT dist_id_zipcode_key UNIQUE (dist_id, zipcode);
```

Para adicionar uma restrição de chave primária com nome automático a uma tabela, observando que uma tabela só pode ter uma chave primária:

```
ALTER TABLE distributors ADD PRIMARY KEY (dist_id);
```

Para mover uma tabela para um espaço de tabelas diferente:

```
ALTER TABLE distributors SET TABLESPACE fasttablespace;
```

Para mover uma tabela para um esquema diferente:

```
ALTER TABLE myschema.distributors SET SCHEMA yourschema;
```

Para recriar uma restrição de chave primária, sem bloquear as atualizações enquanto o índice é reconstruído:

```
CREATE UNIQUE INDEX CONCURRENTLY dist_id_temp_idx ON distributors (dist_id);
ALTER TABLE distributors DROP CONSTRAINT distributors_pkey,
    ADD CONSTRAINT distributors_pkey PRIMARY KEY USING INDEX dist_id_temp_idx;
```

Para anexar uma partição a uma tabela com partição por intervalo:

```
ALTER TABLE measurement
    ATTACH PARTITION measurement_y2016m07 FOR VALUES FROM ('2016-07-01') TO ('2016-08-01');
```

Para anexar uma partição a uma tabela com partição de lista:

```
ALTER TABLE cities
    ATTACH PARTITION cities_ab FOR VALUES IN ('a', 'b');
```

Para anexar uma partição a uma tabela com partição de hash:

```
ALTER TABLE orders
    ATTACH PARTITION orders_p4 FOR VALUES WITH (MODULUS 4, REMAINDER 3);
```

Para associar uma partição padrão a uma tabela particionada:

```
ALTER TABLE cities
    ATTACH PARTITION cities_partdef DEFAULT;
```

Para desvincular uma partição de uma tabela particionada:

```
ALTER TABLE measurement
    DETACH PARTITION measurement_y2015m12;
```

## Compatibilidade

Os formulários `ADD [COLUMN]`, `DROP [COLUMN]`, `DROP IDENTITY`, `RESTART`, `SET DEFAULT`, `SET DATA TYPE` (sem `USING`, `SET GENERATED` e `SET sequence_option`) estão em conformidade com o padrão SQL. O formulário `ADD table_constraint` está em conformidade com o padrão SQL quando as cláusulas `USING INDEX` e `NOT VALID` são omitidas e o tipo de restrição é um dos `CHECK`, `UNIQUE`, `PRIMARY KEY` ou `REFERENCES`. Os outros formulários são extensões do padrão SQL do PostgreSQL. Além disso, a capacidade de especificar mais de uma manipulação em um único comando `ALTER TABLE` é uma extensão.

`ALTER TABLE DROP COLUMN` pode ser usado para descartar a única coluna de uma tabela, deixando uma tabela de coluna zero. Esta é uma extensão do SQL, que não permite tabelas de coluna zero.

## Veja também

[Crie uma tabela](sql-createtable.md "CREATE TABLE")