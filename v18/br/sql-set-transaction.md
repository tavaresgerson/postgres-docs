## SET TRANSACTION

SET TRANSACTION — define as características da transação atual

## Sinopse

```
SET TRANSACTION transaction_mode [, ...]
SET TRANSACTION SNAPSHOT snapshot_id
SET SESSION CHARACTERISTICS AS TRANSACTION transaction_mode [, ...]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

## Descrição

O comando `SET TRANSACTION` define as características da transação atual. Não tem efeito em quaisquer transações subsequentes. `SET SESSION CHARACTERISTICS` define as características de transação padrão para transações subsequentes de uma sessão. Esses padrões podem ser ignorados pelo `SET TRANSACTION` para uma transação individual.

As características disponíveis das transações são o nível de isolamento da transação, o modo de acesso à transação (leitura/escrita ou apenas leitura) e o modo diferível. Além disso, uma instantânea pode ser selecionada, embora apenas para a transação atual, não como padrão de sessão.

O nível de isolamento de uma transação determina quais dados a transação pode ver quando outras transações estão sendo executadas simultaneamente:

`READ COMMITTED`: Uma declaração só pode ver linhas comprometidas antes de ela começar. Esse é o padrão.

`REPEATABLE READ`: Todas as declarações da transação atual só podem ver linhas comprometidas antes da primeira consulta ou declaração de modificação de dados ter sido executada nesta transação.

`SERIALIZABLE`: Todas as declarações da transação atual só podem ver linhas comprometidas antes da primeira consulta ou declaração de modificação de dados ter sido executada nesta transação. Se um padrão de leituras e escritas entre transações concorrentes serializáveis criasse uma situação que não poderia ter ocorrido para qualquer execução serial (uma de cada vez) dessas transações, uma delas será revertida com um erro `serialization_failure`.

O padrão SQL define um nível adicional, `READ UNCOMMITTED`. No PostgreSQL, `READ UNCOMMITTED` é tratado como `READ COMMITTED`.

O nível de isolamento de transação não pode ser alterado após a execução da primeira consulta ou declaração de modificação de dados (`SELECT`, `INSERT`, `DELETE`, `UPDATE`, `MERGE`, `FETCH`, ou `COPY`) de uma transação. Consulte o [Capítulo 13](mvcc.md "Chapter 13. Concurrency Control") para obter mais informações sobre isolamento de transação e controle de concorrência.

O modo de acesso à transação determina se a transação é de leitura/escrita ou apenas de leitura. Leitura/escrita é o padrão. Quando uma transação é apenas de leitura, os seguintes comandos SQL são desaconselhados: `INSERT`, `UPDATE`, `DELETE`, `MERGE` e `COPY FROM`, se a tabela para a qual ela seria escrita não for uma tabela temporária; todos os comandos `CREATE`, `ALTER` e `DROP`; `COMMENT`, `GRANT`, `REVOKE`, `TRUNCATE`; e `EXPLAIN ANALYZE` e `EXECUTE`, se o comando que seria executado estiver entre os listados. Essa é uma noção de apenas leitura de alto nível que não impede todas as escritas no disco.

A propriedade de transação `DEFERRABLE` não tem efeito a menos que a transação também seja `SERIALIZABLE` e `READ ONLY`. Quando todas essas três propriedades são selecionadas para uma transação, a transação pode bloquear quando adquirir seu instantâneo pela primeira vez, após o que ela é capaz de executar sem o overhead normal de uma transação `SERIALIZABLE` e sem qualquer risco de contribuir para ou ser cancelada por uma falha de serialização. Esse modo é bem adequado para relatórios ou backups de longa duração.

O comando `SET TRANSACTION SNAPSHOT` permite que uma nova transação seja executada com o mesmo *snapshot* que uma transação existente. A transação pré-existente deve ter exportado seu snapshot com a função `pg_export_snapshot` (consulte [Seção 9.28.5](functions-admin.md#FUNCTIONS-SNAPSHOT-SYNCHRONIZATION)). Essa função retorna um identificador de snapshot, que deve ser fornecido ao `SET TRANSACTION SNAPSHOT` para especificar qual snapshot deve ser importado. O identificador deve ser escrito como uma literal de string neste comando, por exemplo, `'00000003-0000001B-1'`. O `SET TRANSACTION SNAPSHOT` só pode ser executado no início de uma transação, antes da primeira consulta ou declaração de modificação de dados (`SELECT`, `INSERT`, `DELETE`, `UPDATE`, `MERGE`, `FETCH` ou `COPY`) da transação. Além disso, a transação deve já estar definida no nível de isolamento `SERIALIZABLE` ou `REPEATABLE READ` (caso contrário, o snapshot seria descartado imediatamente, uma vez que o modo `READ COMMITTED` gera um novo snapshot para cada comando). Se a transação que importa o snapshot usa o nível de isolamento `SERIALIZABLE`, então a transação que exportou o snapshot também deve usar esse nível de isolamento. Além disso, uma transação serializável não-somente-leia não pode importar um snapshot de uma transação somente-leia.

## Notas

Se `SET TRANSACTION` for executado sem um `START TRANSACTION` ou `BEGIN` prévio, ele emite um aviso e, caso contrário, não tem efeito.

É possível dispensar `SET TRANSACTION` especificando, em vez disso, o *`transaction_modes`* desejado em `BEGIN` ou `START TRANSACTION`. Mas essa opção não está disponível para `SET TRANSACTION SNAPSHOT`.

Os modos de transação padrão da sessão também podem ser definidos ou examinados através dos parâmetros de configuração [default_transaction_isolation](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-ISOLATION), [default_transaction_read_only](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-READ-ONLY) e [default_transaction_deferrable](runtime-config-client.md#GUC-DEFAULT-TRANSACTION-DEFERRABLE). (Na verdade, `SET SESSION CHARACTERISTICS` é apenas um equivalente verbose para definir essas variáveis com `SET`.). Isso significa que os padrões podem ser definidos no arquivo de configuração, via `ALTER DATABASE`, etc. Consulte o [Capítulo 19](runtime-config.md "Chapter 19. Server Configuration") para mais informações.

Os modos das transações atuais podem ser configurados ou examinados de maneira semelhante pelos parâmetros de configuração [transaction_isolation](runtime-config-client.md#GUC-TRANSACTION-ISOLATION), [transaction_read_only](runtime-config-client.md#GUC-TRANSACTION-READ-ONLY) e [transaction_deferrable](runtime-config-client.md#GUC-TRANSACTION-DEFERRABLE). Configurar um desses parâmetros tem o mesmo efeito que a opção correspondente `SET TRANSACTION`, com as mesmas restrições sobre quando pode ser feito. No entanto, esses parâmetros não podem ser configurados no arquivo de configuração ou a partir de qualquer fonte que não seja o SQL ao vivo.

## Exemplos

Para iniciar uma nova transação com o mesmo instantâneo de uma transação já existente, primeiro exporte o instantâneo da transação existente. Isso retornará o identificador do instantâneo, por exemplo:

```
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SELECT pg_export_snapshot();
 pg_export_snapshot
---------------------
 00000003-0000001B-1
(1 row)
```

Em seguida, forneça o identificador do instantâneo em um comando `SET TRANSACTION SNAPSHOT` no início da transação recém-aberta:

```
BEGIN TRANSACTION ISOLATION LEVEL REPEATABLE READ;
SET TRANSACTION SNAPSHOT '00000003-0000001B-1';
```

## Compatibilidade

Esses comandos são definidos no padrão SQL, exceto pelo modo de transação `DEFERRABLE` e o formulário `SET TRANSACTION SNAPSHOT`, que são extensões do PostgreSQL.

`SERIALIZABLE` é o nível de isolamento de transação padrão no padrão. No PostgreSQL, o padrão é normalmente `READ COMMITTED`, mas você pode alterá-lo conforme mencionado acima.

No padrão SQL, há outra característica de transação que pode ser definida com esses comandos: o tamanho da área de diagnóstico. Esse conceito é específico para SQL embutido e, portanto, não é implementado no servidor PostgreSQL.

O padrão SQL exige vírgulas entre os sucessivos *`transaction_modes`*, mas, por razões históricas, o PostgreSQL permite que as vírgulas sejam omitidas.