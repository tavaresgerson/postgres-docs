## COMEÇAR

COMEÇAR — iniciar um bloco de transação

## Sinopse

```
BEGIN [ WORK | TRANSACTION ] [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

## Descrição

`BEGIN` inicia um bloco de transação, ou seja, todas as declarações após um comando `BEGIN` serão executadas em uma única transação até que um [`COMMIT`](sql-commit.md "COMMIT") ou [`ROLLBACK`](sql-rollback.md "ROLLBACK") explícito seja dado. Por padrão (sem `BEGIN`), o PostgreSQL executa transações no modo “autocommit”, ou seja, cada declaração é executada em sua própria transação e um commit é implicitamente realizado no final da declaração (se a execução foi bem-sucedida, caso contrário, um rollback é feito).

As declarações são executadas mais rapidamente em um bloco de transação, porque o início/commit da transação requer uma atividade significativa de CPU e disco. A execução de múltiplas declarações dentro de uma transação também é útil para garantir a consistência ao fazer várias alterações relacionadas: outras sessões não poderão ver os estados intermediários em que nem todas as atualizações relacionadas foram feitas.

Se o nível de isolamento, o modo de leitura/escrita ou o modo diferível for especificado, a nova transação terá essas características, como se `SET TRANSACTION` (sql-set-transaction.md "SET TRANSACTION") tivesse sido executado.

## Parâmetros

`WORK` `TRANSACTION`: Palavras-chave opcionais. Elas não têm efeito.

Consulte [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para obter informações sobre o significado dos outros parâmetros desta declaração.

## Notas

`START TRANSACTION`](sql-start-transaction.md "START TRANSACTION") tem a mesma funcionalidade que `BEGIN`.

Utilize `COMMIT`(sql-commit.md "COMMIT") ou `ROLLBACK`(sql-rollback.md "ROLLBACK") para encerrar um bloco de transação.

A emissão de `BEGIN` quando já estiver dentro de um bloco de transação provocará uma mensagem de alerta. O estado da transação não será afetado. Para aninhar transações dentro de um bloco de transação, use pontos de salvamento (consulte [SAVEPOINT](sql-savepoint.md "SAVEPOINT")).

Por razões de compatibilidade reversa, as vírgulas entre os *`transaction_modes`* consecutivos podem ser omitidas.

## Exemplos

Para iniciar um bloco de transação:

```
BEGIN;
```

## Compatibilidade

`BEGIN` é uma extensão de linguagem do PostgreSQL. É equivalente ao comando padrão SQL `START TRANSACTION`(sql-start-transaction.md "START TRANSACTION"), cuja página de referência contém informações adicionais sobre compatibilidade.

O `DEFERRABLE` *`transaction_mode`* é uma extensão de linguagem do PostgreSQL.

Aliás, a palavra-chave `BEGIN` é usada para um propósito diferente em SQL embutido. É aconselhável ter cuidado com a semântica da transação ao transferir aplicativos de banco de dados.

## Veja também

[COMMIT](sql-commit.md "COMMIT"), [ROLLBACK](sql-rollback.md "ROLLBACK"), [START TRANSACTION](sql-start-transaction.md "START TRANSACTION"), [SAVEPOINT](sql-savepoint.md "SAVEPOINT")