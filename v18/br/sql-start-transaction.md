## COMEÇAR A TRANSAÇÃO

INICIAR TRANSAÇÃO — iniciar um bloco de transação

## Sinopse

```
START TRANSACTION [ transaction_mode [, ...] ]

where transaction_mode is one of:

    ISOLATION LEVEL { SERIALIZABLE | REPEATABLE READ | READ COMMITTED | READ UNCOMMITTED }
    READ WRITE | READ ONLY
    [ NOT ] DEFERRABLE
```

## Descrição

Este comando inicia um novo bloco de transação. Se o nível de isolamento, o modo de leitura/escrita ou o modo diferível for especificado, a nova transação terá essas características, como se `SET TRANSACTION` (sql-set-transaction.md "SET TRANSACTION") tivesse sido executado. Isso é o mesmo que o comando `BEGIN` (sql-begin.md "BEGIN").

## Parâmetros

Consulte [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION") para obter informações sobre o significado dos parâmetros desta declaração.

## Compatibilidade

No padrão, não é necessário emitir `START TRANSACTION` para iniciar um bloco de transação: qualquer comando SQL implicitamente inicia um bloco. O comportamento do PostgreSQL pode ser visto como emitir implicitamente um `COMMIT` após cada comando que não segue `START TRANSACTION` (ou `BEGIN`), e, portanto, é frequentemente chamado de “autocommit”. Outros sistemas de banco de dados relacionais podem oferecer um recurso de autocommit como uma conveniência.

O `DEFERRABLE` *`transaction_mode`* é uma extensão de linguagem do PostgreSQL.

O padrão SQL exige vírgulas entre os sucessivos *`transaction_modes`*, mas, por razões históricas, o PostgreSQL permite que as vírgulas sejam omitidas.

Veja também a seção de compatibilidade de [SET TRANSACTION](sql-set-transaction.md "SET TRANSACTION").

## Veja também

[INÍCIO](sql-begin.md "BEGIN"), [COMITAMENTO](sql-commit.md "COMMIT"), [RETRAÇÃO](sql-rollback.md "ROLLBACK"), [PUNTO DE RETIRO](sql-savepoint.md "SAVEPOINT"), [DEFINIÇÃO DE TRANSAÇÃO](sql-set-transaction.md "SET TRANSACTION")